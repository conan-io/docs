.. _virtualenv_python_generator:

virtualenv_python
=================

.. warning::

    This generator is deprecated. The :ref:`virtualenv_generator` generator already contains all the
    environment variables declared in the graph of dependencies. Use it together with
    the :ref:`virtualrunenv_generator` generator to populate the ``DYLD_LIBRARY_PATH``, ``LD_LIBRARY_PATH``
    and ``PATH`` variables with the information of the dependencies too.


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
