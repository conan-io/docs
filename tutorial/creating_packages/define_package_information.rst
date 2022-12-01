Define the package information for consumers
============================================

In the previous tutorial section, we explained how to store the headers and binaries of a
library in a Conan package. These files are reused by consumers that depend on the package
but we have to provide some additional information so that Conan can pass that to the
build system and consumers can compile and link against our package.

For instance, in our example, we are building a static library named *hello* that once
it's built will result in a *libhello.a* file in Linux and macOS or a *hello.lib* file in
Windows. Also, we are packaging a header file *hello.h* with the declaration of the
library functions. The Conan package ends up with the following structure in the Conan
local cache:

.. code-block:: text

    .
    ├── include
    │   └── hello.h
    └── lib
        └── libhello.a

Then, consumers that want to link against this library will need some information:

- The location of the *include* folder in the Conan local cache to search for the
  *hello.h* file.
- The name of the library file to link against it (*libhello.a* or *hello.lib*)
- The location of the *lib* folder in the Conan local cache to search for the library
  file.

Conan provides an abstraction over all the information consumers may need in the
:ref:`cpp_info<conan_conanfile_model_cppinfo>` attribute of the ConanFile. This attribute
is set in the ``package_info()`` method. Let's have a look at the ``package_info()``
method of our *hello/1.0* Conan package:

.. code-block:: python
    :caption: *conanfile.py*

    def package_info(self):
        self.cpp_info.libs = ["hello"]

We can see a couple of things:

- We are adding a *hello* library to the ``libs`` property of the ``cpp_info`` to tell
  consumers that they should link the libraries from that list.

- We are **not adding** information about the *lib* or *include* folders where the
  library and headers files are packaged. The ``cpp_info`` object provides the
  ``.includedirs`` and ``.libdirs`` properties to define those locations but Conan sets
  their value as ``lib`` and ``include`` by default so it's not needed to add those in this
  case. If you were copying the package files to a different location then you have to set
  those explicitly. The declaration of the ``package_info`` method in our Conan package
  would be equivalent to this one:

.. code-block:: python
    :caption: *conanfile.py*

    def package_info(self):
        self.cpp_info.libs = ["hello"]
        # conan sets libdirs = ["lib"] and includedirs = ["include"] by default
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.includedirs = ["include"]


Setting information in the package_info() method
------------------------------------------------

Besides what we already learned to do in the ``package_info()`` method there are
also other typical use cases, for example:

- Define information for consumers depending on settings or options
- Customizing certain information that generators produce for consumers, things like
  the target names for CMake or the generated files names for pkg-config
- Propagating configuration values to consumers
- Propagating environment information to consumers
- Define components for Conan packages that provide multiple libraries

Let's see some of those. First, clone the project sources again. You can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/package_information


For this section of the tutorial we introduced some changes in the library and recipe.
Let's check the relevant parts:


Changes introduced in the library sources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, please note that we are using `other branch
<https://github.com/czoido/libhello/tree/package_info>`_ from the **libhello** library.
Let's check the *CMakeLists.txt* to build the library:


.. code-block:: text
    :caption: *CMakeLists.txt*
    :emphasize-lines: 9,11

    cmake_minimum_required(VERSION 3.15)
    project(hello CXX)

    ...

    add_library(hello src/hello.cpp)

    if (BUILD_SHARED_LIBS)
        set_target_properties(hello PROPERTIES OUTPUT_NAME hello-shared)
    else()
        set_target_properties(hello PROPERTIES OUTPUT_NAME hello-static)
    endif()

    ...

As you can see, now we are setting the output name for the library depending if we are
building the library as static or shared. Now let's see how to translate these changes to
the Conan recipe.


Changes introduced in the recipe
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First we have to conditionally set the library nanme depending on the
``self.options.shared`` option.

.. code-block:: python
    :caption: *conanfile.py*
    :emphasize-lines: 9, 14-17

    class helloRecipe(ConanFile):
        ...

        def source(self):
            git = Git(self)
            git.clone(url="https://github.com/conan-io/libhello.git", target=".")
            # Please, be aware that using the head of the branch instead of an inmutable tag
            # or commit is not a good practice in general
            git.checkout("package_info")

        ...

        def package_info(self):
            if self.options.shared:
                self.cpp_info.libs = ["hello-shared"]
            else:
                self.cpp_info.libs = ["hello-static"]


Now, let's create the Conan package with ``shared=False`` for example and check that we
are packaging the correct library (*libhello-static.a* or *hello-static.lib*) and that we
are linking the correct library in the *test_package*.

.. code-block:: bash
    :emphasize-lines: 4,14,22

    $ conan create . -s compiler.cppstd=gnu11 --build=missing
    ...
    -- Install configuration: "Release"
    -- Installing: /Users/carlosz/.conan2/p/tmp/a311fcf8a63f3206/p/lib/libhello-static.a
    -- Installing: /Users/carlosz/.conan2/p/tmp/a311fcf8a63f3206/p/include/hello.h
    hello/1.0 package(): Packaged 1 '.h' file: hello.h
    hello/1.0 package(): Packaged 1 '.a' file: libhello-static.a
    hello/1.0: Package 'fd7c4113dad406f7d8211b3470c16627b54ff3af' created
    ...
    -- Build files have been written to: /Users/carlosz/.conan2/p/tmp/a311fcf8a63f3206/b/build/Release
    hello/1.0: CMake command: cmake --build "/Users/carlosz/.conan2/p/tmp/a311fcf8a63f3206/b/build/Release" -- -j16
    hello/1.0: RUN: cmake --build "/Users/carlosz/.conan2/p/tmp/a311fcf8a63f3206/b/build/Release" -- -j16
    [ 25%] Building CXX object CMakeFiles/hello.dir/src/hello.cpp.o
    [ 50%] Linking CXX static library libhello-static.a
    [ 50%] Built target hello
    [ 75%] Building CXX object tests/CMakeFiles/test_hello.dir/test.cpp.o
    [100%] Linking CXX executable test_hello
    [100%] Built target test_hello
    hello/1.0: RUN: tests/test_hello
    ...
    [ 50%] Building CXX object CMakeFiles/example.dir/src/example.cpp.o
    [100%] Linking CXX executable example
    [100%] Built target example

    -------- Testing the package: Running test() --------
    hello/1.0 (test package): Running test()
    hello/1.0 (test package): RUN: ./example
    hello/1.0: Hello World Release! (with color!)

As you can see both the tests and the Conan test_package linked against the
*libhello-static.a* library successfully.

Properties model: setting information for specific generators
-------------------------------------------------------------

First, please note that we are using `another branch
<https://github.com/conan-io/libhello/tree/with_tests>`_ from the **libhello** library. This
branch has two novelties on the library side:

- Package to another place. Imagine that we are packaging our library files in other
  place... let's see how to change that... Add flags, defines, system_libs...
- Different library names for debug/release
- Use options to propagate information conditionally
- Add a system_lib dependency ? add flags ? 
- Set target names for libraries ?
- Introduce properties ?
- Talk about self.conf_info...

Providing environment information
---------------------------------

buildenv_info and runenv_info


Read more
---------

- Using components
- 