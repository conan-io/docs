<a id="examples-extensions-package-signing-sigstore"></a>

# Signing packages with Sigstore (Cosign)

This is an example of a package signing plugin implementation using [Sigstore](https://www.sigstore.dev/) via
[Cosign](https://github.com/sigstore/cosign).
You need **Cosign** (version 3.0.0 or newer) on your `PATH`.
See the [Cosign releases](https://github.com/sigstore/cosign/releases) page for binaries.

#### WARNING
This feature is experimental and subject to breaking changes.
See [the Conan stability](https://docs.conan.io/2//introduction.html.md#stability) section for more information.

This example is available in the examples2 repository: [examples/extensions/plugins/sigstore_sign](https://github.com/conan-io/examples2/tree/main/examples/extensions/plugins/sigstore_sign).

#### NOTE
Cosign is used here for demonstration only. The package signing plugin mechanism is backend-agnostic; you could implement
a similar plugin with other tools (for example OpenSSL or GPG) by changing the commands invoked from `sign()` and `verify()`,
as described in [Package signing](https://docs.conan.io/2//reference/extensions/package_signing.html.md#reference-extensions-package-signing).

## Generating the signing key pair

Generate a Cosign key pair (Cosign prompts for a passphrase to protect the private key):

```bash
$ cosign generate-key-pair --output-key-prefix signing
```

This creates `signing.key` (private) and `signing.pub` (public).
Use the passphrase later to set the `COSIGN_PASSWORD` environment variable when configuring the plugin (see below).

## Configuring the plugin

1. Copy `sign.py` and `signing-config.json` from the examples2 folder into your Conan home:

   `CONAN_HOME/extensions/plugins/sign/sign.py`

   `CONAN_HOME/extensions/plugins/sign/signing-config.json`
2. Place the generated keys in a folder named after the **provider** used by the plugin. This example uses `my-organization`
   (the name is hardcoded in `sign.py`):

   `CONAN_HOME/extensions/plugins/sign/my-organization/signing.key`

   `CONAN_HOME/extensions/plugins/sign/my-organization/signing.pub`
3. Set the `COSIGN_PASSWORD` environment variable. The plugin **requires** this variable to be present when signing:
   Cosign reads it instead of prompting on the terminal. Set it to the **private key passphrase** you chose when generating the key pair.
   If the key has **no** passphrase, set `COSIGN_PASSWORD` to an empty value.

Your layout should look like this:

```text
CONAN_HOME/
└── extensions/
    └── plugins/
        └── sign/
            ├── sign.py
            ├── signing-config.json
            └── my-organization/
                ├── signing.key
                └── signing.pub
```

## Implementation

#### NOTE
**Method name convention:** Use the literal string `sigstore` (lowercase) in the `method` field when your plugin uses this
Cosign/Sigstore tools. This is a convenient way to identify the signing method used to sign the package and so the verifier
can pick the right backend.

For signing, `sign()` invokes **cosign sign-blob** on Conan’s `pkgsign-manifest.json`, writes a Sigstore **bundle**
(`artifact.sigstore.json`) next to the manifest, and returns metadata for `pkgsign-signatures.json`:

```python
def sign(ref, artifacts_folder, signature_folder, **kwargs):
    ...
    cosign_sign_cmd = [
        "cosign",
        "sign-blob",
        "--key",
        privkey_filepath,
        "--bundle",
        bundle_filepath,
        "-y",
        f"--signing-config={_signing_config_path()}",
        manifest_filepath,
    ]
    try:
        _run_command(cosign_sign_cmd)
        ConanOutput().success(f"Package signed for reference {ref}")
    except Exception as exc:
        raise ConanException(f"Error signing artifact: {exc}") from exc

    return [
        {
            "method": "sigstore",
            "provider": provider,
            "sign_artifacts": {
                "manifest": "pkgsign-manifest.json",
                "bundle": "artifact.sigstore.json",
            },
        }
    ]
```

For verification, `verify()` reads `pkgsign-signatures.json`, resolves the manifest and bundle paths, loads the public key for
the recorded **provider**, and runs **cosign verify-blob** (without Rekor support):

```python
def verify(ref, artifacts_folder, signature_folder, files, **kwargs):
    ...
    cosign_verify_cmd = [
        "cosign",
        "verify-blob",
        "--key",
        pubkey_filepath,
        "--bundle",
        bundle_filepath,
        "--private-infrastructure=true",
        manifest_filepath,
    ]
    try:
        _run_command(cosign_verify_cmd)
        ConanOutput().success(f"Package verified for reference {ref}")
    except Exception as exc:
        raise ConanException(f"Error verifying signature {bundle_filepath}: {exc}") from exc
```

If verification fails, the plugin raises `ConanException`. On success it does not return a value.

You can read more about `pkgsign-manifest.json` at [Package signing](https://docs.conan.io/2//reference/extensions/package_signing.html.md#reference-extensions-package-signing).

## Signing packages

Create a package and sign it:

```bash
$ conan new cmake_lib -d name=hello -d version=1.0
$ conan create
$ conan cache sign hello/1.0

hello/1.0: Compressing conan_sources.tgz
hello/1.0:dee9f7f985eb1c20e3c41afaa8c35e2a34b5ae0b: Compressing conan_package.tgz
Running command: cosign sign-blob --key .../sign/my-organization/signing.key --bundle .../metadata/sign/artifact.sigstore.json -y --signing-config=.../sign/signing-config.json .../metadata/sign/pkgsign-manifest.json
Package signed for reference hello/1.0
...
[Package sign] Summary: OK=2, FAILED=0
```

#### NOTE
Starting with Conan 2.26.0, **conan upload** does not sign packages automatically. Use **conan cache sign** before upload
when remotes should store signatures. See [Package signing](https://docs.conan.io/2//reference/extensions/package_signing.html.md#reference-extensions-package-signing).

## Verifying packages

Verify recipe and package binaries in the cache:

```bash
$ conan cache verify hello/1.0

[Package sign] Checksum verified for file conan_sources.tgz (...)
...
Running command: cosign verify-blob --key .../sign/my-organization/signing.pub --bundle .../metadata/sign/artifact.sigstore.json --private-infrastructure=true .../metadata/sign/pkgsign-manifest.json
Package verified for reference hello/1.0
...
[Package sign] Summary: OK=2, FAILED=0
```

Packages downloaded from a remote are verified on install (for example **conan install**).

#### SEE ALSO
Plugin API and manifest details: [Package signing](https://docs.conan.io/2//reference/extensions/package_signing.html.md#reference-extensions-package-signing).
