.. _global_conf:

global.conf
===========

.. warning::

    This new configuration mechanism is an **experimental** feature subject to breaking changes in future releases.


The **global.conf** file is located in the Conan user home directory.

Global configuration
--------------------

- ``core:required_conan_version = "expression"`` allows defining a version expression like ">=1.30". Conan will raise an error if its current version does not satisfy the condition
- ``core.package_id:msvc_visual_incompatible`` allows opting-out the fallback from the new ``msvc`` compiler to the ``Visual Studio`` compiler existing binaries



Tools configurations
--------------------

Tools and user configurations allows them to be defined both in the *global.conf* file and in profile files. Profile values will
have priority over globally defined ones in *global.conf*, and can be defined as:

.. code-block:: text

    [settings]
    ...

    [conf]
    tools.microsoft.msbuild:verbosity=Diagnostic
    tools.microsoft.msbuild:max_cpu_count=20
    tools.microsoft.msbuild:vs_version = 16
    tools.build:processes=10
    tools.ninja:jobs=30
    tools.gnu.make:jobs=40

Existing configurations:

- ``tools.microsoft.msbuild:verbosity`` allows defining a value from ``"Quiet", "Minimal", "Normal",
  "Detailed", "Diagnostic"`` for build using the
  MSBuild system, it could be with the ``tools.microsoft.MSBuild`` or with the ``tools.cmake.CMake``
  helpers.

- ``tools.microsoft.msbuild:max_cpu_count`` argument for the ``/m`` (``/maxCpuCount``) when running
  ``MSBuild`` standalone or via CMake (overrides the general ``tools.build:processes``).

- ``tools.microsoft.msbuild:vs_version`` defines the compiler version when using using the new ``msvc`` compiler.

- ``tools.build:processes``: number of processes to use for every build-helper.

- ``tools.ninja:jobs`` argument for the ``--jobs`` parameter when running Ninja generator via CMake
  or Meson. (overrides the general ``tools.build:processes``).

- ``tools.gnu.make:jobs``: argument for the ``--jobs`` parameter when running ``make``
  (overrides the general ``tools.build:processes``).

To list all possible configurations available, run :command:`conan config list`.
