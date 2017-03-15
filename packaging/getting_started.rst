.. _packaging_getting_started:

Getting started
================

To start learning about creating packages, we will create a package from an existing source code repository: https://github.com/memsharded/hello. You can check that project, it is a very simple "hello world" C++ library, using CMake as build system to build a library and an executable. It has nothing related to conan in it. We are using such github repository as an example, but the same process would apply to other source code origins, like downloading a zip or tarball from the internet.

.. note::

    For this concrete example you will need, besides a C++ compiler, both CMake and git installed and in your path. They are not required by conan, you could use your own build system and version control instead.


Creating the package recipe
-----------------------------

First, let's create a folder for our package recipe, and use the ``conan new`` helper command that will create a working package recipe for us:

.. code-block:: bash

   $ mkdir mypkg && cd mypkg
   $ conan new Hello/0.1@demo/testing -t


This will generate the following files:

::

   conanfile.py
   test_package
      conanfile.py
      CMakeLists.txt
      example.cpp


At the root level, there is a ``conanfile.py`` which is the main recipe file, the one actually defining our package. Also a ``test_package`` folder, which contains a simple example consuming project that will require and link with the created package. It is useful to make sure that our package is correctly created.

Let`s have a look to the root package recipe ``conanfile.py``:

.. code-block:: python

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
            # patch to ensure compatibility
            tools.replace_in_file("hello/CMakeLists.txt", "PROJECT(MyHello)", '''PROJECT(MyHello)
    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()''')

        def build(self):
            cmake = CMake(self.settings)
            shared = "-DBUILD_SHARED_LIBS=ON" if self.options.shared else ""
            self.run('cmake hello %s %s' % (cmake.command_line, shared))
            self.run("cmake --build . %s" % cmake.build_config)

        def package(self):
            self.copy("*.h", dst="include", src="hello")
            self.copy("*.lib", dst="lib", keep_path=False)
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.so", dst="lib", keep_path=False)
            self.copy("*.a", dst="lib", keep_path=False)

        def package_info(self):
            self.cpp_info.libs = ["hello"]


This is a complete package recipe. Without worrying too much about every detail, these are the basics:

* The ``settings`` field defines the configuration that defines the different binary packages. In this example we are defining that any change to the OS, compiler, architecture or build type will generate a different package binary. 

* This package recipe is also able to create different package binaries for static and shared libraries with the ``shared`` option, which is defaulted to False (i.e. by default it will use static linkage). 

* The ``source()`` method executes a ``git clone`` to retrieve the sources from github. Other origins, as downloading a zip file are also possible. As you can see, any manipulation of the code can be done, as checking out any branch or tag, or patching the source code. In this example, we are adding two lines to the existing CMake code, to ensure binary compatibility. Don't worry too much about it now, we'll visit it later.

* The ``build()`` first configures the project, then builds it, with standard CMake commands. The ``CMake`` object is just a helper to easy the translation of conan settings to CMake command line arguments. Also remember that **CMake is not strictly required**. You can build packages directly invoking **make**, **MSBuild**, **SCons** or any other build system.

* The ``package()`` method copies artifacts (headers, libs) from the build folder to the final package folder. 

* Finally, the ``package_info()`` method defines that consumer must link with the "hello" library when using this package. Other information as include or lib paths can be defined as well. This information is used for files created by generators to be used by consumers, as ``conanbuildinfo.cmake``



The test_package folder
-----------------------------

.. note::

   The **test_package** is different from the library unit or integration tests, which should be more
   comprehensive. These tests are "package" tests, and validate that the package is properly
   created, and that package consumers will be able to link against it and reuse it.

If you have a look to the ``test_package`` folder, you will realize that the ``example.cpp`` and the ``CMakeLists.txt`` files don't have anything special. Then the ``test_package/conanfile.py`` file, is just another recipe, you can think of it as the consumer ``conanfile.txt`` we have already seen in previous sections:


.. code-block:: python

    channel = os.getenv("CONAN_CHANNEL", "testing")
    username = os.getenv("CONAN_USERNAME", "demo")

    class HelloTestConan(ConanFile):
        settings = "os", "compiler", "build_type", "arch"
        requires = "Hello/0.1@%s/%s" % (username, channel)
        generators = "cmake"

        def imports(self):
            self.copy("*.dll", "bin", "bin")
            self.copy("*.dylib", "bin", "bin")

        def test(self):
            os.chdir("bin")
            self.run(".%sexample" % os.sep)

The main differences with the above ``conanfile.py`` are:

- It doesn't have a name and version, because we are not creating a package, so they are not necessary.
- It defines a ``requires`` field, that points to our package ``Hello/0.1@demo/testing``. This is exactly the same as the ``[requires]`` field of ``conanfile.txt``
- The ``package()`` and ``package_info()`` methods are not required, since we are not creating a package.
- The ``test()`` method specifies which binaries have to be run.
- The ``imports()`` method is defined to copy shared libraries to the ``bin`` folder, so when dynamic linkage is used, and the ``test()`` method launches the ``example`` executable, they are found and ``example`` runs.


Creating and testing packages
-------------------------------

We can create and test the package with our default settings simply by:

.. code-block:: bash

   $ conan test_package
   ...
   Hello world!


If you see "Hello world!", it worked.

This will perform the following steps:

- Copy ("export" in conan terms) the ``conanfile.py`` from the user folder into the conan local cache.
- Move to the ``test_package`` folder, and create a temporary ``build`` folder.
- Execute there a ``conan install .. --build=Hello``, so it installs the requirements of the ``test_package/conanfile.py``. Note that it will build Hello from sources
- Build and launch the ``example`` consuming application, calling the ``test_package/conanfile.py`` ``build()`` and ``test()`` methods respectively



This command uses the ``--build=Hello`` option by default, i.e. it always re-builds the package.
If you just want to check if the package is properly created, but don't want to re-build it, use the ``--build=missing`` option:

.. code-block:: bash

   $ conan test_package --build=missing
   ...
   Hello world!
   
The ``conan test_package`` command receives the same command line parameters as ``conan install`` so you can pass to it the same settings, options, and command line switches. So if you want to create and test packages for different configurations, you could:

.. code-block:: bash

   $ conan test_package -s build_type=Debug
   $ conan test_package -o Hello:shared=True -s arch=x86
   ...
   $ conan test_package ...


Any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write us</a>
