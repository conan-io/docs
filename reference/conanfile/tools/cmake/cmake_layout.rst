.. _cmake_layout:

cmake_layout
------------

.. warning::

    These tools are still **experimental** (so subject to breaking changes) but with very stable syntax.
    We encourage the usage of it to be prepared for Conan 2.0.

Available since: `1.45.0 <https://github.com/conan-io/conan/releases/tag/1.45.0>`_

For example, this would implement the standard CMake project layout:

.. code:: python

    from conan.tools.cmake import cmake_layout

    def layout(self):
        cmake_layout(self)


.. note::

    To try it you can use the ``conan new hello/0.1 --template=cmake_lib`` template.

The ``cmake_layout()`` sets the ``folders`` and ``cpp``
attributes described in the (:ref:`layout reference <layout_folders_reference>`).

The assigned values depend on the CMake generator that will be used.
It can be defined with the ``tools.cmake.cmaketoolchain:generator`` [conf] entry or passing it in the recipe to the
``cmake_layout(self, cmake_generator)`` function. The assigned values are different if it is a
multi-config generator (like Visual Studio or Xcode), or a single-config generator (like Unix Makefiles).

These are the values assigned by the ``cmake_layout``:

- ``conanfile.folders.source``: *src_folder* argument or ``.`` if not specified.
- ``conanfile.folders.build``:
    - ``build``: if the cmake generator is multi-configuration.
    - ``build/Debug`` or ``build/Release``: if the cmake generator is single-configuration, depending on the
      build_type.
    - The ``"build"`` string, can be defined to other value by the ``build_folder`` argument.
- ``conanfile.folders.generators``: ``build/generators``
- ``conanfile.cpp.source.includedirs``: ``["include"]``
- ``conanfile.cpp.build.libdirs`` and ``conanfile.cpp.build.bindirs``:
    - ``["Release"]`` or ``["Debug"]`` for a multi-configuration cmake generator.
    - ``.`` for a single-configuration cmake generator.


.. code:: python

    def layout(self):
        cmake_layout(self, src_folder="subfolder", build_folder="build")


**Arguments:**

- ``src_folder``: (default ``"."``) internally defines ``self.folders.source=src_folder``
  if ``conanfile.folders.subproject`` is not defined, otherwise it will define the value
  relative to ``conanfile.folders.subproject``

- ``build_folder``: (default ``"build"``) defines the base name for the folder containing the build artifacts.


Multi-setting/option cmake_layout
=================================


The ``folders.build`` and ``conanfile.folders.generators`` can be customized to take into account the ``settings``
and ``options`` and not only the ``build_type``. Use the ``tools.cmake.cmake_layout:build_folder_vars``
conf to declare a list of settings or options:

.. code:: bash

    conan install . -c tools.cmake.cmake_layout:build_folder_vars="['settings.compiler', 'options.shared']"

For the previous example, the values assigned by the ``cmake_layout`` (installing the Release/static default
configuration) would be:

- ``conanfile.folders.build``:
    - ``build/apple-clang-shared_false``: if the cmake generator is multi-configuration.
    - ``build/apple-clang-shared_false/Debug``: if the cmake generator is single-configuration.
- ``conanfile.folders.generators``: ``build/generators``

If we repeat the previous install with a different configuration:

.. code:: bash

    conan install . -o shared=True -c tools.cmake.cmake_layout:build_folder_vars="['settings.compiler', 'options.shared']"

The values assigned by the ``cmake_layout`` (installing the Release/shared configuration) would be:

- ``conanfile.folders.build``:
    - ``build/apple-clang-shared_true``: if the cmake generator is multi-configuration.
    - ``build/apple-clang-shared_true/Debug``: if the cmake generator is single-configuration.
- ``conanfile.folders.generators``: ``build-apple-clang-shared_true/generators``


So we can keep separated folders for any number of different configurations that we want to install.

The ``CMakePresets.json`` file generated at the :ref:`CMakeToolchain<conan-cmake-toolchain>`
generator, will also take this ``tools.cmake.cmake_layout:build_folder_vars`` config into account to generate different
names for the presets, being very handy to install N configurations and building our project for any of them by
selecting the chosen preset.

.. note::

    The ``settings.build_type`` value is forbidden in ``tools.cmake.cmake_layout:build_folder_vars`` because the
    build_type is already managed automatically with multi-config support in ``CMakeDeps`` and ``CMakeToolchain``.
