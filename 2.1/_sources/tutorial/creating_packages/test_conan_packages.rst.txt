.. _tutorial_creating_test:

Testing Conan packages
======================

In all the previous sections of the tutorial, we used the *test_package*. It was invoked
automatically at the end of the ``conan create`` command after building our package
verifying that the package is created correctly. Let's explain the *test_package* in more
detail in this section:

Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/testing_packages


Some important notes to have in mind about the *test_package*:

* The *test_package* folder is different from unit or integration tests. These tests are
  “package” tests, and validate that the package is properly created, and that the package
  consumers will be able to link against it and reuse it.

* It is a small Conan project itself, it contains its own *conanfile.py*, and its source
  code including build scripts, that depends on the package being created, and builds and
  execute a small application that requires the library in the package.

* It doesn't belong to the package. It only exist in the source repository, not in the
  package.

The *test_package* folder for our hello/1.0 Conan package has the following contents:

.. code-block:: text

   test_package
    ├── CMakeLists.txt
    ├── conanfile.py
    └── src
        └── example.cpp

Let's have a look at the different files that are part of the *test_package*. First,
*example.cpp* is just a minimal example of how to use the *libhello* library that we are
packaging:

.. code-block:: cpp
    :caption: *test_package/src/example.cpp*

    #include "hello.h"

    int main() {
        hello();
    }

Then the *CMakeLists.txt* file to tell CMake how to build the example:

.. code-block:: cmake
    :caption: *test_package/CMakeLists.txt*

    cmake_minimum_required(VERSION 3.15)
    project(PackageTest CXX)

    find_package(hello CONFIG REQUIRED)

    add_executable(example src/example.cpp)
    target_link_libraries(example hello::hello)

Finally, the recipe for the *test_package* that consumes the *hello/1.0* Conan package:

.. code-block:: python
    :caption: *test_package/conanfile.py*

    import os

    from conan import ConanFile
    from conan.tools.cmake import CMake, cmake_layout
    from conan.tools.build import can_run


    class helloTestConan(ConanFile):
        settings = "os", "compiler", "build_type", "arch"
        generators = "CMakeDeps", "CMakeToolchain"

        def requirements(self):
            self.requires(self.tested_reference_str)

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

        def layout(self):
            cmake_layout(self)

        def test(self):
            if can_run(self):
                cmd = os.path.join(self.cpp.build.bindir, "example")
                self.run(cmd, env="conanrun")

Let's go through the most relevant parts:

* We add the requirements in the ``requirements()`` method, but in this case we use the
  ``tested_reference_str`` attribute that Conan sets to pass to the test_package. This is
  a convenience attribute to avoid hardcoding the package name in the test_package so that
  we can reuse the same test_package for several versions of the same Conan package. In
  our case, this variable will take the ``hello/1.0`` value.

* We define a ``test()`` method. This method will only be invoked in the *test_package*
  recipes. It executes immediately after ``build()`` is called, and it's meant to run some
  executable or tests on binaries to prove the package is correctly created. A couple of
  comments about the contents of our ``test()`` method:
  
  - We are using the :ref:`conan.tools.build.cross_building<conan_tools_build_can_run>`
    tool to check if we can run the built executable in our platform. This tool will
    return the value of the ``tools.build.cross_building:can_run`` in case it's set.
    Otherwise it will return if we are cross-building or not. It’s an useful feature for
    the case your architecture can run more than one target. For instance, Mac M1 machines
    can run both *armv8* and *x86_64*.

  - We run the example binary, that was generated in the ``self.cpp.build.bindir`` folder
    using the environment information that Conan put in the run environment. Conan will
    then invoke a launcher containing the runtime environment information, anything that
    is necessary for the environment to run the compiled executables and applications.

Now that we have gone through all the important bits of the code, let's try our
*test_package*. Although we already learned that the *test_package* is invoked when we
call to ``conan create``, you can also just create the *test_package* if you have already
created the ``hello/1.0`` package in the Conan cache. This is done with the :ref:`conan
test<reference_commands>` command:

.. code-block:: bash
    :emphasize-lines: 18, 21

    $ conan test test_package hello/1.0

    ...

    -------- test_package: Computing necessary packages --------
    Requirements
        fmt/8.1.1#cd132b054cf999f31bd2fd2424053ddc:ff7a496f48fca9a88dc478962881e015f4a5b98f#1d9bb4c015de50bcb4a338c07229b3bc - Cache
        hello/1.0#25e0b5c00ae41ef9fbfbbb1e5ac86e1e:fd7c4113dad406f7d8211b3470c16627b54ff3af#4ff3fd65a1d37b52436bf62ea6eaac04 - Cache
    Test requirements
        gtest/1.11.0#d136b3379fdb29bdfe31404b916b29e1:656efb9d626073d4ffa0dda2cc8178bc408b1bee#ee8cbd2bf32d1c89e553bdd9d5606127 - Skip
 
    ...

    [ 50%] Building CXX object CMakeFiles/example.dir/src/example.cpp.o
    [100%] Linking CXX executable example
    [100%] Built target example

    -------- Testing the package: Running test() --------
    hello/1.0 (test package): Running test()
    hello/1.0 (test package): RUN: ./example
    hello/1.0: Hello World Release! (with color!)

As you can see in the output, our *test_package* builds successfully testing that the
*hello/1.0* Conan package can be consumed with no problem.


.. seealso::

    - Test *tool_requires* packages
    - ...
