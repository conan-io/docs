.. _reference_runners_ssh:

SSH runner
=============

.. include:: ../../common/experimental_warning.inc

How to use a SSH runner
--------------------------

To run Conan inside a docker container you need to define a ``[runner]`` section in your host profile using the following fields:

- ``type`` **(mandatory)**: define the runner we want to use, in this case ``ssh``.
- ``host`` **(mandatory)**: hostname of the runner to connect to. This runner has to be already accessible by the host machine via SSH protocol and must have ``python3`` installed.
- ``configfile`` **(optional, default False)**: if True, Conan will retrieve the ssh configuration from the default location (``~/.ssh/config``). It can also accept an absolute path to the file.

..  note::

    - The runner profile section doesn't affect the package id.

Extra configuration
-------------------

For extra SSH configuration, refer to https://linux.die.net/man/5/ssh_config.

As an example:

..  code-block:: text

    Host windows-vm
      HostName 10.211.55.3
      User <username>
      ForwardAgent yes

In conan host profile:

..  code-block:: text

    [runner]
    type=ssh
    configfile=True
    host=windows-vm


How to run a `conan create` in a runner
---------------------------------------

..  note::

    The SSH runner feature is only supported by ``conan create`` command. The ``conan install --build`` command is not supported.

In the following links you can find some examples about how to use a conan SSH runner:

- :ref:`Creating a Conan package using a SSH runner<examples_runners_ssh_basic>`
