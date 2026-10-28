.. _cmake_layout:

cmake_layout
============

The ``cmake_layout()`` sets the :ref:`folders<conan_conanfile_attributes_folders>` and
:ref:`cpp<conan_conanfile_attributes_cpp>` attributes to follow the structure of a typical CMake project.


.. code:: python

    from conan.tools.cmake import cmake_layout

    def layout(self):
        cmake_layout(self)


.. note::

    To try it you can use the ``conan new cmake_lib -d name=hello -d version=1.0`` template.



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


Reference
---------


.. currentmodule:: conan.tools.cmake.layout

.. autofunction:: cmake_layout


conf
----

``cmake_layout`` is affected by these ``[conf]`` variables:

- **tools.cmake.cmake_layout:build_folder_vars** list of settings, options and/or ``self.name`` and ``self.version`` to
  customize the ``conanfile.folders.build`` folder. See section :ref:`cmake_layout_multi_name` below.
- **tools.cmake.cmake_layout:build_folder** (*new since Conan 2.2.0*)(*experimental*) uses its value as the base folder of the ``conanfile.folders.build``
  for local builds.
- **tools.cmake.cmake_layout:test_folder** (*new since Conan 2.2.0*)(*experimental*) uses its value as the base folder of the ``conanfile.folders.build``
  for test_package builds. If that value is ``$TMP``, Conan will create and use a temporal folder.


.. _cmake_layout_multi_name:

Multi-setting/option cmake_layout
---------------------------------


The ``folders.build`` and ``conanfile.folders.generators`` can be customized to take into account the ``settings``
and ``options`` and not only the ``build_type``. Use the ``tools.cmake.cmake_layout:build_folder_vars``
conf to declare a list of settings, options and/or ``self.name`` and ``self.version``:

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

The ``CMakePresets.json`` file generated at the :ref:`CMakeToolchain<conan_tools_cmaketoolchain>`
generator, will also take this ``tools.cmake.cmake_layout:build_folder_vars`` config into account to generate different
names for the presets, being very handy to install N configurations and building our project for any of them by
selecting the chosen preset.
