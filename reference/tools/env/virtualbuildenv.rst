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
        requires = "zlib/1.3.1", "bzip2/1.0.8"

        def generate(self):
            ms = VirtualBuildEnv(self)
            ms.generate()


Note that instantiating the ``VirtualBuildEnv()`` generator without later calling the ``generate()`` method,
which is intended only for the ``generate()`` recipe method, will inhibit the creation of environment files.

So something like:

.. code-block:: python

    ms = VirtualBuildEnv(self)
    my_env_var = ms.vars().get("MY_ENV_VAR")
    # does not create conanbuildenv.sh|.bat files


will stop creating the ``conanbuild.sh|.bat`` and ``conanbuildenv.sh|.bat`` files that are created by default,
even when ``VirtualBuildEnv`` is not instantiated.

In order to keep creating those files, the ``auto_generate=True`` argument can be passed to the constructor, as:

.. code-block:: python

    ms = VirtualBuildEnv(self, auto_generate=True)
    my_env_var = ms.vars().get("MY_ENV_VAR")
    # does create conanbuildenv.sh|.bat files



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

    To create ``.ps1`` files required for PowerShell, you need to set the
    ``tools.env.virtualenv:powershell`` configuration with the value of the PowerShell
    executable (e.g., ``powershell.exe`` or ``pwsh``). Note that, setting it to ``True``
    or ``False`` is deprecated as of Conan 2.11.0 and should no longer be used.


.. note::

    To create ``.env`` dotenv files, use the **experimental** (new in Conan 2.21) ``tools.env:dotenv`` configuration.
    These files are not intended to be activated as scripts, but loaded by tools such as IDEs.
    The configuration specific files such as ``conanbuildenv-Release.env`` will be generated, as the
    environment can be different for Release and Debug configurations.
    These files at the moment do not use variable interpolation due to some VScode limitations, 
    a warning is printed pointing to https://github.com/microsoft/vscode-cpptools/issues/13781 to
    track progress. 
    Please open a Github ticket to report any feedback about this feature.



.. _reference_tools_env_virtualbuildenv_disable:

Disabling VirtualBuildEnv
-------------------------

It is possible to disable the generation of the ``VirtualBuildEnv`` and ``VirtualRunEnv`` files with 
different mechanisms:

- By passing ``--envs-generation=false`` to the ``conan install`` command, it will disable the generation
  of environment files (both ``VirtualBuildEnv`` and ``VirtualRunEnv``) for the current consumer only
  (dependencies that need to be built from source will generate their own environment files as needed).
  **This feature is experimental and subject to change**.
- Recipes can instantiate a ``VirtualBuildEnv(self)`` in their ``generate()`` method, without calling
  their ``generate()`` method. That will inhibit the creation of environment files for that specific
  recipe:

  .. code-block:: python

    def generate(self):
        VirtualBuildEnv(self)
        # do not call its generate() method
        # discouraged, in most cases, it is desired
        # to call generate()
        VirtualRunEnv(self)
        # Same for VirtualRunEnv

- Recipes can directly define their ``virtualbuildenv = False`` attribute to inhibit the automatic
  default creation of ``VirtualBuildEnv`` files for this recipe:

  .. code-block:: python

    class Pkg(ConanFile):
        virtualbuildenv = False
        # Also for VirtualRunEnv
        virtualrunenv = False


.. warning::

    In general, disabling the generation of environment files is **discouraged**. Environment files are the
    mechanism use for things like ``[tool_requires]`` defined in the profiles to be able to inject those 
    tools dynamically in dependencies, even if those dependencies didn't directly declare such 
    ``tool_requires``. Without proper ``VirtualBuildEnv`` files in the recipe, the ``tool_requires`` will
    fail to apply.


Reference
---------

.. currentmodule:: conan.tools.env.virtualbuildenv

.. autoclass:: VirtualBuildEnv
    :members:
