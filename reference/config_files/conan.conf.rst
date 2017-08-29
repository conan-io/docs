.. _conan_conf:

conan.conf
==========

The typical location of the **conan.conf** file is the directory ``~/.conan/conan.conf``:

.. code-block:: text

    [log]
    run_to_output = True        # environment CONAN_LOG_RUN_TO_OUTPUT
    run_to_file = False         # environment CONAN_LOG_RUN_TO_FILE
    level = 50                  # environment CONAN_LOGGING_LEVEL
    # trace_file =              # environment CONAN_TRACE_FILE
    print_run_commands = False  # environment CONAN_PRINT_RUN_COMMANDS

    [general]
    default_profile = default
    compression_level = 9                 # environment CONAN_COMPRESSION_LEVEL
    sysrequires_sudo = True               # environment CONAN_SYSREQUIRES_SUDO
    # bash_path = ""                      # environment CONAN_BASH_PATH (only windows)
    # recipe_linter = False               # environment CONAN_RECIPE_LINTER
    # pylintrc = path/to/pylintrc_file    # environment CONAN_PYLINTRC

    # cmake_generator                     # environment CONAN_CMAKE_GENERATOR
    # http://www.vtk.org/Wiki/CMake_Cross_Compiling
    # cmake_toolchain_file                # environment CONAN_CMAKE_TOOLCHAIN_FILE
    # cmake_system_name                   # environment CONAN_CMAKE_SYSTEM_NAME
    # cmake_system_version                # environment CONAN_CMAKE_SYSTEM_VERSION
    # cmake_system_processor              # environment CONAN_CMAKE_SYSTEM_PROCESSOR
    # cmake_find_root_path                # environment CONAN_CMAKE_FIND_ROOT_PATH
    # cmake_find_root_path_mode_program   # environment CONAN_CMAKE_FIND_ROOT_PATH_MODE_PROGRAM
    # cmake_find_root_path_mode_library   # environment CONAN_CMAKE_FIND_ROOT_PATH_MODE_LIBRARY
    # cmake_find_root_path_mode_include   # environment CONAN_CMAKE_FIND_ROOT_PATH_MODE_INCLUDE

    # cpu_count = 1             # environment CONAN_CPU_COUNT


    [storage]
    # This is the default path, but you can write your own. It must be an absolute path or a
    # path beginning with "~" (if the environment var CONAN_USER_HOME is specified, this directory, even
    # with "~/", will be relative to the conan user home, not to the system user home)
    path = ~/.conan/data

    [proxies]
    # Empty section will try to use system proxies.
    # If don't want proxy at all, remove section [proxies]
    # As documented in http://docs.python-requests.org/en/latest/user/advanced/#proxies
    # http = http://user:pass@10.10.1.10:3128/
    # http = http://10.10.1.10:3128
    # https = http://10.10.1.10:1080


    # Default settings now declared in the default profile


Log
+++

The ``run_to_output`` variable, defaulted to 1, will print to the ``stdout`` the output from the ``self.run`` executions in the conanfile.
You can also adjust the environment variable ``CONAN_LOG_RUN_TO_OUTPUT``.

The ``run_to_file`` variable, defaulted to False, will print the output from the ``self.run`` executions to the path that the variable specifies.
You can also adjust the environment variable ``CONAN_LOG_RUN_TO_FILE``.

The ``level`` variable, defaulted to 50 (critical events), declares the LOG level . If you want to show more detailed logging information,
set this variable to lower values, as 10 to show debug information.                #
You can also adjust the environment variable ``CONAN_LOGGING_LEVEL``.

The ``trace_file`` variable enable extra logging information about your conan command executions.
Set it with an absolute path to a file.
You can also adjust the environment variable ``CONAN_TRACE_FILE``.

The ``print_run_commands``, when is 1, Conan will print the executed commands in ``self.run`` to the output.
You can also adjust the environment variable CONAN_PRINT_RUN_COMMANDS

General
+++++++
The ``bash_path`` variable is used only in windows to help the :ref:`tools.run_in_windows_bash()<run_in_windows_bash_tool>` function
to locate our Cygwin/MSYS2 bash. Set it with the bash executable path if it's not in the PATH or you want to use a different one.

The ``recipe_linter`` variable allows to disable the package recipe analysis (linting) executed at ``conan install``. Please note that this linting is very recommended, specially for sharing package recipes and collaborating with others.

The ``pylintrc`` variable points to a custom ``pylintrc`` file that allows configuring custom rules for the python linter executed at ``export`` time. A use case could be to define some custom indents (though the standard pep8 4-spaces indent is recommended, there are companies that define different styles). The ``pylintrc`` file has the form:

.. code :: text

    [FORMAT]
    indent-string='  '

Running ``pylint --generate-rcfile`` will output a complete rcfile with commments explaining the fields.
    
The ``cmake_***`` variables will declare the corresponding CMake variable when you use the :ref:`cmake generator<cmake_generator>` and
the :ref:`CMake build tool<cmake_reference>`.

The ``cpu_count`` variable set the number of cores that the :ref:`tools.cpu_count()<cpu_count>` will return, by default the number of cores
available in your machine.
Conan recipes can use the cpu_count() tool to build the library using more than one core.


Storage
+++++++
The ``storage.path`` variable define the path where all the packages will be stored (on Windows, it is recomended to assign it to
some unit, e.g. map it to X: in order to avoid hitting the 260 chars path name length limit).


.. note::

    If you want to change the default "conan home" (directory where ``conan.conf`` file is) you can adjust
    the environment variable ``CONAN_USER_HOME``.


.. _proxys:

Proxies
+++++++
If you are not using proxies at all, you can just remove the ``[proxies]`` section
completely. You might want to try to use your system defined configuration. You can try to
do this with a blank ``[proxies]`` section:

.. code-block:: text

    [proxies]
    # Empty section will try to use system proxies.
    # If don't want proxy at all, remove section [proxies]
    
You can specify http and https proxies as follows:

.. code-block:: text

    [proxies]
    # As documented in http://docs.python-requests.org/en/latest/user/advanced/#proxies
    http: http://user:pass@10.10.1.10:3128/
    http: http://10.10.1.10:3128
    https: http://10.10.1.10:1080


If this fails, you might also try to set environment variables:

.. code-block:: bash

   # linux/osx
   $ export HTTP_PROXY="http://10.10.1.10:3128"
   $ export HTTPS_PROXY="http://10.10.1.10:1080"

   # with user/password
   $ export HTTP_PROXY="http://user:pass@10.10.1.10:3128/"
   $ export HTTPS_PROXY="http://user:pass@10.10.1.10:3128/"

   # windows (note, no quotes here)
   $ set HTTP_PROXY=http://10.10.1.10:3128
   $ set HTTPS_PROXY=http://10.10.1.10:1080