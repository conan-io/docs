.. _makefiles_howto:


Creating and reusing packages based on Makefiles
============================================================

Conan can create packages and reuse them with Makefiles. The ``AutoToolsBuildEnvironment``
build helper helps with most of the necessary tasks.

This how-to has been tested in Windows with MinGW and Linux with gcc. It uses static libraries
but could be extended to shared libraries too. The Makefiles surely can be improved. They are just an example.


Creating packages
------------------

Start cloning the existing example repository, containing a simple "Hello World" library, and application:

.. code-block:: bash

    $ git clone https://github.com/memsharded/conan-example-makefiles
    $ cd conan-example-makefiles
    $ cd hellolib


It contains a *src* folder with the source code and a *conanfile.py* file for creating a package.

Inside the *src* folder, there is *Makefile* to build the static library. This *Makefile* uses
standard variables like ``$(CPPFLAGS)`` or ``$(CXX)`` to build it:

.. code-block:: make

    SRC = hello.cpp
    OBJ = $(SRC:.cpp=.o)
    OUT = libhello.a
    INCLUDES = -I.

    .SUFFIXES: .cpp

    default: $(OUT)

    .cpp.o:
        $(CXX) $(INCLUDES) $(CPPFLAGS) $(CXXFLAGS) -c $< -o $@

    $(OUT): $(OBJ)
        ar rcs $(OUT) $(OBJ)


The *conanfile.py* file uses the ``AutoToolsBuildEnvironment`` build helper. This helper defines
the necessary environment variables with information from dependencies, as well as other variables
to match the current Conan settings (like ``-m32`` or ``-m64`` based on the Conan ``arch`` setting)

.. code-block:: python

    from conans import ConanFile, AutoToolsBuildEnvironment
    from conans import tools

    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"
        settings = "os", "compiler", "build_type", "arch"
        generators = "cmake"
        exports_sources = "src/*"

        def build(self):
            with tools.chdir("src"):
                env_build = AutoToolsBuildEnvironment(self)
                # env_build.configure() # use it to run "./configure" if using autotools
                env_build.make()

        def package(self):
            self.copy("*.h", dst="include", src="src")
            self.copy("*.lib", dst="lib", keep_path=False)
            self.copy("*.a", dst="lib", keep_path=False)

        def package_info(self):
            self.cpp_info.libs = ["hello"]


With this *conanfile.py* you can create the package:

.. code-block:: bash

    $ conan create . user/testing -s compiler=gcc -s compiler.version=4.9 -s compiler.libcxx=libstdc++


Using packages
------------------

Now let's move to the application folder:

.. code-block:: bash

    $ cd ../helloapp


There you can also see a *src* folder with a *Makefile* creating an executable:

.. code-block:: make

    SRC = app.cpp
    OBJ = $(SRC:.cpp=.o)
    OUT = app
    INCLUDES = -I.

    .SUFFIXES: .cpp

    default: $(OUT)

    .cpp.o:
        $(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $< -o $@

    $(OUT): $(OBJ)
        $(CXX) -o $(OUT)  $(OBJ)  $(LDFLAGS)  $(LIBS) 


And also a *conanfile.py* very similar to the previous one. In this case adding a ``requires`` and a ``deploy()`` method:

.. code-block:: python
   :emphasize-lines: 9, 20

    from conans import ConanFile, AutoToolsBuildEnvironment
    from conans import tools

    class AppConan(ConanFile):
        name = "App"
        version = "0.1"
        settings = "os", "compiler", "build_type", "arch"
        exports_sources = "src/*"
        requires = "Hello/0.1@user/testing"

        def build(self):
            with tools.chdir("src"):
                env_build = AutoToolsBuildEnvironment(self)
                env_build.make()

        def package(self):
            self.copy("*app", dst="bin", keep_path=False)
            self.copy("*app.exe", dst="bin", keep_path=False)

        def deploy(self):
            self.copy("*", src="bin", dst="bin")


Note that in this case, the ``AutoToolsBuildEnvironment`` will automatically set values to ``CPPFLAGS``,
``LDFLAGS``, ``LIBS``, etc. existing in the *Makefile* with the correct include directories, library names,
etc. to properly build and link with the ``hello`` library contained in the "Hello" package.

As above, we can create the package with:

.. code-block:: bash

    $ conan create . user/testing -s compiler=gcc -s compiler.version=4.9 -s compiler.libcxx=libstdc++


There are different ways to run executables contained in packages, like using ``virtualrunenv`` generators.
In this case, since the package has a ``deploy()`` method, we can use it:

.. code-block:: bash

    $ conan install Hello/0.1user/testing -s compiler=gcc -s compiler.version=4.9 -s compiler.libcxx=libstdc++
    $ ./bin/app
    $ Hello World Release!
