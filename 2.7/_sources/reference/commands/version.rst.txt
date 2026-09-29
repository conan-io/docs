.. _reference_commands_version:

conan version
=============

.. include:: ../../common/experimental_warning.inc

.. autocommand::
    :command: conan version -h


The :command:`conan version` command shows information about the system and Python environment,
including Conan version, Python version, system platform, architecture, release, CPU, and more:

* **version**: The Conan version.
* **conan_path**: The path to the Conan script.
* *python*: A sub-dictionary containing information about the Python environment, including:
    * **version**: The version of Python being used.
    * **sys_version**: The full Python system version.
    * **sys_executable**: The path to the Python executable.
    * **is_frozen**: An indicator of whether the Python script is being run as a frozen file (e.g., using py2exe or PyInstaller).
    * **architecture**: The architecture detected by Python.
* *system*: A sub-dictionary containing information about the operating system, including:
    * **version**: The version of the operating system.
    * **platform**: The platform of the system.
    * **system**: The name of the operating system.
    * **release**: The release version of the operating system.
    * **cpu**: Information about the system's CPU.

.. code-block:: text

    $ conan version
    version: 2.0.6
    conan_path: /conan/venv/bin/conan
    python
      version: 3.10.4
      sys_version: 3.10.4 (main, May 17 2022, 10:53:07) [Clang 13.1.6 (clang-1316.0.21.2.3)]
      sys_executable: /conan/venv/bin/python
      is_frozen: False
      architecture: arm64
    system
      version: Darwin Kernel Version 23.4.0: Fri Mar 15 00:12:37 PDT 2024; root:xnu-10063.101.17~1/RELEASE_ARM64_T6031
      platform: macOS-14.4.1-arm64-arm-64bit
      system: Darwin
      release: 23.4.0
      cpu: arm


The :command:`conan version --format=json` returns a JSON output format in ``stdout`` (which can be redirected to a file) with the following structure:

.. code-block:: text

    $ conan version --format=json
    {
        "version": "2.0.6",
        "conan_path": "/Users/myUser/Documents/GitHub/conan/venv/bin/conan",
        "python": {
            "version": "3.10.4",
            "sys_version": "3.10.4 (main, May 17 2022, 10:53:07) [Clang 13.1.6 (clang-1316.0.21.2.3)]",
            "sys_executable": "/conan/venv/bin/python",
            "is_frozen": false,
            "architecture": "arm64"
        },
        "system": {
            "version": "Darwin Kernel Version 23.4.0: Fri Mar 15 00:12:37 PDT 2024; root:xnu-10063.101.17~1/RELEASE_ARM64_T6031",
            "platform": "macOS-14.4.1-arm64-arm-64bit",
            "system": "Darwin",
            "release": "23.4.0",
            "cpu": "arm"
        }
    }
