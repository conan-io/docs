
.. _msbuild:

MSBuild
=======

Calls Visual Studio :command:'msbuild` command to build a *.sln* project:

.. code-block:: python

    from conans import ConanFile, MSBuild

    class ExampleConan(ConanFile):
        ...

        def build(self):
            msbuild = MSBuild(self)
            msbuild.build("MyProject.sln")

Internally the ``MSBuild`` build helper uses :ref:`visual_studio_build` to adjust the ``LIB`` and ``CL`` environment variables with all the
information from the requirements: include directories, library names, flags etc. and then calls :command:`msbuild`.

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
              vcvars_ver=None, winsdk_version=None, properties=None)

Builds Visual Studio project with the given parameters.

Parameters:
    - **project_file** (Required): Path to the *.sln* file.
    - **targets** (Optional, Defaulted to ``None``): List of targets to build.
    - **upgrade_project** (Optional, Defaulted to ``True``): Will call :command:`devenv` to upgrade the solution to your current Visual Studio.
    - **build_type** (Optional, Defaulted to ``None``): Use a custom build type name instead of the default ``settings.build_type`` one.
    - **arch** (Optional, Defaulted to ``None``): Use a custom architecture name instead of the ``settings.arch`` one.
      It will be used to build the ``/p:Configuration=`` parameter of ``msbuild``.
      It can be used as the key of the **platforms** parameter. E.g. ``arch="x86", platforms={"x86": "i386"}``
    - **force_vcvars** (Optional, Defaulted to ``False``): Will ignore if the environment is already set for a different Visual Studio version.
    - **parallel** (Optional, Defaulted to ``True``): Will use the configured number of cores in the :ref:`conan_conf` file or :ref:`cpu_count`:

        - **In the solution**: Building the solution with the projects in parallel. (``/m:`` parameter).
        - **CL compiler**: Building the sources in parallel. (``/MP:`` compiler flag)
    - **toolset** (Optional, Defaulted to ``None``): Specify a toolset. Will append a ``/p:PlatformToolset`` option.
    - **platforms** (Optional, Defaulted to ``None``): Dictionary with the mapping of archs/platforms from Conan naming to another one. It
      is useful for Visual Studio solutions that have a different naming in architectures. Example: ``platforms={"x86":"Win32"}`` (Visual
      solution uses "Win32" instead of "x86"). This dictionary will update the default one:

      .. code-block:: python

          msvc_arch = {'x86': 'x86',
                       'x86_64': 'x64',
                       'armv7': 'ARM',
                       'armv8': 'ARM64'}

    - **use_env** (Optional, Defaulted to ``True``: Applies the argument ``/p:UseEnv=true`` to the :command:`msbuild` call.
    - **vcvars_ver** (Optional, Defaulted to ``None``): Specifies the Visual Studio compiler toolset to use.
    - **winsdk_version** (Optional, Defaulted to ``None``): Specifies the version of the Windows SDK to use.
    - **properties** (Optional, Defaulted to ``None``): Dictionary with new properties, for each element in the dictionary ``{name: value}``
      it will append a ``/p:name="value"`` option.

.. note::

    The ``MSBuild()`` build helper will, before calling to ``msbuild``, call :ref:`vcvars_command<vcvars_command>` to adjust the environment according to the settings.
    When cross-building from x64 to x86 the toolchain by default is ``x86``.
    If you want to use ``amd64_x86`` instead, set the environment variable ``PreferredToolArchitecture=x64``.


get_command()
+++++++++++++

Returns a string command calling :command:`msbuild`.

.. code-block:: python

    def get_command(self, project_file, props_file_path=None, targets=None, upgrade_project=True, build_type=None,
                    arch=None, parallel=True, toolset=None, platforms=None, use_env=False):

Parameters:
    - Same parameters as the ``build()`` method.

.. _visual_studio_build:

VisualStudioBuildEnvironment
============================

Prepares the needed environment variables to invoke the Visual Studio compiler.
Use it together with :ref:`vcvars_command`.

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
    - **with_build_type_flags** (Optional, Defaulted to ``True``): If ``True``, it adjusts the compiler flags
      according to the ``build_type`` setting. e.g: `-Zi`, `-Ob0`, `-Od`...


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

List with cxx flags from requirements' ``cpp_info.cppflags``.

link_flags
++++++++++

List with linker flags from requirements' ``cpp_info.sharedlinkflags`` and ``cpp_info.exelinkflags``

std
+++

If the setting ``cppstd`` is set, the property will contain the corresponding flag of the language
standard.

parallel
++++++++

Defaulted to ``False``.

Sets the flag ``/MP`` in order to compile the sources in parallel using cores found by
:ref:`cpu_count`.

.. seealso::

    Read more about :ref:`environment_append_tool`.
