.. _conan_tools:

tools
=====

Tools are all things that can be imported and used in Conan recipes.

.. warning::

    These tools are **experimental** and subject to breaking changes.

.. important::

    This is the current design for Conan 2.0, and these will be the supported tools. Only the tools documented
    in this section will be available in Conan 2.0.

    Most of the utilities defined in "conan.tools" will require very soon to define both the "host" and "build" profiles.
    It is very recommended to start defining both profiles immediately to avoid future breaking.
    Furthermore, some features, like trying to cross-compile might not work at all if the "build" profile is not provided.


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
   tools/gnu
   tools/google
   tools/apple
   tools/meson
   tools/intel
   tools/microsoft
   tools/qbs
   tools/env
   tools/files
   tools/layout
