.. _visual_studio_build_environment:


VisualStudioBuildEnvironment
============================

Prepares the needed environment variables to invoke the Visual Studio compiler:

.. code-block:: python
   :emphasize-lines: 9, 10, 11

   from conans import ConanFile, VisualStudioBuildEnvironment

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

+--------------------+---------------------------------------------------------------------------------------------------------------------+
| NAME               | DESCRIPTION                                                                                                         |
+====================+=====================================================================================================================+
| LIB                | Library paths separated with ";"                                                                                    |
+--------------------+---------------------------------------------------------------------------------------------------------------------+
| CL                 | "/I" flags with include directories, Runtime (/MT, /MD...), Definitions (/DXXX), and any other C and CXX flags.     |
+--------------------+---------------------------------------------------------------------------------------------------------------------+


**Attributes**

+-----------------------------+----------------------------------------------------------------------------------------------------------------------------+
| PROPERTY                    | DESCRIPTION                                                                                                                |
+=============================+============================================================================================================================+
| .include_paths              |  List with directories of include paths                                                                                    |
+-----------------------------+----------------------------------------------------------------------------------------------------------------------------+
| .lib_paths                  |  List with directories of libraries                                                                                        |
+-----------------------------+----------------------------------------------------------------------------------------------------------------------------+
| .defines                    |  List with definitions (from requirements cpp_info.defines)                                                                |
+-----------------------------+----------------------------------------------------------------------------------------------------------------------------+
| .runtime                    |  List with directories (from settings.compiler.runtime)                                                                    |
+-----------------------------+----------------------------------------------------------------------------------------------------------------------------+
| .flags                      |  List with flag (from requirements cpp_info.cflags                                                                         |
+-----------------------------+----------------------------------------------------------------------------------------------------------------------------+
| .cxx_flags                  |  List with cxx flags (from requirements cpp_info.cppflags                                                                  |
+-----------------------------+----------------------------------------------------------------------------------------------------------------------------+
| .link_flags                 |  List with linker flags (from requirements cpp_info.sharedlinkflags and cpp_info.exelinkflags                              |
+-----------------------------+----------------------------------------------------------------------------------------------------------------------------+



You can adjust the automatically filled values modifying the attributes above:


.. code-block:: python
   :emphasize-lines: 3, 4, 5

      def build(self):
         if self.settings.compiler == "Visual Studio":
            env_build = VisualStudioBuildEnvironment(self)
            env_build.include_paths.append("mycustom/directory/to/headers")
            env_build.lib_paths.append("mycustom/directory/to/libs")
            env_build.link_flags = []
            with tools.environment_append(env_build.vars):
                vcvars = tools.vcvars_command(self.settings)
                self.run('%s && cl /c /EHsc hello.cpp' % vcvars)
                self.run('%s && lib hello.obj -OUT:hello.lib' % vcvars


.. seealso:: - :ref:`Reference/Tools/environment_append <environment_append_tool>`