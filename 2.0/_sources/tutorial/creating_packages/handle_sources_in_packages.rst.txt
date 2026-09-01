.. _creating_packages_handle_sources_in_packages:

Handle sources in packages
==========================

In the :ref:`previous tutorial section<creating_packages_create_your_first_conan_package>`
we created a Conan package for a "Hello World" C++ library. We used the
``exports_sources`` attribute of the Conanfile to declare the location of the sources for
the library. This method is the simplest way to define the location of the source files
when they are in the same folder as the Conanfile. However, sometimes the source files are
stored in a repository or a file in a remote server, and not in the same location as the
Conanfile. In this section, we will modify the recipe we created previously by adding a
``source()`` method and explain how to:

* Retrieve the sources from a *zip* file stored in a remote repository.
* Retrieve the sources from a branch of a *git* repository.

Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/handle_sources

The structure of the project is the same as the one in the previous example but without
the library sources:

.. code-block:: text

    .
    ├── CMakeLists.txt
    ├── conanfile.py
    └── test_package
        ├── CMakeLists.txt
        ├── conanfile.py
        └── src
            └── example.cpp

Sources from a *zip* file stored in a remote repository
-------------------------------------------------------

Let's have a look at the changes in the *conanfile.py*:

.. code-block:: python

    from conan import ConanFile
    from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
    from conan.tools.files import get


    class helloRecipe(ConanFile):
        name = "hello"
        version = "1.0"

        ...

        # Binary configuration
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False], "fPIC": [True, False]}
        default_options = {"shared": False, "fPIC": True}

        def source(self):
            # Please, be aware that using the head of the branch instead of an immutable tag
            # or commit is a bad practice and not allowed by Conan
            get(self, "https://github.com/conan-io/libhello/archive/refs/heads/main.zip", 
                      strip_root=True)

        def config_options(self):
            if self.settings.os == "Windows":
                del self.options.fPIC

        def layout(self):
            cmake_layout(self)

        def generate(self):
            tc = CMakeToolchain(self)
            tc.generate()

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

        def package(self):
            cmake = CMake(self)
            cmake.install()

        def package_info(self):
            self.cpp_info.libs = ["hello"]

As you can see, the recipe is the same but instead of declaring the ``exports_sources``
attribute as we did previously, i.e.

.. code-block:: python

    exports_sources = "CMakeLists.txt", "src/*", "include/*"


we declare a ``source()`` method with this information:

.. code-block:: python

    def source(self):
        # Please, be aware that using the head of the branch instead of an immutable tag
        # or commit is strongly discouraged, unsupported by Conan and likely to cause issues
        get(self, "https://github.com/conan-io/libhello/archive/refs/heads/main.zip", 
                  strip_root=True)

We used the :ref:`conan.tools.files.get()<conan_tools_files_get>` tool that will first
**download** the *zip* file from the URL that we pass as an argument and then **unzip**
it. Note that we pass the ``strip_root=True`` argument so that if all the unzipped
contents are in a single folder, all the contents are moved to the parent folder (check
the :ref:`conan.tools.files.unzip()<conan_tools_files_unzip>` reference for more details).

.. warning::

    It is expected that retrieving the sources in the future produces the same results. Using mutable source origins, like a moving reference in git (e.g HEAD branch), or the URL to a file where the contents may change over time, is strongly discouraged and not supported. Not following this practice will result in undefined behavior likely to cause breakages


The contents of the zip file are the same as the sources we previously had beside the
Conan recipe, so if you do a :command:`conan create` the results will be the
same as before.

.. code-block:: text
    :emphasize-lines: 8-13

    $ conan create .

    ...

    -------- Installing packages ----------

    Installing (downloading, building) binaries...
    hello/1.0: Calling source() in /Users/user/.conan2/p/0fcb5ffd11025446/s/.
    Downloading update_source.zip

    hello/1.0: Unzipping 3.7KB
    Unzipping 100 %                                                       
    hello/1.0: Copying sources to build folder
    hello/1.0: Building your package in /Users/user/.conan2/p/tmp/369786d0fb355069/b

    ...

    -------- Testing the package: Running test() ----------
    hello/1.0 (test package): Running test()
    hello/1.0 (test package): RUN: ./example
    hello/1.0: Hello World Release!
    hello/1.0: __x86_64__ defined
    hello/1.0: __cplusplus199711
    hello/1.0: __GNUC__4
    hello/1.0: __GNUC_MINOR__2
    hello/1.0: __clang_major__13
    hello/1.0: __clang_minor__1
    hello/1.0: __apple_build_version__13160021

Please, check the highlighted lines with the messages about the download and unzip operation.


Sources from a branch in a *git* repository
-------------------------------------------

Now, let's modify the ``source()`` method to bring the sources from a *git* repository
instead of a *zip* file. We show just the relevant parts:

.. code-block:: python

    ...

    from conan.tools.scm import Git


    class helloRecipe(ConanFile):
        name = "hello"
        version = "1.0"

        ...

        def source(self):
            git = Git(self)
            git.clone(url="https://github.com/conan-io/libhello.git", target=".")

        ...


Here, we use the :ref:`conan.tools.scm.Git()<reference>` tool. The ``Git`` class
implements several methods to work with *git* repositories. In this case, we call the clone
method to clone the `<https://github.com/conan-io/libhello.git>`_ repository in the
default branch using the same folder for cloning the sources instead of a subfolder
(passing the ``target="."`` argument). 


.. warning::

    As above, this is only a simple example. The source origin for ``Git()`` also has to be immutable, it is necessary to checkout out an immutable tag or a specific commit to guarantee the correct behavior. Using the HEAD of the repository is not allowed and can cause undefined behavior and breakages.

To checkout a commit or tag in the repository we use the ``checkout()``
method of the Git tool:

.. code-block:: python

    def source(self):
        git = Git(self)
        git.clone(url="https://github.com/conan-io/libhello.git", target=".")
        git.checkout("<tag> or <commit hash>")

For more information about the ``Git`` class methods, please check the
:ref:`conan.tools.scm.Git()<reference>` reference.

Note that it's also possible to run other commands by invoking the ``self.run()`` method.


.. _creating_packages_handle_sources_in_packages_conandata:

Using the conandata.yml file
----------------------------

We can write a file named ``conandata.yml`` in the same folder of the ``conanfile.py``.
This file will be automatically exported and parsed by Conan and we can read that information from the recipe.
This is handy for example to extract the URLs of the external sources repositories, zip files etc.
This is an example of ``conandata.yml``:

.. code-block:: yaml

    sources:
      "1.0":
        url: "https://github.com/conan-io/libhello/archive/refs/heads/main.zip"
        sha256: "7bc71c682895758a996ccf33b70b91611f51252832b01ef3b4675371510ee466"
        strip_root: true
      "1.1":
        url: ...
        sha256: ...


The recipe doesn't need to be modified for each version of the code. We can pass all the ``keys`` of the specified version
(``url``, ``sha256``, and ``strip_root``) as arguments to the ``get`` function, that, in this case, allow us to verify that the downloaded
zip file has the correct ``sha256``. So we could modify the source method to this:


.. code-block:: python

    def source(self):
        get(self, **self.conan_data["sources"][self.version])
        # Similar to:
        # data = self.conan_data["sources"][self.version]
        # get(self, data["url"], sha256=data["sha256"], strip_root=data["strip_root"])



Read more
---------

- :ref:`Patching sources<examples_tools_files_patches>`
- :ref:`Capturing Git SCM source information<examples_tools_scm_git_capture>` instead of copying sources with ``exports_sources``.
- ...

.. seealso::

    - :ref:`source() method reference<reference_conanfile_methods_source>`
