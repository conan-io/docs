.. _conan_tools_ros_rosenv:

ROSEnv
======

The ``ROSEnv`` generator is an environment generator that, in conjuction with :ref:`CMakeDeps <conan_tools_cmakedeps>`
and :ref:`CMakeToolchain <conan_tools_cmaketoolchain>`, allows to consume Conan packages from a ROS package.

.. code-block:: text
    :caption: conanfile.txt

    [requires]
    fmt/11.0.2

    [generators]
    CMakeDeps
    CMakeToolchain
    ROSEnv

This generator will create a `conanrosenv.sh` script with the required environment variables that allow CMake and Colcon
to locate the pacckages installed by Conan.

This script needs to be *sourced* before the :command:`colcon build` command:

.. code-block:: bash

    $ cd workspace
    $ conan install ...
    $ source conanrosenv.sh
    $ colcon build


Reference
---------

.. currentmodule:: conan.tools.ros

.. autoclass:: ROSEnv
    :members:
