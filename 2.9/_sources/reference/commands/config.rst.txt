conan config
============

Manage the Conan configuration in the Conan home.


conan config home
-----------------

.. autocommand::
    :command: conan config home -h


The ``conan config home`` command returns the path of the Conan home folder.

.. code-block:: text

    $ conan config home

    /home/user/.conan2


.. _reference_commands_conan_config_install:

conan config install
--------------------

.. autocommand::
    :command: conan config install -h


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
You can force certain files to be copied over by using the ``!`` negation syntax:

.. code-block:: text

    # Ignore all files
    *
    # But copy the file named "settings.yml"
    !settings.yml


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

      $ conan config install http://github.com/user/conan_config/.git --args="--recursive"

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


.. _reference_commands_conan_config_install_pkg:

conan config install-pkg
------------------------

.. include:: ../../common/experimental_warning.inc


.. autocommand::
    :command: conan config install-pkg -h


This command allows to install configuration from a Conan package stored in a Conan server.

The packages containing configuration follow some special rules:

- They must define the ``package_type = "configuration"``
- The configuration files must be packaged in the final "binary" package, following the same layout as they would for other ``conan config install`` cases.
- They cannot be used as ``requires`` of other packages, because that would result in a chicken-and-egg problem.
- They cannot contain ``requires`` to other packages
- The configuration packages are created with ``conan create`` and ``conan export-pkg`` as other packages, and uploaded to the servers with ``conan upload``

To install configuration from a Conan configuration package, it is possible:

- To generate a lockfile file with ``--lockfile-out``. This lockfile file can be passed to ``conan config install-pkg --lockfile`` (it will automatically loaded it if is named ``conan.lock`` and found in the current directory) in the future to guarantee the same exact version.
- Version ranges can be used ``conan config install-pkg "myconf/[>=1.0 <2]"`` is correct, and it will install the latest one in that range.
- ``conan config install-pkg`` always look in the server for the latest version or revision.
- If the same version and revision was downloaded and installed from the server, ``conan config install-pkg`` will be a no-op unless ``--force`` is used, in this case the configuration will be overwritten.

It is also possible to make the version of the configuration affect all packages ``package_id`` and be part of the binary model, by activating the ``core.package_id:config_mode`` conf (this is also experimental), to any available mode, like ``minor_mode``.

As the ``conan config install-pkg`` command downloads the package from a Conan remote server, it can download from an already existing remote,
or it can download from a Conan remote directly specifying the repository URL:

.. code:: bash

    $ conan config install-pkg myconf/version --url=<url/conan/remote/repo>



conan config list
-----------------

.. autocommand::
    :command: conan config list -h


Displays all the Conan built-in configurations. There are 2 groups:

- ``core.xxxx``: These can only be defined in ``global.conf`` and are used by Conan internally
- ``tools.xxxx``: These can be defined both in ``global.conf`` and profiles, and will be used by
  recipes and tools used within recipes, like ``CMakeToolchain``


.. autocommand::
    :command: conan config list

It is possible to list only the configurations that match a given pattern, like:

.. code:: bash

    $  conan config list proxy
    core.net.http:clean_system_proxy: If defined, the proxies system env-vars will be discarded
    core.net.http:no_proxy_match: List of urls to skip from proxies configuration
    core.net.http:proxies: Dictionary containing the proxy configuration


.. seealso::

    - These configurations can be defined in ``global.conf``, profile files and command line, see 
      :ref:`Conan configuration files <reference_config_files>`


conan config show
-----------------

.. autocommand::
    :command: conan config show -h


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
