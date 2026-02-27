.. _reference_config_files_conanrc:

.conanrc
========

.. warning::

  This feature is in **preview**.
  See :ref:`the Conan stability<stability>` section for more information.

The **.conanrc** file can be placed in the folder where you are running Conan or any
parent folder. This file is used to set up the Conan user home directory by defining the
`conan_home` value. This value will take precedence over the :ref:`CONAN_HOME
<reference_environment_variables_conan_home>` environment variable in case it's also
defined. Below are some examples of how you can define the Conan user home in the
**.conanrc** file:

Set the Conan home to an absolute folder:

.. code-block:: bash

    # accepts comments
    conan_home=/absolute/folder

Set the Conan home to a relative folder inside the current folder:

.. code-block:: bash

    conan_home=./relative/folder/inside/current/folder

Set the Conan home to a relative folder outside the current folder:

.. code-block:: bash

    conan_home=../relative/folder/outside/current/folder

Set the Conan home to a path containing the `~` symbol, which will be expanded to the system's user home:

.. code-block:: bash

    conan_home=~/use/the/user/home/to/expand/it

Be aware that the **.conanrc** file is searched for in all parent folders. For
example, in this structure:

.. code-block:: bash

    .
    .conanrc
    |-- project1
    |-- project2


If you are running from the folder `project1`, the parent folders are traversed recursively
until a **.conanrc** file is found, in case it exists.
