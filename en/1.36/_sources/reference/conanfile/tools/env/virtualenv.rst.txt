VirtualEnv
==========

.. warning::

    This is a **very experimental** feature and it will have breaking changes in future releases.


The ``VirtualEnv`` generator can be used by name in conanfiles:

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):
        generators = "VirtualEnv"

.. code-block:: text
    :caption: conanfile.txt

    [generators]
    VirtualEnv

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code-block:: python
    :caption: conanfile.py

    from conans import ConanFile
    from conan.tools.env import VirtualEnv

    class Pkg(ConanFile):
        settings = "os", "compiler", "arch", "build_type"
        requires = "zlib/1.2.11", "bzip2/1.0.8"

        def generate(self):
            ms = VirtualEnv(self)
            ms.generate()

When the ``VirtualEnv`` generator is used, calling ``conan install`` will generate files containing environment variables information:


- *conanbuildenv* .bat or .sh scripts, that are automatically loaded if existing by the ``self.run()`` recipes methods. *conanbuildenv* is the build time environment information. It is collected from the direct ``build_requires`` in "build" context recipes from the ``self.buildenv_info`` definition plus the ``self.runenv_info`` of the transitive dependencies of those ``build_requires``.
- *conanrunenv* .bat or .sh scripts, that can be explicitly opted-in in ``self.run()`` recipes methods with ``self.run(..., env=["conanrunenv"])``. *conanrunenv* is the runtime environment information, anything that is necessary in the environment to actually run the compiled executables and applications.
- In both cases, whenever the runtime environment information is necessary, it wil also be automatically deduced from the ``self.cpp_info`` definition of the package, to define ``PATH``, ``LD_LIBRARY_PATH``, ``DYLD_LIBRARY_PATH`` and ``DYLD_FRAMEWORK_PATH`` environment variables.
