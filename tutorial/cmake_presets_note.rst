.. note::

    We use CMake presets in this example. This requires CMake >= 3.23 because the
    "include" from ``CMakeUserPresets.json`` to ``CMakePresets.json`` is only supported
    since that version. If you prefer not to use presets you can use something like:

    .. code-block:: bash

        cmake <path> -G <CMake generator> -DCMAKE_TOOLCHAIN_FILE=<path to conan_toolchain.cmake> -DCMAKE_POLICY_DEFAULT_CMP0091=NEW -DCMAKE_BUILD_TYPE=Release

    Conan will show this CMake command everytime you run ``conan install`` in case you can't use the presets feature.
