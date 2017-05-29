Conan.io moves to JFrog Bintray!
================================

`JFrog Bintray now supports Conan repositories`_ that work seamlessly with the Conan client letting you freely upload
your C/C++ Conan packages.
All packages currently hosted on conan.io will be migrated to Bintray, and conan.io will be deprecated.

This page describes how you should prepare for the migration and how to use the central Conan repositories on Bintray
that will replace conan.io for your public OSS packages.

.. _`JFrog Bintray now supports Conan repositories`: http://blog.conan.io/2017/05/25/bintray-support-conan-repositories.html

.. _note:
    If you are only using Conan with a private server (conan_server or Artifactory), then this migration does not affect you.


Conan repositories on Bintray
-----------------------------

**Personal repositories**

On Bintray, you can create and manage as many free, personal Conan repositories as you like. On an OSS account, all
packages you upload are public, and anyone can use them by simply adding your repository to their Conan remotes.
To allow collaboration on open source projects, you can also create Organizations in Bintray and add members who will
be able to create and edit packages in your organization’s repositories.

**Central repositories**

Bintray will also host two central repositories:

  - **conan-transit**
    This repository will be an exact copy of the current conan.io repository at the time it is migrated as described below.
    It will be a read-only repository meaning that you can download any packages that it hosts, but will not be able to
    upload any new packages to it.

  - **conan-center**
    This repository will host moderated, curated and well-maintained packages, and is the place where you can share
    your packages with the community. To share your package, you upload it to your own (or your organization’s)
    repositories and submit a request to include it in ``conan-center``.


The migration
-------------


On **June 11, 2017**, from 08:00 CET until 19:00 CET, the conan.io server will be unavailable.
During that time we will migrate all packages from conan.io to the ``conan-transit`` repository on Bintray.

Once service is restored:

  - All the packages that were on conan.io will have been migrated to ``conan-transit``
  - The current conan.io api domain will be redirected to the ``conan-transit`` repository which will be
    available for downloading packages (read only).


conan.io package consumers
--------------------------

If you only consume packages from conan.io you will mostly be unaffected, and there is no preparation required from you
before the migration.

After the migration, any requests to the old server.conan.io domain will be redirected to the new ``conan-transit``
repository on Bintray. Since ``conan-transit``  will contain a copy of all packages in the old conan.io, these requests
will keep working transparently.

Nevertheless, as a best practice, we recommend that you point your Conan client directly to the new repositories as follows:


.. code-block:: bash

   $ conan remote remove conan.io
   $ conan remote add conan-center https://conan.bintray.com
   $ conan remote add conan-transit https://conan-transit.bintray.com

If, for some reason, you still wanted to read from the old conan.io repository, its contents the remote will be https://legacy-server.conan.io

conan.io package creators
-------------------------

If you have created and uploaded packages to conan.io, then you should follow the steps below:


Before the migration
____________________

1. **Create a Bintray Open Source account**

   Browse to https://bintray.com/signup/oss and submit the form to create your account. Note that you don’t have to use
   the same username that you had in your Conan account.


2. **Create a Conan repository**

   If you intend to collaborate with other users, you first need to create a Bintray organization, and create your
   repository under the organization’s profile rather than under your own user profile.

   On your user profile (or organization profile) click “Add new repository”.
   Fill in the Create Repository form making sure to select Conan as the Type.


3. **Get your API key**

   Your API key is the “password” used to authenticate the Conan client to Bintray, NOT your Bintray password.
   To create an API key, you need to edit your user profile.


4. **Add your Bintray repository**

   Add a Conan remote in your Conan client pointing to your Bintray repository

    .. code-block:: bash

      $ conan remote add <REMOTE> <YOUR_BINTRAY_REPO_URL>

   Use the Set Me Up button  on your repository’s page on Bintray to get its URL


5. **Upload your packages**

  Upload all your packages from conan.io to your Conan repository on Bintray. Remember you can use:

  - ``conan install {reference} –all`` to download all your binary packages along with their respective recipes
  - ``conan upload {reference} –all –r bintray`` to upload them all to your personal repository on Bintray.
    When prompted, for a username and  password, enter your Bintray username and your API key

**Note about permissions**:
The username from the references of the Conan packages is not associated to the Bintray user.
For example, on conan.io, the zlib/1.2.8@lasote/stable package can only be uploaded or updated by the user, “lasote”.
On Bintray you can upload any package to a personal repository, even if it belongs to a different Conan user.
For example, a Bintray user called Foo could upload zlib/1.2.8@lasote/stable package to its own repository.


6. **Packages for your own use**

If your packages are just for you, and you are not concerned about sharing them with others or breaking others builds
that might be depending on your packages, you can just remove them from conan.io.
They won’t be migrated to the ``conan-transit``.
Then you will be done, just start using your personal or organization repositories in bintray.



After the migration
___________________


If you are uploading packages for your own internal use, or for use by your team, then your personal or organization’s
repositories are sufficient.

Here is how to configure your Conan client to start using the new Bintray repositories:


.. code-block:: bash

    $ conan remote remove conan.io
    $ conan remote add conan-center https://conan.bintray.com
    $ conan remote add conan-transit https://conan-transit.bintray.com


If, for some reason, you still wanted to read from the old conan.io repository (which by now is read-only),
the new remote should point to https://legacy-server.conan.io

By specifying your remotes in this way, your Conan client will try to resolve packages and to install them from
repositories in the following order of priority:

  1. Your own repository
  2. ``conan-center``
  3. ``conan-transit``

As described above, ``conan-transit`` will contain a snapshot of conan.io at the time it was migrated to Bintray,
including a copy of the packages you had uploaded to your own repositories, and these will all be read-only.
If you now upload new versions to your repositories, ``conan-transit`` will become outdated, however, packages you had
previously loaded before the migration will still be available to your consumers, so none of their builds will break.

**Working with conan-center**

As a moderated and curated repository, ``conan-center`` will not be populated automatically. Initially, it will be empty.
To have your recipe or binary package available on ``conan-center``, you need to submit an inclusion request to Bintray,
and the Bintray team will review your request.


    - If you are the author of an open source library, your package will be approved.
      Keep in mind that it is your responsibility to maintain acceptable standards of quality for all packages your submit
      for inclusion in ``conan-center``.
    - If you are packaging a third-party library, you need to follow the guidelines below:

        - The recipes must contain a :ref:`test_package<packaging_getting_started>`
        - If the library supports it, the recipe has to be compatible with Windows, Linux and OSX.
        - Have CI enabled to test it. (Pending full documentation)
        - Provide a general review of the recipe. Bintray team will make suggestions for improvements or
          better/cleaner ways to do implement the code.

