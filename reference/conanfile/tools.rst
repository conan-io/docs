.. _conan_tools:

tools
=====

Tools are all things that can be imported and used in Conan recipes.

.. important::

    This is the current design for Conan 2.0, and these will be the supported tools. Only the tools documented
    in this section will be available in Conan 2.0.

    Some of the features used in this section are still **under development**, while they are
    recommended and usable and we will try not to break them in future releases, some breaking
    changes might still happen if necessary to prepare for the *Conan 2.0 release*.

    Most of the utilities defined in "conan.tools" will require very soon to define both the "host" and "build" profiles.
    It is very recommended to start defining both profiles immediately to avoid future breaking.
    Furthermore, some features, like trying to cross-compile might not work at all if the "build" profile is not provided.


The import path is always like:

.. code-block:: python

    from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake
    from conan.tools.microsoft import MSBuildToolchain, MSBuildDeps, MSBuild


The main guidelines are:

- Imports must be in the form ``from conan.tools.xxx import yyy``, or ``from conan.tools import xxx``.
  Do not use ``from conan import tools`` nor ``from conan.tools.xxx.yyy import zzz``.
- Everything that recipes can use belong to ``from conan.tools``. Any other import is private implementation
  and shouldn't be used in recipes (except ``from conan import ConanFile`` and ``from conan.errors``)
- Only documented tools with explicitly documented imports can be used in recipes. Do not use any other import not found
  in this section of the documentation, even if they are in the ``from conan.tools`` namespace.


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
   tools/system
   tools/files
   tools/layout
   tools/scm
   tools/build
