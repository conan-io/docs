.. _examples-tools-cmake-toolchain-build-project-extend-presets:

CMakeToolchain: Extending your CMakePresets with Conan generated ones
=====================================================================

In this example we are going to see how to extend your own CMakePresets to include Conan
generated ones.

.. include:: ../../../../tutorial/cmake_presets_note.inc

Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/examples/tools/cmake/cmake_toolchain/extend_own_cmake_presets

Please open the `conanfile.py` and check how it sets ``tc.user_presets_path =
'ConanPresets.json'``. By modifying this attribute of `CMakeToolchain`, you can change the
default filename of the generated preset.

.. code:: python

    def generate(self):
        tc = CMakeToolchain(self)
        tc.user_presets_path = 'ConanPresets.json'
        tc.generate()
        ...

Now you can provide your own ``CMakePresets.json``, besides the ``CMakeLists.txt``:

.. code-block:: json
    :caption: CMakePresets.json

    {
    "version": 4,
    "include": ["./ConanPresets.json"],
    "configurePresets": [
        {
            "name": "default",
            "displayName": "multi config",
            "inherits": "conan-default"
        },
        {
            "name": "release",
            "displayName": "release single config",
            "inherits": "conan-release"
        },
        {
            "name": "debug",
            "displayName": "debug single config",
            "inherits": "conan-debug"
        }
    ],
    "buildPresets": [
        {
            "name": "multi-release",
            "configurePreset": "default",
            "configuration": "Release",
            "inherits": "conan-release"
        },
        {
            "name": "multi-debug",
            "configurePreset": "default",
            "configuration": "Debug",
            "inherits": "conan-debug"
        },
        {
            "name": "release",
            "configurePreset": "release",
            "configuration": "Release",
            "inherits": "conan-release"
        },
        {
            "name": "debug",
            "configurePreset": "debug",
            "configuration": "Debug",
            "inherits": "conan-debug"
        }
    ]
    }

Note how the ``"include": ["./ConanPresets.json"],`` and that every preset ``inherits`` a
Conan generated one.

We can now install for both Release and Debug (and other configurations also, with the
help of ``build_folder_vars`` if we want):

.. code-block:: bash

    $ conan install . 
    $ conan install . -s build_type=Debug

And build and run our application, by using **our own presets** that extend the Conan generated ones:

.. code-block:: bash
    
    # Linux (single-config, 2 configure, 2 builds)
    $ cmake --preset debug
    $ cmake --build --preset debug
    $ ./build/Debug/foo
    > Hello World Debug!
    
    $ cmake --preset release
    $ cmake --build --preset release
    $ ./build/Release/foo
    > Hello World Release!

    # Windows VS (Multi-config, 1 configure 2 builds)
    $ cmake --preset default

    $ cmake --build --preset multi-debug
    $ build\\Debug\\foo
    > Hello World Debug!

    $ cmake --build --preset multi-release
    $ build\\Release\\foo
    > Hello World Release!
