.. _examples_extensions_package_signing_openssl:

Signing packages with OpenSSL
=============================

This is an example of a Package Signing Plugin implementation using the `OpensSSL digest tool <https://docs.openssl.org/3.1/man1/openssl-dgst/>`_.
You will need to have ``openssl`` installed and available on your path.

.. include:: ../../../common/experimental_warning.inc

This example is available in the examples2 repository: https://github.com/conan-io/examples2/tree/main/examples/extensions/plugins/openssl_sign

Generating the signing keys
+++++++++++++++++++++++++++

To sign and verify the packages using the plugin, first, we will need a public and private key.

To generate the keys using the ``openssl`` executable, we can run:

.. code-block:: bash

    $ openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048

This will generate the private key used to sign the packages.

Now, we can get the public key from it with this command:

.. code-block:: bash

    $ openssl pkey -in private_key.pem -pubout -out public_key.pem

The plugin will use this public key to verify the packages.


Configuring the plugin
++++++++++++++++++++++

.. caution::

    This example stores a private key next to the plugin for simplicity. **Do not do this in production**.
    Instead, load the signing key from environment variables or a secret manager, or delegate signing to a remote signing service.
    **Always keep the private key out of the Conan cache and out of source control**.

1. Copy the ``examples/extensions/plugins/openssl_sign/sign.py`` file to your Conan home at ``CONAN_HOME/extensions/plugins/sign/sign.py``.

2. Now, place the private key ``private_key.pem`` and the public key ``public_key.pem`` inside a folder ``my-organization`` next to the ``sign.py``
   file (``CONAN_HOME/extensions/plugins/sign/my-organization/<copy_keys_here>``).

The ``my-organization`` folder serves as the **provider** in this example, and it is used by the plugin to identify the organization that owns the keys.
This will be used later by the ``verify()`` function to **verify the package with the matching public key**.

.. tip::

    The Package Signing plugin is installed in the Conan configuration folder, so they can be easily distributed as part of the client
    configuration using the :ref:`conan config install<reference_commands_conan_config_install>` command.


Signing packages
++++++++++++++++

Now that the plugin is configured, we can create a package and sign it afterwards:

.. code-block:: bash

    $ conan new cmake_lib -d name=hello -d version=1.0
    $ conan create

For signing the recipe and package, use the dedicated command:

.. code-block:: bash

    $ conan cache sign hello/1.0

    hello/1.0: Compressing conan_sources.tgz
    hello/1.0:dee9f7f985eb1c20e3c41afaa8c35e2a34b5ae0b: Compressing conan_package.tgz
    Running command: openssl dgst -sha256 -sign C:\Users\user\.conan2\extensions\plugins\sign\my-organization\private_key.pem -out C:\Users\user\.conan2\p\hello092ffa809a9a1\d\metadata\sign\pkgsign-manifest.json.sig C:\Users\user\.conan2\p\hello092ffa809a9a1\d\metadata\sign\pkgsign-manifest.json
    Package signed for reference hello/1.0
    Running command: openssl dgst -sha256 -sign C:\Users\user\.conan2\extensions\plugins\sign\my-organization\private_key.pem -out C:\Users\user\.conan2\p\b\hello5b13c694fef4a\d\metadata\sign\pkgsign-manifest.json.sig C:\Users\user\.conan2\p\b\hello5b13c694fef4a\d\metadata\sign\pkgsign-manifest.json
    Package signed for reference hello/1.0:dee9f7f985eb1c20e3c41afaa8c35e2a34b5ae0b
    [Package sign] Results:

    hello/1.0
    revisions
        53321bba8793db6fea5ea1a98dd6f3d6
        packages
            dee9f7f985eb1c20e3c41afaa8c35e2a34b5ae0b
            revisions
                4b1eaf2e27996cb39cb3774f185fcd8e

    [Package sign] Summary: OK=2, FAILED=0

As you see, the command is executing the ``sign()`` function of the plugin that uses the ``openssl`` executable to sign the recipe and the package with a command similar to:

.. code-block:: bash

    $ openssl dgst -sha256 -sign private_key.pem -out pkgsign-manifest.json.sig pkgsign-manifest.json

````

And it is also using the conan-generated ``pkgsign-manifest.json`` file to create the signature.
You can read more about this manifest file at :ref:`reference_extensions_package_signing`.


Verifying packages
++++++++++++++++++

For verifying the recipe and package, use the dedicated command:

.. code-block:: bash

    $ conan cache verify hello/1.0

    [Package sign] Checksum verified for file conan_sources.tgz (4ce077cbea9ce87a481b5d6dbb50bd791f4e37e931754cdeb40aeb017baed66c).
    [Package sign] Checksum verified for file conanfile.py (0ec44c268f0f255ab59a246c3d13ae6dbd487dea7635b584236b701047f92ba0).
    [Package sign] Checksum verified for file conanmanifest.txt (f7f00bb74ed8469a367ed02faded3c763130da9b63dae23916b2a4f099625b15).
    Running command: openssl dgst -sha256 -verify C:\Users\user\.conan2\extensions\plugins\sign\my-organization\public_key.pem -signature C:\Users\user\.conan2\p\hello092ffa809a9a1\d\metadata\sign\pkgsign-manifest.json.sig C:\Users\user\.conan2\p\hello092ffa809a9a1\d\metadata\sign\pkgsign-manifest.json
    Package verified for reference hello/1.0
    [Package sign] Checksum verified for file conan_package.tgz (5cc1b9e330fe5bb6ad5904db45d78ecd6bdc71bcc18eff8d19a1ed126ba5a5aa).
    [Package sign] Checksum verified for file conaninfo.txt (f80367b17176346e10640ed813d6d2f1c45ed526822ff71066696179d16e2f2f).
    [Package sign] Checksum verified for file conanmanifest.txt (91429ce32c2d0a99de6459a589ac9c35933ed65165ee5c564b6534da57fdfa65).
    Running command: openssl dgst -sha256 -verify C:\Users\user\.conan2\extensions\plugins\sign\my-organization\public_key.pem -signature C:\Users\user\.conan2\p\b\hello5b13c694fef4a\d\metadata\sign\pkgsign-manifest.json.sig C:\Users\user\.conan2\p\b\hello5b13c694fef4a\d\metadata\sign\pkgsign-manifest.json
    Package verified for reference hello/1.0:dee9f7f985eb1c20e3c41afaa8c35e2a34b5ae0b
    [Package sign] Results:

    hello/1.0
    revisions
        53321bba8793db6fea5ea1a98dd6f3d6
        packages
            dee9f7f985eb1c20e3c41afaa8c35e2a34b5ae0b
            revisions
                4b1eaf2e27996cb39cb3774f185fcd8e

    [Package sign] Summary: OK=2, FAILED=0

As you see, Conan is performing an internal checksum verification for the files and calling the ``verify()`` function of the plugin that uses
the ``openssl`` executable to verify the recipe and the package with a command similar to:

.. code-block:: bash

    $ openssl dgst -sha256 -verify public_key.pem -signature pkgsign-manifest.json.sig pkgsign-manifest.json

.. seealso::

    If you want to create your own package signing plugin, check the reference documentation at
    :ref:`reference_extensions_package_signing`.
