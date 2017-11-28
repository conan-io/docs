
Uploading to Bintray
====================


Central repositories
--------------------

Bintray host two central repositories:

  - `conan-transit`_

    This repository is an exact copy of the conan.io repository at **June 11, 2017 08:00 CET**.
    It is a read-only repository, you can download any packages that it hosts, but you are not able to
    upload packages to it.

  - `conan-center`_

    This repository has moderated, curated and well-maintained packages, and is the place where you can share
    your packages with the community. To share your package, you upload it to your own (or your organization’s)
    repositories and submit a request to include it in `conan-center`_. Check :ref:`Working with conan-center<conan_center_flow>`


Using the new Bintray repositories
------------------------------------

Using the new Bintray ``conan-transit`` repository is automatic, as the old ``server.conan.io`` has been automatically redirected to the ``conan-transit`` repository. However, it is preferred if you can update to explicitly use the new repositories, as the redirect is just a temporary solution. To do this, first remove the old conan.io repository, then add the new ones, in order:


.. code-block:: bash

    $ conan remote remove conan.io
    $ conan remote add conan-center https://conan.bintray.com
    $ conan remote add conan-transit https://conan-transit.bintray.com

If, for some reason, you still wanted to read from the old conan.io repository (but please, avoid it if possible), which by now is read-only,
the new remote should point to https://legacy-server.conan.io.

If you are just reading packages, this should be enough. You can navigate the bintray repos from: https://bintray.com/conan


Uploading packages to Bintray
-------------------------------

Conan packages can be uploaded to bintray under your own users or organizations. You can follow these steps:


1. **Create a Bintray Open Source account**

   Browse to https://bintray.com/signup/oss and submit the form to create your account. Note that you don’t have to use
   the same username that you had in your Conan account.

   .. warning::

    Please **make sure you use the Open Source Software OSS account**. 
    Follow this link: https://bintray.com/signup/oss.
    Bintray provides free conan repositories for OSS projects, no need to open a Pro or Enterprise Trial account.
    
2. **Create a Conan repository**

   If you intend to collaborate with other users, you first need to create a Bintray organization, and create your
   repository under the organization’s profile rather than under your own user profile.

   On your user profile (or organization profile) click “Add new repository”.
   Fill in the Create Repository form making sure to select Conan as the Type.

3. **Add your Bintray repository**

   Add a Conan remote in your Conan client pointing to your Bintray repository

    .. code-block:: bash

      $ conan remote add <REMOTE> <YOUR_BINTRAY_REPO_URL>

   Use the Set Me Up button on your repository’s page on Bintray to get its URL

4. **Get your API key**

   Your API key is the “password” used to authenticate the Conan client to Bintray, NOT your Bintray password.
   To get your API key, you need to go to “Edit Your Profile” in your Bintray account and check the *API Key* section.

5. **Set your user credentials**

   Add your conan user with the API Key, your remote and your Bintray user name

    .. code-block:: bash

      $ conan user -p <APIKEY> -r <REMOTE> <USERNAME>

By specifying your remotes in this way, your Conan client will try to resolve packages and to install them from
repositories in the following order of priority:

  1. `conan-center`_
  2. `conan-transit`_
  3. Your own repository

If you want to have your own repository prioritized, please remove the ``conan-transit`` and ``conan-center`` repository, then add yours first, then the others:

.. code-block:: bash

    $ conan remote remove conan-center
    $ conan remote remove conan-transit
    $ conan remote add <your_remote <your_url>
    $ conan remote add conan-center https://conan.bintray.com
    $ conan remote add conan-transit https://conan-transit.bintray.com


As described above, `conan-transit`_ contains a snapshot of conan.io at the time it was migrated to Bintray,
including a copy of the packages you had uploaded to your own repositories, and these will all be read-only.
If you now upload new versions to your repositories, `conan-transit`_ will become outdated, however, packages you had
previously loaded before the migration will still be available to your consumers, so none of their builds will break.

.. _`conan-transit`: https://bintray.com/conan/conan-transit
.. _`conan-center`: https://bintray.com/conan/conan-center
