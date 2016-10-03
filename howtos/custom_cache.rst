.. _custom_cache:


Virtual environments: concurrency, Continuous Integration, isolation
=========================================================================================

Conan needs access to some, per user, configuration files, as the **conan.conf** file that
defines the basic client app configuration. By convention, this file will be located in the
user home folder **~/.conan/**. This folder will typically also store the package cache, in
**~/.conan/data**. Though this later is configurable in *conan.conf*, still conan needs
some place to look for this initial configuration file.

There are some scenarios in which you might want to use different initial locations for the
conan client application:

- Concurrent builds. If you want to test in parallel the installation of packages that might
  overlap, as two different binary configuration of the same package, this could be a problem
  for the default configuration. Installation of packages uses the ``source()``, ``build()``,
  ``package()`` methods to create the packages, and those methods will be fired only when the
  respective folder do not exist. Concurrently executing the ``source()`` method of the same
  package could have unexpected behavior. Note that it is **totally safe to run concurrent builds**
  of projects depending on installed conan packages. It is also safe to run concurrent installation
  of different packages. The only problem could be trying to install concurrently the same package.
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


Using different caches is very simple. You can just define the environment variable **CONAN_USER_HOME**.
By setting this variable to different paths, you have multiple virtual conan environments, 
something like python "virtualenvs". Just changing the value of **CONAN_USER_HOME** you can 
switch among isolated environments that will have independent package storage caches, but also
different user credentials, different user defaul settings, and different remotes configuration.

**Note:** Use an absolute path and without quotes in Windows.

Windows users:

.. code-block:: bash

   $ SET CONAN_USER_HOME=c:\data
   $ conan install # call conan normally, config & data will be in c:\data


Linux/OSx users:

.. code-block:: bash

   $ export CONAN_USER_HOME=/tmp/conan
   $ conan install # call conan normally, config & data will be in /tmp/conan
   
You can now:

- Build concurrent jobs, parallel builds in Continous Integration or locally, just setting the
  variable before launching conan commands
- You can test locally different user credentials, default configurations, different remotes,
  just by switching from one environment to the others:
  
.. code-block:: bash

   $ export CONAN_USER_HOME=/tmp/conan
   $ conan search  //using that /tmp/conan environment
   $ conan user  //using that /tmp/conan environment
   
   $ export CONAN_USER_HOME=/tmp/conan2
   $ conan search  //different packages
   $ conan user  //can be different users
   
   $ export CONAN_USER_HOME=/tmp/conan  // just go back to use the other environment
  

