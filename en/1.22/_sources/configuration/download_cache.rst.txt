.. _download_cache:

Download cache
==============

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.


Conan implements a shared download cache that can be used to reduce the time needed to populate the Conan package cache
with commands like :command:`install`, :command:`create`.

This cache is purely an optimization mechanism. It is completely different to the :ref:`Conan package cache <custom_cache>`, (typically the ``<userhome>/.conan`` folder).
It is not related to the ``short_paths`` mechanism for long path in Windows, nor to the ``short_paths`` cache folder. The cache will contain a copy
of the artifacts, it is not a new location of files. Those files will still be copied to the Conan package cache, which will not change anything,
its behavior, layout or location of any file.

This cache (whose path can be configured in the *conan.conf* file) will store the following items:

- All files that are downloaded from a Conan server (conan_server, Artifactory), both in the api V1 (without revisions) and V2 (with revisions).
  This includes files like *conanfile.py*, but also the zipped artifacts like *conan_package.tgz* or *conan_sources.tgz*.
- The downloads done by users with the ``tools.download()`` or ``tools.get()`` helpers, as long as they provide a checksum (md5, sha1, etc.). If
  a checksum is not provided, even if the download cache is enabled, the download will be always executed and the files will not be cached.


.. warning::

    The cache computes a sha256 checksum of the download URL and the file checksum whenever is available. As not always the file checksums
    are available, the download cache will not be able to correctly cache artifacts with revisions enabled if a proxy suddenly and
    transparently changes a existing server and moves it to a new location, without the clients changing the URL too.


Activating/deactivating the download cache
------------------------------------------

The download cache is activated and configured in the :ref:`conan_conf` like this:

.. code-block:: text

    [storage]
    download_cache=/path/to/my/cache

It can be defined from the command line:

.. code-block:: bash

    $ conan config set storage.download_cache="/path/to/my/cache"
    # Display it
    $ conan config get storage.download_cache


And, as the *conan.conf* is part of the configuration, you can also put a common *conan.conf* file in a git repo or zip file and use
the :ref:`conan_config_install` command to automatically install it in Conan clients.


To deactivate the download cache, you can remove the entry ``download_cache`` from the *conan.conf* with the command:

.. code-block:: bash

    $ conan config rm storage.download_cache


Concurrency, multiple caches and CI
-----------------------------------

The downloads cache implements exclusive locks for concurrency, so it can be shared among different concurrent Conan instances.
This is a typical scenario in CI servers, in which each job uses a different Conan package cache (defined by ``CONAN_USER_HOME`` environment
variable). Every different Conan instance could configure its download cache to share the same storage. The download cache implements interprocess
exclusive locks, so only 1 process will access at a time to a given cached artifact. If other processes needs the same artifact, they will wait
until it is released, avoiding multiple downloads of the same file, even if they were requested almost simultaneously.

For Continuous Integration processes, it is recommended to have a different Conan package cache (``CONAN_USER_HOME``) for each job, in most of the cases,
because the Conan package cache is not concurrent, and it might also have old dependencies, stale packages, etc. It is better to run CI jobs in a clean
environment.


Removing cached files
---------------------

The download cache will store a lot of artifacts, for all recipes, packages, versions and configurations that are used. This can grow and consume
a lot of storage. If you are using this feature, provide for a sufficiently large and fast download cache folder.

At the moment, it is only a folder. You can clean the cached artifacts just by removing that folder and its contents. You might also be able to 
run scripts and jobs that remove old artifacts only. If you do such operations, please make sure that there are not other Conan processes using
it simultaneously, or they might fail.
