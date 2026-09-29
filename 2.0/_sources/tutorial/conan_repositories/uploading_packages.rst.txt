.. _uploading_packages:

Uploading Packages
==================

In the previous section we learned how to :ref:`set up a Conan repository
<setting_up_conan_remotes>`. Now we will go through the process of uploading both recipes
and binaries to this remote and store them for later use on another machine, project, or
for sharing purposes.

First, check if the remote you want to upload to is already in your current remote list:

.. code-block:: bash

    $ conan remote list

You can search any remote in the same way you search your Conan local cache. Actually,
many Conan commands can specify a specific remote.

.. code-block:: bash

    $ conan search "*" -r=my_local_server

Now, upload the package recipe and all the packages to your remote. In this example, we
are using our ``my_local_server`` remote, but you could use any other.

.. code-block:: bash

    $ conan upload hello -r=my_local_server

Now try again to read the information from the remote. We refer to it as remote, even if
it is running on your local machine, as it could be running on another server in your LAN:

.. code-block:: bash

    $ conan search hello -r=my_local_server


Now we can check if we can download and use them in a project. For that purpose, we first
have to **remove the local copies**, otherwise the remote packages will not be downloaded. Since we
have just uploaded them, they are identical to the local ones.

.. code-block:: bash

    $ conan remove hello -c
    $ conan list hello

Now, to install the uploaded package from the Conan repository just do:

.. code-block:: bash

    $ conan install --requires=hello/1.0 -r=my_local_server

You can check the package existence on your local computer again with:

.. code-block:: bash

    $ conan list hello


Read more
---------

- :ref:`conan upload command reference <reference_commands_upload>`
- :ref:`conan remote command reference <reference_commands_remote>`
- :ref:`conan search command reference <reference_commands_search>`