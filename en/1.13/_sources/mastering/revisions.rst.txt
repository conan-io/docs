Package Revisions
==================

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.


The goal of the `revisions feature` is to achieve package immutability, so nothing in a server is ever overwritten.

.. note::

    This is the first piece to achieve reproducibility: Recreate the exact dependency graph by using some
    mechanism like a ``graph lock`` file. For example, if we store a ``graph lock`` file for the different releases
    of our project, we can install the same dependencies just by using the graph lock.

    **IMPORTANT:** The reproducibility is in the Conan roadmap and currently under development.


How it works
------------

**In the client**

- When a **recipe** is exported, Conan calculates a unique ID (revision). For every change,
  a new recipe revision (RREV) will be calculated:

   - If Conan detects some control version system (Git or SVN) in the conanfile directory, the commit hash will be used as the RREV.
   - Otherwise, the checksum hash of the recipe manifest will be used as the RREV.

.. note::

   In future versions Conan will let the user choose to use the "recipe manifest" instead of the scm. For example,
   when you use a mono-repo with N recipes, it is more convenient to calculate each
   recipe revision based on its contents and not in the common github repository commit hash.
   (https://github.com/conan-io/conan/issues/4413)


- When a **package** is created (by running :ref:`conan create<conan_create>` or :ref:`conan export-pkg<conan_export-pkg>`)
  a new package revision (PREV) will be calculated always using the hash of the package contents.
  The packages and their revisions (PREVs) belongs to a concrete recipe revision (RREV).
  The same package ID (for example for Linux/GCC5/Debug), can have multiple revisions (PREVs) that belong
  to a concrete RREV.


If a client request a reference like `lib/1.0@conan/stable`, Conan will retrieve automatically the latest revision.
In the client cache there is **only one revision installed at the same time**.

The revisions can be pinned when you write a reference (in the recipe requires, or in a reference in a
conan install command…) but if you don’t specify a revision the server will retrieve the latest revision.

You can specify the references in the following formats:

+---------------------------------------------+----------------------------------------------------------------+
| Reference                                   | Meaning                                                        |
+=============================================+================================================================+
| `lib/1.0@conan/stable`                      | Latest RREV for lib/1.0@conan/stable                           |
+---------------------------------------------+----------------------------------------------------------------+
| `lib/1.0@conan/stable#RREV`                 | Specific RREV for lib/1.0@conan/stable                         |
+---------------------------------------------+----------------------------------------------------------------+
| `lib/1.0@conan/stable#RREV:PACKAGE_ID`      | A binary package belonging to the specific RREV                |
+---------------------------------------------+----------------------------------------------------------------+
| `lib/1.0@conan/stable#RREV:PACKAGE_ID#PREV` | A binary package revision PREV belonging to the specific RREV  |
+---------------------------------------------+----------------------------------------------------------------+


**In the server**

By using a new folder layout and protocol it is able to store multiple revisions, both for recipes and binary
packages.


How to activate the revisions
-----------------------------

You have to explicitly activate the feature by:

 - Adding ``revisions_enabled=1`` in the ``[general]`` section of your `conan.conf` file.
 - Setting the ``CONAN_REVISIONS_ENABLED=1`` environment variable.


Take into account that it changes the default Conan behavior. e.g:

    - A client with revisions enabled will only find binary packages that belongs to the installed recipe revision.
      For example, If you create a recipe and run ``conan create . user/channel`` and then you modify the recipe and
      export it ``conan export . user/channel``, the binary package generated in the ``conan create`` command doesn't
      belong to the new exported recipe, so it won't be located unless the previous recipe is recovered.

    - If you generate and upload N binary packages for a recipe revision, if you upload the revision you need to
      generate and upload again the N binaries if you want them to be used with the new recipe.


Server support
--------------

   - ``conan_server`` >= 1.13.
   - ``Artifactory`` coming soon.
   - ``Bintray`` coming soon.
