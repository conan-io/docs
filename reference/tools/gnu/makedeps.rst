.. _conan_tools_gnu_makedeps:

MakeDeps
========

.. include:: ../../../common/experimental_warning.inc

.. _MakeDeps:

``MakeDeps`` is the dependencies generator for make. It generates a Makefile file named ``conandeps.mk``
containing a valid make file syntax with all dependencies listed, including their components.

This generator can be used by name in conanfiles:

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):
        generators = "MakeDeps"

.. code-block:: text
    :caption: conanfile.txt

    [generators]
    MakeDeps

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code:: python

    from conan import ConanFile
    from conan.tools.gnu import MakeDeps

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        requires = "zlib/1.2.13"

        def generate(self):
            pc = MakeDeps(self)
            pc.generate()


Generated files
---------------

`make` format file named ``conandeps.mk``, containing a valid makefile file syntax.
The ``prefix`` variable is automatically adjusted to the ``package_folder``:

.. code-block:: makefile

    CONAN_DEPS = zlib

    # zlib/1.2.13
    CONAN_NAME_ZLIB = zlib
    CONAN_VERSION_ZLIB = 1.2.13
    CONAN_REFERENCE_ZLIB = zlib/1.2.13
    CONAN_ROOT_ZLIB = /home/conan/.conan2/p/b/zlib273508b343e8c/p
    CONAN_INCLUDE_DIRS_ZLIB = $(CONAN_INCLUDE_DIR_FLAG)$(CONAN_ROOT_ZLIB)/include
    CONAN_LIB_DIRS_ZLIB = $(CONAN_LIB_DIR_FLAG)$(CONAN_ROOT_ZLIB)/lib
    CONAN_BIN_DIRS_ZLIB = $(CONAN_BIN_DIR_FLAG)$(CONAN_ROOT_ZLIB)/bin
    CONAN_LIBS_ZLIB = $(CONAN_LIB_FLAG)z

    CONAN_INCLUDE_DIRS = $(CONAN_INCLUDE_DIRS_ZLIB)
    CONAN_LIB_DIRS = $(CONAN_LIB_DIRS_ZLIB)
    CONAN_BIN_DIRS = $(CONAN_BIN_DIRS_ZLIB)
    CONAN_LIBS = $(CONAN_LIBS_ZLIB)

Properties
++++++++++

Makefile variables will be generated for each property set in `package_info()` of all dependencies and their components. Let's take following receipt:

.. code:: python

    from conan import ConanFile

    class MyLib(ConanFile):

        name = "mylib"
        version = "1.0"

        def package_info(self):
            self.cpp_info.set_property("my.prop", "some vale")
            self.cpp_info.components["mycomp"].set_property("comp_prop", "comp_value")

The resulting makefile variable assignments would look like this:

.. code-block:: makefile

    # mylib/1.0
    
    #[...]
    CONAN_PROPERTY_MYLIB_MY_PROP = some value
    CONAN_PROPERTY_MYLIB_MYCOMP_COMP_PROP = comp_value

When substituting package names, component names and property names into makefile variable names, the names are converted to uppercase and all characters except `A-Z`, `0-9` and `_` are replaced with `_` (see example above with a dot in the property name). The property value is not modified, it is put to the right side of the variable assignment literally. Any whitespace and special character remain unchagend, no quotation or escaping is applied, because GNU Make is not consistent in escaping spaces and cannot handle whitespaces in path names anyway. Because values with newlines would break the makefile they are skipped and a warning is displayed.


Customization
-------------

Flags
+++++

By default, the ``conandeps.mk`` will contain all dependencies listed, including their ``cpp_info`` information, but will not pass any flags to the compiler.

Thus, the consumer should pass the following flags to the compiler:

- **CONAN_LIB_FLAG**: Add a prefix to all libs variables, e.g. ``-l``
- **CONAN_DEFINE_FLAG**: Add a prefix to all defines variables, e.g. ``-D``
- **CONAN_SYSTEM_LIB_FLAG**: Add a prefix to all system_libs variables, e.g. ``-l``
- **CONAN_INCLUDE_DIR_FLAG**: Add a prefix to all include dirs variables, e.g. ``-I``
- **CONAN_LIB_DIR_FLAG**: Add a prefix to all lib dirs variables, e.g. ``-L``
- **CONAN_BIN_DIR_FLAG**: Add a prefix to all bin dirs variables, e.g. ``-L``

Those flags should be appended as prefixes to flags variables. For example, if the ``CONAN_LIB_FLAG`` is set to ``-l``, the ``CONAN_LIBS`` variable will be set to ``-lz``.

Reference
---------

.. currentmodule:: conan.tools.gnu

.. autoclass:: MakeDeps
    :members:
