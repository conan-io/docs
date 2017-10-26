.. _concurrency:


Concurrency
============

From conan 0.28, the conan local cache support some degree of concurrency, allowing simultaneous creation or installation of different packages, or building different binaries for the same package. 

The concurrency is implemented with a Readers-Writers lock mechanism, which in turn uses ``fasteners`` library file locks to achieve multi-platform portability. As this "mutex" resource is by definition not enough to implement a Readers-Writers solution, some active-wait with time sleeps in a loop is necessary. However, this time sleeps will be rare, only sleeping when there is actually a collision and waiting on a lock.

The lock files will be stored inside each ``Pkg/version/user/channel`` folder in the local cache, in a ``rw`` file for locking the entire package, or in a set of locks (one per each different binary package, under a subfolder called ``locks``, each lock named with the binary ID of the package)

It is possible to disable the locking mechanism in ``conan.conf``:

.. code-block:: text

  [general]
  cache_no_locks = True