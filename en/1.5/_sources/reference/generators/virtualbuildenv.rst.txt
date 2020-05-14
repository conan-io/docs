.. _virtualbuildenv_generator:

virtualbuildenv
===============

.. container:: out_reference_box

    This is the reference page for ``virtualbuildenv`` generator.
    Go to :ref:`Mastering/Virtual Environments<virtual_environment_generator>` if you want to learn
    how to use Conan virtual environments.

Created files
-------------

- *activate_build.{sh|bat}*
- *deactivate_build.{sh|bat}*

Usage
-----

Linux/OSX:

.. code-block:: bash

    $ source activate_build.sh

Windows:

.. code-block:: bash

    $ activate_build.bat

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


In the case of using this generator to compile with Visual Studio, it also sets the environment
variables needed via ``tools.vcvars()`` to build your project. Some of these variables are:

.. code-block:: bash

    VSINSTALLDIR=C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/
    WINDIR=C:/WINDOWS
    WindowsLibPath=C:/Program Files (x86)/Windows Kits/10/UnionMetadata/10.0.16299.0;
    WindowsSdkBinPath=C:/Program Files (x86)/Windows Kits/10/bin/
    WindowsSdkDir=C:/Program Files (x86)/Windows Kits/10/
    WindowsSDKLibVersion=10.0.16299.0/
    WindowsSdkVerBinPath=C:/Program Files (x86)/Windows Kits/10/bin/10.0.16299.0/