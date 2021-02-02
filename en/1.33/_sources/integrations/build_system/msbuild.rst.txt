.. _msbuild_integration:


|visual_logo| MSBuild (Visual Studio)
=====================================

If you are using CMake to generate your Visual Studio projects, this is not the right section, go to :ref:`cmake` instead.
This section is about native integration with Microsoft MSBuild, using properties files.

Conan can be integrated with **MSBuild** natively, the build system of Visual Studio in different ways:


- Using the ``conan.tools.microsoft`` tools: ``MSBuildDeps``, ``MSBuildToolchain`` and ``MSBuild`` helpers to generate properties
  files for your project, containing information about the project dependencies and toolchain. This is the new integration that is
  experimental but will become the standard one in Conan 2.0. Go to :ref:`conan_tools_microsoft` for more information.
- Using the ``visual_studio`` or ``visual_studio_multi`` generators to create a MSBuild properties *conanbuildinfo.props* file.
  This is the older integration, it is more stable now, but it wil be deprecated and removed in Conan 2.0. Keep reading this page for more information.


With *visual_studio* generator
------------------------------

Use the **visual_studio** generator, or **visual_studio_multi**, if you are maintaining your Visual Studio projects, and want to use Conan to to tell Visual Studio how to find your third-party dependencies.

You can use the **visual_studio** generator to manage your requirements via your *Visual Studio*  project.


This generator creates a `Visual Studio project properties`_ file, with all the *include paths*, *lib paths*, *libs*, *flags* etc., that can be imported in your project.

Open ``conanfile.txt`` and change (or add) the ``visual_studio`` generator:

.. code-block:: text

    [requires]
    poco/1.9.4

    [generators]
    visual_studio

Install the requirements:

.. code-block:: bash

    $ conan install .

Go to your Visual Studio project, and open the **Property Manager** (usually in **View -> Other Windows -> Property Manager**).

.. image:: ../../images/conan-property_manager.png

Click the **+** icon and select the generated ``conanbuildinfo.props`` file:

.. image:: ../../images/conan-property_manager2.png

Build your project as usual.

.. note::

    Remember to set your project's architecture and build type accordingly, explicitly or implicitly, when issuing the
    :command:`conan install` command. If these values don't match, your build will probably fail.

    e.g. **Release/x64**

.. seealso::

    Check :ref:`visualstudio_generator` for the complete reference.

.. _building_visual_project:

Build an existing Visual Studio project
---------------------------------------

You can build an existing Visual Studio from your ``build()`` method using the :ref:`MSBuild()<msbuild>` build helper.

.. code-block:: python

    from conans import ConanFile, MSBuild

    class ExampleConan(ConanFile):
        ...

        def build(self):
            msbuild = MSBuild(self)
            msbuild.build("MyProject.sln")

Toolsets
--------

You can use the sub-setting ``toolset`` of the Visual Studio compiler to specify a custom toolset.
It will be automatically applied when using the ``CMake()`` and ``MSBuild()`` build helpers.
The toolset can also be specified manually in these build helpers with the ``toolset`` parameter.

By default, Conan will not generate a new binary package if the specified ``compiler.toolset``
matches an already generated package for the corresponding ``compiler.version``.
Check the :ref:`package_id()<method_package_id>` reference to learn more.

.. seealso::

    Check the :ref:`CMake()<cmake_reference>` reference section for more info.


.. _`CMake docs`: https://cmake.org/cmake/help/v3.0/manual/cmake-generators.7.html
.. |visual_logo| image:: ../../images/conan-visual-studio-logo.png
.. _`Visual Studio project properties`: https://docs.microsoft.com/en-us/visualstudio/ide/managing-project-and-solution-properties?view=vs-2017
