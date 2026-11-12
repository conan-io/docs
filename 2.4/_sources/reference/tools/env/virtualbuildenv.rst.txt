.. _conan_tools_env_virtualbuildenv:

VirtualBuildEnv
===============

VirtualBuildEnv is a generator that produces a *conanbuildenv* .bat, .ps1 or .sh script containing the environment variables
of the build time context:

    - From the ``self.buildenv_info`` of the direct ``tool_requires`` in "build" context.
    - From the ``self.runenv_info`` of the transitive dependencies of those ``tool_requires``.


It can be used by name in conanfiles:

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):
        generators = "VirtualBuildEnv"


.. code-block:: text
    :caption: conanfile.txt

    [generators]
    VirtualBuildEnv

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code-block:: python
    :caption: conanfile.py

    from conan import ConanFile
    from conan.tools.env import VirtualBuildEnv

    class Pkg(ConanFile):
        settings = "os", "compiler", "arch", "build_type"
        requires = "zlib/1.2.11", "bzip2/1.0.8"

        def generate(self):
            ms = VirtualBuildEnv(self)
            ms.generate()



Generated files
---------------

This generator (for example the invocation of ``conan install --tool-require=cmake/3.20.0@ -g VirtualBuildEnv``)
will create the following files:

- conanbuildenv-release-x86_64.(bat|ps1|sh): This file contains the actual definition of environment variables
  like PATH, LD_LIBRARY_PATH, etc, and any other variable defined in the dependencies ``buildenv_info``
  corresponding to the ``build`` context, and to the current installed
  configuration. If a repeated call is done with other settings, a different file will be created.
  After the execution or sourcing of this file, a new deactivation script will be generated, capturing the current
  environment, so the environment can be restored when desired. The file will be named also following the
  current active configuration, like ``deactivate_conanbuildenv-release-x86_64.bat``.
- conanbuild.(bat|ps1|sh): Accumulates the calls to one or more other scripts, in case there are multiple tools
  in the generate process that create files, to give one single convenient file for all. This only calls
  the latest specific configuration one, that is, if ``conan install`` is called first for Release build type,
  and then for Debug, ``conanbuild.(bat|ps1|sh)`` script will call the Debug one.
- deactivate_conanbuild.(bat|ps1|sh): Accumulates the deactivation calls defined in the above ``conanbuild.(bat|ps1|sh)``.
  This file should only be called after the accumulated activate has been called first.

.. note::

    To create ``.ps1`` files required for Powershell it is necessary to set to True the following conf: ``tools.env.virtualenv:powershell``.

Reference
---------

.. currentmodule:: conan.tools.env.virtualbuildenv

.. autoclass:: VirtualBuildEnv
    :members:
