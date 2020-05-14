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
                     parallel=True, build_type=None, toolset=None)

Parameters:
    - **conanfile** (Required): Conanfile object. Usually ``self`` in a conanfile.py
    - **generator** (Optional, Defaulted to ``None``): Specify a custom generator instead of autodetect it. e.j: "MinGW Makefiles"
    - **cmake_system_name** (Optional, Defaulted to ``True``): Specify a custom value for ``CMAKE_SYSTEM_NAME`` instead of autodetect it.
    - **parallel** (Optional, Defaulted to ``True``): If ``True``, will append the `-jN` attribute for parallel building being N the :ref:`cpu_count()<cpu_count>`.
    - **build_type** (Optional, Defaulted to ``None``): Force the build type to be declared in ``CMAKE_BUILD_TYPE``. If you set this parameter the build type
      not will be taken from the settings.
    - **toolset** (Optional, Defaulted to ``None``): Specify a toolset for Visual Studio.

Attributes
----------

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


command_line (read only)
++++++++++++++++++++++++

Generator, conan definitions and flags that reflects the specified Conan settings.

.. code-block:: text

    -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release ... -DCONAN_C_FLAGS=-m64 -Wno-dev

build_config (read only)
++++++++++++++++++++++++

Value for ``--config`` option for Multi-configuration IDEs.

.. code-block:: text

    --config Release

definitions
+++++++++++

The CMake helper will automatically append some definitions based on your settings:

+-------------------------------------------+--------------------------------------------------------------------------+
| Variable                                  | Description                                                              |
+===========================================+==========================================================================+
| CMAKE_BUILD_TYPE                          |  Debug or Release (from self.settings.build_type)                        |
+-------------------------------------------+--------------------------------------------------------------------------+
| CMAKE_OSX_ARCHITECTURES                   |  "i386" if architecture is x86 in an OSX system                          |
+-------------------------------------------+--------------------------------------------------------------------------+
| BUILD_SHARED_LIBS                         |  Only If your conanfile has a "shared" option                            |
+-------------------------------------------+--------------------------------------------------------------------------+
| CONAN_COMPILER                            |  Conan internal variable to check compiler                               |
+-------------------------------------------+--------------------------------------------------------------------------+
| CMAKE_SYSTEM_NAME                         |  If detected cross building it's set to self.settings.os                 |
+-------------------------------------------+--------------------------------------------------------------------------+
| CMAKE_SYSTEM_VERSION                      |  If detected cross building it's set to the self.settings.os_version     |
+-------------------------------------------+--------------------------------------------------------------------------+
| CMAKE_ANDROID_ARCH_ABI                    |  If detected cross building to Android                                   |
+-------------------------------------------+--------------------------------------------------------------------------+
| CONAN_LIBCXX                              |  from self.settings.compiler.libcxx                                      |
+-------------------------------------------+--------------------------------------------------------------------------+
| CONAN_CMAKE_SYSTEM_PROCESSOR              |  Definition only set if same environment variable is declared by user    |
+-------------------------------------------+--------------------------------------------------------------------------+
| CONAN_CMAKE_FIND_ROOT_PATH                |  Definition only set if same environment variable is declared by user    |
+-------------------------------------------+--------------------------------------------------------------------------+
| CONAN_CMAKE_FIND_ROOT_PATH_MODE_PROGRAM   |  Definition only set if same environment variable is declared by user    |
+-------------------------------------------+--------------------------------------------------------------------------+
| CONAN_CMAKE_FIND_ROOT_PATH_MODE_LIBRARY   |  Definition only set if same environment variable is declared by user    |
+-------------------------------------------+--------------------------------------------------------------------------+
| CONAN_CMAKE_FIND_ROOT_PATH_MODE_INCLUDE   |  Definition only set if same environment variable is declared by user    |
+-------------------------------------------+--------------------------------------------------------------------------+
| CONAN_SHARED_LINKER_FLAGS                 |  -m32 and -m64 based on your architecture                                |
+-------------------------------------------+--------------------------------------------------------------------------+
| CONAN_C_FLAGS                             |  -m32 and -m64 based on your architecture and /MP for MSVS               |
+-------------------------------------------+--------------------------------------------------------------------------+
| CONAN_C_FLAGS                             |  -m32 and -m64 based on your architecture and /MP for MSVS               |
+-------------------------------------------+--------------------------------------------------------------------------+
| CONAN_LINK_RUNTIME                        |  Runtime from self.settings.compiler.runtime for MSVS                    |
+-------------------------------------------+--------------------------------------------------------------------------+
| CONAN_CMAKE_CXX_STANDARD                  |  From setting ``cppstd``                                                 |
+-------------------------------------------+--------------------------------------------------------------------------+
| CONAN_CMAKE_CXX_EXTENSIONS                |  From setting ``cppstd``, when GNU extensions are enabled                |
+-------------------------------------------+--------------------------------------------------------------------------+
| CONAN_STD_CXX_FLAG                        |  From setting ``cppstd``. Flag for compiler directly (for CMake < 3.1)   |
+-------------------------------------------+--------------------------------------------------------------------------+



But you can change the automatic definitions after the ``CMake()`` object creation using the ``definitions`` property:

.. code-block:: python

    from conans import ConanFile, CMake

    class ExampleConan(ConanFile):
        ...

        def build(self):
            cmake = CMake(self)
            cmake.definitions["CMAKE_SYSTEM_NAME"] = "Generic"
            cmake.configure()
            cmake.build()
            cmake.install() # Build --target=install


Methods
-------

configure()
+++++++++++

.. code-block:: python

    def configure(self, args=None, defs=None, source_folder=None, build_folder=None,
                  cache_build_folder=None)

Configures `CMake` project with the given parameters.

Parameters:
    - **args** (Optional, Defaulted to ``None``): A list of additional arguments to be passed to the ``cmake`` command. Each argument will be escaped according to the current shell. No extra arguments will be added if ``args=None``
    - **definitions** (Optional, Defaulted to ``None``): A dict that will be converted to a list of CMake command line variable definitions of the form ``-DKEY=VALUE``. Each value will be escaped according to the current shell and can be either ``str``, ``bool`` or of numeric type
    - **source_folder**: CMake's source directory where ``CMakeLists.txt`` is located. The default value is the ``self.source_folder``.
      Relative paths are allowed and will be relative to ``self.source_folder``.
    - **build_folder**: CMake's output directory. The default value is the ``self.build_folder`` if ``None`` is specified.
      The ``CMake`` object will store ``build_folder`` internally for subsequent calls to ``build()``.
    - **cache_build_folder** (Optional, Defaulted to ``None``): Use the given subfolder as build folder when building the package in the local cache.
      This argument doesn't have effect when the package is being built in user folder with :command:`conan build` but overrides **build_folder** when working in the local cache.
      See :ref:`self.in_local_cache<in_local_cache>`.

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

    def test(args=None, build_dir=None, target=None)

Build `CMake` test target (could be RUN_TESTS in multi-config projects or ``test`` in single-config projects), which usually means building and running unit tests

Parameters:
    - **args** (Optional, Defaulted to ``None``): A list of additional arguments to be passed to the ``cmake`` command. Each argument will be escaped according to the current shell. No extra arguments will be added if ``args=None``.
    - **build_dir** (Optional, Defaulted to ``None``): CMake's output directory. If ``None`` is specified the ``build_folder`` from ``configure()`` will be used.
    - **target** (Optional, default to ``None``). Alternative target name for running the tests. If not defined RUN_TESTS or ``test`` will be used


install()
+++++++++

.. code-block:: python

    def install(args=None, build_dir=None)

Installs `CMake` project with the given parameters.

Parameters:
    - **args** (Optional, Defaulted to ``None``): A list of additional arguments to be passed to the ``cmake`` command. Each argument will be escaped according to the current shell. No extra arguments will be added if ``args=None``.
    - **build_dir** (Optional, Defaulted to ``None``): CMake's output directory. If ``None`` is specified the ``build_folder`` from ``configure()`` will be used.


patch_config_paths() [EXPERIMENTAL]
+++++++++++++++++++++++++++++++++++

.. code-block:: python

    def patch_config_paths()


This method changes references to the absolute path of the installed package in exported CMake config files to the appropriate Conan
variable. This makes most CMake config files portable.

For example, if a package foo installs a file called *fooConfig.cmake* to be used by cmake's ``find_package()`` method, normally this file
will contain absolute paths to the installed package folder, for example it will contain a line such as:

.. code-block:: text

    SET(Foo_INSTALL_DIR /home/developer/.conan/data/Foo/1.0.0/...)

This will cause cmake's ``find_package()`` method to fail when someone else installs the package via Conan. This function will replace such
paths to:

.. code-block:: text

    SET(Foo_INSTALL_DIR ${CONAN_FOO_ROOT})

Which is a variable that is set by *conanbuildinfo.cmake*, so that ``find_package()`` now correctly works on this Conan package.

If the ``install()`` method of the CMake object in the conanfile is used, this function should be called **after** that invocation. For
example:

.. code-block:: python

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.install()
        cmake.patch_config_paths()

Environment variables
---------------------

There are some environment variables that will also affect the ``CMake()`` helper class. Check them in the
:ref:`CMAKE RELATED VARIABLES<cmake_related_variables>` section.
