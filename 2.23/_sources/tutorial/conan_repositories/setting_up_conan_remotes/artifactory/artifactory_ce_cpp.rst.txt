.. _artifactory_ce_cpp:

Artifactory Community Edition for C/C++
=======================================

Artifactory Community Edition (CE) for C/C++ is the recommended server for development and
hosting private packages for a team or company. It is completely free, and features a
WebUI, advanced authentication and permissions, great performance and scalability, a REST
API, a generic CLI tool and generic repositories to host any kind of source or binary
artifact.

This is a very brief introduction to Artifactory CE. For the complete Artifactory CE
documentation, visit `Artifactory docs <https://jfrog.com/help/>`_.

Running Artifactory CE
----------------------

The recommended way of running Artifactory CE is using Docker.
The latest image is ``releases-docker.jfrog.io/jfrog/artifactory-cpp-ce:latest``:

.. code-block:: bash

    $ docker run --name artifactory -d -e JF_SHARED_DATABASE_TYPE=derby -e JF_SHARED_DATABASE_ALLOWNONPOSTGRESQL=true -p 8081:8081 -p 8082:8082 releases-docker.jfrog.io/jfrog/artifactory-cpp-ce:latest


This is running Artifactory CE with an embedded Derby database. For better performance in production, you might want to check
the `Single node Artifactory installation <https://jfrog.com/help/r/jfrog-installation-setup-documentation/install-artifactory-single-node-with-docker>`_ 
and the full `Artifactory installation guide <https://jfrog.com/help/r/jfrog-installation-setup-documentation>`_.

For versions older than Artifactory 7.77, alternative installation methods like
downloading installers from `Download Page <https://conan.io/downloads.html>`_ are available.
After unzipping these installers, Artifactory can be launched by double-clicking
the ``artifactory.bat`` on Windows or ``artifactory.sh`` script in the *app/bin* subfolder, depending on the OS. 

Once Artifactory has started, navigate to the default URL `http://localhost:8081` where
the Web UI should be running. The default user and password are ``admin:password``.

Creating and Using a Conan Repo
-------------------------------

Navigate to Administration -> Repositories -> Repositories, then click on the "Add
Repositories" button and select "Local Repository". A dialog for selecting the package
type will appear. Select **Conan**, then type a "Repository Key" (the name of the
repository you are about to create), for example "conan-local", and click on "Create Local
Repository". You can create multiple repositories to serve different flows, teams, or
projects.

.. image:: ../../../../images/artifactory/artifactory_local_repository.png

Now, let's configure the Conan client to connect with the "conan-local" repository. First,
add the remote to the Conan remote registry:

.. code-block:: bash

    $ conan remote add artifactory http://localhost:8081/artifactory/api/conan/conan-local

Then configure the credentials for the remote:

.. code-block:: bash

    $ conan remote login artifactory <user> -p <password>

From now, you can upload, download, search, etc. the remote repos similarly to the other
repo types.

.. code-block:: bash

    $ conan upload <package_name> -r=artifactory
    $ conan search "*" -r=artifactory
