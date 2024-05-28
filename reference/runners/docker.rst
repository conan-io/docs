.. _reference_runners_docker:

Docker runner
=============

.. include:: ../../common/experimental_warning.inc

How to use a docker runner
--------------------------

To run Conan inside a docker container you need to define a ``[runner]`` section in your host profile using the following fields:

- ``type`` **(mandatory)**: define the runner we want to use, in this case ``docker``.
- ``dockerfile`` **(optional, default None)**: absolute path to a Dockerfile in case you want to build a docker image.
- ``image`` **(optional, default conan-runner-default)**: docker image name you want to download from a docker registry or the name of the built image in case you define a dockerfile path.
- ``cache`` **(optional, default clean)**: how docker container uses (or not) the host's Conan cache.

    - ``clean``: use an empty cache.
    - ``copy``: copy the host cache inside the container using the :ref:`conan cache save/restore<reference_commands_cache>` command.
    - ``shared``: mount the host's Conan cache as a shared volume.

- ``remove`` **(optional, default false)**: ``true`` or ``false``. Remove the container after running the Conan command.
- ``configfile``  **(optional, default None)**: Absolute path to a configuration file with extra parameters (see **extra configuration** section for more info).

..  note::

    The runner profile section doesn't affect the package id.

Extra configuration
-------------------

If you need more control over the build and execution of the container, you can define more parameters inside a ``configfile`` yaml.

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
        mount: # A dictionary to configure volumes mounted inside the container.
            /home/user1/: # The host path or a volume name
                bind: /mnt/vol2 # The path to mount the volume inside the container
                mode: rw # rw to mount the volume read/write, or ro to mount it read-only.

How to run a `conan create` in a runner
---------------------------------------

..  note::

    The docker runner feature is only supported by ``conan create`` command. The ``conan install --build`` command is not supported.

In the following links you can find some examples about how to use a conan docker runner:

- :ref:`Creating a Conan package using a Docker runner<examples_runners_docker_basic>`
- :ref:`Using a docker runner configfile to parameterize the Dockerfile base image<examples_runners_docker_configfile_build_args>`
