.. _examples-tools-cmake-toolchain-inject-variables:

CMakeToolchain: Inject arbitrary CMake variables into dependencies
==================================================================

You can find the sources to recreate this project in the `examples2 repository
<https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/examples/tools/cmake/cmake_toolchain/user_toolchain_profile


In the general case, Conan package recipes provide the necessary abstractions via settings, confs, and options
to control different aspects of the build. Many recipes define ``options`` to activate or deactivate features,
optional dependencies, or binary characteristics. Configurations like ``tools.build:cxxflags`` can be used to
inject arbitrary C++ compile flags.

In some exceptional cases, it might be desired to inject CMake variables directly into dependencies doing CMake
builds. This is possible when these dependencies use the ``CMakeToolchain`` integration. Let's check it in this
simple example.

If we have the following package recipe, with a simple ``conanfile.py`` and a ``CMakeLists.txt`` printing a variable:

.. code-block:: python
    :caption: conanfile.py

    from conan import ConanFile
    from conan.tools.cmake import CMake

    class AppConan(ConanFile):
        name = "foo"
        version = "1.0"
        settings = "os", "compiler", "build_type", "arch"
        exports_sources = "CMakeLists.txt"

        generators = "CMakeToolchain"

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()


.. code-block:: cmake
    :caption: CMakeLists.txt

    cmake_minimum_required(VERSION 3.15)
    project(foo LANGUAGES NONE)
    message(STATUS "MYVAR1 ${MY_USER_VAR1}!!")

We can define a profile file and a ``myvars.cmake`` file (both in the same folder) like the following:

.. code-block:: ini
    :caption: myprofile

    include(default)
    [conf]
    tools.cmake.cmaketoolchain:user_toolchain+={{profile_dir}}/myvars.cmake

Note the ``{{profile_dir}}`` is a jinja template expression that evaluates to the current profile folder, allowing
to compute the necessary path to ``myvars.cmake`` file. The ``tools.cmake.cmaketoolchain:user_toolchain`` is a **list**
of files to inject to the generated ``conan_toolchain.cmake``, so the ``+=`` operator is used to append to it.

The ``myvars.cmake`` can define as many variables as we want:

.. code-block:: cmake
    :caption: myvars.cmake

    set(MY_USER_VAR1 "MYVALUE1")


Applying this profile, we can see that the package CMake build effectively uses the variable provided in the 
external ``myvars.cmake`` file:

.. code-block:: bash

    $ conan create . -pr=myprofile
    ...
    -- MY_USER_VAR1 MYVALUE1

Note that using ``user_toolchain`` while defining values for confs like ``tools.cmake.cmaketoolchain:system_name`` is supported.

The ``tools.cmake.cmaketoolchain:user_toolchain`` conf value might also be passed in the command line ``-c`` argument,
but the location of the ``myvars.cmake`` needs to be absolute to be found, as jinja replacement doesn't happen in the
command line.
