.. _creating_packages_add_dependencies_to_packages:

Add dependencies to packages
============================

In the :ref:`previous tutorial section<tutorial_creating_packages>` we created a Conan
package for a "Hello World" C++ library. We used the
:ref:`conan.tools.scm.Git()<reference>` tool to retrieve the sources from a git
repository. So far, the package does not have any dependency on other Conan packages.
Let's explain how to add a dependency to our package in a very similar way to how we did in
the :ref:`consuming packages section<consuming_packages_flexibility_of_conanfile_py>`. We
will add some fancy colour output to our "Hello World" library using the `fmt 
<https://conan.io/center/fmt>`__ library.

Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/add_requires

You will notice some changes in the `conanfile.py` file from the previous recipe.
Let's check the relevant parts:

.. code-block:: python

    ...
    from conan.tools.build import check_max_cppstd, check_min_cppstd
    ...

    class helloRecipe(ConanFile):
        name = "hello"
        version = "1.0"

        ...
        generators = "CMakeDeps"
        ...

        def validate(self):
            check_min_cppstd(self, "11")
            check_max_cppstd(self, "20")

        def requirements(self):
            self.requires("fmt/8.1.1")

        def source(self):
            git = Git(self)
            git.clone(url="https://github.com/conan-io/libhello.git", target=".")
            # Please, be aware that using the head of the branch instead of an immutable tag
            # or commit is not a good practice in general
            git.checkout("require_fmt")


* First, we set the ``generators`` class attribute to make Conan invoke the
  :ref:`CMakeDeps<conan_tools_cmakedeps>` generator. This was not needed in the previous recipe as we
  did not have dependencies. ``CMakeDeps`` will generate all the config files CMake needs
  to find the ``fmt`` library.

* Next, we use the :ref:`requires()<reference_conanfile_methods>` method to add the
  `fmt <https://conan.io/center/fmt>`__  dependency to our package.

* Also, check that we added an extra line in the :ref:`source()<reference_conanfile_methods>`
  method. We use the `Git().checkout` method to checkout the source code in the
  `require_fmt <https://github.com/conan-io/libhello/tree/require_fmt>`__ branch. This
  branch contains the changes in the source code to add colours to the library messages,
  and also in the ``CMakeLists.txt`` to declare that we are using the ``fmt`` library.

* Finally, note we added the :ref:`validate()<reference_conanfile_methods>` method to the
  recipe. We already used this method in the :ref:`consuming packages
  section<consuming_packages_flexibility_of_conanfile_py>` to raise an error for
  non-supported configurations. Here, we call the
  :ref:`check_min_cppstd()<conan_tools_build_check_min_cppstd>` and
  :ref:`check_max_cppstd()<conan_tools_build_check_max_cppstd>` to check that we are using at
  least C++11 and at most C++20 standards in our settings.


You can check the new sources, using the fmt library in the
`require_fmt <https://github.com/conan-io/libhello/tree/require_fmt>`__. You will see that
the `hello.cpp <https://github.com/conan-io/libhello/blob/require_fmt/src/hello.cpp>`__
file adds colours to the output messages:

.. code-block:: cpp

  #include <fmt/color.h>

  #include "hello.h"

  void hello(){
      #ifdef NDEBUG
      fmt::print(fg(fmt::color::crimson) | fmt::emphasis::bold, "hello/1.0: Hello World Release!\n");
      #else
      fmt::print(fg(fmt::color::crimson) | fmt::emphasis::bold, "hello/1.0: Hello World Debug!\n");
      #endif
      ...


Let's build the package from sources with the current default configuration, and then let
the ``test_package`` folder test the package. You should see the output messages with
colour now:


.. code-block:: bash

    $ conan create . --build=missing
    -------- Exporting the recipe ----------
    ...
    -------- Testing the package: Running test() ----------
    hello/1.0 (test package): Running test()
    hello/1.0 (test package): RUN: ./example
    hello/1.0: Hello World Release!
      hello/1.0: __x86_64__ defined
      hello/1.0: __cplusplus 201103
      hello/1.0: __GNUC__ 4
      hello/1.0: __GNUC_MINOR__ 2
      hello/1.0: __clang_major__ 13
      hello/1.0: __clang_minor__ 1
      hello/1.0: __apple_build_version__ 13160021

Read more
---------

- :ref:`Reference for requirements() method <reference_conanfile_methods_requirements>`.
- :ref:`Introduction to versioning <consuming_packages_intro_versioning>`.
