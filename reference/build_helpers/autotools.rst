.. _autotools_reference:


AutoToolsBuildEnvironment
=========================

Prepares the needed environment variables to invoke  **configure**/**make**:

.. code-block:: python

      def build(self):
         env_build = AutoToolsBuildEnvironment(self)
         env_build.configure()
         env_build.make()



Or calling `configure` and `make` manually:

.. code-block:: python

      def build(self):
         env_build = AutoToolsBuildEnvironment(self)
         with tools.environment_append(env_build.vars):
            self.run("./configure")
            self.run("make")




Methods
-------

- **configure** (configure_dir=None, args=None, build=None, host=None, target=None, pkg_config_paths=None)

    - **configure_dir**: Directory where the ``configure`` script is.
    - **args**: A list of additional arguments to be passed to the ``configure`` script. Each argument will be escaped according to the current shell. No extra arguments will be added if ``args=None``
    - **build**: To specify a value for the parameter ``--build``. If ``None`` it will try to detect the value if cross building is detected according to the settings. If ``False``, it will not use this argument at all.
    - **host**: To specify a value for the parameter ``--host``. If ``None`` it will try to detect the value if cross building is detected according to the settings. If ``False``, it will not use this argument at all.
    - **target**: To specify a value for the parameter ``--target``. If ``None`` it will try to detect the value if cross building is detected according to the settings. If ``False``, it will not use this argument at all.
    - **pkg_config_paths**: To specify folders (in a list) where to find ``*.pc`` files (by using the env var ``PKG_CONFIG_PATH``.
      If None is specified but the conanfile is using the ``pkg_config`` generator, the ``self.build_folder`` will be added to the ``PKG_CONFIG_PATH`` in order to locate the pc files of the requirements of the conanfile.

- **make** (args=None, make_program=Nonw)

    - **args**: A list of additional arguments to be passed to the ``make`` command. Each argument will be escaped according to the current shell. No extra arguments will be added if ``args=None``
    - **make_program**: Allows to specify a different ``make`` executable, e.j: ``mingw32-make``. Also the environment variable :ref:`CONAN_MAKE_PROGRAM<conan_make_program>` can be used.

**Set environment variables**

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


**Attributes**

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



You can adjust the automatically filled values modifying the attributes above:


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


.. seealso:: - :ref:`Reference/Tools/environment_append <environment_append_tool>`