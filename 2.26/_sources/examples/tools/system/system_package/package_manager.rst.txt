.. _examples_tools_system_package_manager:

Wrapping system requirements in a Conan package
===============================================

Conan can manage system packages, allowing you to install platform-specific dependencies easily.
This is useful when you need to install platform-specific system packages.
For example, you may need to install a package that provides a specific driver or graphics library that only works on a specific platform.

Conan provides a way to install system packages using the :ref:`system package manager<conan_tools_system_package_manager>` tool.

In this example, we are going to explore the steps needed to create a wrapper package around a system library and what is needed to consume it in a Conan package.
Note that the package will not contain the binary artifacts, it will just manage to check/install them calling ``system_requirements()`` and the respective system package managers (e.g Apt, Yum).
In this example, we are going to create a Conan package to wrap the system `ncurses <https://invisible-island.net/ncurses/>`_
requirement and then show how to use this requirement in an application.

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
        └── ncurses_version.c


The ``conanfile.py`` file is the recipe that wraps the ncurses system library.
Finally, the **consumer** directory contains a simple C application that uses the ncurses library, we will visit it later.

When wrapping a pre-built system library, we do not need to build the project from source, only install the
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
            supported_os = ["Linux", "Macos", "FreeBSD"]
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

            self.cpp_info.set_property("cmake_file_name", "Curses")
            self.cpp_info.set_property("cmake_target_name", "Curses::Curses")
            self.cpp_info.set_property("cmake_additional_variables_prefixes", ["CURSES",])

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

Now, let's check the **consumer** directory. This directory contains a simple C application that uses the ncurses library.

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
        exports_sources = "CMakeLists.txt", "ncurses_version.c"

        def requirements(self):
            if self.settings.os in ["Linux", "Macos", "FreeBSD"]:
                self.requires("ncurses/system")

        def layout(self):
            cmake_layout(self)

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

            app_path = os.path.join(self.build_folder, "ncurses_version")
            self.output.info(f"The example application has been successfully built.\nPlease run the executable using: '{app_path}'")

The recipe is simple. It requires the **ncurses** package we just created and uses the **CMake** tool to build the application.
Once the application is built, it shows the **ncurses_version** application path, so you can run it manually as you wish and check its output.

The **ncurses_version.c** file is a simple C application that uses the ncurses library to print the ncurses version,
but using white background and blue text:

.. code-block:: c

    #include <stdlib.h>
    #include <stdio.h>
    #include <string.h>

    #include <ncurses.h>


    int main(void) {
        int max_y, max_x;
        char message [256] = {0};

        initscr();

        start_color();
        init_pair(1, COLOR_BLUE, COLOR_WHITE);
        getmaxyx(stdscr, max_y, max_x);

        snprintf(message, sizeof(message), "Conan 2.x Examples - Installed ncurses version: %s\n", curses_version());
        attron(COLOR_PAIR(1));
        mvprintw(max_y / 2, max_x / 2 - (strlen(message) / 2), "%s", message);
        attroff(COLOR_PAIR(1));

        refresh();

        return EXIT_SUCCESS;
    }

The **CMakeLists.txt** file is a simple CMake file that builds the **ncurses_version** application:

.. code-block:: cmake

    cmake_minimum_required(VERSION 3.15)
    project(ncurses_version C)

    find_package(Curses CONFIG REQUIRED)

    add_executable(${PROJECT_NAME} ncurses_version.c)
    target_link_libraries(${PROJECT_NAME} PRIVATE Curses::Curses)

The CMake target **Curses::Curses** is provided by the **ncurses** package we just created. It follows the official CMake module for `FindCurses <https://cmake.org/cmake/help/latest/module/FindCurses.html>`_.
The information about libraries and include directories is now available in the **cpp_info** object, as we filled it using the **PkgConfig** tool.

Now, let's build the application:

.. code-block:: bash

    $ cd consumer/
    $ conan build . --name=ncurses-version --version=0.1.0
      ...
      conanfile.py (ncurses-version/0.1.0): The example application has been successfully built.
      Please run the executable using: '/tmp/consumer/build/Release/ncurses_version'

After building the application, it will show the executable path. You can run it to check the output:

.. code-block:: bash

   $ /tmp/consumer/build/Release/ncurses_version

   Conan 2.x Examples - Installed ncurses version: ncurses 6.0.20160213

Don't worry if the displayed version is different from the one shown here or the executable path different.
It depends on the version installed in your system and where you built the application.

That's it! You have successfully packaged a system library and consumed it in a Conan package.


.. _examples_tools_system_package_manager_wrapper:

Wrapping a library installed in the system as a Conan package
-------------------------------------------------------------

As a variant of the above case, it is also possible to apply the above strategy to libraries that 
are installed in the system, but not necessarily installed by the system package manager, nor
necessarily in the common system locations where the compilers will find them by default.

Suppose that there is an existing library, already compiled in a user folder such as:

.. code-block:: text

    /home/myuser/mymath
                    └── include
                        ├── mymath.h
                    └── lib
                        ├── mymath.lib

And ``/home/myuser/mymath`` is not added to the compilers default paths or anything like that.

In general, a more recommended approach is to create a full package from those precompiled binaries,
and upload that package, and then manage it as any other regular package. See the tutorial about
:ref:`creating packages from pre-compiled binaries here<creating_packages_other_prebuilt>`.

But in some scenarios, it might still be desirable to use that library from its installed location
``/home/myuser/mymath`` without putting the artifacts inside a Conan package. This can be done
with a "wrapper" recipe, similar to the one above, but which does not have any ``system_requirements()``
method.

It could be something like:


.. code-block:: python

    from conan import ConanFile

    class MyMath(ConanFile):
        name = "mymath"
        version = "1.2"  # In this case an actual version might make more sense
        package_type = "static-library"

        def package_info(self):
            self.cpp_info.bindirs = []
            # Absolute paths are allowed here
            self.cpp_info.includedirs = ["/home/myuser/mymath/include"]
            self.cpp_info.libdirs = ["/home/myuser/mymath/lib"]
            self.cpp_info.libs = ["mymath"]


Note that it is also possible to still do conditions based on settings, in case that the library
is installed in the system in different locations based on the platform:

.. code-block:: python

    settings = "os"

    def package_info(self):
        self.cpp_info.bindirs = []
        # Absolute paths are allowed here
        if self.settings.os == "Windows":
            self.cpp_info.includedirs = ["C:/Users/myuser/mymath/include"]
            self.cpp_info.libdirs = ["C:/Users/myuser/mymath/lib"]
        else:
            self.cpp_info.includedirs = ["/home/myuser/mymath/include"]
            self.cpp_info.libdirs = ["/home/myuser/mymath/lib"]
        self.cpp_info.libs = ["mymath"]


It might even be possible to parametrize those absolute paths with some environment variable
specific for that platform too.

.. note::

    **Best practices**

    - The use of "wrapper" recipes like this one should be minimized, as it makes reproducibility and
      traceability harder. Creating a real package putting the headers and libraries inside it, uploading
      it to the server, makes it possible to achieve such traceability and reproducibility.
    - This type of "wrapper" recipe can be convenient together with the ``[replace_requires]`` feature,
      for specific platform constraints, like a platform that mandates that some ``openssl`` library must
      be the one contained in a sysroot, not the one from the Conan package ``openssl/version``, but in
      general, such a dependency to ``openssl/version`` is required by other packages. In those cases, writing
      a wrapper recipe around the sysroot ``openssl`` and using ``[replace_requires]`` to force the dependency
      graph to resolve to it could make sense.
