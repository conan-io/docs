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

It is also possible use a ``conanconfig.yml`` file as an input to the command:

.. code-block:: bash

  $ conan lock upgrade-config . --update-config-requires=config/1.0


.. seealso::

  - See the :ref:`conan config install-pkg<reference_commands_conan_config_install_pkg>` command.
