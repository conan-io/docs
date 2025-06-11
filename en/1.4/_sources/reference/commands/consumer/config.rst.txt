
.. _conan_config:

conan config
============

.. code-block:: bash

    $ conan config [-h] {rm,set,get,install} ...

Manages Conan configuration. Edits the conan.conf or installs config files.

.. code-block:: text

    positional arguments:
      {rm,set,get,install}  sub-command help
        rm                  Remove an existing config element
        set                 Set a value for a configuration item
        get                 Get the value of configuration item
        install             install a full configuration from a local or remote
                            zip file

    optional arguments:
      -h, --help            show this help message and exit


**Examples**

- Change the logging level to 10:

  .. code-block:: bash

      $ conan config set log.level=10

- Get the logging level:

  .. code-block:: bash

      $ conan config get log.level
      $> 10

.. _conan_config_install:

conan config install
--------------------

The ``config install`` is intended to share the Conan client configuration. For example, in a company or organization,
is important to have common ``settings.yml``, ``profiles``, etc.

It retrieves a zip file from a local directory or url and apply the files in the local Conan configuration.

The zip can contain only a subset of all the allowed configuration files, only the present files will be
replaced, except the **conan.conf** file, that will apply only the declared variables in the zipped ``conan.conf`` file
and will keep the rest of the local variables.

The **profiles files**, that will be overwritten if already present, but won't delete any other profile file that the user
has in the local machine.

All files in the zip will be copied to the conan home directory.
These are the special files and the rules applied to merge them:

+--------------------------------+----------------------------------------------------------------------+
| File                           | How it is applied                                                    |
+================================+======================================================================+
| profiles/MyProfile             | Overrides the local ~/.conan/profiles/MyProfile if already exists    |
+--------------------------------+----------------------------------------------------------------------+
| settings.yml                   | Overrides the local ~/.conan/settings.yml                            |
+--------------------------------+----------------------------------------------------------------------+
| remotes.txt                    | Overrides remotes. Will remove remotes that are not present in file  |
+--------------------------------+----------------------------------------------------------------------+
| config/conan.conf              | Merges the variables, overriding only the declared variables         |
+--------------------------------+----------------------------------------------------------------------+

The local cache *registry.txt* file contains the remotes definitions, as well as the mapping from packages
to remotes. In general it is not a good idea to add it to the installed files.

The specified URL will be stored in the ``general.config_install`` variable of the ``conan.conf`` file,
so following calls to :command:`conan config install` command doesn't need to specify the URL.

**Examples**:

- Install the configuration from an url:

  .. code-block:: bash

      $ conan config install http://url/to/some/config.zip

  Conan config command stores the specified URL in the conan.conf ``general.config_install`` variable.

- Install from an url skipping SSL verification:

  .. code-block:: bash

      $ conan config install http://url/to/some/config.zip --verify-ssl=False

  This will disable the SSL check of the certificate. This option is defaulted to ``True``.

- Refresh the configuration again:

  .. code-block:: bash

      $ conan config install

  It's not needed to specify the url again, it is already stored.

- Install the configuration from a local path:

  .. code-block:: bash

      $ conan config install /path/to/some/config.zip
