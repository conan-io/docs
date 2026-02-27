.. _cmake_generator:


`cmake`
=======

.. container:: out_reference_box

    This is the reference page for ``cmake`` generator.
    Go to :ref:`Integrations/CMake<cmake>` if you want to learn how to integrate your project or recipes with CMake.


It generates a file named ``conanbuildinfo.cmake`` and declares some variables and methods

.. _conanbuildinfocmake_variables:

Variables in conanbuildinfo.cmake
---------------------------------

- **Package declared vars**

For each requirement ``conanbuildinfo.cmake`` file declares the following variables.
``XXX`` is the name of the require in uppercase. e.k "ZLIB" for ``zlib/1.2.8@lasote/stable`` requirement:

+--------------------------------+----------------------------------------------------------------------+
| NAME                           | VALUE                                                                |
+================================+======================================================================+
| CONAN_XXX_ROOT                 | Abs path to root package folder.                                     |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_INCLUDE_DIRS_XXX         | Header's folders                                                     |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_LIB_DIRS_XXX             | Library folders  (default {CONAN_XXX_ROOT}/lib)                      |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_BIN_DIRS_XXX             | Binary folders  (default {CONAN_XXX_ROOT}/bin)                       |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_LIBS_XXX                 | Library names to link                                                |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_DEFINES_XXX              | Library defines                                                      |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_COMPILE_DEFINITIONS_XXX  | Compile definitions                                                  |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_CXX_FLAGS_XXX            | CXX flags                                                            |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_SHARED_LINK_FLAGS_XXX    | Shared link flags                                                    |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_C_FLAGS_XXX              | C flags                                                              |
+--------------------------------+----------------------------------------------------------------------+


- **Global declared vars**

Conan also declares some global variables with the aggregated values of all our requirements.
The values are ordered in the right order according to the dependency tree.

+--------------------------------+----------------------------------------------------------------------+
| NAME                           | VALUE                                                                |
+================================+======================================================================+
| CONAN_INCLUDE_DIRS             | Aggregated header's folders                                          |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_LIB_DIRS                 | Aggregated library folders                                           |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_BIN_DIRS                 | Aggregated binary folders                                            |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_LIBS                     | Aggregated library names to link                                     |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_DEFINES                  | Aggregated library defines                                           |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_COMPILE_DEFINITIONS      | Aggregated compile definitions                                       |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_CXX_FLAGS                | Aggregated CXX flags                                                 |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_SHARED_LINK_FLAGS        | Aggregated Shared link flags                                         |
+--------------------------------+----------------------------------------------------------------------+
| CONAN_C_FLAGS                  | Aggregated C flags                                                   |
+--------------------------------+----------------------------------------------------------------------+


- **Variables from user_info**

If any of the requirements is filling the :ref:`user_info<method_package_info_user_info>` object in the :ref:`package_info<method_package_info>`
method a set of variables will be declared following this naming:

+--------------------------------+----------------------------------------------------------------------+
| NAME                           | VALUE                                                                |
+================================+======================================================================+
| CONAN_USER_XXXX_YYYY           | User declared value                                                  |
+--------------------------------+----------------------------------------------------------------------+

``XXXX`` is the name of the requirement in uppercase and ``YYYY`` the variable name. e.j:


.. code-block:: python


   class MyLibConan(ConanFile):
       name = "MyLib"
       version = "1.6.0"

       # ...

       def package_info(self):
           self.user_info.var1 = 2


When other library requires ``MyLib`` and uses the cmake generator:

**conanbuildinfo.cmake**:

.. code-block:: python

    # ...
    set(CONAN_USER_MYLIB_var1 "2")



.. _conanbuildinfocmake_methods:

Methods available in conanbuildinfo.cmake
-----------------------------------------

conan_basic_setup
_________________

Setup all the CMake vars according to our settings, by default with the global approach (no targets).

**parameters**: You can combine several parameters to the ``conan_basic_setup`` macro. e.j: ``conan_basic_setup(TARGETS KEEP_RPATHS)``

    - ``TARGETS``:  Setup all the CMake vars by target (only CMake > 3.1.2)
    - ``NO_OUTPUT_DIRS``: Do not adjust the output directories
    - ``KEEP_RPATHS``: Do not adjust the CMAKE_SKIP_RPATH variable in OSX


conan_target_link_libraries
___________________________

Helper to link all libraries to a specified target.

Other optional methods
______________________

There are other methods automatically called by ``conan_basic_setup()`` but you can use them directly:

+--------------------------------+----------------------------------------------------------------------+
| NAME                           | DESCRIPTION                                                          |
+================================+======================================================================+
| conan_check_compiler()         |  Checks that your compiler matches with the declared in the settings |
+--------------------------------+----------------------------------------------------------------------+
| conan_output_dirs_setup()      |  Adjust the bin/ and lib/ output directories                         |
+--------------------------------+----------------------------------------------------------------------+
| conan_set_find_library_paths() |  Set CMAKE_INCLUDE_PATH and CMAKE_INCLUDE_PATH                       |
+--------------------------------+----------------------------------------------------------------------+
| conan_global_flags()           |  Set include_directories, link_directories, link_directories, flags  |
+--------------------------------+----------------------------------------------------------------------+
| conan_define_targets()         |  Define the targets (target flags instead of global flags)           |
+--------------------------------+----------------------------------------------------------------------+
| conan_set_rpath()              |  Set CMAKE_SKIP_RPATH=1  if APPLE                                    |
+--------------------------------+----------------------------------------------------------------------+
| conan_set_vs_runtime()         |  Adjust the runtime flags (/MD /MDd /MT /MTd)                        |
+--------------------------------+----------------------------------------------------------------------+
| conan_set_libcxx(TARGETS)      |  Adjust the standard library flags (libstdc++, libc++, libstdc++11)  |
+--------------------------------+----------------------------------------------------------------------+
| conan_set_find_paths()         |  Adjust CMAKE_MODULE_PATH and CMAKE_PREFIX_PATH                      |
+--------------------------------+----------------------------------------------------------------------+

Targets generated by conanbuildinfo.cmake
-----------------------------------------

If you use ``conan_basic_setup(TARGETS)``, then some cmake targets will be generated (this only works for CMake > 3.1.2)

These targets are:

- A ``CONAN_PKG::PkgName`` target per package in the dependency graph. This is an ``IMPORTED INTERFACE`` target. IMPORTED
  because it is external, a pre-compiled library. INTERFACE, because it doesn't necessarily match a library,
  it could be a header-only library, or the package could even contain several libraries. It contains all the
  properties (include paths, compile flags, etc) that are defined in the ``package_info()`` method of the package.
- Inside each package a ``CONAN_LIB::PkgName_LibName`` target will be generated for each library. Its type is ``IMPORTED
  UNKNOWN``, its mainly purpose is to provide a correct link order. Their only properties are the location and the
  dependencies
- A ``CONAN_PKG`` depends on every ``CONAN_LIB`` that belongs to it, and to its direct public dependencies (i.e. other ``CONAN_PKG``
  targets from its ``requires``)
- Each ``CONAN_LIB`` depends on the direct public dependencies ``CONAN_PKG`` targets of its container package. This guarantees
  correct link order.
