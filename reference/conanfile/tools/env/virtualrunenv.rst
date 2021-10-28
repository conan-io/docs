.. _conan_tools_env_virtualrunenv:

VirtualRunEnv
===============

.. warning::

    This is a **very experimental** feature and it will have breaking changes in future releases.


The ``VirtualRunEnv`` generator can be used by name in conanfiles:

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

    from conans import ConanFile
    from conan.tools.env import VirtualRunEnv

    class Pkg(ConanFile):
        settings = "os", "compiler", "arch", "build_type"
        requires = "zlib/1.2.11", "bzip2/1.0.8"

        def generate(self):
            ms = VirtualRunEnv(self)
            ms.generate()

When the ``VirtualRunEnv`` generator is used, calling :command:`conan install` will generate a *conanrunenv* .bat or .sh script
containing environment variables of the run time environment.

The launcher contains the runtime environment information, anything that is necessary in the environment to actually run
the compiled executables and applications. The information is obtained from the ``self.runenv_info`` and also automatically
deduced from the ``self.cpp_info`` definition of the package, to define ``PATH``, ``LD_LIBRARY_PATH``, ``DYLD_LIBRARY_PATH``
and ``DYLD_FRAMEWORK_PATH`` environment variables.

This generator will create the following files:

- conanrunenv-release-x86_64.(bat|sh): This file contains the actual definition of environment variables
  like PATH, LD_LIBRARY_PATH, etc, and ``runenv_info`` of dependencies corresponding to the ``host`` context,
  and to the current installed configuration. If a repeated call is done with other settings, a different file will be created.
- conanrun.(bat|sh): Accumulates the calls to one or more other scripts to give one single convenient file
  for all. This only calls the latest specific configuration one, that is, if ``conan install`` is called first for Release build type,
  and then for Debug, ``conanrun.(bat|sh)`` script will call the Debug one.

After the execution of one of those files, a new deactivation script will be generated, capturing the current
environment, so the environment can be restored when desired. The file will be named also following the
current active configuration, like ``deactivate_conanrunenv-release-x86_64.bat``.


Constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile):

- ``conanfile``: the current recipe object. Always use ``self``.


generate()
++++++++++

.. code:: python

    def generate(self, scope="run"):


Parameters:

    * **scope** (Defaulted to ``run``): Add the launcher automatically to the ``conanrun`` launcher. Read more
      in the :ref:`Environment documentation <conan_tools_env_environment_model>`.
