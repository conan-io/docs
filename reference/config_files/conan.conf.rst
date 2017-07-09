.. _conan_conf:

conan.conf
==========

This is the typical ``~/.conan/conan.conf`` file:

.. code-block:: text

    [storage]
    # This is the default path, but you can write your own
    path = ~/.conan/data

    [proxies]
    # Empty section will try to use system proxies.
    # If don't want proxy at all, remove section [proxies]
    # As documented in http://docs.python-requests.org/en/latest/user/advanced/#proxies
    # http = http://user:pass@10.10.1.10:3128/
    # http = http://10.10.1.10:3128
    # https = http://10.10.1.10:1080


    [log]
    run_to_output = True        # environment CONAN_LOG_RUN_TO_OUTPUT
    run_to_file = False         # environment CONAN_LOG_RUN_TO_FILE
    level = 50                  # environment CONAN_LOGGING_LEVEL
    # trace_file =              # environment CONAN_TRACE_FILE
    print_run_commands = False  # environment CONAN_PRINT_RUN_COMMANDS

    [general]
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


    [settings_defaults]
    arch=x86_64
    build_type=Release
    compiler=Visual Studio
    compiler.runtime=MD
    compiler.version=14
    os=Windows

Here you can configure the path where all the packages will be stored (on Windows, it is recomended to assign it to
some unit, e.g. map it to X: in order to avoid hitting the 260 chars path name length limit).

You can also adjust the "path" setting using the environment variable **CONAN_USER_HOME**. 
Check the :ref:`how to control the cache<custom_cache>` section.

The remotes are managed in the order in which they are listed. The first one is assumed to be the default
for uploads. For downloads they are also accessed sequentially, until a matching binary package is found.

The settings defaults are the setting values used whenever you issue a ``conan install`` command over a ``conanfile`` in one of your projects **for the first time**. After that, the settings and options will
be cached in the project ``conaninfo.txt`` file. The initial values for these default settings are
auto-detected the first time you run a ``conan`` command.

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


.. _proxys:

Proxies
++++++++++
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