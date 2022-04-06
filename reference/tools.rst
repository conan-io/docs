.. _conan_tools:

tools
=====

Tools are all things that can be imported and used in Conan recipes.

The import path is always like:

.. code-block:: python

    from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake
    form conan.tools.microsoft import MSBuildToolchain, MSBuildDeps, MSBuild


The main guidelines are:

- Everything that recipes can import belong to ``from conan.tools``. Any other thing is private implementation
  and shouldn't be used in recipes.
- Only documented, public (not preceded by ``_``) tools can be used in recipes.


Contents:

.. toctree::
   :maxdepth: 2

   tools/cmake
   tools/env
   tools/build
   tools/files
