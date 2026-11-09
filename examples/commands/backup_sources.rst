.. _examples_commands_backup_sources:

Backing up the sources of third-party dependencies
==================================================

The :ref:`sources backup feature<conan_backup_sources>` transparently uploads the sources downloaded by recipes
(from Github releases, project web pages, etc.) to a server of your own, so that future builds are reproducible
even if the original URLs disappear. By default, those backups are uploaded together with the packages with
:command:`conan upload`. But what if we want to back up the sources of our dependencies **without** building
and uploading any package? This is the case for example for populating the backup server from a CI job, or for
dependencies that are already available in a remote as binaries, and that would be skipped during the upload.

There are two ways to do that, both ending with the :ref:`conan cache backup-upload<reference_commands_cache>` command:

- Retrieving the sources of a full dependency graph with :command:`conan graph info` and ``tools.build:download_source=True``.
- Retrieving the sources of a single recipe with :command:`conan source`.

The ``backup-upload`` command uploads **all** the source backups that are in the cache,
regardless of which package they belong to, if any.


Configuring the backup server
-----------------------------

Let's define the following :ref:`global.conf<reference_config_files_global_conf>`, using the URL of a
backup repository that accepts ``PUT`` and ``GET`` HTTP methods
(see :ref:`how to create one in Artifactory<devops_artifactory_backup_sources_repo>`):

.. code-block:: text
    :caption: global.conf

    core.sources:upload_url=https://myteam.myorg.com/artifactory/backup-sources/
    core.sources:download_urls=["origin", "https://myteam.myorg.com/artifactory/backup-sources/"]

If the repository requires authentication, define it in the :ref:`source_credentials.json<reference_config_files_source_credentials>` file.
Check the :ref:`sources backup configuration<backup_sources_config>` for the rest of the available configuration items,
like ``core.sources:exclude_urls``.


Backing up the sources of a dependency graph
--------------------------------------------

Recipes download their sources in the ``source()`` method, that is only executed when the package is built from source.
The ``tools.build:download_source=True`` conf forces the execution of ``source()`` for all the packages in the graph,
even if there are binaries available, without needing to build anything. This can be done with :command:`conan graph info`
(or :command:`conan install`):

.. code-block:: bash

    $ conan graph info --requires=libiconv/1.17 -c tools.build:download_source=True

Once the sources are downloaded to the Conan cache (to the ``core.sources:download_cache`` folder),
we can upload all of them to the backup server:

.. code-block:: bash

    $ conan cache backup-upload

    -------- Uploading backup sources --------
    Uploading summary '8f74213b56238c85a50a5329f77e06198771e70dd9a739779f4c02f65d971313.json' to backup sources server
    Uploading file '8f74213b56238c85a50a5329f77e06198771e70dd9a739779f4c02f65d971313' to backup sources server
    Upload backup sources complete

Each source is stored in the backup server with the ``sha256`` of the downloaded file as name, plus a ``.json`` file with
the references and original URLs that the file belongs to:

.. code-block:: json
    :caption: 8f74213b56238c85a50a5329f77e06198771e70dd9a739779f4c02f65d971313.json

    {
      "references": {
        "libiconv/1.17": [
          "https://ftpmirror.gnu.org/gnu/libiconv/libiconv-1.17.tar.gz",
          "https://ftp.gnu.org/gnu/libiconv/libiconv-1.17.tar.gz"
        ]
      },
      "timestamp": 1794226585
    }

.. note::

    - Only the sources downloaded with ``get()`` or ``download()`` providing a ``sha256`` are backed up.
    - The ``tools.build:download_source=True`` conf applies to all the packages in the graph, including the
      ``tool_requires``, so their sources will be backed up too. It can be restricted to some packages with
      the conf pattern syntax, like ``-c libiconv/*:tools.build:download_source=True``.
    - Sources that were fetched from a URL in ``core.sources:exclude_urls`` are not uploaded.


Backing up the sources of a single recipe
-----------------------------------------

If we have the recipe in a folder, for example in the Conan Center Index repository or in our own recipes repository,
we can run the :command:`conan source` command directly, which only executes the ``source()`` method
without building anything:

.. code-block:: python
    :caption: conanfile.py

    from conan import ConanFile
    from conan.tools.files import get

    class ZlibRecipe(ConanFile):
        name = "zlib"
        version = "1.3.1"

        def source(self):
            get(self, **self.conan_data["sources"][self.version], strip_root=True)

.. code-block:: yaml
    :caption: conandata.yml

    sources:
      "1.3.1":
        url: "https://github.com/madler/zlib/releases/download/v1.3.1/zlib-1.3.1.tar.gz"
        sha256: "9a93b2b7dfdac77ceba5a558a580e74667dd6fede4585b91eefb60f03b72df23"

.. code-block:: bash

    $ conan source .
    Getting sources for conanfile.py (zlib/1.3.1)
    Calling source() in /home/user/zlib
    Sources correctly downloaded from https://github.com/madler/zlib/releases/download/v1.3.1/zlib-1.3.1.tar.gz
    Uncompressing zlib-1.3.1.tar.gz to .

    $ conan cache backup-upload
    -------- Uploading backup sources --------
    Uploading summary '9a93b2b7dfdac77ceba5a558a580e74667dd6fede4585b91eefb60f03b72df23.json' to backup sources server
    Uploading file '9a93b2b7dfdac77ceba5a558a580e74667dd6fede4585b91eefb60f03b72df23' to backup sources server
    Upload backup sources complete

This approach can be automated for many recipes by simply looping over their folders, and then uploading
all the backups at once with a single ``conan cache backup-upload``.


Using the backup
----------------

Once the sources are in the backup server, any build that has the ``core.sources:download_urls`` conf above
will be able to fetch the sources from it when the original URL is not available (or before trying it,
if the backup server is listed first in ``core.sources:download_urls``). See
:ref:`how to run Conan with the backup configured<conan_backup_sources>` for more details.
