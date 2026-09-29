.. _cmake_reference:

CMake
=====

The `CMake` class helps us to invoke `cmake` command with the generator, flags and definitions, reflecting the specified Conan settings.

There are two ways to invoke your cmake tools:

- Using the helper attributes ``cmake.command_line`` and ``cmake.build_config``:

.. code-block:: python

   from conans import ConanFile, CMake

    class ExampleConan(ConanFile):
        ...

        def build(self):
            cmake = CMake(self)
            self.run('cmake "%s" %s' % (self.source_folder, cmake.command_line))
            self.run('cmake --build . %s' % cmake.build_config)
            self.run('cmake --build . --target install')

- Using the helper methods:

.. code-block:: python

    from conans import ConanFile, CMake

    class ExampleConan(ConanFile):
        ...

        def build(self):
            cmake = CMake(self)
            # same as cmake.configure(source_folder=self.source_folder, build_folder=self.build_folder)
            cmake.configure()
            cmake.build()
            cmake.test() # Build the "RUN_TESTS" or "test" target
            # Build the "install" target, defining CMAKE_INSTALL_PREFIX to self.package_folder
            cmake.install()


Constructor
-----------

.. code-block:: python

    class CMake(object):

        def __init__(self, conanfile, generator=None, cmake_system_name=True,
                     parallel=True, build_type=None, toolset=None, make_program=None,
                     set_cmake_flags=False, msbuild_verbosity=None, cmake_program=None,
                     generator_platform=None)

Parameters:
    - **conanfile** (Required): Conanfile object. Usually ``self`` in a *conanfile.py*
    - **generator** (Optional, Defaulted to ``None``): Specify a custom generator instead of autodetect it. e.g., "MinGW Makefiles"
    - **cmake_system_name** (Optional, Defaulted to ``True``): Specify a custom value for ``CMAKE_SYSTEM_NAME`` instead of autodetect it.
    - **parallel** (Optional, Defaulted to ``True``): If ``True``, will append the `-jN` attribute for parallel building being N the :ref:`cpu_count()<tools_cpu_count>`.
      Also applies to parallel test execution (by defining ``CTEST_PARALLEL_LEVEL`` environment variable).
    - **build_type** (Optional, Defaulted to ``None``): Force the build type instead of taking the value from the settings. Note this will
      also make the ``CMAKE_BUILD_TYPE`` to be declared for multi configuration generators.
    - **toolset** (Optional, Defaulted to ``None``): Specify a toolset for Visual Studio.
    - **make_program** (Optional, Defaulted to ``None``): Indicate path to ``make``.
    - **set_cmake_flags** (Optional, Defaulted to ``None``): Whether or not to set CMake flags like ``CMAKE_CXX_FLAGS``, ``CMAKE_C_FLAGS``, etc.
    - **msbuild_verbosity** (Optional, Defaulted to ``None``): verbosity level for MSBuild (in case of Visual Studio generator).
    - **cmake_program** (Optional, Defaulted to ``None``): Path to the custom cmake executable.
    - **generator_platform** (Optional, Defaulted to ``None``): Generator platform name or none to autodetect (-A cmake option).

Attributes
----------

generator
+++++++++

Specifies a custom CMake generator to use, see also `cmake-generators documentation <https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html>`_.

generator_platform
++++++++++++++++++

Specifies a custom CMake generator platform to use, see also `CMAKE_GENERATOR_PLATFORM documentation <https://cmake.org/cmake/help/latest/variable/CMAKE_GENERATOR_PLATFORM.html>`_.

verbose
+++++++

**Defaulted to**: ``False``

Set it to ``True`` or ``False`` to automatically set the definition ``CMAKE_VERBOSE_MAKEFILE``.

.. code-block:: python

    from conans import ConanFile, CMake

    class ExampleConan(ConanFile):
        ...

        def build(self):
            cmake = CMake(self)
            cmake.verbose = True
            cmake.configure()
            cmake.build()


build_folder (Read only)
++++++++++++++++++++++++

Build folder where the ``configure()`` and ``build()`` methods will be called.

build_type [Deprecated]
+++++++++++++++++++++++

Build type can be forced with this variable instead of taking it from the settings.

flags (Read only)
+++++++++++++++++

Flag conversion of ``definitions`` to be used in the command line invocation (``-D``).

is_multi_configuration (Read only)
++++++++++++++++++++++++++++++++++

Indicates whether the generator selected allows builds with multi configuration: Release, Debug...
Multi configuration generators are Visual Studio and Xcode ones.

command_line (Read only)
++++++++++++++++++++++++

Arguments and flags calculated by the build helper that will be applied. It indicates the generator, the Conan definitions and the flags
converted from the specified Conan settings. For example:

.. code-block:: bash

    -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release ... -DCONAN_C_FLAGS=-m64 -Wno-dev

build_config (Read only)
++++++++++++++++++++++++

Value for :command:`--config` option for Multi-configuration IDEs. This flag will only be set if the generator ``is_multi_configuration``
and ``build_type`` was not forced in constructor class.

An example of the value of this property could be:

.. code-block:: bash

    --config Release

parallel
++++++++

**Defaulted to**: ``True``

Run CMake process in parallel for compilation, installation and testing. This is translated into the proper command line argument:
For ``Unix Makefiles`` it is ``-jX`` and for ``Visual Studio`` it is ``/m:X``.

However, the parallel executing can be changed for testing like this:

.. code-block:: python

    cmake = CMake(self)
    cmake.configure()
    cmake.build()  # 'parallel' is enabled by default
    cmake.parallel = False
    cmake.test()

In the case of ``cmake.test()`` this flag sets the ``CTEST_PARALLEL_LEVEL`` variable to the according value in :ref:`tools_cpu_count`.

definitions
+++++++++++

The CMake helper will automatically append some definitions based on your settings:

+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| Variable                                  | Description                                                                                                                  |
+===========================================+==============================================================================================================================+
| CMAKE_BUILD_TYPE                          | Debug, Release... from ``self.settings.build_type`` or ``build_type`` attribute **only** if ``is_multi_configuration``       |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| CMAKE_OSX_ARCHITECTURES                   | ``i386`` if architecture is x86 in an OSX system                                                                             |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| BUILD_SHARED_LIBS                         | Only if your recipe has a ``shared`` option                                                                                  |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| CONAN_COMPILER                            | Conan internal variable to check the compiler                                                                                |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| CMAKE_SYSTEM_NAME                         | Set to ``self.settings.os`` value if cross-building is detected                                                              |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| CMAKE_SYSTEM_VERSION                      | Set to ``self.settings.os_version`` value if cross-building is detected                                                      |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| CMAKE_ANDROID_ARCH_ABI                    | Set to a suitable value if cross-building to an Android is detected                                                          |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| CONAN_LIBCXX                              | Set to ``self.settings.compiler.libcxx`` value                                                                               |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| CONAN_CMAKE_SYSTEM_PROCESSOR              | Definition set only if same environment variable is declared by user                                                         |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| CONAN_CMAKE_FIND_ROOT_PATH                | Definition set only if same environment variable is declared by user                                                         |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| CONAN_CMAKE_FIND_ROOT_PATH_MODE_PROGRAM   | Definition set only if same environment variable is declared by user                                                         |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| CONAN_CMAKE_FIND_ROOT_PATH_MODE_LIBRARY   | Definition set only if same environment variable is declared by user                                                         |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| CONAN_CMAKE_FIND_ROOT_PATH_MODE_INCLUDE   | Definition set only if same environment variable is declared by user                                                         |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| CONAN_CMAKE_POSITION_INDEPENDENT_CODE     | Set when ``fPIC`` option exists and ``True`` or ``fPIC`` exists and ``False`` but ``shared`` option exists and ``True``      |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| CONAN_SHARED_LINKER_FLAGS                 | Set to ``-m32`` or ``-m64`` values based on the architecture                                                                 |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| CONAN_C_FLAGS                             | Set to ``-m32`` or ``-m64`` values based on the architecture and ``/MP`` for MSVS                                            |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| CONAN_CXX_FLAGS                           | Set to ``-m32`` or ``-m64`` values based on the architecture and ``/MP`` for MSVS                                            |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| CONAN_LINK_RUNTIME                        | Set to the runtime value from ``self.settings.compiler.runtime`` for MSVS                                                    |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| CONAN_CMAKE_CXX_STANDARD                  | Set to the ``self.settings.compiler.cppstd`` value (or ``self.settings.cppstd`` for backward compatibility)                  |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| CONAN_CMAKE_CXX_EXTENSIONS                | Set to ``ON`` or ``OFF`` value when GNU extensions for the given C++ standard are enabled                                    |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| CONAN_STD_CXX_FLAG                        | Set to the flag corresponding to the C++ standard defined in ``self.settings.compiler.cppstd``. Used for CMake < 3.1)        |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| CMAKE_EXPORT_NO_PACKAGE_REGISTRY          | Defined by default to disable the package registry                                                                           |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| CONAN_IN_LOCAL_CACHE                      | ``ON`` if the build runs in local cache, ``OFF`` if running in a user folder                                                 |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+
| CONAN_EXPORTED                            | Defined when CMake is called using Conan CMake helper                                                                        |
+-------------------------------------------+------------------------------------------------------------------------------------------------------------------------------+

There are some definitions set to be used later on the the ``install()`` step too:

+-----------------------------+---------------------------------------------+
| Variable                    | Description                                 |
+=============================+=============================================+
| CMAKE_INSTALL_PREFIX        | Set to ``conanfile.package_folder`` value.  |
+-----------------------------+---------------------------------------------+
| CMAKE_INSTALL_BINDIR        | Set to *bin* inside the package folder.     |
+-----------------------------+---------------------------------------------+
| CMAKE_INSTALL_SBINDIR       | Set to *bin* inside the package folder.     |
+-----------------------------+---------------------------------------------+
| CMAKE_INSTALL_LIBEXECDIR    | Set to *bin* inside the package folder.     |
+-----------------------------+---------------------------------------------+
| CMAKE_INSTALL_LIBDIR        | Set to *lib* inside the package folder.     |
+-----------------------------+---------------------------------------------+
| CMAKE_INSTALL_INCLUDEDIR    | Set to *include* inside the package folder. |
+-----------------------------+---------------------------------------------+
| CMAKE_INSTALL_OLDINCLUDEDIR | Set to *include* inside the package folder. |
+-----------------------------+---------------------------------------------+
| CMAKE_INSTALL_DATAROOTDIR   | Set to *share* inside the package folder.   |
+-----------------------------+---------------------------------------------+

But you can change the automatic definitions after the ``CMake()`` object creation using the ``definitions`` property or even add your own
ones:

.. code-block:: python

    from conans import ConanFile, CMake

    class ExampleConan(ConanFile):
        ...

        def build(self):
            cmake = CMake(self)
            cmake.definitions["CMAKE_SYSTEM_NAME"] = "Generic"
            cmake.definitions["MY_CUSTOM_DEFINITION"] = True
            cmake.configure()
            cmake.build()
            cmake.install()  # Build --target=install

Note that definitions changed **after** the ``configure()`` call will **not** take effect later on the ``build()``, ``test()`` or
``install()`` ones.

Methods
-------

configure()
+++++++++++

.. code-block:: python

    def configure(self, args=None, defs=None, source_dir=None, build_dir=None,
                  source_folder=None, build_folder=None, cache_build_folder=None,
                  pkg_config_paths=None)

Configures `CMake` project with the given parameters.

Parameters:
    - **args** (Optional, Defaulted to ``None``): A list of additional arguments to be passed to the ``cmake`` command. Each argument will be escaped according to the current shell. No extra arguments will be added if ``args=None``
    - **defs** (Optional, Defaulted to ``None``): A dict that will be converted to a list of CMake command line variable definitions of the form ``-DKEY=VALUE``. Each value will be escaped according to the current shell and can be either ``str``, ``bool`` or of numeric type
    - **source_dir** (Optional, Defaulted to ``None``): **[DEPRECATED]** Use ``source_folder`` instead. CMake's source directory where
      *CMakeLists.txt* is located. The default value is the ``build`` folder if ``None`` is specified (or the ``source`` folder if
      ``no_copy_source`` is specified). Relative paths are allowed and will be relative to ``build_folder``.
    - **build_dir** (Optional, Defaulted to ``None``): **[DEPRECATED]** Use ``build_folder`` instead. CMake's output directory. The
      default value is the package ``build`` root folder if ``None`` is specified. The ``CMake`` object will store ``build_folder``
      internally for subsequent calls to ``build()``.
    - **source_folder**: CMake's source directory where ``CMakeLists.txt`` is located. The default value is the ``self.source_folder``.
      Relative paths are allowed and will be relative to ``self.source_folder``.
    - **build_folder**: CMake's output directory. The default value is the ``self.build_folder`` if ``None`` is specified.
      The ``CMake`` object will store ``build_folder`` internally for subsequent calls to ``build()``.
    - **cache_build_folder** (Optional, Defaulted to ``None``): Use the given subfolder as build folder when building the package in the local cache.
      This argument doesn't have effect when the package is being built in user folder with :command:`conan build` but overrides **build_folder** when working in the local cache.
      See :ref:`self.in_local_cache<in_local_cache>`.
    - **pkg_config_paths** (Optional, Defaulted to ``None``): Specify folders (in a list) of relative paths to the install folder or
      absolute ones where to find ``*.pc`` files (by using the env var ``PKG_CONFIG_PATH``). If ``None`` is specified but the conanfile
      is using the ``pkg_config`` generator, the ``self.install_folder`` will be added to the ``PKG_CONFIG_PATH`` in order to locate the
      pc files of the requirements of the conanfile.

build()
+++++++

.. code-block:: python

    def build(self, args=None, build_dir=None, target=None)

Builds `CMake` project with the given parameters.

Parameters:
    - **args** (Optional, Defaulted to ``None``): A list of additional arguments to be passed to the ``cmake`` command. Each argument will be escaped according to the current shell. No extra arguments will be added if ``args=None``
    - **build_dir** (Optional, Defaulted to ``None``): CMake's output directory. If ``None`` is specified the ``build_dir`` from ``configure()`` will be used.
    - **target** (Optional, Defaulted to ``None``): Specifies the target to execute. The default *all* target will be built if ``None`` is specified. ``"install"`` can be used to relocate files to aid packaging.

test()
++++++

.. code-block:: python

    def test(args=None, build_dir=None, target=None, output_on_failure=False)

Build `CMake` test target (could be RUN_TESTS in multi-config projects or ``test`` in single-config projects), which usually means building and running unit tests

Parameters:
    - **args** (Optional, Defaulted to ``None``): A list of additional arguments to be passed to the ``cmake`` command. Each argument will be escaped according to the current shell. No extra arguments will be added if ``args=None``.
    - **build_dir** (Optional, Defaulted to ``None``): CMake's output directory. If ``None`` is specified the ``build_folder`` from ``configure()`` will be used.
    - **target** (Optional, default to ``None``). Alternative target name for running the tests. If not defined RUN_TESTS or ``test`` will be used.
    - **output_on_failure** (Optional, default to ``False``). Enables ctest to show output of failed tests by defining ``CTEST_OUTPUT_ON_FAILURE`` environment variable (same effect as ``ctest --output-on-failure``).

install()
+++++++++

.. code-block:: python

    def install(args=None, build_dir=None)

Installs `CMake` project with the given parameters.

Parameters:
    - **args** (Optional, Defaulted to ``None``): A list of additional arguments to be passed to the ``cmake`` command. Each argument will be escaped according to the current shell. No extra arguments will be added if ``args=None``.
    - **build_dir** (Optional, Defaulted to ``None``): CMake's output directory. If ``None`` is specified the ``build_folder`` from ``configure()`` will be used.


.. _patch_config_paths:


patch_config_paths() [EXPERIMENTAL]
+++++++++++++++++++++++++++++++++++

.. code-block:: python

    def patch_config_paths()

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

This method changes references to the absolute path of the installed package in exported CMake config files to the appropriate Conan
variable. Method also changes references to other packages installation paths in export CMake config files to Conan variable
with their installation roots.
This makes most CMake config files portable.

For example, if a package foo installs a file called *fooConfig.cmake* to be used by cmake's ``find_package()`` method, normally this file
will contain absolute paths to the installed package folder, for example it will contain a line such as:

.. code-block:: text

    SET(Foo_INSTALL_DIR /home/developer/.conan/data/Foo/1.0.0/...)

This will cause cmake's ``find_package()`` method to fail when someone else installs the package via Conan. This function will replace such
paths to:

.. code-block:: text

    SET(Foo_INSTALL_DIR ${CONAN_FOO_ROOT})

Which is a variable that is set by *conanbuildinfo.cmake*, so that ``find_package()`` now correctly works on this Conan package.

For dependent packages method replaces lines with references to dependencies installation paths such as:

.. code-block:: text

    SET_TARGET_PROPERTIES(foo PROPERTIES INTERFACE_INCLUDE_DIRECTORIES "/home/developer/.conan/data/Bar/1.0.0/user/channel/id/include")

to following lines:

.. code-block:: text

    SET_TARGET_PROPERTIES(foo PROPERTIES INTERFACE_INCLUDE_DIRECTORIES "${CONAN_BAR_ROOT}/include")

If the ``install()`` method of the CMake object in the conanfile is used, this function should be called **after** that invocation. For
example:

.. code-block:: python

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()
        cmake.patch_config_paths()

get_version()
+++++++++++++

.. code-block:: python

    @staticmethod
    def get_version()

Returns the CMake version in a ``conans.model.Version`` object as it is evaluated by the
command line. Will raise if cannot resolve it to valid version.

Environment variables
---------------------

There are some environment variables that will also affect the ``CMake()`` helper class. Check them in the
:ref:`CMAKE RELATED VARIABLES<cmake_related_variables>` section.

Example
-------
The following example of ``conanfile.py`` shows you how to manage a project with conan and CMake.

.. code-block:: python

    from conans import ConanFile, CMake

    class SomePackage(ConanFile):
        name = "SomePackage"
        version = "1.0.0"
        settings = "os", "compiler", "build_type", "arch"
        generators = "cmake"

    def configure_cmake(self):
        cmake = CMake(self)

        # put definitions here so that they are re-used in cmake between
        # build() and package()
        cmake.definitions["SOME_DEFINITION_NAME"] = "On"

        cmake.configure()
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

        # run unit tests after the build
        cmake.test()

        # run custom make command
        self.run("make -j3 check)

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

Default used generators
-----------------------

When a compiler or its version is not detected, the CMake helper uses a default generator based on the platform operating system.
For Unix systems it generates ``Unix Makefiles``. For Windows there is no default generator, it will be detected by CMake automatically.
