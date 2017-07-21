.. _cmake_reference:


CMake
=====

Invoke `cmake` explicitly with the helper ``command_line`` and ``build_config`` attributes:

.. code-block:: python

   def build(self):
      cmake = CMake(self)
      self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
      self.run('cmake --build . %s' % cmake.build_config)


Using the helper methods:


.. code-block:: python

   def build(self):
      cmake = CMake(self)
      cmake.configure(source_dir=self.conanfile_directory, build_dir="./")
      cmake.build()
      cmake.install()




Constructor
-----------

CMake(conanfile, generator=None, cmake_system_name=True, parallel=True)

- **conanfile**: Conanfile object. Usually ``self`` in a conanfile.py
- **generator**: Specify a custom generator instead of autodetect it. e.j: "MinGW Makefiles"
- **cmake_system_name**: Specify a custom value for ``CMAKE_SYSTEM_NAME`` instead of autodetect it.
- **paralell**: If true, will append the `-jN` attribute for parallel building being N the :ref:`cpu_count()<cpu_count>`



Attributes
----------

- **command_line** (read only): Generator, conan definitions and flags that reflects the specified Conan settings.

.. code-block:: text

     -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release ... -DCONAN_C_FLAGS=-m64 -Wno-dev

- **build_config** (read only): Value for ``--config`` option for Multi-configuration IDEs.

.. code-block:: text

    --config Release


- **definitions**: The CMake helper will automatically append some definitions based on your settings:

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

  But you can change the automatic definitions after the ``CMake()`` object creation using the ``definitions`` property:

.. code-block:: python

   def build(self):
      cmake = CMake(self)
      cmake.definitions["CMAKE_SYSTEM_NAME"] = "Generic"
      cmake.configure()
      cmake.build()
      cmake.install() # Build --target=install


Methods
-------

- **configure** (args=None, defs=None, source_dir=None, build_dir=None)

    - **args**: A list of additional arguments to be passed to the ``cmake`` command. Each argument will be escaped according to the current shell. No extra arguments will be added if ``args=None``
    - **defs**: A dict that will be converted to a list of CMake command line variable definitions of the form ``-DKEY=VALUE``. Each value will be escaped according to the current shell and can be either ``str``, ``bool`` or of numeric type
    - **source_dir**: CMake's source directory where ``CMakeLists.txt`` is located. The default value is ``conan_file.conanfile_directory`` if ``None`` is specified. Relative paths are allowed and will be relative to ``build_dir``
    - **build_dir**: CMake's output directory. The default value is ``conan_file.conanfile_directory`` if ``None`` is specified. The ``CMake`` object will store ``build_dir`` internally for subsequent calls to ``build()``

- **build** (args=None, build_dir=None, target=None)

    - **args**: A list of additional arguments to be passed to the ``cmake`` command. Each argument will be escaped according to the current shell. No extra arguments will be added if ``args=None``
    - **build_dir**: CMake's output directory. If ``None`` is specified the ``build_dir`` from ``configure()`` will be used. ``conan_file.conanfile_directory`` is used if ``configure()`` has not been called
    - **target**: Specifies the target to execute. The default *all* target will be built if ``None`` is specified. ``"install"`` can be used to relocate files to aid packaging

- **install** (args=None, build_dir=None, target=None)

    - **args**: A list of additional arguments to be passed to the ``cmake`` command. Each argument will be escaped according to the current shell. No extra arguments will be added if ``args=None``
    - **build_dir**: CMake's output directory. If ``None`` is specified the ``build_dir`` from ``configure()`` will be used. ``conan_file.conanfile_directory`` is used if ``configure()`` has not been called
