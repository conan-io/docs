conan.tools.microsoft
=====================

These tools allow a native integration for Microsoft Visual Studio, natively (without using CMake,
but using directly Visual Studio solutions, projects and property files).

.. warning::

    These tools are **experimental** and subject to breaking changes.

MSBuildDeps
-----------

The ``MSBuildDeps`` is the dependency information generator for Microsoft MSBuild build system.
It will generate multiple *xxxx.props* properties files one per dependency of a package,
to be used by consumers using MSBuild or Visual Studio, just adding the generated properties files
to the solution and projects.

It is important to highlight that this one is a **dependencies generator** and it is focused
on the **dependencies** of a conanfile, not the current build.

The ``MSBuildDeps`` generator can be used by name in conanfiles:

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):
        generators = "MSBuildDeps"

.. code-block:: text
    :caption: conanfile.txt

    [generators]
    MSBuildDeps

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code-block:: python
    :caption: conanfile.py

    from conans import ConanFile
    from conan.tools.microsoft import MSBuildDeps

    class Pkg(ConanFile):
        settings = "os", "compiler", "arch", "build_type"
        requires = "zlib/1.2.11", "bzip2/1.0.8"

        def generate(self):
            ms = MSBuildDeps(self)
            ms.generate()

When the ``MSBuildDeps`` generator is used, every invocation of ``conan install`` will
generate properties files, one per dependency and per configuration. For the last *conanfile.py*
above:

.. code-block:: bash

    $ conan install conanfile.py # default is Release
    $ conan install conanfile.py -s build_type=Debug

This is a multi-configuration generator, and will generate different files for the different Debug/Release
configuration. The above commands the following files will be generated:

- *conan_zlib_release_x64.props*: Properties file for the ``zlib`` dependency, Release config
- *conan_zlib_debug_x64.props*: Properties file for the ``zlib`` dependency, Debug config
- *conan_zlib.props*: Properties file for ``zlib``. It conditionally includes, depending on the configuration,
  one of the above Release/Debug properties files.
- Same 3 files will be generated for every dependency in the graph, in this case ``conan_bzip.props`` too, which
  will conditionally include the Release/Debug bzip properties files.
- *conan_deps.props*: Properties files including all direct dependencies, in this case, it includes ``conan_zlib.props``
  and ``conan_bzip2.props``

You will be adding the *conan_deps.props* to your solution project files if you want to depend on all the declared
dependencies. For single project solutions, this is probably the way to go. For multi-project solutions, you might
be more efficient and add properties files per project. You could add *conan_zlib.props* properties to "project1"
in the solution and *conan_bzip2.props* to "project2" in the solution for example.

Custom configurations
+++++++++++++++++++++

If your Visual Studio project defines custom configurations, like ``ReleaseShared``, or ``MyCustomConfig``,
it is possible to define it into the ``MSBuildDeps`` generator, so different project configurations can
use different set of dependencies. Let's say that our current project can be built as a shared library,
with the custom configuration ``ReleaseShared``, and the package also controls this with the ``shared``
option:

.. code-block:: python

    from conans import ConanFile
    from conan.tools.microsoft import MSBuildDeps

    class Pkg(ConanFile):
        settings = "os", "compiler", "arch", "build_type"
        options = {"shared": [True, False]}
        default_options = {"shared": False}
        requires = "zlib/1.2.11"

        def generate(self):
            ms = MSBuildDeps(self)
            # We assume that -o *:shared=True is used to install all shared deps too
            if self.options.shared:
                ms.configuration = str(self.settings.build_type) + "Shared"
            ms.generate()

This will manage to generate new properties files for this custom configuration, and switching it
in the IDE allows to be switching dependencies configuration like Debug/Release, it could be also
switching dependencies from static to shared libraries.


MSBuildToolchain
----------------

The ``MSBuildToolchain`` is the toolchain generator for MSBuild. It will generate MSBuild properties files
that can be added to the Visual Studio solution projects. This generator translates
the current package configuration, settings, and options, into MSBuild properties files syntax.

The ``MSBuildToolchain`` generator can be used by name in conanfiles:

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):
        generators = "MSBuildToolchain"

.. code-block:: text
    :caption: conanfile.txt

    [generators]
    MSBuildToolchain

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code:: python

    from conans import ConanFile
    from conan.tools.microsoft import MSBuildToolchain

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = MSBuildToolchain(self)
            tc.generate()


The ``MSBuildToolchain`` will generate two files after a ``conan install`` command:

.. code-block:: bash

    $ conan install conanfile.py # default is Release
    $ conan install conanfile.py -s build_type=Debug


- The main *conantoolchain.props* file, to be added to the project.
- A *conantoolchain_<config>.props* file, that will be conditionally included from the previous
  *conantoolchain.props* file based on the configuration and platform, e.g.:
  *conantoolchain_release_x86.props*

Every invocation to ``conan install`` with different configuration will create a new properties ``.props``
file, that will also be conditionally included. This allows to install different configurations,
then switch among them directly from the Visual Studio IDE.

The MSBuildToolchain files can configure:

- The Visual Studio runtime (MT/MD/MTd/MDd), obtained from Conan input settings
- The C++ standard, obtained from Conan input settings

One of the advantages of using toolchains is that they can help to achieve the exact same build
with local development flows, than when the package is created in the cache.


MSBuild
-------

The ``MSBuild`` build helper is a wrapper around the command line invocation of MSBuild. It will abstract the
calls like ``msbuild "MyProject.sln" /p:Configuration=<conf> /p:Platform=<platform>`` into Python method calls.

The ``MSBuild`` helper can be used like:

.. code:: python

    from conans import conanfile
    from conan.tools.microsoft import MSBuild

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def build(self):
            msbuild = MSBuild(self)
            msbuild.build("MyProject.sln")

The ``MSBuild.build()`` method internally implements a call to ``msbuild`` like:

.. code:: bash

    $ <vcvars-cmd> && msbuild "MyProject.sln" /p:Configuration=<conf> /p:Platform=<platform>

Where:

- ``vcvars-cmd`` is calling the Visual Studio prompt that matches the current recipe ``settings``
- ``conf`` is the configuration, typically Release, Debug, which will be obtained from ``settings.build_type``
  but this will be configurable. Please open a `Github issue <https://github.com/conan-io/conan/issues>`_ if you want to define custom configurations.
- ``platform`` is the architecture, a mapping from the ``settings.arch`` to the common 'x86', 'x64', 'ARM', 'ARM64'.
  If your platform is unsupported, please report in `Github issues <https://github.com/conan-io/conan/issues>`_ as well:
