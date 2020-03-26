.. _collaborate_packages:

How to collaborate with other users' packages
=============================================

If a certain existing package does not work for you, or you need to store pre-compiled binaries for a platform not provided by the original
package creator, you might still be able to do so:

Collaborate from source repository
----------------------------------

If the original package creator has the package recipe in a repository, this would be the simplest approach. Just clone the package recipe
on your machine, change something if you want, and then export the package recipe under your own user name. Point your project's
``[requires]`` to the new package name, and use it as usual:

.. code-block:: bash

    $ git clone <repository>
    $ cd <repository>
    //make changes if desired
    $ conan export . <youruser/yourchannel>

You can just directly run:

.. code-block:: bash

    $ conan create . demo/testing

Once you have generated the desired binaries, you can store your pre-compiled binaries in your Bintray repository or on your own Conan
server:

.. code-block:: bash

    $ conan upload package/0.1@myuser/stable -r=myremote --all

Finally, if you made useful changes, you might want to create a pull request to the original repository of the package creator.

Copy a package
--------------

If you don't need to modify the original package creator recipe, it is fine to just copy the package to your local storage. You can copy the
recipes and existing binary packages. This could be enough for caching existing binary packages from the original remote into your own
remote, under your own username:

.. code-block:: bash

   $ conan copy poco/1.9.4@ myuser/testing
   $ conan upload poco/1.9.4@myuser/testing -r=myremote --all
