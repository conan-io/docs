Define the package information for consumers
============================================

In the previous tutorial section we explained how to store the
headers and binaries of a library in a Conan package. These files are reused by consumers
that depend on the package but we have to provide some additional information so that
Conan can pass that to the build system and consumers can compile and link against our
package.

For instance, in our example we are building a static library with name *hello* that once
it's built will result in a *libhello.a* in Linux and MacOS or *hello.lib* in Windows.
Also, we are packaging a header file *hello.h* with the declaration of the library
functions. The Conan package ends up with the following structure in the Conan local cache:

.. code-block:: text

    .
    ├── include
    │   └── hello.h
    └── lib
        └── libhello.a

Then, consumers that want to link against this library will need to have some information:

- Add the *include* folder in the Conan local cache to the locations to search for the
  *hello.h* file
- We have to link agains a library named *libhello.a*
- That library is in a folder named *lib* in the Conan local cache.

Conan provides an abstraction over all this information with the
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

- We are not adding anything specific for the *lib* or *include* folders where the library
  and headers files are packaged. The ``cpp_info`` object has the ``.includedirs`` and
  ``.libdirs`` properties to define those locations but Conan sets their value as *lib*
  and *include* by default so it's not needed to add those in this case. If you were
  copying the package files to a different location then you should set those explicitly.
  The declaration of the ``package_info`` method in our Conan package would be completely
  equivalent to this one:

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
also other typical use cases, like for examples:

- Define information for consumers depending on settings or options
- Customizing certain the information that generators produce for consumers, things like
  the target names for CMake or the generated files names for pkg-config
- Propagating configuration values to consumers
- Propagating environment information to consumers

Let's see some of those. First, clone the project sources again. You can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/package_information


For this section of the tutorial we introduced some changes in the library and recipe.
Let's check the relevant parts:


Changes introduced in the library sources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First, please note that we are using `another branch
<https://github.com/conan-io/libhello/tree/package_info>`_ from the **libhello** library.
Let's check the *CMakeLists.txt* to build the library:


.. code-block:: text
    :caption: *CMakeLists.txt*
    :emphasize-lines: 8,12

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

As you can see, now we are setting the output name for the library depending on if the
library is static or shared. Now let's see how these changes affect the information that
we have to set in the Conan recipe for consumers.


Changes introduced in the recipe
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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




Properties model: setting information for specific generators
-------------------------------------------------------------



First, please note that we are using `another branch
<https://github.com/conan-io/libhello/tree/with_tests>`_ from the **libhello** library. This
branch has two novelties on the library side:


- Package to another place. Imagine that we are packaging our library files in other place... let's see how to change that...
Add flags, defines, system_libs...
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