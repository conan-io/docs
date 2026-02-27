.. _reference_environment_variables:

Environment variables
=====================

These are very few environment variables that can be used to configure some of the Conan behavior.
These variables are the exception, for customization and configuration control, Conan uses the 
:ref:`global.conf configuration<reference_config_files_global_conf>` and the :ref:`profile [conf] section<reference_config_files_profiles>`

.. _reference_environment_variables_conan_home:

CONAN_HOME
----------

This variable controls the location of the Conan home folder.
By default, if it is not defined, it will be ``<username>/.conan2``.

.. note::

    Recall that the Conan package cache, contained in the Conan home, is not concurrent. Different parallel tasks
    like those that can happen in CI, need to use a separate cache, and defining ``CONAN_HOME`` is the way to do it.


CONAN_DEFAULT_PROFILE
---------------------

The default profile will be the ``"default"`` file in the Conan cache. This environment variable allows to define
a different default name. There are also ``conf`` items ``core:default_profile`` and ``core:default_build_profile``
to define such default profile names, this env-var should be used only when the ``conf`` is not enough.


Remote login variables
----------------------

``CONAN_LOGIN_USERNAME``, ``CONAN_LOGIN_USERNAME_{REMOTE_NAME}`` define the login username for a given remote.
``CONAN_PASSWORD``, ``CONAN_PASSWORD_{REMOTE_NAME}`` define the login password for a given remote.

These environment variables are just a substitute of the interactive input of the username or password when Conan CLI
requests it. They do not perform any kind of authentication unless the remote server throws an authentication
challenge. That means that for some remote servers configured to allow anonymous usage, these will not be
used, and the user will remain as an unauthenticated user, unless a ``conan remote login`` or ``conan remote auth``
is done first.

When the Conan CLI is about to ask the user for the remote password, it will check the variable ``CONAN_LOGIN_USERNAME_{REMOTE_NAME}``
or ``CONAN_PASSWORD_{REMOTE_NAME}`` first, if the variable is not declared Conan will try to use the variable 
``CONAN_LOGIN_USERNAME`` and ``CONAN_PASSWORD`` respectively, if the variable is not declared either,
Conan will request to the user to input a password or fail.

The remote name is transformed to all uppercase. If the remote name contains "-",
you have to replace it with "_" in the variable name.

.. note::

    - These variables are useful for unattended executions like CI servers or automated tasks, as CI secrets
    - These variables are not recommended for developer machines.
    - Recall that these variables do not perform authentication unless the remote server requests it.
    - The ``core:non_interactive`` conf can be defined in ``global.conf`` to force Conan to fail if any interactive prompt is requested, 
      to avoid CI process being stuck.

Terminal color variables
------------------------

Conan default behavior is try to autodetect the output. If the output is redirected to a file, or other support not ``tty``, 
that cannot print colors, it will disable colored output. For regular terminals, it will try to do colored output, unless some
of the following change that behavior: 

- ``CLICOLOR_FORCE`` Forces the generation of terminal color escape characters, no matter what the autodetection of terminal is.
- ``NO_COLOR`` disables the generation of color escape characters. This will be ignored if ``CLICOLOR_FORCE`` is activated.
- ``CONAN_COLOR_DARK`` will revert the color scheme for white/light background terminals (default assumes dark background).


Logging
-------

The environment variable ``CONAN_LOG_LEVEL`` can define the Conan command line verbosity in the same way that the ``-v``
command line argument, with the same values (``error``, ``verbose``, etc.). It also has priority over the value of the command line arg if both are present.
This can be useful to temporarily change the log level in CI pipelines, in automation, etc., without needing to modify the 
command line arguments.
