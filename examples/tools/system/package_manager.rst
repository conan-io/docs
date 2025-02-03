.. _examples_tools_system_package_manager:

Wrapping system requirements in a Conan package
===============================================

Conan can manage system packages, allowing you to install platform-specific dependencies easily.
This is useful when you need to install platform-specific system packages.
For example, you may need to install a package that provides a specific driver or graphics library that only works on a specific platform.

Conan provides a way to install system packages using the :ref:`system package manager<conan_tools_system_package_manager>` tool.

In this example, we are going to explore the steps needed to package a system library and what is needed to consume it in a Conan package.
For this illustration, we are going to package a simple C++ application that uses the `ncurses <https://invisible-island.net/ncurses/>`_ library.

Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/examples/tools/system/package_manager/


You will find the following tree structure:

.. code-block:: text

    .
    ├── conanfile.py
    └── consumer
        ├── CMakeLists.txt
        ├── conanfile.py
        └── ncurses_version.cpp


The **conanfile.py** file is the recipe that packages the ncurses library.
Finally, the **consumer** directory contains a simple C++ application that uses the ncurses library, we will visit it later.

When packaging a pre-built system library, we do not need to build the project from source, only install the
system library and package its information.
In this case, we are going to check the **conanfile.py** file that packages the ncurses library first:

.. code-block:: python

    from conan import ConanFile
    from conan.tools.system import package_manager
    from conan.tools.gnu import PkgConfig
    from conan.errors import ConanInvalidConfiguration

    required_conan_version = ">=2.0"


    class SysNcursesConan(ConanFile):
        name = "ncurses"
        version = "system"
        description = "A textual user interfaces that work across a wide variety of terminals"
        topics = ("curses", "terminal", "toolkit")
        homepage = "https://invisible-mirror.net/archives/ncurses/"
        license = "MIT"
        package_type = "shared-library"
        settings = "os", "arch", "compiler", "build_type"

        def package_id(self):
            self.info.clear()

        def validate(self):
            supported_os = ["Linux", "Macos"]
            if self.settings.os not in supported_os:
                raise ConanInvalidConfiguration(f"{self.ref} wraps a system package only supported by {supported_os}.")

        def system_requirements(self):
            dnf = package_manager.Dnf(self)
            dnf.install(["ncurses-devel"], update=True, check=True)

            yum = package_manager.Yum(self)
            yum.install(["ncurses-devel"], update=True, check=True)

            apt = package_manager.Apt(self)
            apt.install(["libncurses-dev"], update=True, check=True)

            pacman = package_manager.PacMan(self)
            pacman.install(["ncurses"], update=True, check=True)

            zypper = package_manager.Zypper(self)
            zypper.install(["ncurses"], update=True, check=True)

            brew = package_manager.Brew(self)
            brew.install(["ncurses"], update=True, check=True)

            pkg = package_manager.Pkg(self)
            pkg.install(["ncurses"], update=True, check=True)

        def package_info(self):
            self.cpp_info.bindirs = []
            self.cpp_info.includedirs = []
            self.cpp_info.libdirs = []

            pkg_config = PkgConfig(self, 'ncurses')
            pkg_config.fill_cpp_info(self.cpp_info, is_system=True)


In this **conanfile.py** file, we are using the :ref:`system package manager<conan_tools_system_package_manager>` tool
to install the ncurses library based on different package managers, under the
:ref:`system_requirements<reference_conanfile_methods_system_requirements>` method. It's important to note that the
``system_requirements`` method is called always, when building, or even if the package is already installed.
This is useful to ensure that the package is installed in the system.

Each package manager may vary the package name used to install the ncurses library, so we need to check the package manager
documentation to find the correct package name first.

Another important detail is the **package_info** method. In this method, we are using the
:ref:`PkgConfig<conan_tools_gnu_pkgconfig>` tool to fill the **cpp_info** data, based on the file ``ncurses.pc``
installed by the system package manager.

Now, let's install the ncurses library using the **conanfile.py** file:

.. code-block:: bash

    $ conan create . --build=missing -c tools.system.package_manager:mode=install -c tools.system.package_manager:sudo=true

Note that we are using the :ref:`Conan configuration<conan_tools_system_package_manager_config>`
``tools.system.package_manager:mode`` as **install**, otherwise, Conan will not install the system package, but check
if it is installed only. The same for ``tools.system.package_manager:sudo`` as **True** to run the package manager with root privileges.
As a result of this command, you should be able to see the **ncurses** library installed in your system, in case not been installed yet.

Now, let's check the **consumer** directory. This directory contains a simple C++ application that uses the ncurses library.

The **conanfile.py** file in the **consumer** directory is:

.. code-block:: python

    from conan import ConanFile
    from conan.tools.build import can_run
    from conan.tools.cmake import cmake_layout, CMake
    import os


    class AppNCursesVersionConan(ConanFile):
        settings = "os", "compiler", "build_type", "arch"
        generators = "CMakeDeps", "CMakeToolchain"
        package_type = "application"
        exports_sources = "CMakeLists.txt", "ncurses_version.cpp"

        def requirements(self):
            if self.settings.os in ["Linux", "Macos", "FreeBSD"]:
                self.requires("ncurses/system")

        def layout(self):
            cmake_layout(self)

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

            self.run(os.path.join(self.build_folder, "ncurses_version"), env="conanrun")

The recipe is simple. It requires the **ncurses** package we just created and uses the **CMake** tool to build the application.
Once the application is built, it runs the **ncurses_version** application, so we can check the executable output as its result.

The **ncurses_version.cpp** file is a simple C++ application that uses the ncurses library to print the ncurses version:

.. code-block:: cpp

    #include <cstdlib>
    #include <cstdio>
    #include <ncurses.h>


    int main(int argc, char *argv[]) {
        printf("Conan 2.x Examples - Installed NCurses version: %s\n", curses_version());
        return EXIT_SUCCESS;
    }

The **CMakeLists.txt** file is a simple CMake file that builds the **ncurses_version** application:

.. code-block:: cmake

    cmake_minimum_required(VERSION 3.15)
    project(ncurses_version CXX)

    find_package(ncurses CONFIG REQUIRED)

    add_executable(${PROJECT_NAME} ncurses_version.cpp)
    target_link_libraries(${PROJECT_NAME} PRIVATE ncurses::ncurses)

    install(TARGETS ${PROJECT_NAME} DESTINATION bin)

The CMake target **ncurses::ncurses** is provided by the **ncurses** package we just created.
The information about libraries and include directories is now available in the **cpp_info** object, as we filled it using the **PkgConfig** tool.

Now, let's build the application:

.. code-block:: bash

    $ cd consumer/
    $ conan build . --build-folder=build

After building the application, it should be executed automatically, so you may see its output:

.. code-block:: bash

   Conan 2.x Examples - Installed NCurses version: ncurses 6.2.20200212

Don't worry if the displayed version is different from the one shown here. It depends on the version installed in your system.

That's it! You have successfully packaged a system library and consumed it in a Conan package.