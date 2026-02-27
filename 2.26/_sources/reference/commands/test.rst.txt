.. _reference_commands_test:

conan test
===========

.. autocommand::
    :command: conan test -h


The ``conan test`` command uses the *test_package* folder specified in ``path`` to tests the package reference specified in ``reference``.

When using the ``cmake_layout()`` functionality inside ``test_package``, the conf ``tools.cmake.cmake_layout:test_folder`` can be used
to define the location of the build artifacts for the ``test_package``. See :ref:`cmake_layout() docs<cmake_layout>`.
Likewise, the full path to the build artifacts will be defined by the ``self.folders.build_folder_vars`` attribute.


- **tools.cmake.cmake_layout:test_folder** (*new since Conan 2.2.0*)(*experimental*) uses its value as the base folder of the ``conanfile.folders.build``
  for test_package builds. If that value is ``$TMP``, Conan will create and use a temporal folder.


.. seealso::

    - Read the tutorial about :ref:`testing Conan packages <tutorial_creating_test>`.
