.. _client_certificates:


client.crt / client.key
=======================

Conan support client TLS certificates. Create a ``client.crt`` with the client certificate in the
conan home directory (default ~/.conan) and a ``client.key`` with the private key.

You could also create only the ``client.crt`` file containing both the certificate and the private key
concatenated.