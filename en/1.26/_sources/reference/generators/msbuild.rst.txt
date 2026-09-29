.. _msbuild_generator:

msbuild
=======

Introduced in Conan 1.26. This generator is aimed to supersede the existing ``visualstudio``
and ``visualstudiomulti`` generators.

.. warning::

    This generator is experimental and subject to breaking changes.

This is a generator to be used for Visual Studio projects (*.sln* solutions and *.vcxproject* files),
natively, without using CMake at all. The generator will create Visual Studio properties files
that can be added to the projects and solutions in the IDE, under the "properties" tab.

If a conanfile declares two requirements ``"zlib/1.2.11", "poco/1.9.4"``, then
running the :command:`conan install -g=msbuild` will create the following files:

- One properties file for each dependency and transitive dependency, like *conan_zlib.props*, 
  *conan_openssl.props*and *conan_poco.props*. These files will transitively import other files, 
  in this case as the ``poco`` package depends on ``openssl``, the *conan_poco.props* will import
  *conan_openssl.props* file.
- One file for each dependency for each configuration, like *conan_zlib_release_x64_v141.props*,
  containing the corresponding variables (include folders, library folders, library name, etc.)
  for that configuration, like the ``<ConanzlibIncludeDirectories>`` variable. These files are 
  conditionally included per configuration by the base dependency file (*conan_zlib.props*). 
- One *conan_deps.props* Visual Studio properties file, importing all the direct
  dependencies, in this example both *conan_zlib.props* and *conan_poco.props*.


The per-configuration files are created after installing that specific configurations.

.. code:: bash

    $ conan install . -g msbuild -s build_type=Release -s arch=x86_64
    # This will generate the conan_xxx_release_x64 properties files
    $ conan install . -g msbuild -s build_type=Debug -s arch=x86
    # This will generate the conan_xxx_debug_x86 properties files

This is a multi-configuration generator, after installing different configurations
it is possible to switch the configuration directly in the Visual Studio IDE.

If a Visual Studio solutions consists of multiple subprojects, it is possible to add
individual property files to specific subprojects, making it available that dependency
and its transitive dependencies to that subproject only.
