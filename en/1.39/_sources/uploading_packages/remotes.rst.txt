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
  check the `Artifactory Comparison Matrix <https://www.jfrog.com/confluence/display/JFROG/Artifactory+Comparison+Matrix>`_.
- **Conan server**: Simple, free and open source, MIT licensed server that comes bundled with the Conan client.
  Check :ref:`running_your_server` for more information.

For distribution:

- **Artifactory Cloud-hosted instance**: Artifactory Cloud, where JFrog manages, maintains and scales
  the infrastructure and provides automated server backups with free updates and guaranteed uptime.
  It's offered with a free tier designed for individual with reduced usage.
  Check :ref:`artifactory_cloud` for more information.

.. _conan_center:

conancenter
-----------

**ConanCenter** (https://conan.io/center) is the main official repository for open source
Conan packages. It is configured as the default remote in the Conan client, but if you want to add it manually:

.. code-block:: bash

    $ conan remote add conancenter https://center.conan.io

It contains **packages without "user/channel"** that can be used directly as `pkg/version` (`zlib/1.2.11`): These packages are created
automatically from the central GitHub repository `conan-center-index <https://github.com/conan-io/conan-center-index>`_, with an automated
build service: C3I (ConanCenter Continuous Integration).

To contribute packages to ConanCenter, read the :ref:`ConanCenter guide <conan_center_flow>` for more information.

conan-center [deprecated]
-------------------------

**conan-center** was the official repository but is is no longer recommended. It is configured as the second default remote in the Conan
client to keep backwards compatibility:

.. code-block:: bash

    $ conan-center: https://conan.bintray.com [Verify SSL: True]

It contains all the packages from the ConanCenter remote as well as **legacy packages with full reference** (`zlib/1.2.11@conan/stable`).
These package binaries were created by users in their own Bintray repositories and included in this main repository. This flow of
contributing packages to ConanCenter is no longer available and packages are **not recommended** and should be considered as **legacy**.

.. important::

    This remote contains packages that are no longer maintained and will be removed from Conan's default configuration soon. We strongly
    encourage users to use `conancenter` and swift to the official package references without **user/channel**
    (`zlib/1.2.11@conan/stable` -> `zlib/1.2.11`).


.. _`conancenter`: https://conan.io/center
.. _Artifactory documentation: https://www.jfrog.com/confluence/display/JFROG/JFrog+Artifactory
