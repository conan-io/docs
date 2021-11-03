.. _conan_tools_microsoft:


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

.. important::

    This class will require very soon to define both the "host" and "build" profiles. It is very recommended to
    start defining both profiles immediately to avoid future breaking. Furthermore, some features, like trying to
    cross-compile might not work at all if the "build" profile is not provided.


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

- *conan_zlib_vars_release_x64.props*: ``Conanzlibxxxx`` variables definitions for the ``zlib`` dependency, Release config, like ``ConanzlibIncludeDirs``, ``ConanzlibLibs``, etc.
- *conan_zlib_vars_debug_x64.props*: Same ``Conanzlib``variables for ``zlib`` dependency, Debug config
- *conan_zlib_release_x64.props*: Activation of ``Conanzlibxxxx`` variables in the current build as standard C/C++ build configuration, Release config. This file contains also the transitive dependencies definitions.
- *conan_zlib_debug_x64.props*: Same activation of ``Conanzlibxxxx`` variables, Debug config, also inclusion of transitive dependencies.
- *conan_zlib.props*: Properties file for ``zlib``. It conditionally includes, depending on the configuration,
  one of the two immediately above Release/Debug properties files.
- Same 5 files will be generated for every dependency in the graph, in this case ``conan_bzip.props`` too, which
  will conditionally include the Release/Debug bzip properties files.
- *conandeps.props*: Properties files including all direct dependencies, in this case, it includes ``conan_zlib.props``
  and ``conan_bzip2.props``

You will be adding the *conandeps.props* to your solution project files if you want to depend on all the declared
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

Included dependencies
+++++++++++++++++++++

``MSBuildDeps`` uses the new experimental ``self.dependencies`` access to dependencies. The following
dependencies will be translated to properties files:

- All direct dependencies, that is, the ones declared by the current ``conanfile``, that lives in the
  host context: all regular ``requires``, plus the ``build_requires`` that are in the host context,
  for example test frameworks as ``gtest`` or ``catch``.
- All transitive ``requires`` of those direct dependencies (all in the host context)
- Build requires, in the build context, that is, application and executables that run in the build
  machine irrespective of the destination platform, are added exclusively to the ``<ExecutablePath>``
  property, taking the value from ``$(Conan{{name}}BinaryDirectories)`` defined properties. This
  allows to define custom build commands, invoke code generation tools, with the ``<CustomBuild>`` and
  ``<Command>`` elements.


MSBuildToolchain
----------------

The ``MSBuildToolchain`` is the toolchain generator for MSBuild. It will generate MSBuild properties files
that can be added to the Visual Studio solution projects. This generator translates
the current package configuration, settings, and options, into MSBuild properties files syntax.

.. important::

    This class will require very soon to define both the "host" and "build" profiles. It is very recommended to
    start defining both profiles immediately to avoid future breaking. Furthermore, some features, like trying to
    cross-compile might not work at all if the "build" profile is not provided.


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


The ``MSBuildToolchain`` will generate three files after a ``conan install`` command:

.. code-block:: bash

    $ conan install conanfile.py # default is Release
    $ conan install conanfile.py -s build_type=Debug


- The main *conantoolchain.props* file, to be added to the project.
- A *conantoolchain_<config>.props* file, that will be conditionally included from the previous
  *conantoolchain.props* file based on the configuration and platform, e.g.:
  *conantoolchain_release_x86.props*
- A *conanvcvars.bat* file with the necessary ``vcvars`` invocation to define the build environment if necessary
  to build from the command line or from automated tools (might not be necessary if opening the IDE). This file
  will be automatically called by the ``tools.microsoft.MSBuild`` helper ``build()`` method.


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
  If your platform is unsupported, please report in `Github issues <https://github.com/conan-io/conan/issues>`_ as well.


conf
++++

- ``tools.microsoft.msbuild:verbosity`` will accept one of ``"Quiet", "Minimal", "Normal", "Detailed", "Diagnostic"`` to be passed
  to the ``MSBuild.build()`` call as ``msbuild .... /verbosity:XXX``



VCVars
------

Generates a file called ``conanvcvars.bat`` that activate the Visual Studio developer command prompt according
to the current settings by wrapping the `vcvarsall <https://docs.microsoft.com/en-us/cpp/build/building-on-the-command-line?view=vs-2017>`_
Microsoft bash script.


The ``VCVars`` generator can be used by name in conanfiles:

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):
        generators = "VCVars"

.. code-block:: text
    :caption: conanfile.txt

    [generators]
    VCVars

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code-block:: python
    :caption: conanfile.py

    from conans import ConanFile
    from conan.tools.microsoft import VCVars

    class Pkg(ConanFile):
        settings = "os", "compiler", "arch", "build_type"
        requires = "zlib/1.2.11", "bzip2/1.0.8"

        def generate(self):
            ms = VCVars(self)
            ms.generate()

Constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile):

- ``conanfile``: the current recipe object. Always use ``self``.


generate()
++++++++++

.. code:: python

    def generate(self, scope="build"):

Parameters:

    * **scope** (Defaulted to ``"build"``): Add the launcher automatically to the ``conanbuild`` launcher. Read more
      in the :ref:`Environment documentation <conan_tools_env_environment_model>`.
