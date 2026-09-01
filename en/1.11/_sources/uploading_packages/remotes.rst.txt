.. _remotes:

Remotes
=======

In the previous sections, we built several packages on our computer that were stored
in the local cache, typically under *~/.conan/data*. Now, you might want to upload them to a Conan server
for later use on another machine, project, or for sharing purposes.

Conan packages can be uploaded to different remotes previously configured with a name and a URL.
The remotes are just servers used as binary repositories that store packages by reference.

There are several possibilities when uploading packages to a server:

For private development:

- **Artifactory Community Edition for C/C++**: Artifactory Community Edition (CE) for C/C++ is a
  completely free Artifactory server that implements both Conan and generic repositories. It is
  the recommended server for companies and teams wanting to host their own private repository.
  It has a web UI, advanced authentication and permissions, very good performance and scalability,
  a REST API, and can host generic artifacts (tarballs, zips, etc). Check :ref:`artifactory_ce`
  for more information.
- **Artifactory Pro**: Artifactory is the binary repository manager for all major packaging formats. It
  is the recommended remote type for enterprise and professional package management. Check the
  `Artifactory documentation`_ for more information. For a comparison between Artifactory editions,
  check the `Artifactory Comparison Matrix <https://www.jfrog.com/confluence/display/RTF/Artifactory+Comparison+Matrix>`_.
- **Conan server**: Simple, free and open source, MIT licensed server that comes bundled with the Conan client.
  Check :ref:`running_your_server` for more information.

For distribution:

- **Bintray**: Bintray is a cloud platform that gives you full control over how you publish, store,
  promote, and distribute software. You can create binary repositories in Bintray to share Conan
  packages or even create an organization. It is free for open source packages, and the recommended
  server to distribute to the C and C++ communities. Check :ref:`using_bintray` for more information.

.. _bintray_repositories:

Bintray Official Repositories
-----------------------------

Conan official repositories for open source libraries are hosted in Bintray. These repositories are maintained by the Conan
team. Currently there are two central repositories:

.. _conan_center:

Conan Center
++++++++++++

**conan-center**: https://bintray.com/conan/conan-center

.. pull-quote::

   This repository contains moderated, curated and well-maintained packages, and is the place in which you
   can share your packages with the community. To share your package, upload it to your own
   (or your organization's) repositories and submit an inclusion request to `conan-center`_.
   Check :ref:`conan-center guide <conan_center_flow>` for more information.

Conan Transit
+++++++++++++

**conan-transit**: https://bintray.com/conan/conan-transit (DEPRECATED)

.. pull-quote::

   Deprecated. Contains mostly outdated packages some of which are not compatible with the latest Conan
   versions, so refrain from using them. This repository only exists for backward compatibility purposes.
   It is not a default remote in the Conan client and will be completely removed soon. This
   repository is an exact duplicate of the old ``server.conan.io`` repository at
   **June 11, 2017 08:00 CET**. It's a read-only repository, allowing you to only download hosted
   packages.

Conan comes with **conan-center** repository configured by default. Just in case you want to manually configure this repository you can
always add it like this:

.. code-block:: bash

    $ conan remote add conan-center https://conan.bintray.com

Bintray Community Repositories
------------------------------

There are a number of popular community repositories that may be of interest for Conan users for retrieving
open source packages. A number of these repositories are not affiliated with the Conan team.

Bincrafters
+++++++++++

**bincrafters** : https://bintray.com/bincrafters/public-conan

.. pull-quote::

    The `Bincrafters <https://bincrafters.github.io>`_ team builds binary software packages for the
    OSS community. This repository contains a wide and growing variety of Conan packages from
    contributors.

    Use the following command to add this remote to Conan:

    .. code-block:: bash

        $ conan remote add bincrafters https://api.bintray.com/conan/bincrafters/public-conan

Conan Community
+++++++++++++++

**conan-community** : https://bintray.com/conan-community/conan

.. pull-quote::

    Created by Conan developers, and should be considered an incubator for maturing packages before contacting authors or including them in
    `conan-center`_. This repository contains work-in-progress packages that may still not work and may not be fully featured.

    Use the following command to add this remote to Conan:

    .. code-block:: bash

        $ conan remote add conan-community https://api.bintray.com/conan/conan-community/conan

.. note::

    If you are working in a team, you probably want to use the same remotes everywhere: developer machines, CI. The ``conan config install``
    command can automatically define the remotes in a Conan client, as well as other resources as profiles. Have a look at the
    :ref:`conan_config_install` command.


.. _`conan-center`: https://bintray.com/conan/conan-center
.. _Artifactory documentation: https://www.jfrog.com/confluence/display/RTF/Welcome+to+Artifactory
