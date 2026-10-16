.. spelling::

  MyProfile


.. _conan_config:

conan config
============

.. code-block:: bash

    $ conan config [-h] {rm,set,get,install} ...

Manages Conan configuration. Used to edit conan.conf, or install config files.

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

It can get its configuration files from a local or remote zip file, from a local directory or from a git repository. It then installs the
files in the local Conan configuration.

The configuration may contain all or a subset of the allowed configuration files. Only the files that are present will be
replaced. The only exception is the *conan.conf* file for which only the variables declared will be installed,
leaving the other variables unchanged.

This means for example that **profiles** and **hooks** files will be overwritten if already present, but no profile or hook file that the
user has in the local machine will be deleted.

All the configuration files will be copied to the Conan home directory. These are the special files and the rules applied to merge them:

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
| hooks/my_hook.py               | Overrides the local ~/.conan/hooks/my_hook.py if already exists      |
+--------------------------------+----------------------------------------------------------------------+

The file *remotes.txt* is the only file listed above which does not have a direct counterpart in
the *~/.conan* folder. Its format is a list of entries, one on each line, with the form of

.. code-block:: text

    [remote name] [remote url] [bool]

where ``[bool]`` (either ``True`` or ``False``) indicates whether SSL should be used to verify that remote. The remote definitions can be
found in the *registry.txt*/*registry.json* files and they provide a helpful starting point when writing the *remotes.txt* to be packaged in
a Conan client configuration.

.. important::
    The local cache *registry.txt*/*registry.json* file contains the remotes definitions as well as the mapping of installed packages from
    remotes. Sharing the complete contents of this file via this command is not recommended as this records the status of the local cache,
    which may be different from one machine to another.

The specified URL or path, the arguments used (if any) and the source type (from git, from dir, from zip file or from URL) will be stored in
the ``general.config_install`` variable of the *conan.conf* file, so as following calls to :command:`conan config install` command doesn't
need to specify them.

**Examples**:

- Install the configuration from a URL:

  .. code-block:: bash

      $ conan config install http://url/to/some/config.zip

  Conan config command stores the specified URL in the conan.conf ``general.config_install`` variable.

- Install the configuration from a Git repository with submodules:

  .. code-block:: bash

      $ conan config install http://github.com/user/conan_config/.git --args "--recursive"

  You can also force the git download by using :command:`--type git` (in case it is not deduced from the URL automatically):

  .. code-block:: bash

      $ conan config install http://github.com/user/conan_config/.git --type git

- Install from a URL skipping SSL verification:

  .. code-block:: bash

      $ conan config install http://url/to/some/config.zip --verify-ssl=False

  This will disable the SSL check of the certificate. This option is defaulted to ``True`` and it is also stored in *conan.conf*, so
  following calls to this command don't need to specify it again.

- Refresh the configuration again:

  .. code-block:: bash

      $ conan config install

  It's not needed to specify the url again, it is already stored.

- Install the configuration from a local path:

  .. code-block:: bash

      $ conan config install /path/to/some/config.zip
