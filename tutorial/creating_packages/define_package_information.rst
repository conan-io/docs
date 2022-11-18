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
    :emphasize-lines: 3

    def package_info(self):
        self.cpp_info.libs = ["hello"]


As you can see, we are just defining 


Providing environment information
---------------------------------

asdasd



Read more
---------

- ...
