.. _conan_server:

Setting-up a Conan Server
=========================

.. important::

    This server is mainly used for testing (though it might work fine for small teams). We
    recommend using :ref:`Artifactory Community Edition for C/C++ <artifactory_ce_cpp>` or
    :ref:`Artifactory Cloud-hosted instance <artifactory_free_tier>` for private
    development or :ref:`Artifactory Pro
    <https://www.jfrog.com/confluence/display/JFROG/Artifactory+Comparison+Matrix>`_ as
    Enterprise solution.

The *conan_server* is a free and open source server that implements Conan remote
repositories. It is a very simple application, used for testing inside the Conan client
and distributed as a separate pip package.

Install the :ref:`conan_server <https://pypi.org/project/conan-server/>`_ using pip:

.. code:: bash

   $ pip install conan-server
