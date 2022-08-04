Build packages: the build() method
==================================

.. important::

    In this example, we retrieve the *fmt* and *gtest* Conan packages from a Conan
    repository with packages compatible with Conan 2.0. To run this example successfully
    you should add this remote to your Conan configuration (if did not already do it)
    doing: ``conan remote add conanv2
    https://conanv2beta.jfrog.io/artifactory/api/conan/conan --index 0``


We have already used a Conan recipe that has a ``build()`` method that invokes a build
system to build our packages. In this tutorial, we will modify that method and explain how
you can use it recipe to do things like building and running tests, conditional patching
of source code or select the build system you want to use conditionally.

Please, first clone the sources to recreate this project. You can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/build_method

You will notice some changes in the **conanfile.py** file from the previous recipe.
Let's check the relevant parts:

.. code-block:: python
    :emphasize-lines: 12, 19, 27-28, 35-36

    class helloRecipe(ConanFile):
        name = "hello"
        version = "1.0"

        ...

        def source(self):
            git = Git(self)
            git.clone(url="https://github.com/conan-io/libhello.git", target=".")
            # Please, be aware that using the head of the branch instead of an inmutable tag
            # or commit is not a good practice in general
            git.checkout("with_tests")

        ...

        def requirements(self):
            if self.options.with_fmt:
                self.requires("fmt/8.1.1")
            self.test_requires("gtest/1.11.0")

        ...

        def generate(self):
            tc = CMakeToolchain(self)
            if self.options.with_fmt:
                tc.variables["WITH_FMT"] = True
            if not self.conf.get("tools.build:skip_test", default=False):
                tc.variables["BUILD_TESTS"] = True
            tc.generate()

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()
            if not self.conf.get("tools.build:skip_test", default=False):
                self.run(os.path.join(self.cpp.build.bindirs[0], "tests", "test_hello"))

        ...


Changes introduced in the library
---------------------------------

First, please note that we are using `another branch
<https://github.com/conan-io/libhello/tree/with_tests>`_ from the **libhello** library. This
branch has two novelties on the library side:

* We added a new function called ``compose_message()`` to the `library sources
  <https://github.com/conan-io/libhello/blob/with_tests/src/hello.cpp>`_ so we can add
  some unit tests over this function. This function is just creating an output message
  based on the arguments passed.

* The `CMakeLists.txt
  <https://github.com/conan-io/libhello/blob/with_tests/CMakeLists.txt>`_ uses a
  ``BUILD_TEST`` CMake variable that conditionally adds the *tests* directory.

.. code-block:: cmake
    :emphasize-lines: 12, 19, 27-28, 35-36

    cmake_minimum_required(VERSION 3.15)
    project(hello CXX)

    ...

    if (BUILD_TESTS)
        add_subdirectory(tests)
    endif()

    ...

* We have a `CMakeLists.txt
  <https://github.com/conan-io/libhello/blob/with_tests/tests/CMakeLists.txt>`_ in the
  *tests* folder using `googletest <https://github.com/google/googletest>`_ as for
  testing.

.. code-block:: cmake

    cmake_minimum_required(VERSION 3.15)
    project(PackageTest CXX)

    find_package(GTest REQUIRED CONFIG)

    add_executable(test_hello test.cpp)
    target_link_libraries(test_hello GTest::gtest GTest::gtest_main hello)


With basic tests on the functionality of the ``compose_message()`` function:


.. code-block:: cpp

    #include "../include/hello.h"

    #include <limits.h>

    #include "gtest/gtest.h"

    namespace {
        TEST(HelloTest, ComposeMessages) {
        EXPECT_EQ(std::string("hello/1.0: Hello World Release! (with color!)\n"), compose_message("Release", "with color!"));
        ...
        }
    }


Changes introduced in the recipe
--------------------------------

* We added the *gtest/1.11.0* requirement to the recipe as a ``test_requires()``. This is
  a special type of requirement intended for testing libraries like Catch2 or gtest.

* We use the `tools.build:skip_test` configuration, to tell CMake wether to build and run
  the tests or not. This configuration controls the execution of ``CMake.test()`` and
  ``Meson.test()`` but can also be used for other testing environments like in this case.


Read more
---------

- ...
