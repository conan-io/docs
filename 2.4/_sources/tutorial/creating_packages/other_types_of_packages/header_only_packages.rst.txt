.. _creating_packages_other_header_only:

Header-only packages
====================

In this section, we are going to learn how to create a recipe for a header-only library.

Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/other_packages/header_only


A header-only library is composed only of header files. That means a consumer doesn't link with any library but
includes headers, so we need only one binary configuration for a header-only library.

In the :ref:`Create your first Conan package
<creating_packages_create_your_first_conan_package>` section, we learned about the settings, and how building the
recipe applying different ``build_type`` (Release/Debug) generates a new binary package.

As we only need one binary package, we don't need to declare the `settings` attribute.
This is a basic recipe for a header-only recipe:

.. code-block:: python
   :caption: conanfile.py


    from conan import ConanFile
    from conan.tools.files import copy


    class SumConan(ConanFile):
        name = "sum"
        version = "0.1"
        # No settings/options are necessary, this is header only
        exports_sources = "include/*"
        # We can avoid copying the sources to the build folder in the cache
        no_copy_source = True

        def package(self):
            # This will also copy the "include" folder
            copy(self, "*.h", self.source_folder, self.package_folder)

        def package_info(self):
            # For header-only packages, libdirs and bindirs are not used
            # so it's necessary to set those as empty.
            self.cpp_info.bindirs = []
            self.cpp_info.libdirs = []

Please, note that we are setting ``cpp_info.bindirs`` and ``cpp_info.libdirs`` to ``[]`` because
header-only libraries don't have compiled libraries or binaries, but they default to ``["bin"]``, and ``["lib"]``, then it is necessary to change it.

Also check that we are setting the :ref:`no_copy_source
<conan_conanfile_properties_no_copy_source>` attribute to ``True`` so that the source code
will not be copied from the ``source_folder`` to the ``build_folder``. This is a typical
optimization for header-only libraries to avoid extra copies.

Our header-only library is this simple function that sums two numbers:


.. code-block:: cpp
   :caption: include/sum.h

    inline int sum(int a, int b){
        return a + b;
    }


The folder `examples2/tutorial/creating_packages/other_packages/header_only` in the cloned project contains a ``test_package``
folder with an example of an application consuming the header-only library. So we can run a ``conan create .`` command
to build the package and test the package:

.. code-block:: bash

    $ conan create .
    ...
    [ 50%] Building CXX object CMakeFiles/example.dir/src/example.cpp.o
    [100%] Linking CXX executable example
    [100%] Built target example

    -------- Testing the package: Running test() ----------
    sum/0.1 (test package): Running test()
    sum/0.1 (test package): RUN: ./example
    1 + 3 = 4

After running the ``conan create`` a new binary package is created for the header-only library, and we can see how the
``test_package`` project can use it correctly.

We can list the binary packages created running this command:

.. code-block:: bash

    $ conan list "sum/0.1#:*"
    Local Cache
      sum
        sum/0.1
          revisions
            c1a714a086933b067bcbf12002fb0780 (2024-05-09 15:28:51 UTC)
              packages
                da39a3ee5e6b4b0d3255bfef95601890afd80709
                  info

We get one package with the package ID ``da39a3ee5e6b4b0d3255bfef95601890afd80709``.
Let's see what happen if we run the ``conan create`` but specifying ``-s build_type=Debug``:

.. code-block:: bash

    $ conan create . -s build_type=Debug
    $ conan list "sum/0.1#:*"
    Local Cache
      sum
        sum/0.1
          revisions
            c1a714a086933b067bcbf12002fb0780 (2024-05-09 15:28:51 UTC)
              packages
                da39a3ee5e6b4b0d3255bfef95601890afd80709
                  info

Even in the ``test_package`` executable is built for Debug, we get the same binary package for the header-only library.
This is because we didn't specify the ``settings`` attribute in the recipe, so the changes in the input settings (``-s build_type=Debug``)
do not affect the recipe and therefore the generated binary package is always the same.


Header-only library with tests
------------------------------

In the previous example, we saw why a recipe header-only library shouldn't declare the ``settings`` attribute,
but sometimes the recipe needs them to build some executable, for example, for testing the library.
Nonetheless, the binary package of the header-only library should still be unique, so we are going to review how to
achieve that.


Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/other_packages/header_only_gtest

We have the same header-only library that sums two numbers, but now we have this recipe:


.. code-block:: python

    import os
    from conan import ConanFile
    from conan.tools.files import copy
    from conan.tools.cmake import cmake_layout, CMake


    class SumConan(ConanFile):
        name = "sum"
        version = "0.1"
        settings = "os", "arch", "compiler", "build_type"
        exports_sources = "include/*", "test/*"
        no_copy_source = True
        generators = "CMakeToolchain", "CMakeDeps"

        def requirements(self):
            self.test_requires("gtest/1.11.0")

        def validate(self):
            check_min_cppstd(self, 11)

        def layout(self):
            cmake_layout(self)

        def build(self):
            if not self.conf.get("tools.build:skip_test", default=False):
                cmake = CMake(self)
                cmake.configure(build_script_folder="test")
                cmake.build()
                self.run(os.path.join(self.cpp.build.bindir, "test_sum"))

        def package(self):
            # This will also copy the "include" folder
            copy(self, "*.h", self.source_folder, self.package_folder)

        def package_info(self):
            # For header-only packages, libdirs and bindirs are not used
            # so it's necessary to set those as empty.
            self.cpp_info.bindirs = []
            self.cpp_info.libdirs = []

        def package_id(self):
            self.info.clear()




These are the changes introduced in the recipe:

    - We are introducing a ``test_require`` to ``gtest/1.11.0``. A ``test_require`` is similar to a regular requirement
      but it is not propagated to the consumers and cannot conflict.
    - ``gtest`` needs at least C++11 to build. So we introduced a ``validate()`` method calling ``check_min_cppstd``.
    - As we are building the ``gtest`` examples with CMake, we use the generators ``CMakeToolchain`` and ``CMakeDeps``,
      and we declared the ``cmake_layout()`` to have a known/standard directory structure.
    - We have a ``build()`` method, building the tests, but only when the standard conf ``tools.build:skip_test`` is not
      True. Use that conf as a standard way to enable/disable the testing. It is used by the helpers like ``CMake`` to
      skip the ``cmake.test()`` in case we implement the tests in CMake.
    - We have a ``package_id()`` method calling ``self.info.clear()``. This is internally removing all the information
      (settings, options, requirements) from the package_id calculation so we generate only one configuration for our
      header-only library.


We can call ``conan create`` to build and test our package.

   .. code-block:: bash

         $ conan create . -s compiler.cppstd=14 --build missing
         ...
         Running main() from /Users/luism/.conan2/p/tmp/9bf83ef65d5ff0d6/b/googletest/src/gtest_main.cc
         [==========] Running 1 test from 1 test suite.
         [----------] Global test environment set-up.
         [----------] 1 test from SumTest
         [ RUN      ] SumTest.BasicSum
         [       OK ] SumTest.BasicSum (0 ms)
         [----------] 1 test from SumTest (0 ms total)

         [----------] Global test environment tear-down
         [==========] 1 test from 1 test suite ran. (0 ms total)
         [  PASSED  ] 1 test.
         sum/0.1: Package 'da39a3ee5e6b4b0d3255bfef95601890afd80709' built
         ...

We can run ``conan create`` again specifying a different ``compiler.cppstd`` and the built package would be the same:

   .. code-block:: bash

         $ conan create . -s compiler.cppstd=17
         ...
         sum/0.1: RUN: ./test_sum
         Running main() from /Users/luism/.conan2/p/tmp/9bf83ef65d5ff0d6/b/googletest/src/gtest_main.cc
         [==========] Running 1 test from 1 test suite.
         [----------] Global test environment set-up.
         [----------] 1 test from SumTest
         [ RUN      ] SumTest.BasicSum
         [       OK ] SumTest.BasicSum (0 ms)
         [----------] 1 test from SumTest (0 ms total)

         [----------] Global test environment tear-down
         [==========] 1 test from 1 test suite ran. (0 ms total)
         [  PASSED  ] 1 test.
         sum/0.1: Package 'da39a3ee5e6b4b0d3255bfef95601890afd80709' built

   .. note::

      Once we have the ``sum/0.1`` binary package available (in a server, after a ``conan upload``, or in the local cache),
      we can install it even if we don't specify input values for ``os``, ``arch``, ... etc. This is a new feature of Conan 2.X.

      We could call ``conan install --require sum/0.1`` with an empty profile and would get the binary package from the
      server. But if we miss the binary and we need to build the package again, it will fail because of the lack of
      settings.
