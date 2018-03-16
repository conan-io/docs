
.. _msbuild:

MSBuild
=======

Calls Visual Studio ``msbuild`` command to build a ``sln`` project:

.. code-block:: python

    from conans import ConanFile, MSBuild

    class ExampleConan(ConanFile):
        ...

        def build(self):
            msbuild = MSBuild(self)
            msbuild.build("MyProject.sln")

Internally the ``MSBuild`` build helper uses:

    - :ref:`VisualStudioBuildEnvironment<visual_studio_build>` to adjust the ``LIB`` and ``CL``
      environment variables with all the information from the requirements: include directories, library names, flags etc.
    - :ref:`tools.msvc_build_command<msvc_build_command>` to call msbuild.

You can adjust all the information from the requirements accessing to the ``build_env`` that it is a
:ref:`VisualStudioBuildEnvironment<visual_studio_build>` object:

.. code-block:: python
   :emphasize-lines: 8, 9, 10

    from conans import ConanFile, MSBuild

    class ExampleConan(ConanFile):
        ...

        def build(self):
            msbuild = MSBuild(self)
            msbuild.build_env.include_paths.append("mycustom/directory/to/headers")
            msbuild.build_env.lib_paths.append("mycustom/directory/to/libs")
            msbuild.build_env.link_flags = []

            msbuild.build("MyProject.sln")

Constructor
-----------

.. code-block:: python

    class MSBuild(object):

        def __init__(self, conanfile)

Parameters:
    - **conanfile** (Required): ConanFile object. Usually ``self`` in a ``conanfile.py``.

Methods
-------

build()
+++++++

.. code-block:: python

    def build(self, project_file, targets=None, upgrade_project=True, build_type=None, arch=None,
              parallel=True, force_vcvars=False, toolset=None, platforms=None)

Builds Visual Studio project with the given parameters. It will call ``tools.msvc_build_command()``.

Parameters:
    - **project_file** (Required): Path to the ``sln`` file.
    - **targets** (Optional, Defaulted to ``None``): List of targets to build.
    - **upgrade_project** (Optional, Defaulted to ``True``): Will call ``devenv`` to upgrade the solution to your current Visual Studio.
    - **build_type** (Optional, Defaulted to ``None``): Optional. Defaulted to None, will use the ``settings.build_type``
    - **arch** (Optional, Defaulted to ``None``): Optional. Defaulted to None, will use ``settings.arch``
    - **force_vcvars** (Optional, Defaulted to ``False``): Will ignore if the environment is already set for a different Visual Studio version.
    - **parallel** (Optional, Defaulted to ``True``): Will use the configured number of cores in the :ref:`conan.conf<conan_conf>` file (``cpu_count``).
    - **toolset** (Optional, Defaulted to ``None``): Specify a toolset. Will append a ``/p:PlatformToolset`` option.
    - **platforms** (Optional, Defaulted to ``None``): Dictionary with the mapping of archs/platforms from Conan naming to another one. It
      is useful for Visual Studio solutions that have a different naming in architectures. Example: ``platforms={"x86":"Win32"}`` (Visual
      solution uses "Win32" instead of "x86"). This dictionary will update the default one:

      .. code-block:: python

          msvc_arch = {'x86': 'x86',
                       'x86_64': 'x64',
                       'armv7': 'ARM',
                       'armv8': 'ARM64'}


get_command()
++++++++++++++

Returns a string command calling ``msbuild``

.. code-block:: python

    def get_command(self, project_file, props_file_path=None, targets=None, upgrade_project=True, build_type=None,
                    arch=None, parallel=True, toolset=None, platforms=None, use_env=False):

Parameters:
    - **project_file** (Optional, defaulted to None): Path to a properties file to include in the project.
    - Same other parameters than **build()**



.. _visual_studio_build:


VisualStudioBuildEnvironment
============================

Prepares the needed environment variables to invoke the Visual Studio compiler.
Use it together with :ref:`vcvars_command tool <tools>`

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