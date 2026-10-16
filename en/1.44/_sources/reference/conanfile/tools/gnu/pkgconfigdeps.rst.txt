.. _conan_tools_pkgconfig:


PkgConfigDeps
=============

.. warning::

    These tools are **experimental** and subject to breaking changes.

.. _PkgConfigDeps:

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
    Libs: -L"${libdir}" -lz -F Frameworks
    Cflags: -I"${includedir}"


Components
++++++++++

If a recipe uses :ref:`components<package_information_components>`, the files generated will be *<[PKG-NAME]-[COMP-NAME]>.pc* with their corresponding
flags and require relations.

Additionally, a *<PKG-NAME>.pc* is generated to maintain compatibility for consumers with recipes that start supporting components. This
*<PKG-NAME>.pc* file will declare all the components of the package as requires while the rest of the fields will be empty, relying on
the propagation of flags coming from the components *<[PKG-NAME]-[COMP-NAME]>.pc* files.


.. _PkgConfigDeps Properties:

Properties
++++++++++

The following properties affect the ``PkgConfigDeps`` generator:

- **pkg_config_name** property sets the ``names`` property for *pkg_config* generator.
- **pkg_config_aliases** property sets some aliases of any package/component name for *pkg_config* generator. This property only accepts list-like Python objects.
- **pkg_config_custom_content** property supported by the *pkg_config* generator that will add user
  defined content to the *.pc* files created by this generator.

These properties can be defined at global ``cpp_info`` level or at component level.

Example:

.. code-block:: python

    def package_info(self):
        custom_content = "datadir=${prefix}/share"
        self.cpp_info.set_property("pkg_config_custom_content", custom_content)
        self.cpp_info.set_property("pkg_config_name", "myname")
        self.cpp_info.components["mycomponent"].set_property("pkg_config_name", "componentname")
        self.cpp_info.components["mycomponent"].set_property("pkg_config_aliases", ["alias1", "alias2"])


Names and aliases
++++++++++++++++++

Aliases are available since: `1.43.0 <https://github.com/conan-io/conan/releases>`_

By default, the ``*.pc`` files will be named following these rules:

* For packages, it uses the package name, e.g., package ``zlib/1.2.11`` -> ``zlib.pc``.
* For components, the package name + hyphen + component name, e.g., ``openssl/3.0.0`` with ``self.cpp_info.components["crytpo"]``  -> ``openssl-crypto.pc``.

You can change that default behavior with the ``pkg_config_name`` and ``pkg_config_aliases`` properties. For instance, ``openssl/3.0.0``` recipe has these ``pkg_config_name`` properties already declared:

.. code:: python

    from conans import ConanFile

    class OpenSSLConan(ConanFile):
        name = "openssl"

        # any code here

        def package_info(self):
            self.cpp_info.set_property("pkg_config_name", "openssl")
            self.cpp_info.components["crypto"].set_property("pkg_config_name", "libcrypto")
            self.cpp_info.components["ssl"].set_property("pkg_config_name", "libssl")

Run :command:`conan install openssl/3.0.0@ -g PkgConfigDeps` and check the ``*.pc`` files created:

- libcrypto.pc
- libssl.pc
- openssl.pc
- zlib.pc *(openssl requires zlib)*

Their ``pkg_config_name`` properties are used as the final PC file names:

.. code-block:: text
    :caption: openssl.pc

    Name: openssl
    Description: Conan package: openssl
    Version: 3.0.0
    Requires: libcrypto libssl


.. code-block:: text
    :caption: libcrypto.pc

    prefix=/Users/conan_user/.conan/data/openssl/3.0.0/_/_/package/88955cec2844f731470e07bd44ce5a3a24ec88b7
    libdir1=${prefix}/lib
    includedir1=${prefix}/include

    Name: libcrypto
    Description: Conan component: libcrypto
    Version: 3.0.0
    Libs: -L"${libdir1}" -lcrypto -F Frameworks
    Cflags: -I"${includedir1}"
    Requires: zlib


Now, let's see how ``pkg_config_aliases`` property works step by step.

Let's create our own ``myopenssl/1.0.0`` recipe and define several aliases like the following:

.. code:: python

    from conans import ConanFile

    class MyOpenSSLConan(ConanFile):
        name = "myopenssl"
        version = "1.0.0"

        def package_info(self):
            # Aliases
            self.cpp_info.set_property("pkg_config_aliases", ["myopenssl_alias"])
            self.cpp_info.components["mycrypto"].set_property("pkg_config_aliases", ["mycrypto", "crp"])
            self.cpp_info.components["myssl"].set_property("pkg_config_aliases", ["myssl"])

Then, after creating the package locally with :command:`conan create .` and consuming it :command:`conan install myopenssl/1.0.0@ -g PkgConfigDeps`, the files created will be:

- myopenssl-mycrypto.pc
- myopenssl-myssl.pc
- myopenssl.pc
- crp.pc *(alias of myopenssl-mycrypto)*
- mycrypto.pc *(alias of myopenssl-mycrypto)*
- myssl.pc *(alias of myopenssl-myssl)*
- myopenssl_alias.pc *(alias of myopenssl)*

Where any of those aliases files contains something like this:

.. code-block:: text
    :caption: mycrypto.pc

    Name: mycrypto
    Description: Alias mycrypto for myopenssl-mycrypto
    Version: 1.0.0
    Requires: myopenssl-mycrypto

It's also possible to use both properties together:

.. code:: python

    from conans import ConanFile

    class MyOpenSSLConan(ConanFile):
        name = "myopenssl"
        version = "1.0.0"

        # any code here

        def package_info(self):
            self.cpp_info.set_property("pkg_config_name", "myopenssl")
            self.cpp_info.components["mycrypto"].set_property("pkg_config_name", "libmycrypto")
            self.cpp_info.components["myssl"].set_property("pkg_config_name", "libmyssl")
            # Aliases
            self.cpp_info.set_property("pkg_config_aliases", ["myopenssl_alias"])
            self.cpp_info.components["mycrypto"].set_property("pkg_config_aliases", ["mycrypto", "crp"])
            self.cpp_info.components["myssl"].set_property("pkg_config_aliases", ["myssl"])

After executing the commands mentioned above, the files are:

- libmycrypto.pc
- libmyssl.pc
- myopenssl.pc
- crp.pc *(alias of libmycrypto)*
- mycrypto.pc *(alias of libmycrypto)*
- myssl.pc *(alias of libmyssl)*
- myopenssl_alias.pc *(alias of myopenssl)*

The only change is which name the alias is pointing to:

.. code-block:: text
    :caption: mycrypto.pc

    Name: mycrypto
    Description: Alias mycrypto for libmycrypto
    Version: 1.0.0
    Requires: libmycrypto
