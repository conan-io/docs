conan lock update
=================

.. autocommand::
    :command: conan lock update -h


The ``conan lock update`` command is able to update ``requires``, ``build_requires``, ``python_requires`` or ``config_requires`` items from an existing lockfile.

For example, if we have the following ``conan.lock``:

.. code-block:: bash

  $ cat conan.lock
  {
      "version": "0.5",
      "requires": [
          "math/1.0#85d927a4a067a531b1a9c7619522c015%1702683583.3411012",
          "engine/1.0#fd2b006646a54397c16a1478ac4111ac%1702683583.3544693"
      ],
      "build_requires": [
          "cmake/1.0#85d927a4a067a531b1a9c7619522c015%1702683583.3411012",
          "ninja/1.0#fd2b006646a54397c16a1478ac4111ac%1702683583.3544693"
      ],
      "python_requires": [
          "mytool/1.0#85d927a4a067a531b1a9c7619522c015%1702683583.3411012",
          "othertool/1.0#fd2b006646a54397c16a1478ac4111ac%1702683583.3544693"
      ]
  }
  


The ``conan lock update`` command:

.. code-block:: bash

  $ conan lock update --requires=math/1.1 --build-requires=cmake/1.1

Will result in the following ``conan.lock``:

.. code-block:: bash

  $ cat conan.lock
  {
      "version": "0.5",
      "requires": [
          "math/1.1",
          "engine/1.0#fd2b006646a54397c16a1478ac4111ac%1702683583.3544693"
      ],
      "build_requires": [
          "cmake/1.1",
          "ninja/1.0#fd2b006646a54397c16a1478ac4111ac%1702683583.3544693"
      ],
      "python_requires": [
          "mytool/1.0#85d927a4a067a531b1a9c7619522c015%1702683583.3411012",
          "othertool/1.0#fd2b006646a54397c16a1478ac4111ac%1702683583.3544693"
      ]
  }


The command will replace existing locked references that matches the same package name with the provided argument values.
If the provided references does not exist in the lockfile, they will be added (same as ``conan lock add`` command).

This command is similar to do a ``conan lock remove`` followed by a ``conan lock add`` command.
