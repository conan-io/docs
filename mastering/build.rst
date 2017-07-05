Build helpers
=============

There are several helpers that can assist to automate the ``build()`` method for popular build systems:

.. _building_with_cmake:

CMake
-----

The `CMake` class help us to invoke `cmake` command with the generator, flags and definitions, reflecting the specified Conan settings.


There are two ways to invoke your cmake tools:

- Using the helper attributes ``cmake.command_line`` and ``cmake.build_config``:

.. code-block:: python

   def build(self):
      cmake = CMake(self)
      self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
      self.run('cmake --build . %s' % cmake.build_config)



- Using the helper methods:

.. code-block:: python

   def build(self):
      cmake = CMake(self)
      cmake.configure(source_dir=self.conanfile_directory, build_dir="./")
      cmake.build()



.. seealso:: Check the section :ref:`Reference/Build Helpers/CMake <cmake_reference>` to find out more.


.. _building_with_autotools:


Autotools: configure / make
---------------------------

If you are using **configure**/**make** you can use **AutoToolsBuildEnvironment** helper.
This helper sets ``LIBS``, ``LDFLAGS``, ``CFLAGS``, ``CXXFLAGS`` and ``CPPFLAGS`` environment variables based on your requirements.

It works using the :ref:`environment_append <environment_append_tool>` context manager applied to your **configure and make** commands:

.. code-block:: python
   :emphasize-lines: 13, 14
   
   from conans import ConanFile, AutoToolsBuildEnvironment

   class ExampleConan(ConanFile):
      settings = "os", "compiler", "build_type", "arch"
      requires = "Poco/1.7.8p3@pocoproject/stable"
      default_options = "Poco:shared=True", "OpenSSL:shared=True"
     
      def imports(self):
         self.copy("*.dll", dst="bin", src="bin")
         self.copy("*.dylib*", dst="bin", src="lib")
   
      def build(self):
         env_build = AutoToolsBuildEnvironment(self)
         with tools.environment_append(env_build.vars):
            self.run("./configure")
            self.run("make")


For Windows users:

    - It also works with **nmake**.
    - If you have ``MSYS2``/``MinGW`` installed and in the PATH you take advantage of the :ref:`tools.run_in_windows_bash_tool <run_in_windows_bash_tool>` command:


.. code-block:: python
   :emphasize-lines: 8, 9, 10, 11, 12, 21, 22

   from conans import ConanFile, AutoToolsBuildEnvironment

   class ExampleConan(ConanFile):
      settings = "os", "compiler", "build_type", "arch"
      requires = "Poco/1.7.8p3@pocoproject/stable"
      default_options = "Poco:shared=True", "OpenSSL:shared=True"

      def _run_cmd(self, command):
        if self.settings.os == "Windows":
            tools.run_in_windows_bash(self, command)
        else:
            self.run(command)

      def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")

      def build(self):
         env_build = AutoToolsBuildEnvironment(self)
         with tools.environment_append(env_build.vars):
            self._run_cmd("./configure")
            self._run_cmd("make")


You can change some variables like ``.fpic``, ``.libs``, ``.include_paths``, ``defines`` before accessing the ``vars`` to override
an automatic value or add new values:

.. code-block:: python
   :emphasize-lines: 8, 9, 10

   from conans import ConanFile, AutoToolsBuildEnvironment

   class ExampleConan(ConanFile):
      ...

      def build(self):
         env_build = AutoToolsBuildEnvironment(self)
         env_build.fpic = True
         env_build.libs.append("pthread")
         env_build.defines.append("NEW_DEFINE=23")

         with tools.environment_append(env_build.vars):
            self.run("./configure")
            self.run("make")



.. seealso:: Check the :ref:`Reference/Build Helpers/AutoToolsBuildEnvironment <autotools_reference>` to see the complete reference.



.. _building_with_visual_studio:

Visual Studio
---------------

You can invoke your Visual Studio compiler from command line using the ``VisualStudioBuildEnvironment`` and the
:ref:`vcvars_command tool <tools>`, that will point to your Visual Studio installation.


Example:

.. code-block:: python
   :emphasize-lines: 10, 11, 12

    from conans import ConanFile, VisualStudioBuildEnvironment, tools

    class ExampleConan(ConanFile):
      ...

      def build(self):
         if self.settings.compiler == "Visual Studio":
            env_build = VisualStudioBuildEnvironment(self)
            with tools.environment_append(env_build.vars):
                vcvars = tools.vcvars_command(self.settings)
                self.run('%s && cl /c /EHsc hello.cpp' % vcvars)
                self.run('%s && lib hello.obj -OUT:hello.lib' % vcvars

.. seealso:: Check the :ref:`Reference/Build Helpers/VisualStudioBuildEnvironment <visual_studio_build_environment>` to see the complete reference.


.. _building_with_gcc_clang:

GCC or Clang
---------------

You could use the **gcc** generator directly to build your source code.
It's valid to invoke both gcc and clang compilers.


.. code-block:: python
   :emphasize-lines: 15

   from conans import ConanFile

   class PocoTimerConan(ConanFile):
      settings = "os", "compiler", "build_type", "arch"
      requires = "Poco/1.7.8p3@pocoproject/stable"
      generators = "gcc"
      default_options = "Poco:shared=True", "OpenSSL:shared=True"

      def imports(self):
         self.copy("*.dll", dst="bin", src="bin") # From bin to bin
         self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin

      def build(self):
         self.run("mkdir -p bin")
         command = 'g++ timer.cpp @conanbuildinfo.gcc -o bin/timer'
         self.run(command)



.. seealso:: Check the :ref:`Reference/Generators/gcc <gcc_generator>` for the complete reference.



RunEnvironment
--------------

The ``RunEnvironment`` helper prepare ``PATH``, ``LD_LIBRARY_PATH`` and ``DYLIB_LIBRARY_PATH`` environment variables to locate shared libraries and executables of your requirements at runtime.

This helper is specially useful:

- If you are requiring packages with shared libraries and you are running some executable that needs those libraries.
- If you have a requirement with some tool (executable) and you need it in the path.


Example:


.. code-block:: python
   :emphasize-lines: 7, 8, 9

   from conans import ConanFile, AutoToolsBuildEnvironment

   class ExampleConan(ConanFile):
      ...

      def build(self):
         env_build = RunEnvironment(self)
         with tools.environment_append(env_build.vars):
            self.run("....")
            # All the requirements bin folder will be available at PATH
            # All the lib folders will be available in LD_LIBRARY_PATH and DYLIB_LIBRARY_PATH

.. seealso:: Check the :ref:`Reference/Build Helpers/RunEnvironment <run_environment_reference>` to see the complete reference.

