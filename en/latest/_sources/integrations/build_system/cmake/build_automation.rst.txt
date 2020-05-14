
Build automation
================

You can invoke CMake from your conanfile.py file and automate the build of your library/project.
Conan provides a ``CMake()`` helper. This helper is useful in calling the ``cmake`` command both for creating Conan packages
or automating your project build with the :command:`conan build .` command. The ``CMake()`` helper will take into account
your settings in order to automatically set definitions and a generator according to your compiler, build_type, etc.

.. seealso:: Check the section :ref:`Building with CMake<cmake_reference>`.
