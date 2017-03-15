Build helpers
==================
There are several helpers that can assist to automate the ``build()`` method for popular build systems:

CMake
-----------------

The CMake class has two properties ``command_line`` and ``build_config`` to help running cmake commands:

.. code-block:: python

   def build(self):
      cmake = CMake(self.settings)
      self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
      self.run('cmake --build . %s' % cmake.build_config)

They will set up flags and a cmake generator that reflects the specified Conan settings. However the two methods ``configure()`` and ``build()`` operate with cmake on a higher level:

CMake.configure()
++++++++++++++++++++

The ``cmake`` invocation in the configuration step is highly customizable:

.. code-block:: python

   CMake.configure(self, conan_file, args=None, defs=None, source_dir=None, build_dir=None)


- ``conan_file`` is the ConanFile to use and read settings from. Typically ``self`` is passed
- ``args`` is a list of additional arguments to be passed to the ``cmake`` command. Each argument will be escaped according to the current shell. No extra arguments will be added if ``args=None``
- ``defs`` is a dict that will be converted to a list of CMake command line variable definitions of the form ``-DKEY=VALUE``. Each value will be escaped according to the current shell and can be either ``str``, ``bool`` or of numeric type
- ``source_dir`` is CMake's source directory where ``CMakeLists.txt`` is located. The default value is ``conan_file.conanfile_directory`` if ``None`` is specified. Relative paths are allowed and will be relative to ``build_dir``
- ``build_dir`` is CMake's output directory. The default value is ``conan_file.conanfile_directory`` if ``None`` is specified. The ``CMake`` object will store ``build_dir`` internally for subsequent calls to ``build()``

CMake.build()
++++++++++++++++++++

.. code-block:: python

   CMake.build(self, conan_file, args=None, build_dir=None, target=None)


- ``conan_file`` is the ``ConanFile`` to use and read settings from. Typically ``self`` is passed
- ``args`` is a list of additional arguments to be passed to the ``cmake`` command. Each argument will be escaped according to the current shell. No extra arguments will be added if ``args=None``
- ``build_dir`` is CMake's output directory. If ``None`` is specified the ``build_dir`` from ``configure()`` will be used. ``conan_file.conanfile_directory`` is used if ``configure()`` has not been called
- ``target`` specifies the target to execute. The default *all* target will be built if ``None`` is specified. ``"install"`` can be used to relocate files to aid packaging


.. _building_with_autotools:


Autotools: configure / make
----------------------------------

If you are using **configure**/**make** you can use **AutoToolsBuildEnvironment** helper.
This helper sets ``LIBS``, ``LDFLAGS``, ``CFLAGS``, ``CXXFLAGS`` and ``CPPFLAGS`` environment variables based on your requirements.

It works using the *environment_append* context manager applied to your **configure and make** commands:

.. code-block:: python
   :emphasize-lines: 13, 14
   
   from conans import ConanFile, AutoToolsBuildEnvironment

   class ExampleConan(ConanFile):
      settings = "os", "compiler", "build_type", "arch"
      requires = "Poco/1.7.3@lasote/stable"
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
    - If you have ``MSYS2``/``MinGW`` installed and in the PATH you take advantage of the ``tool.run_in_windows_bash`` command:


.. code-block:: python
   :emphasize-lines: 8, 9, 10, 11, 12, 21, 22

   from conans import ConanFile, AutoToolsBuildEnvironment

   class ExampleConan(ConanFile):
      settings = "os", "compiler", "build_type", "arch"
      requires = "Poco/1.7.3@lasote/stable"
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


The ``AutoToolsBuildEnvironment`` lets to adjust some variables before calling the `vars` method, so you can
add or change some default value automatically filled:

+-----------------------------+---------------------------------------------------------------------+
| PROPERTY                    | DESCRIPTION                                                         |
+=============================+=====================================================================+
| .fpic                       | Boolean, Set it to True if you want to append the -fPIC flag        |
+-----------------------------+---------------------------------------------------------------------+
| .libs                       | List with library names of the requirements  (-l in LIBS)           |
+-----------------------------+---------------------------------------------------------------------+
| .include_paths              | List with the include paths of the requires (-I in CPPFLAGS)        |
+-----------------------------+---------------------------------------------------------------------+
| .library_paths              | List with library paths of the requirements  (-L in LDFLAGS)        |
+-----------------------------+---------------------------------------------------------------------+
| .defines                    | List with variables that will be defined with -D  in CPPFLAGS       |
+-----------------------------+---------------------------------------------------------------------+
| .flags                      | List with compilation flags (CFLAGS and CXXFLAGS)                   |
+-----------------------------+---------------------------------------------------------------------+
| .cxx_flags                  | List with only c++ compilation flags (CXXFLAGS)                     |
+-----------------------------+---------------------------------------------------------------------+
| .link_flags                 | List with linker flags                                              |
+-----------------------------+---------------------------------------------------------------------+


Example:


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


Set environment variables:

+--------------------+---------------------------------------------------------------------+
| NAME               | DESCRIPTION                                                         |
+====================+=====================================================================+
| LIBS               | Library names to link                                               |
+--------------------+---------------------------------------------------------------------+
| LDFLAGS            | Link flags, (-L, -m64, -m32)                                        |
+--------------------+---------------------------------------------------------------------+
| CFLAGS             | Options for the C compiler (-g, -s, -m64, -m32, -fPIC)              |
+--------------------+---------------------------------------------------------------------+
| CXXFLAGS           | Options for the C++ compiler (-g, -s, -stdlib, -m64, -m32, -fPIC)   |
+--------------------+---------------------------------------------------------------------+
| CPPFLAGS           | Preprocessor definitions (-D, -I)                                   |
+--------------------+---------------------------------------------------------------------+


.. note::

 The **ConfigureEnvironment** helper has been deprecated. if you are still using it we recommend to read
 the :ref:`Migrate to new env variables management guide <migrate_to_new_environment_management>`.


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


Set environment variables:

+--------------------+---------------------------------------------------------------------+
| NAME               | DESCRIPTION                                                         |
+====================+=====================================================================+
| LIB                | Library paths separated with ";"                                    |
+--------------------+---------------------------------------------------------------------+
| CL                 | "/I" flags with include directories                                 |
+--------------------+---------------------------------------------------------------------+



GCC or Clang
---------------

You could use the **gcc** generator directly to build your source code.
It's valid to invoke both gcc and clang compilers.


.. code-block:: python
   :emphasize-lines: 15

   from conans import ConanFile

   class PocoTimerConan(ConanFile):
      settings = "os", "compiler", "build_type", "arch"
      requires = "Poco/1.7.3@lasote/stable"
      generators = "gcc"
      default_options = "Poco:shared=True", "OpenSSL:shared=True"

      def imports(self):
         self.copy("*.dll", dst="bin", src="bin") # From bin to bin
         self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin

      def build(self):
         self.run("mkdir -p bin")
         command = 'g++ timer.cpp @conanbuildinfo.gcc -o bin/timer'
         self.run(command)
