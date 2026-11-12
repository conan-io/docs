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



Constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile):

- ``conanfile``: the current recipe object. Always use ``self``.


generate()
++++++++++

.. code:: python

    def generate(self, auto_activate=True):


Parameters:

    * **auto_activate** (Defaulted to ``True``): Add the launcher automatically to the ``conanenv`` launcher. Read more
      in the :ref:`Environment documentation <conan_tools_env_environment_model>`.
