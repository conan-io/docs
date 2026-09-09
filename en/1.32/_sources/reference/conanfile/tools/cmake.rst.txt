conan.tools.cmake
=================

.. warning::

    These tools are **experimental** and subject to breaking changes.

CMakeDeps
---------
Not yet available


CMakeToolchain
--------------
The ``CMakeToolchain`` is the toolchain generator for CMake. It will generate toolchain files that can be used in the
command line invocation of CMake with the ``-DCMAKE_TOOLCHAIN_FILE=conantoolchain.cmake``. This generator translates
the current package configuration, settings, and options, into CMake toolchain syntax.


CMake
-----
The ``CMake`` build helper is a wrapper around the command line invocation of cmake. It will abstract the
calls like ``cmake --build . --config Release`` into Python method calls.
