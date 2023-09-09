.. _conan_backup_sources:

Backing up third-party sources with Conan
=========================================

For recipes and build scripts for open source, publicly available libraries,
it is common practice to download the sources from a canonical source, like Github releases, or project download web pages.
Keeping a record of the origin of these files is useful for traceability purposes.
However, it is often not guaranteed that the files will be available in the long term,
and a user in the future building the same recipe from source may encounter a problem.
Conan can thus can be configured to transparently retrieve sources from a configured mirror,
without modifying the recipes or `conandata.yml`.
Additionally, these sources can be transparently uploaded alongside via ``conan upload``.

The *backup sources* feature is intended for storing the downloaded recipe sources in a file server in our own infrastructure,
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

- A remote backup repository is set up. This should allow ``PUT`` and ``GET`` HTTP methods to modify and fetch its contents.
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

.. note::

   Developers can also set this up in a similar way if needed, specially the ``core.sources:download_urls`` conf


Creating the backup repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
We'll want to create a generic Artifactory remote.
Read :ref:`Creating a public read Artifactory repo<devops_artifactory_new_anonymous_repo>`
for instructions on how to create it and give it public read permissions.

We'll also want to create a separate "backup uploader" user that has manage permissions on our remote, so it's able to write to the repository.
Once the user has the necessary permissions, we'll want to create an access token for the new user too.

<IMAGE>

Setting up the necessary configs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The CI machine's :ref:`global.conf<reference_config_files_global_conf>` file should contain the
``core.sources:download_urls`` and ``core.sources:upload_url`` items, and the `source_credentials.json` file
should also contain the access token we generated in the previous step to allow uploading to the repository.

.. code-block:: text
   :caption: global.conf

   core.sources:download_urls=["<my_artifactory_url>/backup-sources", "origin"]
   core.sources:upload_url="<my_artifactory_url>/backup-sources"


.. code-block:: json
   :caption: source_credentials.json

   {
      "credentials": [

      ]
   }


.. note::

   The recommended approach for dealing with the configuration of CI workers and developers in your organization is
   to install the configs using the ``conan config install`` command on a repository. Read more here **MISSING LINK**


Run Conan as normal
~~~~~~~~~~~~~~~~~~~

With the above steps completed, Conan can now be used as normal, and for every downloaded source,
a copy will be stored locally as explained in the Usage section above.

.. code-block:: text
   :caption: The client will now print information regarding from which remote it was capable of downloading the sources

   $ conan create . --version=1.3

   ...

   ======== Installing packages ========
   zlib/1.3: Calling source() in /Users/ruben/.conan2/p/zlib0f4e45286ecd1/s/src
   zlib/1.3: Sources for ['https://zlib.net/fossils/zlib-1.3.tar.gz', 'https://github.com/madler/zlib/releases/download/v1.3/zlib-1.3.tar.gz'] found in remote backup https://c3i.jfrog.io/artifactory/conan-center-backup-sources/

   -------- Installing package zlib/1.3 (1 of 1) --------

   ...


If we now again try to run this, we'll find that no download is performed and the locally stored version of the files is used.



Upload the packages
~~~~~~~~~~~~~~~~~~~

Once a package has been created as shown above, when the CI now uploads the resulting binary to your Conan repository
with the usual ``conan upload zlib/1.3 -c``, it will now also upload the source backups for that same reference to your backups remote.

<IMAGE>

.. note::

   See <MISSING LINK TO PKGLIST> for a way to only upload the packages that have been built
