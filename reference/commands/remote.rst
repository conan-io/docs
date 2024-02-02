.. _reference_commands_remote:

conan remote
============

Use this command to add, edit and remove Conan repositories from the Conan remote
registry and also manage authentication to those remotes. For more information on how to
work with Conan repositories, please check the :ref:`dedicated section <conan_repositories>`.

.. autohelp::
    :command: conan remote


conan remote add
----------------

.. autohelp::
    :command: conan remote add


conan remote auth
-----------------

.. autohelp::
    :command: conan remote auth


conan remote disable
--------------------

.. autohelp::
    :command: conan remote disable


conan remote enable
-------------------

.. autohelp::
    :command: conan remote enable


conan remote list
-----------------

.. autohelp::
    :command: conan remote list


conan remote list-users
-----------------------

.. autohelp::
    :command: conan remote list-users


conan remote login
------------------

.. autohelp::
    :command: conan remote login


conan remote logout
-------------------

.. autohelp::
    :command: conan remote logout


conan remote remove
-------------------

.. autohelp::
    :command: conan remote remove


conan remote rename
-------------------

.. autohelp::
    :command: conan remote rename


conan remote set-user
---------------------

.. autohelp::
    :command: conan remote set-user


conan remote update
-------------------

<<<<<<< HEAD
.. code-block:: text

    $ conan remote update -h
    usage: conan remote update [-h] [-v [V]] [-cc CORE_CONF] [--url URL]
                               [--secure] [--insecure] [--index INDEX]
                               [-ap [ALLOWED_PACKAGES ...]]
                               remote

    Update a remote.

    positional arguments:
      remote                Name of the remote to update

    options:
      -h, --help            show this help message and exit
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      -cc CORE_CONF, --core-conf CORE_CONF
                            Global configuration for Conan
      --url URL             New url for the remote
      --secure              Don't allow insecure server connections when using SSL
      --insecure            Allow insecure server connections when using SSL
      --index INDEX         Insert the remote at a specific position in the remote
                            list
      -ap [ALLOWED_PACKAGES ...], --allowed-packages [ALLOWED_PACKAGES ...]
                            Add recipe reference pattern to the list of allowed
                            packages for this remote
=======
.. autohelp::
    :command: conan remote update
>>>>>>> release/2.0


Read more
---------

- :ref:`Uploading packages tutorial <uploading_packages>`
- :ref:`Working with Conan repositories <conan_repositories>`
- :ref:`Upload Conan packages to remotes using conan upload command <reference_commands_upload>`
