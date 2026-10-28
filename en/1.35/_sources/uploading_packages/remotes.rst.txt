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

Conan-center
-------------

**Conan-center** (https://conan.io/center) is the main official repository for open source
Conan packages. It is configured as the default remote in the Conan client, but if you want to add it manually:

.. code-block:: bash

    $ conan remote add conan-center https://conan.bintray.com


There are 2 different types of packages right now in Conan-center:

- **Packages with full reference**: Packages like `pkg/version@user/channel`. These packages binaries were created by users in their own
  Bintray repositories, and included here. This flow of contributing packages to Conan-center is deprecated now.
  These packages are not recommended and should be considered as legacy.
- **Packages without "user/channel"**: Can be used directly as `pkg/version`: These packages are created
  automatically from the central Github repository `conan-center-index <https://github.com/conan-io/conan-center-index>`_,
  with an automated build service: C3I (Conan-Center Continuous Integration). These packages are the recommended
  ones to use from ConanCenter.

To contribute packages to Conan-center, read the :ref:`conan-center guide <conan_center_flow>` for more information.


.. _`conan-center`: https://bintray.com/conan/conan-center
.. _Artifactory documentation: https://www.jfrog.com/confluence/display/JFROG/JFrog+Artifactory
