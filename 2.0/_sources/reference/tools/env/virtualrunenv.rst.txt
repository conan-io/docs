.. _conan_tools_env_virtualrunenv:

VirtualRunEnv
=============

``VirtualRunEnv`` is a generator that produces a launcher *conanrunenv* .bat, .ps1 or .sh script containing environment variables
of the run time environment.

The launcher contains the runtime environment information, anything that is necessary in the environment to actually run
the compiled executables and applications. The information is obtained from:

    - The ``self.runenv_info`` of the dependencies corresponding to the ``host`` context.
    - Also automatically deduced from the ``self.cpp_info`` definition of the package, to define ``PATH``,
      ``LD_LIBRARY_PATH``, ``DYLD_LIBRARY_PATH`` and ``DYLD_FRAMEWORK_PATH`` environment variables.

It can be used by name in conanfiles:

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):
        generators = "VirtualRunEnv"

.. code-block:: text
    :caption: conanfile.txt

    [generators]
    VirtualRunEnv

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code-block:: python
    :caption: conanfile.py

    from conan import ConanFile
    from conan.tools.env import VirtualRunEnv

    class Pkg(ConanFile):
        settings = "os", "compiler", "arch", "build_type"
        requires = "zlib/1.2.11", "bzip2/1.0.8"

        def generate(self):
            ms = VirtualRunEnv(self)
            ms.generate()



Generated files
---------------

- conanrunenv-release-x86_64.(bat|ps1|sh): This file contains the actual definition of environment variables
  like PATH, LD_LIBRARY_PATH, etc, and ``runenv_info`` of dependencies corresponding to the ``host`` context,
  and to the current installed configuration. If a repeated call is done with other settings, a different file will be created.
- conanrun.(bat|ps1|sh): Accumulates the calls to one or more other scripts to give one single convenient file
  for all. This only calls the latest specific configuration one, that is, if ``conan install`` is called first for Release build type,
  and then for Debug, ``conanrun.(bat|ps1|sh)`` script will call the Debug one.

After the execution of one of those files, a new deactivation script will be generated, capturing the current
environment, so the environment can be restored when desired. The file will be named also following the
current active configuration, like ``deactivate_conanrunenv-release-x86_64.bat``.

.. note::

    To create ``.ps1`` files required for Powershell it is necessary to set to True the following conf: ``tools.env.virtualenv:powershell``.

Reference
---------

.. currentmodule:: conan.tools.env.virtualrunenv

.. autoclass:: VirtualRunEnv
    :members:
