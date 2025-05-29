.. _make:

Make
====

Conan provides integration with plain Makefiles by means of the ``make`` generator. If you are using ``Makefile`` to build your project you
could get the information of the dependencies in a *conanbuildinfo.mak* file. All you have to do is indicate the generator like this:

.. code-block:: text
   :caption: *conanfile.txt*

    [generators]
    make

.. code-block:: text
   :caption: *conanfile.py*

    class MyConan(ConanFile):
        ...
        generators = "make"

Example
-------

We are going to use the same example from :ref:`getting_started`, a MD5 Encrypter app.

This is the main file for it:

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

As this project relies on the Poco Libraries we are going to create a *conanfile.txt* with our requirement and declare there the Make
generator too:

.. code-block:: text
   :caption: conanfile.txt

    [requires]
    Poco/1.9.0@pocoproject/stable

    [generators]
    make

In order to use this generator within your project, use the following Makefile as a reference:

.. code-block:: makefile
   :caption: Makefile

    include conanbuildinfo.mak

    #----------------------------------------
    #     Make variables for a sample App
    #----------------------------------------

    CXX_SRCS = \
    main.cpp

    CXX_OBJ_FILES = \
    main.o

    EXE_FILENAME = \
    main


    #----------------------------------------
    #     Prepare flags from variables
    #----------------------------------------

    CFLAGS          += $(CONAN_CFLAGS)
    CXXFLAGS        += $(CONAN_CXXFLAGS)
    CPPFLAGS        += $(addprefix -I, $(CONAN_INCLUDE_DIRS))
    CPPFLAGS        += $(addprefix -D, $(CONAN_DEFINES))
    LDFLAGS         += $(addprefix -L, $(CONAN_LIB_DIRS))
    LDLIBS          += $(addprefix -l, $(CONAN_LIBS))


    #----------------------------------------
    #     Make Commands
    #----------------------------------------

    COMPILE_CXX_COMMAND         ?= \
        g++ -c $(CPPFLAGS) $(CXXFLAGS) $< -o $@

    CREATE_EXE_COMMAND          ?= \
        g++ $(CXX_OBJ_FILES) \
        $(CXXFLAGS) $(LDFLAGS) $(LDLIBS) \
        -o $(EXE_FILENAME)


    #----------------------------------------
    #     Make Rules
    #----------------------------------------

    .PHONY                  :   exe
    exe                     :   $(EXE_FILENAME)

    $(EXE_FILENAME)         :   $(CXX_OBJ_FILES)
        $(CREATE_EXE_COMMAND)

    %.o                     :   $(CXX_SRCS)
        $(COMPILE_CXX_COMMAND)

Now we are going to let Conan retrieve the dependencies and generate the dependency information in a *conanbuildinfo.mak*:

.. code-block:: bash

    $ conan install .

Then let's call :command:`make` to generate our project:

.. code-block:: bash

    $ make exe

Now you can run your application with ``./main``.

.. seealso::

    Check the complete reference of the :ref:`Make generator<make_generator>`.
