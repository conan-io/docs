.. _examples_tools_files_patches:

Patching sources
================

In this example we are going to see how to patch the source code. This is necessary sometimes, specially when you are
creating a package for a third party library. A patch might be required in the build system scripts or even in the
source code of the library if you want, for example, to apply a security patch.

Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples/tools/files/patches


Patching using 'replace_in_file'
--------------------------------

The simplest way to patch a file is using the ``replace_in_file`` tool in your recipe. It searches in a file the specified
string and replaces it with another string.

in source() method
^^^^^^^^^^^^^^^^^^

The source() method is called only once for all the configurations (different calls to :command:`conan create` for different settings/options)
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

We are replacing the ``"Hello World"`` string with "Hello Friends!".
We can run ``conan create .`` and verify that if the replace was done:

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
---------------------------

If you have a patch file (diff between two versions of a file), you can use the ``conan.tools.files.patch`` tool to apply it.
The rules about where to apply the patch (``source()`` or ``build()`` methods) are the same.

We have this patch file, where we are changing again the message to say "Hello Patched World Release!":


.. code-block:: text

    --- a/src/hello.cpp
    +++ b/src/hello.cpp
    @@ -3,9 +3,9 @@

     void hello(){
         #ifdef NDEBUG
    -    std::cout << "hello/1.0: Hello World Release!\n";
    +    std::cout << "hello/1.0: Hello Patched World Release!\n";
         #else
    -    std::cout << "hello/1.0: Hello World Debug!\n";
    +    std::cout << "hello/1.0: Hello Patched World Debug!\n";
         #endif

         // ARCHITECTURES


Edit the ``conanfile.py`` to:

1. Import the ``patch`` tool.
2. Add ``exports_sources`` to the patch file so we have it available in the cache.
3. Call the ``patch`` tool.


.. code-block:: python
    :emphasize-lines: 4, 15, 19, 20

    import os
    from conan import ConanFile
    from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
    from conan.tools.files import get, replace_in_file, patch


    class helloRecipe(ConanFile):
        name = "hello"
        version = "1.0"

        # Binary configuration
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False], "fPIC": [True, False]}
        default_options = {"shared": False, "fPIC": True}
        exports_sources = "*.patch"

        def source(self):
            get(self, "https://github.com/conan-io/libhello/archive/refs/heads/main.zip", strip_root=True)
            patch_file = os.path.join(self.export_sources_folder, "hello_patched.patch")
            patch(self, patch_file=patch_file)

        ...

We can run "conan create" and see that the patch worked:

.. code-block:: bash

    $ conan create .
    ...
    -------- Testing the package: Running test() --------
    hello/1.0: Hello Patched World Release!
    ...


We can also use the ``conandata.yml`` :ref:`introduced in the tutorial<creating_packages_handle_sources_in_packages_conandata>` so we
can declare the patches to apply for each version:


.. code-block:: yaml

    patches:
      "1.0":
        - patch_file: "hello_patched.patch"


And there are the changes we introduce in the ``source()`` method:


.. code-block:: python

    .. code-block:: python

        def source(self):
            get(self, "https://github.com/conan-io/libhello/archive/refs/heads/main.zip", strip_root=True)
            patches = self.conan_data["patches"][self.version]
            for p in patches:
                patch_file = os.path.join(self.export_sources_folder, p["patch_file"])
                patch(self, patch_file=patch_file)


Check :ref:`patch <conan_tools_files_patch>` for more details.


If we run the :command:`conan create`, the patch is also applied:

.. code-block:: bash

    $ conan create .
    ...
    -------- Testing the package: Running test() --------
    hello/1.0: Hello Patched World Release!
    ...

Patching using "apply_conandata_patches" tool
---------------------------------------------

The example above works but it is a bit complex. If you follow the same yml structure (check the
:ref:`apply_conandata_patches <conan_tools_files_apply_conandata_patches>` to see the full supported yml) you
only need to call ``apply_conandata_patches``:


.. code-block:: python

    from conan import ConanFile
    from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
    from conan.tools.files import get, apply_conandata_patches


    class helloRecipe(ConanFile):
        name = "hello"
        version = "1.0"

        ...

        def source(self):
            get(self, "https://github.com/conan-io/libhello/archive/refs/heads/main.zip", strip_root=True)
            apply_conandata_patches(self)


Let's check if the patch is also applied:

.. code-block:: bash

    $ conan create .
    ...
    -------- Testing the package: Running test() --------
    hello/1.0: Hello Patched World Release!
    ...
