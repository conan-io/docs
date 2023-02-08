.. _artifactory:

Artifactory
============

`JFrog's Artifactory <https://jfrog.com/artifactory/>`_ is the single solution for housing and managing all the
artifacts, binaries, packages, files, containers, and components for use throughout your software supply chain. This
pairs nicely with Conan since its power comes from binary management for C/C++. Being able to host these packages for
your team is an essential part.

- `Artifact management options <https://jfrog.com/artifact-management/>`_

    These artifacts need to be stored and shared with all the developers on a project. Some possible solutions include
    a shared drive, a source control management tool or an artifact management repository. A shared drive has limitations
    including limited version control and no artifact deployment capability. A source control management tool is really
    only designed for managing source code text files and not complex artifacts like large binaries.

.. _using_artifactory:

Using Artifactory
-----------------

In Artifactory, you can create and manage as many free, personal Conan repositories as you like.
On an `Free-Tier`_ account, all packages you *upload are public*, and anyone can use them by simply adding your
repository to their Conan remotes. You still can create private repositories using :ref:`Artifactory CE<artifactory_ce>`
or Artifactory Cloud Premium account.

.. important::

    Conan 2.0 support in Artifactory starting around v6.9 with recipe revisions however it is **strongly recommended** to have
    a version above 7.41 which was in use by ConanCenter during the final development and is known to work in the majority of use cases.

    Complete support for Conan 2.0 was introduced with 7.52. Please refer to the `Artifactory Changelog <https://www.jfrog.com/confluence/display/JFROG/Artifactory+Release+Notes>`_
    to ensure no bugfixes appear in more recent versions.

.. _artifactory_ce:

Artifactory Community Edition for C/C++
---------------------------------------

Artifactory Community Edition (CE) for C/C++ is the recommended server for development and hosting private
packages for a team or company. It is completely free, and it features a WebUI, advanced authentication and permissions, great performance
and scalability, a REST API, a generic CLI tool and generic repositories to host any kind of source or binary
artifact.

This is a very brief introduction to Artifactory CE. For the complete Artifactory CE documentation,
visit `Artifactory docs <https://www.jfrog.com/confluence/>`_.

Running Artifactory CE
++++++++++++++++++++++

There are several ways to download and run Artifactory CE. The simplest one might be to download and unzip the
designated zip file, though other installers, including also installing from a Docker image. The `Download Page <https://conan.io/downloads.html>`_ has a link for you to follow.
When the file is unzipped, launch Artifactory by double clicking the artifactory.bat(Windows) or artifactory.sh script in the *app/bin*
subfolder, depending on the OS.
Artifactory comes with JDK bundled, please `read Artifactory requirements <https://www.jfrog.com/confluence/display/JFROG/System+Requirements>`_.

.. image:: ../../images/artifactory/conan-artifactory_ce.png

Once Artifactory has started, navigate to the default URL `http://localhost:8081`, where the Web UI should be running.
The default user and password are ``admin:password``.

Starting with Artifactory Cloud Free-Tier
+++++++++++++++++++++++++++++++++++++++++

Conan packages can be uploaded to Artifactory under your own users or organizations. To create a
repository follow these steps:

1. **Create an Artifactory Free-Tier account**

   Browse to https://jfrog.com/community/start-free/ and submit the form to create your account. Note that
   you don't have to use the same username that you use for your Conan account.

Creating and Using a Conan Repo
-------------------------------

Navigate in the web UI to Admin -> Repositories -> Local, then click on the "New" button. A dialog for selecting the package
type will appear, select Conan, then type a "Repository Key" (the name of the repository you are about to create),
for example "conan-local". You can create multiple repositories to serve different flows, teams, or projects.

Now, it is necessary to configure the client. Go to Artifacts, and click on the created repository. The "Set Me Up"
button in the top right corner provides instructions on how to configure the remote in the Conan client:

.. code-block:: bash

    $ conan remote add artifactory http://localhost:8081/artifactory/api/conan/conan-local


From now, you can upload, download, search, etc. the remote repos similarly to the other repo types.

.. code-block:: bash

    $ conan upload "*" -r=artifactory
    $ conan search "*" -r=artifactory


2. **Add your Artifactory repository**

   To get the correct address, click on ``Application -> Artifactory -> Artifacts -> Set Me Up``:

   Add a Conan remote in your Conan client pointing to your Artifactory repository.

   .. code-block:: bash

       $ conan remote add <REMOTE> <YOUR_ARTIFACTORY_REPO_URL>

4. **Get your API key**

   Your API key is the “password” used to authenticate the Conan client to Artifactory, NOT your Artifactory
   password. To get your API key, go to “Set Me Up” and enter your account password. Your API key will
   appear on conan user command line listed on Set Me Up box:


5. **Set your user credentials**

   Add your Conan user with the API Key, your remote and your Artifactory user name:

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

Migrating from Other Servers
----------------------------

If you are already running another server, for example, the open source *conan_server*, it is easy to migrate
your packages, using the Conan client to download the packages and re-upload them to the new server.

This Python script might be helpful, given that it already defines the respective ``local`` and ``artifactory`` remotes:

.. code-block:: python

    import os
    import subprocess

    def run(cmd):
        ret = os.system(cmd)
        if ret != 0:
            raise Exception("Command failed: %s" % cmd)

    # Assuming local is a conan_server and artifactory are remotes which has been added
    output = subprocess.check_output("conan search -r=local --raw")
    packages = output.splitlines()

    for package in packages:
        print("Downloading %s" % package)
        run("conan download %s -r=local" % package)

    run("conan upload \"*\" --all --confirm -r=artifactory")
