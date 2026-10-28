.. _reference_conanfile_methods_build_system_requirements:

build_system_requirements()
===========================

.. include:: ../../../common/experimental_warning.inc

The ``build_system_requirements()`` method is a companion to ``system_requirements()`` intended specifically
for system packages that are only needed when **building from source** (i.e., when the package binary is
being compiled). It is not called when a pre-built binary is retrieved from a server or cache.

The key difference from ``system_requirements()`` is that ``build_system_requirements()`` installs packages
using the **build machine architecture** (``settings_build.arch``) rather than the host architecture. This
is especially important in cross-compilation scenarios where the build and host machines have different
architectures.

Then, these requirements are intended to be "tools", executables used at build time, but not libraries that
would be linked in the consumers libraries or applications.

.. code-block:: python

    from conan import ConanFile
    from conan.tools.system.package_manager import Apt

    class MyPkg(ConanFile):
        name = "mypkg"
        version = "1.0"
        settings = "os", "arch"

        def build_system_requirements(self):
            # Installed using build machine arch (settings_build.arch),
            # only when building from source
            apt = Apt(self)
            apt.install(["build-essential", "pkg-config"])

        def system_requirements(self):
            # Installed using host arch (settings.arch), always
            apt = Apt(self)
            apt.install(["libssl-dev"])

.. note::

   ``build_system_requirements()`` is only invoked when the package is being built from source.
   If the binary is already available in the cache or a remote, this method is skipped.


.. seealso::

   - :ref:`reference_conanfile_methods_system_requirements`
   - :ref:`conan_tools_system_package_manager`
