.. _artifactory_cloud:

Uploading to Artifactory Cloud Instance
=======================================

Conan packages can be uploaded to Artifactory under your own users or organizations. To create a
repository follow these steps:

1. **Create an Artifactory Free-Tier account**

   Browse to https://jfrog.com/community/start-free/ and submit the form to create your account. Note that
   you don't have to use the same username that you use for your Conan account.

   .. image:: ../../images/artifactory/conan-artifactory_create_account.png

2. **Add your Artifactory repository**

   To get the correct address, click on ``Application -> Artifactory -> Artifacts -> Set Me Up``:

   .. image:: ../../images/artifactory/conan-artifactory_setme_up.png

   Add a Conan remote in your Conan client pointing to your Artifactory repository.

   .. code-block:: bash

       $ conan remote add <REMOTE> <YOUR_ARTIFACTORY_REPO_URL>

4. **Get your API key**

   Your API key is the “password” used to authenticate the Conan client to Artifactory, NOT your Artifatory
   password. To get your API key, go to “Set Me Up” and enter your account password. Your API key will
   appear on conan user command line listed on Set Me Up box:

   .. image:: ../../images/artifactory/conan-artifactory_token.png

5. **Set your user credentials**

   Add your Conan user with the API Key, your remote and your Artifatory user name:

   .. code-block:: bash

       $ conan user -p <APIKEY> -r <REMOTE> <USEREMAIL>

Setting the remotes in this way will cause your Conan client to resolve packages and install them from
repositories in the following order of priority:

  1. `conancenter`_
  2. Your own repository

If you want to have your own repository first, please use the ``--insert`` command line option
when adding it:

.. code-block:: bash

    $ conan remote add <your_remote> <your_url> --insert 0
    $ conan remote list
      <your remote>: <your_url> [Verify SSL: True]
      conancenter: https://center.conan.io [Verify SSL: True]

.. tip::

    Check the full reference of :ref:`$ conan remote<conan_remote>` command.


.. _`conancenter`: https://conan.io/center
