.. _conan_v2:

Conan migration guide to 2.0
============================

Conan team is working hard on the next major release. We've been gathering feedback from the
community about our features and we think it's time to break some default behaviors, clean
the codebase and add space for new developments. Development is ongoing and the `Conan 2.0
Tribe <https://conan.io/tribe.html>`_ is having discussions about it.

Conan 2.0-alpha `is already released <https://pypi.org/project/conan/#history>`_  and can
be installed from PyPI doing:

.. code-block:: bash

    $ pip install conan==2.0.0-alpha1

The documentation for 2.0 is still far from being complete, but we are working on it and
you can access it `with the right version label
<https://docs.conan.io/en/2.0-alpha/index.html>`_.


This section summarizes some of the necessary changes during Conan 1.X to be ready to upgrade to Conan 2.0:

Update the syntax of your Conanfile
-----------------------------------

- Use the ``from conan import ConanFile`` import instead of the legacy ``from conans ...`` (note the plural)
- Do not use dictionary expressions in your recipe ``settings`` definition (like ``settings = {"os": ["Windows", "Linux"]}``. This
  way of limiting supported configurations by one recipe will be removed. Use the ``validate()`` method instead to raise
  ``ConanInvalidConfiguration`` if strictly necessary to fail fast for unsupported configurations.
- Use ``self.test_requires()`` to define test requirements instead of the legacy
  ``self.build_requires(..., force_host_context)``.
- Move all your packages to lowercase. Uppercase package names (or versions/user/channel) will not be possible in 2.0.


New namespace conan.tools.xxxxx
-------------------------------

Use generators and helpers only from ``conan.tools.xxxx`` space. All the other ones are
going to be removed. Please check the :ref:`tools<tools>` section to learn more about the new tools
available for Conan 2.0.

Host and build profiles and new cross-building model
----------------------------------------------------

Use always build and host profiles. You can enable it by passing ``-pr:b=default`` in the
command line to most commands. Do not use ``os_build``, ``arch_build`` anywhere in your
recipes or code.

Conan uses revisions by default in Conan 2.0
--------------------------------------------

Conan 2.0 uses :ref:`revisions<package_revisions>` by default and the local cache 2.0 will
store multiple recipe and package revisions for your Conan packages (Conan 1.X supports
only one revision). To start working with revisions enabled in Conan 1.X, please enable
them in your Conan configuration:

.. code-block:: bash

    $ conan config set general.revisions_enabled=True

self.dependencies to access information about dependencies
----------------------------------------------------------

Do not use ``self.deps_cpp_info``, ``self.deps_env_info`` or ``self.deps_user_info``. Use
the `self.dependencies access
<https://docs.conan.io/en/latest/reference/conanfile/dependencies.html#dependencies-interface>`_
to get information about dependencies.

Commands that disappear in 2.0: copy
------------------------------------

Do not use the ``conan copy`` command to change user/channel. Packages will be immutable,
and this command will dissapear in 2.0. Package promotions are generally done in the
server side, copying packages from one server repository to another repository.

Editables don't use external templates any more. New layout model
-----------------------------------------------------------------

If you are using ``editables``, the external template files are going to be removed. Use
the ``layout()`` method definition instead. Please check the documentation for more
information about :ref:`layouts <conan_tools_layout>`.

.. _conanv2_properties_model:

New properties model for the cpp_info in Conan 2.0 generators
-------------------------------------------------------------

.. toctree::
   :hidden:

   migrating_to_2.0/properties.rst

Using ``.names``, ``.filenames`` and ``.build_modules`` will not work any more for new
generators, like :ref:`CMakeDeps<CMakeDeps>` and :ref:`PkgConfigDeps<PkgConfigDeps>`.
They have a new way of setting this information using ``set_property`` and
``get_property`` methods of the ``cpp_info`` object (available since Conan 1.36).

.. code-block:: python

    def set_property(self, property_name, value)
    def get_property(self, property_name):

New properties ``cmake_target_name``, ``cmake_file_name``, ``cmake_module_target_name``,
``cmake_module_file_name``, ``pkg_config_name`` and ``cmake_build_modules`` are defined to allow
migrating ``names``, ``filenames`` and ``build_modules`` properties to this model. In Conan 2.0 this
will be the default way of setting these properties for all generators and also passing
custom properties to generators.

.. important::

  The 2 mechanisms are completely independent:

  - Old way using ``.names``, ``.filenames`` will work exclusively for legacy generators like ``cmake_find_package``
  - New properties, like ``set_property("cmake_target_name")`` will work exclusively for new generators
    like ``CMakeDeps``. They have changed to be absolute, and that would break legacy generators.
  - Recipes that want to provide support for both generators need to provide the 2 definitions in their
    ``package_info()``

New properties defined for *CMake* generators family, used by :ref:`CMakeDeps<CMakeDeps>` generator:

- **cmake_file_name** property will define in ``CMakeDeps`` the name of the generated config file (``xxx-config.cmake``)
- **cmake_target_name** property will define the absolute target name in ``CMakeDeps``
- **cmake_module_file_name** property defines the generated filename for modules (``Findxxxx.cmake``)
- **cmake_module_target_name** defines the absolute target name for find modules.
- **cmake_build_modules** property replaces the ``build_modules`` property.
- **cmake_find_mode** will tell :ref:`CMakeDeps<CMakeDeps>` to generate config
  files, modules files, both or none of them, depending on the value set (``config``,
  ``module``, ``both`` or ``none``)


Properties related to *pkg_config*, supported by both legacy :ref:`pkg_config<pkg_config_generator>` and new :ref:`PkgConfigDeps<PkgConfigDeps>`:

- **pkg_config_name** property equivalent to the ``names`` attribute.
- **pkg_config_custom_content** property supported by both generators that will add user
  defined content to the *.pc* files created by the generator

Properties related to *pkg_config*, only supported by new :ref:`PkgConfigDeps<PkgConfigDeps>`:

- **pkg_config_aliases** property sets some aliases of any package/component name for the ``PkgConfigDeps`` generator only,
  it doesn't work in ``pkg_config``. This property only accepts list-like Python objects.

All of these properties, but ``cmake_file_name`` and ``cmake_module_file_name`` can be defined at
global ``cpp_info`` level or at component level.

The `set/get_property` model is very useful if you are creating a :ref:`custom generator<custom_generator>`.
Using ``set_property()`` you can pass the parameters of your choice and read them using the
``get_property()`` method inside the generator.

.. code-block:: python

    def package_info(self):
        ...
        # you have created a custom generator that reads the 'custom_property' property and you set here
        # the value to 'prop_value'
        self.cpp_info.components["mycomponent"].set_property("custom_property", "prop_value")
        ...

Please **check a detailed migration guide** in the :ref:`dedicated section <properties_migration>`.