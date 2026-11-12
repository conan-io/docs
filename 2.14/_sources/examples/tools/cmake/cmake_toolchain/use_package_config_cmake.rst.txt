.. _examples-tools-cmake-toolchain-use-package-config-cmake:

CMakeToolchain: Using xxx-config.cmake files inside packages
============================================================

Conan relies in the general case in the ``package_info()`` abstraction to allow packages built with any build system
to be usable from any other package built with any other build system. In the CMake case, Conan relies on the
``CMakeDeps`` generator to generate ``xxxx-config.cmake`` files for every dependency, even if those dependencies 
didn't generate one or aren't built with CMake at all.

ConanCenter users this abstraction, not packaging the ``xxx-config.cmake`` files, and using the information in ``package_info()``.
This is very important to provide as build-system agnostic as possible packages and be fair with different build systems,
vendors and users. For example, there are many Conan users happily using native MSBuild (VS) projects without any CMake at all.
If ConanCenter packages were only built using the in-package ``config.cmake`` files, this wouldn't be possible.

But the fact that ConanCenter does that, doesn't mean that this is not possible or mandatory. It is perfectly possible
to use the in-packages ``xxx-config.cmake`` files, dropping the usage of ``CMakeDeps`` generator.


You can find the sources to recreate this example in the `examples2 repository
<https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/examples/tools/cmake/pkg_config_files


If we have a look to the ``conanfile.py``:

.. code-block:: python

    class pkgRecipe(ConanFile):
        name = "pkg"
        version = "0.1"
        ...

        def package_info(self):
            # No information provided, only the in-package .cmake is used here
            # Other build systems or CMake via CMakeDeps will fail
            self.cpp_info.builddirs = ["pkg/cmake"]
            self.cpp_info.set_property("cmake_find_mode", "none")


This is a very typical recipe, the main difference is the ``package_info()`` method. Three important things to notice:

- It doesn't define fields like ``self.cpp_info.libs = ["mypkg"]``. Conan will not be propagating this information to
  the consumer, the only place this information will be is inside the in-package ``xxx-config.cmake`` file
- Just in case there are some users still instantiating ``CMakeDeps``, it is disabling the client side generation of the
  ``xxx-config.cmake`` file with ``set_property("cmake_find_mode", "none")``
- It is defining that it will contain the build scripts (like the ``xxx-config.cmake`` package) inside that folder, to
  be located by consumers.

So the responsibility of defining the package details has been transferred to the ``CMakeLists.txt`` that contains:

.. code-block:: cmake

    add_library(mylib src/pkg.cpp)  # Use a different name than the package, to make sure

    set_target_properties(mylib PROPERTIES PUBLIC_HEADER "include/pkg.h")
    target_include_directories(mylib PUBLIC
            $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
            $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
        )

    # Use non default mypkgConfig name
    install(TARGETS mylib EXPORT mypkgConfig)
    export(TARGETS mylib
        NAMESPACE mypkg::  # to simulate a different name and see it works
        FILE "${CMAKE_CURRENT_BINARY_DIR}/mypkgConfig.cmake"
    )
    install(EXPORT mypkgConfig
        DESTINATION "${CMAKE_INSTALL_PREFIX}/pkg/cmake"
        NAMESPACE mypkg::
    )

With that information, when ``conan create`` is executed:

- The ``build()`` method will build the package
- The ``package()`` method will call ``cmake install``, which will create the ``mypkgConfig.cmake`` file
- It will be created in the package folder ``pkg/cmake/mypkgConfig.cmake`` file
- It will contain enough information for the headers, and it will create a ``mypkg::mylib`` target.

Note that the details of the config filename, the namespace and the target are also not known by Conan,
so this is also something that the consumer build scripts should know.


This is enough to have a package with an internal ``mypkgConfig.cmake`` file that can be used by consumers.
In this example code, the consumer is just the ``test_package/conanfile.py``, but exactly the same wouldn
apply to any arbitrary consumer.

The consumer ``conanfile.py`` doesn't need to use ``CMakeDeps`` at all, only ``generators = "CMakeToolchain"``.
Note that the ``CMakeToolchain`` generator is still necessary, because the ``mypkgConfig.cmake`` needs to 
be found inside the Conan cache. The ``CMakeToolchain`` generated ``conan_toolchain.cmake`` file contains
these paths defined.

The consumer ``CMakeLists.txt`` would be standard:

.. code-block:: cmake

    find_package(mypkg CONFIG REQUIRED)

    add_executable(example src/example.cpp)
    target_link_libraries(example mypkg::mylib)


You can verify it works with:

.. code-block:: bash

    $ conan create .

    ======== Testing the package: Executing test ========
    pkg/0.1 (test package): Running test()
    pkg/0.1 (test package): RUN: Release\example
    pkg/0.1: Hello World Release!
    pkg/0.1: _M_X64 defined
    pkg/0.1: MSVC runtime: MultiThreadedDLL
    pkg/0.1: _MSC_VER1939
    pkg/0.1: _MSVC_LANG201402
    pkg/0.1: __cplusplus199711
    pkg/0.1 test_package


Important considerations
------------------------

The presented approach has one limitation, it doesn't work for multi-configuration IDEs.
Implementing this approach won't allow developers to directly switch from IDEs like Visual Studio from Release to Debug
and viceversa, and it will require a ``conan install`` to change. It is not an issue at all for single-config setups,
but for VS developers it can be a bit inconvenient. The team is working on the VS plugin that might help to mitigate this.
The reason is a CMake limitation, ``find_package()`` can only find one configuration, and with ``CMakeDeps`` being dropped 
here, there is nothing that Conan can do to avoid this limitation.

It is important to know that it is also the package author and the package ``CMakeLists.txt`` responsibility to correctly
manage transitivity to other dependencies, and this is not trivial in some cases. There are risks that if not done
correctly the in-package ``xxx-config.cmake`` file can locate its transitive dependencies elsewhere, like in the system,
but not in the transtive Conan package dependencies. 

Finally, recall that these packages won't be usable by other build systems rather than CMake.
