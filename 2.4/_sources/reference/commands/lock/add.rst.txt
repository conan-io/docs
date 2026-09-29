conan lock add
==============

.. autocommand::
    :command: conan lock add -h


The ``conan lock add`` command is able to add a package version to an existing or new lockfile ``requires``, ``build_requires`` or ``python_requires``.

For example, the following is able to create a lockfile (by default, named ``conan.lock``):

.. code-block:: bash

  $ conan lock add --requires=pkg/1.1 --build-requires=tool/2.2 --python-requires=mypytool/3.3 
  Generated lockfile: ...conan.lock

  $cat conan.lock
  {
      "version": "0.5",
      "requires": [
          "pkg/1.1"
      ],
      "build_requires": [
          "tool/2.2"
      ],
      "python_requires": [
          "mypytool/3.3"
      ]
  }


The ``conan lock add`` command also allows to provide an existing lockfile as an input,
and it will add the arguments to the existing lockfile, maintaining the
package versions sorted:

.. code-block:: bash

  $ conan lock add --build-requires=tool/2.3 --lockfile=conan.lock
  Using lockfile: '.../conan.lock'
  Generated lockfile: .../conan.lock

  $ cat conan.lock
  {
      "version": "0.5",
      "requires": [
          "pkg/1.1"
      ],
      "build_requires": [
          "tool/2.3",
          "tool/2.2"
      ],
      "python_requires": [
          "mypytool/3.3"
      ]
  }


The ``conan lock add`` command does not perform any checking on the lockfile, the packages, the existence of packages,
the existence of package versions, or the existence of those packages in a given dependency graph, it is a basic manipulation of the json information.
When that lockfile is applied to resolve a dependency graph, it is possible that the added versions do not exist,
or do not resolve for the ``conanfile.py`` recipes defined version ranges.

Moreover, the list of versions is still sorted. Adding an older version like ``tool/2.1`` to the previous lockfile
won't make that version being used automatically if the recipes contain the version range ``tool/[>=2.0 <3]``, because
the ``tool/2.2`` version is listed there and the range will resolve to it, not to the older ``tool/2.1``.

Note that a lockfile created with ``conan lock add`` can be incomplete and not contain all necessary locked versions
that a full dependency graph would need. For those cases, recall that the ``--lockfile-partial`` argument can be applied. 
Note also that if a ``conan.lock`` file exist in the current folder, Conan commands like ``conan install`` will automatically use it.
Please have a look to the :ref:`lockfiles tutorial<tutorial_versioning_lockfiles>`.

If explicitly adding revisions, please recall that the revisions are timestamp sorted. If more than one revision exists in the lockfile,
it is mandatory to provide the timestamps of those revisions, so the sorting makes sense, which can be done with:


.. code-block:: bash

  $ conan lock add --requires=pkg/1.1#revision%timestamp


.. warning::

  - It is forbidden to manually manipulate a Conan lockfile, changing the strict sorting of references, and that could result in
    any arbitrary undefined behavior.
  - Recall that it is not possible to ``conan lock add`` a version range. The version might be not fully complete (like not providing
    the revision), but it must be an exact version.


.. note::

  **Best practices**

  This command will not be necessary in many situations. The existing ``conan install``, ``conan create``, ``conan lock``, ``conan export``,
  ``conan graph`` commands can directly update or produce new lockfiles with the new information of the packages they are creating, and 
  those new or updated lockfiles can be used to continue with the processing.
