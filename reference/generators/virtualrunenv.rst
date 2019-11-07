.. _virtualrunenv_generator:

virtualrunenv
=============

.. container:: out_reference_box

    This is the reference page for ``virtualrunenv`` generator.
    Go to :ref:`Mastering/Virtual Environments<virtual_environment_generator>` if you want to learn how to use Conan virtual environments.

Created files
-------------

- activate_run.{sh|bat}
- deactivate_run.{sh|bat}

Usage
-----

Linux/macOS:

.. code-block:: bash

    > source activate_run.sh

Windows:

.. code-block:: bash

    > activate_run.bat

Variables declared
------------------

+--------------------+---------------------------------------------------------------------+
| ENVIRONMENT VAR    | DESCRIPTION                                                         |
+====================+=====================================================================+
| PATH               | With every ``bin`` folder of your requirements.                     |
+--------------------+---------------------------------------------------------------------+
| LD_LIBRARY_PATH    | ``lib`` folders of  your requirements.                              |
+--------------------+---------------------------------------------------------------------+
| DYLD_LIBRARY_PATH  | ``lib`` folders of  your requirements.                              |
+--------------------+---------------------------------------------------------------------+
| DYLD_FRAMEWORK_PATH| ``framework_paths`` folders of  your requirements.                  |
+--------------------+---------------------------------------------------------------------+
