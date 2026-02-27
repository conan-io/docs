.. _registry.txt:

registry.txt
============

This file is generally automatically managed, and it has also access via the :command:`conan remote`
command but just in case you might need to change it. It contains information about the known
remotes and from which remotes are each package retrieved:

.. code-block:: text

    conan-center https://conan.bintray.com True
    local http://localhost:9300 True

    Hello/0.1@demo/testing local


The first section of the file is listing ``remote-name``: ``remote-url`` ``verify_ssl``. Adding, removing or changing
those lines, will add, remove or change the respective remote. If verify_ssl, conan client will verify the SSL certificates
for that remote server.

The second part of the file contains a list of conan-package-reference: remote-name. This is
a reference to which remote was that package retrieved from, which will act also as the default
for operations on that package.

Be careful when modifying the remotes, as the information of the packages has to remain consistent,
e.g. if removing a remote, all package references referencing that remote has to be removed too.
