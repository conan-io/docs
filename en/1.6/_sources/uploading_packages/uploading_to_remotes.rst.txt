Uploading packages to remotes
=============================

First, check if the remote you want to upload to is already in your current remote list:

.. code-block:: bash

    $ conan remote list

You can add any remote easily. For a remote running in your machine, you could run:

.. code-block:: bash

    $ conan remote add my_local_server http://localhost:9300

You can search any remote in the same way you search your computer. Actually, many conan commands
can specify a specific remote.

.. code-block:: bash

    $ conan search -r=my_local_server

Now, upload the package recipe and all the packages to your remote. In this example we are using
our ``my_local_server`` remote, but you could use any other.

.. code-block:: bash

    $ conan upload Hello/0.1@demo/testing --all -r=my_local_server

You might be prompted for a username and password. The default conan server remote has a
**demo/demo** account we can use for testing.

The ``--all`` option will upload the package recipe plus all the binary packages. Now try again to
read the information from the remote (we refer to it as remote, even if it is running on your local
machine, as it could be run on another server in your LAN):

.. code-block:: bash

    $ conan search Hello/0.1@demo/testing -r=my_local_server

.. note::

    If package upload fails, you can try to upload it again. Conan keeps track of the
    upload integrity and will only upload missing files.

Now we can check if we are able to download and use them in a project. For that purpose, we first
have to **remove the local copies**, otherwise the remote packages will not be downloaded. Since we
have just uploaded them, they are identical to the local ones.

.. code-block:: bash

    $ conan remove Hello*
    $ conan search

Since we have our test setup from the previous section, we can just use it for our test. Go to your
package folder and run the tests again, now saying that we don't want to build the sources again, we
just want to check if we can download the binaries and use them:

.. code-block:: bash

    $ conan create . demo/testing --not-export --build=never

You will see that the test is built, but the packages are not. The binaries are simply downloaded
from your local server. You can check their existence on your local computer again with:

.. code-block:: bash

    $ conan search
