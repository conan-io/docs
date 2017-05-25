Conan.io moves to JFrog Bintray!
================================


`JFrog Bintray now supports Conan repositories`_ that work seamlessly with the Conan client letting you freely upload your C/C++ Conan packages.
This page describes how you should prepare for the migration and how to the new central repositories on Bintray.

.. _`JFrog Bintray now supports Conan repositories`: http://blog.conan.io/2017/05/25/bintray-support-conan-repositories.html

.. _note:
    If you are only using Conan with a private server (conan_server or Artifactory), then this migration does not affect you.


Conan Repositories on Bintray
-----------------------------

- You can have multiple personal free Conan repositories for your packages. Your packages will be public,
  anyone can use them just by adding your repository to their conan remotes.
  You can also create organizations for open source projects and communities.

- Also there will be two central repositories:

    - **conan-transit:** Will contain an exact copy of the current conan.io and will be read only.
    - **conan-center:** Will contain moderated/curated/well maintained packages.
      The users that want to share their packages with the community need to include their packages in this repository by making an inclusion request from their own repositories


The migration
-------------

The day **11 June 2017 at 08:00am CET** the conan.io server will be unavailable **until 07:00pm CET**.

When the service is restored:
    - All the packages will be migrated to conan-transit
    - The current conan.io api domain will be redirected to the ``conan-transit`` repository and will be read only.


conan.io package consumers
--------------------------

If you are just consuming packages from conan.io you will mostly be unaffected. Before the migration date you have nothing to do.

After the migration. The old ``server.conan.io` domain will be redirected to the new Bintray conan-transit repository `
that will contain a copy of the old conan.io, so it will keep working transparently.

However, you are encouraged to directly point your conan client to the new repositories:

.. code-block:: bash

  $ conan remote remove conan.io
  $ conan remote add conan-center https://conan.bintray.com
  $ conan remote add conan-transit https://conan-transit.bintray.com

If for some reason, you still wanted to read (read-only) from the old conan.io repository, the remote will be https://legacy-server.conan.io


conan.io package creators
-------------------------

If you are creating and uploading packages to conan.io, then you should follow these steps:

Before the migration
____________________

1. Go to https://bintray.com/signup/oss and create a Bintray Open Source Account.  It doesn’t matter if the username you had in Conan is already taken. If you are going to collaborate with other users you probably want to create an organization.

2. On your user profile click “Add new repository” and select conan.

3. Get your API-key for your bintray account. This is the **password** you have to use in the conan client to authenticate in Bintray, NOT your bintray password

4. Add a conan remote in your conan client pointing to your bintray repository.


.. code-block:: bash

  $ conan remote add bintray https://conan.bintray.com


You can use the “Set me up” button to get the URL

5. Upload to your conan repository all your packages from conan.io.

   Remember, you can use:

   - ``conan install {reference} –all`` command to download both the recipe and all the binary packages
   - ``conan upload {reference} –all –r bintray`` to upload them all to your personal repository.
     When prompted, for user password, introduce your bintray user and your API key.

**Note about permissions**: The username from the references of the conan packages is not associated to the Bintray user,
for example, on conan.io zlib/1.2.8@lasote/stable package can only be uploaded or updated by the “lasote” user.
On Bintray you can upload any package to a personal repository, for example, the Bintray user “lasote” will be able to upload any
package even if the package belongs to a different Conan username, a user called Foo could upload zlib/1.2.8@lasote/stable package to its own repository.

6. Packages just for you or your team. If your packages are just for you, and you are not concerned about sharing them with others or breaking others builds that might be depending on your packages, you can just remove them from conan.io. They won’t be migrated to the conan-transit. Then you will be done, just start using your personal or organization repositories in bintray.


After the migration
___________________

If you are just using packages for you or your team, then you are already good with using your personal or organization repositories.

First thing is to start using the new bintray repositories:

.. code-block:: bash

    $ conan remote remove conan.io
    $ conan remote add conan-center https://conan.bintray.com
    $ conan remote add conan-transit https://conan-transit.bintray.com


If for some reason, you still wanted to read (read-only) from the old conan.io repository, the remote will be ``https://legacy-server.conan.io``

Remotes created in this order will have the priority:

  - Packages will be installed from your own repo.
  - Then if not found from conan-center.
  - Finally from conan-transit.

Conan-transit will contain a copy of the packages you have in your own repository and it will be read-only.
If you upload new versions to your own repository, the ``conan-transit`` will be outdated, but still used by your consumers so nothing will break.

**In conan-center repository**

This repository will be moderated, and initially empty, if you want to incorporate a recipe or binary packages to ``conan-center`` you need to make an inclusion request.
The inclusion request will be reviewed following some rules:

-  If you are the **author of an Open Source library** your package will be approved. No matter the quality, you are responsible of your library’s package quality.
-  If you are packaging a **third party library**:

    - The recipes must contain a :ref:`test_package<test_package>`
    - If the library supports it, the recipe has to be compatible with Windows, Linux and OSX,
    - Have CI enabled to test it. (conan-package-tools LINK)
    - A general review of the recipe, will suggest improvements or better/cleaner ways to do something
