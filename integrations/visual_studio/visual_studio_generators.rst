

|visual_logo| Visual Studio integration (*.props* file)
=======================================================

.. container:: out_reference_box

    Learn about other ways to integrate with Visual Studio in the
    :ref:`Integrations/Visual Studio<visual_studio>` section.


Visual Studio generators
------------------------

Use the **visual_studio** generator, or **visual_studio_multi**, if you are maintaining your
Visual Studio projects, and want to use Conan to to tell Visual Studio how to find your
third-party dependencies. (For old versions of Visual Studio check :ref:`visualstudiolegacy_generator`.)

You can use the **visual_studio** generator to manage your requirements via your
*Visual Studio*  project.


This generator creates a `Visual Studio project properties`_ file, with all the
*include paths*, *lib paths*, *libs*, *flags* etc., that can be imported in your project.

Open *conanfile.txt* and change (or add) the ``visual_studio`` generator:

.. code-block:: text

    [requires]
    Poco/1.7.8p3@pocoproject/stable

    [generators]
    visual_studio

Install the requirements:

.. code-block:: bash

    $ conan install .

Go to your Visual Studio project, and open the **Property Manager** (usually
in **View -> Other Windows -> Property Manager**).

.. image:: ../../images/property_manager.png

Click the **+** icon and select the generated *conanbuildinfo.props* file:

.. image:: ../../images/property_manager2.png

Build your project as usual.

.. note::

    Remember to set your project's architecture and build type accordingly, explicitly or
    implicitly, when issuing the :command:`conan install` command. If these values don't match,
    your build will probably fail.

    e.g. **Release/x64**

.. seealso::

    Check :ref:`visualstudio_generator` for the complete reference about the generator.



.. |visual_logo| image:: ../../images/visual-studio-logo.png
                 :width: 100 px
                 :alt: Visual Studio logo
.. _`Visual Studio project properties`: https://docs.microsoft.com/en-us/visualstudio/ide/managing-project-and-solution-properties?view=vs-2017
