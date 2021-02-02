.. _cmake_other_generators:

Ninja, NMake, Borland
=========================

These build systems still don't have a Conan generator for using them natively. However, if
you are using CMake, you can instruct Conan to use them instead of the default generator
(typically ``Unix Makefiles``).

Set it globally in your *conan.conf* file:

.. code-block:: bash

    $ conan config set general.cmake_generator=Ninja

or use the environment variable :ref:`CONAN_CMAKE_GENERATOR <env_vars>`.
