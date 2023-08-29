.. _integrations:


Integrations
============

Conan provides seamless integration with several platforms, build systems, and IDEs. Conan
brings off-the-shelf support for some of the most important operating systems, including
Windows, Linux, macOS, Android, and iOS. Some of the most important build systems
supported by Conan include CMake, MSBuild, Meson, Autotools and Make. In addition to build
systems, Conan also provides integration with popular IDEs, such as Visual Studio and
Xcode.

.. toctree::
   :maxdepth: 2

   integrations/cmake
   integrations/visual_studio
   integrations/autotools
   integrations/makefile
   integrations/xcode
   integrations/meson
   integrations/android
   integrations/jfrog

.. warning::

    Even though there's a plugin for Visual Studio IDE and another for CLion, it's not
    recommended to use them right now because they're not updated for the 2.0 version yet.
    However, we intend to resume working on these plugins and enhance their functionality
    once Conan 2.0 is released.
