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

Running from source (linux)
---------------------------

Conan installer includes a simple executable **conan_server** for a server quick start.
But you can use **conan server** trough the WSGI application so you can run the app, for example, with gunicorn.


First, install the conan repository from source and install the requirements:

.. code-block:: bash

    $ git clone https://github.com/conan-io/conan.git
    $ cd conan
    $ git checkout master
    $ pip install -r conans/requirements.txt
    $ pip install -r conans/requirements_server.txt
    $ pip install gunicorn
    
    
- Run the server aplication with gunicorn, in the following example we will run server in port 9000 with 4 workers:


.. code-block:: bash

    $ gunicorn -b 0.0.0.0:9000 -w 4 conans.server.server_launcher:app



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
