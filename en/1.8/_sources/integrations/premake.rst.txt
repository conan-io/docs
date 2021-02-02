
|premake_logo| Premake
_________________________

`Premake`_ version 4 has **experimental** support as a generator package.

You can find this generator in this repository: https://github.com/memsharded/conan-premake

In order to use it, clone the repository and export the recipe to the local cache:

.. code-block:: bash

    $ git clone https://github.com/memsharded/conan-premake
    $ conan export conan-premake memsharded/testing

Now you can use this generator as a requirement in your recipes **but also as a generator**:

.. code-block:: text

    [requires]
    PremakeGen@0.1@memsharded/testing

    [generators]
    Premake

.. seealso::

    Check the :ref:`generator package examples<dyn_generators>` to learn how to create and share custom generators like this one.


.. |premake_logo| image:: ../images/premake_logo.png
.. _`Premake`: https://premake.github.io/