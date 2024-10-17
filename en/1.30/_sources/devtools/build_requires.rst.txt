.. _build_requires:

Build requirements
==================

There are some requirements that don't feel natural to add to a package recipe. For example, imagine that you had a ``cmake/3.4`` package in
Conan. Would you add it as a requirement to the ``zlib`` package, so it will install cmake first in order to build ``zlib``?

In short:

- There are requirements that are only needed when you need to build a package from sources, but if the binary package already exists, you
  don't want to install or retrieve them.
- These could be dev tools, compilers, build systems, code analyzers, testing libraries, etc.
- They can be very orthogonal to the creation of the package. It doesn't matter whether you build zlib with CMake 3.4, 3.5 or 3.6. As long
  as the *CMakeLists.txt* is compatible, it will produce the same final package.
- You don't want to add a lot of different versions (like those of CMake) to be able to use them to build the package. You want to easily
  change the requirements, without needing to edit the zlib package recipe.
- Some of them might not even be taken into account when a package like zlib is created, such as cross-compiling it to Android (in which
  the Android toolchain would be a build requirement too).

To address these needs Conan implements ``build_requires``.


Declaring build requirements
----------------------------

Build requirements can be declared in profiles, like:

.. code-block:: ini
   :caption: my_profile

    [build_requires]
    tool1/0.1@user/channel
    tool2/0.1@user/channel, tool3/0.1@user/channel
    *: tool4/0.1@user/channel
    my_pkg*: tool5/0.1@user/channel
    &: tool6/0.1@user/channel
    &!: tool7/0.1@user/channel

Build requirements are specified by a ``pattern:``. If such pattern is not specified, it will be assumed to be ``*``, i.e. to apply to all
packages. Packages can be declared in different lines or by a comma separated list. In this example, ``tool1``, ``tool2``, ``tool3`` and
``tool4`` will be used for all packages in the dependency graph (while running :command:`conan install` or :command:`conan create`).

If a pattern like ``my_pkg*`` is specified, the declared build requirements will only be applied to packages matching that pattern: ``tool5``
will not be applied to Zlib for example, but it will be applied to ``my_pkg_zlib``.

The special case of a **consumer** conanfile (without name or version) it is impossible to match with a pattern, so it is handled with the
special character ``&``:

- ``&`` means apply these build requirements to the consumer conanfile
- ``&!`` means apply the build requirements to all packages except the consumer one.

Remember that the consumer conanfile is the one inside the *test_package* folder or the one referenced in the :command:`conan install`
command.

Build requirements can also be specified in a package recipe, with the ``build_requires`` attribute and the ``build_requirements()`` method:

.. code-block:: python

    class MyPkg(ConanFile):
        build_requires = "tool_a/0.2@user/testing", "tool_b/0.2@user/testing"

        def build_requirements(self):
            # useful for example for conditional build_requires
            # This means, if we are running on a Windows machine, require ToolWin
            if platform.system() == "Windows":
                self.build_requires("tool_win/0.1@user/stable")

The above ``tool_a`` and ``tool_b`` will always be retrieved and used for building this recipe, while the ``tool_win`` one will only be used
only in Windows.

If any build requirement defined inside ``build_requirements()`` has the same package name as the one defined in the ``build_requires``
attribute, the one inside the ``build_requirements()`` method will prevail.

As a rule of thumb, downstream defined values always override upstream dependency values. If some build requirement is defined in the
profile, it will overwrite the build requirements defined in package recipes that have the same package name.


.. _build_requires_context:

Build and Host contexts
-----------------------

.. warning::

    This section refers to the **experimental feature** that is activated when using ``--profile:build`` and ``--profile:host``
    in the command-line. It is currently under development, features can be added or removed in the following versions.


Conan v1.24 differentiates between the ``build`` context and the ``host`` context in the dependency graph (read more about
the meaning of ``host`` and ``build`` platforms in the :ref:`cross building <cross_building>` section) **when the user
supplies two profiles** to the command line using the ``--profile:build`` and ``--profile:host`` arguments:

* The **host context** is populated with the root package (the one specified in the :command:`conan install` or :command:`conan create` command),
  all its requirements and the build requirements forced to be in the host context.
* The **build context** contains the rest of  build requirements and all of them in the profiles. This category typically
  includes all the :ref:`dev tools <create_installer_packages>` like CMake, compilers, linkers,...


Build requirements declared in the recipes can be forced to stay in the host context, this is needed for testing libraries that will
be linked to the generated library or other executable we want to deploy to the ``host`` platform, for example:

.. code-block:: python

    class MyPkg(ConanFile):
        build_requires = "nasm/2.14"  # 'build' context (nasm.exe will be available)

        def build_requirements(self):
            self.build_requires("protobuf/3.6.1")  # 'build' context (protoc.exe will be available)
            self.build_requires("gtest/0.1", force_host_context=True)  # 'host' context (our library will link with it)


.. image:: ../images/xbuild/conan-cross-build-variables.png
   :width: 500 px
   :align: center


Take into account that the same package (executable or library) can appear two times in the graph, in the ``host`` and
in the ``build`` context, with different package IDs. Conan will propagate the proper information to the consumers:

* Build requirements in the ``host`` context will propagate like any other requirement:

  + ``cpp_info``: all information will be available in the ``deps_cpp_info["xxx"]`` object.
  + ``env_info``: won't be propagated.
  + ``user_info``: will be available using the ``deps_user_info["xxx"]`` object.

* Build requirements in the ``build`` context will propagate all the ``env_info`` and Conan will also populate the
  environment variables ``DYLD_LIBRARY_PATH``, ``LD_LIBRARY_PATH`` and ``PATH`` with the corresponding information from
  the ``cpp_info`` object. All this information will be available in the ``deps_env_info`` object.

  Custom information declared in the ``user_info`` attribute will be available in the ``user_info_build["xxx"]`` object
  in the consumer *conanfile*.


.. important::

    If no ``--profile:build`` is provided, all build requirements will belong to the one and only context and they will share
    their dependencies with the libraries we are building. In this scenario all the build requirements propagate ``user_info``,
    ``cpp_info`` and ``env_info`` to the consumer's ``deps_user_info``, ``deps_cpp_info`` and ``deps_env_info``.


Properties of build requirements
--------------------------------

The behavior of ``build_requires`` is the same irrespective if they are defined in the profile or if defined in the package recipe.

- They will only be retrieved and installed if some package that has to be built from sources and matches the declared pattern. Otherwise,
  they will not even be checked for existence.
- Options and environment variables declared in the profile as well as in the command line will affect the build requirements for packages.
  In that way, you can define, for example, for the ``cmake/3.16.3`` package which CMake version will be installed.
- Build requirements will be activated for matching packages, see the section above about :ref:`build requires context <build_requires_context>`
  to know the information that this package will propagate to its consumers.
- Build requirements can also be transitive. They can declare their own requirements, both normal requirements and their own build
  requirements. Normal logic for dependency graph resolution applies, such as conflict resolution and dependency overriding.
- Each matching pattern will produce a different dependency graph of build requirements. These graphs are cached so that they are only
  computed once. If a build requirement applies to different packages with the same configuration it will only be installed once (same
  behavior as normal dependencies - once they are cached locally, there is no need to retrieve or build them again).
- Build requirements do not affect the binary package ID. If using a different build requirement produces a different binary, you should
  consider adding an option or a setting to model that (if not already modeled).
- Can also use version-ranges, like ``Tool/[>0.3]@user/channel``.
- Build requirements are not listed in :command:`conan info` nor are represented in the graph (with :command:`conan info --graph`).


Example: testing framework and build tool
-----------------------------------------

One example of build requirement is a testing framework implemented as a library, another good example is a build tool used
in the compile process. Let's call them ``mytest_framework`` and ``cmake_turbo``, and imagine we already have a package available
for both of them.

Build requirements can be checked for existence (whether they've been applied) in the recipes, which can be useful for conditional logic in
the recipes. In this example, we could have one recipe with the following ``build()`` method:

.. code-block:: python

    def build_requirements(self):
        if self.options.enable_testing:
            self.build_requires("mytest_framework/0.1@user/channel", force_host_context=True)

    def build(self):
        # Use our own 'cmake_turbo' if it is available
        use_cmake_turbo = "cmake_turbo" in self.deps_env_info.deps
        cmake_executable = "cmake_turbo" if use_cmake_turbo else None
        cmake = CMake(self, cmake_program=cmake_executable)
        cmake.configure(defs={"ENABLE_TESTING": self.options.enable_testing})
        cmake.build()
        if enable_testing:
            cmake.test()

And the package *CMakeLists.txt*:

.. code-block:: cmake

    project(PackageTest CXX)
    cmake_minimum_required(VERSION 2.8.12)

    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()
    if(ENABLE_TESTING)
        add_executable(example test.cpp)
        target_link_libraries(example ${CONAN_LIBS})

        enable_testing()
        add_test(NAME example
                  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
                  COMMAND example)
    endif()

This package recipe won't retrieve the ``cmake_turbo`` package for normal installation:

.. code-block:: bash

    $ conan install .

But if the following profile is defined:

.. code-block:: ini
   :caption: use_cmake_turbo_profile

    [build_requires]
    cmake_turbo/0.1@user/channel

then the install command will retrieve the ``cmake_turbo`` and use it:

.. code-block:: bash

    $ conan install . --profile=use_cmake_turbo_profile


Although the previous line would work it is preferred to use the feature from Conan v1.24 and provide
two profiles to the command line, that way the build requirements in the ``build`` context won't 
interfer with the ``host`` graph if they share common requirements (see :ref:`section about dev tools <create_installer_packages>`).
It can also be needed if cross compiling (see :ref:`section about cross compiling <cross_building_build_requires>`).

.. code-block:: bash

    $ conan install . --profile:host=use_cmake_turbo_profile --profile:build=build_machine
