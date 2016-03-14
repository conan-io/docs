Uploading packages
==================

In the previous section, we built several packages on our local computer. Now, you
might want to upload both the package recipe and the built packages to a conan server for later reuse on another machine, project,
or for sharing them.

This way, if someone includes our package recipe reference in a **[requires]** section of a **conanfile.txt** (Hello/0.1@demo/testing) and his settings matches
with the settings we used to generate our already uploaded packages, conan will directly download the built package. In case that no package
is found, the user could use the package recipe with the **conan install --build** command to generate its own binary package.

.. note::

   If you are just evaluating conan, it is very simple to run a test conan server. You 
   can just run it on your machine. Go to the :doc:`../server`.
         
         
         
First, you can check both your local and remote packages:

.. code-block:: bash

   $ conan search Hello*
   $ conan search Hello* -r=local
   
The latter checks your current ``localhost`` server, but you could also query other servers
like the ``conan.io`` one.


Now, try to upload the package recipe and all the packages:

.. code-block:: bash

   $ conan upload Hello/0.1@demo/testing --all -r=local
   

You might be prompted for a username and password. The local conan server has a demo/demo account
we can use for testing. If you want to try the conan.io server, you need to register first
at the `conan.io <http://www.conan.io>`_ site.
   
The ``--all`` option will upload the package recipe plus all the binary packages. Now try again to read the information from the remote (we refer to it as remote, even
if it is running on your local machine, as it could be run on another server in your LAN):

.. code-block:: bash

   $ conan search Hello* -r=local
   
.. note::

   if something fails during the upload, you can try to upload it again. Conan keeps track of the
   upload integrity and will only upload missing files.
   
Now we can check if we are able to download and use them in a project. For that purpose, we first
have to remove the local copies, otherwise the remote packages will not be downloaded. Since we have
just uploaded them, they are identical to the local ones.

.. code-block:: bash

   $ conan remove Hello*
   $ conan search Hello*

Since we have our test setup from the previous section, we can just use it for our test. Go
to the ``hellopack`` folder and run the tests again, now indicating that we don't want to 
build the sources again, we just want to check if we can download the binaries and use them:

.. code-block:: bash

   $ python build.py --build=never


You will see that the tests are built, but the packages are not. The binaries are simply 
downloaded from the server. You can check their existence on your local computer again with:

.. code-block:: bash

   $ conan search Hello*


.. note::

   This is a basic introduction of the package creation process. You can find out more about
   conan's full packaging capabilities in the :ref:`reference<reference>`.


.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write us</a>
