.. _conan_conf:

conan.conf
==========

This is the typical ``~/.conan/conan.conf`` file:

.. code-block:: text

    [storage]
    # This is the default path, but you can write your own
    path: ~/.conan/data

    [proxies]
    # Empty section will try to use system proxies.

    [log]
    run_to_output = True        # environment CONAN_LOG_RUN_TO_OUTPUT
    run_to_file = False         # environment CONAN_LOG_RUN_TO_FILE
    level = 50                  # environment CONAN_LOGGING_LEVEL
    # trace_file =              # environment CONAN_TRACE_FILE
    print_run_commands = False  # environment CONAN_PRINT_RUN_COMMANDS

    [general]
    compression_level = 9       # environment CONAN_COMPRESSION_LEVEL
    sysrequires_sudo = True     # environment CONAN_SYSREQUIRES_SUDO
    # cmake_generator           # environment CONAN_CMAKE_GENERATOR

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

The settings defaults are the setting values used whenever you issue a ``conan install`` command over a
``conanfile`` in one of your projects **for the first time**. After that, the settings and options will
be cached in the project ``conaninfo.txt`` file. The initial values for these default settings are
auto-detected the first time you run a ``conan`` command.


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