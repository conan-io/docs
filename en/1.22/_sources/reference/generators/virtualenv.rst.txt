.. spelling::

  ps


.. _virtualenv_generator:

virtualenv
==========

.. container:: out_reference_box

    This is the reference page for ``virtualenv`` generator.
    Go to :ref:`Mastering/Virtual Environments<virtual_environment_generator>` if you want to learn how to use Conan virtual environments.

Created files
-------------

- activate.{sh|bat|ps1}
- deactivate.{sh|bat|ps1}

Usage
-----

Linux/macOS:

.. code-block:: bash

    > source activate.sh

Windows:

.. code-block:: bash

    > activate.bat

Variables declared
------------------

+-----------------+--------------------------------------------------------------------------------------------------+
| ENVIRONMENT VAR | VALUE                                                                                            |
+=================+==================================================================================================+
| PS1             | New shell prompt value corresponding to the current directory name                               |
+-----------------+--------------------------------------------------------------------------------------------------+
| OLD_PS1         | Old PS1 value, to recover it in deactivation                                                     |
+-----------------+--------------------------------------------------------------------------------------------------+
| `XXXX`          | Any variable declared in the ``self.env_info`` object of the requirements.                       |
+-----------------+--------------------------------------------------------------------------------------------------+
