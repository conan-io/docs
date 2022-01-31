.. _conan_tools_system_package_manager:

conan.tools.system.package_manager
==================================

The tools under `conan.tools.system.package_manager` are wrappers around some of the most
popular system package managers for different platforms. You can use them to invoke these
system package managers in the recipes and perform the most typical operations, like
installing a package, updating the packages already instaled or checking if a package is
already instaled.

You can use these tools inside the :ref:`method_system_requirements` method of your recipe, like:


..  code-block:: python
    :caption: conanfile.py

    from conan.tools.system.package_manager import Apt, Yum, PacMan, Zypper

    def system_requirements(self):
        Apt(self).install(["libgl-dev"])
        Yum(self).install(["libglvnd-devel"])
        PacMan(self).install(["libglvnd"])
        Zypper(self).install(["Mesa-libGL-devel"])

Conan will automatically try to choose which package manager to used by looking at the
Operating System name. For the example above, if we are running on Ubuntu Linux, Conan
will ignore all the calls but the ``Apt()`` one. Conan uses the following mapping by
default:

- *Apt* for **Linux** with distribution names: *ubuntu*, *debian*
- *Yum* for **Linux** with distribution names: *pidora*, *scientific*, *xenserver*, *amazon*, *oracle*, *amzn*, *almalinux*
- *Dnf* for **Linux** with distribution names: *fedora*, *rhel*, *centos*, *mageia*
- *Brew* for **macOS**
- *PacMan* for **Linux** with distribution names: *arch*, *manjaro* and when using **Windows** with *msys2*
- *Chocolatey* for **Windows**
- *Zypper* for **Linux** with distribution names: *opensuse*, *sles*
- *Pkg* for **Linux** with distribution names: *freebsd*
- *PkgUtil* for **Solaris**

You can override this default mapping and set the package manager tool you want to use by
default setting the configuration property `tools.system.package_manager:tool`.

Configuration properties that affect tools in conan.tools.system.package_manager
--------------------------------------------------------------------------------

- ``tools.system.package_manager:tool``: to choose which package manager tool you want to
  use by default: ``"apt-get"``, ``"yum"``, ``"dnf"``, ``"brew"``, ``"pacman"``,
  ``"choco"``, ``"zypper"``, ``"pkg" or ``"pkgutil"``
- ``tools.system.package_manager:mode``: mode to use when invoking the package manager
  tool. There are two possible values:
 - ``"check"``: will not try to update the package manager database or install any packages in any case. This is the default value.
 - ``"install"``: it will allow conan to perform update or install operations.
- ``tools.system.package_manager:sudo``: Use 'sudo' when invoking the package manager tools in Linux (``False`` by default)
- ``tools.system.package_manager:sudo_askpass``: Use the '-A' argument if using sudo in Linux to invoke the system package manager (``False`` by default)


conan.tools.system.package_manager.Apt
--------------------------------------


conan.tools.system.package_manager.Yum
--------------------------------------


conan.tools.system.package_manager.Dnf
--------------------------------------


conan.tools.system.package_manager.Brew
---------------------------------------


conan.tools.system.package_manager.Pkg
--------------------------------------


conan.tools.system.package_manager.PkgUtil
------------------------------------------


conan.tools.system.package_manager.Chocolatey
---------------------------------------------


conan.tools.system.package_manager.PacMan
-----------------------------------------


conan.tools.system.package_manager.Zypper
-----------------------------------------

