.. _packaging_getting_started:

Getting Started
===============

To start learning about creating packages, we will create a package from the existing source code
repository: https://github.com/memsharded/hello. You can check that project, it is a very simple
"hello world" C++ library, using CMake as the build system to build a library and an executable. It does not contain
any association with Conan.

We are using a similar GitHub repository as an example, but the same process also applies to other source
code origins, like downloading a zip or tarball from the internet.

.. note::

    For this concrete example you will need, besides a C++ compiler, both *CMake* and *git*
    installed and in your path. They are not required by Conan, so you could use your own build system
    and version control instead.

Creating the Package Recipe
---------------------------

First, let's create a folder for our package recipe, and use the :command:`conan new` helper command that
will create a working package recipe for us:

.. code-block:: bash

    $ mkdir mypkg && cd mypkg
    $ conan new Hello/0.1 -t

This will generate the following files:

.. code-block:: text

    conanfile.py
    test_package
      CMakeLists.txt
      conanfile.py
      example.cpp

On the root level, there is a *conanfile.py* which is the main recipe file, responsible for
defining our package. Also, there is a *test_package* folder, which contains a simple example
consuming project that will require and link with the created package. It is useful to make sure
that our package is correctly created.

Let's have a look at the root package recipe *conanfile.py*:

.. code-block:: python

    from conans import ConanFile, CMake, tools

    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"
        license = "<Put the package license here>"
        url = "<Package recipe repository url here, for issues about the package>"
        description = "<Description of Hello here>"
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False]}
        default_options = {"shared": False}
        generators = "cmake"

        def source(self):
            self.run("git clone https://github.com/memsharded/hello.git")
            self.run("cd hello && git checkout static_shared")
            # This small hack might be useful to guarantee proper /MT /MD linkage
            # in MSVC if the packaged project doesn't have variables to set it
            # properly
            tools.replace_in_file("hello/CMakeLists.txt", "PROJECT(MyHello)",
                                  '''PROJECT(MyHello)
    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()''')

        def build(self):
            cmake = CMake(self)
            cmake.configure(source_folder="hello")
            cmake.build()

            # Explicit way:
            # self.run('cmake %s/hello %s'
            #          % (self.source_folder, cmake.command_line))
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

This is a complete package recipe. Without going into detail, these are the
basics:

- The ``settings`` field defines the configuration of the different binary packages. In
  this example, we defined that any change to the OS, compiler, architecture or build type will
  generate a different binary package. Please note that Conan generates different binary packages for
  different introduced configuration (in this case settings) for the same recipe.

  Note that the platform on which the recipe is running and the package being built differ from
  the final platform where the code will be running (``self.settings.os`` and ``self.settings.arch``) if
  the package is being cross-built. So if you want to apply a different build depending on the current
  build machine, you need to check it:

  .. code-block:: python

         def build(self):
             if platform.system() == "Windows":
                 cmake = CMake(self)
                 cmake.configure(source_folder="hello")
                 cmake.build()
             else:
                 env_build = AutoToolsBuildEnvironment(self)
                 env_build.configure()
                 env_build.make()

  Learn more in the :ref:`Cross building <cross_building>` section.

- This package recipe is also able to create different binary packages for static and shared
  libraries with the ``shared`` option, which is set by default to ``False`` (i.e. by default it will use
  static linkage).

- The ``source()`` method executes a :command:`git clone` to retrieve the sources from Github. Other
  origins, such as downloading a zip file are also available. As you can see, any manipulation of the
  code can be done, such as checking out any branch or tag, or patching the source code. In this example,
  we are adding two lines to the existing CMake code, to ensure binary compatibility. Don't worry
  about it now, we'll deal with it later.

- The ``build()`` configures the project, and then proceeds to build it using standard CMake commands. The
  ``CMake`` object just assists to translate the Conan settings to CMake command line
  arguments. Please note that **CMake is not strictly required**. You can build packages directly
  by invoking **make**, **MSBuild**, **SCons** or any other build system.

  .. seealso:: Check the :ref:`existing build helpers <build_helpers>`.

- The ``package()`` method copies artifacts (headers, libs) from the build folder to the final
  package folder. 

- Finally, the ``package_info()`` method defines that the consumer must link with the "hello" library
  when using this package. Other information as include or lib paths can be defined as well. This
  information is used for files created by generators to be used by consumers, as
  *conanbuildinfo.cmake*.

.. note::

    When writing your own *conanfile.py* references, please bear in mind that you should follow the rules in
    :ref:`conanfile_reference`

The test_package Folder
-----------------------

.. note::

    The **test_package** differs from the library unit or integration tests, which should be
    more comprehensive. These tests are "package" tests, and validate that the package is properly
    created, and that the package consumers will be able to link against it and reuse it.

If you look at the ``test_package`` folder, you will realize that the ``example.cpp`` and the
``CMakeLists.txt`` files don't have unique characteristics. The *test_package/conanfile.py* file is just
another recipe, that can be perceived as a consumer *conanfile.txt* that has been displayed in
previous sections:

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

The *conanfile.py* described above has the following characteristics:

- It doesn't have a name and version, as we are not creating a package so they are not
  necessary.
- The ``package()`` and ``package_info()`` methods are not required since we are not creating a
  package.
- The ``test()`` method specifies which binaries need to run.
- The ``imports()`` method is set to copy the shared libraries to the ``bin`` folder. When
  dynamic linking is applied, and the ``test()`` method launches the ``example`` executable, they are
  found causing the ``example`` to run.

.. note::

    An important difference with respect to standard package recipes is that you don't have
    to declare a ``requires`` attribute to depend on the tested ``Hello/0.1@demo/testing`` package
    as the ``requires`` will automatically be injected by Conan during the run. However, if you choose to
    declare it explicitly, it will work, but you will have to remember to bump the version,
    and possibly also the user and channel if you decide to change them.

.. _creating_and_testing_packages:

Creating and Testing Packages
-----------------------------

You can create and test the package with our default settings simply by running:

.. code-block:: bash

    $ conan create . demo/testing
    ...
    Hello world!

If "Hello world!" is displayed, it worked.

The :command:`conan create` command does the following:

- Copies ("export" in Conan terms) the *conanfile.py* from the user folder into the **local cache**.
- Installs the package, forcing it to be built from the sources.
- Moves to the *test_package* folder and creates a temporary *build* folder.
- Executes the :command:`conan install ..`, to install the requirements of the
  *test_package/conanfile.py*. Note that it will build "Hello" from the sources.
- Builds and launches the *example* consuming application, calling the *test_package/conanfile.py*
  ``build()`` and ``test()`` methods respectively.

Using Conan commands, the :command:`conan create` command would be equivalent to:

.. code-block:: bash

    $ conan export . demo/testing
    $ conan install Hello/0.1@demo/testing --build=Hello
    # package is created now, use test to test it
    $ conan test test_package Hello/0.1@demo/testing

The :command:`conan create` command receives the same command line parameters as :command:`conan install` so
you can pass to it the same settings, options, and command line switches. If you want to create and
test packages for different configurations, you could:

.. code-block:: bash

    $ conan create . demo/testing -s build_type=Debug
    $ conan create . demo/testing -o Hello:shared=True -s arch=x86
    $ conan create . demo/testing -pr my_gcc49_debug_profile
    ...
    $ conan create ...


.. _settings_vs_options:

Settings vs. Options
--------------------

We have used settings such as ``os``, ``arch`` and ``compiler``. Note the above package recipe also contains a
``shared`` option (defined as ``options = {"shared": [True, False]}``). What is the difference between
settings and options?

**Settings** are a project-wide configuration, something that typically affects the whole project that
is being built. For example, the operating system or the architecture would be naturally the same for all
packages in a dependency graph, linking a Linux library for a Windows app, or
mixing architectures is impossible.

Settings cannot be defaulted in a package recipe. A recipe for a given library cannot say that its default is
``os=Windows``. The ``os`` will be given by the environment in which that recipe is processed. It is
a mandatory input.

Settings are configurable. You can edit, add, remove settings or subsettings in your *settings.yml* file.
See :ref:`the settings.yml reference <settings_yml>`.

On the other hand, **options** are a package-specific configuration. Static or shared library are not
settings that apply to all packages. Some can be header only libraries while others packages can be just data,
or package executables. Packages can contain a mixture of different artifacts. ``shared`` is a common
option, but packages can define and use any options they want.

Options are defined in the package recipe, including their supported values, while other can be defaulted by the package
recipe itself. A package for a library can well define that by default it will be a static library (a typical default).
If not specified other. the package will be static.

There are some exceptions to the above. For example, settings can be defined per-package using the command line:

.. code-block:: bash

    $ conan install . -s MyPkg:compiler=gcc -s compiler=clang ..

This will use ``gcc`` for MyPkg and ``clang`` for the rest of the dependencies (extremely rare case).

There are situations whereby many packages use the same option, thereby allowing you to set its value once using patterns, like:

.. code-block:: bash

    $ conan install . -o *:shared=True

Any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.

.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write us</a>
