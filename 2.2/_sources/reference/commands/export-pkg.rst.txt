.. _reference_commands_export-pkg:

conan export-pkg
================

.. autocommand::
    :command: conan export-pkg -h


The ``conan export-pkg`` command creates a package binary directly from pre-compiled binaries in a user folder. This command can be useful in different cases:

- When creating a package for some closed source or pre-compiled binaries provided by a vendor. In this case, it is not necessary that the ``conanfile.py`` recipe contains a ``build()`` method, and providing the ``package()`` and ``package_info()`` method are enough to package those pre-compiled binaries. In this case the ``build_policy = "never"`` could make sense to indicate it is not possible to ``conan install --build=this_pkg``, as it doesn't know how to build from sources when it is a dependency.
- When testing some recipe locally in the :ref:`local development flow<local_package_development_flow>`, it can be used to quickly put the locally built binaries in the cache to make them available to other packages for testing, without needing to go through a full ``conan create`` that would be slower.

In general, it is expected that when ``conan export-pkg`` executes, the possible Conan dependencies that were necessary to build this package had already been installed via ``conan install``, so it is not necessary to download dependencies at ``export-pkg`` time. But if for some reason this is not the case, the command defines ``--remote`` and ``--no-remote`` arguments, similar to other commands, as well as the ``--skip-binaries`` optimization that could save some time installing dependencies binaries if they are not strictly necessary for the current ``export-pkg``. But this is the responsibility of the user, as it is possible that such binaries are actually necessary, for example, if a ``tool_requires = "cmake/x.y"`` is used and the ``package()`` method implements a ``cmake.install()`` call, this will definitely need the binaries for the dependencies installed in the current machine to execute.


.. seealso::

    - Check the :ref:`JSON format output <reference_commands_graph_info_json_format>` for this command.
    - Read the tutorial about the :ref:`local package development flow <local_package_development_flow>`.
