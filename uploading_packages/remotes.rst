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

Central repositories
--------------------

Conan official repositories are hosted in Bintray. Currently there are two central repositories:

**conan-center**: https://bintray.com/conan/conan-center

.. pull-quote::

   This repository has moderated, curated and well-maintained packages, and is the place where you
   can share your packages with the community. To share your package, you upload it to your own (or
   your organization’s) repositories and submit a request to include it in `conan-center`_. Check
   :ref:`Working with conan-center<conan_center_flow>`

**conan-transit**: https://bintray.com/conan/conan-transit

.. pull-quote::

   This repository is an exact copy of the old ``server.conan.io`` repository at **June 11, 2017
   08:00 CET**. It is a read-only repository, sou you can download any packages that it hosts but
   you are not able to upload packages to it. If you now upload new versions to your bintray
   repositories, `conan-transit`_ will become outdated. However, packages you had previously loaded
   before the migration will still be available to your consumers, so none of their builds will
   break.

Community repositories
----------------------

There are some community repositories that may be of interest for conan users to retrieve packages
from:

Bintray community repositories:

- Bincrafters:

- conan-community:

.. _`conan-transit`: https://bintray.com/conan/conan-transit
.. _`conan-center`: https://bintray.com/conan/conan-center
.. _Artifactory documentation: https://www.jfrog.com/confluence/display/RTF/Welcome+to+Artifactory
