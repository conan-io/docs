(Experimental) conan lock upgrade
=================================

.. autocommand::
    :command: conan lock upgrade -h


The ``conan lock upgrade`` command is able to upgrade ``requires``, ``build_requires``, ``python_requires`` or ``config_requires`` items from an existing lockfile.

For example, if we have the following ``conan.lock``:

.. code-block:: bash

  $ cat conan.lock
  {
      "version": "0.5",
      "requires": [
          "libb/1.0#7e88fd43dc3c8171b6f38f8d1b139641%1740472377.657901",
          "liba/1.0#b0546195fd5bf19a0e6742510fff8855%1740472377.653885"
      ],
      "build_requires": [
          "libc/1.0#dc77a17d3e566df710241e3b1f380b8c%1740472377.661421"
      ],
      "python_requires": [
          "libd/1.0#9f077ce58183dad0f59e36d6bd73ebe1%1740472377.6647942"
      ],
      "config_requires": []
  }
  

And these packages available in the cache:

.. code-block:: bash

  $ conan list "*" --format=compact

  Found 9 pkg/version recipes matching * in local cache
  Local Cache
    liba/1.0
    liba/1.9
    libb/1.0
    libb/1.1
    libb/1.2
    libc/1.0
    libc/1.1
    libd/1.0
    libd/1.1


Using the ``conan lock upgrade`` command with the appropiate ``--update-**`` arguments:

.. code-block:: bash

  $ conan lock upgrade --requires=liba/[>=1.0 <2] --tool-requires=libc/[<2.0] --update-requires=liba/[*] --update-build-requires=libc/1.0

Will result in the following ``conan.lock``:

.. code-block:: bash

  $ cat conan.lock
  {
      "version": "0.5",
      "requires": [
          "libb/1.0#7e88fd43dc3c8171b6f38f8d1b139641%1740484122.087734",
          "liba/1.9#b0546195fd5bf19a0e6742510fff8855%1740484122.108484"
      ],
      "build_requires": [
          "libc/1.1#dc77a17d3e566df710241e3b1f380b8c%1740484122.119971"
      ],
      "python_requires": [
          "libd/1.0#9f077ce58183dad0f59e36d6bd73ebe1%1740484122.095434"
      ],
      "config_requires": []
  }


The command will upgrade existing locked references that match the same
package name with versions that match the version ranges provided by required
arguments.


The ``conan lock upgrade`` command may also be able to upgrade ``requires``, ``build_requires``, ``python_requires`` from a conanfile.
This use case enhances the functionality of version ranges.

Let's consider the following conanfile:

.. code-block:: python

  from conan import ConanFile
  class HelloConan(ConanFile):
      requires = ("liba/[>=1.0 <2]", "libb/[<1.2]")
      tool_requires = "libc/[>=1.0]"
      python_requires = "libd/[>=1.0 <1.2]"

Starting from the same environment and ``conan.lock`` file from previous example.

Running the following command

.. code-block:: bash

  $ conan lock upgrade . --update-requires=liba/1.0 --update-requires=libb/[*] --update-build-requires=libc/[*] --update-python-requires=libd/1.0"

Will result in the following ``conan.lock``:

.. code-block:: bash

  {
      "version": "0.5",
      "requires": [
          "libb/1.1#7e88fd43dc3c8171b6f38f8d1b139641%1740488410.3630772",
          "liba/1.9#b0546195fd5bf19a0e6742510fff8855%1740488410.356828"
      ],
      "build_requires": [
          "libc/1.1#dc77a17d3e566df710241e3b1f380b8c%1740488410.371875"
      ],
      "python_requires": [
          "libd/1.1#9f077ce58183dad0f59e36d6bd73ebe1%1740488410.376066"
      ],
      "config_requires": []
  }


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
