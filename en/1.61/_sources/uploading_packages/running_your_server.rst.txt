.. _running_your_server:

Running conan_server
====================

The *conan_server* is a free and open source server that implements Conan remote repositories. It is a very simple application,
bundled with the regular Conan client installation. In most cases, it is recommended to use the free Artifactory
Community Edition for C/C++ server, check :ref:`artifactory_ce` for more information.

``conan_server`` needs Python>=3.6 for running.

Running the simple open source *conan_server* that comes with the Conan installers (or pip packages) is simple. Just open
a terminal and type:

.. code:: bash

   $ conan_server
   
.. note::

    On Windows, you may experience problems with the server if you run it under bash/msys. It is
    better to launch it in a regular ``cmd`` window.

This server is mainly used for testing (though it might work fine for small teams). If you need a
more stable, responsive and robust server, you should run it from source:

Running from Source (linux)
---------------------------

The Conan installer includes a simple executable **conan_server** for a server quick start.
But you can use the **conan server** through the WSGI application, which means that you can use gunicorn
to run the app, for example.


First, clone the Conan repository from source and install the requirements:

.. code-block:: bash

    $ git clone https://github.com/conan-io/conan.git
    $ cd conan
    $ pip install -r conans/requirements.txt
    $ pip install -r conans/requirements_server.txt
    $ pip install gunicorn
    
    
Run the server application with ``gunicorn``. In the following example, we run the server on port 9300 with four workers and a timeout of 5 minutes (300 seconds, for large uploads/downloads, you can also decrease it if you don't have very large binaries):


.. code-block:: bash

    $ gunicorn -b 0.0.0.0:9300 -w 4 -t 300 conans.server.server_launcher:app


.. note::

    Please note the timeout of ``-t 300`` seconds, resulting in a 5 minute parameter. If your transfers are very large or on a slow network, you might need to increase that value.

You can also bind to an IPv6 address or specify both IPv4 and IPv6 addresses:

.. code-block:: bash

    $ gunicorn -b 0.0.0.0:9300 -b [::1]:9300 -w 4 -t 300 conans.server.server_launcher:app


Server Configuration
--------------------
By default your server configuration is saved under ``~/.conan_server/server.conf``, however you can modify this behaviour by either setting the ``CONAN_SERVER_HOME`` environment variable or launching the server with ``-d`` or ``--server_dir`` command line argument followed by desired path. In case you use one of the options your configuration file will be stored under ``server_directory/server.conf`` Please note that command line argument will override the environment variable. You can change configuration values in ``server.conf``, prior to launching the server. Note that the server does not support hot-reload, and thus in order to see configuration changes you will have to manually relaunch the server.

The server configuration file is by default:

.. code-block:: text

   [server]
   jwt_secret: MnpuzsExftskYGOMgaTYDKfw
   jwt_expire_minutes: 120
   
   ssl_enabled: False
   port: 9300
   public_port:
   host_name: localhost
   
   store_adapter: disk
   authorize_timeout: 1800
   
   # Just for disk storage adapter
   disk_storage_path: ~/.conan_server/data
   disk_authorize_timeout: 1800
   
   updown_secret: NyiSWNWnwumTVpGpoANuyyhR
   
   
   [write_permissions]
   # "opencv/2.3.4@lasote/testing": default_user,default_user2
   
   [read_permissions]  
   # opencv/1.2.3@lasote/testing: default_user default_user2
   # By default all users can read all blocks
   */*@*/*: *
     
   [users]
   demo: demo
   

Server Parameters
+++++++++++++++++

.. note:

    The Conan server from v1.1 supports relative URLs, allowing you to avoid setting ``host_name``, ``public_port`` and ``ssl_enabled``.
    The URLs used to upload/download packages will be automatically generated in the client following the URL of the remote.
    This allows accessing the Conan server from different networks.

* ``port``: Port where **conan_server** will run.
* The client server authorization is done with JWT. ``jwt_secret`` is a random string used to 
  generate authentication tokens. You can change it safely anytime (in fact it is a good practice).
  The change will just force users to log in again. ``jwt_expire_minutes`` is the amount of time
  that users remain logged-in within the client without having to introduce their credentials
  again.

Other parameters (not recommended from Conan 1.1, but necessary for previous versions):

* ``host_name``: If you set ``host_name``, you must use the machine's IP
  where you are running your server (or domain name), something like **host_name: 192.168.1.100**.
  This IP (or domain name) has to be visible (and resolved) by the Conan client, so take it into account
  if your server has multiple network interfaces.

* ``public_port``:  Might be needed when running virtualized, Docker or any other kind of port redirection.
  File uploads/downloads are served with their own URLs, generated by the system, so the file storage backend is independent.
  Those URLs need the public port they have to communicate from the outside. If you leave it 
  blank, the ``port`` value is used.
  
  **Example:** Use conan_server in a Docker container that internally runs in the 9300 port but
  exposes the 9999 port (where the clients will connect to):
  
    .. code-block:: bash 
       
       docker run ... -p9300:9999 ... # Check Docker docs for that
      
      
    **server.conf**
    
    .. code-block:: text
      
      
       [server]
    
       ssl_enabled: False
       port: 9300
       public_port: 9999
       host_name: localhost
  
* ``ssl_enabled`` Conan doesn't handle the SSL traffic by itself, but you can use a proxy like Nginx to redirect the SSL traffic to your Conan server.
  If your Conan clients are connecting with "https", set `ssl_enabled` to True. This way the conan_server will generate the upload/download urls with "https" instead of "http".



.. note::

   **Important**: The Conan client, by default, will validate the server SSL certificates and won't connect if it's invalid.
   If you have self signed certificates you have two options:

   1. Use the :command:`conan remote` command to disable the SSL certificate checks. E.g., *conan remote add/update myremote https://somedir False*
   2. Append the server *.crt* file contents to *~/.conan/cacert.pem* file.

   To learn more, see :ref:`How to manage SSL (TLS) certificates <use_tls_certificates>`.

Conan has implemented an extensible storage backend based on the abstract class ``StorageAdapter``.
Currently, the server only supports storage on ``disk``. The folder in which the uploaded packages
are stored (i.e., the folder you would want to backup) is defined in the ``disk_storage_path``.

The storage backend might use a different channel, and uploads/downloads are authorized up to
a maximum of ``authorize_timeout`` seconds. The value should sufficient so that large downloads/uploads
are not rejected, but not too big to prevent hanging up the file transfers. The value
``disk_authorize_timeout`` is not currently used. File transfers are authorized with their own
tokens, generated with the secret ``updown_secret``. This value should be different from the above
``jwt_secret``.

Running the Conan Server with SSL using Nginx
+++++++++++++++++++++++++++++++++++++++++++++

    **server.conf**

    .. code-block:: text

       [server]
       port: 9300


    **nginx conf file**
    
    .. code-block:: text

       server { 
           listen 443;
           server_name myservername.mydomain.com;
       
           location / {
             proxy_pass http://0.0.0.0:9300;
           }
           ssl on;
           ssl_certificate /etc/nginx/ssl/server.crt;
           ssl_certificate_key /etc/nginx/ssl/server.key;
       }

    **remote configuration in Conan client**

    .. code-block:: text

        $ conan remote add myremote https://myservername.mydomain.com

Running the Conan Server with SSL using Nginx in a Subdirectory
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    **server.conf**

    .. code-block:: text

       [server]
       port: 9300

    **nginx conf file**

    .. code-block:: text

        server {

               listen 443;
               ssl on;
               ssl_certificate /usr/local/etc/nginx/ssl/server.crt;
               ssl_certificate_key /usr/local/etc/nginx/ssl/server.key;
               server_name myservername.mydomain.com;

               location /subdir/ {
                  proxy_pass http://0.0.0.0:9300/;
               }
          }

    **remote configuration in Conan client**

    .. code-block:: text

        $ conan remote add myremote https://myservername.mydomain.com/subdir/

Running Conan Server using Apache
+++++++++++++++++++++++++++++++++

    You need to install ``mod_wsgi``. If you want to use Conan installed from ``pip``, the conf file should be similar to the following example:

    **Apache conf file** (e.g., /etc/apache2/sites-available/0_conan.conf)

    .. code-block:: text

        <VirtualHost *:80>
            WSGIScriptAlias / /usr/local/lib/python3.6/dist-packages/conans/server/server_launcher.py
            WSGICallableObject app
            WSGIPassAuthorization On

            <Directory /usr/local/lib/python3.6/dist-packages/conans>
                Require all granted
            </Directory>
        </VirtualHost>


    If you want to use Conan checked out from source in, for example in `/srv/conan`, the conf file should be as follows:

    **Apache conf file** (e.g., /etc/apache2/sites-available/0_conan.conf)

    .. code-block:: text

        <VirtualHost *:80>
            WSGIScriptAlias / /srv/conan/conans/server/server_launcher.py
            WSGICallableObject app
            WSGIPassAuthorization On

            <Directory /srv/conan/conans>
                Require all granted
            </Directory>
        </VirtualHost>

    The directive ``WSGIPassAuthorization On`` is needed to pass the HTTP basic authentication to Conan.

    Also take into account that the server config files are located in the home of the configured Apache user,
    e.g., var/www/.conan_server, so remember to use that directory to configure your Conan server.

Permissions Parameters
++++++++++++++++++++++

By default, the server configuration when set to Read can be done anonymous,
but uploading requires you to be  registered users. Users can easily be registered in the ``[users]`` section,
by defining a pair of ``login: password`` for each one. Plain text passwords are used at the moment, but
as the server is on-premises (behind firewall), you just need to trust your sysadmin :)

If you want to restrict read/write access to specific packages, configure the ``[read_permissions]``
and ``[write_permissions]`` sections. These sections specify the sequence of patterns and authorized users,
in the form:

.. code-block:: text

    # use a comma-separated, no-spaces list of users
    package/version@user/channel: allowed_user1,allowed_user2

E.g.:

.. code-block:: text

   */*@*/*: * # allow all users to all packages
   PackageA/*@*/*: john,peter # allow john and peter access to any PackageA
   */*@project/*: john # Allow john to access any package from the "project" user
   
The rules are evaluated in order. If the left side of the pattern matches, the rule is applied
and it will not continue searching for matches.

Authentication
++++++++++++++

By default, Conan provides a simple ``user: password`` users list in the ``server.conf`` file.

There is also a plugin mechanism for setting other authentication methods. The process to install any of them 
is a simple two-step process:

1. Copy the authenticator source file into the ``.conan_server/plugins/authenticator`` folder.
2. Add ``custom_authenticator: authenticator_name`` to the ``server.conf`` [server] section.

This is a list of available authenticators, visit their URLs to retrieve them, but also to report issues and collaborate:

- **htpasswd**: Use your server Apache htpasswd file to authenticate users. Get it: https://github.com/d-schiffner/conan-htpasswd
- **LDAP**: Use your LDAP server to authenticate users. Get it: https://github.com/uilianries/conan-ldap-authentication

Create Your Own Custom Authenticator
____________________________________

If you want to create your own Authenticator, create a Python module
in ``~/.conan_server/plugins/authenticator/my_authenticator.py``

**Example:**

.. code-block:: python

     def get_class():
         return MyAuthenticator()


     class MyAuthenticator(object):
         def valid_user(self, username, plain_password):
             return username == "foo" and plain_password == "bar"

The module has to implement:

- A factory function ``get_class()`` that returns a class with a ``valid_user()`` method instance.
- The class containing the ``valid_user()`` that has to return True if the user and password are valid or False otherwise.

Authorizations
++++++++++++++

By default, Conan uses the contents of the ``[read_permissions]`` and ``[write_permissions]`` sections
to authorize or reject a request.

A plugin system is also available to customize the authorization mechanism. The installation of such a plugin
is a simple two-step process:

1. Copy the authorizer's source file into the ``.conan_server/plugins/authorizer`` folder.
2. Add ``custom_authorizer: authorizer_name`` to the ``server.conf`` [server] section.

Create Your Own Custom Authorizer
_________________________________

If you want to create your own Authorizer, create a Python module
in ``~/.conan_server/plugins/authorizer/my_authorizer.py``

**Example:**

.. code-block:: python

     from conans.errors import AuthenticationException, ForbiddenException

     def get_class():
         return MyAuthorizer()

     class MyAuthorizer(object):
         def _check_conan(self, username, ref):
             if ref.user == username:
                 return

             if username:
                 raise ForbiddenException("Permission denied")
             else:
                 raise AuthenticationException()

         def _check_package(self, username, pref):
            self._check(username, pref.ref)

         check_read_conan = _check_conan
         check_write_conan = _check_conan
         check_delete_conan = _check_conan
         check_read_package = _check_package
         check_write_package = _check_package
         check_delete_package = _check_package

The module has to implement:

- A factory function ``get_class()`` that returns an instance of a class conforming to the Authorizer's interface.
- A class that implements all the methods defined in the Authorizer interface:
    - ``check_read_conan()`` is used to decide whether to allow read access to a recipe.
    - ``check_write_conan()`` is used to decide whether to allow write access to a recipe.
    - ``check_delete_conan()`` is used to decide whether to allow a recipe's deletion.
    - ``check_read_package()`` is used to decide whether to allow read access to a package.
    - ``check_write_package()`` is used to decide whether to allow write access to a package.
    - ``check_delete_package()`` is used to decide whether to allow a package's deletion.

The ``check_*_conan()`` methods are called with a username and ``conans.model.ref.ConanFileReference`` instance as their arguments.
Meanwhile the ``check_*_package()`` methods are passed a username and ``conans.model.ref.PackageReference`` instance as their arguments.
These methods should raise an exception, unless the user is allowed to perform the requested action.


Got any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write us</a>
