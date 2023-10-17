.. _devops_metadata:

Managing package metadata files
===============================

.. include:: ../common/experimental_warning.inc

Conan packages store the library headers, libraries and executable binaries, licenses and sometimes other data files or build files that might be necessary to use those packages.

But there are many other files that are generated during the build, or that are relevant for the current package, that we want to manage and store them:

- Full build logs
- The tests executables
- The tests results
- Coverage, sanitizers, or other source or binary analysis tools results
- Context and metadata about the build, exact machine, environment, author, CI data
- Other compliance and security related files


There are several important reasons to store and track these files like regulations, compliance, security, reproducibility and traceability.
The problem with these files is that they can be large/heavy, if we store them inside the package (just copying the artifacts in the ``package()`` method), this will make the packages much larger, and it will affect the speed of downloading, unzipping and using packages in general. And this typically happens a lot of times, both in developer machines but also in CI, and it can have an impact on the developer experience and infrastructure costs. Furthermore, packages are immutable, that is, once a package has been created, it shouldn't be modified. This might be a problem if we want to add extra metadata files after the package has been created, or even after the package has been uploaded.


The **metadata files** feature allows to create, upload, append and store metadata associated to packages in an integrated and unified way, while avoiding the impact on developers and CI speed and costs, because metadata files are not downloaded and unzipped by default when packages are used.


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

   $ conan create . --name=pkg --version=0.1
   $ conan cache path pkg/0.1 --folder=metadata
   # folder containing the recipe metadata
   $ conan cache path pkg/0.1:package_id --folder=metadata
   # folder containing the specific "package_id" binary metadata


It is also possible to use the "local flow" commands and get local "metadata" folders. But if we want to do this, it is very recommended
to use a ``layout()`` method like this to avoid the excessive pollution of the current folder:

.. code-block:: python

   def layout(self):
      # Or something else, like the "cmake_layout(self)" built-in layout
      self.folders.build = "mybuild"
      self.folders.generators = "mybuild/generators"
   

And then the local commands will allow to test and debug the functionality:

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
we could specify ``--metadata=logs*`` to upload only the logs metadata, but not other possible ones like ``test`` metadata.


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


The retrieval of the metadata is done with ``download`` per-package, or for a list of packages (``conan download --list``), but it is not
possible to do it (in a built-in way, it is possible with extensions, like using a deployer or custom commands) for a full dependency graph.


.. note::

    **Best practices**

   - Metadata shouldn't be necessary for using packages. It should be possible to consume recipes and packages without downloading their
     metadata. If metadata is mandatory for a package to be used, then it is not metadata and should be packaged as headers and binaries.
   - Metadata reading access should not be a frequent operation, or something that developers have to do. Metadata read is intended for
     excepcional cases, when some build logs need to be recovered for compliance, or some test executables might be needed for debugging or
     re-checking a crash.
   - Metadata is not automatically zipped or unzipped. Storing many individual files can be inefficient for upload, download and storage,
     and it might be recommended to zip those metadata files. It is the user recipe or hook responsibility to do that if desired.


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
