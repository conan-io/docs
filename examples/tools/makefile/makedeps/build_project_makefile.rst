.. _examples_tools_makefile_makedeps_build_project_makefile:

Build a project using Makefile with Conan MakeDeps
==================================================

In this example, we are going to create a simple logger application that uses one of the most popular C++ libraries:
`spdlog <https://github.com/gabime/spdlog/>`_  and `fmt <https://fmt.dev/latest/index.html/>`_.

We'll use `Make <https://www.gnu.org/software/make/>`_ as build system, so you should get it installed
on Linux and Mac before going forward with this example.

Please, first, clone the sources to recreate this project, you can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: shell

    git clone https://github.com/conan-io/examples2.git
    cd examples2/examples/tools/makefile/makedeps/logger

We start with a very simple C++ language project with the following structure:

.. code-block:: text

    .
    ├── Makefile
    ├── conanfile.txt
    └── src
        └── main.cpp

This project contains a basic `Makefile <https://www.gnu.org/software/make/manual/make.html#Introduction>`_ including the **spdlog** variable dependency and the
source code for the logger program in *main.cpp*.

Let's have a look at the *main.cpp* file, it only prints a quote said by Corin, but uses ``spdlog::info`` method for it.

.. code-block:: cpp
    :caption: **main.cpp**

    #include <cstdlib>
    #include "spdlog/spdlog.h"


    int main(void) {
        spdlog::info("To be a Cimmerian warrior, you must have both cunning and balance as well as speed and strength.");
        return EXIT_SUCCESS;
    }

The *Makefile* specifies that ``logger`` is the expected executable and that it should be linked to the ``spdlog`` and ``fmt`` libraries.
To simplify the usage, we use global variables to store the paths, flags and libraries.

.. code-block:: make
    :caption: **Makefile**

    ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
    SRC_FOLDER    = $(ROOT_DIR)/src
    BUILD_FOLDER  = $(ROOT_DIR)/build

    include $(BUILD_FOLDER)/conandeps.mk

    CXXFLAGS      += $(CONAN_CXXFLAGS) -std=c++11
    CPPFLAGS      += $(addprefix -I, $(CONAN_INCLUDE_DIRS))
    CPPFLAGS      += $(addprefix -D, $(CONAN_DEFINES))
    LDFLAGS       += $(addprefix -L, $(CONAN_LIB_DIRS))
    LDLIBS        += $(addprefix -l, $(CONAN_LIBS))
    LDLIBS        += $(addprefix -l, $(CONAN_SYSTEM_LIBS))
    EXELINKFLAGS  += $(CONAN_EXELINKFLAGS)


    all:
        $(CXX) $(SRC_FOLDER)/main.cpp $(CPPFLAGS) $(CXXFLAGS) $(LDFLAGS) $(LDLIBS) $(EXELINKFLAGS) -o $(BUILD_FOLDER)/logger

The *conanfile.txt* looks simple as it just installs the **spdlog** package and uses **MakeDeps** to build our project.

.. code-block:: ini
    :caption: **conanfile.txt**

    [requires]
    spdlog/1.12.0

    [generators]
    MakeDeps

In this case, we will use :ref:`MakeDeps<conan_tools_gnu_makedeps>` to generate information about where the **spdlog** library
files are installed thanks to the `makedeps.mk` file and using a `conanbuild[.sh|.bat]` file that describes the compilation environment.

We will use Conan to install **spdlog** library, generate a dependency file for Makefile, for find **spdlog** and **fmt** by make.


Building on Linux and macOS
---------------------------

First, we should install some requirements. On Linux you need to have ``make`` package installed,
its package name should vary according to the Linux distribution.

For this example, we will not consider a specific Conan profile, but ``spdlog`` is highly compatible with many different configurations.
So it should work mostly with versions of GCC and Clang compiler.

As the first step, we should install all dependencies listed in the ``conanfile.txt``.
The command :ref: `conan install<reference_commands_install>` will not only install the ``spdlog`` package,
but also build it from sources in case your profile does not match with a pre-built binary in your remotes.
Plus, it will provide these generators listed in the ``conanfile.txt``

.. code-block:: shell

    conan install conanfile.txt --output-folder=build --build=missing

After running ``conan install`` command, we should have new files present in the *build* folder:

.. code-block:: text


    └── logger
        ├── Makefile
        ├── build
        │   ├── conanbuild.sh
        │   ├── conanbuildenv-release-armv8.sh
        │   ├── conandeps.mk
        │   ├── conanrun.sh
        │   ├── conanrunenv-release-armv8.sh
        │   ├── deactivate_conanbuild.sh
        │   ├── deactivate_conanbuildenv-release-armv8.sh
        │   └── deactivate_conanrun.sh
        ├── conandeps.mk
        ├── conanfile.txt
        ├── run_example.sh
        └── src
            └── main.cpp


These files are the result of those generators listed in the ``conanfile.txt``.
Once all files needed to build the example are generated and ``spdlog`` is installed, now we can load the script ``conanbuild.sh``.

.. code-block:: shell

    source conanbuild.sh

The ``conanbuild.sh`` is a default file generated by the :ref:`VirtualBuildEnv<conan_tools_env_virtualbuildenv>` and helps us to load other
script files, so we don't need to execute more manual steps to load each generator file. It will not affect our build right now because we don't have any
other toolchain generator, but it will be useful in the next examples.

Then, finally, we can build the project to generate the logger application.
Now we run the ``make`` command, which will consume the ``Makefile``.

.. code-block:: shell

    make

The ``make`` command will read the ``Makefile`` and first, include ``conandeps.mk``, loading all variables that we need to find **spdlog** and **fmt**.
Then, it will append the ``CXXFLAGS``, ``CPPFLAGS``, ``LDFLAGS``, ``LDLIBS`` and ``EXELINKFLAGS`` variables with the information provided by ``conandeps.mk``.
Finally, it will invoke the compiler, then, build the ``main.cpp``, generating the executable ``logger`` in the same folder.

.. code-block:: shell

    ./logger
    To be a Cimmerian warrior, you must have both cunning and balance as well as speed and strength.

The final output is the result of a new application, printing a message with the help of ``spdlog`` library, and built by ``make``.
