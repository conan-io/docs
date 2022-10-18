Package files: the package() method
===================================

.. important::

    In this example, we retrieve the *fmt* Conan package from a Conan repository with
    packages compatible with Conan 2.0. To run this example successfully you should add
    this remote to your Conan configuration (if did not already do it) doing: ``conan
    remote add conanv2 https://conanv2beta.jfrog.io/artifactory/api/conan/conan --index
    0``


We already used the ``package()`` method in our `hello` package to invoke CMake's install
step. In this tutorial, we will explain the use of the :ref:`CMake.install()
<conan-cmake-build-helper>` with more detail and also how to modify this method do things
like:

- Using :ref:`conan.tools.files <conan_tools_files>` utilities to copy the generated
  artifacts from the build folder to the package folder
- Copying package licenses
- Manage how symlinks are packaged

Please, first clone the sources to recreate this project. You can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/package_method


Using CMake install step in the package() method
------------------------------------------------

This is the simplest choice when you have already defined in your `CMakeLists.txt` the
functionality of extracting the artifacts (headers, libraries, binaries) from the build
and source folder to a predetermined place and maybe do some post-processing of those
artifacts. This will work without changes in your `CMakeLists.txt` because Conan will set
the ``CMAKE_INSTALL_PREFIX`` CMake variable to the recipe :ref:`package_folder
<conan_conanfile_properties_package_folder>` attribute. Then, just calling `install()` in
the `CMakeLists.txt` over the created target is enough for Conan to move the built
artifacts to the correct location in the Conan local cache.

.. code-block:: text
    :caption: *CMakeLists.txt*
    :emphasize-lines: 10

    cmake_minimum_required(VERSION 3.15)
    project(hello CXX)

    add_library(hello src/hello.cpp)
    target_include_directories(hello PUBLIC include)
    set_target_properties(hello PROPERTIES PUBLIC_HEADER "include/hello.h")

    ...

    install(TARGETS hello)

.. code-block:: python
    :caption: *conanfile.py*
    :emphasize-lines: 10

    cmake_minimum_required(VERSION 3.15)
    project(hello CXX)

    add_library(hello src/hello.cpp)
    target_include_directories(hello PUBLIC include)
    set_target_properties(hello PROPERTIES PUBLIC_HEADER "include/hello.h")

    ...

    install(TARGETS hello)


Use conan.tools.files.copy in the package() method
--------------------------------------------------







licenses
--------

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()


        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))
        tools.rmdir(os.path.join(self.package_folder, "share"))
        tools.remove_files_by_mask(os.path.join(self.package_folder, "lib"), "*.pdb")
        tools.remove_files_by_mask(os.path.join(self.package_folder, "bin"), "*.pdb")

    def package(self):
        self.copy("DOC/License.txt", src="", dst="licenses")
        self.copy("DOC/unRarLicense.txt", src="", dst="licenses")
        if self.settings.os == "Windows":
            self.copy("*.exe", src="CPP/7zip", dst="bin", keep_path=False)
            self.copy("*.dll", src="CPP/7zip", dst="bin", keep_path=False)


other packaging patterns
------------------------

    def package(self):
        ags_lib_path = os.path.join(self.source_folder, self._source_subfolder, "ags_lib")
        self.copy("LICENSE.txt", dst="licenses", src=ags_lib_path)
        self.copy("*.h", dst="include", src=os.path.join(ags_lib_path, "inc"))

        if self.settings.compiler == "Visual Studio":
            win_arch = self._convert_arch_to_win_arch(self.settings.arch)
            if self.options.shared:
                shared_lib = "amd_ags_{arch}.dll".format(arch=win_arch)
                symbol_lib = "amd_ags_{arch}.lib".format(arch=win_arch)
                self.copy(shared_lib, dst="bin", src=os.path.join(ags_lib_path, "lib"))
                self.copy(symbol_lib, dst="lib", src=os.path.join(ags_lib_path, "lib"))
            else:
                vs_version = self._convert_msvc_version_to_vs_version(self.settings.compiler.version)
                static_lib = "amd_ags_{arch}_{vs_version}_{runtime}.lib".format(arch=win_arch, vs_version=vs_version, runtime=self.settings.compiler.runtime)
                self.copy(static_lib, dst="lib", src=os.path.join(ags_lib_path, "lib"))

fix symlinks, fix _fix_permissions, fix library names, fix install dirs!!!!
----------------------------------------------------------------------------


    def package(self):
        copy(self, "*", src=self._source_subfolder, dst=self.package_folder, keep_path=True)
        copy(self, "*NOTICE", src=self._source_subfolder, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, "*NOTICE.toolchain", src=self._source_subfolder, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, "cmake-wrapper.cmd", src=self.build_folder, dst=self.package_folder)
        copy(self, "cmake-wrapper", src=self.build_folder, dst=self.package_folder)
        self._fix_broken_links()
        self._fix_permissions()

Build and run tests for your project
------------------------------------

#######################

Links to 1.x docs:

- https://docs.conan.io/en/latest/reference/conanfile/methods.html#package
- https://docs.conan.io/en/latest/howtos/cmake_install.html#reuse-cmake-install

To be covered here:

- copy/autotools.install/cmake.install…
- copiado de licencias
- Symlink management? fix _fix_permissions, fix library names, fix install dirs!!!!
- Autotools install case for shared!!!

#######################






Read more
---------

- ...