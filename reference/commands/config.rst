conan config
============

Manage the Conan configuration in the Conan home.


conan config home
-----------------

.. code-block:: text

    $ conan config home --help
    usage: conan config home [-h] [-v [V]]
    Show the Conan home folder.

    optional arguments:
      -h, --help  show this help message and exit
      -v [V]      Level of detail of the output. Valid options from less verbose
                  to more verbose: -vquiet, -verror, -vwarning, -vnotice,
                  -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace


The ``conan config home`` command returns the path of the Conan home folder.

.. code-block:: text

    $ conan config home


.. _reference_commands_conan_config_install:

conan config install
--------------------

.. code-block:: text

    $ conan config install -h
    usage: conan config install [-h] [-v [V]]
                                [--verify-ssl [VERIFY_SSL] | --insecure]
                                [-t {git,dir,file,url}] [-a ARGS]
                                [-sf SOURCE_FOLDER] [-tf TARGET_FOLDER]
                                item

    Install the configuration (remotes, profiles, conf), from git, http or a
    folder, into the Conan home folder.

    positional arguments:
      item                  git repository, local file or folder or zip file
                            (local or http) where the configuration is stored

    optional arguments:
      -h, --help            show this help message and exit
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      --verify-ssl [VERIFY_SSL]
                            Verify SSL connection when downloading file
      --insecure            Allow insecure server connections when using SSL.
                            Equivalent to --verify-ssl=False
      -t {git,dir,file,url}, --type {git,dir,file,url}
                            Type of remote config
      -a ARGS, --args ARGS  String with extra arguments for "git clone"
      -sf SOURCE_FOLDER, --source-folder SOURCE_FOLDER
                            Install files only from a source subfolder from the
                            specified origin
      -tf TARGET_FOLDER, --target-folder TARGET_FOLDER
                            Install to that path in the conan cache



The ``conan config install`` command is intended to install in the current home a common shared Conan
configuration, like the definitions of ``remotes``, ``profiles``, ``settings``, ``hooks``, ``extensions``, etc.

The command can use as source any of the following:

- A URL pointing to a zip archive containing the configuration files
- A git repository containing the files
- A local folder
- Just one file

Files in the current Conan home will be replaced by the ones from the installation source.
All the configuration files can be shared and installed this way:

- ``remotes.json`` for the definition of remotes
- Any custom profile files inside a ``profiles`` subfolder
- Custom ``settings.yml``
- Custom ``global.conf``
- All the extensions, including plugins, hooks.
- Custom user commands.

This command reads a ``.conanignore`` file which, if present, filters which files and folders
are copied over to the user's Conan home folder.
This file uses `fnmatch <https://docs.python.org/3/library/fnmatch.html>`_ patterns
to match over the folder contents, excluding those entries that match from the config installation.
See `conan-io/command-extensions's .conanignore <https://github.com/conan-io/command-extensions/blob/main/.conanignore>`_ for an example of such a file.


**Examples**:

- Install the configuration from a URL:

  .. code-block:: text

      $ conan config install http://url/to/some/config.zip


- Install the configuration from a URL, but only getting the files inside a *origin* folder
  inside the zip file, and putting them inside a *target* folder in the local cache:

  .. code-block:: text

      $ conan config install http://url/to/some/config.zip -sf=origin -tf=target

- Install configuration from 2 different zip files from 2 different urls, using different source
  and target folders for each one, then update all:

  .. code-block:: text

      $ conan config install http://url/to/some/config.zip -sf=origin -tf=target
      $ conan config install http://url/to/some/config.zip -sf=origin2 -tf=target2
      $ conan config install http://other/url/to/other.zip -sf=hooks -tf=hooks

- Install the configuration from a Git repository with submodules:

  .. code-block:: text

      $ conan config install http://github.com/user/conan_config/.git --args "--recursive"

  You can also force the git download by using :command:`--type git` (in case it is not deduced from the URL automatically):

  .. code-block:: text

      $ conan config install http://github.com/user/conan_config/.git --type git

- Install from a URL skipping SSL verification:

  .. code-block:: text

      $ conan config install http://url/to/some/config.zip --verify-ssl=False

  This will disable the SSL check of the certificate.

- Install a specific file from a local path:

  .. code-block:: text

      $ conan config install my_settings/settings.yml

- Install the configuration from a local path:

  .. code-block:: text

      $ conan config install /path/to/some/config.zip


conan config list
-----------------
.. code-block:: text

    $ conan config list -h
    usage: conan config list [-h] [-f FORMAT] [-v [V]]

    Show all the Conan available configurations: core and tools.

    optional arguments:
      -h, --help            show this help message and exit
      -f FORMAT, --format FORMAT
                            Select the output format: json
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace



Displays all the Conan built-in configurations. There are 2 groups:

- ``core.xxxx``: These can only be defined in ``global.conf`` and are used by Conan internally
- ``tools.xxxx``: These can be defined both in ``global.conf`` and profiles, and will be used by
  recipes and tools used within recipes, like ``CMakeToolchain``

.. include:: ../../common/config_list.inc


.. seealso::

    - :ref:`Conan configuration files <reference_config_files>`


conan config show
-----------------
.. code-block:: text

    $ conan config show -h
    usage: conan config show [-h] [-f FORMAT] [-v [V]] pattern

    Get the value of the specified conf

    positional arguments:
      pattern               Conf item(s) pattern for which to query their value

    optional arguments:
      -h, --help            show this help message and exit
      -f FORMAT, --format FORMAT
                            Select the output format: json
      -v [V]                Level of detail of the output. Valid options from
                            less verbose to more verbose: -vquiet, -verror,
                            -vwarning, -vnotice, -vstatus, -v or -vverbose, -vv
                            or -vdebug, -vvv or -vtrace

Shows the values of the conf items that match the given pattern.

For a *global.conf* consisting of

.. code-block:: text

    tools.build:jobs=42
    tools.files.download:retry_wait=10
    tools.files.download:retry=7
    core.net.http:timeout=30
    core.net.http:max_retries=5
    zlib*/:tools.files.download:retry_wait=100
    zlib*/:tools.files.download:retry=5

You can get all the values:

.. code-block:: text

    $ conan config show "*"

    core.net.http:max_retries: 5
    core.net.http:timeout: 30
    tools.files.download:retry: 7
    tools.files.download:retry_wait: 10
    tools.build:jobs: 42
    zlib*/:tools.files.download:retry: 5
    zlib*/:tools.files.download:retry_wait: 100

Or just those referring to the ``tools.files`` section:

.. code-block:: text

    $ conan config show "*tools.files*"

    tools.files.download:retry: 7
    tools.files.download:retry_wait: 10
    zlib*/:tools.files.download:retry: 5
    zlib*/:tools.files.download:retry_wait: 100

Notice the first ``*`` in the pattern. This will match all the package patterns.
Removing it will make the command only show global confs:

.. code-block:: text

    $ conan config show "tools.files*"

    tools.files.download:retry: 7
    tools.files.download:retry_wait: 10
