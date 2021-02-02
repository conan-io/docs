.. _use_tls_certificates:

How to manage SSL (TLS) certificates
====================================


Server certificate validation
-----------------------------

By default, when a remote is added, if the URL schema is ``https``, the Conan client will verify
the certificate using a list of authorities declared in the ``cacert.pem`` file located in the conan home (~/.conan).

If you have a self signed certificate (not signed by any authority) you have two options:

- Use the :ref:`conan remote<conan_remote>` command to disable the SSL verification.
- Append your server ``crt`` file to the ``cacert.pem`` file.


Client certificates
-------------------

If your server is requiring client certificates to validate a connection from a Conan client,
you need to create two files in the conan home directory (default ~/.conan):

- A file ``client.crt`` with the client certificate.
- A file ``client.key`` with the private key.

.. note::

    You can create only the ``client.crt`` file containing both the certificate and the private key
    concatenated and not create the ``client.key``

    If you are a familiar with the `curl <https://curl.haxx.se/docs/manpage.html>`_ tool, this mechanism is
    similar to specify the ``--cert`` / ``--key`` parameters.