

Patching sources
================


In this example we are going to see how to patch the source code. This is necessary sometimes, specially when you are
creating a package for a third party library. A patch might be required in the build system scripts or even in the
source code of the library if you want, for example, to apply a security patch.

Please, first clone the sources to recreate this project. You can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples/tools/files/patches


Patching using 'replace_in_file'
================================

The simplest way to patch a file is using the ``replace_in_file`` tool in your recipe. It searches in a file the specified
string and replace it with other string.

in source() method
^^^^^^^^^^^^^^^^^^

The source() method is called only once for all the configurations (different calls to ``conan create`` for different settings/options)
so you should patch only in the ``source()`` method if the changes are common for all the configurations.

Look at the ``source()`` method at the ``conanfile.py``:


.. code-block:: python

    import os
    from conan import ConanFile
    from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
    from conan.tools.files import get, replace_in_file


    class helloRecipe(ConanFile):
        name = "hello"
        version = "1.0"

        # Binary configuration
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False], "fPIC": [True, False]}
        default_options = {"shared": False, "fPIC": True}

        def source(self):
            get(self, "https://github.com/conan-io/libhello/archive/refs/heads/main.zip", strip_root=True)
            replace_in_file(self, os.path.join(self.source_folder, "src", "hello.cpp"), "Hello World", "Hello Friends!")

        ...

We are replacing the ``"Hello World"`` string with "Hello Friends!". We can run ``conan create .`` and verify that
if the replace was done:

.. code-block:: bash

    $ conan create .
    ...
    -------- Testing the package: Running test() --------
    hello/1.0: Hello Friends! Release!
    ...

in build() method
^^^^^^^^^^^^^^^^^

In this case, we need to apply a different patch depending on the configuration (`self.settings`, `self.options`...),
so it has to be done in the ``build()`` method. Let's modify the recipe to introduce a change that depends on the
``self.options.shared``:


.. code-block:: python

    class helloRecipe(ConanFile):

        ...

        def source(self):
            get(self, "https://github.com/conan-io/libhello/archive/refs/heads/main.zip", strip_root=True)

        def build(self):
            replace_in_file(self, os.path.join(self.source_folder, "src", "hello.cpp"),
                            "Hello World",
                            "Hello {} Friends!".format("Shared" if self.options.shared else "Static"))
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

        ...

If we call ``conan create`` with different ``option.shared`` we can check the output:

.. code-block:: bash

    $ conan create .
    ...
    hello/1.0: Hello Static Friends! Release!
    ...

    $ conan create . -o shared=True
    ...
    hello/1.0: Hello Shared Friends! Debug!
    ...


Patching using "patch" tool
===========================



Patching using "apply_conandata_patches" tool
=============================================

