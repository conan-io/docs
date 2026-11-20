.. _integrations_cps:

CPS (Common Package Specification)
==================================

.. include:: ../common/experimental_warning.inc

The `Common Package Specification (CPS) <https://cps-org.github.io/cps/>`_ is an effort to create
a standard, build-system agnostic, JSON description of the binary packages of C and C++ libraries
and applications: where the headers and libraries are, which definitions have to be used, which
other packages and components are required, etc. It aims to replace the many different and
build-system specific ways to describe this information, like CMake ``xxx-config.cmake`` files,
``.pc`` files for pkg-config, MSBuild ``.props`` files, and so on, improving the interoperability
between package managers and build systems. The specification is being developed collaboratively
by different tools and companies, including Kitware (CMake) and JFrog (Conan).

CPS files are named ``<name>.cps``, and can have additional files for specific configurations, like
``<name>@release.cps`` or ``<name>@debug.cps``. CMake (>=4.4) can both generate CPS files
(``install(PACKAGE_INFO <name> EXPORT <name>)``) and consume them with ``find_package()``.

The CPS support in Conan is **experimental**, it is evolving together with the specification and
with the CMake implementation, and it can have breaking changes in future Conan versions. It
requires CMake>=4.4 for the CMake integration.

.. seealso::

    - The :ref:`videos<videos>` section contains talks by Diego Rodriguez-Losada about CPS and its Conan implementation:
      :ref:`std::cpp 2025<using_stdcpp2025_cps>`, an introduction to CPS, and
      :ref:`CppCon 2024<cppcon2024_cps>`, about a package specification and its implementation in Conan.
      The earlier :ref:`CppCon 2023<cppcon2023_build_tools>` talk is related, but predates the CPS standard.


The ``CPSDeps`` generator
-------------------------

Conan already has all the information that CPS files need in the ``package_info()`` method of
every recipe: libraries, include directories, definitions, system libraries, components,
requirements between components... This is the information that Conan generators use to create
``xxx-config.cmake``, ``.pc`` or ``.props`` files for the consumers. This is the main advantage
of the Conan approach: the ``CPSDeps`` generator can create the CPS files for **any** package,
including all the existing recipes in ConanCenter, without requiring any change in those recipes.

.. code-block:: python
    :caption: conanfile.py

    from conan import ConanFile

    class Pkg(ConanFile):
        settings = "os", "compiler", "arch", "build_type"
        requires = "zlib/1.3.1"
        generators = "CPSDeps"

It can also be used directly from the command line:

.. code-block:: bash

    $ conan install --requires=zlib/1.3.1 -g CPSDeps

The generator creates, inside the ``build/cps`` folder of the consumer, one folder per binary
configuration (named after the compiler, version, architecture, C++ standard, build type and
``shared`` option, like ``msvc-193-x86_64-release``). Inside it, a ``cps`` folder contains one
``<name>.cps`` file for every dependency:

.. code-block:: text

    build/cps/
    ├── cpsmap-msvc-193-x86_64-release.json
    └── msvc-193-x86_64-release/
        └── cps/
            └── zlib.cps

The ``cpsmap-<configuration>.json`` file is a mapping from the name of every dependency to the
path of its ``.cps`` file, that can be used by other tools to locate the files.

If a package already contains its own ``<name>.cps`` file at the root of the package folder (for
example because it was built with CMake and it was packaged, see the next section), then the
generator will not create a new file, but the mapping will point to the one in the package.


Round trip with CMake
---------------------

Recipes packaging CMake projects that generate CPS files (with ``install(PACKAGE_INFO)`` in CMake>=4.4)
can feed the CPS information back to Conan, so it can be used by consumers with **any** build system.
This is the "round trip": CMake generates the CPS file, Conan reads it and populates the ``cpp_info``, and
then Conan generators create the files for the consumers' build system, which can be CMake or any other.

.. code-block:: cmake
    :caption: CMakeLists.txt

    cmake_minimum_required(VERSION 4.4)
    project(mypkg CXX)

    add_library(mypkg src/mypkg.cpp)
    target_include_directories(mypkg PUBLIC
                $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
                $<INSTALL_INTERFACE:include>)
    target_compile_definitions(mypkg PUBLIC FOO BAR=42)
    set_target_properties(mypkg PROPERTIES PUBLIC_HEADER "include/mypkg.h")

    install(TARGETS mypkg EXPORT mypkg)
    install(PACKAGE_INFO mypkg EXPORT mypkg)

.. code-block:: python
    :caption: conanfile.py

    import glob

    from conan import ConanFile
    from conan.cps import CPS
    from conan.tools.cmake import CMake, cmake_layout


    class MypkgRecipe(ConanFile):
        name = "mypkg"
        version = "0.1"
        package_type = "library"
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False], "fPIC": [True, False]}
        default_options = {"shared": False, "fPIC": True}

        exports_sources = "CMakeLists.txt", "src/*", "include/*"
        implements = ["auto_shared_fpic"]
        generators = "CMakeToolchain"

        def layout(self):
            cmake_layout(self)

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

        def package(self):
            cmake = CMake(self)
            cmake.install()

        def package_info(self):
            # Locate the CPS file that CMake installed in the package, and
            # translate it to the Conan "cpp_info" model
            cps_file = glob.glob("**/mypkg.cps", recursive=True)[0]
            self.cpp_info = CPS.load(cps_file).to_conan()

``CPS.load()`` reads the ``mypkg.cps`` file, together with the ``mypkg@release.cps`` or
``mypkg@debug.cps`` files that might exist next to it, and ``to_conan()`` converts them to a
``cpp_info`` object (with components, if the CPS file defines them). The package is still using
the standard Conan model, so it can be consumed with any generator.

Consuming from CMake
^^^^^^^^^^^^^^^^^^^^

When the consumer uses ``CMakeConfigDeps`` and sets the ``cmake_find_mode`` property of the package to
``none``, Conan will not generate a ``<name>-config.cmake`` file. If the package contains a
``<name>.cps`` file, the generator will detect it and make CMake ``find_package()`` find that
CPS file in the package:

.. code-block:: python
    :caption: conanfile.py

    from conan.tools.cmake import CMakeConfigDeps

    def generate(self):
        deps = CMakeConfigDeps(self)
        deps.set_property("mypkg", "cmake_find_mode", "none")
        deps.generate()

.. code-block:: cmake
    :caption: CMakeLists.txt

    find_package(mypkg CONFIG REQUIRED)
    target_link_libraries(example mypkg::mypkg)

The CPS file will be the one that CMake generated, the same that a user not using Conan would
get from the installed package.

Consuming from other build systems
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Because ``package_info()`` populated the ``cpp_info`` from the CPS file, the package can be consumed
from build systems other than CMake, using the usual Conan generators, for example ``MSBuildDeps`` for
MSBuild and Visual Studio, ``PkgConfigDeps`` for Meson and Autotools, and others.
This means that a project can use CMake and CPS for building and describing the library, and still
be consumed transparently by consumers using MSBuild, without any extra work by the package creator:

.. code-block:: python
    :caption: conanfile.py of the consumer

    from conan import ConanFile

    class Consumer(ConanFile):
        settings = "os", "compiler", "arch", "build_type"
        requires = "mypkg/0.1"
        generators = "MSBuildDeps"

.. note::

    The recipe above is just using the generic conversion ``CPS.load(...).to_conan()``. Recipes
    can still define or complete the ``cpp_info`` manually in ``package_info()``, when needed.


Current limitations
-------------------

- The support is experimental, and the generated information and the API of ``conan.cps`` can change.
- The CPS specification itself is still evolving, so only a subset of its fields is supported.
- The CMake integration requires CMake>=4.4.
