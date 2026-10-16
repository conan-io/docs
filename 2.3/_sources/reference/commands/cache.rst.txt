.. _reference_commands_cache:

conan cache
===========

Perform file operations in the local cache (of recipes and/or packages).


conan cache path
----------------

.. autocommand::
    :command: conan cache path -h


The ``conan cache path`` returns the path in the cache of a given reference. Depending on the reference, it
could return the path of a recipe, or the path to a package binary. 

Let's say that we have created a package in our current cache with:

.. code-block:: text
    
    $ conan new cmake_lib -d name=pkg -d version=0.1
    $ conan create .
    ...
    Requirements
        pkg/0.1#cdc0d9d0e8f554d3df2388c535137d77 - Cache

    Requirements
        pkg/0.1#cdc0d9d0e8f554d3df2388c535137d77:2401fa1d188d289bb25c37cfa3317e13e377a351 - Build


And now we are interested in obtaining the path where our ``pkg/0.1`` recipe ``conanfile.py`` has been exported:

.. code-block:: text

    $ conan cache path pkg/0.1
    <path to conan cache>/p/5cb229164ec1d245/e

    $ ls <path to conan cache>/p/5cb229164ec1d245/e
    conanfile.py  conanmanifest.txt

By default, if the recipe revision is not specified, it means the "latest" revision in the cache. This can 
also be made explicit by the literal ``#latest``, and also any recipe revision can be explicitly defined,
these commands are equivalent to the above:

.. code-block:: text

    $ conan cache path pkg/0.1#latest
    <path to conan cache>/p/5cb229164ec1d245/e

    # The recipe revision might be different in your case. 
    # Check the "conan create" output to get yours
    $ conan cache path pkg/0.1#cdc0d9d0e8f554d3df2388c535137d77
    <path to conan cache>/p/5cb229164ec1d245/e


Together with the recipe folder, there are a two other folders that are common to all the binaries
produced with this recipe: the "export_source" folder and the "source" folder. Both can be
obtained with:

.. code-block:: text

    $ conan cache path pkg/0.1 --folder=export_source
    <path to conan cache>/p/5cb229164ec1d245/es

    $ ls <path to conan cache>/p/5cb229164ec1d245/es
    CMakeLists.txt  include/  src/

    $ conan cache path pkg/0.1 --folder=source
    <path to conan cache>/p/5cb229164ec1d245/s

    $ ls <path to conan cache>/p/5cb229164ec1d245/s
    CMakeLists.txt  include/  src/


In this case the contents of the "source" folder are identical to the ones of the "export_source" folder
because the recipe did not implement any ``source()`` method that could retrieve code or do any other operation
over the code, like applying patches.

The recipe revision by default will be ``#latest``, this follows the same rules as above.

Note that these two folders will not exist if the package has not been built from source, like when a precompiled
binary is retrieve from a server.
    

It is also possible to obtain the folders of the binary packages providing the ``package_id``:

.. code-block:: text

    # Your package_id might be different, it depends on the platform
    # Check the "conan create" output to obtain yours
    $ conan cache path pkg/0.1:2401fa1d188d289bb25c37cfa3317e13e377a351
    <path to conan cache>/p/1cae77d6250c23b7/p

    $ ls <path to conan cache>/p/1cae77d6250c23b7/p
    conaninfo.txt  conanmanifest.txt  include/  lib/

As above, by default it will resolve to the "latest" recipe revision and package revision.
The command above is equal to explicitly defining ``#latest`` or the exact revisions.
All the commands below are equivalent to the above one:

.. code-block:: text

    $ conan cache path pkg/0.1#latest:2401fa1d188d289bb25c37cfa3317e13e377a351
    <path to conan cache>/p/1cae77d6250c23b7/p

    $ conan cache path pkg/0.1#latest:2401fa1d188d289bb25c37cfa3317e13e377a351#latest
    <path to conan cache>/p/1cae77d6250c23b7/p

    $ conan cache path pkg/0.1#cdc0d9d0e8f554d3df2388c535137d77:2401fa1d188d289bb25c37cfa3317e13e377a351
    <path to conan cache>/p/1cae77d6250c23b7/p


It is possible to access the "build" folder with all the temporary build artifacts:

.. code-block:: text

    $ conan cache path pkg/0.1:2401fa1d188d289bb25c37cfa3317e13e377a351 --folder=build
    <path to conan cache>/p/1cae77d6250c23b7/b

    ls -al <path to conan cache>/p/1cae77d6250c23b7/b
    build/  CMakeLists.txt  CMakeUserPresets.json  conaninfo.txt  include/  src/

Again, the "build" folder will only exist if the package was built from source.


.. note::

    **Best practices**
    
    - This ``conan cache path`` command is intended for eventual inspection of the cache, but the cache
      package storage must be considered **read-only**. Do not modify, change, remove or add files from the cache.
    - If you are using this command to obtain the path to artifacts and then copying them, consider the usage of a ``deployer``
      instead. In the general case, extracting artifacts from the cache manually is discouraged.
    - Developers can use the ``conan list ... --format=compact`` to get the full references in a compact way that can
      be copied and pasted into the ``conan cache path`` command


conan cache clean
-----------------

.. autocommand::
    :command: conan cache clean -h


This command will remove all temporary folders, along with the source, build and download folder
that Conan generates in its execution. It will do so for every matching reference passed in *pattern*,
unless a specific flag is supplied, in which case only the specified folders will be removed.


**Examples**:


- Remove all non-critical files:

  .. code-block:: text

      $ conan cache clean "*"


- Remove all temporary files:

  .. code-block:: text

      $ conan cache clean "*" --temp


- Remove the download folders for the ``zlib`` recipe:

  .. code-block:: text

      $ conan cache clean "zlib*" --download


- Remove everything but the download folder for the ``zlib`` recipe:

  .. code-block:: text

      $ conan cache clean "*" --source --build --temp


conan cache check-integrity
---------------------------

.. autocommand::
    :command: conan cache check-integrity -h


The ``conan cache check-integrity`` command checks the integrity of Conan packages in the
local cache. This means that it will throw an error if any file included in the
``conanmanifest.txt`` is missing or does not match the declared checksum in that file.

For example, to verify the integrity of the whole Conan local cache, do:

.. code-block:: text

    $ conan cache check-integrity "*"
    mypkg/1.0: Integrity checked: ok
    mypkg/1.0:454923cd42d0da27b9b1294ebc3e4ecc84020747: Integrity checked: ok
    mypkg/1.0:454923cd42d0da27b9b1294ebc3e4ecc84020747: Integrity checked: ok
    zlib/1.2.11: Integrity checked: ok
    zlib/1.2.11:6fe7fa69f760aee504e0be85c12b2327c716f9e7: Integrity checked: ok


conan cache backup-upload
-------------------------

.. autocommand::
    :command: conan cache backup-upload -h


The ``conan cache backup-upload`` will upload all source backups present in the local cache to the backup server,
(excluding those which have been fetched from the excluded urls listed in the ``core.sources:exclude_urls`` conf),
regardless of which package they belong to, if any.



conan cache save
----------------

.. autocommand::
    :command: conan cache save -h


Read more in :ref:`devops_save_restore`.


conan cache restore
-------------------

.. autocommand::
    :command: conan cache restore -h


Read more in :ref:`devops_save_restore`.
