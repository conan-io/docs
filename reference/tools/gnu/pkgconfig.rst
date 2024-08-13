PkgConfig
=========

This tool can execute ``pkg_config`` executable to extract information from existing ``.pc`` files.
This can be useful for example to create a "system" package recipe over some system installed library,
as a way to automatically extract the ``.pc`` information from the system. Or if some proprietary package
has a build system that only outputs ``.pc`` files.


Usage:

Read a ``pc`` file and access the information:

.. code-block:: python

    pkg_config = PkgConfig(conanfile, "libastral", pkg_config_path=<somedir>)

    print(pkg_config.provides) # something like"libastral = 6.6.6"
    print(pkg_config.version) # something like"6.6.6"
    print(pkg_config.includedirs) # something like['/usr/local/include/libastral']
    print(pkg_config.defines) # something like['_USE_LIBASTRAL']
    print(pkg_config.libs) # something like['astral', 'm']
    print(pkg_config.libdirs) # something like['/usr/local/lib/libastral']
    print(pkg_config.linkflags) # something like['-Wl,--whole-archive']
    print(pkg_config.variables['prefix']) # something like'/usr/local'


Using PkgConfig to fill a ``cpp_info`` object
---------------------------------------------

The ``PkgConfig`` class can be used to fill a ``CppInfo`` object with the information that will be consumed by ``PkgConfigDeps`` generator later.
This is a useful feature when packaging a system library that provides a ``.pc`` file, or when a proprietary package has a build system that only outputs ``.pc`` files.

.. code-block:: python

    def package_info(self):
        pkg_config = PkgConfig(conanfile, "libastral", pkg_config_path=tmp_dir)
        pkg_config.fill_cpp_info(self.cpp_info, is_system=False, system_libs=["m", "rt"])


However, ``PkgConfig`` will invoke the ``pkg-config`` executable to extract the information from the ``.pc`` file.
The ``pkg-config`` executable must be available in the system path for this case, otherwise, it will fail when installing the consumed package.


Using pkg-config from Conan package instead of system
-----------------------------------------------------

.. include:: ../../../common/experimental_warning.inc

In case not having ``pkg-config`` available in the system, it is possible to use the ``pkg-config`` executable provided by a Conan package:

.. code-block:: python

    import os
    from conan import ConanFile
    from conan.tools.gnu import PkgConfig
    from conan.tools import CppInfo

    class Pkg(ConanFile):

        def tool_requires(self):
            self.requires("pkgconf/[*]")

        ...

        def package(self):
            pkg_config = PkgConfig(self, "libastral", pkg_config_path=".")
            cpp_info = CppInfo(self)
            pkg_config.fill_cpp_info(cpp_info, is_system=False, system_libs=["m", "rt"])
            cpp_info.save(os.path.join(self.package_folder, "cpp_info.json"))

        def package_info(self):
            self.cpp_info = CppInfo(self).load(os.path.join(self.package_folder, "cpp_info.json"))


The ``pkg-config`` executable provided by the Conan package ``pkgconf`` will be invoked only when creating the Conan binary package.
The ``.pc`` information will be extracted from the ``cpp_info.json`` file located in the package folder, it will fill the ``self.cpp_info`` object.
This way, the ``PkgConfig`` will not need to invoke the ``pkg-config`` executable again to extract the information from the ``.pc`` file,
when consuming the package.

Reference
---------


.. currentmodule:: conan.tools.gnu

.. autoclass:: PkgConfig
    :members:



conf
^^^^

This helper will listen to ``tools.gnu:pkg_config`` from the :ref:`reference_config_files_global_conf` to define
the ``pkg_config`` executable name or full path. It will by default it is ``pkg-config``.
