.. _text_generator:

txt
===

.. container:: out_reference_box

    This is the reference page for ``txt`` generator.
    Go to :ref:`Integrations/Custom integrations / Use the text generator<txt_integration>` to know how to use it.

File format
-----------

The generated ``conanbuildinfo.txt`` file is a generic config file with ``[sections]`` and values.

Package declared vars
-----------------------

For each requirement ``conanbuildinfo.txt`` file declares the following sections.
``XXX`` is the name of the require in lowercase. e.k "zlib" for ``zlib/1.2.8@lasote/stable`` requirement:

+-----------------------------+---------------------------------------------------------------------+
| SECTION                     | DESCRIPTION                                                         |
+=============================+=====================================================================+
| [include_dirs_XXX]          | List with the include paths of the requirement                      |
+-----------------------------+---------------------------------------------------------------------+
| [libdirs_XXX]               | List with library paths of the requirement                          |
+-----------------------------+---------------------------------------------------------------------+
| [bindirs_XXX]               | List with binary directories of the requirement                     |
+-----------------------------+---------------------------------------------------------------------+
| [resdirs_XXX]               | List with the resource directories of the requirement               |
+-----------------------------+---------------------------------------------------------------------+
| [builddirs_XXX]             | List with the build directories of the requirement                  |
+-----------------------------+---------------------------------------------------------------------+
| [libs_XXX]                  | List with library names of the requirement                          |
+-----------------------------+---------------------------------------------------------------------+
| [defines_XXX]               | List with the defines of the requirement                            |
+-----------------------------+---------------------------------------------------------------------+
| [cflags_XXX]                | List with C compilation flags                                       |
+-----------------------------+---------------------------------------------------------------------+
| [sharedlinkflags_XXX]       | List with shared libraries link flags                               |
+-----------------------------+---------------------------------------------------------------------+
| [exelinkflags_XXX]          | List with executable link flags                                     |
+-----------------------------+---------------------------------------------------------------------+
| [cppflags_XXX]              | List with C++ compilation flags                                     |
+-----------------------------+---------------------------------------------------------------------+
| [rootpath_XXX]              | Root path of the package                                            |
+-----------------------------+---------------------------------------------------------------------+

**Global declared vars**

Conan also declares some global variables with the aggregated values of all our requirements.
The values are ordered in the right order according to the dependency tree.

+-----------------------------+---------------------------------------------------------------------+
| SECTION                     | DESCRIPTION                                                         |
+=============================+=====================================================================+
| [include_dirs]              | List with the aggregated include paths of the requirements          |
+-----------------------------+---------------------------------------------------------------------+
| [libdirs]                   | List with aggregated library paths of the requirements              |
+-----------------------------+---------------------------------------------------------------------+
| [bindirs]                   | List with aggregated binary directories of the requirements         |
+-----------------------------+---------------------------------------------------------------------+
| [resdirs]                   | List with the aggregated resource directories of the requirements   |
+-----------------------------+---------------------------------------------------------------------+
| [builddirs]                 | List with the aggregated build directories of the requirements      |
+-----------------------------+---------------------------------------------------------------------+
| [libs]                      | List with aggregated library names of the requirements              |
+-----------------------------+---------------------------------------------------------------------+
| [defines]                   | List with the aggregated defines of the requirements                |
+-----------------------------+---------------------------------------------------------------------+
| [cflags]                    | List with aggregated C compilation flags                            |
+-----------------------------+---------------------------------------------------------------------+
| [sharedlinkflags]           | List with aggregated shared libraries link flags                    |
+-----------------------------+---------------------------------------------------------------------+
| [exelinkflags]              | List with aggregated executable link flags                          |
+-----------------------------+---------------------------------------------------------------------+
| [cppflags]                  | List with aggregated C++ compilation flags                          |
+-----------------------------+---------------------------------------------------------------------+
