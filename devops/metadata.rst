.. _devops_metadata:

Managing package metadata files
===============================

.. include:: ../common/experimental_warning.inc


A Conan package is typically composed by several C and C++ artifacts, headers, compiled libraries and executables. But there are other files that might not be necessary for the normal consumption of such a package, but which could be very important for compliance, technical or business reasons, for example:

- Full build logs
- The tests executables
- The tests results from running the test suite
- Debugging artifacts like heavy .pdb files
- Coverage, sanitizers, or other source or binary analysis tools results
- Context and metadata about the build, exact machine, environment, author, CI data
- Other compliance and security related files


There are several important reasons to store and track these files like regulations, compliance, security, reproducibility and traceability.
The problem with these files is that they can be large/heavy, if we store them inside the package (just copying the artifacts in the ``package()`` method), this will make the packages much larger, and it will affect the speed of downloading, unzipping and using packages in general. And this typically happens a lot of times, both in developer machines but also in CI, and it can have an impact on the developer experience and infrastructure costs. Furthermore, packages are immutable, that is, once a package has been created, it shouldn't be modified. This might be a problem if we want to add extra metadata files after the package has been created, or even after the package has been uploaded.


The **metadata files** feature allows to create, upload, append and store metadata associated to packages in an integrated and unified way, while avoiding the impact on developers and CI speed and costs, because metadata files are not downloaded and unzipped by default when packages are used.


It is important to highlight that there are two types of metadata:

- Recipe metadata, associated to the ``conanfile.py`` recipe, the metadata should be common to all binaries created from this recipe (package name, version and recipe revision). This metadata will probably be less common, but for example results of some scanning of the source code, that would be common for all configurations and builds, can be recipe metadata.
- Package binary metadata, associated to the package binary for a given specific configuration and represented by a ``package_id``. Build logs, tests reports, etc, that are specific to a binary configuration will be package metadata.


Creating metadata in recipes
----------------------------
Recipes can directly define metadata in their methods. A common use case would be to store logs.
Using the ``self.recipe_metadata_folder`` and ``self.package_metadata_folder``, the recipe can store files
in those locations.

.. code-block:: python

   import os
   from conan import ConanFile
   from conan.tools.files import save, copy

   class Pkg(ConanFile):
      name = "pkg"
      version = "0.1"

      def layout(self):
         # Or something else, like the "cmake_layout(self)" built-in layout
         self.folders.build = "mybuild"
         self.folders.generators = "mybuild/generators"

      def export(self):
         # logs that might be generated in the recipe folder at "export" time.
         # these would be associated with the recipe repo and original source of the recipe repo
         copy(self, "*.log", src=self.recipe_folder,
              dst=os.path.join(self.recipe_metadata_folder, "logs"))

      def source(self):
         # logs originated in the source() step, for example downloading files, patches or other stuff
         save(self, os.path.join(self.recipe_metadata_folder, "logs", "src.log"), "srclog!!")

      def build(self):
         # logs originated at build() step, the most common ones
         save(self, "mylogs.txt", "some logs!!!")
         copy(self, "mylogs.txt", src=self.build_folder,
              dst=os.path.join(self.package_metadata_folder, "logs"))


Note that "recipe" methods (those that are common for all binaries, like ``export()`` and ``source()``) should use
``self.recipe_metadata_folder``, while "package" specific methods (``build()``, ``package()``) should use the
``self.package_metadata_folder``.

Doing a ``conan create`` over this recipe, will create "metadata" folders in the Conan cache. We can have a look at those folders with:

.. code-block:: bash

   $ conan create .
   $ conan cache path pkg/0.1 --folder=metadata
   # folder containing the recipe metadata
   $ conan cache path pkg/0.1:package_id --folder=metadata
   # folder containing the specific "package_id" binary metadata


It is also possible to use the "local flow" commands and get local "metadata" folders. If we want to do this, it is very recommended
to use a ``layout()`` method like above to avoid cluttering the current folder. Then the local commands will allow to test and debug the functionality:

.. code-block:: bash

   $ conan source .
   # check local metadata/logs/src.log file
   $ conan build .
   # check local mybuild/metadata/logs/mylogs.txt file


**NOTE**: This metadata is not valid for the ``conan export-pkg`` flow. If you want to use the ``export-pkg`` flow you might want to check the
"Adding metadata" section below.


Creating metadata with hooks
----------------------------
If there is some common metadata accross recipes, it is possible to capture it without modifying the recipes, using hooks.
Let's say that we have a simpler recipe:

.. code-block:: python

   import os
   from conan import ConanFile
   from conan.tools.files import save, copy

   class Pkg(ConanFile):
      name = "pkg"
      version = "0.1"
      no_copy_source = True

      def layout(self):
         self.folders.build = "mybuild"
         self.folders.generators = "mybuild/generators"

      def source(self):
         save(self, "logs/src.log", "srclog!!")

      def build(self):
         save(self, "logs/mylogs.txt", "some logs!!!")

As we can see, this is not using the metadata folders at all.
Let's define now the following hooks:

.. code-block:: python

   import os
   from conan.tools.files import copy

   def post_export(conanfile):
         conanfile.output.info("post_export")
         copy(conanfile, "*.log", src=conanfile.recipe_folder,
            dst=os.path.join(conanfile.recipe_metadata_folder, "logs"))

   def post_source(conanfile):
         conanfile.output.info("post_source")
         copy(conanfile, "*", src=os.path.join(conanfile.source_folder, "logs"),
            dst=os.path.join(conanfile.recipe_metadata_folder, "logs"))

   def post_build(conanfile):
         conanfile.output.info("post_build")
         copy(conanfile, "*", src=os.path.join(conanfile.build_folder, "logs"),
            dst=os.path.join(conanfile.package_metadata_folder, "logs"))


The usage of these hooks will have a very similar effect to the in-recipe approach: the metadata files
will be created in the cache when ``conan create`` executes, and also locally for the ``conan source`` and ``conan build``
local flow.


Adding metadata with commands
-----------------------------

Metadata files can be added or modified after the package has been created. To achieve this, using the ``conan cache path``
command will return the folders to do that operation, so copying, creating or modifying files in that location will achieve this.

.. code-block:: bash

   $ conan create . --name=pkg --version=0.1
   $ conan cache path pkg/0.1 --folder=metadata
   # folder to put the metadata, initially empty if we didn't use hooks
   # and the recipe didn't store any metadata. We can copy and put files
   # in the folder
   $ conan cache path pkg/0.1:package_id --folder=metadata
   # same as above, for the package metadata, we can copy and put files in
   # the returned folder


This metadata is added locally, in the Conan cache. If you want to update the server metadata, uploading it from the cache is necessary.


Uploading metadata
------------------

So far the metadata has been created locally, stored in the Conan cache. Uploading the metadata to the server is integrated with
the existing ``conan upload`` command:

.. code-block:: bash

   $ conan upload "*" -c -r=default
   # Uploads recipes, packages and metadata to the "default" remote
   ...
   pkg/0.1: Recipe metadata: 1 files
   pkg/0.1:da39a3ee5e6b4b0d3255bfef95601890afd80709: Package metadata: 1 files


By default, ``conan upload`` will upload recipes and packages metadata when a recipe or a package is uploaded to the server.
But there are some situations that Conan will completely avoid this upload, if it detects that the revisions do already exist
in the server, it will not upload the recipes or the packages.
If the metadata has been locally modified or added new files, we can force the upload explicitly with:

.. code-block:: bash

   # We added some metadata to the packages in the cache
   # But those packages already exist in the server
   $ conan upload "*" -c -r=default --metadata="*"
   ...
   pkg/0.1: Recipe metadata: 1 files
   pkg/0.1:da39a3ee5e6b4b0d3255bfef95601890afd80709: Package metadata: 1 files

The ``--metadata`` argument allows to specify the metadata files that we are uploading. If we structure them in folders,
we could specify ``--metadata="logs*"`` to upload only the logs metadata, but not other possible ones like ``test`` metadata.

.. code-block:: bash

   # Upload only the logs metadata of the zlib/1.2.13 binaries
   # This will upload the logs even if zlib/1.2.13 is already in the server
   $ conan upload "zlib/1.2.13:*" -r=remote -c --metadata="logs/*"
   # Multiple patterns are allowed:
   $ conan upload "*" -r=remote -c --metadata="logs/*" --metadata="tests/*"

Sometimes it might be useful to upload packages without uploading the metadata, even if the metadata cache folders contain files.
To ignore uploading the metadata, use an empty argument as metadata pattern:

.. code-block:: bash

   # Upload only the packages, not the metadata
   $ conan upload "*" -r=remote -c --metadata=""

The case of mixing ``--metadata=""`` with ``--metadata="*"`` is not allowed, and it will raise an error.

.. code-block:: bash

   # Invalid command, it will raise an error
   $ conan upload "*" -r=remote -c --metadata="" --metadata="logs/*"
   ERROR: Empty string and patterns can not be mixed for metadata.


Downloading metadata
--------------------

As described above, metadata is not downloaded by default. When packages are downloaded with a ``conan install`` or ``conan create``
fetching dependencies from the servers, the metadata from those servers will not be downloaded.

The way to recover the metadata from the server is to explicitly specify it with the ``conan download`` command:

.. code-block:: bash

   # Get the metadata of the "pkg/0.1" package
   $ conan download pkg/0.1 -r=default --metadata="*"
   ...
   $ conan cache path pkg/0.1 --folder=metadata
   # Inspect the recipe metadata in the returned folder
   $ conan cache path pkg/0.1:package_id --folder=metadata
   # Inspect the package metadata for binary "package_id"


The retrieval of the metadata is done with ``download`` per-package. If we want to download the metadata for a whole dependency graph, it is necessary to use "package-lists":

.. code-block:: bash

    $ conan install . --format=json -r=remote > graph.json
    $ conan list --graph=graph.json --format=json > pkglist.json
    # the list will contain the "remote" origin of downloaded packages
    $ conan download --list=pkglist.json --metadata="*" -r=remote


Note that the "package-list" will only contain associated to the "remote" origin the packages that were downloaded. If they were previously in the cache, then, they will not be listed under the "remote" origin and the metadata will not be downloaded. If you want to collect the dependencies metadata, recall to download it when the package is installed from the server.
There are other possibilities, like a custom command that can automatically collect and download dependencies metadata from the servers.


Removing metadata
-----------------
At the moment it is not possible to remove metadata from the server side using Conan, as the metadata are "additive", it is possible to add new data, but not to remove it (otherwise it would not be possible to add new metadata without downloading first all the previous metadata, and that can be quite inefficient and more error prone, specially sensitive to possible race conditions).

The recommendation to remove metatada from the server side would be to use the tools, web interface or APIs that the server might provide.

.. note::

    **Best practices**

   - Metadata shouldn't be necessary for using packages. It should be possible to consume recipes and packages without downloading their
     metadata. If metadata is mandatory for a package to be used, then it is not metadata and should be packaged as headers and binaries.
   - Metadata reading access should not be a frequent operation, or something that developers have to do. Metadata read is intended for
     excepcional cases, when some build logs need to be recovered for compliance, or some test executables might be needed for debugging or
     re-checking a crash.
   - Conan does not do any compression or decompression of the metadata files. If there are a lot of metadata files, consider zipping them yourself, otherwise the upload of those many files can take a lot of time. If you need to handle different types of metadata (logs, tests, reports), zipping the files under each category might be better to be able to filter with the ``--metadata=xxx`` argument.


test_package as metadata
------------------------

This is an illustrative example of usage of metadata, storing the full ``test_package`` folder as
metadata to later recover it and execute it. Note that this is not necessarily intended for production.

Let's  start with a hook that automatically stores as **recipe metadata** the ``test_package`` folder

.. code-block:: python

   import os
   from conan.tools.files import copy

   def post_export(conanfile):
      conanfile.output.info("Storing test_package")
      folder = os.path.join(conanfile.recipe_folder, "test_package")
      copy(conanfile, "*", src=folder,
            dst=os.path.join(conanfile.recipe_metadata_folder, "test_package"))


Note that this hook doesn't take into account that ``test_package`` can be dirty with tons of temporary build
objects (it should be cleaned before being added to metadata), and it doesn't check that ``test_package`` might
not exist at all and crash.

When a package is created and uploaded, it will upload to the server the recipe metadata containing the ``test_package``:

.. code-block:: bash

   $ conan create ...
   $ conan upload "*" -c -r=default  # uploads metadata
   ...
   pkg/0.1: Recipe metadata: 1 files

Let's remove the local copy, and assume that the package is installed, but the metadata is not:

.. code-block:: bash

   $ conan remove "*" -c  # lets remove the local packages
   $ conan install --requires=pkg/0.1 -r=default  # this will not download metadata


If at this stage the installed package is failing in our application, we could recover the ``test_package``,
downloading it, and copying it to our current folder:

.. code-block:: bash

   $ conan download pkg/0.1 -r=default --metadata="test_package*"
   $ conan cache path pkg/0.1 --folder=metadata
   # copy the test_package folder from the cache, to the current folder
   # like `cp -R ...`

   # Execute the test_package
   $ conan test metadata/test_package pkg/0.1
   pkg/0.1 (test package): Running test()


.. seealso::

   - TODO: Examples how to collect the metadata of a complete dependency graph with some custom deployer or command


This is an **experimental** feature. We are looking forward to hearing your feedback, use cases and needs, to keep improving this feature. Please report it in `Github issues <https://github.com/conan-io/conan/issues>`_
