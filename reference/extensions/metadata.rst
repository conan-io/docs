.. _reference_extensions_metadata:

Recipe and package metadata files
=================================

.. include:: ../../common/experimental_warning.inc


A Conan package is typically composed by several C and C++ artifacts, headers, compiled libraries, executables. But there are other files that might not be necessary for the normal consumption of such a package, but that could be very important for compliance, technical or business reasons, for example:

- Logs resulting from the build
- Tests executables that were used to validate the build
- Test or coverage reports of running the test suite
- Debugging artifacts like heavy .pdb files
- Any side generated artifact, like documentation

It is trivial to package these artifacts in the final Conan packages, just using the ``package()`` method, and specifying that we want them as part of the final package. But this has 2 major disadvantages:

- We would be paying the cost of the download and unzip every time we ``install`` this package because it is a necessary dependency to build other packages. This can be a lot of money in data transfer and computing.
- It is not possible to add metadata files once a package has been created, as Conan packages are immutable. But very often it is necessary to add metadata files after the Conan package is there, as a result of some posterior processing with the already created package.


To handle this case, Conan introduces recipe and package metadata files. It is a mechanism to add files to the recipes and package binaries, uploading those files to the servers, so they are stored together with the Conan artifacts. But the metadata will not be downloaded by default when ``conan install`` is executed (or when dependencies are installed in the general case), and the retrieval of metadata will be explicit. 

It is important to highlight that there are two types of metadata:
- Recipe metadata, associated to the ``conanfile.py`` recipe, the metadata should be common to all binaries created from this recipe (package name, version and recipe revision). This metadata will probably be less common, but for example results of some scanning of the source code, that would be common for all configurations and builds, can be recipe metadata.
- Package binary metadata, associated to the package binary for a given specific configuration and represented by a ``package_id``. Build logs, tests reports, etc, that are specific to a binary configuration will be package metadata.

Let's see how metadata can be created, uploaded and downloaded:


Generating metadata from recipes
--------------------------------

It is possible to create both recipe and package metadata directly from recipes, thanks to the ``recipe_metadata_folder`` and the ``pkg_metadata_folder``

.. code-block:: python

    import os
    from conan import ConanFile
    from conan.tools.files import save, copy

    class Meta(ConanFile):
        name = "meta"
        version = "0.1"

        def export(self):
            # Storing in recipe metadata some files existing in the source repo
            copy(self, "*.log", src=self.recipe_folder,
                 dst=os.path.join(self.recipe_metadata_folder, "logs"))

        def source(self):
            save(self, os.path.join("logs", "src.log"), "srclog!!")
            # Copying in recipe metadata some files resulting of the source() method
            # A good example could be automatically generated code that we want a copy
            # for compliance
            copy(self, "logs*", src=".", dst=self.recipe_metadata_folder)

        def build(self):
            # The build can be generating some logs
            save(self, "mylogs.txt", "some logs!!!")

            # Copying the build logs to package metadata
            # This could be moved to the package() method
            copy(self, "mylogs.txt", src=self.build_folder,
                 dst=os.path.join(self.pkg_metadata_folder, "logs"))


With this recipe, we can do:

.. code-block:: bash

    $ conan create .
    # It will create the Conan package
    # And the recipe and package metadata

The metadata capture also works locally. If instead of creating a package you are executing local methods:

.. code-block:: bash

    $ conan source .
    # It will call source() method
    # and store files in a "metadata" local folder
    $ conan build .
    # It will call build() method
    # and store files in a "metadata" local folder

Note that we haven't defined a ``layout()`` method in the above, but in practice, this would be recommended, and it will
also avoid metadata folder collisions for this case.


Reading metadata
----------------

How can we check and read what metadata was created? Using the ``conan cache path`` command we get access to the Cache folders:

.. code-block:: bash

    # To obtain the recipe metadata
    # (it defaults to the latest revision, use meta/0.1#revision if want another one)
    $ conan cache path meta/0.1 --folder=metadata
    <userhome>/.conan2/p/meta98daf335d1d77/d/metadata
    $ ls -l <userhome>/.conan2/p/meta98daf335d1d77/d/metadata/logs
    # Assuming we had a "file.log" together with the conanfile.py
    src.log file.log

In the same way we can have access to the package metadata, by specifying the ``package_id``:

.. code-block:: bash

    # To obtain the recipe metadata
    $ conan cache path meta/0.1:da39a3ee5e6b4b0d3255bfef95601890afd80709 --folder=metadata
    <userhome>.conan2/p/b/metaf3993f7804ad7/d/metadata
    $ ls <userhome>/.conan2/p/b/metaf3993f7804ad7/d/metadata/logs
    mylogs.txt


Generating metadata from hooks
------------------------------

In the case above we modified the recipe to explicitly store or copy the metadata we wanted. If this task is orthogonal to all recipes that we are managing, it is possible to implement it in a **hook**, instead of modifying the recipe.

An equivalent implementation of the above in a hook would be:

.. code-block:: python

    import os
    from conan.tools.files import copy

    def post_export(conanfile):
        # To copy the logs that were original in the source repo together with 
        # the conanfile.py, as RECIPE metadata
        copy(conanfile, "*.log", src=conanfile.recipe_folder,
             dst=os.path.join(conanfile.recipe_metadata_folder, "logs"))

    def post_source(conanfile):
        # to copy the files generated during the source() execution
        # as RECIPE metadata
        copy(conanfile, "*", src=os.path.join(conanfile.source_folder, "logs"),
             dst=os.path.join(conanfile.recipe_metadata_folder, "logs"))

    def post_build(conanfile):
        # to copy the files generated during the build() execution
        # This is PACKAGE metatada
        copy(conanfile, "*", src=os.path.join(conanfile.build_folder, "logs"),
             dst=os.path.join(conanfile.pkg_metadata_folder, "logs"))


If we put this hook (or install it with ``conan config install``) in the cache, the recipe could be simplified to:
      
.. code-block:: python

    from conan import ConanFile
    from conan.tools.files import save

    class Pkg(ConanFile):
        name = "meta"
        version = "0.1"

        def source(self):
            save(self, "logs/src.log", "srclog!!")

        def build(self):
            save(self, "logs/mylogs.txt", "some logs!!!")


And after a ``conan create`` the same recipe and package metadata would be created.


Upload metadata
---------------

The metadata files will be uploaded automatically when ``conan upload`` is executed. When a recipe or a package is uploaded to a remote, it will upload all metadata by default.

The ``conan upload`` command is efficient, and it avoids re-uploading artifacts if they are already in the server. That means that if new metadata is added to a recipe or a package, unless the ``--metadata`` argument is provided, the metadata will not be uploaded:

.. code-block:: bash

    # Upload all not existing in the server,
    # with all the metadata
    $ conan upload "*" -r=remote -c
    # Upload only the logs metadata of the zlib/1.2.13 binaries
    # This will upload the logs even if zlib/1.2.13 is already in the server
    $ conan upload zlib/1.2.13:* -r=remote -c --metadata="logs/*"
    # Multiple patterns are allowed:
    $ conan upload "*" -r=remote -c --metadata="logs/*" --metadata="tests/*"


AFter the upload, if you can inspect in the server side, you should be able to see the "metadata" folders under recipe revisions and package revisions, containing the uploaded files.

.. note::

    Conan does not do any compression or decompression of the metadata files. If there are a lot of metadata files, consider zipping them yourself, otherwise the upload of those many files can take a lot of time. If you need to handle different types of metadata (logs, tests, reports), zipping the files under each category might be better to be able to filter with the ``--metadata=xxx`` argument.


Adding metadata to existing recipes and binaries
------------------------------------------------

It is possible to add new metadata to recipes and packages even after the package has been created, and also uploaded. For example, if we have a package that has been created, installed or downloaded, we can put new metadata files in the metadata folders directly.

If we want to add metadata to a recipe:


.. code-block:: bash

    # To obtain the recipe metadata folder
    # (it defaults to the latest revision, use meta/0.1#revision if want another one)
    $ conan cache path meta/0.1 --folder=metadata
    <userhome>/.conan2/p/meta98daf335d1d77/d/metadata
    # copy my "logs" folder in my cwd to the recipe metadata folder
    $ cp -R logs <userhome>/.conan2/p/meta98daf335d1d77/d/metadata
    # Now upload the metadata
    $ conan upload meta/0.1 -r=remote -c --metadata="*"


Likewise we can do the same for the package binary:

.. code-block:: bash

    # To obtain the recipe metadata folder
    # (it defaults to the latest revision, use meta/0.1#revision if want another one)
    $  $ conan cache path meta/0.1:da39a3ee5e6b4b0d3255bfef95601890afd80709 --folder=metadata
    <userhome>/.conan2/p/metaf3993f7804ad7/d/metadata
    # copy my "logs" folder in my cwd to the package metadata folder
    $ cp -R logs <userhome>/.conan2/p/metaf3993f7804ad7/d/metadata
    # Now upload the metadata
    $ conan upload "meta/0.1:*"" -r=remote -c --metadata="*"


Downloading metadata
--------------------

Metadata is not downloaded by default, and it is not downloaded in normal ``install`` operations, when dependencies are downlaoded and installed for usage.

Metadata can be retrieved explicitly by the ``conan download`` command:

.. code-block:: bash

    # download all the metadata from that server
    $ conan download zlib/1.2.13:* --metadata="*" -r=remote
    # download the source code (recipe) metadata of all versions of zlib
    $ conan download zlib/* --metadata="code/*"  -r=remote


If we want to download the metadata for a whole dependency graph, it is necessary to use "package-lists":

.. code-block:: bash

    $ conan install . --format=json -r=remote > graph.json
    $ conan list --graph=graph.json --format=json > pkglist.json
    # the list will contain the "remote" origin of downloaded packages
    $ conan download --list=pkglist.json --metadata="*" -r=remote


Note that the "package-list" will only contain associated to the "remote" origin the packages that were downloaded. If they were previously in the cache, then, they will not be listed under the "remote" origin and the metadata will not be downloaded.


Removing metadata
-----------------

At the moment it is not possible to remove metadata from the server side using Conan, as the metadata are "additive", it is possible to add new data, but not to remove it (otherwise it would not be possible to add new metadata without downloading first all the previous metadata, and that can be quite inefficient and more error prone, specially sensitive to possible race conditions).

The recommendation to remove metatada from the server side would be to use the tools, web interface or APIs that the server might provide.


.. note::

    **Best practices**

    - If you are constantly downloading metadata in many of your ``install`` operations, that might indicate an abuse of the system. Metadata retrieval should be way less common than ``install`` operations.
    - Package usage shouldn't rely on metadata, if normal consumption of a package makes the metadata mandatory, then this metadata should be part of the package instead.
    - If there are many small files, it might be necessary to zip those files to avoid excessive upload and download time.
    - As metadata will not be downloaded by default, it will not be promoted by default in ``conan download`` + ``conan upload`` operations. The recommended way to run a server-server promotion (copy) is using the server tools, and guaranteeing that the metadata folders are copied too.
    - This is an **experimental** feature. We are looking forward to hearing your feedback, use cases and needs, to keep improving this feature. Please report it in `Github issues<https://github.com/conan-io/conan/issues>`_ .


.. seealso::

    - There is an :ref:`example of storing the "test_package" folder as metadata<examples_extensions_metadata_test_package>` and how to recover and use it.
