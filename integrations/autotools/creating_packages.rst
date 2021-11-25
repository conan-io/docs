.. _autotools_packages:


|gnu_logo|

Creating and reusing packages with Autotools
============================================

Conan can create packages and reuse them with Autotools (configure/make).

This how-to has been tested in Windows with MinGW and Linux with gcc. It uses static libraries
but could be extended to shared libraries too. The Makefiles surely can be improved, they are just an example.


Creating packages
-----------------

Sources for this example can be found in our `examples repository <https://github.com/conan-io/examples>`_
in the *features/makefiles* folder:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples.git
    $ cd examples/features/makefiles
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


The *conanfile.py* file uses the ``AutoTools`` build helper. This helper defines
the necessary environment variables with information from dependencies, as well as other variables
to match the current Conan settings (like ``-m32`` or ``-m64`` based on the Conan ``arch`` setting)

.. code-block:: python

   from conans import ConanFile
   from conans import tools
   from conan.tools.gnu import Autotools


   class HelloConan(ConanFile):
       name = "hello"
       version = "0.1"
       settings = "os", "compiler", "build_type", "arch"
       exports_sources = "src/*"
       generators = "AutotoolsToolchain"

       def build(self):
           with tools.chdir("src"):
               atools = Autotools(self)
               atools.make()

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
   :emphasize-lines: 11, 23, 24

   from conans import ConanFile
   from conans import tools
   from conan.tools.gnu import Autotools


   class AppConan(ConanFile):
       name = "app"
       version = "0.1"
       settings = "os", "compiler", "build_type", "arch"
       exports_sources = "src/*"
       requires = "hello/0.1@user/testing"
       generators = "AutotoolsDeps", "AutotoolsToolchain"

       def build(self):
           with tools.chdir("src"):
               atools = Autotools(self)
               atools.make()

       def package(self):
           self.copy("*app", dst="bin", keep_path=False)
           self.copy("*app.exe", dst="bin", keep_path=False)

       def deploy(self):
           self.copy("*", src="bin", dst="bin")



Note that in this case, the ``AutoToolsDeps`` and ``AutotoolsToolchain`` generators will automatically set
values to ``CPPFLAGS``, ``LDFLAGS``, ``LIBS``, etc. existing in the *Makefile* with the correct include
directories, library names, etc. to properly build and link with the ``hello`` library contained in the
"hello" package.

As above, we can create the package with:

.. code-block:: bash

    $ conan create . user/testing -s compiler=gcc -s compiler.version=4.9 -s compiler.libcxx=libstdc++


There are different ways to run executables contained in packages, like using ``virtualrunenv`` generators.
In this case, since the package has a ``deploy()`` method, we can use it:

.. code-block:: bash

    $ conan install app/0.1@user/testing -s compiler=gcc -s compiler.version=4.9 -s compiler.libcxx=libstdc++
    $ ./bin/app
    $ Hello World Release!

.. |gnu_logo| image:: ../../images/conan-gnu-logo.png
