Running your server
===================

Running the pre-packaged server that comes with the conan installers is simple. Just open
a terminal and type:

.. code:: bash

   $ conan_server
   
.. note::

    On Windows, you might experience problems with the server, if you run it under bash/msys. It is
    better to launch it in a regular ``cmd`` window.

This server is mainly for testing (though it might work fine for small teams). If you need a 
more stable, responsive and robust server, you should run it from source:

Running from source (linux)
---------------------------

The conan installer includes a simple executable **conan_server** for a server quick start.
But you can use the **conan server** trough the WSGI application, which means that you can use gunicorn
to run the app, for example.


First, clone the conan repository from source and install the requirements:

.. code-block:: bash

    $ git clone https://github.com/conan-io/conan.git
    $ cd conan
    $ git checkout master
    $ pip install -r conans/requirements.txt
    $ pip install -r conans/requirements_server.txt
    $ pip install gunicorn
    
    
- Run the server aplication with gunicorn. In the following example we will run server on port 9000 with 4 workers:


.. code-block:: bash

    $ gunicorn -b 0.0.0.0:9000 -w 4 conans.server.server_launcher:app



Server configuration
--------------------
Your server configuration lives in ``~/.conan_server/server.conf``. You can change values
there, prior to launching the server. Not that the server is not reloaded when the values are changed. You
have to stop and restart it manually.

TODO: explain server settings

User management
---------------
Users in server.conf file: TODO


Got any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:support@conan.io" target="_blank">write us</a>
