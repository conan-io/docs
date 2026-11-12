.. _virtualbuildenv_generator:

virtualbuildenv
===============

.. container:: out_reference_box

    This is the reference page for ``virtualbuildenv`` generator.
    Go to :ref:`Mastering/Virtual Environments<virtual_environment_generator>` if you want to learn how to use conan virtual environments.


Created files
-------------

- activate_build.{sh|bat}
- deactivate_build.{sh|bat}

Usage
-----

Linux/OSX:

.. code-block:: bash

    > source activate_build.sh


Windows:

.. code-block:: bash

    > activate_build.bat



Variables declared
------------------

+--------------------+---------------------------------------------------------------------+
| ENVIRONMENT VAR    | DESCRIPTION                                                         |
+====================+=====================================================================+
| LIBS               | Library names to link                                               |
+--------------------+---------------------------------------------------------------------+
| LDFLAGS            | Link flags, (-L, -m64, -m32)                                        |
+--------------------+---------------------------------------------------------------------+
| CFLAGS             | Options for the C compiler (-g, -s, -m64, -m32, -fPIC)              |
+--------------------+---------------------------------------------------------------------+
| CXXFLAGS           | Options for the C++ compiler (-g, -s, -stdlib, -m64, -m32, -fPIC)   |
+--------------------+---------------------------------------------------------------------+
| CPPFLAGS           | Preprocessor definitions (-D, -I)                                   |
+--------------------+---------------------------------------------------------------------+
| LIB                | Library paths separated with ";"     (Visual Studio)                |
+--------------------+---------------------------------------------------------------------+
| CL                 | "/I" flags with include directories   (Visual Studio)               |
+--------------------+---------------------------------------------------------------------+

