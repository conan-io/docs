
.. _msbuild:

MSBuild
=======

Calls Visual Studio :command:`MSBuild` command to build a *.sln* project:

.. code-block:: python

    from conans import ConanFile, MSBuild

    class ExampleConan(ConanFile):
        ...

        def build(self):
            msbuild = MSBuild(self)
            msbuild.build("MyProject.sln")

Internally the ``MSBuild`` build helper uses :ref:`visual_studio_build` to adjust the ``LIB`` and ``CL`` environment variables with all the
information from the requirements: include directories, library names, flags etc. and then calls :command:`MSBuild`.

    - :ref:`VisualStudioBuildEnvironment<visual_studio_build>` to adjust the ``LIB`` and ``CL``
      environment variables with all the information from the requirements: include directories, library names, flags etc.
    - :ref:`tools_msvc_build_command` to call :command:``MSBuild``.

You can adjust all the information from the requirements accessing to the ``build_env`` that it is a :ref:`visual_studio_build` object:

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


To inject the flags corresponding to the ``compiler.runtime``, ``build_type`` and
``compiler.cppstd`` settings, this build helper also generates a
properties file (in the build folder) that is passed to :command:``MSBuild`` with
:command:``/p:ForceImportBeforeCppTargets="conan_build.props"``.

Constructor
-----------

.. code-block:: python

    class MSBuild(object):

        def __init__(self, conanfile)

Parameters:
    - **conanfile** (Required): ConanFile object. Usually ``self`` in a *conanfile.py*.

Attributes
----------

build_env
+++++++++

A :ref:`visual_studio_build` object with the needed environment variables.

Methods
-------

build()
+++++++

.. code-block:: python

    def build(self, project_file, targets=None, upgrade_project=True, build_type=None, arch=None,
              parallel=True, force_vcvars=False, toolset=None, platforms=None, use_env=True,
              vcvars_ver=None, winsdk_version=None, properties=None, output_binary_log=None,
              property_file_name=None, verbosity=None, definitions=None,
              user_property_file_name=None)

Builds Visual Studio project with the given parameters.

Parameters:
    - **project_file** (Required): Path to the *.sln* file.
    - **targets** (Optional, Defaulted to ``None``): Sets ``/target`` flag to the specified list of targets to build.
    - **upgrade_project** (Optional, Defaulted to ``True``): Will call :command:`devenv /upgrade` to upgrade the solution to your current
      Visual Studio.
    - **build_type** (Optional, Defaulted to ``None``): Sets ``/p:Configuration`` flag to the specified value. It will override the value
      from ``settings.build_type``.
    - **arch** (Optional, Defaulted to ``None``): Sets ``/p:Platform`` flag to the specified value. It will override the value from
      ``settings.arch``. This value (or the ``settings.arch`` one if not overridden) will be used as the key for the ``msvc_arch``
      dictionary that returns the final string used for the ``/p:Platform`` flag (see **platforms** argument documentation below).
    - **parallel** (Optional, Defaulted to ``True``): Will use the configured number of cores in the :ref:`conan_conf` file or
      :ref:`tools_cpu_count`:

        - **In the solution**: Building the solution with the projects in parallel. (``/m:`` parameter).
        - **CL compiler**: Building the sources in parallel. (``/MP:`` compiler flag).
    - **force_vcvars** (Optional, Defaulted to ``False``): Will ignore if the environment is already set for a different Visual Studio
      version.
    - **toolset** (Optional, Defaulted to ``None``): Sets ``/p:PlatformToolset`` to the specified toolset. When ``None`` it will apply the
      setting ``compiler.toolset`` if specified. When ``False`` it will skip adjusting the ``/p:PlatformToolset``.
    - **platforms** (Optional, Defaulted to ``None``): This dictionary will update the default one (see ``msvc_arch`` below) and will be
      used to get the mapping of architectures to platforms from the Conan naming to another one. It is useful for Visual Studio solutions
      that have a different naming in architectures. Example: ``platforms={"x86":"Win32"}`` (Visual solution uses "Win32" instead of "x86").

      .. code-block:: python

          msvc_arch = {'x86': 'x86',
                       'x86_64': 'x64',
                       'armv7': 'ARM',
                       'armv8': 'ARM64'}

    - **use_env** (Optional, Defaulted to ``True``: Sets ``/p:UseEnv=true`` flag. Note that this setting does not guarantee that
      environment variables from Conan will not be used by the compiler or linker. This is an MSBuild setting which simply
      specifies the behavior when environment variables conflict with equivalent properties from the project (via *.vcxproj*,
      *.props* or *.targets* files).  Conan will still apply the relevant compiler and linker environment variables when spawning
      the MSBuild process. For example, if ``use_env=False`` is specified **and** if there is no ``AdditionalDependencies`` variable
      defined in the project, the ``LINK`` environment variable passed by Conan will still be used by the linker because it technically
      doesn't conflict with the project variable.
    - **vcvars_ver** (Optional, Defaulted to ``None``): Specifies the Visual Studio compiler toolset to use.
    - **winsdk_version** (Optional, Defaulted to ``None``): Specifies the version of the Windows SDK to use.
    - **properties** (Optional, Defaulted to ``None``): Dictionary with new properties, for each element in the dictionary ``{name: value}``
      it will append a ``/p:name="value"`` option.
    - **output_binary_log** (Optional, Defaulted to ``None``): Sets ``/bl`` flag. If set to ``True`` then MSBuild will output a binary log
      file called *msbuild.binlog* in the working directory. It can also be used to set the name of log file like this
      ``output_binary_log="my_log.binlog"``. This parameter is only supported
      `starting from MSBuild version 15.3 and onwards <http://msbuildlog.com/>`_.
    - **property_file_name** (Optional, Defaulted to ``None``): Sets ``p:ForceImportBeforeCppTargets``. When ``None`` it will generate a
      file named *conan_build.props*. You can specify a different name for the generated properties file.
    - **verbosity** (Optional, Defaulted to ``None``): Sets the ``/verbosity`` flag to the specified verbosity level. Possible values are
      ``"quiet"``, ``"minimal"``, ``"normal"``, ``"detailed"`` and ``"diagnostic"``.
    - **definitions** (Optional, Defaulted to ``None``): Dictionary with additional compiler definitions to be applied during the build.
      Use a dictionary with the desired key and its value set to ``None`` to set a compiler definition with no value.
    - **user_property_file_name** (Optional, Defaulted to ``None``): Filename or list of filenames of user properties files to be automatically passed to the build command. These files have priority over the *conan_build.props* file (user can override that file values), and if a list of file names is provided, later file names also have priority over the former ones. These filenames will be passed, together with *conan_build.props* files as ``/p:ForceImportBeforeCppTargets`` argument.


.. note::

    The ``MSBuild()`` build helper will, before calling to :command:`MSBuild`, call :ref:`tools_vcvars_command` to adjust the environment
    according to the settings. When cross-building from x64 to x86 the toolchain by default is ``x86``. If you want to use ``amd64_x86``
    instead, set the environment variable ``PreferredToolArchitecture=x64``.

get_command()
+++++++++++++

Returns a string command calling :command:`MSBuild`.

.. code-block:: python

    def get_command(self, project_file, props_file_path=None, targets=None, upgrade_project=True,
                    build_type=None, arch=None, parallel=True, toolset=None, platforms=None,
                    use_env=False, properties=None, output_binary_log=None, verbosity=None,
                    user_property_file_name=None)

Parameters:
    - **props_file_path** (Optional, Defaulted to ``None``): Path to a property file to be included in the compilation command. This
      parameter is automatically set by the ``build()`` method to set the runtime from settings.
    - Same parameters as the ``build()`` method.

get_version()
+++++++++++++

Static method that returns the version of MSBuild for the specified settings.

.. code-block:: python

    def get_version(settings)

Result is returned in a ``conans.model.Version`` object as it is evaluated by the command line. It will raise an exception if it cannot
resolve it to a valid result.

Parameters:
    - **settings** (Required): Conanfile settings. Use ``self.settings``.

.. _visual_studio_build:

VisualStudioBuildEnvironment
============================

Prepares the needed environment variables to invoke the Visual Studio compiler.
Use it together with :ref:`tools_vcvars_command`.

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

You can adjust the automatically filled attributes:

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

Constructor
-----------

.. code-block:: python

    class VisualStudioBuildEnvironment(object):

        def __init__(self, conanfile, with_build_type_flags=True)

Parameters:
    - **conanfile** (Required): ConanFile object. Usually ``self`` in a *conanfile.py*.
    - **with_build_type_flags** (Optional, Defaulted to ``True``): If ``True``, it adjusts the compiler flags according to the
      ``build_type`` setting. e.g: `-Zi`, `-Ob0`, `-Od`...

Environment variables
---------------------

+--------------------+---------------------------------------------------------------------------------------------------------------------+
| NAME               | DESCRIPTION                                                                                                         |
+====================+=====================================================================================================================+
| LIB                | Library paths separated with ";"                                                                                    |
+--------------------+---------------------------------------------------------------------------------------------------------------------+
| CL                 | "/I" flags with include directories, Runtime (/MT, /MD...), Definitions (/DXXX), and any other C and CXX flags.     |
+--------------------+---------------------------------------------------------------------------------------------------------------------+

Attributes
----------

include_paths
+++++++++++++

List with directories of include paths.

lib_paths
+++++++++

List with directories of libraries.

defines
+++++++

List with definitions from requirements' ``cpp_info.defines``.

runtime
+++++++

List with directories from ``settings.compiler.runtime``.

flags
+++++

List with flags from requirements' ``cpp_info.cflags``.

cxx_flags
+++++++++

List with cxx flags from requirements' ``cpp_info.cxxflags``.

link_flags
++++++++++

List with linker flags from requirements' ``cpp_info.sharedlinkflags`` and ``cpp_info.exelinkflags``

std
+++

This property contains the flag corresponding to the C++ standard. If you are still using
the deprecated setting ``cppstd`` (see :ref:`manage_cpp_standard`) and you are not providing
any value for this setting, the property will be ``None``.

parallel
++++++++

Defaulted to ``False``.

Sets the flag ``/MP`` in order to compile the sources in parallel using cores found by :ref:`tools_cpu_count`.

.. seealso::

    Read more about :ref:`tools_environment_append`.
