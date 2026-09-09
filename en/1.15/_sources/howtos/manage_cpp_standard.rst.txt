.. _manage_cpp_standard:

How to manage C++ standard [EXPERIMENTAL]
=========================================

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.
    Previously, it was implemented as a first level setting ``cppstd``, we encourage
    you to adopt the new subsetting and update your recipes if they were including the
    deprecated one in its :ref:`settings_property` attribute.


The setting representing the C++ standard is ``compiler.cppstd``.
The detected default profile doesn't set any value for the ``compiler.cppstd`` setting,

The consumer can specify it in a :ref:`profile<profiles>` or with the ``-s`` parameter:

.. code-block:: bash

    conan install . -s compiler.cppstd=gnu14


As it is a subsetting, it can have different values for each compiler (also, take into account
that depending on the version of the compiler the standard could have only partial support
and may change the ABI).

Valid values for ``compiler=Visual Studio``:

+--------------------+---------------------------------------------------------------------+
| VALUE              | DESCRIPTION                                                         |
+====================+=====================================================================+
| 14                 | C++ 14                                                              |
+--------------------+---------------------------------------------------------------------+
| 17                 | C++ 17                                                              |
+--------------------+---------------------------------------------------------------------+
| 20                 | C++ 20 (Still C++20 Working Draft)                                  |
+--------------------+---------------------------------------------------------------------+

Valid values for other compilers:

+--------------------+---------------------------------------------------------------------+
| VALUE              | DESCRIPTION                                                         |
+====================+=====================================================================+
| 98                 | C++ 98                                                              |
+--------------------+---------------------------------------------------------------------+
| gnu98              | C++ 98 with GNU extensions                                          |
+--------------------+---------------------------------------------------------------------+
| 11                 | C++ 11                                                              |
+--------------------+---------------------------------------------------------------------+
| gnu11              | C++ 11 with GNU extensions                                          |
+--------------------+---------------------------------------------------------------------+
| 14                 | C++ 14                                                              |
+--------------------+---------------------------------------------------------------------+
| gnu14              | C++ 14 with GNU extensions                                          |
+--------------------+---------------------------------------------------------------------+
| 17                 | C++ 17                                                              |
+--------------------+---------------------------------------------------------------------+
| gnu17              | C++ 17 with GNU extensions                                          |
+--------------------+---------------------------------------------------------------------+
| 20                 | C++ 20 (Partial support)                                            |
+--------------------+---------------------------------------------------------------------+
| gnu20              | C++ 20 with GNU extensions (Partial support)                        |
+--------------------+---------------------------------------------------------------------+



Build helpers
-------------

The value of ``compiler.cppstd`` provided by the consumer is used by the build helpers:

 - The :ref:`CMake<cmake_reference>` build helper will set the ``CONAN_CMAKE_CXX_STANDARD`` and ``CONAN_CMAKE_CXX_EXTENSIONS`` definitions that will be
   converted to the corresponding CMake variables to activate the standard automatically with the ``conan_basic_setup()`` macro.

 - The :ref:`AutotoolsBuildEnvironment <autotools_reference>` build helper will adjust the needed flag to ``CXXFLAGS`` automatically.

 - The :ref:`MSBuild/VisualStudioBuildEnvironment <msbuild>` build helper will adjust the needed flag to ``CL`` env var automatically.


Package compatibility
---------------------

By default Conan will detect the default standard of your compiler to not generate different binary packages.
For example, you already built some ``gcc 6.1`` packages, where the default C++ standard is ``gnu14``.
If you introduce the ``compiler.cppstd`` setting in your profile with the ``gnu14`` value, Conan won't generate
new packages, because it was already the default of your compiler.

.. note::

    Check the :ref:`package_id() <method_package_id>` reference to know more.

.. note::

   Conan 1.x will also generate the same packages as the ones generated with the deprecated
   setting ``cppstd`` for the default value of the standard.
