.. _make:

Make
====

Conan provides two integrations for plain Makefiles:

 | The :ref:`Make generator<make_generator>`
 | The :ref:`Make toolchain<make_toolchain>` (experimental)

Refer to the links above for more detail about each of them. Here we provide a
high-level explanation of how these integrations are meant to be used. 

If you are using ``Makefile`` to build your project you can use one or both of
these depending on your needs.

The ``make`` generator outputs all the variables related to package dependencies
into a file which is named *conanbuildinfo.mak*. The ``make`` toolchain outputs
all the variables related to settings, options, and platform into a file which
is named ``conan_toolchain.mak``. 

To use the generator, indicate it in your ``conanfile`` like this:

.. code-block:: text
   :caption: *conanfile.txt*

    [generators]
    make

.. code-block:: python
   :caption: *conanfile.py*

    class MyConan(ConanFile):
        ...
        generators = "make"

To use the toolchain, add the following function to your ``conanfile``:

.. code-block:: python
   :caption: *conanfile.py*

    class MyConan(ConanFile):
        ...
        def generate(self):
            tc = Make(self)
            tc.generate()

**NOTE**: This can only be used in a ``conanfile.py`` and not ``conanfile.txt``.


Example
-------

We are going to use the same example from :ref:`getting_started`, a MD5 hash calculator app.

This is the main source file for it:

.. code-block:: cpp
   :caption: main.cpp

    #include "Poco/MD5Engine.h"
    #include "Poco/DigestStream.h"

    #include <iostream>


    int main(int argc, char** argv)
    {
        Poco::MD5Engine md5;
        Poco::DigestOutputStream ds(md5);
        ds << "abcdefghijklmnopqrstuvwxyz";
        ds.close();
        std::cout << Poco::DigestEngine::digestToHex(md5.digest()) << std::endl;
        return 0;
    }

As this project relies on the Poco Libraries we are going to create a ``conanfile.py`` with our requirement and also declare the Make
generator and Make toolchain. For simplicity, this ``conanfile`` declares an
empty build and package step. They're not needed for for the local developer
workflow. 

.. code-block:: python
   :caption: *conanfile.py*
          
    from conans import ConanFile
    from conan.tools.gnu import MakeToolchain
    
    class MyConan(ConanFile):
        name = "myconan"
        version = "0.1"
        settings = "os", "arch", "compiler", "build_type"
        generators = "make"
        exports_sources = "*"

        def generate(self):
            tc = MakeToolchain(self)
            tc.generate()

        def build(self):
            pass

        def package(self):
            pass

In order to use this generator within your project, use the following Makefile as a reference:

.. code-block:: makefile
   :caption: Makefile

    #----------------------------------------
    #     Prepare flags from make generator
    #----------------------------------------

    include conanbuildinfo.mak
    $(call CONAN_BASIC_SETUP)

    #----------------------------------------
    #     Prepare flags from make toolchain
    #----------------------------------------

    include conan_toolchain.mak
    $(call CONAN_TC_SETUP)

    #----------------------------------------
    #     Make variables for a sample App
    #----------------------------------------

    SRCS          = main.cpp
    OBJS          = main.o
    EXE_FILENAME  = main

    #----------------------------------------
    #     Make Rules
    #----------------------------------------

    .PHONY                  :   exe
    exe                     :   $(EXE_FILENAME)

    $(EXE_FILENAME)         :   $(OBJS)
        g++ $(OBJS) $(CXXFLAGS) $(LDFLAGS) $(LDLIBS) -o $(EXE_FILENAME)

    %.o                     :   $(SRCS)
        g++ -c $(CPPFLAGS) $(CXXFLAGS) $< -o $@

Now we are going to let Conan retrieve the dependencies, generate the
dependency information in the file ``conanbuildinfo.mak``, and generate the
options and settings information in the file ``conan_toolchain.mak``:

.. code-block:: bash

    $ conan install .

Then let's call :command:`make` to generate our project:

.. code-block:: bash

    $ make exe

Now you can run your application with ``./main``.

.. seealso::

    | Complete reference for :ref:`Make generator<make_generator>`
    | Complete reference for :ref:`Make toolchain<make_toolchain>` (experimental)

