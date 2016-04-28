


.. code-block:: bash

   # linux/osx
   $ export HTTP_PROXY="http://10.10.1.10:3128"
   $ export HTTPS_PROXY="http://10.10.1.10:1080"

   # with user/password
   $ export HTTP_PROXY="http://user:pass@10.10.1.10:3128/"
   $ export HTTPS_PROXY="http://user:pass@10.10.1.10:3128/"

   # windows (note, no quotes here)
   $ set HTTP_PROXY=http://10.10.1.10:3128
   $ set HTTPS_PROXY=http://10.10.1.10:1080

This is a temporary solution while conan gets configuration for it (probably in conan.conf)