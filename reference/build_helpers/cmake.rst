.. _cmake_reference:


CMake
=====

Invoke `cmake` explicitly with the helper ``command_line`` and ``build_config`` attributes:

.. code-block:: python

   def build(self):
      cmake = CMake(self.settings)
      self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
      self.run('cmake --build . %s' % cmake.build_config)


Using the helper methods:


.. code-block:: python

   def build(self):
      cmake = CMake(self.settings)
      cmake.configure(self, source_dir=self.conanfile_directory, build_dir="./")
      cmake.build(self)


Constructor
-----------

CMake(settings, generator=None, cmake_system_name=True, parallel=True)

- **settings**: Settings object. Usually ``self.settings`` in a conanfile.py
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


Methods
-------

- **configure** (conan_file, args=None, defs=None, source_dir=None, build_dir=None)

    - **conan_file**: The ConanFile to use and read settings from. Typically ``self`` is passed
    - **args**: A list of additional arguments to be passed to the ``cmake`` command. Each argument will be escaped according to the current shell. No extra arguments will be added if ``args=None``
    - **defs**: A dict that will be converted to a list of CMake command line variable definitions of the form ``-DKEY=VALUE``. Each value will be escaped according to the current shell and can be either ``str``, ``bool`` or of numeric type
    - **source_dir**: CMake's source directory where ``CMakeLists.txt`` is located. The default value is ``conan_file.conanfile_directory`` if ``None`` is specified. Relative paths are allowed and will be relative to ``build_dir``
    - **build_dir**: CMake's output directory. The default value is ``conan_file.conanfile_directory`` if ``None`` is specified. The ``CMake`` object will store ``build_dir`` internally for subsequent calls to ``build()``

- **build** (conan_file, args=None, build_dir=None, target=None)

    - **conan_file**: The ``ConanFile`` to use and read settings from. Typically ``self`` is passed
    - **args**: A list of additional arguments to be passed to the ``cmake`` command. Each argument will be escaped according to the current shell. No extra arguments will be added if ``args=None``
    - **build_dir**: CMake's output directory. If ``None`` is specified the ``build_dir`` from ``configure()`` will be used. ``conan_file.conanfile_directory`` is used if ``configure()`` has not been called
    - **target**: Specifies the target to execute. The default *all* target will be built if ``None`` is specified. ``"install"`` can be used to relocate files to aid packaging


