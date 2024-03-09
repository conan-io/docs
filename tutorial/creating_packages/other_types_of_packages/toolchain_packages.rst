.. _tutorial_other_toolchain_packages:


Creating a Conan package for a toolchain
========================================

After learning how to create recipes for tool requires packaging applications we can use
during the build, we are going to show an example on how to create a recipe that packages
a precompiled toolchain or compiler for building other packages.

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

Here, you will find a Conan recipe (and the *test_package*) to package an ARM toolchain
for cross-compiling to Linux ARM for both 32 and 64 bits. To simplify a bit, we are
assuming that we can just cross-build from Linux x86_64 to Linux ARM, both 32 and 64 bits.

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

        def source(self):
            download(self, "https://developer.arm.com/GetEula?Id=37988a7c-c40e-4b78-9fd1-62c20b507aa8", "LICENSE", verify=False)

        def build(self):
            toolchain, sha = self._get_toolchain(self.settings_target.arch)
            get(self, f"https://developer.arm.com/-/media/Files/downloads/gnu/13.2.rel1/binrel/arm-gnu-toolchain-13.2.rel1-x86_64-{toolchain}.tar.xz",
                sha256=sha, strip_root=True)            

        def package_id(self):
            self.info.settings_target = self.settings_target
            # We only want the ``arch`` setting
            self.info.settings_target.rm_safe("os")
            self.info.settings_target.rm_safe("compiler")
            self.info.settings_target.rm_safe("build_type")

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

As you may recall, the :ref:`validate() method<reference_conanfile_methods_validate>` is
used to indicate that a package is not compatible with certain configurations. As
mentioned earlier, we are limiting the usage of this package to a *Linux x86_64* platform
for cross-compiling to a *Linux ARM* target, supporting both 32-bit and 64-bit
architectures. Let's check how we incorporate this information into the ``validate()``
method and discuss the various types of settings involved:

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

First, it's important to acknowledge that only the ``os`` and ``arch`` settings are
declared. These settings represent the machine that will compile the package for the
toolchain, so we only need to verify that they correspond to ``Linux`` and ``x86_64``, as
these are the platforms for which the toolchain binaries are intended.

It is important to note that for this package, which is to be used as a ``tool_requires``,
these settings do not relate to the ``host`` profile but to the ``build`` profile. This
distinction is recognized by Conan when creating the package with the ``--build-require``
argument. This will make the ``settings`` and the ``settings_build`` to be equal within
the context of package creation.

**Validating the target platform**

In scenarios involving cross-compilation, validations regarding the target platform, where
the executable generated by the toolchain's compilers will run, must refer to the
``settings_target``. These settings come from the information in the ``host`` profile. For
instance, if compiling for a Raspberry Pi, that will be the information stored in the
``settings_target``. Again, Conan is aware that ``settings_target`` should be populated with the
``host`` profile information due to the use of the ``--build-require`` flag during package
creation.


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


As you can see, several verifications are made to ensure the validity of the operating
system and architectures for the resulting binaries' execution environment. Additionally,
it verifies that the compiler's name and version align with the expectations for the
``host`` context.

Downloading the binaries for the toolchain and packaging it
-----------------------------------------------------------

.. code-block:: python

    ...

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

    ...

The `source()` method is used to download the recipe license, as it's found on the ARM
toolchains' download page. However, this is the only action performed there. The actual
toolchain binaries are fetched in the `build()` method. This approach is necessary because
the toolchain package is designed to support both 32-bit and 64-bit architectures,
requiring us to download two distinct sets of toolchain binaries. Which binary the package
ends up with depends on the `settings_target` architecture. This conditional downloading
process can't happen in the `source()` method, as it :ref:`caches the downloaded contents
<reference_conanfile_methods_source_caching>`.

The `package()` method doesn't have anything out of the ordinary; it simply copies the
downloaded files into the package folder, license included.


Adding ``settings_target`` to the Package ID information
--------------------------------------------------------

In recipes designed for cross-compiling scenarios, particularly those involving toolchains
that target specific architectures or operating systems, and the binary package can be
different based on the target platform we may need to modify the ``package_id()`` to
ensure that Conan correctly identifies and differentiates between binaries based on the
target platform they are intended for.

In this case, we extend the ``package_id()`` method to include ``settings_target``, which
encapsulates the target platform's configuration (in this case if it's 32 or 64 bit):


.. code-block:: python

    def package_id(self):
        # Assign settings_target to the package ID to differentiate binaries by target platform. 
        self.info.settings_target = self.settings_target
        
        # We only want the ``arch`` setting
        self.info.settings_target.rm_safe("os")
        self.info.settings_target.rm_safe("compiler")
        self.info.settings_target.rm_safe("build_type")

By specifying ``self.info.settings_target = self.settings_target``, we explicitly instruct
Conan to consider the target platform's settings when generating the package ID. In this
case we remove ``os``, ``compiler`` and ``build_type`` settings as changing them will not
be relevant for selecting the toolchain we will use for building and leave only the
``arch`` setting that will be used to decide if want to produce binaries for 32 or 64
bits.


Define information for consumers
-------------------------------

The ``package_info()`` method is pivotal for defining package information that is crucial
for its consumers. This method allows you to specify details about the executable paths,
compiler executables, and any other configuration details required by projects that depend
on this toolchain package.

.. code-block:: python

    def package_info(self):
        toolchain, _ = self._get_toolchain(self.settings_target.arch)
        self.cpp_info.bindirs.append(os.path.join(self.package_folder, toolchain, "bin"))

        self.conf_info.define("tools.build:compiler_executables", {
            "c":   f"{toolchain}-gcc",
            "cpp": f"{toolchain}-g++",
            "asm": f"{toolchain}-as"
        })
        

Testing the Conan toolchain package
-----------------------------------

To verify the functionality and ensure the correct setup of the toolchain package, a test
package is used. This package attempts to compile a simple project using the provided
toolchain and examines the resulting binary.

.. code-block:: python
    :caption: test_package/conanfile.py

    from conan import ConanFile
    from conan.tools.cmake import CMake, cmake_layout
    import os


    class TestPackgeConan(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        generators = "CMakeToolchain", "VirtualBuildEnv"
        test_type = "explicit"

        def build_requirements(self):
            self.tool_requires(self.tested_reference_str)

        def layout(self):
            cmake_layout(self)

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

        def test(self):
            if self.settings.arch in ["armv6", "armv7", "armv7hf"]:
                toolchain = "arm-none-linux-gnueabihf"
            else:
                toolchain = "aarch64-none-linux-gnu"
            self.run(f"{toolchain}-gcc --version")
            test_file = os.path.join(self.cpp.build.bindirs[0], "test_package")
            self.run(f"file {test_file}")

This test package ensures that the toolchain is functional and that binaries produced with
it are correctly targeted for the specified architecture, providing a solid foundation for
cross-compilation tasks.


Cross-building a simple example with the toolchain
--------------------------------------------------



.. seealso::

    - :ref:`More info on settings_target<binary_model_extending_cross_build_target_settings>`

