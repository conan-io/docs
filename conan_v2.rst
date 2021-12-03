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

- Do not use dictionary expressions in your recipe ``settings`` definition (like ``settings = {"os": ["Windows", "Linux"]}``. This
  way of limiting supported configurations by one recipe will be removed. Use the ``validate()`` method instead to raise
  ``ConanInvalidConfiguration`` if strictly necessary to fail fast for unsupported configurations.
- Use ``self.test_requires()`` to define test requirements instead of the legacy
  ``self.build_requires(..., force_host_context)``.
- Move all your packages to lowercase. Uppercase package names (or versions/user/channel) will not be possible in 2.0.

.. _conanv2_properties_model:

New properties model for the cpp_info in Conan 2.0 generators. Migrating from .names, .filenames and .build_modules to set_property()
-------------------------------------------------------------------------------------------------------------------------------------

.. warning::

    Using ``set_property`` and ``get_property`` methods for ``cpp_info`` is an **experimental**
    feature subject to breaking changes in future releases.

Using ``names``, ``filenames`` and ``build_modules`` will not work any more for new
generators, like :ref:`CMakeDeps<CMakeDeps>` and :ref:`PkgConfigDeps<PkgConfigDeps>`. 
They have a new way of setting this information using ``set_property`` and
``get_property`` methods of the ``cpp_info`` object (available since Conan 1.36).

.. code-block:: python

    def set_property(self, property_name, value, generator=None)
    def get_property(self, property_name, generator=None):

New properties ``cmake_target_name``, ``cmake_file_name``, ``cmake_module_target_name``,
``cmake_module_file_name``, ``pkg_config_name`` and ``cmake_build_modules`` are defined to allow
migrating ``names``, ``filenames`` and ``build_modules`` properties to this model. In Conan 2.0 this
will be the default way of setting these properties for all generators and also passing
custom properties to generators.

New properties defined for *CMake* generators family, used by :ref:`CMakeDeps<CMakeDeps>` generator:

- **cmake_file_name** property will affect all cmake generators that accept the ``filenames``
  property (*cmake_find_package* and *cmake_find_package_multi*).
- **cmake_target_name** property will affect all cmake generators that accept the ``names`` property
  (*cmake*, *cmake_multi*, *cmake_find_package*, *cmake_find_package_multi* and *cmake_paths*).
- **cmake_module_file_name** property supported by *cmake_find_package* generator. Sets the file name of the
  module files created by this generator.
- **cmake_module_target_name** supported by *cmake_find_package* generator. Sets the target name of the
  module files created by this generator.
- **cmake_build_modules** property replaces the ``build_modules`` property.
- **cmake_find_mode** will tell ref:`CMakeDeps<CMakeDeps>` to generate config
  files, modules files, both or none of them, depending on the value set (``config``,
  ``module``, ``both`` or ``none``)


Properties related to *pkg_config*, used by legacy ``pkg_config`` and new :ref:`PkgConfigDeps<PkgConfigDeps>`:

- **pkg_config_name** property sets the ``names`` property for *pkg_config* generator.
- **pkg_config_custom_content** property supported by the *pkg_config* generator that will add user
  defined content to the *.pc* files created by this generator

All of these properties, but ``cmake_file_name`` and ``cmake_module_file_name`` can be defined at
global ``cpp_info`` level or at component level.

For most cases, it is recommended not to use the ``generator`` argument. The properties are generic
for build systems, and different generators that integrate with a given build system could be reading
such generic properties. 

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

**Migrating from the .names and .filenames model to set_property()**

Migrating from `.names` to ``set_property()`` is easy, but there are some details to take
into account for properties like ``cmake_target_name`` and ``cmake_file_name``. Let's see
some examples.

**Migrating from .names to cmake_target_name**

It is important to note that ``cmake_target_name`` is **not** goint to take the same value
as the ``.names`` attribute did. With the ``.names`` attribute, if you set a name for the
target in CMake, Conan would automatically create a "namespaced" target name with that
name. This code, for example:

.. code-block:: python

    def package_info(self):
        ...
        self.cpp_info.components.names["cmake_find_package"] = "myname"
        ...

Will create a CMake target named ``myname::myname``.

The property ``cmake_target_name`` accepts **complete** target names. That means that the
name you set with this property will be the one added to the CMake generated
files without appending any more information to it. 
To translate the last example to the set_property model you should add the following
declaration:

.. code-block:: python

    def package_info(self):
        ...
        self.cpp_info.components.names["cmake_find_package"] = "myname::myname"
        ...

Note that you can use whatever name you want, it can have a different namespace, like
``mynamespace::myname`` or use a name with no namespace at all.

Also, please note that you may want to have different target names
for both `config <https://cmake.org/cmake/help/v3.15/command/find_package.html#full-signature-and-config-mode>`_
and `module <https://cmake.org/cmake/help/v3.15/command/find_package.html#basic-signature-and-module-mode>`_ CMake generated files.
For example, you have a package named ``myssl`` and you want to generate a ``Findmyssl.cmake`` 
module that declares the target ``MySSL::SSL``, but for config mode you
want to declare the target ``MySSL`` without namespaces. You can do that using the
``cmake_module_target_name`` property. Also, when setting this property, remember to set
``cmake_find_mode`` so that `CMakeDeps` generates those module files. Let's see an
example:

.. code-block:: python

    class MySSL(ConanFile):
        name = "myssl"
        version = "1.0"
        ...
        def package_info(self):
            self.cpp_info.set_property("cmake_target_name", "MySSL")
            self.cpp_info.set_property("cmake_module_target_name", "MySSL::SSL")
            self.cpp_info.set_property("cmake_find_mode", "both")
        ...


**Migrating from .filenames to cmake_file_name**

To migrate from ``.filenames`` to names just use the same ``.filenames`` value for the
property ``cmake_file_name``. For example:

.. code-block:: python

    def package_info(self):
        ...
        self.cpp_info.filenames["cmake_find_package"] = "MyFileName"
        self.cpp_info.filenames["cmake_find_package_multi"] = "MyFileName"
        ...

Could be declared like this with ``set_property()``:

.. code-block:: python

    def package_info(self):
        ...
        self.cpp_info.set_property("cmake_file_name", "MyFileName")
        ...

Please note that for the legacy ``.names`` and ``.filenames`` model, if ``.filenames`` is
not declared but ``.names`` is, then Conan will automatically set the value of
``.filenames`` to the value of ``.names``. So for example:

.. code-block:: python

    def package_info(self):
        ...
        self.cpp_info.names["cmake_find_package"] = "SomeName"
        self.cpp_info.names["cmake_find_package_multi"] = "SomeName"
        ...

This will use "SomeName" to compose the generated filenames. In this case you should set ``cmake_file_name`` to "SomeName":

.. code-block:: python

    def package_info(self):
        ...
        self.cpp_info.set_property("cmake_file_name", "SomeName")
        ...

Also, please note that you may want to use different file names
for both `config <https://cmake.org/cmake/help/v3.15/command/find_package.html#full-signature-and-config-mode>`_
and `module <https://cmake.org/cmake/help/v3.15/command/find_package.html#basic-signature-and-module-mode>`_ CMake generated files.
If we take the previous example of the ``myssl`` and you want to generate a ``FindMySSL.cmake`` for module mode and 
``myssl-config.cmake`` for config mode, you can set the ``cmake_module_file_name`` to set the value for the module file:

.. code-block:: python

    class MySSL(ConanFile):
        name = "myssl"
        version = "1.0"
        ...
        def package_info(self):
            self.cpp_info.set_property("cmake_file_name", "myssl")
            self.cpp_info.set_property("cmake_module_file_name", "MySSL")
            self.cpp_info.set_property("cmake_find_mode", "both")
        ...

You can read more about this properties in the :ref:`CMakeDeps<CMakeDeps Properties>` properties reference.

**Migrating components information**

As we said, all these properties but ``cmake_file_name`` and ``cmake_module_file_name`` have components
support, so for example:

.. code-block:: python

    def package_info(self):
        ...
        self.cpp_info.components["mycomponent"].names["cmake_find_package"] = "mycomponent-name"
        self.cpp_info.components["mycomponent"].names["cmake_find_package_multi"] = "mycomponent-name"
        self.cpp_info.components["mycomponent"].names["pkg_config"] = "mypkg-config-name"
        self.cpp_info.components["mycomponent"].build_modules.append(os.path.join("lib", "mypkg_bm.cmake"))
        ...

Could be declared like this with the properties model:

.. code-block:: python

    def package_info(self):
        ...
        self.cpp_info.components["mycomponent"].set_property("cmake_target_name", "component_namespace::mycomponent-name")
        self.cpp_info.components["mycomponent"].set_property("cmake_build_modules", [os.path.join("lib", "mypkg_bm.cmake")])
        self.cpp_info.components["mycomponent"].set_property("pkg_config_name", "mypkg-config-name")
        self.cpp_info.components["mycomponent"].set_property("custom_name", "mycomponent-name", "custom_generator")
        ...


Please **note** that most of the legacy generators like `cmake`, `cmake_multi`,
`cmake_find_package`, `cmake_find_package_multi` and `cmake_paths` do not listen to these
properties at all, so if you want to maintain compatibility with consumers that use those
generators and also that information for new generators like
`CMakeDeps` you need both models living together in the same recipe.

.. seealso::

    Read :ref:`package_information_components` and :ref:`method_package_info` to learn more.


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

Commands that dissapear in 2.0: copy
------------------------------------

Do not use the ``conan copy`` command to change user/channel. Packages will be immutable,
and this command will dissapear in 2.0. Package promotions are generally done in the
server side, copying packages from one server repository to another repository.

Editables don't use external templates any more. New layout model
-----------------------------------------------------------------

If you are using ``editables``, the external template files are going to be removed. Use
the ``layout()`` method definition instead. Please check the documentation for more
information about :ref:`layouts <conan_tools_layout>`.

