.. _devops_save_restore:

Save and restore packages from/to the cache
===========================================

.. include:: ../common/experimental_warning.inc

With the ``conan cache save`` and ``conan cache restore`` commands, it is possible to create a .tgz from one or several packages from a Conan cache and later restore those packages into another Conan cache. There are some scenarios this can be useful:

- In Continuous Integration, specially if doing distributed builds, it might be very convenient to be able to move temporary packages recently built. Most CI systems have the capability of transferring files between jobs for this purpose. The Conan cache is not concurrent, sometimes for paralllel jobs different caches have to be used. 
- For air-gapped setups, in which packages can only be transferred via client side.
- Developers directly sharing some packages with other developers for testing or inspection.


The process of saving the packages is using the ``conan cache save`` command.
It can use a pattern, like the ``conan list`` command, but it can also accept a package-list, like other commands like ``remove, upload, download``. For example:

.. code-block:: bash

  $ conan cache save "pkg/*:*"
  Saving pkg/1.0: p/pkg1df6df1a3b33c
  Saving pkg/1.0:9a4eb3c8701508aa9458b1a73d0633783ecc2270: p/b/pkgd573962ec2c90/p
  Saving pkg/1.0:9a4eb3c8701508aa9458b1a73d0633783ecc2270 metadata: p/b/pkgd573962ec2c90/p
  ...
  # creates conan_cache_save.tgz

The ``conan_cache_save.tgz`` file contains the packages named ``pkg`` (any version), the last recipe revision, and the last package revision of all the package binaries.
The name of the file can be changed with the optional ``--file=xxxx`` argument. Some important considerations:

- The command saves the contents of the cache "recipe" folders, containing the subfolders "export", "export_sources", "download", "source" and recipe "metadata".
- The command saves the contents of the "package" and the package "metadata" folders, but not the binary "build" or "download", that are considered temporary folders.
- If the user doesn't want any of those folders to be saved, they can be cleaned before saving them with ``conan cache clean`` command
- The command saves the cache files and artifacts as well as the metadata (revisions, package_id) to be able to restore those packages in another cache. But it doesn't save any other cache state like ``settings.yml``, ``global.conf``, ``remotes``, etc. If the saved packages require any other specific configuration, it should be managed with ``conan config install``.

We can move this ``conan_cache_save.tgz`` file to another Conan cache and restore it as:

.. code-block:: bash

  $ conan cache restore conan_cache_save.tgz
  Restore: pkg/1.0 in p/pkg1df6df1a3b33c
  Restore: pkg/1.0:9a4eb3c8701508aa9458b1a73d0633783ecc2270 in p/b/pkg773791b8c97aa/p
  Restore: pkg/1.0:9a4eb3c8701508aa9458b1a73d0633783ecc2270 metadata in p/b/pkg773791b8c97aa/d/metadata
  ...

The restore process will overwrite existing packages if they already exist in the cache.


.. note::

   **Best practices**

   - Saving and restoring packages is not a substitute for proper storage (upload) of packages in a Conan server repository.
     It is only intended as a transitory mechanism, in CI systems, to save an air-gap, etc., but not as a long-term storage
     and retrieval.
   - Saving and restoring packages is not a substitute for proper backup of server repositories. The recommended way to 
     implement long term backup of Conan packages is using some server side backup strategy.
   - The storage format and serialization is not guaranteed at this moment to be future-proof and stable. It is expected
     to work in the same Conan version, but future Conan versions might break the storage format created with previous versions. 
     (this is aligned with the above recommendation to not use it as a backup strategy)
