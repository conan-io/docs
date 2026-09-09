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
| CONAN_DEFINES_<PKG-NAME>             | Library definitions                                                     |
+--------------------------------------+-------------------------------------------------------------------------+
| CONAN_CFLAGS_<PKG-NAME>              | Options for the C compiler (-g, -s, -m64, -m32, -fPIC)                  |
+--------------------------------------+-------------------------------------------------------------------------+
| CONAN_CXXFLAGS_<PKG-NAME>            | Options for the C++ compiler (-g, -s, -stdlib, -m64, -m32, -fPIC, -std) |
+--------------------------------------+-------------------------------------------------------------------------+
| CONAN_SHAREDLINKFLAGS_<PKG-NAME>     | Library Shared linker flags                                             |
+--------------------------------------+-------------------------------------------------------------------------+
| CONAN_EXELINK_FLAGS_<PKG-NAME>       | Executable linker flags                                                 |
+--------------------------------------+-------------------------------------------------------------------------+

Conan also declares some **global variables** with the aggregated values of all our requirements. The values are ordered in the right order
according to the dependency tree.

+--------------------------------+----------------------------------------------------------------------+
| NAME                           | VALUE                                                                |
+================================+======================================================================+
| CONAN_ROOTPATH                 | Aggregated root folders                                              |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_SYSROOT                  | Aggregated system root folders                                       |
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

.. important::

    Note that the mapping of the Conan variables to the Make ones is done taking the following rules into account and we suggest to use the
    variables indicated under the *Makefile* column to apply to a common naming:

    +--------------+----------------------+------------+
    | ``cpp_info`` | *conanbuildinfo.mak* | *Makefile* |
    +==============+======================+============+
    | defines      | CONAN_DEFINES        | CPPFLAGS   |
    +--------------+----------------------+------------+
    | includedirs  | CONAN_INCLUDE_DIRS   | CPPFLAGS   |
    +--------------+----------------------+------------+
    | libdirs      | CONAN_LIB_DIRS       | LDFLAGS    |
    +--------------+----------------------+------------+
    | libs         | CONAN_LIBS           | LDLIBS     |
    +--------------+----------------------+------------+
    | cflags       | CONAN_CFLAGS         | CFLAGS     |
    +--------------+----------------------+------------+
    | cppflags     | CONAN_CXXFLAGS       | CXXFLAGS   |
    +--------------+----------------------+------------+
