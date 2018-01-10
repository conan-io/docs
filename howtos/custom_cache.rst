.. _custom_cache:


Conan local cache: concurrency, Continuous Integration, isolation
=========================================================================================

Conan needs access to some, per user, configuration files, as the **conan.conf** file that
defines the basic client app configuration. By convention, this file will be located in the
user home folder **~/.conan/**. This folder will typically also store the package cache, in
**~/.conan/data**. Though the latter is configurable in *conan.conf*, still conan needs
some place to look for this initial configuration file.

There are some scenarios in which you might want to use different initial locations for the
conan client application:

- Continuous Integration (CI) environments, in which multiple jobs can also work concurrently.
  Moreover, these environments would typically want to run with different user credentials, different
  remote configurations, etc. Note that using Continuous Integration with the same user, with
  isolated machine instances (virtual machines), or with sequential jobs is perfectly possible. For
  example, we use a lot CI cloud services of travis-ci and appveyor.
- Independent per project management and storage. If as a single developer you want to
  manage different projects with different user credentials (for the same remote, having different
  users for different remotes is also fine), consuming packages from different remotes, you might
  find that having a single user configuration is not enough. Having independent caches might
  allow also to take away with you very easily the requirements of a certain project.
- Conan supports some concurrency in the local cache. Different packages can be installed or created
  simultaneously, and even different binaries for the same package can be installed or created
  concurrently. However, concurrent operations like removal of packages while creating them will
  fail. If you need different environments that operate totally independently, you probably want
  to use different conan caches for that.


Using different caches is very simple. You can just define the environment variable **CONAN_USER_HOME**.
By setting this variable to different paths, you have multiple conan caches, 
something like python "virtualenvs". Just changing the value of **CONAN_USER_HOME** you can 
switch among isolated conan instantes that will have independent package storage caches, but also
different user credentials, different user default settings, and different remotes configuration.

.. note::

    Use an absolute path or a path starting with ~/ (relative to user home). In Windows do not use quotes.

Windows users:

.. code-block:: bash

   $ SET CONAN_USER_HOME=c:\data
   $ conan install . # call conan normally, config & data will be in c:\data


Linux/OSx users:

.. code-block:: bash

   $ export CONAN_USER_HOME=/tmp/conan
   $ conan install . # call conan normally, config & data will be in /tmp/conan
   
You can now:

- Build concurrent jobs, parallel builds in Continous Integration or locally, just setting the
  variable before launching conan commands
- You can test locally different user credentials, default configurations, different remotes,
  just by switching from one cache to the others:
  
.. code-block:: bash

   $ export CONAN_USER_HOME=/tmp/conan
   $ conan search  # using that /tmp/conan cache
   $ conan user  # using that /tmp/conan cache
   
   $ export CONAN_USER_HOME=/tmp/conan2
   $ conan search  # different packages
   $ conan user  # can be different users
   
   $ export CONAN_USER_HOME=/tmp/conan  # just go back to use the other cache
