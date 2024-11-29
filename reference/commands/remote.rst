.. _reference_commands_remote:

conan remote
============

Use this command to add, edit and remove Conan repositories from the Conan remote
registry and also manage authentication to those remotes. For more information on how to
work with Conan repositories, please check the :ref:`dedicated section <conan_repositories>`.

.. autocommand::
    :command: conan remote -h


conan remote add
----------------

.. autocommand::
    :command: conan remote add -h


conan remote auth
-----------------

.. autocommand::
    :command: conan remote auth -h


.. note::

   If a remote which allows anonymous access matches the pattern given to the command, Conan won't try to authenticate with it by default.
   If you want to authenticate with a remote that allows anonymous access, you can use the ``--force`` option.

conan remote disable
--------------------

.. autocommand::
    :command: conan remote disable -h


conan remote enable
-------------------

.. autocommand::
    :command: conan remote enable -h


conan remote list
-----------------

.. autocommand::
    :command: conan remote list -h


conan remote list-users
-----------------------

.. autocommand::
    :command: conan remote list-users -h


conan remote login
------------------

.. autocommand::
    :command: conan remote login -h


conan remote logout
-------------------

.. autocommand::
    :command: conan remote logout -h


conan remote remove
-------------------

.. autocommand::
    :command: conan remote remove -h


conan remote rename
-------------------

.. autocommand::
    :command: conan remote rename -h


conan remote set-user
---------------------

.. autocommand::
    :command: conan remote set-user -h


conan remote update
-------------------

.. autocommand::
    :command: conan remote update -h


.. seealso::

    - :ref:`Uploading packages tutorial <uploading_packages>`
    - :ref:`Working with Conan repositories <conan_repositories>`
    - :ref:`Upload Conan packages to remotes using conan upload command <reference_commands_upload>`
