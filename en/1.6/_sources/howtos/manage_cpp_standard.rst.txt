.. _manage_gcc_standard:

How to manage C++ standard
==========================

.. warning::

    This feature is experimental

The setting representing the C++ standard is ``cppstd``.
The detected default profile doesn't set any value for the ``cppstd`` setting.

The consumer can specify it in a :ref:`profile<profiles>` or with the ``-s`` parameter:

.. code-block:: bash

    conan install . -s cppstd=gnu14

This setting will only be applied to the recipes specifying ``cppstd`` in the ``settings`` field:


.. code-block:: python
   :emphasize-lines: 4

    class LibConan(ConanFile):
        name = "lib"
        version = "1.0"
        settings = "cppstd", "os", "compiler", "build_type", "arch"


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

When the ``cppstd`` setting is declared in the recipe and the consumer specify a value for it:

 - The :ref:`CMake<cmake_reference>` build helper will set the ``CONAN_CMAKE_CXX_STANDARD`` and ``CONAN_CMAKE_CXX_EXTENSIONS`` definitions, that will be
   converted to the corresponding CMake variables to activate the standard automatically with the ``conan_basic_setup()`` macro.

 - The :ref:`AutotoolsBuildEnvironment <autotools_reference>` build helper will adjust the needed flag to ``CXXFLAGS`` automatically.

 - The :ref:`MSBuild/VisualStudioBuildEnvironment <msbuild>` build helper will adjust the needed flag to ``CL`` env var automatically.


Package compatibility
---------------------

By default Conan will detect the default standard of your compiler to not generate different binary packages.
For example, you already built some ``gcc > 6.1`` packages, where the default std is ``gnu14``.
If you introduce the ``cppstd`` setting in your recipes and specify the ``gnu14`` value, Conan won't generate
new packages, because it was already the default of your compiler.

.. note::

    Check the :ref:`package_id() <method_package_id>` reference to know more.
