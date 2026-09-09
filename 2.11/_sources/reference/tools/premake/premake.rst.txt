.. _conan_tools_premake_premake:

Premake
=======

.. include:: ../../../common/experimental_warning.inc


The ``Premake`` build helper is a wrapper around the command line invocation of Premake. It will abstract the
project configuration command.

The helper is intended to be used in the *conanfile.py* ``build()`` method, to call Premake commands automatically
when a package is being built directly by Conan (create, install)


.. code-block:: python

    from conan.tools.premake import Premake
    from conan.tools.microsoft import MSBuild

    class Pkg(ConanFile):
        settings = "os", "compiler", "build_type", "arch"

        # The VCVars generator might be needed in Windows-MSVC
        generators = "VCVars"

        def build(self):
            p = Premake(self)
            p.configure()
            # At the moment Premake does not contain .build() method
            # report in Github issues your use cases and feedback to request it
            build_type = str(self.settings.build_type)
            if self.settings.os == "Windows":
                msbuild = MSBuild(self)
                msbuild.build("HelloWorld.sln")
            else:
                self.run(f"make config={build_type.lower()}_x86_64")
            p = os.path.join(self.build_folder, "bin", build_type, "HelloWorld")
            self.run(f'"{p}"')
