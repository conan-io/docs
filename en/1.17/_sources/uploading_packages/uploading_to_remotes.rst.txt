Uploading Packages to Remotes
=============================

First, check if the remote you want to upload to is already in your current remote list:

.. code-block:: bash

    $ conan remote list

You can easily add any remote. To run a remote on your machine:

.. code-block:: bash

    $ conan remote add my_local_server http://localhost:9300

You can search any remote in the same way you search your computer. Actually, many Conan commands
can specify a specific remote.

.. code-block:: bash

    $ conan search -r=my_local_server

Now, upload the package recipe and all the packages to your remote. In this example, we are using
our ``my_local_server`` remote, but you could use any other.

.. code-block:: bash

    $ conan upload Hello/0.1@demo/testing --all -r=my_local_server

You might be prompted for a username and password. The default Conan server remote has a
**demo/demo** account we can use for testing.


The ``--all`` option will upload the package recipe plus all the binary packages. Omitting the
``--all`` option will upload the package recipe *only*. For fine-grained control over which binary
packages are upload to the server, consider using the ``--packages/-p`` or ``--query/-q`` flags.
``--packages`` allows you to explicitly declare which package gets uploaded to the server by
specifying the package ID. ``--query`` accepts a query parameter, e.g. ``arch=armv8 and os=Linux``,
and only uploads binary packages which match this query. When using the ``--query`` flag, ensure
that your query string is enclosed in quotes to make the parameter explicit to your shell. For
example, ``conan upload <package> -q 'arch=x86_64 and os=Linux' ...`` is appropriate use of the
``--query`` flag.

Now try again to read the information from the remote. We refer to it as remote, even if it is running on your local
machine, as it could be running on another server in your LAN:

.. code-block:: bash

    $ conan search Hello/0.1@demo/testing -r=my_local_server

.. note::

    If package upload fails, you can try to upload it again. Conan keeps track of the
    upload integrity and will only upload missing files.

Now we can check if we can download and use them in a project. For that purpose, we first
have to **remove the local copies**, otherwise the remote packages will not be downloaded. Since we
have just uploaded them, they are identical to the local ones.

.. code-block:: bash

    $ conan remove Hello*
    $ conan search

Since we have our test setup from the previous section, we can just use it for our test. Go to your
package folder and run the tests again, now saying that we don't want to build the sources again. We
just want to check if we can download the binaries and use them:

.. code-block:: bash

    $ conan create . demo/testing --not-export --build=never

You will see that the test is built, but the packages are not. The binaries are simply downloaded
from your local server. You can check their existence on your local computer again with:

.. code-block:: bash

    $ conan search
