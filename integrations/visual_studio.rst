.. _visual_studio:


Visual Studio
=============

|visual_logo| 


Conan can be integrated with **Visual Studio** in two different ways:

- Using **cmake** generator to create a **conanbuildinfo.cmake** file.
- Using **visual_studio** generator to create a  **conanbuildinfo.props** file.


With CMake
----------

Check the :ref:`generator<generators>` section to read about the **cmake** generator.
Check official `CMake docs`_ to know more about generating Visual Studio projects with CMake.


.. _`CMake docs`: https://cmake.org/cmake/help/v3.0/manual/cmake-generators.7.html

With *visual_studio* generator
------------------------------



You can use **visual_studio**  :ref:`generator<generators>` to manage your requirements with your *Visual Studio*  project.


.. |visual_logo| image:: ../images/visual-studio-logo.png


This generator creates a `Visual Studio project properties`_ file, with all the *include paths*, *lib paths*, *libs*, *flags* etc, that can be imported in your project.

.. _`Visual Studio project properties`: https://msdn.microsoft.com/en-us/library/669zx6zc.aspx

Open ``conanfile.txt`` and change (or add) **visual_studio** generator:

    
.. code-block:: text

   [requires]
   Poco/1.6.1@lasote/stable
   
   [generators]
   visual_studio

Install the requirements

.. code-block:: bash

   $ conan install
   
Go to your Visual Studio project, and open the **Property Manager**, usually in **View -> Other Windows -> Property Manager**.

.. image:: ../images/property_manager.png

Click the **"+"** icon and select the generated ``conanbuildinfo.props`` file:

.. image::  ../images/property_manager2.png

Build your project normally.

.. note::
    
    Remember to set your project's architecture and build type with the specified, explicitly or implicitly, by **conan install** command.
    If these values don't match you build will probably fail.

    EX: **Release/x64**    
    