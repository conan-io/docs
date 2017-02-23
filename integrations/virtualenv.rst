.. _virtual_environment_generator:


Virtual Environments
====================

Virtualenv generator
--------------------

Conan provides a **virtualenv** generator, able to read from each dependency the :ref:`self.env_info<environment_information>` 
variables declared in the ``package_info()`` method and generate two scripts "activate" and "deactivate". These scripts set/unset all env variables in the current shell.


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
   


In windows are available ``activate.bat``/``deactivate.bat`` and ``activate.ps1``/``deactivate.ps1`` if you are using powershell.
   
Now you can run ``cmake --version`` and check that you have the installed CMake in path.


Deactivate the virtual environment (or close the console) to restore the environment variables:


.. code-block:: bash

   $ source deactivate.sh # Windows: deactivate.bat without the source
   
   
Read the Howto :ref:`Create installer packages<create_installer_packages>` to know more about virtual environment feature.

Virtualbuildenv environment
---------------------------

Use the generator ``virtualbuildenv`` to activate an environment that will set the environment variables for
Autotools and Visual Studio.

This will generate ``activate_build`` and ``deactivate_build`` files. You can concatenate several virtualenv activations
so you could activate a regular virtualenv to get the inherited environment variables from the requirements and then activate
a build virtualenv to set the variables related with the build system.

Read More about the building environment variables defined in the sections :ref:`Building with autotools <building_with_autotools>`
and :ref:`Building with Visual Studio <building_with_visual_studio>`.


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


It will generate a ``conanenv.txt`` file.

  