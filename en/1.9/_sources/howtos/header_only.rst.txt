.. _header_only:

How to package header-only libraries
====================================

Without unit tests
------------------
Packaging a header only library, without requiring to build and run unit tests for it within conan, can be
done with a very simple recipe. Assuming you have the recipe in the source repo root folder, and the headers
in a subfolder called ``include``, you could do:

.. code-block:: python

    from conans import ConanFile

    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"
        # No settings/options are necessary, this is header only
        exports_sources = "include/*"
        no_copy_source = True

        def package(self):
            self.copy("*.h")

If you want to package an external repository, you can use the ``source()`` method to do a clone or download
instead of the ``exports_sources`` fields.

- There is no need for ``settings``, as changing them will not affect the final package artifacts
- There is no need for ``build()`` method, as header-only are not built
- There is no need for a custom ``package_info()`` method. The default one already adds "include" subfolder
  to the include path
- ``no_copy_source = True`` will disable the copy of the source folder to the build directory as there is
  no need to do so because source code is not modified at all by the ``configure()`` or ``build()`` methods.
- Note that this recipe has no other dependencies, settings or options. If it had any of those, it would be very
  convenient to add the ``package_id()`` method, to ensure that only one package with always the same ID is
  create irrespective of the configurations and dependencies:

.. code-block:: python

    def package_id(self):
        self.info.header_only()

Package is created with:

.. code-block:: bash

    $ conan create . user/channel

With unit tests
---------------

If you want to run the library unit test while packaging, you would need this recipe:

.. code-block:: python

    from conans import ConanFile, CMake

    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"
        settings = "os", "compiler", "arch", "build_type"
        exports_sources = "include/*", "CMakeLists.txt", "example.cpp"
        no_copy_source = True
        
        def build(self): # this is not building a library, just tests
            cmake = CMake(self)
            cmake.configure()
            cmake.build()
            cmake.test()
        
        def package(self):
            self.copy("*.h")

        def package_id(self):
            self.info.header_only()


.. tip::
    .. _header_only_unit_tests_tip:

    If you are :ref:`cross building <cross_building>` your **library** or **app** you'll probably need
    to skip the **unit tests** because your target binary cannot be executed in current building host.
    To do it you can use :ref:`tools.get_env() <tools_get_env>` in combination with
    :ref:`CONAN_RUN_TESTS <conan_run_tests>` env variable, defined as **False**
    in profile for cross building and replace ``cmake.test()`` with:

    .. code-block:: python

        if tools.get_env("CONAN_RUN_TESTS", True):
            cmake.test()

Which will use a ``CMakeLists.txt`` file in the root folder:

.. code-block:: cmake

    project(Package CXX)
    cmake_minimum_required(VERSION 2.8.12)

    include_directories("include")
    add_executable(example example.cpp)

    enable_testing()
    add_test(NAME example
            WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
            COMMAND example)

and some ``example.cpp`` file, which will be our "unit test" of the library:

.. code-block:: cpp

    #include <iostream>
    #include "hello.h"

    int main() {
        hello();
    }


- This will use different compilers and versions, as configured by conan settings (in command line or
  profiles), but will always generate just 1 output package, always with the same ID.
- The necessary files for the unit tests, must be ``exports_sources`` too (or retrieved from ``source()`` method)
- If the package had dependencies, via ``requires``, it would be necessary to add the ``generators = "cmake"``
  to the package recipe and adding the ``conanbuildinfo.cmake`` file to the testing CMakeLists.txt:

.. code-block:: cmake

    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()

    add_executable(example example.cpp)
    target_link_libraries(example ${CONAN_LIBS}) # not necessary if dependencies are also header-only

Package is created with:

.. code-block:: bash

    $ conan create . user/channel


.. note::

    This with/without tests is referring to running full unitary tests over the library, which is different to the :command:`test` functionality
    that checks the integrity of the package. The above examples are describing the approaches for unit-testing the library within the
    recipe. In either case, it is recommended to have a *test_package* folder, so the :command:`conan create` command checks the package once
    it is created. Check the :ref:`packaging getting started guide<packaging_getting_started>`
