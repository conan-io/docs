.. _cmake_other_generators:

Ninja, NMake, Borland
=========================

These build systems still don't have a Conan generator for using them natively. However, if
you are using cmake, you can instruct Conan to use them instead of the default generator
(typically ``Unix Makefiles``) defining the environment variable ``CONAN_CMAKE_GENERATOR``.

Read more about this variable in :ref:`env_vars`.
