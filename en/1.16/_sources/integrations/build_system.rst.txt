.. _integration_build_systems:

Build systems
=============

Conan can be integrated with any build system. This can be done with:


- :ref:`Generators<generators>`: Conan can write file/s in different formats gathering all the information
  from the dependency tree, like include directories, library names, library dirs...

- :ref:`Build Helpers<build_helpers>`: Conan provides some classes to help calling your build system, translating
  the `settings` and `options` to the arguments, flags or environment variables that your build system expect.


.. toctree::
   :maxdepth: 2

   build_system/cmake
   build_system/msbuild
   build_system/makefile
   build_system/ninja
   build_system/pkg_config_pc_files
   build_system/boost_build
   build_system/b2
   build_system/qmake
   build_system/premake
   build_system/make
   build_system/qbs
   build_system/meson
   build_system/scons
   build_system/gcc
