.. _proxys:

Using proxies
======================

Using a proxy to connect remotes from the client
-------------------------------------------------
The ``~/.conan/conan.conf`` file allows defining proxy information for the conan client.
If you are not using proxies at all, you can just remove the ``[proxies]`` section
completely. You might want to try to use your system defined configuration. You can try to
do this with a blank ``[proxies]`` section:

.. code-block:: text

    [proxies]
    # Empty section will try to use system proxies.
    # If don't want proxy at all, remove section [proxies]
    
You can specify http and https proxies as follows:

.. code-block:: text

    [proxies]
    # As documented in http://docs.python-requests.org/en/latest/user/advanced/#proxies
    http: http://user:pass@10.10.1.10:3128/
    http: http://10.10.1.10:3128
    https: http://10.10.1.10:1080


If this fails, you might also try to set environment variables:

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


Configuring conan server behind a proxy
-----------------------------------------
Todo