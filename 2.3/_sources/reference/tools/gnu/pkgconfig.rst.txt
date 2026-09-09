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


Use the ``pc`` file information to fill a ``cpp_info`` object:


.. code-block:: python

    def package_info(self):
        pkg_config = PkgConfig(conanfile, "libastral", pkg_config_path=tmp_dir)
        pkg_config.fill_cpp_info(self.cpp_info, is_system=False, system_libs=["m", "rt"])



Reference
---------


.. currentmodule:: conan.tools.gnu

.. autoclass:: PkgConfig
    :members:



conf
^^^^

This helper will listen to ``tools.gnu:pkg_config`` from the :ref:`reference_config_files_global_conf` to define
the ``pkg_config`` executable name or full path. It will by default it is ``pkg-config``.
