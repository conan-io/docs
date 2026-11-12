.. _examples_tools_gnu_pkg_config_sysroot:

Using PkgConfig.fill_cpp_info with PKG_CONFIG_PATH from a profile
=================================================================

The :ref:`PkgConfig<conan_tools_gnu_pkgconfig>` helper can read a ``.pc`` file and use
its contents to fill a ``cpp_info`` object with ``fill_cpp_info()``. When
``pkg_config_path`` is not passed explicitly, ``pkg-config`` locates the ``.pc`` file
via the ``PKG_CONFIG_PATH`` environment variable, which can be defined in the profile
``[buildenv]`` section.

A common scenario is cross-compilation with an external toolchain: the toolchain provides
a sysroot that already ships ``.pc`` files describing its libraries (``gl.pc``, ``EGL.pc``,
``zlib.pc``, ...), and the host profile points ``PKG_CONFIG_PATH`` at the sysroot's
``pkgconfig`` folder. A wrapper recipe can then read those ``.pc`` files at ``package()``
time and expose the information to consumers without hard-coding include and library paths.

The challenge comes when users try to define ``PKG_CONFIG_PATH`` in the ``[buildenv]`` section
of a profile, because that is not available in the ``package_info()`` method of the recipes,
as the package information cannot rely on the "build environment", as the build environment
is only available when the package is being built, but not necessarily when the package is
being consumed.

The example below uses a fabricated ``mylibastral.pc`` next to the profile to keep it
self-contained, but the mechanism is exactly the same as pointing to a real sysroot folder,
to illustrate how this could be implemented if necessary.


.. important::

    This strategy is valid only for "system" packages, that is, recipes that act as a wrapper
    around a system or sysroot dependency (typical in cross-compilation with an external
    toolchain). Regular Conan packages that build and package their own artifacts should
    not use this.


The **profile** below adds a folder containing ``.pc`` files to ``PKG_CONFIG_PATH``. The
``profile_dir`` Jinja variable resolves to the folder that contains the profile itself,
so a ``mypcs/`` folder next to the profile can be used directly:

.. code-block:: ini
    :caption: *myprofile*

    [settings]
    os=Linux
    arch=armv8

    [buildenv]
    PKG_CONFIG_PATH+=(path){{ profile_dir }}/mypcs

In a real cross-compilation setup, that path would typically point to the sysroot
folder shipped by the toolchain, for example ``{{ sysroot }}/usr/lib/pkgconfig``.

The ``.pc`` file located in the ``mypcs`` folder besides the profile describes the library 
(include folders, library folders, libs, defines, link flags, ...):

.. code-block:: text
    :caption: *mypcs/mylibastral.pc*

    prefix=/usr/local
    exec_prefix=${prefix}
    libdir=${exec_prefix}/lib
    includedir=${prefix}/include

    Name: mylibastral
    Description: Interface library for Astral data flows
    Version: 6.6.6
    Libs: -L${libdir}/libastral -lastral -lm -Wl,--whole-archive
    Cflags: -I${includedir}/libastral -D_USE_LIBASTRAL


The ``conanfile.py`` recipe uses ``PkgConfig`` to read ``mylibastral.pc`` and populate a ``CppInfo``
object. It does it at ``package()`` time, when the package is being built (the policies are added so the
package is automatically build when necessary in the current machine, and binaries are never uploaded, as 
the information from that .pc file will only be valid in the current machine).
Notice that ``pkg_config_path`` is not passed: it is picked up from
``PKG_CONFIG_PATH`` defined in the profile. The resulting ``CppInfo`` is serialized to
the package folder in ``package()``, and reloaded in ``package_info()``:

.. code-block:: python
    :caption: *conanfile.py*

    import os
    from conan import ConanFile
    from conan.tools.gnu import PkgConfig
    from conan.tools import CppInfo


    class Pkg(ConanFile):
        name = "mypkg"
        version = "0.1"
        build_policy = "missing"
        upload_policy = "skip"

        def package(self):
            # This method executes at package build time, it has 
            # available the build environment "buildenv"
            pkg_config = PkgConfig(self, "mylibastral")
            cpp_info = CppInfo(self)
            pkg_config.fill_cpp_info(cpp_info, is_system=False, system_libs=["m"])
            cpp_info.save(os.path.join(self.package_folder, "cpp_info.json"))

        def package_info(self):
            # This method executes at package consumption time, it will
            # NOT have available the build environment, but it can load a file
            # generated at build/package time
            self.cpp_info = CppInfo(self).load("cpp_info.json")


Let's now create and consume the package:

.. code-block:: bash

    $ conan create . -pr=myprofile
    $ conan install --requires=mypkg/0.1 -pr=myprofile -g CMakeDeps

The generated ``mypkg-none-armv8-data.cmake`` will contain the include/lib folders,
libs, defines and link flags read from ``mylibastral.pc``, something like:

.. code-block:: cmake

    set(mypkg_INCLUDE_DIRS_NONE "/usr/local/include/libastral")
    set(mypkg_LIB_DIRS_NONE "/usr/local/lib/libastral")
    set(mypkg_LIBS_NONE astral)
    set(mypkg_SYSTEM_LIBS_NONE m)
    set(mypkg_DEFINITIONS_NONE "-D_USE_LIBASTRAL")
    set(mypkg_COMPILE_DEFINITIONS_NONE "_USE_LIBASTRAL")
    set(mypkg_SHARED_LINK_FLAGS_NONE "-Wl,--whole-archive")
