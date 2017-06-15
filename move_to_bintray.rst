Conan.io is now on Bintray
==========================

On Bintray, you can create and manage as many free, personal Conan repositories as you like.
On an OSS account, all packages you upload are public, and anyone can use them by simply adding your repository to their
Conan remotes.

To allow collaboration on open source projects, you can also create
`Organizations <https://bintray.com/docs/usermanual/interacting/interacting_bintrayorganizations.html>`_ in Bintray
and add members who will be able to create and edit packages in your organization’s repositories.

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

Using the new Bintray ``conan-transit`` repository is automatic, as the old ``server.conan.io`` has been automatically redirected to the ``conan-transit`` repository. However, it is preferred if you can update to explicitely use the new repositories, as the redirect is just a temporary solution. To do this, first remove the old conan.io repository, then add the new ones, in order:


.. code-block:: bash

    $ conan remote remove conan.io
    $ conan remote add conan-center https://conan.bintray.com
    $ conan remote add conan-transit https://conan-transit.bintray.com

If, for some reason, you still wanted to read from the old conan.io repository (but please, avoid it if possible), which by now is read-only,
the new remote should point to https://legacy-server.conan.io.

If you are just reading packages, this should be enough. You can navigate the bintray repos from: https://bintray.com/conan


Uploading packages to Bintray
-------------------------------

Conan packages can be uploaded to bintray under your own users or organizations. YOu can follow these steps:


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


4. **Add your Bintray repository** (Optional, only if you want to host your packages in Bintray)

   Add a Conan remote in your Conan client pointing to your Bintray repository

    .. code-block:: bash

      $ conan remote add <REMOTE> <YOUR_BINTRAY_REPO_URL>

   Use the Set Me Up button on your repository’s page on Bintray to get its URL


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

.. _conan_center_flow:

Contributing packages to conan-center
--------------------------------------

As a moderated and curated repository, `conan-center`_ will not be populated automatically. Initially, it will be empty.
To have your recipe or binary package available on `conan-center`_, you need to submit an inclusion request to Bintray,
and the Bintray team will review your request.

    - If you are the author of an open source library, your package will be approved.
      Keep in mind that it is your responsibility to maintain acceptable standards of quality for all packages you submit
      for inclusion in `conan-center`_.
    - If you are packaging a third-party library, you need to follow the guidelines below:

        - The recipes must contain a :ref:`test_package<packaging_getting_started>`
        - If the library supports it, the recipe has to be compatible with Windows, Linux and OSX.
        - Have CI enabled to test it. (Pending full documentation)
        - Provide a general review of the recipe. Bintray team will make suggestions for improvements or
          better/cleaner ways to do implement the code.

.. _`conan-transit`: https://bintray.com/conan/conan-transit
.. _`conan-center`: https://bintray.com/conan/conan-center
