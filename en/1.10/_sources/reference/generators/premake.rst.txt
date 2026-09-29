.. spelling::

  cppdefines

.. _premake_generator:

`premake` [EXPERIMENTAL]
========================

.. container:: out_reference_box

    This is the reference page for ``premake`` generator.
    Go to :ref:`Integrations/premake<premake>` if you want to learn how to integrate your project or recipes with premake.

Generates a file name ``conanbuildinfo.lua`` that can be used for your premake builds (both premake 4 and premake 5 are supported).
The file contains:

- N groups of variables, one group per require, declaring the same individual values: include dirs, libs, bin dirs, defines, etc.
- One group of global variables with aggregated values for all requirements.

**Package declared vars**

For each requirement ``conanbuildinfo.lua`` file declares the following variables.
```XXX``` is the name of the require. e.g. "zlib" for ``zlib/1.2.11@lasote/stable`` requirement:

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
| conan_cppdefines_XXX      | Compile definitions                                  |
+---------------------------+------------------------------------------------------+
| conan_cppflags_XXX        | CXX flags                                            |
+---------------------------+------------------------------------------------------+
| conan_cflags_XXX          | C flags                                              |
+---------------------------+------------------------------------------------------+
| conan_sharedlinkflags_XXX | Shared link flags                                    |
+---------------------------+------------------------------------------------------+
| conan_exelinkflags_XXX    | Executable link flags                                |
+---------------------------+------------------------------------------------------+
| conan_rootpath_XXX        | Abs path to root package folder                      |
+---------------------------+------------------------------------------------------+

**Global declared vars**

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
| conan_cppdefines          | Aggregated compile definitions                       |
+---------------------------+------------------------------------------------------+
| conan_cppflags            | Aggregated CXX flags                                 |
+---------------------------+------------------------------------------------------+
| conan_cflags              | Aggregated C flags                                   |
+---------------------------+------------------------------------------------------+
| conan_sharedlinkflags     | Aggregated shared link flags                         |
+---------------------------+------------------------------------------------------+
| conan_exelinkflags        | Aggregated executable link flags                     |
+---------------------------+------------------------------------------------------+
