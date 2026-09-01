
.. _conan_upload:

conan upload
============

.. code-block:: bash

    $ conan upload [-h] [-p PACKAGE] [-q QUERY] [-r REMOTE] [--all]
                   [--skip-upload] [--force] [--check] [-c] [--retry RETRY]
                   [--retry-wait RETRY_WAIT] [-no [{all,recipe}]] [-j JSON]
                   pattern_or_reference

Uploads a recipe and binary packages to a remote.

If no remote is specified, the first configured remote (by default conan-center, use
'conan remote list' to list the remotes) will be used.

.. code-block:: text

    positional arguments:
      pattern_or_reference  Pattern, recipe reference or package reference e.g.,
                            'boost/*', 'MyPackage/1.2@user/channel', 'MyPackage/1.
                            2@user/channel:af7901d8bdfde621d086181aa1c495c25a17b13
                            7'

    optional arguments:
      -h, --help            show this help message and exit
      -p PACKAGE, --package PACKAGE
                            Package ID [DEPRECATED: use full reference instead]
      -q QUERY, --query QUERY
                            Only upload packages matching a specific query.
                            Packages query: 'os=Windows AND (arch=x86 OR
                            compiler=gcc)'. The 'pattern_or_reference' parameter
                            has to be a reference: MyPackage/1.2@user/channel
      -r REMOTE, --remote REMOTE
                            upload to this specific remote
      --all                 Upload both package recipe and packages
      --skip-upload         Do not upload anything, just run the checks and the
                            compression
      --force               Do not check conan recipe date, override remote with
                            local
      --check               Perform an integrity check, using the manifests,
                            before upload
      -c, --confirm         Upload all matching recipes without confirmation
      --retry RETRY         In case of fail retries to upload again the specified
                            times.

      --retry-wait RETRY_WAIT
                            Waits specified seconds before retry again
      -no [{all,recipe}], --no-overwrite [{all,recipe}]
                            Uploads package only if recipe is the same as the
                            remote one
      -j JSON, --json JSON  json file path where the upload information will be
                            written to


**Examples**:

Uploads a package recipe (*conanfile.py* and the exported files):

.. code-block:: bash

    $ conan upload OpenCV/1.4.0@lasote/stable


Uploads a package recipe and a single binary package:

.. code-block:: bash

    $ conan upload OpenCV/1.4.0@lasote/stable:d50a0d523d98c15bb147b18fa7d203887c38be8b

Uploads a package recipe and all the generated binary packages to a specified remote:

.. code-block:: bash

    $ conan upload OpenCV/1.4.0@lasote/stable --all -r my_remote

Uploads all recipes and binary packages from our local cache to ``my_remote`` without confirmation:

.. code-block:: bash

    $ conan upload "*" --all -r my_remote -c

Uploads the recipe for OpenCV alongside any of its binary packages which are built with settings
``arch=x86_64`` and ``os=Linux`` from our local cache to ``my_remote``:

.. code-block:: bash

    $ conan upload OpenCV/1.4.0@lasote/stable -q 'arch=x86_64 and os=Linux' -r my_remote

Upload all local packages and recipes beginning with "Op" retrying 3 times and waiting 10 seconds
between upload attempts:

.. code-block:: bash

    $ conan upload "Op*" --all -r my_remote -c --retry 3 --retry-wait 10

Upload packages without overwriting the recipe and packages if the recipe has changed:

.. code-block:: bash

    $ conan upload OpenCV/1.4.0@lasote/stable --all --no-overwrite  # defaults to --no-overwrite all

Upload packages without overwriting the recipe if the packages have changed:

.. code-block:: bash

    $ conan upload OpenCV/1.4.0@lasote/stable --all --no-overwrite recipe
