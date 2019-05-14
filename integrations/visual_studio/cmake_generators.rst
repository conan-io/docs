

|visual_logo| Visual Studio integration (CMake)
===============================================

.. container:: out_reference_box

    Learn about other ways to integrate with Visual Studio in the
    :ref:`Integrations/Visual Studio<visual_studio>` section.


CMake generators
----------------

Use one of the :ref:`CMake generators provided by Conan <cmake>` and then create the Visual
Studio solution using the proper generator by CMake:

.. code-block:: bash

    cmake <path/to/CMakeLists.txt> -G "Visual Studio 16 2019"

Have a look to the `CMake documentation`_ to know which are the names of the generators and which
ones are available for your CMake version.

However, beware of some current CMake limitations, such as not dealing well with find-packages,
because CMake doesn't know how to handle finding both debug and release packages.


CMake integration (Visual Studio 2017 or superior)
--------------------------------------------------

Starting from Visual Studio 2017, the IDE by Microsoft includes a direct integration with CMake
that allows to open a folder that contains a *CMakeLists.txt* file and Visual Studio will use
it to define the project build.

Read all about this integration in :ref:`this how-to<visual2017_cmake_howto>`.

.. |visual_logo| image:: ../../images/visual-studio-logo.png
                 :width: 100 px
                 :alt: Visual Studio logo

.. _`CMake documentation`: https://cmake.org/cmake/help/v3.14/manual/cmake-generators.7.html