Remotes
=======

In the previous sections, we built several packages in our computer, those packages are stored
in the local cache, typically *~/.conan/data*. Now, you might want to upload them to a conan server
for later reuse on another machine, project, or for sharing them.

Conan packages can be uploaded to different remotes previously configured with a name and an URL.
The remotes are just servers used as binary repositories that store packages by reference.

There are 3 possibilities to have a server where to upload packages:

- **Conan server**: You can run your own conan server that comes packaged with normal conan
  installers. Check :ref:`running_your_server` for more information.
- **Bintray**: Bintray is a cloud platform that gives you full control over how you publish, store,
  promote, and distribute software. You can create binary repositories in Bintray to share conan
  packages or even create an organization. This is the recommended remote type for OSS
  packages. Check :ref:`using_bintray` for more information.
- **Artifactory**: Artifactory is a binary repository manager for all major packaging formats,
  build tools and CI servers. It can host conan packages and manage them. It is the recommended
  remote type for professional package distribution. Check
  `Artifactory documentation`_ for more information.

.. note::

    If you are just evaluating conan, you can create an account on https://bintray.com and create
    a Conan repository, or you can run a conan server.

    - Go to the :doc:`running_your_server` to see how to launch it.
    - Go to the :ref:`Using Bintray<using_bintray>` section to know more about how to use Bintray.

Official repositories
---------------------

Conan official repositories are hosted in Bintray. These repositories are maintained by the Conan
team. Currently there are two central repositories:

**conan-center**: https://bintray.com/conan/conan-center

.. pull-quote::

   This repository has moderated, curated and well-maintained packages, and is the place where you
   can share your packages with the community. To share your package, you can upload it to your own
   (or your organization’s) repositories and submit a request to include it in `conan-center`_.
   Check :ref:`conan-center guide <conan_center_flow>` for more information.

**conan-transit**: https://bintray.com/conan/conan-transit

.. pull-quote::

   This repository is an exact copy of the old ``server.conan.io`` repository at **June 11, 2017
   08:00 CET**. It's a read-only repository, so you can only download hosted packages but
   you won't be able to upload anything else. This repository only exists for backwards
   compatibility and the currently hosted packages **will never be updated**.

Conan comes with both **conan-center** and **conan-transit** repositories configured by default.
Just in case you want to manually configure these repositories you can always add them like this:

.. code-block:: bash

    $ conan remote add conan-center https://conan.bintray.com
    $ conan remote add conan-transit https://conan-transit.bintray.com

If you are just reading packages, this should be enough. You can navigate the bintray repos from:
https://bintray.com/conan

Community repositories
----------------------

There are some popular community repositories that may be of interest for conan users to retrieve
packages from. Some of these repositories are not affiliated with the Conan team.

**bincrafters** : https://bintray.com/bincrafters/public-conan

.. pull-quote::

    The `Bincrafters <https://bincrafters.github.io>`_ team builds binary software packages for the
    OSS community. This repository contains a wide and growing variety of conan packages from
    contributors.

    Use the following command to add this remote to Conan:

    .. code-block:: bash

        $ conan remote add bincrafters https://api.bintray.com/conan/bincrafters/public-conan


.. _`conan-transit`: https://bintray.com/conan/conan-transit
.. _`conan-center`: https://bintray.com/conan/conan-center
.. _Artifactory documentation: https://www.jfrog.com/confluence/display/RTF/Welcome+to+Artifactory
