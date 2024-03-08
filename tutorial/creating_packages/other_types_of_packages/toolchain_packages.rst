.. _tutorial_other_toolchain_packages:


Creating a package for a toolchain
==================================

After learning how to create recipes for tool requires packaging applications we can use
during the build we are coing to show an example on how to create a recipe that packages a
precompiled toolchain or compiler for building other packages.

In the section ":ref:`consuming_packages_cross_building_with_conan`", we discussed the
basics of cross-compiling applications using Conan with a focus on the "build" and "host"
contexts. We learned how to configure Conan to use different profiles for the build
machine and the target host machine, enabling us to cross-compile applications for
platforms like Raspberry Pi from an Ubuntu Linux machine.

However, in that section, we assumed the existence of a cross-compiling toolchain or
compiler as part of the build environment, set up through Conan profiles. Now, we will
take a step further by demonstrating how to create a Conan package for such a toolchain.
This package can then be used as a `tool_require` in other Conan recipes, simplifying the
process of setting up the environment for cross-compilation.

Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/other_packages/toolchain_packages/toolchain

Here, you will find a conan recipe (and the *test_package*) to package an ARM toolchain for cross-compiling
to Linux ARM for both 32 and 64 bits. To simplify a bit, we are assuming that we can just
cross-build from Linux x86_64 to Linux ARM, both 32 and 64 bits. 

.. code-block:: bash

    .
    ├── conanfile.py
    └── test_package
        ├── CMakeLists.txt
        ├── conanfile.py
        └── test_package.cpp


Let's check the recipe and go through the most relevant parts:


.. code-block:: python
    :caption: conanfile.py

    import os
    from conan import ConanFile
    from conan.tools.files import get, copy, download
    from conan.errors import ConanInvalidConfiguration
    from conan.tools.scm import Version

    class ArmToolchainPackage(ConanFile):
        name = "arm-toolchain"
        version = "13.2"
        ...
        settings = "os", "arch"
        package_type = "application"

        def _archs32(self):
            return ["armv6", "armv7", "armv7hf"]
        
        def _archs64(self):
            return ["armv8", "armv8.3"]

        def _get_toolchain(self, target_arch):
            if target_arch in self._archs32():
                return ("arm-none-linux-gnueabihf", 
                        "df0f4927a67d1fd366ff81e40bd8c385a9324fbdde60437a512d106215f257b3")
            else:
                return ("aarch64-none-linux-gnu", 
                        "12fcdf13a7430655229b20438a49e8566e26551ba08759922cdaf4695b0d4e23")

        def validate(self):
            if self.settings.arch != "x86_64" or self.settings.os != "Linux":
                raise ConanInvalidConfiguration(f"This toolchain is not compatible with {self.settings.os}-{self.settings.arch}. "
                                                "It can only run on Linux-x86_64.")

            valid_archs = self._archs32() + self._archs64()
            if self.settings_target.os != "Linux" or self.settings_target.arch not in valid_archs:
                raise ConanInvalidConfiguration(f"This toolchain only supports building for Linux-{valid_archs.join(',')}. "
                                            f"{self.settings_target.os}-{self.settings_target.arch} is not supported.")

            if self.settings_target.compiler != "gcc":
                raise ConanInvalidConfiguration(f"The compiler is set to '{self.settings_target.compiler}', but this "
                                                "toolchain only supports building with gcc.")

            if Version(self.settings_target.compiler.version) >= Version("14") or Version(self.settings_target.compiler.version) < Version("13"):
                raise ConanInvalidConfiguration(f"Invalid gcc version '{self.settings_target.compiler.version}'. "
                                                    "Only 13.X versions are supported for the compiler.")


        def package_id(self):
            self.info.settings_target = self.settings_target
            # We only want the ``arch`` setting
            self.info.settings_target.rm_safe("os")
            self.info.settings_target.rm_safe("compiler")
            self.info.settings_target.rm_safe("build_type")

        def source(self):
            download(self, "https://developer.arm.com/GetEula?Id=37988a7c-c40e-4b78-9fd1-62c20b507aa8", "LICENSE", verify=False)

        def build(self):
            toolchain, sha = self._get_toolchain(self.settings_target.arch)
            get(self, f"https://developer.arm.com/-/media/Files/downloads/gnu/13.2.rel1/binrel/arm-gnu-toolchain-13.2.rel1-x86_64-{toolchain}.tar.xz",
                sha256=sha, strip_root=True)            

        def package(self):
            toolchain, _ = self._get_toolchain(self.settings_target.arch)
            dirs_to_copy = [toolchain, "bin", "include", "lib", "libexec"]
            for dir_name in dirs_to_copy:
                copy(self, pattern=f"{dir_name}/*", src=self.build_folder, dst=self.package_folder, keep_path=True)
            copy(self, "LICENSE", src=self.build_folder, dst=os.path.join(self.package_folder, "licenses"), keep_path=False)

        def package_info(self):
            toolchain, _ = self._get_toolchain(self.settings_target.arch)
            self.cpp_info.bindirs.append(os.path.join(self.package_folder, toolchain, "bin"))

            self.conf_info.define("tools.build:compiler_executables", {
                "c":   f"{toolchain}-gcc",
                "cpp": f"{toolchain}-g++",
                "asm": f"{toolchain}-as"
            })

Validating the toolchain package: settings, settings_build and settings_target
------------------------------------------------------------------------------

As you already know, the :ref:`validate() method<reference_conanfile_methods_validate>` is
used to mark that the package does not work with some configurations. As we said below, we
are restricting the use of this package to be used by a *Linux* *x86_64* to cross-build to
another Linux ARM for both 32 and 64 bits. Let's see how we translate that information to
the ``validate()`` method and explain the different types of settings in the process:

.. code-block:: python

    ...

    settings = "os", "arch"

    ...

    def validate(self):

        if self.settings.arch != "x86_64" or self.settings.os != "Linux":
            raise ConanInvalidConfiguration(f"This toolchain is not compatible with {self.settings.os}-{self.settings.arch}. "
                                            "It can only run on Linux-x86_64.")
        ...

**Validating the build platform**

Please, first note that we only declared ``os`` and ``arch`` settings. These are in fact
the settings of the machine that will build the package for the toolchain, so we will just
need those to check that these correspond to ``Linux`` and ``x86_64`` becausa that's the
platform the binaries for the toolchain were meant to run into.

It's very important to note that in this case, for this package that is going to be used
as a tool_requires, those settings do not correspond to the ``host`` profile, but to the
``build`` profile. Conan knows about this, because when we create the package later we
will pass the ``--build-require`` argument to the Conan create that will make that the
``settings`` equal in practice to the ``settings_build``.

**Validating the target platform**

In this case, that we are cross-compiling, if we want to make checks on the platform that
is going to run the executable that will be produced by the compilers of the toolchain we
have to refer to them using the ``settings_target``. These settings_target, come in fact
from the information of the ``host`` profile. So, in our case if we are building for a
Raspberry Pi, that will be the information stored in the ``settings_target``. Again, Conan
knows that the settings_target have to be file with the ``host`` profile information
because we pass the ``--build-require`` argument when creating the package.

.. code-block:: python

    def validate(self):
        ...

        valid_archs = self._archs32() + self._archs64()
        if self.settings_target.os != "Linux" or self.settings_target.arch not in valid_archs:
            raise ConanInvalidConfiguration(f"This toolchain only supports building for Linux-{valid_archs.join(',')}. "
                                           f"{self.settings_target.os}-{self.settings_target.arch} is not supported.")

        if self.settings_target.compiler != "gcc":
            raise ConanInvalidConfiguration(f"The compiler is set to '{self.settings_target.compiler}', but this "
                                            "toolchain only supports building with gcc.")

        if Version(self.settings_target.compiler.version) >= Version("14") or Version(self.settings_target.compiler.version) < Version("13"):
            raise ConanInvalidConfiguration(f"Invalid gcc version '{self.settings_target.compiler.version}'. "
                                            "Only 13.X versions are supported for the compiler.")

As you can see, we do some verifications to check that the architectures and os where the
resulting binary will run are valid and also to check that the compiler name and version
corresponds to the expected one in the package for the ``host`` context.

