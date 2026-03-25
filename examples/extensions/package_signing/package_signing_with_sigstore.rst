.. _examples_extensions_package_signing_sigstore:

Signing packages with Sigstore (Cosign)
=======================================

This page describes the `conan Sigstore plugin <https://github.com/danimtb/conan_sigstore_plugin>`_, a reference implementation of the package signing plugin interface that signs Conan manifests using `Sigstore <https://www.sigstore.dev/>`_ via `Cosign <https://github.com/sigstore/cosign>`_.

You need **Cosign** (version greater than 3.0.0) installed on the system and available on your ``PATH``. See the `Cosign releases <https://github.com/sigstore/cosign/releases>`_ page for installation packages.

.. include:: ../../../common/experimental_warning.inc

The plugin source and full README (including CI and tests) live in the repository: `danimtb/conan_sigstore_plugin <https://github.com/danimtb/conan_sigstore_plugin>`_.

.. note::

   Sigstore and Cosign are used here as one possible backend. The package signing
   plugin mechanism is backend-agnostic; other tools (for example OpenSSL or GPG)
   can be integrated with the same Conan hooks by implementing ``sign()`` and
   ``verify()`` as described in :ref:`reference_extensions_package_signing`.

Installing the plugin
+++++++++++++++++++++

Install the extension into your Conan home with :ref:`conan config install<reference_commands_conan_config_install>`:

.. code-block:: bash

    $ conan config install https://github.com/danimtb/conan_sigstore_plugin.git

Conan places the plugin under ``CONAN_HOME/extensions/plugins/sign/`` (for example ``sign.py`` and related files).


Generating the signing key pair
+++++++++++++++++++++++++++++++

Cosign can generate a password-protected key pair. From a shell:

.. code-block:: bash

    $ cosign generate-key-pair --output-key-prefix mykey

This writes ``mykey.key`` (private) and ``mykey.pub`` (public). You will be prompted for a passphrase; **the same passphrase must be available non-interactively when signing**, typically via the ``COSIGN_PASSWORD`` environment variable (see below).


Configuring the plugin
++++++++++++++++++++++

.. caution::

   Storing a private key on disk next to the plugin is convenient for examples only. **Do not rely on that pattern in production.**
   Prefer environment-backed secrets, a hardware or cloud key, or a remote signing service. **Keep private keys out of the Conan cache, out of packages, and out of source control.**

Create or edit ``sigstore-config.yaml`` in the signing plugin directory:

``CONAN_HOME/extensions/plugins/sign/sigstore-config.yaml``

If the file is missing the first time the plugin runs, a template may be created for you to customize.

Minimal example (adjust paths to absolute locations of your keys):

.. code-block:: yaml

    sign:
      enabled: true
      provider: "mycompany"
      private_key: "/absolute/path/to/mykey.key"
      use_rekor: false

    verify:
      enabled: true
      providers:
        mycompany:
          public_key: "/absolute/path/to/mykey.pub"
      use_rekor: false

Each **provider** name ties signing (private key) to verification (public key). You can list multiple providers under ``verify.providers`` if more than one signer is trusted.

Set ``use_rekor: true`` only if you intend to record or check signatures against the `Rekor <https://github.com/sigstore/rekor>`_ transparency log (public Rekor is optional for this plugin).


Environment variables
+++++++++++++++++++++

Environment variables override the YAML file when both are set:

* ``COSIGN_PASSWORD`` — passphrase for the private key (effectively required for unattended signing).
* ``CONAN_SIGSTORE_PLUGIN_ENABLE_SIGN`` — enable or disable signing (signing is on by default).
* ``CONAN_SIGSTORE_PLUGIN_ENABLE_VERIFY`` — enable or disable verification (on by default).
* ``CONAN_SIGSTORE_PLUGIN_ENABLE_REKOR`` — force Rekor usage for sign/verify when set, in line with the plugin’s Rekor support.


How signing and verification work
+++++++++++++++++++++++++++++++++++

When you run :command:`conan cache sign`, Conan generates ``pkgsign-manifest.json`` (checksums of package files), then the plugin signs that manifest with Cosign. Signature metadata is stored in ``pkgsign-signatures.json``; the Sigstore **bundle** (for example ``artifact.sigstore.json``) is included in ``sign_artifacts`` together with the manifest reference. The signing **method** reported in metadata is ``sigstore``.

When you :command:`conan install` from a remote or run :command:`conan cache verify`, Conan checks file checksums against the manifest, then the plugin verifies the Cosign signature using the public key for the provider named in the metadata. Optional Rekor checks apply when enabled.

More detail and the exact JSON shape of ``pkgsign-signatures.json`` are documented in the `plugin README <https://github.com/danimtb/conan_sigstore_plugin/blob/main/README.md>`_.

For the manifest format and plugin API, see :ref:`reference_extensions_package_signing`.


Signing packages
++++++++++++++++

Create a package, then sign recipe and binaries with :command:`conan cache sign`:

.. code-block:: bash

    $ conan new cmake_lib -d name=hello -d version=1.0
    $ conan create
    $ conan cache sign hello/1.0

Successful runs show per-reference signing and a short summary (for example ``OK=2, FAILED=0`` when both recipe and a matching package revision are signed).

.. note::

   Starting with Conan 2.26.0, :command:`conan upload` does not sign packages automatically. Sign with :command:`conan cache sign` before upload if remotes should receive signatures. See :ref:`reference_extensions_package_signing`.


Verifying packages
++++++++++++++++++

Verify locally cached artifacts:

.. code-block:: bash

    $ conan cache verify hello/1.0

Conan verifies checksums of package files, then the plugin verifies the Sigstore/Cosign material for each signature entry. Packages downloaded from a remote are also verified on install when verification is enabled.

.. seealso::

   To implement your own backend or adapt this plugin, use
   :ref:`reference_extensions_package_signing` and the
   `conan_sigstore_plugin <https://github.com/danimtb/conan_sigstore_plugin>`_ source as a starting point.
