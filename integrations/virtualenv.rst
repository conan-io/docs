.. _virtual_environment_generator:


Virtual Environments
====================

Conan provides a **virtualenv** generator, able to read from each dependency the :ref:`self.env_info<environment_information>` variables declared in the ``package_info()`` method and generate two scripts "activate" and "deactivate". These scripts set/unset all env variables in the current shell.


Open ``conanfile.txt`` and change (or add) **virtualenv** generator:


.. code-block:: text

   [requires]
   cmake-installer/0.1@lasote/testing

   [generators]
   virtualenv


Run ``conan install``:

.. code-block:: bash

   $ conan install

And activate the virtual environment:


.. code-block:: bash

   $ source activate.sh # Windows: activate.bat without the source

   
Now you can run ``cmake --version`` and check that you have the installed CMake in path.


Deactivate the virtual environment (or close the console) to restore the environment variables:


.. code-block:: bash

   $ source deactivate.sh # Windows: deactivate.bat without the source
   
   
Read the Howto :ref:`Create installer packages<create_installer_packages>` to know more about virtual environment feature.


Virtual environment dump
------------------------

Besides the automated scripts to activate/deactivate environment variables, it is possible to
do a simple text dump of the environment variables of the dependencies, with the ``env`` generator:


.. code-block:: text

   [requires]
   ...

   [generators]
   env

or

.. code-block:: bash

   $ conan install ... -g env


It will generate a ``conanenv.txt`` file. This file will be used by partial conan commands
like ``build``, ``source``, ``package`` and ``imports``


  