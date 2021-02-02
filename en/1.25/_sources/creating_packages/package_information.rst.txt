.. _package_information:

Define the package information
==============================

When creating a recipe to package a library, it is important to define the information about the package so consumers can get the
information correctly. Conan achieves this by decoupling the information of the package from the format needed using
:ref:`generators_reference`, that translate the generic information into the appropriate format file.

This generic information is defined inside the recipe, using the :ref:`method_package_info` method. There you can declare package information
like the location of the header files, library names, defines, flags...

.. code-block:: python

    from conans import ConanFile

    class MyConan(ConanFile):
        name = "cool_library"
        ...

        def package_info(self):
            self.cpp_info.includedirs = ["include/cool"]
            self.cpp_info.libs = ["libcool"]
            self.cpp_info.defines= ["DEFINE_COOL=1"]

The package information is done using the attributes of the :ref:`cpp_info_attributes_reference` object. This information will be aggregated
by Conan and exposed via ``self.deps_cpp_info`` to consumers and generators.

.. important::

    This information is important as it describes the package contents in a generic way with a pretty straightforward syntax that can later
    be translated to a suitable format. The advantage of having this information here, is that the package could be consumed from a
    different build system that the one used to compile the library. For example, a library that builds using Autotools can be consumed
    later in CMake with this information using any of the CMake generators.

.. seealso::

    Read :ref:`method_package_info` to learn more about this method.

.. _package_information_components:

Using Components
----------------

If your package contains more than one library or you want to define separated components so consumers can have more granular information,
you can use components in your :ref:`method_package_info` method.

.. warning::

    This is a **experimental** feature subject to breaking changes in future releases.

When you are creating a Conan package, it is recommended to have only one library (*.lib*, *.a*, *.so*, *.dll*...) per package. However,
especially with third-party projects like Boost, Poco or OpenSSL, they would contain several libraries inside.

Usually those libraries inside the same package depend on each other and modelling the relationship among them is required.

With **components**, you can model libraries and executables inside the same package and how one depends on the other. Each library or
executable will be one component inside ``cpp_info`` like this:

.. code-block:: python

    def package_info(self):
        self.cpp_info.name = "OpenSSL"
        self.cpp_info.components["crypto"].names["cmake_find_package"] = "Crypto"
        self.cpp_info.components["crypto"].libs = ["libcrypto"]
        self.cpp_info.components["crypto"].defines = ["DEFINE_CRYPTO=1"]
        self.cpp_info.components["ssl"].names["cmake"] = "SSL"
        self.cpp_info.components["ssl"].includedirs = ["include/headers_ssl"]
        self.cpp_info.components["ssl"].libs = ["libssl"]
        self.cpp_info.components["ssl"].requires = ["crypto"]

You can define dependencies among different components using the ``requires`` attribute and the name of the component. The dependency graph
for components will be calculated and values will be aggregated in the correct order for each field.

.. code-block:: python

    def package_info(self):
        self.cpp_info.components["LibA"].libs = ["liba"]      # Name of the library for the 'LibA' component
        self.cpp_info.components["LibA"].requires = ["LibB"]  # Requires point to the name of the component

        self.cpp_info.components["LibB"].libs = ["libb"]

        self.cpp_info.components["LibC"].libs = ["libc"]
        self.cpp_info.components["LibC"].requires = ["LibA"]

        self.cpp_info.components["LibD"].libs = ["libD"]
        self.cpp_info.components["LibD"].requires = ["LibA"]

        self.cpp_info.components["LibE"].libs = ["libe"]
        self.cpp_info.components["LibE"].requires = ["LibB"]

        self.cpp_info.components["LibF"].libs = ["libf"]
        self.cpp_info.components["LibF"].requires = ["LibD", "LibE"]

For consumers and generators, the order of the libraries from this components graph will be:

.. code-block:: python

        self.deps_cpp_info.libs == ["libf", "libe", "libd", "libc", "liba", "libb"]

Declaration of requires from other packages is also allowed:

.. code-block:: python

    class MyConan(ConanFile):
        ...
        requires = "zlib/1.2.11", "openssl/1.1.1g"

    def package_info(self):
        self.cpp_info.components["comp1"].requires = ["zlib::zlib"]             # Depends on all components in zlib package
        self.cpp_info.components["comp2"].requires = ["comp1", "openssl::ssl"]  # Depends on ssl component in openssl package

By default, components **won't link against any other package required by the recipe**. The requires list has to be **populated explicitly**
with the list of components from other packages to use: it can be the full requirement (``zlib::zlib``) or a single component
(``openssl::ssl``).

.. important::

    Components information is still not available from the generators' side. We are planning to complete this feature in next releases.

    Currently, the information of components is not lost but aggregated to the *global* scope and the usage of components should be
    transparent right now.

.. seealso::

    Read :ref:`components reference <cpp_info_attributes_reference>` for more information.
