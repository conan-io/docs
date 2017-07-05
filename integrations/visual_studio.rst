.. _visual_studio:


|visual_logo| Visual Studio
=================================

Conan can be integrated with **Visual Studio** in two different ways:

- Using the **cmake** generator to create a **conanbuildinfo.cmake** file.
- Using the **visual_studio** generator to create a  **conanbuildinfo.props** file.


With CMake
----------

Check the :ref:`generator<generators>` section to read about the **cmake** generator.
Check the official `CMake docs`_ to find out more about generating Visual Studio projects with CMake.


.. _`CMake docs`: https://cmake.org/cmake/help/v3.0/manual/cmake-generators.7.html

With *visual_studio* generator
------------------------------

You can use the **visual_studio** generator to manage your requirements via your *Visual Studio*  project.


.. |visual_logo| image:: ../images/visual-studio-logo.png


This generator creates a `Visual Studio project properties`_ file, with all the *include paths*, *lib paths*, *libs*, *flags* etc, that can be imported in your project.

.. _`Visual Studio project properties`: https://msdn.microsoft.com/en-us/library/669zx6zc.aspx

Open ``conanfile.txt`` and change (or add) the **visual_studio** generator:

    
.. code-block:: text

   [requires]
   Poco/1.7.8p3@pocoproject/stable
   
   [generators]
   visual_studio

Install the requirements:

.. code-block:: bash

   $ conan install
   
Go to your Visual Studio project, and open the **Property Manager**, usually in **View -> Other Windows -> Property Manager**.

.. image:: ../images/property_manager.png

Click the **"+"** icon and select the generated ``conanbuildinfo.props`` file:

.. image::  ../images/property_manager2.png

Build your project as usual.

.. note::
    
    Remember to set your project's architecture and build type accordingly, explicitly or implicitly, when issuing the **conan install** command.
    If these values don't match, you build will probably fail.

    e.g. **Release/x64**    


.. seealso:: Check the :ref:`Reference/Generators/visual_studio <visualstudio_generator>` for the complete reference.



Calling Visual Studio compiler
------------------------------

You can call your Visual Studio compiler from your ``build()`` method using the ``VisualStudioBuildEnvironment``
and the ``tools.vcvars_command``.

Check :ref:`Build Automation/Building with Visual Studio<building_with_visual_studio>` section for more info.



.. _building_visual_project:

Build an existing Visual Studio project
---------------------------------------

You can build an existing Visual Studio from your ``build()`` method using the ``tools.build_sln_command``.


.. seealso:: Check the :ref:`tools.build_sln_command()<build_sln_commmand>` reference section for more info.

