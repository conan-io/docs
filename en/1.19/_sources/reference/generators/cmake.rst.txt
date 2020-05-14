.. _cmake_generator:

cmake
=====

.. container:: out_reference_box

    This is the reference page for ``cmake`` generator.
    Go to :ref:`Integrations/CMake<cmake>` if you want to learn how to integrate your project or recipes with CMake.

It generates a file named *conanbuildinfo.cmake* and declares some variables and methods.

.. _conanbuildinfocmake_variables:

Variables in *conanbuildinfo.cmake*
-----------------------------------

- **Package declared variables**:

  For each requirement *conanbuildinfo.cmake* file declares the following variables. Where ``<PKG-NAME>`` is the placeholder for the name of
  the require in uppercase (``ZLIB`` for ``zlib/1.2.8@lasote/stable``) or the one declared in ``cpp_info.name``:

  +---------------------------------------+----------------------------------------------------------------------+
  | NAME                                  | VALUE                                                                |
  +=======================================+======================================================================+
  | CONAN_<PKG-NAME>_ROOT                 | Abs path to root package folder.                                     |
  +---------------------------------------+----------------------------------------------------------------------+
  | CONAN_INCLUDE_DIRS_<PKG-NAME>         | Header's folders                                                     |
  +---------------------------------------+----------------------------------------------------------------------+
  | CONAN_LIB_DIRS_<PKG-NAME>             | Library folders  (default {CONAN_<PKG-NAME>_ROOT}/lib)               |
  +---------------------------------------+----------------------------------------------------------------------+
  | CONAN_BIN_DIRS_<PKG-NAME>             | Binary folders  (default {CONAN_<PKG-NAME>_ROOT}/bin)                |
  +---------------------------------------+----------------------------------------------------------------------+
  | CONAN_SRC_DIRS_<PKG-NAME>             | Sources folders                                                      |
  +---------------------------------------+----------------------------------------------------------------------+
  | CONAN_LIBS_<PKG-NAME>                 | Library names to link (package libs, system libs and frameworks)     |
  +---------------------------------------+----------------------------------------------------------------------+
  | CONAN_PKG_LIBS_<PKG-NAME>             | Package library names to link                                        |
  +---------------------------------------+----------------------------------------------------------------------+
  | CONAN_SYSTEM_LIBS_<PKG-NAME>          | System library names to link                                         |
  +---------------------------------------+----------------------------------------------------------------------+
  | CONAN_DEFINES_<PKG-NAME>              | Library defines                                                      |
  +---------------------------------------+----------------------------------------------------------------------+
  | CONAN_COMPILE_DEFINITIONS_<PKG-NAME>  | Compile definitions                                                  |
  +---------------------------------------+----------------------------------------------------------------------+
  | CONAN_CXX_FLAGS_<PKG-NAME>            | CXX flags                                                            |
  +---------------------------------------+----------------------------------------------------------------------+
  | CONAN_SHARED_LINK_FLAGS_<PKG-NAME>    | Shared link flags                                                    |
  +---------------------------------------+----------------------------------------------------------------------+
  | CONAN_C_FLAGS_<PKG-NAME>              | C flags                                                              |
  +---------------------------------------+----------------------------------------------------------------------+
  | CONAN_FRAMEWORKS_<PKG-NAME>           | Frameworks names to use them in `find_library()`                     |
  +---------------------------------------+----------------------------------------------------------------------+
  | CONAN_FRAMEWORKS_FOUND_<PKG-NAME>     | Frameworks found after using CONAN_FRAMEWORKS in `find_library()`    |
  +---------------------------------------+----------------------------------------------------------------------+
  | CONAN_FRAMEWORK_PATHS_<PKG-NAME>      | Framework folders to locate the frameworks (OSX)                     |
  +---------------------------------------+----------------------------------------------------------------------+

- **Global declared variables**:

  This generator also declares some global variables with the aggregated values of all our requirements. The values are ordered in the right
  order according to the dependency tree.

  +--------------------------------+----------------------------------------------------------------------+
  | NAME                           | VALUE                                                                |
  +================================+======================================================================+
  | CONAN_INCLUDE_DIRS             | Aggregated header's folders                                          |
  +--------------------------------+----------------------------------------------------------------------+
  | CONAN_LIB_DIRS                 | Aggregated library folders                                           |
  +--------------------------------+----------------------------------------------------------------------+
  | CONAN_BIN_DIRS                 | Aggregated binary folders                                            |
  +--------------------------------+----------------------------------------------------------------------+
  | CONAN_SRC_DIRS                 | Aggregated sources folders                                           |
  +--------------------------------+----------------------------------------------------------------------+
  | CONAN_LIBS                     | Aggregated library names to link (with system libs and frameworks)   |
  +--------------------------------+----------------------------------------------------------------------+
  | CONAN_SYSTEM_LIBS              | Aggregated system libraries names to link                            |
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
  | CONAN_FRAMEWORKS               | Aggregated frameworks to be found with `find_library()` (OSX)        |
  +--------------------------------+----------------------------------------------------------------------+
  | CONAN_FRAMEWORKS_FOUND         | Aggregated found frameworks after `find_library()` call (OSX)        |
  +--------------------------------+----------------------------------------------------------------------+
  | CONAN_FRAMEWORK_PATHS          | Aggregated framework folders (OSX)                                   |
  +--------------------------------+----------------------------------------------------------------------+
  | CONAN_BUILD_MODULES            | Aggregated paths for build module files (like *.cmake*)              |
  +--------------------------------+----------------------------------------------------------------------+

- **User information declared variables**:

  If any of the requirements is filling the :ref:`user_info<method_package_info_user_info>` object in the
  :ref:`package_info<method_package_info>` method a set of variables will be declared following this naming:

  +-----------------------------------+-------------------------------------------------------------------+
  | NAME                              | VALUE                                                             |
  +===================================+===================================================================+
  | CONAN_USER_<PKG-NAME>_<VAR-NAME>  | User declared value                                               |
  +-----------------------------------+-------------------------------------------------------------------+

  Where ``<PKG-NAME>`` means the name of the requirement in uppercase and ``<VAR-NAME>`` the variable name. For example, if this recipe
  declares:

  .. code-block:: python

      class MyLibConan(ConanFile):
          name = "MyLib"
          version = "1.6.0"

          # ...

          def package_info(self):
              self.user_info.var1 = 2

  Other library requiring ``MyLib`` and using this generator will get:

  .. code-block:: cmake
     :caption: *conanbuildinfo.cmake*

      # ...
      set(CONAN_USER_MYLIB_var1 "2")

.. _conanbuildinfocmake_macros:

Macros available in *conanbuildinfo.cmake*
------------------------------------------

conan_basic_setup()
+++++++++++++++++++

This is a helper and general purpose macro that uses all the macros below to set all the CMake variables according to the Conan generated
variables. See the macros below for detailed information.

.. code-block:: cmake

    macro(conan_basic_setup)
        set(options TARGETS NO_OUTPUT_DIRS SKIP_RPATH KEEP_RPATHS SKIP_STD SKIP_FPIC)

Parameters:
    - ``TARGETS`` (Optional): Setup all the CMake variables by target (only CMake > 3.1.2). Activates the call to the macro
      ``conan_target_link_libraries()``.
    - ``NO_OUTPUT_DIRS`` (Optional): Do not adjust the output directories. Deactivates the call to the macro ``conan_output_dirs_setup()``.
    - ``SKIP_RPATH`` (Optional): **[DEPRECATED]** Use ``KEEP_RPATHS`` instead. Activate ``CMAKE_SKIP_RPATH`` variable in OSX.
    - ``KEEP_RPATHS`` (Optional): Do not adjust the ``CMAKE_SKIP_RPATH`` variable in OSX. Activates the call to the macro ``conan_set_rpath()``
    - ``SKIP_STD`` (Optional): Do not adjust the C++ standard flag in ``CMAKE_CXX_FLAGS``. Deactivates the call to the macro
      ``conan_set_std()``.
    - ``SKIP_FPIC`` (Optional): Do not adjust the ``CMAKE_POSITION_INDEPENDENT_CODE`` flag. Deactivates the call to the macro
      ``conan_set_fpic()``.

.. note::

    You can also call each of the following macros individually instead of using the ``conan_basic_setup()``.

conan_target_link_libraries()
+++++++++++++++++++++++++++++

Helper to link all libraries to a specified target.

These targets are:

- A ``CONAN_PKG::<PKG-NAME>`` target per package in the dependency graph. This is an ``IMPORTED INTERFACE`` target. ``IMPORTED`` because it is
  external, a pre-compiled library. ``INTERFACE``, because it doesn't necessarily match a library, it could be a header-only library, or the
  package could even contain several libraries. It contains all the properties (include paths, compile flags, etc.) that are defined in the
  ``package_info()`` method of the recipe.

- Inside each package a ``CONAN_LIB::<PKG-NAME>_<LIB-NAME>`` target will be generated for each library. Its type is ``IMPORTED UNKNOWN`` and its
  main purpose is to provide a correct link order. Their only properties are the location and the dependencies.

- A ``CONAN_PKG`` depends on every ``CONAN_LIB`` that belongs to it, and to its direct public dependencies (e.g. other ``CONAN_PKG`` targets
  from its requirements).

- Each ``CONAN_LIB`` depends on the direct public dependencies ``CONAN_PKG`` targets of its container package. This guarantees correct link
  order.

.. _conan_check_compiler:

conan_check_compiler()
++++++++++++++++++++++

Checks that your compiler matches the one declared in settings.

This method can be disabled setting the :ref:`conan_disable_check_compiler` variable.

conan_output_dirs_setup()
+++++++++++++++++++++++++

Adjusts the *bin/* and *lib/* output directories.

conan_set_find_library_paths()
++++++++++++++++++++++++++++++

Sets ``CMAKE_INCLUDE_PATH`` and ``CMAKE_INCLUDE_PATH``.

conan_global_flags()
++++++++++++++++++++

Sets the corresponding variables to CMake's ``include_directories()`` and ``link_directories()``.

conan_define_targets()
++++++++++++++++++++++

Defines the targets for each dependency (target flags instead of global flags).

conan_set_rpath()
+++++++++++++++++

Sets ``CMAKE_SKIP_RPATH=1`` in the case of working in OSX.

conan_set_vs_runtime()
++++++++++++++++++++++

Adjusts the runtime flags ``/MD``, ``/MDd``, ``/MT`` or ``/MTd`` for Visual Studio.

conan_set_std()
+++++++++++++++

Sets ``CMAKE_CXX_STANDARD`` and ``CMAKE_CXX_EXTENSIONS`` to the appropriate values.

conan_set_libcxx()
++++++++++++++++++

Adjusts the standard library flags (``libc++```, ``libstdc++``, ``libstdc++11``) in ``CMAKE_CXX_FLAGS``.

conan_set_find_paths()
++++++++++++++++++++++

Adjusts ``CMAKE_MODULE_PATH`` and ``CMAKE_PREFIX_PATH`` to the values of ``deps_cpp_info.build_paths``.


conan_include_build_modules()
+++++++++++++++++++++++++++++

Includes CMake files declared in ``CONAN_BUILD_MODULES`` using the ``include(...)`` directive. This loads the functions or macros that
packages may export and makes them available for usage in the consumers *CMakeLists.txt*.

conan_find_apple_frameworks(FRAMEWORKS_FOUND FRAMEWORKS)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Find framework library names provided in `${FRAMEWORKS}` using `find_library()` and return the found values in `FRAMEWORKS_FOUND`.


Input variables for *conanbuildinfo.cmake*
------------------------------------------

CONAN_CMAKE_SILENT_OUTPUT
+++++++++++++++++++++++++

**Default to**: ``FALSE``

Activate it to silence the Conan message output.

.. _conan_disable_check_compiler:

CONAN_DISABLE_CHECK_COMPILER
++++++++++++++++++++++++++++

**Default to**: ``FALSE``

Deactivates the check of the compiler done with the method :ref:`conan_check_compiler`.
