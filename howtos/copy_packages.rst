.. _copy_packages:


Collaborating: Copying and modifying other user packages
============================================================

If a certain existing package does not work for you, or you need to store pre-compiled
binaries for a platform not provided by the original package creator, you might still
be able to do so:

Collaborate from git repository
---------------------------------

If the original package creator has the package recipe in a repository, this would be 
the simplest approach. Just clone the package recipe in your machine, change something
if you want, and then export the package recipe under your own user name. Point your
project's ``[requires]`` to the new package name, and use it as usual:

.. code-block:: bash

   $ git clone <repository>
   $ cd <repository>
   //make changes if desired
   $ conan export <youruser/yourchannel>

If it has ``test_package``, you can just directly run from there

.. code-block:: bash

   $ conan test_package
   
Otherwise, you should just point your project's ``[requires]`` from the original creator to
the new name, including your user account. You typically will build packages from sources:

.. code-block:: bash

   $ conan install .. --build
   
Once the setup is correct, you can store your pre-compiled binaries in your account, in conan.io
or in your own server:

.. code-block:: bash

   $ conan upload Package/0.1@myuser/stable -r=myremote --all

Finally, if you made useful changes, you might want to create a pull request to the
original repository of the package creator.


Copy a package
---------------

If you don't need to modify the original package creator recipe, it is fine to just
copy the package in your local storage. You can copy the recipes that way, and also existing the package binaries.
This could be sufficient for
caching existing binary packages from the conan.io remote into your own remote, under your
own username:

.. code-block:: bash

   $ conan copy Poco/1.7.8p3@pocoproject/stable myuser/stable
   $ conan upload Poco/1.7.8p3@myuser/testing -r=myremote --all
   
Contribute with binaries
---------------------------
It is possible to contribute pre-compiled binaries to the package of a colleague.
That would be the equivalent of a Pull Request, but with binaries. This would be useful for
teams of developers working in different platforms, so they can create binary packages on
their own machine and contribute them back.
If you think this is an interesting feature, please give feedback: would you prefer this approach,
or would you prefer to use a common account with privileges to different users?
