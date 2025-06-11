.. _conan_tools_env_virtualbuildenv:

VirtualBuildEnv
===============

.. warning::

    These tools are still **experimental** (so subject to breaking changes) but with very stable syntax.
    We encourage the usage of it to be prepared for Conan 2.0.

Available since: `1.39.0 <https://github.com/conan-io/conan/releases/tag/1.39.0>`_

The ``VirtualBuildEnv`` generator can be used by name in conanfiles:

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

When the ``VirtualBuildEnv`` generator is used, calling :command:`conan install` will generate a *conanbuildenv* .bat or .sh script
containing environment variables of the build time environment.

That information is collected from the direct ``tool_requires`` in "build" context recipes from the ``self.buildenv_info``
definition plus the ``self.runenv_info`` of the transitive dependencies of those ``tool_requires``.


This generator (for example the invocation of ``conan install cmake/3.20.0@ -g VirtualBuildEnv --build-require``)
will create the following files:

- conanbuildenv-release-x86_64.(bat|sh): This file contains the actual definition of environment variables
  like PATH, LD_LIBRARY_PATH, etc, and any other variable defined in the dependencies ``buildenv_info``
  corresponding to the ``build`` context, and to the current installed
  configuration. If a repeated call is done with other settings, a different file will be created.
  After the execution or sourcing of this file, a new deactivation script will be generated, capturing the current
  environment, so the environment can be restored when desired. The file will be named also following the
  current active configuration, like ``deactivate_conanbuildenv-release-x86_64.bat``.
- conanbuild.(bat|sh): Accumulates the calls to one or more other scripts, in case there are multiple tools
  in the generate process that create files, to give one single convenient file for all. This only calls
  the latest specific configuration one, that is, if ``conan install`` is called first for Release build type,
  and then for Debug, ``conanbuild.(bat|sh)`` script will call the Debug one.
- deactivate_conanbuild.(bat|sh): Accumulates the deactivation calls defined in the above ``conanbuild.(bat|sh)``.
  This file should only be called after the accumulated activate has been called first.


Constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile):

- ``conanfile``: the current recipe object. Always use ``self``.


generate()
++++++++++

.. code:: python

    def generate(self, scope="build"):


Parameters:

    * **scope** (Defaulted to ``"build"``): Add the launcher automatically to the ``conanbuild`` launcher. Read more
      in the :ref:`Environment documentation <conan_tools_env_environment_model>`.
