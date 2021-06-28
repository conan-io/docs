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
if specified), containing a valid pkg-config file syntax. The ``prefix`` variable is automatically adjusted to the ``package_folder``.

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

        def generate(self):
            pc = PkgConfigDeps(self)
            pc.generate()

The ``PkgConfigDeps`` will generate after a ``conan install`` command the `*.pc`:

.. code-block:: bash

    $ conan install .
    # Check the [PC_FILE_NAME].pc created in your current folder

For instance, the `.pc` created could look like this one:

.. code-block:: text

    libdir=/my_absoulte_path/mylib/lib
    libdir2=${prefix}/lib2
    includedir=/my_absoulte_path/mylib/include

    Name: MyLib
    Description: Conan package: MyLib
    Version: 0.1
    Libs: -L"${libdir}" -L"${libdir2}"%s
    Cflags: -I"${includedir}"


Components
++++++++++

If a recipe uses :ref:`components<package_information_components>`, the files generated will be *<COMP-NAME>.pc* with their corresponding
flags and require relations.

Additionally, a *<PKG-NAME>.pc* is generated to maintain compatibility for consumers with recipes that start supporting components. This
*<PKG-NAME>.pc* file will declare the all the components of the package as requires while the rest of the fields will be empty, relying on
the propagation of flags coming from the components *<COMP-NAME>.pc* files.

Go to :ref:`Integrations/pkg-config and pc files/Use the pkg_config generator<pkg_config_generator_example>`
if you want to learn how to use this generator.
