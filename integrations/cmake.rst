.. _integrations_cmake:

|cmake_logo| CMake
==================


Conan provides different tools to integrate with CMake in a transparent way.

Introduced in latest Conan 1.X, Conan 2.0 will use modern build system integrations like
``CMakeDeps`` and ``CMakeToolchain`` that are fully transparent CMake integration (i.e.
the consuming ``CMakeLists.txt`` doesn’t need to be aware at all about Conan). These
integrations can also achieve a better IDE integration, for example via CMakePresets.json.

Read more:

- :ref:`Tools reference <conan_tools>`

.. |cmake_logo| image:: ../images/integrations/conan-cmake-logo.png
