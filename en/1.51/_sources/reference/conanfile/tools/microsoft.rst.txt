.. _conan_tools_microsoft:


conan.tools.microsoft
=====================

These tools allow a native integration for Microsoft Visual Studio, natively (without using CMake,
but using directly Visual Studio solutions, projects and property files).

.. warning::

    These tools are still **experimental** (so subject to breaking changes) but with very stable syntax.
    We encourage the usage of it to be prepared for Conan 2.0.

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

    from conan import ConanFile
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

The above files are generated when the package doesn't have components. If the package has defined components, the following files
will be generated:

- *conan_pkgname_compname_vars_release_x64.props*: Definition of variables for the component ``compname`` of the package ``pkgname``
- *conan_pkgname_compname_release_x64.props*: Activation of the above variables into VS effective variables to be used in the build
- *conan_pkgname_compname.props*: Properties file for component ``compname`` of package ``pkgname``. It conditionally includes, depending on the configuration,
  the specific activation property files.
- *conan_pkgname.props*: Properties file for package ``pkgname``. It includes and aggregates all the components of the package.
- *conandeps.props*: Same as above, aggregates all the direct dependencies property files for the packages (like ``conan_pkgname.props``)


You will be adding the *conandeps.props* to your solution project files if you want to depend on all the declared
dependencies. For single project solutions, this is probably the way to go. For multi-project solutions, you might
be more efficient and add properties files per project. You could add *conan_zlib.props* properties to "project1"
in the solution and *conan_bzip2.props* to "project2" in the solution for example. If the package has components, you
can also add to your solution the specific components you depend on, and not all of them.

Custom configurations
+++++++++++++++++++++

If your Visual Studio project defines custom configurations, like ``ReleaseShared``, or ``MyCustomConfig``,
it is possible to define it into the ``MSBuildDeps`` generator, so different project configurations can
use different set of dependencies. Let's say that our current project can be built as a shared library,
with the custom configuration ``ReleaseShared``, and the package also controls this with the ``shared``
option:

.. code-block:: python

    from conan import ConanFile
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
  host context: all regular ``requires``, plus the ``tool_requires`` that are in the host context,
  for example test frameworks as ``gtest`` or ``catch``.
- All transitive ``requires`` of those direct dependencies (all in the host context)
- Tool requires, in the build context, that is, application and executables that run in the build
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

    from conan import ConanFile
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

conf
++++

``MSBuildToolchain`` is affected by these :ref:`[conf]<global_conf>` variables:

- ``tools.microsoft.msbuildtoolchain:compile_options`` dict-like object of extra compile options to be added to ``<ClCompile>`` section.
  The dict will be translated as follows: ``<[KEY]>[VALUE]</[KEY]>``.
- ``tools.build:cxxflags`` list of extra C++ flags that will be appended to ``<AdditionalOptions>`` section from ``<ClCompile>`` and ``<ResourceCompile>`` one.
- ``tools.build:cflags`` list of extra of pure C flags that will be appended to ``<AdditionalOptions>`` section from ``<ClCompile>`` and ``<ResourceCompile>`` one.
- ``tools.build:sharedlinkflags`` list of extra linker flags that will be appended to ``<AdditionalOptions>`` section from ``<Link>`` one.
- ``tools.build:exelinkflags`` list of extra linker flags that will be appended to ``<AdditionalOptions>`` section from ``<Link>`` one.
- ``tools.build:defines`` list of preprocessor definitions that will be appended to ``<PreprocessorDefinitions>`` section from ``<ResourceCompile>`` one.


MSBuild
-------

The ``MSBuild`` build helper is a wrapper around the command line invocation of MSBuild. It will abstract the
calls like ``msbuild "MyProject.sln" /p:Configuration=<conf> /p:Platform=<platform>`` into Python method calls.

The ``MSBuild`` helper can be used like:

.. code:: python

    from conan import ConanFile
    from conan.tools.microsoft import MSBuild

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def build(self):
            msbuild = MSBuild(self)
            msbuild.build("MyProject.sln")

The ``MSBuild.build()`` method internally implements a call to ``msbuild`` like:

.. code:: bash

    $ <vcvars-cmd> && msbuild "MyProject.sln" /p:Configuration=<configuration> /p:Platform=<platform>

Where:

- ``vcvars-cmd`` is calling the Visual Studio prompt that matches the current recipe ``settings``
- ``configuration``, typically Release, Debug, which will be obtained from ``settings.build_type``
  but this will be configurable with ``msbuild.build_type``.
- ``platform`` is the architecture, a mapping from the ``settings.arch`` to the common 'x86', 'x64', 'ARM', 'ARM64'.
  This is configurable with ``msbuild.platform``.


attributes
++++++++++

You can customize the following attributes in case you need to change them:

- **build_type** (default ``settings.build_type``): Value for the ``/p:Configuration``.
- **platform** (default based on ``settings.arch`` to select one of these values: (``'x86', 'x64', 'ARM', 'ARM64'``):
  Value for the ``/p:Platform``.

Example:

.. code:: python

    from conan import ConanFile
    from conan.tools.microsoft import MSBuild

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def build(self):
            msbuild = MSBuild(self)
            msbuild.build_type = "MyRelease"
            msbuild.platform = "MyPlatform"
            msbuild.build("MyProject.sln")


conf
++++

``MSBuild`` is affected by these :ref:`[conf]<global_conf>` variables:

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

    from conan import ConanFile
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


conan.tools.microsoft.is_msvc()
-------------------------------

.. code-block:: python

    def is_msvc(conanfile):

Validate ``self.settings.compiler`` for which compiler is being used.
It returns ``True`` when the host compiler is ``Visual Studio`` or ``msvc``, otherwise, returns ``False``.
When the ``compiler`` is empty, it returns ``False``.

Parameters:

- **conanfile**: ConanFile instance.

.. code-block:: python

    from conan.tools.microsoft import is_msvc

    def validate(self):
        if not is_msvc(self):
            raise ConanInvalidConfiguration("Only supported by Visual Studio and msvc.")


conan.tools.microsoft.is_msvc_static_runtime()
----------------------------------------------

.. code-block:: python

    def is_msvc_static_runtime(conanfile):

Validate ``self.settings.compiler.runtime`` for which compiler is being used.
It returns ``True`` when the host compiler is ``Visual Studio`` or ``msvc``, and its runtime is ``MT``, ``MTd`` or ``static``.
When the ``compiler`` is empty, it returns ``False``.

Parameters:

- **conanfile**: ConanFile instance.


.. code-block:: python

    from conan.tools.microsoft import is_msvc_static_runtime

    def validate(self):
        if is_msvc_static_runtime(self) and self.options.shared(self):
            raise ConanInvalidConfiguration("This project does not support shared and static runtime together.")


.. _conan_tools_microsoft_msvc_runtime_flag:

conan.tools.microsoft.msvc_runtime_flag()
-----------------------------------------

.. code-block:: python

    def msvc_runtime_flag(conanfile):

If the current compiler is ``Visual Studio``, ``msvc``, ``clang `` or ``intel-cc``, then
detects the runtime type and returns between ``MD``, ``MT``, ``MDd`` or ``MTd``,
otherwise, returns ``""`` (empty string). When the runtime type is ``static``, it returns
``MT``, otherwise, ``MD``. The suffix ``d`` is added when running on Debug mode.

Parameters:

- **conanfile**: Conanfile instance.

.. code-block:: python

    from conan.tools.microsoft import msvc_runtime_flag

    def validate(self):
         if "MT" in msvc_runtime_flag(self):
            self.output.warning("Runtime MT/MTd is not well tested.")



conan.tools.microsoft.unix_path()
---------------------------------

.. code-block:: python

    def unix_path(conanfile, path):

Transforms the specified path into the correct one according to the subsystem.
To determine the subsystem:

   - The ``settings_build.os`` is checked to verify that we are running on "Windows" otherwise, the path is returned
     without changes.

   - If ``settings_build.os.subsystem`` is specified (meaning we are running Conan under that subsystem) it will be
     returned.

   - If ``conanfile.win_bash==True`` (meaning we have to run the commands inside the subsystem), the conf
     ``tools.microsoft.bash:subsystem`` has to be declared or it will raise an Exception.

   - Otherwise the path is returned without changes.

Parameters:

- **conanfile**: ConanFile instance.

.. code-block:: python

    from conan.tools.microsoft import unix_path



    def build(self):
        adjusted_path = unix_path(self, "C:\\path\\to\\stuff")


In the example above, ``adjusted_path`` will be:
    - ``/c/path/to/stuff`` if msys2 or msys
    - ``/cygdrive/c/path/to/stuff`` if cygwin
    - ``/mnt/c/path/to/stuff`` if wsl
    - ``/dev/fs/C/path/to/stuff`` if sfu


check_min_vs()
--------------

Helper method to allow the migration to 2.0 more easily. It will handle internally both ``Visual Studio``
and ``msvc`` compiler settings, raising a ``ConanInvalidConfiguration`` error if the minimum version
is not satisfied


.. code-block:: python

    def check_min_vs(conanfile, version):


- ``conanfile``: Always use ``self``, the current recipe
- ``version``: Minimum version that will be accepted. Use a version number following the MSVC compiler version (or ``msvc`` setting),
  that is, ``191``, ``192``, etc (updates like ``193.1`` are also acceptable)


Example:

.. code-block:: python

    def validate(self):
        check_min_vs(self, "192")
