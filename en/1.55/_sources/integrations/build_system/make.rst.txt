.. _make:

Make
====

.. warning::

    This integration is to be deprecated in Conan 2.0. Check :ref:`the conan.tools.gnu Autotools<conan_tools_gnu>` integration.

Conan provides the :ref:`Make generator<make_generator>` to integrate with plain Makefiles

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


In order to use this generator within your project, use the following Makefile as a reference:

.. code-block:: makefile
   :caption: Makefile

    #----------------------------------------
    #     Prepare flags from make generator
    #----------------------------------------

    include conanbuildinfo.mak

    CFLAGS              += $(CONAN_CFLAGS)
    CXXFLAGS            += $(CONAN_CXXFLAGS)
    CPPFLAGS            += $(addprefix -I, $(CONAN_INCLUDE_DIRS))
    CPPFLAGS            += $(addprefix -D, $(CONAN_DEFINES))
    LDFLAGS             += $(addprefix -L, $(CONAN_LIB_DIRS))
    LDLIBS              += $(addprefix -l, $(CONAN_LIBS))
    EXELINKFLAGS        += $(CONAN_EXELINKFLAGS)

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
