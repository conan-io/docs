.. _registry.txt:

registry.txt / registry.json
============================

.. note::

    *registry.json* was introduced in Conan 1.9 and it substitutes the *registry.txt*. Both files are equivalent in content.

This file is generally automatically managed and it stores information about the remotes configured in the Conan client and the installed
packages in your cache associated with the remote they were retrieved from.

.. important::

    The recommendation is not to modify this file directly and only use it as registry information. In case you want to change a remote the
    information of the remotes can be accessed or changed via the :command:`conan remote` command.

.. code-block:: text
   :caption: *registry.txt*

    conan-center https://conan.bintray.com True
    local http://localhost:9300 True

    Hello/0.1@demo/testing local

The first section of the file is listing ``remote-name``: ``remote-url`` ``verify_ssl``. Adding, removing or changing
those lines, will add, remove or change the respective remote. If ``verify_ssl`` is enabled, Conan will verify the SSL certificates for that
remote server.

The second part of the file contains a list of package references and the remote-name. This is a reference to which remote was that package
retrieved from, which will act also as the default for operations on that package.

Here you have an example of the file *registry.json*:

.. code-block:: json
   :caption: *registry.json*

    {
        "remotes":[
            {
                "name":"conan-center",
                "url":"https://api.bintray.com/conan/conan/conan-center",
                "verify_ssl":true
            },
            {
                "name":"artifactory_local",
                "url":"http://192.168.43.191:8081/artifactory/api/conan/conan-local",
                "verify_ssl":true
            },
            {
                "name":"bincrafters",
                "url":"https://api.bintray.com/conan/bincrafters/public-conan",
                "verify_ssl":true
            }
        ],
        "references":{
            "nanomsg/1.1.2@bincrafters/stable":"bincrafters",
            "Poco/1.9.0@pocoproject/stable:09378ed7f51185386e9f04b212b79fe2d12d005c":"conan-center",
            "hello/1.0@user/channel:2bb76c9adac7b8cd7c5e3b377ac9f06934aba606":"artifactory_local"
        },
        "package_references":{
            "nanomsg/1.1.2@bincrafters/stable:26d575619895d584ff4fb07701901d53ff4cdd6b": "bincrafters",
            "Poco/1.9.0@pocoproject/stable:09378ed7f51185386e9f04b212b79fe2d12d005c":"conan-center",
            "hello/1.0@user/channel:2bb76c9adac7b8cd7c5e3b377ac9f06934aba606":"artifactory_local"
        }
    }