.. _custom_cache:

Conan local cache: concurrency, Continuous Integration, isolation
=================================================================

Conan needs access to some, per user, configuration files, as the **conan.conf** file that
defines the basic client app configuration. By convention, this file will be located in the
user home folder **~/.conan/**. This folder will typically also store the package cache, in
**~/.conan/data**. Though the latter is configurable in *conan.conf*, conan needs
some place to look for this initial configuration file.

There are some scenarios in which you might want to use different initial locations for the
conan client application:

- Continuous Integration (CI) environments, in which multiple jobs can also work concurrently.
  Moreover, these environments would typically want to run with different user credentials, different
  remote configurations, etc. Note that using Continuous Integration with the same user, with
  isolated machine instances (virtual machines), or with sequential jobs is perfectly possible. For
  example, we use a lot CI cloud services of travis-ci and appveyor.
- Independent per project management and storage. If as a single developer you want to
  manage different projects with different user credentials and/or different remotes, you might find
  that having multiple independent caches makes it easier.

Using different caches is very simple. You can just define the environment variable **CONAN_USER_HOME**.
By setting this variable to different paths, you have multiple conan caches,
something like python "virtualenvs". Just changing the value of **CONAN_USER_HOME** you can
switch among isolated conan instances that will have independent package storage caches, but also
different user credentials, different user default settings, and different remotes configuration.

.. note::

    Use an absolute path or a path starting with ~/ (relative to user home). In Windows do not use quotes.

Windows users:

.. code-block:: bash

   $ SET CONAN_USER_HOME=c:\data
   $ conan install . # call conan normally, config & data will be in c:\data


Linux/macOS users:

.. code-block:: bash

   $ export CONAN_USER_HOME=/tmp/conan
   $ conan install . # call conan normally, config & data will be in /tmp/conan

You can now:

- Build concurrent jobs, parallel builds in Continuous Integration or locally, just setting the variable before launching conan commands.
- You can test locally different user credentials, default configurations, different remotes, just by switching from one cache to the
  others.

.. code-block:: bash

    $ export CONAN_USER_HOME=/tmp/conan
    $ conan search  # using that /tmp/conan cache
    $ conan user  # using that /tmp/conan cache

    $ export CONAN_USER_HOME=/tmp/conan2
    $ conan search  # different packages
    $ conan user  # can be different users

    $ export CONAN_USER_HOME=/tmp/conan  # just go back to use the other cache

.. _concurrency:

Concurrency
-----------

Conan local cache support some degree of concurrency, allowing simultaneous creation or installation of different packages, or building
different binaries for the same package. However, concurrent operations like removal of packages while creating them will fail. If you need
different environments that operate totally independently, you probably want to use different conan caches for that.

The concurrency is implemented with a Readers-Writers lock mechanism, which in turn uses ``fasteners`` library file locks to achieve
multi-platform portability. As this "mutex" resource is by definition not enough to implement a Readers-Writers solution, some active-wait
with time sleeps in a loop is necessary. However, this time sleeps will be rare, only sleeping when there is actually a collision and
waiting on a lock.

The lock files will be stored inside each ``Pkg/version/user/channel`` folder in the local cache, in a ``rw`` file for locking the entire
package, or in a set of locks (one per each different binary package, under a subfolder called ``locks``, each lock named with the binary
ID of the package).

It is possible to disable the locking mechanism in ``conan.conf``:

.. code-block:: text

    [general]
    cache_no_locks = True

System Requirements
-------------------

When ``system_requirements()`` runs, Conan creates the ``system_reqs`` folder. This folder could be created individually by package id or
globally when ``global_system_requirements`` is **True**.

However, sometimes you want to run ``system_requirements()`` again for a specific package, so you
could either remove the ``system_reqs.txt`` file for the specific package id, or you could
:ref:`remove system_reqs globally for the package name referred<conan_remove_system_reqs>`.
