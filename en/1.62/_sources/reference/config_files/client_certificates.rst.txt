.. _client_certificates:


client.crt / client.key
=======================

Conan support client TLS certificates. Create a *client.crt* with the client certificate in the
Conan home directory (default *~/.conan*) and a *client.key* with the private key.

You could also create only the ``client.crt`` file containing both the certificate and the private key
concatenated.

Alternatively, you can define a path to those files in whichever location using the `client_cert_path` and `client_cert_key_path`
configuration entries in the :ref:`conan_conf`.
