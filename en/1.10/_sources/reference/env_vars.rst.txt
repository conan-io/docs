.. _env_vars:

Environment variables
=====================

These are the environment variables used to customize Conan.

 Most of them can be set in the *conan.conf* configuration file (inside your ``<userhome>/.conan`` folder). However, this environment
 variables will take precedence over the *conan.conf* configuration.

.. _cmake_related_variables:

CMAKE RELATED VARIABLES
-----------------------

There are some Conan environment variables that will set the equivalent CMake variable using the :ref:`cmake generator<cmake_generator>` and
the :ref:`CMake build tool<cmake_reference>`:


+-----------------------------------------+------------------------------------------------------------------------------------------------+
| Variable                                | CMake set variable                                                                             |
+=========================================+================================================================================================+
| CONAN_CMAKE_TOOLCHAIN_FILE              | CMAKE_TOOLCHAIN_FILE                                                                           |
+-----------------------------------------+------------------------------------------------------------------------------------------------+
| CONAN_CMAKE_SYSTEM_NAME                 | CMAKE_SYSTEM_NAME                                                                              |
+-----------------------------------------+------------------------------------------------------------------------------------------------+
| CONAN_CMAKE_SYSTEM_VERSION              | CMAKE_SYSTEM_VERSION                                                                           |
+-----------------------------------------+------------------------------------------------------------------------------------------------+
| CONAN_CMAKE_SYSTEM_PROCESSOR            | CMAKE_SYSTEM_PROCESSOR                                                                         |
+-----------------------------------------+------------------------------------------------------------------------------------------------+
| CONAN_CMAKE_FIND_ROOT_PATH              | CMAKE_FIND_ROOT_PATH                                                                           |
+-----------------------------------------+------------------------------------------------------------------------------------------------+
| CONAN_CMAKE_FIND_ROOT_PATH_MODE_PROGRAM | CMAKE_FIND_ROOT_PATH_MODE_PROGRAM                                                              |
+-----------------------------------------+------------------------------------------------------------------------------------------------+
| CONAN_CMAKE_FIND_ROOT_PATH_MODE_LIBRARY | CMAKE_FIND_ROOT_PATH_MODE_LIBRARY                                                              |
+-----------------------------------------+------------------------------------------------------------------------------------------------+
| CONAN_CMAKE_FIND_ROOT_PATH_MODE_INCLUDE | CMAKE_FIND_ROOT_PATH_MODE_INCLUDE                                                              |
+-----------------------------------------+------------------------------------------------------------------------------------------------+

.. seealso::

    See `CMake cross building wiki <https://www.vtk.org/Wiki/CMake_Cross_Compiling>`_

.. _conan_bash_path_env:

CONAN_BASH_PATH
---------------

**Defaulted to**: Not defined

Used only in windows to help the :ref:`tools.run_in_windows_bash()<run_in_windows_bash_tool>` function
to locate our Cygwin/MSYS2 bash. Set it with the bash executable path if it's not in the ``PATH`` or you want to use a different one.

CONAN_CMAKE_GENERATOR
---------------------

Conan ``CMake`` helper class is just a convenience to help to translate conan
settings and options into cmake parameters, but you can easily do it yourself, or adapt it.

For some compiler configurations, as ``gcc`` it will use by default the ``Unix Makefiles``
cmake generator. Note that this is not a package settings, building it with makefiles or other
build system, as Ninja, should lead to the same binary if using appropriately the same
underlying compiler settings. So it doesn't make sense to provide a setting or option for this.

So it can be set with the environment variable ``CONAN_CMAKE_GENERATOR``. Just set its value 
to your desired cmake generator (as ``Ninja``).

CONAN_COLOR_DARK
----------------

**Defaulted to**: ``False``/``0``

Set it to ``True``/``1`` to use dark colors in the terminal output, instead of light ones.
Useful for terminal or consoles with light colors as white, so text is rendered in Blue, Black, Magenta,
instead of Yellow, Cyan, White.

CONAN_COLOR_DISPLAY
-------------------

**Defaulted to**: Not defined

By default if undefined conan output will use color if a tty is detected.

Set it to ``False``/``0`` to remove console output colors.
Set it to ``True``/``1`` to force console output colors.

CONAN_COMPRESSION_LEVEL
-----------------------

**Defaulted to**: ``9``

Conan uses ``tgz`` compression for archives before uploading them to remotes. The default compression
level is good and fast enough for most cases, but users with huge packages might want to change it and
set ``CONAN_COMPRESSION_LEVEL`` environment variable to a lower number, which is able to get slightly
bigger archives but much better compression speed.

CONAN_CPU_COUNT
---------------

**Defaulted to**: Number of available cores in your machine.

Set the number of cores that the :ref:`tools.cpu_count()<cpu_count>` will return.
Conan recipes can use the cpu_count() tool to build the library using more than one core.

CONAN_DEFAULT_PROFILE_PATH
--------------------------

**Defaulted to**: Not defined

This variable can be used to define a path to an existing profile file that Conan will use
as default. If relative, the path will be resolved from the profiles folder.

CONAN_NON_INTERACTIVE
---------------------

**Defaulted to**: ``False``/``0``

This environment variable, if set to ``True``/``1``, will prevent interactive prompts.
Invocations of Conan commands where an interactive prompt would otherwise appear, will fail instead.

This variable can also be set in ``conan.conf`` as ``non_interactive = True`` in the ``[general]``
section.


CONAN_ENV_XXXX_YYYY
-------------------

You can override the default settings (located in your ``~/.conan/profiles/default`` directory) with environment variables.

The ``XXXX`` is the setting name upper-case, and the ``YYYY`` (optional) is the sub-setting name.

**Examples**:

- Override the default compiler:

.. code-block:: bash

    CONAN_ENV_COMPILER = "Visual Studio"

- Override the default compiler version:

.. code-block:: bash

    CONAN_ENV_COMPILER_VERSION = "14"

- Override the architecture:

.. code-block:: bash

    CONAN_ENV_ARCH = "x86"

.. _conan_log_run_to_file:

CONAN_LOG_RUN_TO_FILE
---------------------

**Defaulted to**: ``0``

If set to ``1`` will log every ``self.run("{Some command}")`` command output in a file called ``conan_run.log``.
That file will be located in the current execution directory, so if we call ``self.run`` in the conanfile.py's build method, the file
will be located in the build folder.

In case we execute ``self.run`` in our ``source()`` method, the ``conan_run.log`` will be created in the source directory, but then conan will copy it
to the ``build`` folder following the regular execution flow. So the ``conan_run.log`` will contain all the logs from your conanfile.py command
executions.

The file can be included in the conan package (for debugging purposes) using the ``package`` method.

.. code-block:: python

        def package(self):
            self.copy(pattern="conan_run.log", dst="", keep_path=False)

CONAN_LOG_RUN_TO_OUTPUT
-----------------------

**Defaulted to**: ``1``

If set to ``0`` conan won't print the command output to the stdout.
Can be used with ``CONAN_LOG_RUN_TO_FILE`` set to ``1`` to log only to file and not printing the output.

CONAN_LOGGING_LEVEL
-------------------

**Defaulted to**: ``50``

By default conan logging level is only set for critical events. If you want
to show more detailed logging information, set this variable to lower values, as ``10`` to show
debug information.

CONAN_LOGIN_USERNAME, CONAN_LOGIN_USERNAME_{REMOTE_NAME}
--------------------------------------------------------

**Defaulted to**: Not defined

You can define the username for the authentication process using environment variables.
Conan will use a variable **CONAN_LOGIN_USERNAME_{REMOTE_NAME}**, if the variable is not
declared Conan will use the variable **CONAN_LOGIN_USERNAME**, if the variable is not declared either,
Conan will request to the user to input a username.

These variables are useful for unattended executions like CI servers or automated tasks.

If the remote name contains "-" you have to replace it with "_" in the variable name:

For example: For a remote named "conan-center":

.. code-block:: bash

    SET CONAN_LOGIN_USERNAME_CONAN_CENTER=MyUser

.. _conan_make_program:

CONAN_MAKE_PROGRAM
------------------

**Defaulted to**: Not defined

Specify an alternative ``make`` program to use with:

    - The build helper :ref:`AutoToolsBuildEnvironment<autotools_reference>`. Will invoke the specified executable in the `make` method.
    - The build helper :ref:`build helper CMake<cmake_reference>`. By adjusting the CMake variable `CMAKE_MAKE_PROGRAM <https://cmake.org/cmake/help/v3.0/variable/CMAKE_MAKE_PROGRAM.html>`_.

For example:

.. code-block:: bash

    CONAN_MAKE_PROGRAM="/path/to/mingw32-make"

    # Or only the exe name if it is in the path

    CONAN_MAKE_PROGRAM="mingw32-make"

CONAN_PASSWORD, CONAN_PASSWORD_{REMOTE_NAME}
--------------------------------------------

**Defaulted to**: Not defined

You can define the authentication password using environment variables.
Conan will use a variable **CONAN_PASSWORD_{REMOTE_NAME}**, if the variable is not
declared Conan will use the variable **CONAN_PASSWORD**, if the variable is not declared either,
Conan will request to the user to input a password.

These variables are useful for unattended executions like CI servers or automated tasks.

The remote name is transformed to all uppercase. If the remote name contains "-",
you have to replace it with "_" in the variable name.

For example, for a remote named "conan-center":

.. code-block:: bash

    SET CONAN_PASSWORD_CONAN_CENTER=Mypassword

CONAN_HOOKS
-------------

**Defaulted to**: Not defined

Can be set to a comma separated list with the names of the hooks that will be executed when running a Conan command.

.. _conan_print_run_commands:

CONAN_PRINT_RUN_COMMANDS
------------------------

**Defaulted to**: ``0``

If set to ``1``, every ``self.run("{Some command}")`` call will log the executed command {Some command} to the output.

For example: In the `conanfile.py` file:

.. code-block:: python

    self.run("cd %s && %s ./configure" % (self.ZIP_FOLDER_NAME, env_line))

Will print to the output (stout and/or file):

.. code-block:: bash

    ----Running------
    > cd zlib-1.2.9 && env LIBS="" LDFLAGS=" -m64   $LDFLAGS" CFLAGS="-mstackrealign -fPIC $CFLAGS -m64  -s -DNDEBUG  " CPPFLAGS="$CPPFLAGS -m64  -s -DNDEBUG  " C_INCLUDE_PATH=$C_INCLUDE_PATH: CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH: ./configure
    -----------------
    ...

CONAN_READ_ONLY_CACHE
---------------------

**Defaulted to**: Not defined

This environment variable if defined, will make the conan cache read-only. This could prevent
developers to accidentally edit some header of their dependencies while navigating code in their
IDEs.

This variable can also be set in ``conan.conf`` as ``read_only_cache = True`` in the ``[general]``
section.

The packages are made read-only in two points: when a package is built from sources, and when
a package is retrieved from a remote repository.

The packages are not modified for upload, so users should take that into consideration before
uploading packages, as they will be read-only and that could have other side-effects.

.. warning::

    It is not recommended to upload packages directly from developers machines with read-only mode as it could lead to inconsistencies.
    For better reproducibility we recommend that packages are created and uploaded by CI machines.

.. _conan_run_tests:

CONAN_RUN_TESTS
---------------

**Defaulted to**: Not defined (True/False if defined)

This environment variable (if defined) can be used in ``conanfile.py`` to enable/disable the tests for a library or
application.

It can be used as a convention variable and it's specially useful if a library has unit tests
and you are doing :ref:`cross building <cross_building>`, the target binary can't be executed in current
host machine building the package.

It can be defined in your profile files at ``~/.conan/profiles``

.. code-block:: python

    ...
    [env]
    CONAN_RUN_TESTS=False

or declared in command line when invoking :command:`conan install` to reduce the variable scope for conan execution

.. code-block:: bash

    $ conan install . -e CONAN_RUN_TEST=0

See how to retrieve the value with :ref:`tools.get_env() <tools_get_env>` and check a use case
with :ref:`a header only with unit tests recipe <header_only_unit_tests_tip>` while cross building.

See example of build method in ``conanfile.py`` to enable/disable running tests with CMake:

.. code-block:: python

    from conans import ConanFile, CMake, tools

    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()
            if tools.get_env("CONAN_RUN_TESTS", True):
                cmake.test()

.. _env_var_conan_skip_vs_project_upgrade:

CONAN_SKIP_VS_PROJECTS_UPGRADE
------------------------------

**Defaulted to**: ``False``/``0``

When set to ``True``/``1``, the :ref:`build_sln_command<build_sln_command>`, the :ref:`msvc_build_command<msvc_build_command>`
and the :ref:`MSBuild()<msbuild>` build helper, will not call ``devenv`` command to upgrade the ``sln`` project, irrespective of
the ``upgrade_project`` parameter value.

CONAN_SYSREQUIRES_MODE
----------------------

**Defaulted to**: ``enabled`` allowed values ``enabled``/``verify``/``disabled``

This environment variable controls whether system packages should be installed into the system
via ``SystemPackageTool`` helper, typically used in :ref:`method_system_requirements`.

See values behavior:

    - ``enabled``: Default value and any call to install method of ``SystemPackageTool`` helper should modify
      the system packages.
    - ``verify``: Display a report of system packages to be installed and abort with exception.
      Useful if you don't want to allow conan to modify your system but you want to get a report of
      packages to be installed.
    - ``disabled``: Display a report of system packages that should be installed but continue the conan execution and
      doesn't install any package in your system. Useful if you want to keep manual control of these dependencies,
      for example in your development environment.

CONAN_SYSREQUIRES_SUDO
----------------------

**Defaulted to**: ``True``/``1``

This environment variable controls whether ``sudo`` is used for installing apt, yum, etc. system
packages via ``SystemPackageTool`` helper, typically used in ``system_requirements()``.
By default when the environment variable does not exist, "True" is assumed, and ``sudo`` is
automatically prefixed in front of package management commands.  If you set this to "False" or "0"
``sudo`` will not be prefixed in front of the commands, however installation or updates of some
packages may fail due to a lack of privilege, depending on the user account Conan is running under.

CONAN_TEMP_TEST_FOLDER
----------------------

**Defaulted to**: ``False``/``0``

Activating this variable will make build folder of *test_package* to be created in the temporary folder of your machine.

.. _conan_trace_file:

CONAN_TRACE_FILE
----------------

**Defaulted to**: Not defined

If you want extra logging information about your conan command executions, you can enable it by setting the ``CONAN_TRACE_FILE`` environment variable.
Set it with an absolute path to a file.

.. code-block:: bash

    export CONAN_TRACE_FILE=/tmp/conan_trace.log

When the conan command is executed, some traces will be appended to the specified file. 
Each line contains a JSON object. The ``_action`` field contains the action type, like ``COMMAND`` for command executions, 
``EXCEPTION`` for errors and ``REST_API_CALL`` for HTTP calls to a remote.

The logger will append the traces until the ``CONAN_TRACE_FILE`` variable is unset or pointed to a different file.

.. seealso::

    Read more here: :ref:`logging_and_debugging` 

CONAN_USER, CONAN_CHANNEL
-------------------------

Environment variables commonly used in ``test_package`` conanfiles, to allow package creation for
different users and channel without modifying the code. They are also the environment variables
that will be checked when using ``self.user`` or ``self.channel`` in ``conanfile.py`` package recipes
in user space, where a user/channel has not been assigned yet (it is assigned when exported in the local cache).

.. seealso::

    Read more about it in :ref:`user_channel`

CONAN_USER_HOME
---------------

**Defaulted to**: Not defined

Allows defining a custom conan cache directory. Can be useful for concurrent builds under different
users in CI, to retrieve and store per-project specific dependencies (useful for deployment, for example).

.. seealso::

    Read more about it in :ref:`custom_cache`

CONAN_USER_HOME_SHORT
---------------------

**Defaulted to**: Not defined

Specify the base folder to be used with the :ref:`short paths<short_paths_reference>` feature. When not specified, the packages
marked as `short_paths` will be stored in the ``C:\.conan`` (or the current drive letter).

If set to ``None``, it will disable the `short_paths` feature in Windows for modern Windows that enable long paths at the system level.


CONAN_USE_ALWAYS_SHORT_PATHS
----------------------------

**Defaulted to**: Not defined

If defined to ``True`` or ``1``, every package will be stored in the *short paths directory* resolved
by Conan after evaluating ``CONAN_USER_HOME_SHORT`` variable (see above). This variable, therefore,
overrides the value defined in recipes for the attribute :ref:`short paths<short_paths_reference>`.


CONAN_VERBOSE_TRACEBACK
-----------------------

**Defaulted to**: ``0``

When an error is raised in a recipe or even in the conan code base, if set to ``1`` it will show the complete traceback to ease the debugging.

CONAN_VS_INSTALLATION_PREFERENCE
--------------------------------

**Defaulted to**: ``Enterprise, Professional, Community, BuildTools``

This environment variables defines the order of preference when searching for a Visual installation product. This would affect every tool
that uses ``tools.vs_installation_path()`` and will search in the order indicated.

For example:

.. code-block:: bash

    set CONAN_VS_INSTALLATION_PREFERENCE=Enterprise, Professional, Community, BuildTools

It can also be used to fix the type of installation you want to use indicating just one product type:

.. code-block:: bash

    set CONAN_VS_INSTALLATION_PREFERENCE=BuildTools
