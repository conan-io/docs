.. _virtualenv_python_generator:

virtualenv_python
=================

.. warning::

    This is a **deprecated** feature. Please refer to the :ref:`Migration Guidelines<conan2_migration_guide>`
    to find the feature that replaced this one.

Created files
-------------

- activate_run_python.{sh|bat}
- deactivate_run_python.{sh|bat}

Usage
-----

Linux/macOS:

.. code-block:: bash

    > source activate_run_python.sh

Windows:

.. code-block:: bash

    > activate_run_python.bat

Variables declared
------------------

+--------------------+---------------------------------------------------------------------+
| ENVIRONMENT VAR    | DESCRIPTION                                                         |
+====================+=====================================================================+
| PATH               | With every ``bin`` folder of your requirements.                     |
+--------------------+---------------------------------------------------------------------+
| PYTHONPATH         | Union of ``PYTHONPATH`` of your requirements.                       |
+--------------------+---------------------------------------------------------------------+
| LD_LIBRARY_PATH    | ``lib`` folders of  your requirements.                              |
+--------------------+---------------------------------------------------------------------+
| DYLD_LIBRARY_PATH  | ``lib`` folders of  your requirements.                              |
+--------------------+---------------------------------------------------------------------+
