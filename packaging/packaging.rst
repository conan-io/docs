.. _understand_packaging:

Understanding packaging
========================

Manual package creation and testing
---------------------------------------

The previous ``test_package`` approach is not strictly necessary, though **very strongly recommended**.
If we didn't want to use the ``test_package`` functionality, we could just write our recipe ourselves or use the ``conan new`` command without the ``-t`` command line argument.

.. code-block:: bash

   $ mkdir mypkg && cd mypkg
   $ conan new Hello/0.1@demo/testing

This will create just the ``conanfile.py`` recipe file. This file can be introduced in the conan local cache with:

.. code-block:: bash

    $ conan export demo/testing

Once the recipe is there, it can be consumed like any other package, just add ``Hello/0.1@demo/testing`` to some project ``conanfile.txt`` or ``conanfile.py`` requirements and run:

.. code-block:: bash

    $ conan install . --build=missing
    # build and run your project to ensure the package works


Packaging from the source project
-----------------------------------

In the previous package we implemented a ``source()`` method that fetched the source code from github. An alternative approach would be embedding the source code into the package recipe, so it is self-contained and it doesn't require to fetch code from external origins when it is necessary to build from sources.

This could be an appropriate approach if we want the package recipe to live in the same repository as the source code it is packaging. It could be considered as a "snapshot" of the source code too.

First, let's get the initial source code and create the basic package recipe:

.. code-block:: bash

   $ conan new Hello/0.1@demo/testing -t
   $ git clone https://github.com/memsharded/hello.git
   $ cd hello && git checkout static_shared

Now lets modify the ``conanfile.py`` to the following:

.. code-block:: python

    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False]}
        default_options = "shared=False"
        generators = "cmake"
        export_sources = "hello/*"

        def source(self):
            # patch to ensure compatibility
            tools.replace_in_file("hello/CMakeLists.txt", "PROJECT(MyHello)", '''PROJECT(MyHello)
    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()''')

There are two changes:

- Added the ``exports_sources`` field, to tell conan to copy all the files from the user cloned "hello" folder into the package recipe.
- Removed the ``git clone`` commands, now it is not necessary to fetch the source code from github, as the code has been already stored into the recipe.

And simply create the package as previously:

.. code-block:: bash

   $ conan test_package
   ...
   Hello world!
   ERROR: ... while executing example

If you see "Hello world!", the process **has worked OK**, the error message is a request to the user to implement their own test.


The package creation process
------------------------------

It is very useful for package creators and conan users in general to understand the flow of package creation inside the conan local cache, and its layout.

For every package recipe, there are 4 important folders in the conan local cache:

- **export**: The folder where the package recipe is stored.
- **source**: Where the source code for building from sources is stored.
- **build**: Where the actual compilation of sources is done. There will typically be one subfolder for each different binary configuration
- **package**: Where the final package artifacts are stored. There will be one subfolder for each different binary configuration

The "source" and "build" folders only exist when the packages have been built from sources.

.. image:: /images/package_create_flow.png
    :height: 500 px
    :width: 600 px
    :align: center


The process starts when a package is "exported", via the ``conan export`` command or more typically, with the ``conan test_package`` command. The conanfile.py and files especified by the ``exports_sources`` field are copied from the user space into the conan local cache.

The "export" files are copied to the "source" folder, and then the ``source()`` method is executed (if existing). Note that there is only one source folder for all the binary packages. If some source code is to be generated that will be different for different configurations, it cannot be generated in the ``source()`` method, it has to be done in the ``build()`` method.

Then, for each different configuration of settings and options, a package ID will be computed in the form of a SHA-1 hash of such configuration. Sources will be copied to the "build/hashXXX" folder, and the ``build()`` method will be triggered.

After that, the ``package()`` method will be called to copy artifacts from the "build/hashXXX" folder to the "package/hashXXX" folder.

Finally, the ``package_info()`` methods of all dependencies will be called and gathered to be able to generate files for the consumer build system, as the ``conanbuildinfo.cmake`` for the ``cmake`` generator. Also the ``imports`` feature will copy artifacts from the local cache into user space if specified.



Any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write us</a>
