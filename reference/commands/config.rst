
conan config
============


.. code-block:: bash

   $ conan config [-h] {rm,set,get} ...


Manages conan.conf information.

.. code-block:: bash

    positional arguments:
      {rm,set,get}  sub-command help
        rm          rm an existing config element
        set         set/add value
        get         get the value of existing element


**Examples**

- Change the logging level to 10:

.. code-block:: bash

    $ conan config set log.level=10

- Get the logging level:

.. code-block:: bash

    $ conan config get log.level
    $> 10


