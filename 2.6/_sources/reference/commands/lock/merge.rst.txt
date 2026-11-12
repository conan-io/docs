conan lock merge
================

.. autocommand::
    :command: conan lock merge -h


The ``conan lock merge`` command takes 2 or more lockfiles and aggregate them, producing one final lockfile.
For example, if we have 2 lockfiles ``lock1.lock`` and ``lock2.lock``, we can merge both in a final ``conan.lock`` one:

.. code-block:: bash

  # we have 2 lockfiles lock1.lock and lock2.lock
  $ conan lock add --requires=pkg/1.1 --lockfile-out=lock1.lock
  $ cat lock1.lock
  {
      "version": "0.5",
      "requires": [
          "pkg/1.1",
      ],
      "build_requires": [],
      "python_requires": []
  }

  $ conan lock add --requires=other/2.1 --build-requires=tool/3.2 --lockfile-out=lock2.lock
  $ cat lock2.lock
  {
      "version": "0.5",
      "requires": [
          "other/2.1"
      ],
      "build_requires": [
          "tool/3.2"
      ],
      "python_requires": []
  }

  # we can merge both
  $ conan lock merge --lockfile=lock1.lock --lockfile=lock2.lock
  $ cat conan.lock
  {
      "version": "0.5",
      "requires": [
          "pkg/1.1",
          "other/2.1"
      ],
      "build_requires": [
          "tool/3.2"
      ],
      "python_requires": []
  }

Similar to the ``conan lock add`` command, the ``conan lock merge``:

- Does keep strict sorting of the lists of versions
- It does not perform any kind of validation if the packages or versions exist or not, or if they belong to a given dependency graph
- It is a basic processing of the json files, aggregating them.
- It doesn't guarantee that the lockfile will be complete, might require ``--lockfile-partial`` if not
- Recipe revisions, if defined, must contain the timestamp to be sorted correctly.


.. warning::

  - It is forbidden to manually manipulate a Conan lockfile, changing the strict sorting of references, and that could result in
    any arbitrary undefined behavior.
  - Recall that it is not possible to ``conan lock add`` a version range. The version might be not fully complete (like not providing
    the revision), but it must be an exact version.

.. seealso::

  To better understand ``conan lock merge``, it is recommended to first understand lockfiles in general,
  visit the :ref:`lockfiles tutorial<tutorial_versioning_lockfiles>` for a practical introduction to lockfiles.


This ``conan lock merge`` command can be useful to consolidate in a single lockfile when for some reasons there are several lockfiles
that have diverged. A use case would be to create a multi-configuration lockfile that contains all necessary locked versions for
all OSs (Linux, Windows, etc), even if there are conditional dependencies in the graph for the different OSs. At some point when
testing a new dependency version, for example, ``pkg/3.4`` new version, when previously ``pkg/3.3`` was already in the graph, we
might want to have such a new lockfile cleaning the previous ``pkg/3.3``. If we apply the ``--lockfile-clean`` argument that will
remove the non-used versions in the lockfile, but that will also remove the OS-dependant dependencies. So something like this could be 
done: lets say that we have this lockfile (simplified, removed revisions for simplicity) as the result of testing a new ``pkgb/0.2`` version
for our main product ``app1/0.1``:

.. code-block:: json
  :caption: app.lock

  {
    "version": "0.5",
    "requires": [
        "pkgb/0.2",
        "pkgb/0.1",
        "pkgawin/0.1",
        "pkganix/0.1",
        "app1/0.1"
    ]
  }

The ``pkgawin`` and ``pkganix`` are dependencies that exist exclusively in Windows and Linux respectively. Everything looks good,
``pkgb/0.2`` new version works fine with our app, and we want to clean the unused things from the lockfile:

.. code-block:: bash

  $ conan lock create --requires=app1/0.1 --lockfile=app.lock --lockfile-out=win.lock -s os=Windows --lockfile-clean
  # Note how both pkgb/0.1 and pkganix are gone
  $ cat win.lock
  {
    "version": "0.5",
    "requires": [
        "pkgb/0.2",
        "pkgawin/0.1",
        "app1/0.1"
    ]
  }
  $ conan lock create --requires=app1/0.1 --lockfile=app.lock --lockfile-out=nix.lock -s os=Linux --lockfile-clean
  # Note how both pkgb/0.1 and pkgawin are gone
  $ cat win.lock
  {
    "version": "0.5",
    "requires": [
        "pkgb/0.2",
        "pkganix/0.1",
        "app1/0.1"
    ]
  }
    # Finally, merge the 2 clean lockfiles, for keeping just 1 for next iteration
  $ conan lock merge --lockfile=win.lock --lockfile=nix.lock --lockfile-out=final.lock
  $ cat final.lock
  {
    "version": "0.5",
    "requires": [
        "pkgb/0.2",
        "pkgawin/0.1",
        "pkganix/0.1",
        "app1/0.1"
    ]
  }
