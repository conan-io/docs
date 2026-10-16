
.. _creating_packages_preparing_the_build:

Preparing the build
===================

In the :ref:`previous tutorial section<creating_packages_add_dependencies_to_packages>`,
we added the `fmt <https://conan.io/center/fmt>`__ requirement to our Conan package to
provide colour output to our "Hello World" C++ library. In this section, we focus on the
``generate()`` method of the recipe. The aim of this method generating all the
information that could be needed while running the build step. That means things like:

* Write files to be used in the build step, like
  :ref:`scripts<conan_tools_env_environment_model>` that inject environment variables,
  files to pass to the build system, etc.
* Configuring the toolchain to provide extra information based on the settings and options
  or removing information from the toolchain that Conan generates by default and may not
  apply for certain cases.


We explain how to use this method for a simple example based on the previous tutorial section.
We add a `with_fmt` option to the recipe, depending on the value we require the
`fmt` library or not. We use the `generate()` method to modify the toolchain so that
it passes a variable to CMake so that we can conditionally add that library and use `fmt`
or not in the source code.

Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/preparing_the_build

You will notice some changes in the `conanfile.py` file from the previous recipe.
Let's check the relevant parts:

.. code-block:: python
    :emphasize-lines: 12,16,20,29,32,37

    ...
    from conan.tools.build import check_max_cppstd, check_min_cppstd
    ...

    class helloRecipe(ConanFile):
        name = "hello"
        version = "1.0"

        ...
        options = {"shared": [True, False], 
                   "fPIC": [True, False],
                   "with_fmt": [True, False]}

        default_options = {"shared": False, 
                           "fPIC": True,
                           "with_fmt": True}
        ...

        def validate(self):
            if self.options.with_fmt:
                check_min_cppstd(self, "11")
                check_max_cppstd(self, "14")

        def source(self):
            git = Git(self)
            git.clone(url="https://github.com/conan-io/libhello.git", target=".")
            # Please, be aware that using the head of the branch instead of an immutable tag
            # or commit is not a good practice in general
            git.checkout("optional_fmt")

        def requirements(self):
            if self.options.with_fmt:
                self.requires("fmt/8.1.1")

        def generate(self):
            tc = CMakeToolchain(self)
            if self.options.with_fmt:
                tc.variables["WITH_FMT"] = True
            tc.generate()

        ...


As you can see:

* We declare a new ``with_fmt`` option with the default value set to ``True``

* Based on the value of the ``with_fmt`` option:

    - We install or not the ``fmt/8.1.1`` Conan package.
    - We require or not a minimum and a maximum C++ standard as the *fmt* library requires at least C++11 and it will not compile if we try to use a standard above C++14 (just an example, *fmt* can build with more modern standards)
    - We inject the ``WITH_FMT`` variable with the value ``True`` to the :ref:`CMakeToolchain<conan_tools_cmaketoolchain>` so that we
      can use it in the *CMakeLists.txt* of the **hello** library to add the CMake **fmt::fmt** target
      conditionally.

* We are cloning another branch of the library. The *optional_fmt* branch contains
  some changes in the code. Let's see what changed on the CMake side:

.. code-block:: cmake
    :caption: **CMakeLists.txt**
    :emphasize-lines: 8-12

    cmake_minimum_required(VERSION 3.15)
    project(hello CXX)

    add_library(hello src/hello.cpp)
    target_include_directories(hello PUBLIC include)
    set_target_properties(hello PROPERTIES PUBLIC_HEADER "include/hello.h")

    if (WITH_FMT)
        find_package(fmt)
        target_link_libraries(hello fmt::fmt)
        target_compile_definitions(hello PRIVATE USING_FMT=1)
    endif()

    install(TARGETS hello)

As you can see, we use the ``WITH_FMT`` we injected in the
:ref:`CMakeToolchain<conan_tools_cmaketoolchain>`. Depending on the value we will try to find
the fmt library and link our hello library with it. Also, check that we add the
``USING_FMT=1`` compile definition that we use in the source code depending on whether we
choose to add support for ``fmt`` or not.

.. code-block:: cpp
    :caption: **hello.cpp**
    :emphasize-lines: 4,9

    #include <iostream>
    #include "hello.h"

    #if USING_FMT == 1
    #include <fmt/color.h>
    #endif

    void hello(){
        #if USING_FMT == 1
            #ifdef NDEBUG
            fmt::print(fg(fmt::color::crimson) | fmt::emphasis::bold, "hello/1.0: Hello World Release! (with color!)\n");
            #else
            fmt::print(fg(fmt::color::crimson) | fmt::emphasis::bold, "hello/1.0: Hello World Debug! (with color!)\n");
            #endif
        #else
            #ifdef NDEBUG
            std::cout << "hello/1.0: Hello World Release! (without color)" << std::endl;
            #else
            std::cout << "hello/1.0: Hello World Debug! (without color)" << std::endl;
            #endif
        #endif
    }

Let's build the package from sources first using ``with_fmt=True`` and then
``with_fmt=False``. When *test_package* runs it will show different messages depending
on the value of the option.


.. code-block:: bash

    $ conan create . --build=missing -o with_fmt=True
    -------- Exporting the recipe ----------
    ...

    -------- Testing the package: Running test() ----------
    hello/1.0 (test package): Running test()
    hello/1.0 (test package): RUN: ./example
    hello/1.0: Hello World Release! (with color!)

    $ conan create . --build=missing -o with_fmt=False
    -------- Exporting the recipe ----------
    ...

    -------- Testing the package: Running test() ----------
    hello/1.0 (test package): Running test()
    hello/1.0 (test package): RUN: ./example
    hello/1.0: Hello World Release! (without color)

This is just a simple example of how to use the ``generate()`` method to customize the
toolchain based on the value of one option, but there are lots of other things that you
could do in the ``generate()`` method like:

* Create a complete custom toolchain based on your needs to use in your build.
* Access to certain information about the package dependencies, like:
    - The configuration accessing the defined
      :ref:`conf_info<conan_conanfile_model_conf_info>`.
    - Accessing the dependencies options.
    - Import files from dependencies using the :ref:`copy tool<conan_tools_files_copy>`.
      You could also import the files create manifests for the package, collecting all
      dependencies versions and licenses.
* Use the :ref:`Environment tools<conan_tools_env_environment_model>` to generate
  information for the system environment.
* Adding custom configurations besides *Release* and *Debug*, taking into account the
  settings, like *ReleaseShared* or *DebugShared*.

.. seealso::

    - Use the ``generate()`` to :ref:`import files from dependencies<copy_resources_on_generate>`.
    - More based on the examples mentioned above ... 
    - :ref:`generate() method reference<reference_conanfile_methods_generate>`
