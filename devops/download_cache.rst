.. _devops_download_cache:

Download Cache
==============

The Conan download cache is a feature intended to cache downloaded artifacts and recipe files, avoiding recurrent downloads of the same files. This is especially useful in Continuous Integration (CI) environments where multiple jobs might require downloading the same packages, or for developers that switch environments frequently.

Configuration
-------------

The download cache is enabled by setting the ``core.download:download_cache`` configuration in the :ref:`global.conf<reference_config_files_global_conf>` file. 

.. code-block:: text
   :caption: global.conf

   core.download:download_cache = /path/to/download_cache

This configuration points to an absolute path to a folder where the Conan packages and downloaded files will be stored *compressed* as they come from the remote server.

Conan has two configuration variables related to the download cache:

- ``core.download:download_cache``: To cache Conan artifacts (like ``conan_package.tgz`` and ``conan_export.tgz``) downloads.
- ``tools.files.download:download_cache``: To cache user downloads performed via the :ref:`download()<conan_tools_files_download>` or :ref:`get()<conan_tools_files_get>` tools in recipes.

By default, ``tools.files.download:download_cache`` defaults to the value of ``core.download:download_cache``. Thus, it is only necessary to define ``core.download:download_cache`` to enable caching for both Conan packages and user recipe downloads. If a different location is desired for user downloads, ``tools.files.download:download_cache`` can be explicitly set.

Usage
-----

Once enabled, every time Conan needs to download a package artifact or a user file, it will first check if the file is present in the cache folder. If it is, it will be copied from the cache to the Conan cache or recipe folder, avoiding the network request. If it is not, it will be downloaded from the remote server and a copy will be stored in the download cache folder.

The download cache is concurrency safe. Multiple concurrent Conan processes can share the same download cache folder simultaneously.

Download cache vs Backup sources
--------------------------------

While both the download cache and the :ref:`backup sources<conan_backup_sources>` features deal with caching downloaded files, they serve different purposes:

- The **download cache** is a local filesystem cache. Its main purpose is to speed up operations and save bandwidth by keeping a local compressed copy of the downloaded files. It is volatile and can be safely cleared at any time.
- The **backup sources** feature is designed to upload third-party source files (like ``.tar.gz`` from GitHub releases) to your own infrastructure (like an Artifactory server) to ensure traceability and reproducibility in case the original URLs go down.
