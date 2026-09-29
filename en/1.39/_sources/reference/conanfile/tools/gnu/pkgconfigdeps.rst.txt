.. _conan_tools_pkgconfig:


conan.tools.gnu.pkgconfigdeps
=============================

.. warning::

    These tools are **experimental** and subject to breaking changes.


PkgConfigDeps
-------------

Available since: `1.38.0 <https://github.com/conan-io/conan/releases>`_


The ``PkgConfigDeps`` is the dependencies generator for pkg-config. Generates pkg-config files named *<PKG-NAME>.pc*
(where ``<PKG-NAME`` is the name declared by dependencies in ``cpp_info.name`` or in ``cpp_info.names["pkg_config"]``
if specified), containing a valid pkg-config file syntax. Indeed, it can also be defined using ``set_property`` and the
property ``pkg_config_name`` (available since Conan 1.36), for instance:

.. code-block:: python

    self.cpp_info.components["mycomponent"].set_property("pkg_config_name", "mypkg-config-name")


.. note::
    In Conan 2.0 that will be the default way of setting those properties and also passing custom properties to generators.
    Check the :ref:`cpp_info attributes reference <cpp_info_attributes_reference>` for more information.


The ``prefix`` variable is automatically adjusted to the ``package_folder``.


The ``PkgConfigDeps`` generator can be used by name in conanfiles:

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

The ``PkgConfigDeps`` will generate the ``*.pc`` file after a ``conan install`` command:

.. code-block:: bash

    $ conan install .
    # Check the [PC_FILE_NAME].pc created in your current folder

Now, running this command using the previous ``conanfile.py``, you can check the ``zlib.pc`` file created into your current folder:

.. code-block:: text

    prefix=/Users/YOUR_USER/.conan/data/zlib/1.2.11/_/_/package/647afeb69d3b0a2d3d316e80b24d38c714cc6900
    libdir=${prefix}/lib
    includedir=${prefix}/include

    Name: zlib
    Description: Conan package: zlib
    Version: 1.2.11
    Libs: -L"${libdir}" -lz  -Wl,-rpath,"${libdir}" -F Frameworks
    Cflags: -I"${includedir}"


Components
++++++++++

If a recipe uses :ref:`components<package_information_components>`, the files generated will be *<[PKG-NAME]-[COMP-NAME]>.pc* with their corresponding
flags and require relations.

Additionally, a *<PKG-NAME>.pc* is generated to maintain compatibility for consumers with recipes that start supporting components. This
*<PKG-NAME>.pc* file will declare all the components of the package as requires while the rest of the fields will be empty, relying on
the propagation of flags coming from the components *<[PKG-NAME]-[COMP-NAME]>.pc* files.
