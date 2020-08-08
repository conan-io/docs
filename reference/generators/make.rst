.. _make_generator:

make
====

.. container:: out_reference_box

    This is the reference page for ``make`` generator.
    Go to :ref:`Integrations/make<make>` if you want to learn how to integrate your project or recipes with make.

This generators creates a file named *conanbuildinfo.mak* with information of dependencies in different variables that can be used for your
make builds.

Variables
---------

Variables per package. The ``<PKG-NAME>`` placeholder is filled with the name of the Conan package.

+--------------------------------------+-------------------------------------------------------------------------+
| NAME                                 | VALUE                                                                   |
+======================================+=========================================================================+
| CONAN_ROOT_<PKG-NAME>                | Absolute path to root package folder                                    |
+--------------------------------------+-------------------------------------------------------------------------+
| CONAN_SYSROOT_<PKG-NAME>             | System root folder                                                      |
+--------------------------------------+-------------------------------------------------------------------------+
| CONAN_RPATHFLAGS_<PKG-NAME>          | Linker flags to append this LIB_DIRS to RPATH in compiled binary        |
+--------------------------------------+-------------------------------------------------------------------------+
| CONAN_INCLUDE_DIRS_<PKG-NAME>        | Headers folders                                                         |
+--------------------------------------+-------------------------------------------------------------------------+
| CONAN_LIB_DIRS_<PKG-NAME>            | Library folders                                                         |
+--------------------------------------+-------------------------------------------------------------------------+
| CONAN_BIN_DIRS_<PKG-NAME>            | Binary folders                                                          |
+--------------------------------------+-------------------------------------------------------------------------+
| CONAN_BUILD_DIRS_<PKG-NAME>          | Build folders                                                           |
+--------------------------------------+-------------------------------------------------------------------------+
| CONAN_RES_DIRS_<PKG-NAME>            | Resources folders                                                       |
+--------------------------------------+-------------------------------------------------------------------------+
| CONAN_LIBS_<PKG-NAME>                | Library names to link with                                              |
+--------------------------------------+-------------------------------------------------------------------------+
| CONAN_SYSTEM_LIBS_<PKG-NAME>         | System library names to link with                                       |
+--------------------------------------+-------------------------------------------------------------------------+
| CONAN_DEFINES_<PKG-NAME>             | Library definitions                                                     |
+--------------------------------------+-------------------------------------------------------------------------+
| CONAN_CFLAGS_<PKG-NAME>              | Options for the C compiler                                              |
+--------------------------------------+-------------------------------------------------------------------------+
| CONAN_CXXFLAGS_<PKG-NAME>            | Options for the C++ compiler                                            |
+--------------------------------------+-------------------------------------------------------------------------+
| CONAN_SHAREDLINKFLAGS_<PKG-NAME>     | Library Shared linker flags                                             |
+--------------------------------------+-------------------------------------------------------------------------+
| CONAN_EXELINK_FLAGS_<PKG-NAME>       | Executable linker flags                                                 |
+--------------------------------------+-------------------------------------------------------------------------+
| CONAN_FRAMEWORKS_<PKG-NAME>          | Frameworks (OSX)                                                        |
+--------------------------------------+-------------------------------------------------------------------------+
| CONAN_FRAMEWORK_PATHS_<PKG-NAME>     | Framework folders (OSX)  (default {CONAN_XXX_ROOT}/Frameworks           |
+--------------------------------------+-------------------------------------------------------------------------+

The generator also declares some **global variables** with the aggregated values of all our requirements. The values are ordered in the right order
according to the dependency tree.

+--------------------------------+----------------------------------------------------------------------+
| NAME                           | VALUE                                                                |
+================================+======================================================================+
+--------------------------------+----------------------------------------------------------------------+
| CONAN_INCLUDE_DIRS             | Aggregated header folders                                            |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_LIB_DIRS                 | Aggregated library folders                                           |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_BIN_DIRS                 | Aggregated binary folders                                            |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_BUILD_DIRS               | Aggregated build folders                                             |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_RES_DIRS                 | Aggregated resource folders                                          |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_LIBS                     | Aggregated library names to link with                                |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_SYSTEM_LIBS              | Aggregated system library names to link with                         |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_DEFINES                  | Aggregated library definitions                                       |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_CFLAGS                   | Aggregated options for the C compiler                                |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_CXXFLAGS                 | Aggregated options for the C++ compiler                              |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_SHAREDLINKFLAGS          | Aggregated Shared linker flags                                       |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_EXELINKFLAGS             | Aggregated Executable linker flags                                   |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_FRAMEWORKS               | Aggregated frameworks (OSX)                                          |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_FRAMEWORK_PATHS          | Aggregated framework folders (OSX)                                   |
+--------------------------------+----------------------------------------------------------------------+

The generator then further condenses these variables down into a smaller group
of 5 **global variables** by prepending the associated compiler or linker flags
and then combining them together. The 5 variables correspond to 5 standard GnuMake variables: 

`Gnu Make Well-Known Variables
<https://www.gnu.org/software/make/manual/html_node/Implicit-Variables.html/>`__


+-------------------------+--------------------------------------------------------------------------------------------+
| NAME                    | VALUE                                                                                      |
+=========================+============================================================================================+
| CONAN_CFLAGS            | Aggregated options for the C compiler                                                      |
+-------------------------+--------------------------------------------------------------------------------------------+
| CONAN_CXXFLAGS          | Aggregated options for the C++ compiler                                                    |
+-------------------------+--------------------------------------------------------------------------------------------+
| CONAN_CPPFLAGS          | Aggregated defines with -D prefix and header folders with -I prefix                        |
+-------------------------+--------------------------------------------------------------------------------------------+
| CONAN_LDFLAGS           | Aggregated library folders with -L prefix, sharedlinkflags or exelinkflags, and rpathflags |
+-------------------------+--------------------------------------------------------------------------------------------+
| CONAN_LDLIBS            | Aggregated library and system library names with -l prefix                                 |
+-------------------------+--------------------------------------------------------------------------------------------+

Finally, the generator defines one more global variable which is actually a
user-defined function in **Make**.  This combines appends the 5 aggregated
variables listed above to the corresponding GnuMake variable names. The function
is here:

+--------------------------------+----------------------------------------------------------------------+
| NAME                           | USAGE                                                                |
+================================+======================================================================+
| CONAN_BASIC_SETUP              | $(call CONAN_BASIC_SETUP)                                            |
+--------------------------------+----------------------------------------------------------------------+

Here is the mapping from ``CONAN_`` variable name to **GnuMake** variable name
after calling this function.

+--------------------------------+----------------------------------------------------------------------+
| NAME                           | GNU MAKE VARIABLE APPENDED TO                                        |
+================================+======================================================================+
| CONAN_CFLAGS                   | CFLAGS                                                               |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_CXXFLAGS                 | CXXFLAGS                                                             |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_CPPFLAGS                 | CPPFLAGS                                                             |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_LDFLAGS                  | LDFLAGS                                                              |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_LDLIBS                   | LDLIBS                                                               |
+--------------------------------+----------------------------------------------------------------------+
