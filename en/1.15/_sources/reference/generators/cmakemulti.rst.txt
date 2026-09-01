.. _cmakemulti_generator:

cmake_multi
===========

.. container:: out_reference_box

    This is the reference page for ``cmake_multi`` generator.
    Go to :ref:`Integrations/CMake<cmake>` if you want to learn how to integrate your project or recipes with CMake.

This generator will create 3 files with the general information and specific Debug/Release ones:

- *conanbuildinfo_release.cmake*: Variables adjusted only for build type Release
- *conanbuildinfo_debug.cmake*: Variables adjusted only for build type Debug
- *conanbuildinfo_multi.cmake*: Which includes the other two and enables its use and has more generic variables and macros.

Variables in *conanbuildinfo_release.cmake*
-------------------------------------------

Same as :ref:`conanbuildinfo.cmake<conanbuildinfocmake_variables>` with suffix ``_RELEASE``

Variables in *conanbuildinfo_debug.cmake*
-----------------------------------------

Same as :ref:`conanbuildinfo.cmake<conanbuildinfocmake_variables>` with suffix ``_DEBUG``

Macros available in *conanbuildinfo_multi.cmake*
------------------------------------------------

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
    - ``NO_OUTPUT_DIRS`` (Optional): This variable has no effect and it works as if it was activated by default (does not se fixed output
      directories and uses the default ones designated by CMake).
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

- A ``CONAN_PKG::PkgName`` target per package in the dependency graph. This is an ``IMPORTED INTERFACE`` target. ``IMPORTED`` because it is
  external, a pre-compiled library. ``INTERFACE``, because it doesn't necessarily match a library, it could be a header-only library, or the
  package could even contain several libraries. It contains all the properties (include paths, compile flags, etc.) that are defined in the
  ``package_info()`` method of the recipe.

- Inside each package a ``CONAN_LIB::PkgName_LibName`` target will be generated for each library. Its type is ``IMPORTED UNKNOWN`` and its
  main purpose is to provide a correct link order. Their only properties are the location and the dependencies.

- A ``CONAN_PKG`` depends on every ``CONAN_LIB`` that belongs to it, and to its direct public dependencies (e.g. other ``CONAN_PKG`` targets
  from its requirements).

- Each ``CONAN_LIB`` depends on the direct public dependencies ``CONAN_PKG`` targets of its container package. This guarantees correct link
  order.

conan_check_compiler()
++++++++++++++++++++++

Checks that your compiler matches the one declared in settings.

conan_output_dirs_setup()
+++++++++++++++++++++++++

Adjust the *bin/* and *lib/* output directories.

conan_global_flags()
++++++++++++++++++++

Set the corresponding variables to CMake's ``include_directories()`` and ``link_directories()``.

conan_define_targets()
++++++++++++++++++++++

Define the targets for each dependency (target flags instead of global flags).

conan_set_rpath()
+++++++++++++++++

Set ``CMAKE_SKIP_RPATH=1`` in the case of working in OSX.

conan_set_vs_runtime()
++++++++++++++++++++++

Adjust the runtime flags ``/MD``, ``/MDd``, ``/MT`` or ``/MTd`` for Visual Studio.

conan_set_std()
+++++++++++++++

Set ``CMAKE_CXX_STANDARD`` and ``CMAKE_CXX_EXTENSIONS`` to the appropriate values.

conan_set_libcxx()
++++++++++++++++++

Adjust the standard library flags (``libc++```, ``libstdc++``, ``libstdc++11``) in ``CMAKE_CXX_FLAGS``.

conan_set_find_paths()
++++++++++++++++++++++

Adjust ``CMAKE_MODULE_PATH`` and ``CMAKE_PREFIX_PATH`` to the values of ``deps_cpp_info.build_paths``.

Input variables for *conanbuildinfo_multi.cmake*
------------------------------------------------

CONAN_CMAKE_SILENT_OUTPUT
+++++++++++++++++++++++++

**Default to**: ``FALSE``

Activate it to silence the Conan message output.
