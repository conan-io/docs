.. _reference_extensions_package_signing:

Package signing
---------------

This plugin, which must be located in the cache ``extensions/plugins/sign/sign.py`` file contains 2 methods:

- The ``sign(ref, artifacts_folder, signature_folder)`` executes for every recipe and package that is to
  be uploaded to a server. The ``ref`` is the full reference to the artifact, it can be either a recipe 
  reference or a package reference. The ``artifacts_folder`` is the folder containing the files to be 
  uploaded, typically the ``conanfile.py``, ``conan_package.tgz``, ``conanmanifest.txt``, etc. The
  ``signature_folder`` contains the folder in which the generated files should be written.
- The ``verify(ref, artifacts_folder, signature_folder)`` executes when a package is installed from a 
  server, receives the same arguments as above and should be used to verify the integrity or correctness
  of the signatures


Example of a package signer that puts the artifact filenames in a file called ``signature.asc`` when the
package is uploaded and assert that the downloaded artifacts are in the downloaded ``signature.asc``:


.. code-block:: python

    import os

    def sign(ref, artifacts_folder, signature_folder):
        print("Signing ref: ", ref)
        print("Signing folder: ", artifacts_folder)
        files = []
        for f in sorted(os.listdir(artifacts_folder)):
            if os.path.isfile(os.path.join(artifacts_folder, f)):
                files.append(f)
        signature = os.path.join(signature_folder, "signature.asc")
        open(signature, "w").write("\n".join(files))

    def verify(ref, artifacts_folder, signature_folder):
        print("Verifying ref: ", ref)
        print("Verifying folder: ", artifacts_folder)
        signature = os.path.join(signature_folder, "signature.asc")
        contents = open(signature).read()
        print("verifying contents", contents)
        for f in sorted(os.listdir(artifacts_folder)):
            print("VERIFYING ", f)
            if os.path.isfile(os.path.join(artifacts_folder, f)):
                assert f in contents