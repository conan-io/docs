.. _visual_studio:


|visual_logo| Visual Studio
===========================

Conan can be integrated with **Visual Studio** in two different ways:

- Using the ``cmake`` generator to create a *conanbuildinfo.cmake* file.
- Using the ``visual_studio`` generator to create a *conanbuildinfo.props* file.

With CMake
----------

Use the ``cmake`` generator or ``cmake_multi`` if you are using CMake to machine-generate your Visual Studio projects.

Check the :ref:`generators` section to read about the ``cmake`` generator.
Check the official `CMake docs`_ to find out more about generating Visual Studio projects with CMake.

However, beware of some current CMake limitations, such as not dealing well with find-packages, because CMake doesn't know how to handle finding both debug and release packages.

.. note::

    If you want to use the Visual Studio 2017 + CMake integration, :ref:`check this how-to<visual2017_cmake_howto>`

With *visual_studio* generator
------------------------------

Use the **visual_studio** generator, or **visual_studio_multi**, if you are maintaining your Visual Studio projects, and want to use Conan to to tell Visual Studio how to find your third-party dependencies.

You can use the **visual_studio** generator to manage your requirements via your *Visual Studio*  project.


This generator creates a `Visual Studio project properties`_ file, with all the *include paths*, *lib paths*, *libs*, *flags* etc., that can be imported in your project.

Open ``conanfile.txt`` and change (or add) the ``visual_studio`` generator:

.. code-block:: text

    [requires]
    Poco/1.7.8p3@pocoproject/stable

    [generators]
    visual_studio

Install the requirements:

.. code-block:: bash

    $ conan install .

Go to your Visual Studio project, and open the **Property Manager** (usually in **View -> Other Windows -> Property Manager**).

.. image:: ../images/property_manager.png

Click the **+** icon and select the generated ``conanbuildinfo.props`` file:

.. image:: ../images/property_manager2.png

Build your project as usual.

.. note::

    Remember to set your project's architecture and build type accordingly, explicitly or implicitly, when issuing the
    :command:`conan install` command. If these values don't match, your build will probably fail.

    e.g. **Release/x64**

.. seealso::

    Check :ref:`visualstudio_generator` for the complete reference.

Calling Visual Studio compiler
------------------------------

You can call the Visual Studio compiler from your ``build()`` method using the ``VisualStudioBuildEnvironment`` and the
:ref:`tools_vcvars_command`.

Check the :ref:`msbuild` section for more info.

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
.. |visual_logo| image:: ../images/visual-studio-logo.png
.. _`Visual Studio project properties`: https://docs.microsoft.com/en-us/visualstudio/ide/managing-project-and-solution-properties?view=vs-2017
