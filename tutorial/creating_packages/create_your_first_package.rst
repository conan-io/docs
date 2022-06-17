.. _creating_packages_create_your_first_conan_package:

Create your first Conan package
===============================

In previous sections, we *consumed* Conan packages (like the *Zlib* one), first using a
*conanfile.txt* and then with a *conanfile.py*. But a *conanfile.py* recipe file is not only
meant to consume other packages, it can be used to create your own packages as well. In
this section, we explain how to create a simple Conan package with a *conanfile.py* recipe
and how to use Conan commands to build those packages from sources.


.. important::

    This is a **tutorial** section. You are encouraged to execute these commands. For this
    concrete example, you will need **CMake** installed  in your path. It is not strictly
    required by Conan to create packages, you can use other build systems (such as VS,
    Meson, Autotools, and even your own) to do that, without any dependency on CMake.


Use the :command:`conan new` command to create a "Hello World" C++ library example project:

.. code-block:: bash

    $ conan new cmake_lib -d name=hello -d version=1.0


This will create a Conan package project with the following structure.

.. code-block:: text

  .
  ├── CMakeLists.txt
  ├── conanfile.py
  ├── include
  │   └── hello.h
  ├── src
  │   └── hello.cpp
  └── test_package
      ├── CMakeLists.txt
      ├── conanfile.py
      └── src
          └── example.cpp

The generated files are:

- **conanfile.py**: On the root folder, there is a *conanfile.py* which is the main recipe
  file, responsible for defining how the package is built and consumed.
- **CMakeLists.txt**: A simple generic *CMakeLists.txt*, with nothing specific about Conan
  in it.
- **src** folder: the *src* folder that contains the simple C++ "hello" library.
- **test_package** folder: contains an *example* application that will require
  and link with the created package. It is not mandatory, but it is useful to check that
  our package is correctly created.

Let's have a look at the package recipe *conanfile.py*:

.. code-block:: python

  from conan import ConanFile
  from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout


  class helloRecipe(ConanFile):
      name = "hello"
      version = "1.0"

      # Optional metadata
      license = "<Put the package license here>"
      author = "<Put your name here> <And your email here>"
      url = "<Package recipe repository url here, for issues about the package>"
      description = "<Description of hello package here>"
      topics = ("<Put some tag here>", "<here>", "<and here>")

      # Binary configuration
      settings = "os", "compiler", "build_type", "arch"
      options = {"shared": [True, False], "fPIC": [True, False]}
      default_options = {"shared": False, "fPIC": True}

      # Sources are located in the same place as this recipe, copy them to the recipe
      exports_sources = "CMakeLists.txt", "src/*", "include/*"

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


Let's explain the different sections of the recipe briefly:

First, you can see the **name and version** of the Conan package defined:

* ``name``: a string, with a minimum of 2 and a maximum of 100 **lowercase** characters
  that defines the package name. It should start with alphanumeric or underscore and can
  contain alphanumeric, underscore, +, ., - characters.
* ``version``: It is a string, and can take any value, matching the same constraints as
  the ``name`` attribute. In case the version follows semantic versioning in the form
  ``X.Y.Z-pre1+build2``, that value might be used for requiring this package through
  version ranges instead of exact versions.

Then you can see, some attributes defining **metadata**. These are optional but recommended
and define things like a short ``description`` for the package, the ``author`` of the packaged
library, the ``license``, the ``url`` for the package repository, and the ``topics`` that the package
is related to.

After that, there is a section related with the binary configuration. This section defines
the valid settings and options for the package. As we explained in the :ref:`consuming
packages section<settings_and_options_difference>`:

* ``settings`` are project-wide configuration that cannot be defaulted in recipes. Things
  like the operating system, compiler or build configuration that will be common to
  several Conan packages

* ``options`` are package-specific configuration and can be defaulted in recipes, in this case, we
  have the option of creating the package as a shared or static library, being static the default.

After that, the ``exports_sources`` attribute is set to define which sources are part of
the Conan package. These are the sources for the library you want to package. In this case
the sources for our "hello" library.

Then, several methods are declared:

* The ``config_options()`` method (together with ``configure()`` one) allows to fine-tune the binary configuration
  model, for example, in Windows, there is no ``fPIC`` option, so it can be removed.

* The ``layout()`` method declares the locations where we expect to find the source files
  and also those where we want to save the generated files during the build process.
  Things like the folder for the generated binaries or all the files that the Conan
  generators create in the ``generate()`` method. In this case, as our project uses CMake
  as the build system, we call to ``cmake_layout()``. Calling this function will set the
  expected locations for a CMake project. 

* The ``generate()`` method prepares the build of the package from source. In this case, it could be simplified
  to an attribute ``generators = "CMakeToolchain"``, but it is left to show this important method. In this case,
  the execution of ``CMakeToolchain`` ``generate()`` method will create a *conan_toolchain.cmake* file that translates
  the Conan ``settings`` and ``options`` to CMake syntax.

* The ``build()`` method uses the ``CMake`` wrapper to call CMake commands, it is a thin layer that will manage
  to pass in this case the ``-DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake`` argument. It will configure the
  project and build it from source.

* The ``package()`` method copies artifacts (headers, libs) from the build folder to the final
  package folder. It can be done with bare "copy" commands, but in this case, it is leveraging the already
  existing CMake install functionality (if the CMakeLists.txt didn't implement it, it is easy to write ``self.copy()``
  commands in this ``package()`` method.

* Finally, the ``package_info()`` method defines that consumers must link with a "hello" library
  when using this package. Other information as include or lib paths can be defined as well. This
  information is used for files created by generators (as ``CMakeDeps``) to be used by consumers. 
  This is generic information about the current package, and is available to the consumers
  irrespective of the build system they are using and irrespective of the build system we
  have used in the ``build()`` method

The **test_package** folder is not critical now for understanding how packages are created. The important
bits are:

* **test_package** folder is different from unit or integration tests. These tests are
  "package" tests, and validate that the package is properly created and that the package
  consumers will be able to link against it and reuse it.

* It is a small Conan project itself, it contains its ``conanfile.py``, and its source
  code including build scripts, that depends on the package being created, and builds and
  executes a small application that requires the library in the package.

* It doesn't belong in the package. It only exists in the source repository, not in the
  package.


Let's build the package from sources with the current default configuration, and then let
the ``test_package`` folder test the package:

.. code-block:: bash

    $ conan create .
    -------- Exporting the recipe ----------
    hello/1.0: Exporting package recipe
    ...
    [ 50%] Building CXX object CMakeFiles/example.dir/src/example.cpp.o
    [100%] Linking CXX executable example
    [100%] Built target example

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
    ...

If "Hello world Release!" is displayed, it worked. This is what has happened:

* The *conanfile.py* together with the contents of the *src* folder have been copied
  (**exported**, in Conan terms) to the local Conan cache.

* A new build from source for the ``hello/1.0`` package starts, calling the
  ``generate()``, ``build()`` and ``package()`` methods. This creates the binary package
  in the Conan cache.

* Conan then moves to the *test_package* folder and executes a :command:`conan install` +
  :command:`conan build` + ``test()`` method, to check if the package was correctly
  created.

We can now validate that the recipe and the package binary are in the cache:

.. code-block:: bash

    $ conan list recipes hello
    Local Cache:
      hello
        hello/1.0

The :command:`conan create` command receives the same parameters as :command:`conan install`, so
you can pass to it the same settings and options. If we execute the following lines, we will create new package
binaries for Debug configuration or to build the hello library as shared:

.. code-block:: bash

    $ conan create . -s build_type=Debug
    ...
    hello/1.0: Hello World Debug!

    $ conan create . -o hello/1.0:shared=True
    ...
    hello/1.0: Hello World Release!


These new package binaries will be also stored in the Conan cache, ready to be used by any project in this computer,
we can see them with:


.. code-block:: bash

    # list the binary built for the hello/1.0 package
    # latest is a placeholder to show the package that is the latest created
    $ conan list packages hello/1.0#latest
    Local Cache:
      hello/1.0#a778356a93c60fe1f687dc2c2ed1449f:46d0e61c1613f12c0e46d007c90dfda85a76a954
        settings:
          arch=x86_64
          build_type=Release
          compiler=apple-clang
          compiler.cppstd=gnu98
          compiler.libcxx=libc++
          compiler.version=13
          os=Macos
        options:
          fPIC=True
          shared=True
      hello/1.0#a778356a93c60fe1f687dc2c2ed1449f:65b76cd1e932112820b979ce174c2c96968f51fb
        settings:
          arch=x86_64
          build_type=Debug
          compiler=apple-clang
          compiler.cppstd=gnu98
          compiler.libcxx=libc++
          compiler.version=13
          os=Macos
        options:
          fPIC=True
          shared=False
      hello/1.0#a778356a93c60fe1f687dc2c2ed1449f:bde82464870a3362a84c3c5d1dd4094fdd4b1bfd
        settings:
          arch=x86_64
          build_type=Release
          compiler=apple-clang
          compiler.cppstd=gnu98
          compiler.libcxx=libc++
          compiler.version=13
          os=Macos
        options:
          fPIC=True
          shared=False

Now that we have created a simple Conan package, we will explain each of the methods of
the Conanfile in more detail. You will learn how to modify those methods to achieve things
like retrieving the sources from an external repository, adding dependencies to our
package, customising our toolchain and much more.


A note about the Conan cache
----------------------------

When you did the :command:`conan create` command, the build of your package did not take
place in your local folder but in other folder inside the *Conan cache*. This cache is
located in the user home folder under the ``.conan2`` folder. Conan will use the
``~/.conan2`` folder to store the built packages and also different configuration files.
You already used the :command:`conan list` command to list the recipes and binaries stored
in the local cache. There are different subcommands for this command that we will explain
in more detail through this tutorial:

* :command:`conan list recipes`: Search available recipes in the local cache or in the remotes.
* :command:`conan list recipe-revisions`: List all the revisions of a recipe reference.
* :command:`conan list packages`: List all the different packages for a given recipe reference.
* :command:`conan list package-revisions`: List all the revisions of a package.

TODO: add note about Conan references, recipe/package references.


Read more
---------

- Create your first Conan package with Autotools.
- Create your first Conan package with Meson.
- Create your first Conan package with Visual Studio.
