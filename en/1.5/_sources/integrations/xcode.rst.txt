.. _xcode:


|xcode_logo|  Apple/Xcode
_________________________


Conan can be integrated with **XCode** in two different ways:

- Using the **cmake** generator to create a **conanbuildinfo.cmake** file.
- Using the **xcode** generator to create a  **conanbuildinfo.xcconfig** file.


With CMake
----------

Check the :ref:`Integrations/cmake<cmake>` section to read about the **cmake** generator.
Check the official `CMake docs`_ to find out more about generating Xcode projects with CMake.


.. _`CMake docs`: https://cmake.org/cmake/help/v3.0/manual/cmake-generators.7.html

With the *xcode* generator
--------------------------

You can use the **xcode** generator to integrate your requirements in your *Xcode*  project.
This generator creates an ``xcconfig`` file, with all the *include paths*, *lib paths*, *libs*, *flags* etc, that can be imported in your project.


.. |xcode_logo| image:: ../images/xcode_logo.jpg


Open ``conanfile.txt`` and change (or add) the **xcode** generator:

    
.. code-block:: text

   [requires]
   Poco/1.7.8p3@pocoproject/stable
   
   [generators]
   xcode

Install the requirements:

.. code-block:: bash

   $ conan install
   
Go to your **Xcode** project, click on the project and select **Add files to**. 

.. image:: ../images/xcode1.png

Choose ``conanbuildinfo.xcconfig`` generated.

.. image:: ../images/xcode2.png

Click on the project again. In the **info/configurations** section, choose **conanbuildinfo** for *release* and *debug*.

.. image::  ../images/xcode3.png

Build your project as usual.



.. seealso:: Check the :ref:`Reference/Generators/xcode <xcode_generator>` for the complete reference.


.. seealso:: Check the :ref:`Tools section about Apple tools<tools_apple>` to ease the integration with the Apple development tools
             in your recipes using the toolchain as a :ref:`build require<build_requires>`.


.. seealso:: Check the :ref:`Darwin Toolchain package<darwin_toolchain>` section to know how to **cross build** for ``iOS``, ``watchOS`` and ``tvOS``.

