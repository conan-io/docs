.. _conan_backup_sources:

Backup sources
==============

The *backup sources* feature is intended for storing the downloaded recipe sources in a secondary location,
allowing future reproducibility of your builds even in the case where the original download URLs are no longer accessible.

The backup is triggered for the :ref:`download<conan_tools_files_get>` and :ref:`get<conan_tools_files_get>` methods
when a ``sha256`` signature is provided.


Configuration
-------------
This feature is controlled by a few configuration items:

core.sources:download_cache
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Local path to store the sources backup to.

core.sources:download_urls
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
List of URLs that Conan will try to download the sources from, where ``origin`` represents the original URL.
This allows to control the fetch order, either ``["origin", "https://your.backup/remote/"]``
to look into and fetch from your backup remote only if and when the original source is not present,
or ``["https://your.backup/remote/", "origin"]`` to prefer your remote ahead of the recipes.
(*Note that being a list, multiple remotes are also possible*)

core.sources:upload_url
~~~~~~~~~~~~~~~~~~~~~~~~~~~
URL of the remote to upload the backups when calling ``conan upload``,
which might or might not be different from any of the URLs defined for download.

core.sources:exclude_urls
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
List of origins to skip backing up.
If the URL passed to ``get``/``download`` starts with any of the origins included in this list,
the source won't be uploaded to the backup remote when calling ``conan upload``.



Usage
-----
The usage of this feature can look something like:

- A remote backup repository is set up. This should allow ``POST`` and ``GET`` HTTP methods to modify and fetch its contents.
  If access credentials are desired, you can use the :ref:`source_credentials.json<reference_config_files_source_credentials>` feature.
  Its URL can then be set in ``core.sources:download_urls`` and ``core.sources:upload_url``.
- In your recipe's ``source()`` method, ensure the relevant ``get``/``download`` calls supply the ``sha256`` signature of the downloaded files.
- Set ``core.sources:download_cache`` in your :ref:`global.conf<reference_config_files_global_conf>` file if a custom location is desired,
  else the default cache folder will be used
- Run Conan normally, creating packages etc.
- Once some sources have been locally downloaded, the path pointed to by ``core.sources:download_cache`` will contain, for each downloaded file:

  - A blob file (no extensions) with the name of the ``sha256`` signature provided in ``get``/``download``.
  - A ``.json`` file which will also have the name of the ``sha256`` signature,
    that will contain information about which references and which mirrors this blob belongs to.

- Calling ``conan upload`` will now optionally upload the backups for the matching references if ``core.sources:upload_url`` is set.
