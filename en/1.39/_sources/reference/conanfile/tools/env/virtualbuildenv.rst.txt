.. _conan_tools_env_virtualbuildenv:

VirtualBuildEnv
===============

.. warning::

    This is a **very experimental** feature and it will have breaking changes in future releases.


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

    from conans import ConanFile
    from conan.tools.env import VirtualBuildEnv

    class Pkg(ConanFile):
        settings = "os", "compiler", "arch", "build_type"
        requires = "zlib/1.2.11", "bzip2/1.0.8"

        def generate(self):
            ms = VirtualBuildEnv(self)
            ms.generate()

When the ``VirtualBuildEnv`` generator is used, calling :command:`conan install` will generate a *conanbuildenv* .bat or .sh script
containing environment variables of the build time environment.

That information is collected from the direct ``build_requires`` in "build" context recipes from the ``self.buildenv_info``
definition plus the ``self.runenv_info`` of the transitive dependencies of those ``build_requires``.


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
