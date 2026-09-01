.. _conan_tools_system_package_manager:

conan.tools.system.package_manager
==================================

The tools under `conan.tools.system.package_manager` are wrappers around some of the most
popular system package managers for different platforms. You can use them to invoke system
package managers in recipes and perform the most typical operations, like installing a
package, updating the package manager database or checking if a package is installed. By
default, when you invoke them they will not try to install anything on the system, to
change this behavior you can set the value of the ``tools.system.package_manager:mode``
:ref:`configuration<conan_tools_system_package_manager_config>`.


You can use these tools inside the ``system_requirements()`` method of your recipe, like:


..  code-block:: python
    :caption: conanfile.py

    from conan.tools.system.package_manager import Apt, Yum, PacMan, Zypper

    def system_requirements(self):
        # depending on the platform or the tools.system.package_manager:tool configuration
        # only one of these will be executed
        Apt(self).install(["libgl-dev"])
        Yum(self).install(["libglvnd-devel"])
        PacMan(self).install(["libglvnd"])
        Zypper(self).install(["Mesa-libGL-devel"])

Conan will automatically choose which package manager to use by looking at the Operating
System name. In the example above, if we are running on Ubuntu Linux, Conan will ignore
all the calls except for the ``Apt()`` one and will only try to install the packages using the
``apt-get`` tool. Conan uses the following mapping by default:

* *Apt* for **Linux** with distribution names: *ubuntu*, *debian*, *raspbian* or *linuxmint*
* *Yum* for **Linux** with distribution names: *pidora*, *scientific*, *xenserver*, *amazon*, *oracle*, *amzn*, *almalinux* or *rocky*
* *Dnf* for **Linux** with distribution names: *fedora*, *rhel*, *centos*, *mageia*
* *Apk* for **Linux** with distribution names: *alpine*
* *Brew* for **macOS**
* *PacMan* for **Linux** with distribution names: *arch*, *manjaro* and when using **Windows** with *msys2*
* *Chocolatey* for **Windows**
* *Zypper* for **Linux** with distribution names: *opensuse*, *sles*
* *Pkg* for **FreeBSD**
* *PkgUtil* for **Solaris**

You can override this default mapping and set the package manager tool you want to use by
default setting the configuration property `tools.system.package_manager:tool`.

.. _conan_tools_system_package_manager_methods:

Methods available for system package manager tools
--------------------------------------------------

All these wrappers share three methods that represent the most common operations with a
system package manager. They take the same form for all of the package managers except for
*Apt* that also accepts the *recommends* argument for the :ref:`install
method<conan_tools_system_package_manager_apt>`.

* ``install(self, packages, update=False, check=True, host_package=True):`` try to install
  the list of packages passed as a parameter. If the parameter ``check`` is ``True`` it
  will check if those packages are already installed before installing them. If the
  parameter ``update`` is ``True`` it will try to update the package manager database
  before checking and installing. Its behaviour is affected by the value of
  ``tools.system.package_manager:mode``
  :ref:`configuration<conan_tools_system_package_manager_config>`. If the parameter
  ``host_package`` is ``True`` it will install the packages for the host machine
  architecture (the machine that will run the software), it has an effect when cross
  building. This method will return the return code of the executed commands.
* ``install_substitutes(packages_substitutes, update=False, check=True)``: try to install
  the list of lists of substitutes packages passed as a parameter, e.g., ``[["pkg1", "pkg2"], ["pkg3"]]``.
  It succeeds if one of the substitutes list is completely installed, so it's intended to be used when you have
  different packages for different distros. Internally, it's calling the previous
  ``install(packages, update=update, check=check)`` method, so ``update`` and ``check`` have the same
  purpose as above.
* ``update()`` update the system package manager database. Its behaviour is affected by
  the value of ``tools.system.package_manager:mode``
  :ref:`configuration<conan_tools_system_package_manager_config>`.
* ``check(packages)`` check if the list of packages passed as parameter are already
  installed. It will return a list with the packages that are missing.

.. _conan_tools_system_package_manager_config:

Configuration properties that affect how system package managers are invoked
----------------------------------------------------------------------------

As explained above there are several ``[conf]`` that
affect how these tools are invoked:

* ``tools.system.package_manager:tool``: to choose which package manager tool you want to
  use by default: ``"apk"``, ``"apt-get"``, ``"yum"``, ``"dnf"``, ``"brew"``,
  ``"pacman"``, ``"choco"``, ``"zypper"``, ``"pkg"`` or ``"pkgutil"``

* ``tools.system.package_manager:mode``: mode to use when invoking the package manager
  tool. There are two possible values:

  * ``"check"``: it will just check for missing packages at most and will not try to
    update the package manager database or install any packages in any case. It will raise
    an error if required packages are not installed in the system. This is the
    default value.

  * ``"report"``: Just capture the ``.install()`` calls to capture packages, but do not
    check nor install them. Never raises an error. Mostly useful for ``conan graph info``
    commands.

  * ``"report-installed"``: Report, without failing which packages are needed (same as
    ``report``) and also check which of them are actually installed in the current system.

  * ``"install"``: it will allow Conan to perform update or install operations.

* ``tools.system.package_manager:sudo``: Use *sudo* when invoking the package manager
  tools in Linux (``False`` by default)

* ``tools.system.package_manager:sudo_askpass``: Use the ``-A`` argument if using sudo in
  Linux to invoke the system package manager (``False`` by default)


There are some specific arguments for each of these tools. Here is the complete reference:

.. _conan_tools_system_package_manager_apk:

conan.tools.system.package_manager.Apk
---------------------------------------

Will invoke the *apk* command. Enabled by default for **Linux** with distribution names:
*alpine*.

Reference
+++++++++

.. currentmodule:: conan.tools.system.package_manager

.. autoclass:: Apk
    :members:
    :inherited-members:


Alpine Linux does not support multiple architectures in the same repository, so there is
no mapping from Conan architectures to Alpine architectures.

.. _conan_tools_system_package_manager_apt:

conan.tools.system.package_manager.Apt
--------------------------------------

Will invoke the *apt-get* command. Enabled by default for **Linux** with distribution
names: *ubuntu*, *debian*, *raspbian* and *linuxmint*.

Reference
+++++++++

.. currentmodule:: conan.tools.system.package_manager

.. autoclass:: Apt
    :members:
    :inherited-members:


You can pass the ``arch_names`` argument to override the default Conan mapping like this:

..  code-block:: python
    :caption: conanfile.py

    ...
    def system_requirements(self):
        apt = Apt(self, arch_names={"<conan_arch_setting>": "apt_arch_setting"})
        apt.install(["libgl-dev"])

The default mapping that Conan uses for *APT* packages architecture is:

..  code-block:: python

      self._arch_names = {"x86_64": "x86_64",
                          "x86": "i?86",
                          "ppc32": "powerpc",
                          "ppc64le": "ppc64le",
                          "armv7": "armv7",
                          "armv7hf": "armv7hl",
                          "armv8": "aarch64",
                          "s390x": "s390x"} if arch_names is None else arch_names

.. _conan_tools_system_package_manager_yum:

conan.tools.system.package_manager.Yum
--------------------------------------

Will invoke the *yum* command. Enabled by default for **Linux** with distribution names:
*pidora*, *scientific*, *xenserver*, *amazon*, *oracle*, *amzn* and *almalinux*.

Reference
+++++++++

.. currentmodule:: conan.tools.system.package_manager

.. autoclass:: Yum
    :members:
    :inherited-members:


The default mapping Conan uses for *Yum* packages architecture is:

..  code-block:: python

      self._arch_names = {"x86_64": "x86_64",
                          "x86": "i?86",
                          "ppc32": "powerpc",
                          "ppc64le": "ppc64le",
                          "armv7": "armv7",
                          "armv7hf": "armv7hl",
                          "armv8": "aarch64",
                          "s390x": "s390x"} if arch_names is None else arch_names

conan.tools.system.package_manager.Dnf
--------------------------------------

Will invoke the *dnf* command. Enabled by default for **Linux** with distribution names:
*fedora*, *rhel*, *centos* and *mageia*. This tool has exactly the same default values,
constructor and methods than the :ref:`Yum<conan_tools_system_package_manager_yum>` tool.

conan.tools.system.package_manager.PacMan
-----------------------------------------

Will invoke the *pacman* command. Enabled by default for **Linux** with distribution
names: *arch*, *manjaro* and when using **Windows** with *msys2*

Reference
+++++++++

.. currentmodule:: conan.tools.system.package_manager

.. autoclass:: PacMan
    :members:
    :inherited-members:

The default mapping Conan uses for *PacMan* packages architecture is:

..  code-block:: python

      self._arch_names = {"x86": "lib32"} if arch_names is None else arch_names

conan.tools.system.package_manager.Zypper
-----------------------------------------

Will invoke the *zypper* command. Enabled by default for **Linux** with distribution
names: *opensuse*, *sles*.

Reference
+++++++++

.. currentmodule:: conan.tools.system.package_manager

.. autoclass:: Zypper
    :members:
    :inherited-members:

conan.tools.system.package_manager.Brew
---------------------------------------

Will invoke the *brew* command. Enabled by default for **macOS**.

Reference
+++++++++

.. currentmodule:: conan.tools.system.package_manager

.. autoclass:: Brew
    :members:
    :inherited-members:

conan.tools.system.package_manager.Pkg
--------------------------------------

Will invoke the *pkg* command. Enabled by default for **Linux** with distribution names: *freebsd*.

Reference
+++++++++

.. currentmodule:: conan.tools.system.package_manager

.. autoclass:: Pkg
    :members:
    :inherited-members:

conan.tools.system.package_manager.PkgUtil
------------------------------------------

Will invoke the *pkgutil* command. Enabled by default for **Solaris**.

Reference
+++++++++

.. currentmodule:: conan.tools.system.package_manager

.. autoclass:: PkgUtil
    :members:
    :inherited-members:

conan.tools.system.package_manager.Chocolatey
---------------------------------------------

Will invoke the *choco* command. Enabled by default for **Windows**.

Reference
+++++++++

.. currentmodule:: conan.tools.system.package_manager

.. autoclass:: Chocolatey
    :members:
    :inherited-members:
