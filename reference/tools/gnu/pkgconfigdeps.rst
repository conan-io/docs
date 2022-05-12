.. _conan_tools_pkgconfigdeps:


PkgConfigDeps
=============

.. _PkgConfigDeps:

The ``PkgConfigDeps`` is the dependencies generator for pkg-config. Generates pkg-config files named ``<PKG-NAME>.pc``
containing a valid pkg-config file syntax.

This generator can be used by name in conanfiles:

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):
        generators = "PkgConfigDeps"

.. code-block:: text
    :caption: conanfile.txt

    [generators]
    PkgConfigDeps

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code:: python

    from conans import ConanFile
    from conan.tools.gnu import PkgConfigDeps

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        requires = "zlib/1.2.11"

        def generate(self):
            pc = PkgConfigDeps(self)
            pc.generate()


Generated files
---------------

`pkg-config` format files named ``<PKG-NAME>.pc``, containing a valid pkg-config file syntax.
The ``prefix`` variable is automatically adjusted to the ``package_folder``:

.. code-block:: text

    prefix=/Users/YOUR_USER/.conan/data/zlib/1.2.11/_/_/package/647afeb69d3b0a2d3d316e80b24d38c714cc6900
    libdir=${prefix}/lib
    includedir=${prefix}/include

    Name: zlib
    Description: Conan package: zlib
    Version: 1.2.11
    Libs: -L"${libdir}" -lz -F Frameworks
    Cflags: -I"${includedir}"


Customization
-------------


Naming
++++++

By default, the ``*.pc`` files will be named following these rules:

* For packages, it uses the package name, e.g., package ``zlib/1.2.11`` -> ``zlib.pc``.
* For components, the package name + hyphen + component name, e.g., ``openssl/3.0.0`` with ``self.cpp_info.components["crypto"]``  -> ``openssl-crypto.pc``.

You can change that default behavior with the ``pkg_config_name`` and ``pkg_config_aliases`` properties. See :ref:`Properties section below <PkgConfigDeps Properties>`.


If a recipe uses **components**, the files generated will be ``<[PKG-NAME]-[COMP-NAME]>.pc`` with their corresponding
flags and require relations.

Additionally, a ``<PKG-NAME>.pc`` is generated to maintain compatibility for consumers with recipes that start supporting components. This
``<PKG-NAME>.pc`` file declares all the components of the package as requires while the rest of the fields will be empty, relying on
the propagation of flags coming from the components ``<[PKG-NAME]-[COMP-NAME]>.pc`` files.



Reference
---------


.. currentmodule:: conan.tools.gnu

.. autoclass:: PkgConfigDeps
    :members:




.. _PkgConfigDeps Properties:

Properties
++++++++++

The following properties affect the ``PkgConfigDeps`` generator:

- **pkg_config_name** property will define the name of the generated ``*.pc`` file (``xxxxx.pc``)
- **pkg_config_aliases** property sets some aliases of any package/component name for *pkg_config* generator. This property only accepts list-like Python objects.
- **pkg_config_custom_content** property will add user defined content to the *.pc* files created by this generator.
- **component_version** property sets a custom version to be used in the ``Version`` field belonging to the created ``*.pc`` file for that component.

These properties can be defined at global ``cpp_info`` level or at component level.

Example:

.. code-block:: python

    def package_info(self):
        custom_content = "datadir=${prefix}/share"
        self.cpp_info.set_property("pkg_config_custom_content", custom_content)
        self.cpp_info.set_property("pkg_config_name", "myname")
        self.cpp_info.components["mycomponent"].set_property("pkg_config_name", "componentname")
        self.cpp_info.components["mycomponent"].set_property("pkg_config_aliases", ["alias1", "alias2"])
        self.cpp_info.components["mycomponent"].set_property("component_version", "1.14.12")
