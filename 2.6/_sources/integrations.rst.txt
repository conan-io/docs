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
   integrations/clion
   integrations/visual_studio
   integrations/autotools
   integrations/bazel
   integrations/makefile
   integrations/xcode
   integrations/meson
   integrations/android
   integrations/jfrog

.. warning::

    Even though there is a plugin for the Visual Studio IDE, it is not recommended to use
    it right now because it has not been updated for the 2.0 version yet. However, we
    intend to resume working on this plugin and enhance its functionality soon after Conan 2.0
    is released.
