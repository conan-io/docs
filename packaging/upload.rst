Uploading packages
==================

In the previous sections, we built several packages in our computer, those packages are stored
in a local folder, typically ``~/.conan/data``. Now, you
might want to upload them to a conan server for later reuse on another machine, project,
or for sharing them.

.. note::

   If you are just evaluating conan and don't want to register an account on conan.io,
   it is very simple to run a conan server. You can just run it on your current machine. 
   Go to the :doc:`../server` to see how to launch it.
   
   If you want to upload your packages to the conan.io server, you have to register an account
   first at `conan.io <http://www.conan.io>`_ site. You must also rename your packages 
   from "demo" user to your actual username. This can be done with the ``conan copy`` command.
   
   The rest of this doc will assume you are uploading the packages to your local server.
         

First, check if the remote you want to upload to is already in your current remotes:

.. code-block:: bash

   $ conan remote list


You can add any remote easily. For a remote running in your machine, you could run:

.. code-block:: bash

    $ conan remote add local http://localhost:9300


You can search any remote in the same way you search your computer. Actually many conan
commands can specify a specific remote.

.. code-block:: bash

   $ conan search -v -r=local
   

Now, upload the package recipe and all the packages to your remote. In this example we are using
our ``local`` remote, but you could use any other, including ``conan.io``, which often
is the default one:

.. code-block:: bash

   $ conan upload Hello/0.1@demo/testing --all -r=local
   

You might be prompted for a username and password. The default conan server remote has a demo/demo account
we can use for testing.
   
The ``--all`` option will upload the package recipe plus all the binary packages. Now try again to 
read the information from the remote (we refer to it as remote, even
if it is running on your local machine, as it could be run on another server in your LAN):

.. code-block:: bash

   $ conan search -v -r=local
   
.. note::

   if something fails during the upload, you can try to upload it again. Conan keeps track of the
   upload integrity and will only upload missing files.
   
Now we can check if we are able to download and use them in a project. For that purpose, we first
have to **remove the local copies**, otherwise the remote packages will not be downloaded. Since we have
just uploaded them, they are identical to the local ones.

.. code-block:: bash

   $ conan remove Hello*
   $ conan search -v

Since we have our test setup from the previous section, we can just use it for our test. Go
to your project folder (``hello-use`` or ``greet``) and run the tests again, now saying that we don't want to 
build the sources again, we just want to check if we can download the binaries and use them:

.. code-block:: bash

   $ conan test_package --build=never


You will see that the test is built, but the packages are not. The binaries are simply 
downloaded from your local server. You can check their existence on your local computer again with:

.. code-block:: bash

   $ conan search -v


.. note::

   This is a basic introduction of the package creation process. You can find out more about
   conan's full packaging capabilities in the :ref:`reference<reference>`.


.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write us</a>
