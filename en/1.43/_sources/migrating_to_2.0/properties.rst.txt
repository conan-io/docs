.. _properties_migration:

Migrating legacy cpp_info attributes to set_property()
------------------------------------------------------

Migrating from `.names`, `.filenams` and `.build_modules` to ``set_property()`` is easy,
but there are some details to take into account for properties like ``cmake_target_name``
and ``cmake_file_name``. Let's see some examples.

.. important::

  The 2 mechanisms are completely independent:

  - Old way using ``.names``, ``.filenames`` will work exclusively for legacy generators like ``cmake_find_package``
  - New properties, like ``set_property("cmake_target_name")`` will work exclusively for new generators
    like ``CMakeDeps``. They have changed to be absolute, and that would break legacy generators.
  - Recipes that want to provide support for both generators need to provide the 2 definitions in their
    ``package_info()``


Migrating from .names to cmake_target_name
==========================================

It is important to note that ``cmake_target_name`` is **not** going to take the same value
as the ``.names`` attribute did. With the ``.names`` attribute, if you set a name for the
target in CMake, Conan would automatically create a "namespaced" target name with that
name. This code, for example:

.. code-block:: python

    def package_info(self):
        ...
        self.cpp_info.filenames["cmake_find_package"] = "myname"
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
        self.cpp_info.set_property("cmake_target_name", "myname::myname")
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


Migrating from .filenames to cmake_file_name
============================================

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

Migrating components information
================================

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
