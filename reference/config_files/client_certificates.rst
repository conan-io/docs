.. _reference_config_files_client_certificates:


Client certificates
===================

Conan supports client TLS certificates. You can configure the path to your existing *Cacert* file and/or your client
certificate (and the key) using the following configuration variables:

* ``core.net.http:cacert_path``: Path containing a custom Cacert file.
* ``core.net.http:client_cert``: Path or tuple of files containing a client cert (and key).

For instance:

.. code-block:: text
    :caption: **[CONAN_HOME]/global.conf**

    core.net.http:cacert_path=/path/to/cacert_file
    core.net.http:client_cert=/path/to/client_certificate


.. seealso::

    You can see more information about configurations in :ref:`global.conf section <reference_config_files_global_conf>`.
