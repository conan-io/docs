.. _env_vars:

Environment variables
=============================

These are the environment variables used to customize conan.

CONAN_CMAKE_GENERATOR
------------------------------
Conan ``CMake`` helper class is just a convenience to help to translate conan
settings and options into cmake parameters, but you can easily do it yourself, or adapt it.

For some compiler configurations, as ``gcc`` it will use by default the ``Unix Makefiles``
cmake generator. Note that this is not a package settings, building it with makefiles or other
build system, as Ninja, should lead to the same binary if using appropriately the same
underlying compiler settings. So it doesn't make sense to provide a setting or option for this.

So it can be set with the environment variable ``CONAN_CMAKE_GENERATOR``. Just set its value 
to your desired cmake generator (as ``Ninja``).


CONAN_USER_HOME
----------------
Allows defining a custom conan cache directory. Can be useful for concurrent builds under different
users in CI, to retrieve and store per-project specific dependencies (useful for deployment, for example).

Read more about it in :ref:`custom_cache`


CONAN_SYSREQUIRES_SUDO
-----------------------
This environment variable controls whether ``sudo`` is used for installing apt, yum, etc. system
packages via ``SystemPackageTool`` helper, typically used in ``system_requirements()``.
Set it to "False" or "0" to don't use sudo.


CONAN_COLOR_DISPLAY
-----------------------
Useful to remove colored output, set it to ``CONAN_COLOR_DISPLAY=0`` to remove console output colors


CONAN_COLOR_DARK
-----------------------
Set it to ``CONAN_COLOR_DARK=1`` to use dark colors in the terminal output, instead of light ones.
Useful for terminal or consoles with light colors as white, so text is rendered in Blue, Black, Magenta,
instead of Yellow, Cyan, White.