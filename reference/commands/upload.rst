
conan upload
============

.. code-block:: bash

	$ conan upload [-h] [--package PACKAGE] [--remote REMOTE] [--all]
                    [--skip_upload] [--force] [--check] [--confirm]
                    [--retry RETRY] [--retry_wait RETRY_WAIT]
                    pattern

Uploads recipes and binary packages from your local cache to a remote server.

If you use the ``--force`` variable, it won't check the package date. It will override the remote with the local package.

If you use a pattern instead of a conan recipe reference you can use the ``-c`` or ``--confirm`` option to upload all the matching recipes.

If you use the ``--retry`` option you can specify how many times should conan try to upload the packages in case of failure. The default is 2.
With ``--retry_wait`` you can specify the seconds to wait between upload attempts.

If no remote is specified, the first configured remote (by default conan.io, use
``conan remote list`` to list the remotes) will be used.


.. code-block:: bash

	positional arguments:
	  pattern               Pattern or package recipe reference, e.g.,
	                        "openssl/*", "MyPackage/1.2@user/channel"

	optional arguments:
	  -h, --help            show this help message and exit
	  --package PACKAGE, -p PACKAGE
	                        package ID to upload
	  --remote REMOTE, -r REMOTE
	                        upload to this specific remote
	  --all                 Upload both package recipe and packages
	  --skip_upload         Do not upload anything, just run the checks and the
	                        compression.
	  --force               Do not check conan recipe date, override remote with
	                        local
	  --check               Perform an integrity check, using the manifests,
	                        before upload
	  --confirm, -c         If pattern is given upload all matching recipes
	                        without confirmation
	  --retry RETRY         In case of fail it will retry the upload again N times
	  --retry_wait RETRY_WAIT
	                        Waits specified seconds before retry again


**Examples**:

Uploads a package recipe (conanfile.py and the exported files):

.. code-block:: bash

	$ conan upload OpenCV/1.4.0@lasote/stable

Uploads a package recipe and all the generated binary packages to a specified remote:

.. code-block:: bash

	$ conan upload OpenCV/1.4.0@lasote/stable --all -r my_remote


Uploads all recipes and binary packages from our local cache to ``my_remote`` without confirmation:

.. code-block:: bash

   $ conan upload "*" --all -r my_remote -c

Upload all local packages and recipes beginning with "Op" retrying 3 times and waiting 10 seconds between upload attempts:

.. code-block:: bash

   $ conan upload "Op*" --all -r my_remote -c --retry 3 --retry_wait 10

