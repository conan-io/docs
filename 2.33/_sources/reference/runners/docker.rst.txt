.. _reference_runners_docker:

Docker runner
=============

.. include:: ../../common/experimental_warning.inc

How to use a docker runner
--------------------------

To run Conan inside a Docker container, a ``[runner]`` section must be defined in the host profile with the following fields:

- ``type`` **(mandatory)**: Specifies the runner to use, in this case, ``docker``.
- ``dockerfile`` **(optional, default: None)**: Absolute path to a Dockerfile, if a Docker image needs to be built.
- ``image`` **(optional, default: conan-runner-default)**: Name of the Docker image to download from a registry or the name of the locally built image if a Dockerfile path is provided.
- ``cache`` **(optional, default: clean)**: Determines how the Docker container interacts with the host's Conan cache.

    - ``clean``: Uses an empty cache.
    - ``copy``: Copies the host cache into the container using the :ref:`conan cache save/restore<reference_commands_cache>` command.
    - ``shared``: Mounts the host’s Conan cache as a shared volume.

- ``remove`` **(optional, default: false)**: Specifies whether to remove the container after executing the Conan command (true or false).
- ``configfile`` **(optional, default: None)**: Absolute path to a configuration file with additional parameters (see **extra configuration** section for details).
- ``build_context`` **(optional, default: None)**: Defines the Docker build context (see **extra configuration** section for details).
- ``platform`` **(optional, default: None)**: Specifies the platform for building the container (e.g., ``linux/amd64``). This is particularly useful for Mac Silicon users.
- ``copy_config_files`` **(optional, default: empty)**: Comma-separated list of `fnmatch <https://docs.python.org/3/library/fnmatch.html>`_ patterns, relative to the Conan home folder, of extra host files/folders to copy into the container's Conan home, for the ``clean`` and ``copy`` cache modes. Disabled by default.

  ..  code-block:: text

      [runner]
      type=docker
      copy_config_files=extensions/*

  A few files are never copied, even if a pattern matches them: the package cache storage folder, the sources backup cache, ``version.txt``, ``.local_recipes_index/*``, and the local remote-login database. ``credentials.json`` and ``source_credentials.json`` are also skipped by default for containing sensitive data, but are copied if their exact name is listed in ``copy_config_files``.

..  note::

    - The ``shared`` cache option may cause permission issues depending on the user inside and outside the container. It is recommended to use the ``copy`` cache for greater stability, despite a slight increase in setup time.
    - The runner profile section does not impact the package ID.


Extra configuration
-------------------

For greater control over the build and execution of the container, additional parameters can be defined within a ``configfile`` YAML file.

..  code-block:: yaml

    image: image_name # The image to build or run.
    build:
        dockerfile: /dockerfile/path # Dockerfile path.
        build_context: /build/context/path # Path within the build context to the Dockerfile.
        build_args: # A dictionary of build arguments
            foo: bar
        cacheFrom: # A list of images used for build cache resolution
            - image_1
    run:
        name: container_name # The name for this container.
        containerEnv: # Environment variables to set inside the container.
            env_var_1: env_value
        containerUser: user_name # Username or UID to run commands as inside the container.
        privileged: False # Run as privileged
        capAdd: # Add kernel capabilities.
            - SYS_ADMIN
            - MKNOD
        securityOpt: # A list of string values to customize labels for MLS systems, such as SELinux.
            - opt_1
        mounts: # A dictionary to configure volumes mounted inside the container.
            /home/user1/: # The host path or a volume name
                bind: /mnt/vol2 # The path to mount the volume inside the container
                mode: rw # rw to mount the volume read/write, or ro to mount it read-only.
        network: my-network # Specifies the network for the container.

How to run a `conan create` in a runner
---------------------------------------

..  note::

    The docker runner feature is only supported by ``conan create`` command. The ``conan install --build`` command is not supported.

The following links provide examples of how to use a Conan Docker runner:

- :ref:`Creating a Conan package using a Docker runner<examples_runners_docker_basic>`
- :ref:`Using a docker runner configfile to parameterize the Dockerfile base image<examples_runners_docker_configfile_build_args>`
