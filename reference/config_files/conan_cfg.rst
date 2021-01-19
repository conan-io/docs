.. _conan_cfg:

conan.cfg
=========

.. warning::

    This new configuration mechanism is an **experimental** feature subject to breaking changes in future releases.


The **conan.cfg** file is located in the Conan user home directory.

Global configuration
--------------------

- ``core:required_conan_version = "expression"`` allows defining a version expression like ">=1.30". Conan will raise an error if its current version does not satisfy the condition
- ``core.package_id:msvc_visual_incompatible`` allows opting-out the fallback from the new ``msvc`` compiler to the ``Visual Studio`` compiler existing binaries



Tools configurations
--------------------

Tools and user configurations allows them to be defined both in the *conan.cfg* file and in profile files. Profile values will
have priority over globally defined ones in *conan.cfg*, and can be defined as:

.. code-block:: text

    [settings]
    ...

    [conf]
    tools.microsoft:msbuild_verbosity=Diagnostic


Existing configurations:

- ``tools.microsoft:msbuild_verbosity`` allows defining a value from ``"Quiet", "Minimal", "Normal", "Detailed", "Diagnostic"`` for build using the
  MSBuild system, it could be with the ``tools.microsoft.MSBuild`` or with the ``tools.cmake.CMake`` helpers.

