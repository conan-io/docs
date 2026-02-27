.. _reference_commands_pkglist:

conan pkglist
=============

.. include:: ../../common/experimental_warning.inc


Perform different operations over package lists:

- Merge multiple package lists (deep merge) into a single one: ``conan pkglist merge``
- Find in which remotes packages from the cache can be found: ``conan pkglist find-remote``


conan pkglist merge
--------------------

.. autocommand::
    :command: conan pkglist merge -h

The ``conan pkglist merge`` command can merge multiple package lists into a single one:

.. code-block:: bash

    $ conan pkglist merge --list=list1.json --list=list2.json --format=json > result.json


The merge will be a deep merge, different versions can be added, and within versions multiple
revisions can be added, and for every recipe revision multiple package_ids can be also accumulated.


conan pkglist find-remote
-------------------------

.. autocommand::
    :command: conan pkglist find-remote -h


The ``conan pkglist find-remote`` command will take a package list of packages in the cache 
(key ``"Local Cache"``) and look for them in the defined remotes. For every exact occurence in a remote
matching the recipe, version, recipe-revision, etc, an entry in the resulting "package lists"
will be added for that specific remote.
