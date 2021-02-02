.. _generators_reference:

Generators
==========

Generators are specific components that provide the information of dependencies calculated by Conan in a suitable format for a build system.
They normally provide Conan users with a *conanbuildinfo.XXX* file that can be included or injected to the specific build system. The file
generated contains information of dependencies in form of different variables and sometimes function helpers too.

You can specify a generator in:

- The ``[generators]`` section from :ref:`conanfile.txt<conanfile_txt_reference>`
- The ``generators`` attribute in :ref:`conanfile.py<conanfile_reference>`

Available generators:

.. toctree::
   :maxdepth: 1

   generators/cmake
   generators/cmakemulti
   generators/cmake_paths
   generators/cmake_find_package
   generators/visualstudio
   generators/visualstudiomulti
   generators/visualstudiolegacy
   generators/xcode
   generators/compiler_args
   generators/gcc
   generators/boost_build
   generators/b2
   generators/qbs
   generators/qmake
   generators/scons
   generators/pkg_config
   generators/virtualenv
   generators/virtualbuildenv
   generators/virtualrunenv
   generators/ycm
   generators/text
   generators/json
   generators/premake
   generators/make
