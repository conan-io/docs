.. spelling::

  cppdefines

.. _premake_generator:

premake
=======

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

.. container:: out_reference_box

    This is the reference page for ``premake`` generator.
    Go to :ref:`Integrations/premake<premake>` if you want to learn how to integrate your project or recipes with premake.

Generates a file name *conanbuildinfo.premake.lua* that can be used for your premake builds (both premake 4 and premake 5 are supported).

The file contains:

- N groups of variables, one group per require, declaring the same individual values: include dirs, libs, bin dirs, defines, etc.
- One group of global variables with aggregated values for all requirements.
- Helper functions to setup the settings in your configuration.

Variables
---------

Package declared variables
++++++++++++++++++++++++++

For each requirement *conanbuildinfo.premake.lua* file declares the following variables.
``XXX`` is the name of the require. e.g. "zlib" for ``zlib/1.2.11@lasote/stable`` requirement:

+---------------------------+------------------------------------------------------+
| NAME                      | VALUE                                                |
+===========================+======================================================+
| conan_includedirs_XXX     | Headers's folders (default {CONAN_XXX_ROOT}/include) |
+---------------------------+------------------------------------------------------+
| conan_libdirs_XXX         | Library folders (default {CONAN_XXX_ROOT}/lib)       |
+---------------------------+------------------------------------------------------+
| conan_bindirs_XXX         | Binary folders (default {CONAN_XXX_ROOT}/bin)        |
+---------------------------+------------------------------------------------------+
| conan_libs_XXX            | Library names to link                                |
+---------------------------+------------------------------------------------------+
| conan_defines_XXX         | Compile definitions                                  |
+---------------------------+------------------------------------------------------+
| conan_cxxflags_XXX        | CXX flags                                            |
+---------------------------+------------------------------------------------------+
| conan_cflags_XXX          | C flags                                              |
+---------------------------+------------------------------------------------------+
| conan_sharedlinkflags_XXX | Shared link flags                                    |
+---------------------------+------------------------------------------------------+
| conan_exelinkflags_XXX    | Executable link flags                                |
+---------------------------+------------------------------------------------------+
| conan_rootpath_XXX        | Abs path to root package folder                      |
+---------------------------+------------------------------------------------------+

Global declared variables
+++++++++++++++++++++++++

+---------------------------+------------------------------------------------------+
| NAME                      | VALUE                                                |
+===========================+======================================================+
| conan_includedirs         | Aggregated headers's folders                         |
+---------------------------+------------------------------------------------------+
| conan_libdirs             | Aggregated library folders                           |
+---------------------------+------------------------------------------------------+
| conan_bindirs             | Aggregated binary folders                            |
+---------------------------+------------------------------------------------------+
| conan_libs                | Aggregated library names to link                     |
+---------------------------+------------------------------------------------------+
| conan_defines             | Aggregated compile definitions                       |
+---------------------------+------------------------------------------------------+
| conan_cxxflags            | Aggregated CXX flags                                 |
+---------------------------+------------------------------------------------------+
| conan_cflags              | Aggregated C flags                                   |
+---------------------------+------------------------------------------------------+
| conan_sharedlinkflags     | Aggregated shared link flags                         |
+---------------------------+------------------------------------------------------+
| conan_exelinkflags        | Aggregated executable link flags                     |
+---------------------------+------------------------------------------------------+

Functions
---------

conan_basic_setup()
+++++++++++++++++++

Basic function to setup the settings into your configuration. Useful to reduce the logic in premake scripts and automate the conversion of
settings:

.. code-block:: lua

    function conan_basic_setup()
        configurations{conan_build_type}
        architecture(conan_arch)
        includedirs{conan_includedirs}
        libdirs{conan_libdirs}
        links{conan_libs}
        defines{conan_cppdefines}
        bindirs{conan_bindirs}
    end
