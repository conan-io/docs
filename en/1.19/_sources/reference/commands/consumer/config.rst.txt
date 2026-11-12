.. spelling::

  MyProfile


.. _conan_config:

conan config
============

.. code-block:: bash

    $ conan config [-h] {get,home,install,rm,set} ...

Manages Conan configuration.

Used to edit conan.conf, or install config files.

.. code-block:: text

    positional arguments:
      {get,home,install,rm,set}
                            sub-command help
        get                 Get the value of configuration item
        home                Retrieve the Conan home directory
        install             Install a full configuration from a local or remote
                            zip file
        rm                  Remove an existing config element
        set                 Set a value for a configuration item

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

- Get the Conan home directory:

  .. code-block:: bash

      $ conan config home
      $> /home/user/.conan

.. _conan_config_install:

conan config install
--------------------

.. code-block:: bash

  usage: conan config install [-h] [--verify-ssl [VERIFY_SSL]] [--type {git}]
                            [--args ARGS] [-sf SOURCE_FOLDER]
                            [-tf TARGET_FOLDER]
                            [item]

  positional arguments:
    item                  git repository, local folder or zip file (local or
                          http) where the configuration is stored

  optional arguments:
    -h, --help            show this help message and exit
    --verify-ssl [VERIFY_SSL]
                          Verify SSL connection when downloading file
    --type {git}, -t {git}
                          Type of remote config
    --args ARGS, -a ARGS  String with extra arguments for "git clone"
    -sf SOURCE_FOLDER, --source-folder SOURCE_FOLDER
                          Install files only from a source subfolder from the
                          specified origin
    -tf TARGET_FOLDER, --target-folder TARGET_FOLDER
                          Install to that path in the conan cache


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

.. note::
    During the installation, Conan skips any file with the name *README.md* or *LICENSE.txt*.

The :command:`conan config install <item>` calls are stored in a *config_install.json* file in the Conan local cache. That allows to issue a :command:`conan config install` command, without arguments, to iterate over the cached configurations, executing them again (updating).


**Examples**:

- Install the configuration from a URL:

  .. code-block:: bash

      $ conan config install http://url/to/some/config.zip


- Install the configuration from a URL, but only getting the files inside a *origin* folder
  inside the zip file, and putting them inside a *target* folder in the local cache:

  .. code-block:: bash

      $ conan config install http://url/to/some/config.zip -sf=origin -tf=target

- Install configuration from 2 different zip files from 2 different urls, using different source
  and target folders for each one, then update all:

  .. code-block:: bash

      $ conan config install http://url/to/some/config.zip -sf=origin -tf=target
      $ conan config install http://url/to/some/config.zip -sf=origin2 -tf=target2
      $ conan config install http://other/url/to/other.zip -sf=hooks -tf=hooks
      # Later on, execute again the previous configurations cached:
      $ conan config install

  It's not needed to specify any argument, it will iterate previously stored configurations in *config_install.json*, executing them again.

- Install the configuration from a Git repository with submodules:

  .. code-block:: bash

      $ conan config install http://github.com/user/conan_config/.git --args "--recursive"

  You can also force the git download by using :command:`--type git` (in case it is not deduced from the URL automatically):

  .. code-block:: bash

      $ conan config install http://github.com/user/conan_config/.git --type git

- Install from a URL skipping SSL verification:

  .. code-block:: bash

      $ conan config install http://url/to/some/config.zip --verify-ssl=False

  This will disable the SSL check of the certificate.

- Install the configuration from a local path:

  .. code-block:: bash

      $ conan config install /path/to/some/config.zip
