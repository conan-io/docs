.. _reference_commands_lock_upgrade_config:

conan lock upgrade-config
=========================


.. include:: ../../../common/experimental_warning.inc

.. autocommand::
    :command: conan lock upgrade-config -h


The ``conan lock upgrade-config`` command is equivalent to the previous ``conan lock upgrade``, but tailored specifically
to upgrade the ``config-requires`` packages that can be installed with ``conan config install-pkg``.

The upgrade can be done over individual requirements passed on the command line:

.. code-block:: bash

  $ conan lock upgrade-config --requires=config/[*] --update-config-requires=config/*

Note that it is important to specify which packages are to be updated with ``--update-config-requires``, because
it is possible that the lockfile contains more than one configuration package.

Also note that the upgrade of the lockfile doesn't change yet or install the configuration.
Until a ``conan config install-pkg`` happens, the active and current configuration will not be updated.

It is also possible to use a ``conanconfig.yml`` file as an input to the command, by passing the path to
its containing folder:

.. code-block:: bash

  $ conan lock upgrade-config . --update-config-requires=config/1.0

.. important::

    The ``path`` argument must point to a folder containing a ``conanconfig.yml`` file
    (typically the folder where ``conan config install-pkg`` is executed), not to a ``conanfile.py``
    or ``conanfile.txt`` recipe. Use ``--requires`` or ``--tool-requires`` to define recipe references
    directly on the command line.


.. seealso::

  - See the :ref:`conan config install-pkg<reference_commands_conan_config_install_pkg>` command.
