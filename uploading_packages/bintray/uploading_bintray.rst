.. _uploading_to_bintray:

Uploading to Bintray
====================

Conan packages can be uploaded to Bintray under your own users or organizations. To create a
repository follow these steps:

1. **Create a Bintray Open Source account**

   Browse to https://bintray.com/signup/oss and submit the form to create your account. Note that
   you don't have to use the same username that you use for your Conan account.

   .. warning::

       Please **make sure you use the Open Source Software OSS account**.
       Follow this link: https://bintray.com/signup/oss.
       Bintray provides free Conan repositories for OSS projects, so there is no need to open a Pro or
       Enterprise Trial account.

2. **Create a Conan repository**

   If you intend to collaborate with other users, you first need to create a Bintray organization,
   and create your repository under the organization’s profile rather than under your own user
   profile.

   In your user profile (or organization profile), click “Add new repository” and fill in the Create
   Repository form. Make sure to select Conan as the Type.

3. **Add your Bintray repository**

   Add a Conan remote in your Conan client pointing to your Bintray repository

   .. code-block:: bash

       $ conan remote add <REMOTE> <YOUR_BINTRAY_REPO_URL>

   Use the Set Me Up button on your repository page on Bintray to get its URL.

4. **Get your API key**

   Your API key is the “password” used to authenticate the Conan client to Bintray, NOT your Bintray
   password. To get your API key, go to “Edit Your Profile” in your Bintray account and
   check the API Key section.

5. **Set your user credentials**

   Add your Conan user with the API Key, your remote and your Bintray user name:

   .. code-block:: bash

       $ conan user -p <APIKEY> -r <REMOTE> <USERNAME>

Setting the remotes in this way will cause your Conan client to resolve packages and install them from
repositories in the following order of priority:

  1. `conan-center`_
  2. Your own repository

If you want to have your own repository first, please use the ``--insert`` command line option
when adding it:

.. code-block:: bash

    $ conan remote add <your_remote> <your_url> --insert 0
    $ conan remote list
      <your remote>: <your_url> [Verify SSL: True]
      conan-center: https://conan.bintray.com [Verify SSL: True]

.. tip::

    Check the full reference of :ref:`$ conan remote<conan_remote>` command.


.. _`conan-center`: https://bintray.com/conan/conan-center
