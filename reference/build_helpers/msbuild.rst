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

    - :ref:`VisualStudioBuildEnvironment<visual_studio_build_environment>` to adjust the ``LIB`` and ``CL``
      environment variables with all the information from the requirements: include directories, library names, flags etc.
    - :ref:`tools.msvc_build_command<msvc_build_command>` to call msbuild.


You can adjust all the information from the requirements accessing to the ``env_build`` that it is a
:ref:`VisualStudioBuildEnvironment<visual_studio_build_environment>` object:

.. code-block:: python
   :emphasize-lines: 3, 4, 5

      def build(self):
          msbuild = MSBuild(self)
          msbuild.env_build.include_paths.append("mycustom/directory/to/headers")
          msbuild.env_build.lib_paths.append("mycustom/directory/to/libs")
          msbuild.env_build.link_flags = []

          msbuild.build("MyProject.sln")

Methods
-------

* **build(self, project_file, targets=None, upgrade_project=True, build_type=None, arch=None, parallel=True, force_vcvars=False, toolset=None)**:

   - **project_file**: Path to the ``sln`` file.
   - **targets**: Optional. Defaulted to None. You can specify a specific target name.
   - **upgrade_project**: Optional. Defaulted to True. Will call ``devenv`` to upgrade the solution to your current Visual Studio.
   - **build_type**: Optional. Defaulted to None, will use the ``settings.build_type``
   - **arch**: Optional. Defaulted to None, will use ``settings.arch``
   - **force_vcvars**: Optional. Defaulted to False. Will ignore if the environment is already set for a different Visual Studio version.
   - **parallel**: Optional. Defaulted to True, will use the configured number of cores in the :ref:`conan.conf<conan_conf>` file (``cpu_count``).
   - **toolset**: Specify a toolset. Will append a ``/p:PlatformToolset`` option.
