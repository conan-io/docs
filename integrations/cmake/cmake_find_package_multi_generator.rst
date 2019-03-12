
.. _cmake_find_package_multi_generator:


``cmake_find_package_multi`` generator
======================================

This generator is similar to the :ref:`cmake_find_package<cmake_find_package_generator>` generator but it allows to work with
multi-configuration projects like ``Visual Studio`` with both ``Debug`` and ``Release``.


Usage
-----

.. code-block:: bash

    $ conan install . -g cmake_find_package_multi -s build_type=Debug
    $ conan install . -g cmake_find_package_multi -s build_type=Release

These commands will generate 3 files for each dependency in your graph:

- ``FindXXX.cmake``: This file will be found by the cmake ``find_package(XXX)`` function. It includes the following files and prepare both
  the targets and the global variables (for the old global CMake approach) for the package ``XXX``.
- ``FindXXX-Release.cmake``: This will contain all the variables and targets for the ``Release`` configuration for the ``XXX`` package.
- ``FindXXX-Debug.cmake``: This will contain all the variables and targets for the ``Release`` configuration for the ``XXX`` package.


The name of the files follows the pattern ``Find<package_name>.cmake``. So for the ``zlib/1.2.11@conan/stable`` package,
a ``Findzlib.cmake`` file will be generated.


.. seealso::

    Check the section :ref:`cmake_cmake_find_package_multi_generator_reference` to read more about this generator and the adjusted CMake
    variables/targets.
