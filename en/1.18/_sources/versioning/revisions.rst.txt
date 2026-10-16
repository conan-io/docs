.. _package_revisions:

Package Revisions
=================

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

The goal of the revisions feature is to achieve package immutability, the packages in a server are never overwritten.

.. note::

    Revisions achieve inmmutatibility. For achieving reproducible builds and reproducible dependencies, **lockfiles**
    are used. Lockfiles can capture an exact state of a dependency graph, down to exact versions and revisions, and use
    it later to force their usage, even if new versions or revisions were uploaded to the servers.

    Learn more about :ref:`lockfiles here.<versioning_lockfiles>`
    

How it works
------------

**In the client**

- When a **recipe** is exported, Conan calculates a unique ID (revision). For every change,
  a new recipe revision (RREV) will be calculated. By default it will use the checksum hash of the
  recipe manifest.

  Nevertheless, the recipe creator can explicitly declare the :ref:`revision mode<revision_mode_attribute>`,
  it can be either ``scm`` (uses version control system or raises) or ``hash`` (use manifest hash).

- When a **package** is created (by running :ref:`conan create<conan_create>` or :ref:`conan export-pkg<conan_export-pkg>`)
  a new package revision (PREV) will be calculated always using the hash of the package contents.
  The packages and their revisions (PREVs) belongs to a concrete recipe revision (RREV).
  The same package ID (for example for Linux/GCC5/Debug), can have multiple revisions (PREVs) that belong
  to a concrete RREV.

If a client requests a reference like ``lib/1.0@conan/stable``, Conan will automatically retrieve the latest revision.
In the client cache there is **only one revision installed simultaneously**.

The revisions can be pinned when you write a reference (in the recipe requires, or in a reference in a
:command:`conan install` command…) but if you don’t specify a revision, the server will retrieve the latest revision.

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

By using a new folder layout and protocol it is able to store multiple revisions, both for recipes and binary packages.

How to activate the revisions
-----------------------------

You have to explicitly activate the feature by:

 - Adding ``revisions_enabled=1`` in the ``[general]`` section of your *conan.conf* file.
 - Setting the ``CONAN_REVISIONS_ENABLED=1`` environment variable.

Take into account that it changes the default Conan behavior. e.g:

    - A client with revisions enabled will only find binary packages that belong to the installed recipe revision.
      For example, If you create a recipe and run :command:`conan create . user/channel` and then you modify the recipe and
      export it (:command:`conan export . user/channel`), the binary package generated in the :command:`conan create` command
      doesn't belong to the new exported recipe. So it won't be located unless the previous recipe is recovered.

    - If you generate and upload N binary packages for a recipe with a given revision, then if you modify the recipe, and thus the recipe
      revision, you need to build and upload N new binaries matching that new recipe revision.

Server support
--------------

   - ``conan_server`` >= 1.13.
   - ``Artifactory`` >= 6.9.
   - ``Bintray``.
