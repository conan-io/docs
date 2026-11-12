.. _conan_tools_premake_premake:

Premake
=======

.. include:: ../../../common/experimental_warning.inc


The ``Premake`` build helper is a wrapper around the command line invocation of Premake. It will abstract the
project configuration and build command.

The helper is intended to be used in the *conanfile.py* ``build()`` method, to call Premake commands automatically
when a package is being built directly by Conan (create, install)

**Usage Example:**

.. code-block:: python

    from conan.tools.premake import Premake

    class Pkg(ConanFile):
        settings = "os", "compiler", "build_type", "arch"

        # The PremakeToolchain generator is always needed to use premake helper
        generators = "PremakeToolchain"

        def build(self):
            p = Premake(self)

            # Set the main Lua configuration file (default: premake5.lua)
            p.luafile = "myproject.lua"

            # Pass custom arguments to Premake (translates to --{key}={value})
            p.arguments["myarg"] = "myvalue"

            # Automatically determines the correct action:
            # - For MSVC, selects vs<version> based on the compiler version
            # - Defaults to "gmake" for other compilers
            # p.configure() will run: premake5 --file=myproject.lua <action> --{key}={value} ...
            p.configure()
            # p.build() will invoke proper compiler depending on action (automatically detected by profile)
            p.build("HelloWorld.sln")

Reference
---------

.. currentmodule:: conan.tools.premake

.. autoclass:: Premake
    :members:

conf
----

The ``Premake`` build helper is affected by these ``[conf]`` variables:

- ``tools.build:verbosity`` which accepts one of ``quiet`` or ``verbose`` and sets the ``--quiet`` flag in ``Premake.configure()``

- ``tools.compilation:verbosity`` which accepts one of ``quiet`` or ``verbose`` and sets the ``--verbose`` flag in ``Premake.build()``

Extra configuration
-------------------

By default, typical Premake configurations are ``Release`` and ``Debug``. 
This configurations could vary depending on the used Premake script.

For example,

.. code-block:: lua

    workspace "MyProject"
        configurations { "Debug", "Release", "DebugDLL", "ReleaseDLL" }

If you wish to use a different configuration than ``Release`` or ``Debug``, you can override the configuration from the ``Premake`` generator.

If the project also have dependencies, you will also need to override the
``configuration`` property of the ``PremakeDeps`` generator accordingly, with the same value.

.. code-block:: python

    class MyRecipe(Conanfile):
        ...
        def _premake_configuration(self):
            return str(self.settings.build_type) + ("DLL" if self.options.shared else "") 

        def generate(self):
            deps = PremakeDeps(self)
            deps.configuration = self._premake_configuration
            deps.generate()
            tc = PremakeToolchain(self)
            tc.generate()

        def build(self):
            premake = Premake(self)
            premake.configure()
            premake.build(workspace="MyProject", configuration=self._premake_configuration)
