conan lock upgrade
==================

.. include:: ../../../common/experimental_warning.inc

.. autocommand::
    :command: conan lock upgrade -h


The ``conan lock upgrade`` command is able to upgrade ``requires``, ``build_requires``, ``python_requires`` or ``config_requires`` items from an existing lockfile.

For example, if we have the following ``conan.lock``:

.. code-block:: bash

  $ cat conan.lock
  {
      "version": "0.5",
      "requires": [
          "package/1.0#b0546195fd5bf19a0e6742510fff8855%1740472377.653885"
      ],
      "build_requires": [
          "cmake/1.0#85d927a4a067a531b1a9c7619522c015%1702683583.3411012",
      ]
  }
  

And these packages available in the cache:

.. code-block:: bash

  $ conan list "*" --format=compact

  Found 9 pkg/version recipes matching * in local cache
  Local Cache
    package/1.0
    package/1.9
    cmake/3.29.0
    cmake/3.30.5


Using the ``conan lock upgrade`` command with the appropiate ``--update-**`` arguments:

.. code-block:: bash

  $ conan lock upgrade --requires=package/[>=1.0 <2] --update-requires=package/[*]

Will result in the following ``conan.lock``:

.. code-block:: bash

  $ cat conan.lock
  {
      "version": "0.5",
      "requires": [
          "package/1.9#b0546195fd5bf19a0e6742510fff8855%1740484122.108484"
      ],
      "build_requires": [
          "cmake/3.29.0#85d927a4a067a531b1a9c7619522c015%1702683583.3411012",
      ]
  }

The same can be done for ``build_requires`` and ``python_requires``.


The command will upgrade existing locked references that match the same
package name with versions that match the version ranges provided by required
arguments.


The ``conan lock upgrade`` command may also be able to upgrade ``requires``, ``build_requires``, ``python_requires`` from a conanfile.
This use case enhances the functionality of version ranges.

Let's consider the following conanfile:

.. code-block:: python

  from conan import ConanFile
  class HelloConan(ConanFile):
      requires = ("math/[>=1.0 <2]")
      tool_requires = "ninja/[>=1.0]"

.. code-block:: bash

  $ conan list "*" --format=compact

  Found 9 pkg/version recipes matching * in local cache
  Local Cache
    math/1.0
    math/2.0
    ninja/1.0
    ninja/1.1

Starting from the same environment and ``conan.lock`` file from previous example.
Running the following command:

.. code-block:: bash

  $ conan lock upgrade . --update-requires=math/1.0 --update-build-requires=ninja/[*]

Will result in the following ``conan.lock``:

.. code-block:: bash

  {
      "version": "0.5",
      "requires": [
          "math/1.0#b0546195fd5bf19a0e6742510fff8855%1740488410.356828"
      ],
      "build_requires": [
          "ninja/1.1#dc77a17d3e566df710241e3b1f380b8c%1740488410.371875"
      ]
  }

``math`` package have not been updated due to the version range specified in
the conanfile, but ``ninja`` has been updated to the latest version available
in the cache.

If a dependency is updated and in the new revision, a transitive dependency is
added, the ``lock upgrade`` command will reflect the new transitive dependency
in the lockfile. E.g.

- ``liba/1.0`` depends on ``libb/1.0``
- ``libb/1.0`` depends on ``libc/1.0`` 

If ``libb/2.0`` depends also on ``libd/1.0``:

.. code-block:: bash

  $ conan lock upgrade --requires=libb/[>=2] --update-requires=libb/*

The resulting lockfile will contain both ``libc/1.0`` and ``libd/1.0``.

.. note::

  Updating transitive dependencies is not supported yet. This is an experimental feature and it may change in the future.
