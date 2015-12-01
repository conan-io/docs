Uploading packages
==================

In the previous section we have just created several packages in your local machine. Now, you
might want to upload to a conan server for later reuse in another machine, project or for
sharing it.

.. note::

   If you are just evaluating conan, it is very simple to run a testing conan server, you 
   can just run it in your machine too. Go to the :doc:`../server`.
         
         
         
First, you can check both your local and remote packages:

.. code-block:: bash

   $ conan search Hello*
   $ conan search Hello* -r=local
   
The latter checks your current ``localhost`` server, but you could also query other servers
like the ``conan.io`` one.


Now, try to upload all the packages:

.. code-block:: bash

   $ conan upload Hello/0.1@demo/testing --all -r=local
   

You might be requested for username and password. The local conan server has a demo/demo account
we can use for testing. If you want to try the conan.io server, you need to register first
at the `conan.io <http://www.conan.io>`_ site.
   
The ``--all`` will upload all the binary packages, plus the exported ``conanfile.py`` to the local
server. Now try again to read the information of the remote (we refer to it as remote, even
if it is running in your localhost, as it could be run in other server in your LAN):

.. code-block:: bash

   $ conan search Hello* -r=local
   
.. note::

   if something fails in the upload, you can try to upload it again. Conan keeps track of the
   upload integrity and will only upload missing files
   
Now we can check that we are able to download and use them in a project. For that purpose we
have first to remote the local copies, otherwise the remote packages will not be downloaded, as
they are an exact copy, we just uploaded them.

.. code-block:: bash

   $ conan remove Hello*
   $ conan search Hello*

As we have our test setup from the previous section, we can just use it to test it. Move
to the ``hellopack`` folder and run the tests again, now indicating that we don't want to 
build the sources again, we just want to check if we can download the binaries and use them:

.. code-block:: bash

   $ python build.py --build=never


You will see that the tests are built, but the packages are not, the binaries are just 
downloaded from the server. You can check their existence in your local computer again with:

.. code-block:: bash

   $ conan search Hello*


.. note::

   This is a basic introduction of the package creation process. Go to the reference to check
   conan full packaging capabilities

.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write us</a>
