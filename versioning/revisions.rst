.. _package_revisions:

Package Revisions
=================

The goal of the revisions feature is to achieve package immutability, the packages in a server are never overwritten.

.. note::

    Revisions achieve immutability. For achieving reproducible builds and reproducible dependencies, **lockfiles**
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

If a client requests a reference like ``lib/1.0@conan/stable``, Conan will automatically retrieve the latest revision in case
the local cache doesn't contain any revisions already. If a client needs to update an existing revision, they have to ask for updates explicitly
with ``-u, --update`` argument to :command:`conan install` command. In the client cache there is
**only one revision installed simultaneously**.

The revisions can be pinned when you write a reference (in the recipe requires, a reference in a
:command:`conan install` command,…) but if you don’t specify a revision, the server will retrieve the latest revision.

You can specify the references in the following formats:

+-----------------------------------------------+--------------------------------------------------------------------+
| Reference                                     | Meaning                                                            |
+===============================================+====================================================================+
| ``lib/1.0@conan/stable``                      | Latest RREV for ``lib/1.0@conan/stable``                           |
+-----------------------------------------------+--------------------------------------------------------------------+
| ``lib/1.0@conan/stable#RREV``                 | Specific RREV for ``lib/1.0@conan/stable``                         |
+-----------------------------------------------+--------------------------------------------------------------------+
| ``lib/1.0@conan/stable#RREV:PACKAGE_ID``      | A binary package belonging to the specific RREV                    |
+-----------------------------------------------+--------------------------------------------------------------------+
| ``lib/1.0@conan/stable#RREV:PACKAGE_ID#PREV`` | A binary package revision PREV belonging to the specific RREV      |
+-----------------------------------------------+--------------------------------------------------------------------+

**In the server**

By using a new folder layout and protocol it is able to store multiple revisions, both for recipes and binary packages.

How to activate the revisions
-----------------------------

You have to explicitly activate the feature by either:

 - Adding ``revisions_enabled=1`` in the ``[general]`` section of your *conan.conf* file (preferred)
 - Setting the ``CONAN_REVISIONS_ENABLED=1`` environment variable.

Take into account that it changes the default Conan behavior. e.g:

    - A client with revisions enabled will only find binary packages that belong to the installed recipe revision.
      For example, If you create a recipe and run :command:`conan create . user/channel` and then you modify the recipe and
      export it (:command:`conan export . user/channel`), the binary package generated in the :command:`conan create` command
      doesn't belong to the new exported recipe. So it won't be located unless the previous recipe is recovered.

    - If you generate and upload N binary packages for a recipe with a given revision, then if you modify the recipe, and thus the recipe
      revision, you need to build and upload N new binaries matching that new recipe revision.


GIT and Line Endings on Windows
-------------------------------

There is one very common problem that users encounter after enabling revisions which all users should be aware of. 
This issue occurs when all of the following conditions are true:

 - Using GIT to retrieve sources with default settings
 - Using Continuous Integration services
 - Building on multiple platforms
 - One of the target platforms is Windows

When cloning a repository on a Windows machine, the GIT client will replace all of the line endings on all of the 
files with @CRLF character. The default line ending outside of Windows is @LF.  

**Problem**

As a result, when Conan does export of an otherwise identical GIT repository/commit on a Windows and a Non-Windows build machine,
the Conan revisions will be different between the two. This has a very unfortunate consequence when two such packages are then 
uploaded to a Conan repository (as is very common in continuous integration workflows). The net consequence of two such uploads, 
is that the next time `conan install` is run for that package, the "latest" revision will only have the binaries for one platform
or the other (whichever CI job finished and uploaded last). If `conan install` is run for the other platform, it will receive
the following error:
    
    ERROR: Missing prebuilt package for <package_ref>

**Workaround**

The problem is unfortunately something that is external to Conan, so we cannot provide a general-purpose fix. We
can only explain the situation as we have done here and suggest a few ways to address the problem.  The most 
straightforward and reasonable solution is to prevent GIT for windows from replacing the line-endings on the Windows 
build machines. This avoids the problem completely by ensuring that the Conan Revisions are the same on Windows and 
Non-Windows machines. There are several ways to achieve the goal. 

For users who can add files at the repository level, a file named `.gitconfig` can be added which contains the following:

        [auto]
          crlf = false

This will solve the problem on the single repository. 

Alternatively, for users who can add steps to the Windows build server environment setup, the following commands 
can be run before the clone of the GIT repository:

        git config --global core.autocrlf false   
        git config --global core.eol lf  

This will solve the problem for all Conan packages which are built on servers that run these commands. 

There are other ways to address the problem as well, but these are the most general options we can suggest. 

          
Server support
--------------

   - ``conan_server`` >= 1.13.
   - ``Artifactory`` >= 6.9.
   - ``Bintray``.
