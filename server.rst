Running your server
===================

Running the pre-packaged server that comes with the conan installers is simple, just open
a terminal and type:

.. code:: bash

   $ conan_server
   
.. note::

    Windows user under bash/msys terminal might experience problems with the server. Please
    launch it better in a regular ``cmd`` window.

This server is mainly for testing (though it might work fine for small teams), if you want a 
more stable, responsive and robust server, you should run it from source:

Running from source
-------------------
First, install the conan repository from source, as indicated in the installation section.

.. code:: bash

   $ gunicorn .... TODO

Server configuration
--------------------
Your server configuration lives in ``~/.conan_server/server.conf``, you can change values
there, prior to launching the server, it is not reloaded if the values are changed, you
have to stop and restart it manually.

TODO: explain server settings

User management
---------------
Users in server.conf file: TODO


Got any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:support@conan.io" target="_blank">write us</a>
