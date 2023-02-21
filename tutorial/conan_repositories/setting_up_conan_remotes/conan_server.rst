.. _conan_server:

Setting-up a Conan Server
=========================

.. important::

    This server is mainly used for testing (though it might work fine for small teams). We
    recommend using :ref:`Artifactory Community Edition for C/C++ <artifactory_ce_cpp>`
    for private development or **Artifactory Pro** as Enterprise solution.

The **Conan Server** is a free and open source server that implements Conan remote
repositories. It is a very simple application, used for testing inside the Conan client
and distributed as a separate pip package.

Install the **Conan Server** using pip:

.. code:: bash

   $ pip install conan-server
