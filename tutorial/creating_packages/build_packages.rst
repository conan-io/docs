.. _tutorial_creating_build:

Build packages: the build() method
==================================

We already used a Conan recipe that has a :ref:`build() method<reference_conanfile_methods_build>` and learned how to use that
to invoke a build system and build our packages. In this tutorial, we will modify that
method and explain how you can use it to do things like:

* Building and running tests
* Conditional patching of the source code
* Select the build system you want to use conditionally

Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/build_method


Build and run tests for your project
------------------------------------

You will notice some changes in the **conanfile.py** file from the previous recipe.
Let's check the relevant parts:

Changes introduced in the recipe
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    :caption: *conanfile.py*
    :emphasize-lines: 12, 19, 33-34

    class helloRecipe(ConanFile):
        name = "hello"
        version = "1.0"

        ...

        def source(self):
            git = Git(self)
            git.clone(url="https://github.com/conan-io/libhello.git", target=".")
            # Please, be aware that using the head of the branch instead of an immutable tag
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
            tc.generate()

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()
            if not self.conf.get("tools.build:skip_test", default=False):
                test_folder = os.path.join("tests")
                if self.settings.os == "Windows":
                    test_folder = os.path.join("tests", str(self.settings.build_type))
                self.run(os.path.join(test_folder, "test_hello"))

        ...

* We added the *gtest/1.11.0* requirement to the recipe as a ``test_requires()``. It's a
  type of requirement intended for testing libraries like **Catch2** or **gtest**.

* We use the ``tools.build:skip_test`` configuration (``False`` by default), to tell CMake
  whether to build and run the tests or not. A couple of things to bear in mind:
 
  - If we set the ``tools.build:skip_test`` configuration to ``True`` Conan will
    automatically inject the ``BUILD_TESTING`` variable to CMake set to ``OFF``. You will
    see in the next section that we are using this variable in our *CMakeLists.txt* to
    decide whether to build the tests or not.
 
  - We use the ``tools.build:skip_test`` configuration in the ``build()`` method,
    after building the package and tests, to decide if we want to run the tests or not.
  
  - In this case we are using **gtest** for testing and we have to check if the
    build method is to run the tests or not. This configuration also affects the
    execution of ``CMake.test()`` if you are using CTest and ``Meson.test()`` for Meson.
  

Changes introduced in the library sources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, please note that we are using `another branch
<https://github.com/conan-io/libhello/tree/with_tests>`_ from the **libhello** library. This
branch has two novelties on the library side:

* We added a new function called ``compose_message()`` to the `library sources
  <https://github.com/conan-io/libhello/blob/with_tests/src/hello.cpp#L9-L12>`_ so we can add
  some unit tests over this function. This function is just creating an output message
  based on the arguments passed.

* As we mentioned in the previous section the `CMakeLists.txt for the library
  <https://github.com/conan-io/libhello/blob/with_tests/CMakeLists.txt#L15-L17>`_ uses the
  ``BUILD_TESTING`` CMake variable that conditionally adds the *tests* directory.

.. code-block:: text
    :caption: *CMakeLists.txt*

    cmake_minimum_required(VERSION 3.15)
    project(hello CXX)

    ...

    if (NOT BUILD_TESTING STREQUAL OFF)
        add_subdirectory(tests)
    endif()

    ...

The ``BUILD_TESTING`` `CMake variable
<https://cmake.org/cmake/help/latest/module/CTest.html>`_ is declared and set to ``OFF``
by Conan (if not already defined) whenever the ``tools.build:skip_test`` configuration is
set to value ``True``. This variable is typically declared by CMake when you use CTest but
using the ``tools.build:skip_test`` configuration you can use it in your *CMakeLists.txt*
even if you are using another testing framework.

* We have a `CMakeLists.txt
  <https://github.com/conan-io/libhello/blob/with_tests/tests/CMakeLists.txt>`_ in the
  *tests* folder using `googletest <https://github.com/google/googletest>`_ for
  testing.

.. code-block:: cmake
    :caption: *tests/CMakeLists.txt*

    cmake_minimum_required(VERSION 3.15)
    project(PackageTest CXX)

    find_package(GTest REQUIRED CONFIG)

    add_executable(test_hello test.cpp)
    target_link_libraries(test_hello GTest::gtest GTest::gtest_main hello)


With basic tests on the functionality of the ``compose_message()`` function:


.. code-block:: cpp
    :caption: *tests/test.cpp*

    #include "../include/hello.h"
    #include "gtest/gtest.h"

    namespace {
        TEST(HelloTest, ComposeMessages) {
        EXPECT_EQ(std::string("hello/1.0: Hello World Release! (with color!)\n"), compose_message("Release", "with color!"));
        ...
        }
    }

Now that we have gone through all the changes in the code, let's try them out:

.. code-block:: bash
    :emphasize-lines: 6-23

    $ conan create . --build=missing -tf=""
    ...
    [ 25%] Building CXX object CMakeFiles/hello.dir/src/hello.cpp.o
    [ 50%] Linking CXX static library libhello.a
    [ 50%] Built target hello
    [ 75%] Building CXX object tests/CMakeFiles/test_hello.dir/test.cpp.o
    [100%] Linking CXX executable test_hello
    [100%] Built target test_hello
    hello/1.0: RUN: ./tests/test_hello
    Capturing current environment in /Users/user/.conan2/p/tmp/c51d80ef47661865/b/build/generators/deactivate_conanbuildenv-release-x86_64.sh
    Configuring environment variables
    Running main() from /Users/user/.conan2/p/tmp/3ad4c6873a47059c/b/googletest/src/gtest_main.cc
    [==========] Running 1 test from 1 test suite.
    [----------] Global test environment set-up.
    [----------] 1 test from HelloTest
    [ RUN      ] HelloTest.ComposeMessages
    [       OK ] HelloTest.ComposeMessages (0 ms)
    [----------] 1 test from HelloTest (0 ms total)

    [----------] Global test environment tear-down
    [==========] 1 test from 1 test suite ran. (0 ms total)
    [  PASSED  ] 1 test.
    hello/1.0: Package '82b6c0c858e739929f74f59c25c187b927d514f3' built
    ...

As you can see, the tests were built and run. Let's use now the ``tools.build:skip_test``
configuration in the command line to skip the test building and running:

.. code-block:: bash

    $ conan create . -c tools.build:skip_test=True -tf=""
    ...
    [ 50%] Building CXX object CMakeFiles/hello.dir/src/hello.cpp.o
    [100%] Linking CXX static library libhello.a
    [100%] Built target hello
    hello/1.0: Package '82b6c0c858e739929f74f59c25c187b927d514f3' built
    ...


You can see now that only the library target was built and that no tests were built or
run.


Conditionally patching the source code
--------------------------------------

If you need to patch the source code the recommended approach is to do that in the
``source()`` method. Sometimes, if that patch depends on settings or options, you have
to use the ``build()`` method to apply patches to the source code before launching the
build. There are :ref:`several ways to do this <examples_tools_files_patches>` in Conan.
One of them would be using the :ref:`replace_in_file <conan_tools_files_replace_in_file>`
tool:

.. code-block:: python

    import os
    from conan import ConanFile
    from conan.tools.files import replace_in_file


    class helloRecipe(ConanFile):
        name = "hello"
        version = "1.0"

        # Binary configuration
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False], "fPIC": [True, False]}
        default_options = {"shared": False, "fPIC": True}

        def build(self):
            replace_in_file(self, os.path.join(self.source_folder, "src", "hello.cpp"), 
                            "Hello World", 
                            "Hello {} Friends".format("Shared" if self.options.shared else "Static"))


Please, note that patching in ``build()`` should be avoided if possible and only be done for
very particular cases as it will make more difficult to develop your packages locally (we
will explain more about this in the :ref:`local development flow section<local_package_development_flow>` later)


Conditionally select your build system
--------------------------------------

It's not uncommon that some packages need one build system or another depending on the
platform we are building on. For example, the *hello* library could build in Windows using
CMake and in Linux and MacOS using Autotools. This can be easily handled in the
``build()`` method like this:


.. code-block:: python

    ...

    class helloRecipe(ConanFile):
        name = "hello"
        version = "1.0"

        # Binary configuration
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False], "fPIC": [True, False]}
        default_options = {"shared": False, "fPIC": True}

        ...

        def generate(self):
            if self.settings.os == "Windows":
                tc = CMakeToolchain(self)
                tc.generate()
                deps = CMakeDeps(self)
                deps.generate()
            else:
                tc = AutotoolsToolchain(self)
                tc.generate()
                deps = PkgConfigDeps(self)
                deps.generate()

        ...

        def build(self):
            if self.settings.os == "Windows":
                cmake = CMake(self)
                cmake.configure()
                cmake.build()
            else:
                autotools = Autotools(self)
                autotools.autoreconf()
                autotools.configure()
                autotools.make()

        ...


.. seealso::

    - :ref:`Patching sources <examples_tools_files_patches>`
