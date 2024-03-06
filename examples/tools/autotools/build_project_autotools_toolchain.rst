.. _examples_tools_autotools_autotools_toolchain_build_project_autotools_toolchain:

Build a simple Autotools project with Conan dependencies
========================================================

.. warning::

  This example will only work for Linux and OSX environments and does not support Windows directly, including msys2/cygwin subsystems.
  However, Windows Subsystem for Linux (WSL) should work since it provides a Linux environment. While Conan offers `win_bash = True` 
  for some level of support in Windows environments with Autotools, it's not applicable in this tutorial.


In this example, we are going to create a string formatter application
that uses one of the most popular C++ libraries: `fmt <https://fmt.dev/latest/index.html/>`_.

We'll use `Autotools <https://www.gnu.org/software/automake/manual/html_node/Autotools-Introduction.html>`_ as build system and `pkg-config <https://www.freedesktop.org/wiki/Software/pkg-config/>`_ as a helper tool in this case, so you should get them installed
on Linux and Mac before going forward with this example.

Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: shell

    git clone https://github.com/conan-io/examples2.git
    cd examples2/examples/tools/autotools/autotoolstoolchain/string_formatter

We start with a very simple C++ language project with the following structure:

.. code-block:: text

    .
    ├── configure.ac
    ├── Makefile.am
    ├── conanfile.txt
    └── src
        └── main.cpp

This project contains a basic `configure.ac <https://www.gnu.org/software/autoconf/manual/autoconf-2.60/html_node/Writing-configure_002eac.html>_` including the **fmt** pkg-config dependency and the
source code for the string formatter program in *main.cpp*.

Let's have a look at the *main.cpp* file, it only prints a simple message but uses ``fmt::print`` method for it.

.. code-block:: cpp
    :caption: **main.cpp**

    #include <cstdlib>
    #include <fmt/core.h>

    int main() {
        fmt::print("{} - The C++ Package Manager!\n", "Conan");
        return EXIT_SUCCESS;
    }

The ``configure.ac`` file checks for a C++ compiler using the ``AC_PROG_CXX`` macro and also checks for the ``fmt.pc`` pkg-config module using the ``PKG_CHECK_MODULES`` macro.

.. code-block:: text
    :caption: **configure.ac**

    AC_INIT([stringformatter], [0.1.0])
    AM_INIT_AUTOMAKE([1.10 -Wall no-define foreign])
    AC_CONFIG_SRCDIR([src/main.cpp])
    AC_CONFIG_FILES([Makefile])
    PKG_CHECK_MODULES([fmt], [fmt])
    AC_PROG_CXX
    AC_OUTPUT

The *Makefile.am* specifies that ``string_formatter`` is the expected executable and that it should be linked to the ``fmt`` library.

.. code-block:: text
    :caption: **Makefile.am**

    AUTOMAKE_OPTIONS = subdir-objects
    ACLOCAL_AMFLAGS = ${ACLOCAL_FLAGS}

    bin_PROGRAMS = string_formatter
    string_formatter_SOURCES = src/main.cpp
    string_formatter_CPPFLAGS = $(fmt_CFLAGS)
    string_formatter_LDADD = $(fmt_LIBS)

The *conanfile.txt* looks simple as it just installs the **fmt** package and uses two generators to build our project.

.. code-block:: ini
    :caption: **conanfile.txt**

    [requires]
    fmt/9.1.0

    [generators]
    AutotoolsToolchain
    PkgConfigDeps

In this case, we will use :ref:`PkgConfigDeps<conan_tools_gnu_pkgconfigdeps>` to generate information about where the **fmt** library
files are installed thanks to the `*.pc` files and :ref:`AutotoolsToolchain<conan_tools_gnu_autotoolstoolchain>` to pass build information
to *autotools* using a `conanbuild[.sh|.bat]` file that describes the compilation environment.

We will use Conan to install **fmt** library, generate a toolchain for Autotools, and, .pc files for find **fmt** by pkg-config.


Building on Linux and macOS
---------------------------

First, we should install some requirements. On Linux you need to have ``automake`` , ``pkgconf`` and ``make`` packages installed,
their packages names should vary according to the Linux distribution, but essentially,
it should include all tools (aclocal, automake, autoconf and make) that you will need to build the following example.

For this example, we will not consider a specific Conan profile, but ``fmt`` is highly compatible with many different configurations.
So it should work mostly with versions of GCC and Clang compiler.

As the first step, we should install all dependencies listed in the ``conanfile.txt``.
The command :ref: `conan install<reference_commands_install>` will not only install the ``fmt`` package,
but also build it from sources in case your profile does not match with a pre-built binary in your remotes.
Plus, it will provide these generators listed in the ``conanfile.txt``

.. code-block:: shell

    conan install . --build=missing

After running ``conan install`` command, we should have new files present in the *string_formatter* folder:

.. code-block:: text


    └── string_formatter
        ├── Makefile.am
        ├── conanautotoolstoolchain.sh
        ├── conanbuild.conf
        ├── conanbuild.sh
        ├── conanbuildenv-release-armv8.sh
        ├── conanfile.txt
        ├── conanrun.sh
        ├── conanrunenv-release-armv8.sh
        ├── configure.ac
        ├── deactivate_conanbuild.sh
        ├── deactivate_conanrun.sh
        ├── fmt-_fmt.pc
        ├── fmt.pc
        ├── run_example.sh
        └── src
            └── main.cpp


These files are the result of those generators listed in the ``conanfile.txt``.
Once all files needed to build the example are generated and ``fmt`` is installed, now we can load the script ``conanbuild.sh``.

.. code-block:: shell

    source conanbuild.sh

The ``conanbuild.sh`` is a default file generated by the :ref:`VirtualBuildEnv<conan_tools_env_virtualbuildenv>` and helps us to load other
script files, so we don't need to execute more manual steps to load each generator file. It will load ``conanautotoolstoolchain.sh``,
generated by `AutotoolsToolchain`, which defines environment variables according to our
Conan profile, used when running ``conan install`` command. Those environment variables configured are related to the compiler
and ``autotools``, like ``CFLAGS``, ``CPPFLAGS``, ``LDFLAGS``, and ``PKG_CONFIG_PATH``.

As the next step, we can configure the project by running the following commands in sequence:

.. code-block:: shell

    aclocal
    automake --add-missing
    autoconf
    ./configure

The `aclocal <https://www.gnu.org/software/automake/manual/html_node/aclocal-Invocation.html>`_ command will read the file ``configure.ac``
and generate a new file named ``aclocal.m4``, which contains macros needed by the ``automake``. As the second step,
the `automake <https://www.gnu.org/software/automake/manual/automake.html>`_ command will read the ``Makefile.am``, and will generate the file ``Makefile.in``.
So the command `autoconf <https://www.gnu.org/software/autoconf/>`_ will use those files and generate the ``configure`` file.
Once we run ``configure``, all environment variables will be consumed. The ``fmt.pc`` will be loaded at this step too,
as ``autotools`` uses the custom ``PKG_CONFIG_PATH`` to find it.

Then, finally, we can build the project to generate the string formatter application.
Now we run the ``make`` command, which will consume the ``Makefile`` generated by ``autotools``.

.. code-block:: shell

    make

The ``make`` command will read the ``Makefile`` and invoke the compiler, then, build the ``main.cpp``, generating the executable ``string_formatter`` in the same folder.

.. code-block:: shell

    ./string_formatter
    Conan - The C++ Package Manager!

The final output is the result of a new application, printing a message with the help of ``fmt`` library, and built by ``Autotools``.
