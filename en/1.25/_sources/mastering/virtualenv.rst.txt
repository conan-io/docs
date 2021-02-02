.. _virtual_environment_generator:


Virtual Environments
====================

Conan offer three special Conan generators to create virtual environments:

- ``virtualenv``:  Declares the :ref:`self.env_info<method_package_info_env_info>` variables of the requirements.
- ``virtualbuildenv``: Special build environment variables for autotools/visual studio.
- ``virtualrunenv``: Special environment variables to locate executables and shared libraries in the requirements.

These virtual environment generators create two executable script files (.sh or .bat depending on the current operating system), one
to ``activate`` the virtual environment (set the environment variables) and one to ``deactivate`` it.

You can aggregate two or more virtual environments, that means that you can activate a ``virtualenv`` and then activate a ``virtualrunenv`` so you will
have available the environment variables declared in the ``env_info`` object of the requirements plus the special environment variables to locate executables
and shared libraries.


Virtualenv generator
--------------------

Conan provides a **virtualenv** generator, able to read from each dependency the :ref:`self.env_info<method_package_info_env_info>`
variables declared in the ``package_info()`` method and generate two scripts "activate" and "deactivate". These scripts set/unset all env variables in the current shell.

**Example**:

The recipe of ``cmake/3.16.3`` appends to the PATH variable the package folder/bin.

You can check existing CMake conan package versions in conan-center with:

.. code-block:: bash

    $ conan search cmake* -r=conan-center


In the **bin** folder there is a **cmake** executable:


.. code-block:: python

  def package_info(self):
    self.env_info.path.append(os.path.join(self.package_folder, "bin"))



Let's prepare a virtual environment to have cmake available in the path. Open ``conanfile.txt`` and change (or add) **virtualenv** generator:


.. code-block:: text

    [requires]
    cmake/3.16.3

    [generators]
    virtualenv

Run :command:`conan install`:

.. code-block:: bash

    $ conan install .

You can also avoid the creation of the *conanfile.txt* completely and directly do:

.. code-block:: bash

    $ conan install cmake/3.16.3 -g=virtualenv

Activate the virtual environment, and now you can run ``cmake --version`` to check that you have the installed CMake in path.


.. code-block:: bash

   $ source activate.sh # Windows: activate.bat without the source
   $ cmake --version

Two sets of scripts are available for Windows - ``activate.bat``/``deactivate.bat`` and ``activate.ps1``/``deactivate.ps1`` if you are using powershell.
Deactivate the virtual environment (or close the console) to restore the environment variables:


.. code-block:: bash

   $ source deactivate.sh # Windows: deactivate.bat without the source


.. seealso:: Read the Howto :ref:`Create installer packages<create_installer_packages>` to learn more about the virtual environment feature.
             Check the section :ref:`Reference/virtualenv<virtualenv_generator>` to see the generator reference.



Virtualbuildenv environment
---------------------------

Use the generator ``virtualbuildenv`` to activate an environment that will set the environment variables for
Autotools and Visual Studio.

The generator will create ``activate_build`` and ``deactivate_build`` files.

.. seealso:: Read More about the building environment variables defined in the sections :ref:`Building with autotools <autotools_reference>` and :ref:`Build with Visual Studio<msbuild>`.

             Check the section :ref:`Reference/virtualbuildenv<virtualbuildenv_generator>` to see the generator reference.


.. _virtual_run_environment_generator:

Virtualrunenv generator
---------------------------

Use the generator ``virtualrunenv`` to activate an environment that will:

- Append to ``PATH`` environment variable every ``bin`` folder of your requirements.
- Append to ``LD_LIBRARY_PATH`` and ``DYLD_LIBRARY_PATH`` environment variables each ``lib`` folder of  your requirements.

The generator will create ``activate_run`` and ``deactivate_run`` files. This generator is especially useful:

- If you are requiring packages with shared libraries and you are running some executable that needs those libraries.
- If you have a requirement with some tool (executable) and you need it in the path.

In the previous example of the ``cmake`` recipe, even if the cmake package doesn't declare the ``self.env_info.path`` variable,
using the virtualrunenv generator, the ``bin`` folder of the package will be available in the PATH. So after activating the virtual environment we could just run ``cmake`` in order to execute the package's cmake.


.. seealso:: - :ref:`Reference/Tools/environment_append <tools_environment_append>`
