.. _conan_backup_sources:

Backup sources
==============

The *backup sources* feature is intended for storing the downloaded recipe sources in a secondary location,
allowing future reproducibility of your builds even in the case where the original download URLs are no longer accessible.

The backup is triggered for the :ref:`download<conan_tools_files_get>` and :ref:`get<conan_tools_files_get>` methods
when a ``sha256`` signature is provided.


Configuration overview
----------------------

This feature is controlled by a few conf items:

* ``core.sources:download_cache``: Local path to store the sources backup to.
  *If not set, the default Conan home cache path will be used.*
* ``core.sources:download_urls``: List of URLs that Conan will try to download the sources from,
  where ``origin`` represents the original URL.
  This allows to control the fetch order, either ``["origin", "https://your.backup/remote/"]``
  to look into and fetch from your backup remote only if and when the original source is not present,
  or ``["https://your.backup/remote/", "origin"]`` to prefer your remote ahead of the recipes.
  Being a list, multiple remotes are also possible. ``["origin"]`` *by default*
* ``core.sources:upload_url``: URL of the remote to upload the backups when calling ``conan upload``,
  which might or might not be different from any of the URLs defined for download. *Empty by default*
* ``core.sources:exclude_urls``: List of origins to skip backing up.
  If the URL passed to ``get``/``download`` starts with any of the origins included in this list,
  the source won't be uploaded to the backup remote when calling ``conan upload``. *Empty by default*


Usage
-----

Let's overview how the feature works by providing an example on configuring and using the feature in CI from beginning to end:

In summary, it looks something like:

- A remote backup repository is set up. This should allow ``POST`` and ``GET`` HTTP methods to modify and fetch its contents.
  An Artifactory generic repository (available in the free Artifactory CE) can be used for this purpose.
  If access credentials are desired (which is strongly recommended for writing), you can use the :ref:`source_credentials.json<reference_config_files_source_credentials>` feature.
- Its URL can then be set in ``core.sources:download_urls`` and ``core.sources:upload_url``.
- In your recipe's ``source()`` method, ensure the relevant ``get``/``download`` calls supply the ``sha256`` signature of the downloaded files.
- Set ``core.sources:download_cache`` in your :ref:`global.conf<reference_config_files_global_conf>` file if a custom location is desired,
  else the default cache folder will be used
- Run Conan normally, creating packages etc.
- Once some sources have been locally downloaded, the path pointed to by ``core.sources:download_cache`` will contain, for each downloaded file:
   - A blob file (no extensions) with the name of the ``sha256`` signature provided in ``get``/``download``.
   - A ``.json`` file which will also have the name of the ``sha256`` signature,
     that will contain information about which references and which mirrors this blob belongs to.
- Calling ``conan upload`` will now optionally upload the backups for the matching references if ``core.sources:upload_url`` is set.


Creating the backup repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's create the backup repository with Artifactory CE. From the UI, create a generic repo to store the files, we'll imaginatively call it "source-backups".
<IMAGE>

Next, we want to allow anonymous read access for our backups
(We'll touch on the :ref:`source_credentials.json<reference_config_files_source_credentials>` feature for restricting upload access,
if you also want restricted read access, follow those same steps for reading). Create a new user, we'll call it "backup reader",
and from the "Access" tab, give it read permissions to our "source-backups" repo.
<IMAGE>
**CHECK, anonymous read is done the other way around!**

As for uploading permissions, we'll do the same now. Create a new user, this time "backup uploader", and give it "Manage" permisisons.
<IMAGE>
We can now create an access token for our "backup uploader" user and store it. This token needs to go into the `source_credentials.json` file
of our machine/CI worker.
<IMAGE>


Setting up the necessary configs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The CI machine's :ref:`global.conf<reference_config_files_global_conf>` file should contain the
``core.sources:download_urls`` and ``core.sources:upload_url`` items, and the `source_credentials.json` file
should also contain the access token we generated in the previous step.
<IMAGE>

There are a few strategies possible in the ``download_urls`` conf depending on your use-case:

* Origin first: ``["origin", "https://your.backup/remote/"]`` to look into and fetch from your backup remote only if and when the original source is not present.
* Remote first: ``["https://your.backup/remote/", "origin"]`` to prefer your remote ahead of the recipes.
  This is useful for example in CI if you are billed more per outbound connection than staying on your own network if the remote is set up there.

.. note::

   The recommended approach for dealing with the configuration of CI workers and developers in your organization is
   to install the configs using the ``conan config install`` command on a repository. Read more here **MISSING LINK**


As explained above, you can also set ``core.sources:download_cache`` if a custom location for the generated backups is desired,
else the default cache folder will be used.


Run Conan as normal
~~~~~~~~~~~~~~~~~~~

With the above steps completed, Conan can now be used as normal, and for every downloaded sources,
a copy will be stored locally as explained in the Usage section above.

<IMAGES> **maybe? SHow that conan outputs some messages saying that it's used the backup**


Upload the packages
~~~~~~~~~~~~~~~~~~~

Once a package has been created as shown above, when the CI now uploads the resulting binary to your Conan repository
with the usual ``conan upload zlib/1.2.13 -c``, it will now also upload the source backups for that same reference to our backups remote.

<IMAGE>

.. note::

   See <MISSING LINK TO PKGLIST> for a way to only upload the packages that have been built
