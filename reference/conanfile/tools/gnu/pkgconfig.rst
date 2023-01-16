PkgConfig
=========

.. important::

    This feature is still **under development**, while it is recommended and usable and we will try not to break them in future releases,
    some breaking changes might still happen if necessary to prepare for the *Conan 2.0 release*.

Available since: `1.45.0 <https://github.com/conan-io/conan/releases/tag/1.45.0>`_


This tool can execute ``pkg_config`` executable to extract information from existing ``.pc`` files.
This can be useful for example to create a "system" package recipe over some system installed library,
as a way to automatically extract the ``.pc`` information from the system. Or if some proprietary package
has a build system that only outputs ``.pc`` files.


The constructor is:

.. code-block:: python

    def __init__(self, conanfile, library, pkg_config_path=None):

- ``conanfile``: The current ``self`` instance of the conanfile using the tool
- ``library``: The library which ``.pc`` file is to be parsed. It must exist in the pkg_config path
- ``pkg_config_path``: If defined it will be prepended to ``PKG_CONFIG_PATH`` environment variable, so
  the execution finds the required files.

It can be used as:

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


There is a convenience method ``fill_cpp_info()``, that can be used in the ``package_info()`` method as:

.. code-block:: python

    def package_info(self):
        pkg_config = PkgConfig(conanfile, "libastral", pkg_config_path=tmp_dir)
        pkg_config.fill_cpp_info(self.cpp_info, is_system=False, system_libs=["m", "rt"])


Where:

- ``cpp_info`` first argument could be the global one or a component one.
- ``is_system``: if ``True``, all detected libraries will be assigned to ``cpp_info.system_libs``, and none to ``cpp_info.libs``.
- ``system_libs``: If ``is_system=False``, this argument allows defining some potential system libraries found that would be assigned to ``cpp_info.system_libs``.
  The remaining detected libs will be assigned to ``cpp_info.libs``.


conf
----

This helper will listen to ``tools.gnu:pkg_config`` :ref:`configuration <global_conf>` to define the ``pkg_config`` executable name or full path.
It will by default it is ``pkg-config``.