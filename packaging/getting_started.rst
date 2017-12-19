.. _packaging_getting_started:

Getting started
===============

To start learning about creating packages, we will create a package from an existing source code repository:
https://github.com/memsharded/hello. You can check that project, it is a very simple "hello world" C++ library,
using CMake as build system to build a library and an executable. It has nothing related to conan in it.

We are using such github repository as an example, but the same process would apply to other source code origins,
like downloading a zip or tarball from the internet.

.. note::

    For this concrete example you will need, besides a C++ compiler, both *CMake* and *git* installed and in your path.
    They are not required by conan, you could use your own build system and version control instead.


Creating the package recipe
---------------------------

First, let's create a folder for our package recipe, and use the ``conan new`` helper command that will create
a working package recipe for us:

.. code-block:: bash

    $ mkdir mypkg && cd mypkg
    $ conan new Hello/0.1 -t


This will generate the following files:

::

    conanfile.py
    test_package
      conanfile.py
      CMakeLists.txt
      example.cpp


At the root level, there is a ``conanfile.py`` which is the main recipe file, the one actually defining our package.
Also there is a ``test_package`` folder, which contains a simple example consuming project that will require
and link with the created package. It is useful to make sure that our package is correctly created.

Let's have a look to the root package recipe ``conanfile.py``:

.. code-block:: python

    from conans import ConanFile, CMake, tools

    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False]}
        default_options = "shared=False"
        generators = "cmake"

        def source(self):
            self.run("git clone https://github.com/memsharded/hello.git")
            self.run("cd hello && git checkout static_shared")
            # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
            # if the packaged project doesn't have variables to set it properly
            tools.replace_in_file("hello/CMakeLists.txt", "PROJECT(MyHello)", '''PROJECT(MyHello)
    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()''')

        def build(self):
            cmake = CMake(self)
            cmake.configure(source_folder="hello")
            cmake.build()

            # Explicit way:
            # self.run('cmake %s/hello %s' % (self.source_folder, cmake.command_line))
            # self.run("cmake --build . %s" % cmake.build_config)

        def package(self):
            self.copy("*.h", dst="include", src="hello")
            self.copy("*hello.lib", dst="lib", keep_path=False)
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.so", dst="lib", keep_path=False)
            self.copy("*.dylib", dst="lib", keep_path=False)
            self.copy("*.a", dst="lib", keep_path=False)

        def package_info(self):
            self.cpp_info.libs = ["hello"]


This is a complete package recipe. Without worrying too much about every detail, these are the basics:

* The ``settings`` field defines the configuration that defines the different binary packages.
  In this example we are defining that any change to the OS, compiler, architecture or build type will
  generate a different binary package. Remember, Conan generates different binary packages for different
  introduced configuration (in this case settings) for the same recipe.

* This package recipe is also able to create different binary packages for static and shared libraries
  with the ``shared`` option, which is defaulted to False (i.e. by default it will use static linkage).

* The ``source()`` method executes a ``git clone`` to retrieve the sources from github.
  Other origins, as downloading a zip file are also available. As you can see, any manipulation of the
  code can be done, as checking out any branch or tag, or patching the source code. In this example,
  we are adding two lines to the existing CMake code, to ensure binary compatibility. Don't worry too
  much about it now, we'll visit it later.

* The ``build()`` first configures the project, then builds it, with standard CMake commands.
  The ``CMake`` object is just a helper to ease the translation of conan settings to CMake command line
  arguments. Also remember that **CMake is not strictly required**. You can build packages directly
  invoking **make**, **MSBuild**, **SCons** or any other build system.

* The ``package()`` method copies artifacts (headers, libs) from the build folder to the final package folder. 

* Finally, the ``package_info()`` method defines that consumer must link with the "hello" library
  when using this package. Other information as include or lib paths can be defined as well.
  This information is used for files created by generators to be used by consumers, as ``conanbuildinfo.cmake``


The test_package folder
-----------------------

.. note::

   The **test_package** is different from the library unit or integration tests, which should be more
   comprehensive. These tests are "package" tests, and validate that the package is properly
   created, and that package consumers will be able to link against it and reuse it.

If you have a look to the ``test_package`` folder, you will realize that the ``example.cpp`` and the
``CMakeLists.txt`` files don't have anything special. The ``test_package/conanfile.py`` file is just
another recipe, you can think of it as the consumer ``conanfile.txt`` we have already seen in previous sections:

.. code-block:: python

    from conans import ConanFile, CMake
    import os

    class HelloTestConan(ConanFile):
        settings = "os", "compiler", "build_type", "arch"
        generators = "cmake"

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

        def imports(self):
            self.copy("*.dll", dst="bin", src="bin")
            self.copy("*.dylib*", dst="bin", src="lib")

        def test(self):
            os.chdir("bin")
            self.run(".%sexample" % os.sep)


The main differences with the above ``conanfile.py`` are:

- It doesn't have a name and version, because we are not creating a package, so they are not necessary.
- The ``package()`` and ``package_info()`` methods are not required, since we are not creating a package.
- The ``test()`` method specifies which binaries have to be run.
- The ``imports()`` method is defined to copy shared libraries to the ``bin`` folder, so when dynamic
  linkage is used, and the ``test()`` method launches the ``example`` executable, they are found and ``example`` runs.

.. note::

    An important difference with respect to normal package recipes, is that this one does not need to declare a
    ``requires`` attribute, to depend on the ``Hello/0.1@demo/testing`` package we are testing. This ``requires``
    will be automatically injected by conan while running. You can however declare it explicitely, it will work,
    but you will have to remember to bump the version, and possibly the user and channel if you change them.


.. _creating_and_testing_packages:

Creating and testing packages
-----------------------------

We can create and test the package with our default settings simply by:

.. code-block:: bash

    $ conan create demo/testing
    ...
    Hello world!


If you see "Hello world!", it worked.

This will perform the following steps:

- Copy ("export" in conan terms) the ``conanfile.py`` from the user folder into the conan local cache.
- Install the package, forcing building it from sources.
- Move to the ``test_package`` folder, and create a temporary ``build`` folder.
- Execute there a ``conan install ..``, so it installs the requirements of the ``test_package/conanfile.py``.
  Note that it will build "Hello" from sources.
- Build and launch the ``example`` consuming application, calling the ``test_package/conanfile.py`` ``build()`` and
  ``test()`` methods respectively.

Using conan commands, the ``conan create`` command would be equivalent to:

.. code-block:: bash

    $ conan export demo/testing
    $ conan install Hello/0.1@demo/testing --build=Hello
    # package is created now, use test to test it
    $ conan test test_package Hello/0.1@demo/testing


The ``conan create`` command receives the same command line parameters as ``conan install`` so you
can pass to it the same settings, options, and command line switches. If you want to create and test
packages for different configurations, you could:

.. code-block:: bash

    $ conan create demo/testing -s build_type=Debug
    $ conan create demo/testing -o Hello:shared=True -s arch=x86
    $ conan create demo/testing -pr my_gcc49_debug_profile
    ...
    $ conan create ...


Any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write us</a>
