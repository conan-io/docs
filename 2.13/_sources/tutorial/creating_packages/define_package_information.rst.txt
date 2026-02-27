.. _tutorial_creating_define_package_info:

Define information for consumers: the package_info() method
===========================================================

In the previous tutorial section, we explained how to store the headers and binaries of a
library in a Conan package using the :ref:`package
method<creating_packages_package_method>`. Consumers that depend on that package will
reuse those files, but we have to provide some additional information so that Conan can
pass that to the build system and consumers can use the package.

For instance, in our example, we are building a static library named *hello* that will
result in a *libhello.a* file in Linux and macOS or a *hello.lib* file in Windows. Also,
we are packaging a header file *hello.h* with the declaration of the library functions.
The Conan package ends up with the following structure in the Conan local cache:

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
:ref:`cpp_info<conan_conanfile_model_cppinfo>` attribute of the ConanFile. The information
for this attribute must be set in the :ref:`package_info() method<reference_conanfile_methods_package_info>`. Let's have a look at the
``package_info()`` method of our *hello/1.0* Conan package:

.. code-block:: python
    :caption: *conanfile.py*

    ...

    class helloRecipe(ConanFile):
        name = "hello"
        version = "1.0"    

        ...

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

    ...
    
    class helloRecipe(ConanFile):
        name = "hello"
        version = "1.0"    

        ...

        def package_info(self):
            self.cpp_info.libs = ["hello"]
            # conan sets libdirs = ["lib"] and includedirs = ["include"] by default
            self.cpp_info.libdirs = ["lib"]
            self.cpp_info.includedirs = ["include"]


Setting information in the package_info() method
------------------------------------------------

Besides what we explained above about the information you can set in the
``package_info()`` method, there are some typical use cases:

- Define information for consumers depending on settings or options
- Customizing certain information that generators provide to consumers, like the target
  names for CMake or the generated files names for pkg-config for example
- Propagating configuration values to consumers
- Propagating environment information to consumers
- Define components for Conan packages that provide multiple libraries

Let's see some of those in action. First, clone the project sources if you haven't done so yet. You can
find them in the `examples2 repository <https://github.com/conan-io/examples2>`_ on
GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/package_information


Define information for consumers depending on settings or options
-----------------------------------------------------------------

For this section of the tutorial we introduced some changes in the library and recipe.
Let's check the relevant parts:


Changes introduced in the library sources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, please note that we are using `another branch
<https://github.com/conan-io/libhello/tree/package_info>`_ from the **libhello** library.
Let's check the library's *CMakeLists.txt*:


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

As you can see, we are setting the output name for the library depending on whether we are
building the library as static (*hello-static*) or as shared (*hello-shared*). Now let's see
how to translate these changes to the Conan recipe.


Changes introduced in the recipe
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To update our recipe according to the changes in the library's *CMakeLists.txt* we have to
conditionally set the library name depending on the ``self.options.shared`` option in the
``package_info()`` method:

.. code-block:: python
    :caption: *conanfile.py*
    :emphasize-lines: 9, 14-17

    class helloRecipe(ConanFile):
        ...

        def source(self):
            git = Git(self)
            git.clone(url="https://github.com/conan-io/libhello.git", target=".")
            # Please, be aware that using the head of the branch instead of an immutable tag
            # or commit is not a good practice in general
            git.checkout("package_info")

        ...

        def package_info(self):
            if self.options.shared:
                self.cpp_info.libs = ["hello-shared"]
            else:
                self.cpp_info.libs = ["hello-static"]


Now, let's create the Conan package with ``shared=False`` (that's the default so no need
to set it explicitly) and check that we are packaging the correct library
(*libhello-static.a* or *hello-static.lib*) and that we are linking the correct library in
the *test_package*.

.. code-block:: bash
    :emphasize-lines: 4,14,22

    $ conan create . --build=missing
    ...
    -- Install configuration: "Release"
    -- Installing: /Users/user/.conan2/p/tmp/a311fcf8a63f3206/p/lib/libhello-static.a
    -- Installing: /Users/user/.conan2/p/tmp/a311fcf8a63f3206/p/include/hello.h
    hello/1.0 package(): Packaged 1 '.h' file: hello.h
    hello/1.0 package(): Packaged 1 '.a' file: libhello-static.a
    hello/1.0: Package 'fd7c4113dad406f7d8211b3470c16627b54ff3af' created
    ...
    -- Build files have been written to: /Users/user/.conan2/p/tmp/a311fcf8a63f3206/b/build/Release
    hello/1.0: CMake command: cmake --build "/Users/user/.conan2/p/tmp/a311fcf8a63f3206/b/build/Release" -- -j16
    hello/1.0: RUN: cmake --build "/Users/user/.conan2/p/tmp/a311fcf8a63f3206/b/build/Release" -- -j16
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

As you can see both the tests for the library and the Conan *test_package* linked against
the *libhello-static.a* library successfully.

.. _tutorial_creating_define_package_info_properties:

Properties model: setting information for specific generators
-------------------------------------------------------------

The :ref:`CppInfo<conan_conanfile_model_cppinfo_attributes>` object provides the
``set_property`` method to set information specific to each generator. For example, in
this tutorial, we use the :ref:`CMakeDeps<conan_tools_cmakedeps>` generator to generate the
information that CMake needs to build a project that requires our library. ``CMakeDeps``,
by default, will set a target name for the library using the same name as the Conan
package. If you have a look at that *CMakeLists.txt* from the *test_package*:

.. code-block:: cmake
    :caption: test_package *CMakeLists.txt*
    :emphasize-lines: 7

    cmake_minimum_required(VERSION 3.15)
    project(PackageTest CXX)

    find_package(hello CONFIG REQUIRED)

    add_executable(example src/example.cpp)
    target_link_libraries(example hello::hello)

You can see that we are linking with the target name ``hello::hello``. Conan sets this
target name by default, but we can change it using the *properties model*. Let's try to
change it to the name ``hello::myhello``. To do this, we have to set the property
``cmake_target_name`` in the package_info method of our *hello/1.0* Conan package:


.. code-block:: python
    :caption: *conanfile.py*
    :emphasize-lines: 10

    class helloRecipe(ConanFile):
        ...

        def package_info(self):
            if self.options.shared:
                self.cpp_info.libs = ["hello-shared"]
            else:
                self.cpp_info.libs = ["hello-static"]

            self.cpp_info.set_property("cmake_target_name", "hello::myhello")


Then, change the target name we are using in the *CMakeLists.txt* in the *test_package*
folder to ``hello::myhello``:

.. code-block:: cmake
    :caption: test_package *CMakeLists.txt*
    :emphasize-lines: 4

    cmake_minimum_required(VERSION 3.15)
    project(PackageTest CXX)
    # ...
    target_link_libraries(example hello::myhello)

And re-create the package:

.. code-block:: bash
    :emphasize-lines: 14

    $ conan create . --build=missing
    Exporting the recipe
    hello/1.0: Exporting package recipe
    hello/1.0: Using the exported files summary hash as the recipe revision: 44d78a68b16b25c5e6d7e8884b8f58b8 
    hello/1.0: A new conanfile.py version was exported
    hello/1.0: Folder: /Users/user/.conan2/p/a8cb81b31dc10d96/e
    hello/1.0: Exported revision: 44d78a68b16b25c5e6d7e8884b8f58b8
    ...
    -------- Testing the package: Building --------
    hello/1.0 (test package): Calling build()
    ...
    -- Detecting CXX compile features
    -- Detecting CXX compile features - done
    -- Conan: Target declared 'hello::myhello'
    ...
    [100%] Linking CXX executable example
    [100%] Built target example

    -------- Testing the package: Running test() --------
    hello/1.0 (test package): Running test()
    hello/1.0 (test package): RUN: ./example
    hello/1.0: Hello World Release! (with color!)

You can see how Conan now declares the ``hello::myhello`` instead of the default
``hello::hello`` and the *test_package* builds successfully.

The target name is not the only property you can set in the CMakeDeps generator. For a
complete list of properties that affect the CMakeDeps generator behaviour, please check
the :ref:`reference<CMakeDeps Properties>`. 

Propagating environment or configuration information to consumers
-----------------------------------------------------------------

You can provide environment information to consumers in the ``package_info()``. To do so,
you can use the ConanFile's :ref:`runenv_info<conan_conanfile_attributes_runenv_info>` and
:ref:`buildenv_info<conan_conanfile_attributes_buildenv_info>` properties:

* ``runenv_info`` :ref:`Environment<conan_tools_env_environment_model>` object that
  defines environment information that consumers that use the package may need when
  **running**. 

* ``buildenv_info`` :ref:`Environment<conan_tools_env_environment_model>` object that
  defines environment information that consumers that use the package may need when
  **building**. 

Please note that it's not necessary to add ``cpp_info.bindirs`` to ``PATH`` or
``cpp_info.libdirs`` to ``LD_LIBRARY_PATH``, those are automatically added by the
:ref:`VirtualBuildEnv<conan_tools_env_virtualbuildenv>` and
:ref:`VirtualRunEnv<conan_tools_env_virtualrunenv>`.

You can also define configuration values in the ``package_info()`` so that consumers can
use that information. To do this, set the
:ref:`conf_info<conan_conanfile_model_conf_info>` property of the ConanFile.

To know more about this use case, please check the :ref:`corresponding
example<examples_conanfile_package_info_conf_and_env>`.

Define components for Conan packages that provide multiple libraries
--------------------------------------------------------------------

There are cases in which a Conan package may provide multiple libraries, for these cases
you can set the separate information for each of those libraries using the components
attribute from the :ref:`CppInfo<conan_conanfile_model_cppinfo_attributes>` object.

To know more about this use case, please check the :ref:`components
example<examples_conanfile_package_info_components>` in the examples section.


.. seealso::

    - :ref:`Propagating environment and configuration information to consumers example<examples_conanfile_package_info_conf_and_env>`
    - :ref:`Define components for Conan packages that provide multiple libraries example<examples_conanfile_package_info_components>`
    - :ref:`package_info() reference<reference_conanfile_methods_package_info>`
