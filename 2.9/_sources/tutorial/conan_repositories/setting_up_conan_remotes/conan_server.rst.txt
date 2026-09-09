.. _conan_server:

Setting-up a Conan Server
=========================

.. important::

    This server is mainly used for testing (though it might work fine for small teams). We
    recommend using the free :ref:`Artifactory Community Edition for C/C++ <artifactory_ce_cpp>`
    for private development or **Artifactory Pro** as Enterprise solution.

The **Conan Server** is a free and open source server that implements Conan remote
repositories. It is a very simple application, used for testing inside the Conan client
and distributed as a separate pip package.

Install the **Conan Server** using pip:

.. code:: bash

   $ pip install conan-server

Then you can run the server:

.. code:: bash

   $ conan_server
    ***********************
    Using config: /Users/user/.conan_server/server.conf
    Storage: /Users/user/.conan_server/data
    Public URL: http://localhost:9300/v2
    PORT: 9300
    ***********************
    Bottle v0.12.24 server starting up (using WSGIRefServer())...
    Listening on http://0.0.0.0:9300/
    Hit Ctrl-C to quit.

.. note::

    On Windows, you may experience problems with the server if you run it under bash/msys.
    It is better to launch it in a regular ``cmd`` window.

.. seealso::

    * :ref:`Conan Server reference <reference_conan_server>`
