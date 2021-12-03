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
    $ cd creating_packages


It contains a *conanfile.py* file for creating a package and a *src* folder with the source code.

It also contains a *Makefile* file to build the static library. This *Makefile* uses standard
variables like ``$(CPPFLAGS)`` or ``$(CXX)`` to build it:

.. code-block:: make

    SRC = src/hello.cpp
    OBJ = $(SRC:.cpp=.o)
    OUT = src/libhello.a
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
    from conan.tools.gnu import Autotools


    class HelloConan(ConanFile):
        name = "hello"
        version = "0.1"
        settings = "os", "compiler", "build_type", "arch"
        exports_sources = "Makefile", "src/*"
        generators = "AutotoolsToolchain"

        def layout(self):
            self.folders.source = "src"

        def build(self):
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

    $ conan create . demo/testing


Using packages
------------------

Now let's move to the application folder:

.. code-block:: bash

    $ cd ../reusing_packages


There you can also see a *Makefile*, for creating an executable:

.. code-block:: make

    SRC = src/app.cpp
    OBJ = $(SRC:.cpp=.o)
    OUT = src/app
    INCLUDES = -I.

    .SUFFIXES: .cpp

    default: $(OUT)

    .cpp.o:
        $(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $< -o $@

    $(OUT): $(OBJ)
        $(CXX) -o $(OUT)  $(OBJ)  $(LDFLAGS)  $(LIBS)


And also a *conanfile.py* very similar to the previous one. In this case it adds a ``requires`` property:

.. code-block:: python
    :emphasize-lines: 10

    from conans import ConanFile
    from conan.tools.gnu import Autotools


    class AppConan(ConanFile):
        name = "app"
        version = "0.1"
        settings = "os", "compiler", "build_type", "arch"
        exports_sources = "Makefile", "src/*"
        requires = "hello/0.1@demo/testing"
        generators = "AutotoolsDeps", "AutotoolsToolchain"

        def layout(self):
            self.folders.source = "src"

        def build(self):
            atools = Autotools(self)
            atools.make()

        def package(self):
            self.copy("*app", dst="bin", keep_path=False)
            self.copy("*app.exe", dst="bin", keep_path=False)


Note that in this case, the ``AutoToolsDeps`` and ``AutotoolsToolchain`` generators will automatically set
values to ``CPPFLAGS``, ``LDFLAGS``, ``LIBS``, etc. existing in the *Makefile* with the correct include
directories, library names, etc. to properly build and link with the ``hello`` library contained in the
"hello" package.

Also note the ``layout`` method, that define where the app sources are (``self.folders.source``).

As above, we can create the package with:

.. code-block:: bash

    $ conan create . demo/testing


While working on a package, the recommended way to run your executables is using the
(:ref:)`VirtualRunEnv<conan_tools_env_virtualrunenv>`generator. Please follow the link to learn more
about what ``VirtualRunEnv`` is and how it works, but here is a quick summary on how to use it:

Calling the VirtualRunEnv generator creates some *.sh* files that update some environment variables
that help you to locate executables and shared libraries:

.. code-block:: bash

    $ mkdir runenv # not necessary, but convenient to avoid cluttering the root directory
    $ cd runenv
    $ conan install app/0.1@demo/testing -g VirtualRunEnv

Then you run the *conanrun.sh* script to enable that environment variables:

.. code-block:: bash

    $ source conanrun.sh
    Capturing current environment in deactivate_conanrunenv-release-x86_64.sh
    Configuring environment variables

And now you can call your binary, because it is now in your ``PATH``:

.. code-block:: bash

    $ app
    Hello World Release!


When you are done, you can restore your environment variables:

.. code-block:: bash

    $ source deactivate_conanrun.sh
    Restoring environment


.. |gnu_logo| image:: ../../images/conan-gnu-logo.png
