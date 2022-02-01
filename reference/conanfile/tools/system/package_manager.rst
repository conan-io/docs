.. _conan_tools_system_package_manager:

conan.tools.system.package_manager
==================================

.. warning::

    These tools are **experimental** and subject to breaking changes.


The tools under `conan.tools.system.package_manager` are wrappers around some of the most
popular system package managers for different platforms. You can use them to invoke system
package managers in recipes and perform the most typical operations, like installing a
package, updating the package manager database or checking if a package is installed.


You can use these tools inside the :ref:`method_system_requirements` method of your recipe, like:


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

* *Apt* for **Linux** with distribution names: *ubuntu*, *debian*
* *Yum* for **Linux** with distribution names: *pidora*, *scientific*, *xenserver*, *amazon*, *oracle*, *amzn*, *almalinux*
* *Dnf* for **Linux** with distribution names: *fedora*, *rhel*, *centos*, *mageia*
* *Brew* for **macOS**
* *PacMan* for **Linux** with distribution names: *arch*, *manjaro* and when using **Windows** with *msys2*
* *Chocolatey* for **Windows**
* *Zypper* for **Linux** with distribution names: *opensuse*, *sles*
* *Pkg* for **Linux** with distribution names: *freebsd*
* *PkgUtil* for **Solaris**

You can override this default mapping and set the package manager tool you want to use by
default setting the configuration property `tools.system.package_manager:tool`.

.. _conan_tools_system_package_manager_methods:

Methods available for system package manager tools 
--------------------------------------------------

All these wrappers share three methods that represent the most common operations with a
system package manager. They take the same form for all of the package managers except for
*Apt* that also accepts the *recommends* argument for the :ref:`install
method<conan_tools_system_package_manager_apt_methods>`.

* ``install(self, packages, update=False, check=False):`` try to install
  the list of packages passed as a parameter. If the parameter ``check`` is ``True`` it
  will check if those packages are already installed before installing them. If the
  parameter ``update`` is ``True`` it will try to update the package manager database
  before checking and installing. Its behaviour is affected by the value of
  ``tools.system.package_manager:mode``
  :ref:`configuration<conan_tools_system_package_manager_config>`.
* ``update()`` update the system package manager database. Its behaviour is affected by
  the value of ``tools.system.package_manager:mode``
  :ref:`configuration<conan_tools_system_package_manager_config>`.
* ``check(packages)`` check if the list of packages passed as parameter are already
  installed.

.. _conan_tools_system_package_manager_config:

Configuration properties that affect how system package managers are invoked
----------------------------------------------------------------------------

As explained above there are several :ref:`configuration properties<global_conf>` that
affect how these tools are invoked:

* ``tools.system.package_manager:tool``: to choose which package manager tool you want to
  use by default: ``"apt-get"``, ``"yum"``, ``"dnf"``, ``"brew"``, ``"pacman"``,
  ``"choco"``, ``"zypper"``, ``"pkg"`` or ``"pkgutil"``

* ``tools.system.package_manager:mode``: mode to use when invoking the package manager
  tool. There are two possible values:

  * ``"check"``: will not try to update the package manager database or install any
    packages in any case. This is the default value.

  * ``"install"``: it will allow Conan to perform update or install operations.

* ``tools.system.package_manager:sudo``: Use *sudo* when invoking the package manager
  tools in Linux (``False`` by default)

* ``tools.system.package_manager:sudo_askpass``: Use the ``-A`` argument if using sudo in
  Linux to invoke the system package manager (``False`` by default)


There are some specific arguments for each of these tools. Here is the complete reference:

conan.tools.system.package_manager.Apt
--------------------------------------

Will invoke the *apt-get* command. Enabled by default for **Linux** with distribution
names: *ubuntu* and *debian*.

Constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile, arch_names=None):

* **conanfile**: the current recipe object. Always use ``self``.
* **arch_names**: this argument maps the Conan architecture setting with the package manager
  tool architecture names. It is ``None`` by default, which means that it will use a
  default mapping for the most common architectures. For example, if you are using
  ``x86_64`` Conan architecture setting, it will map this value to ``amd64`` for *Apt* and
  try to install the ``<package_name>:amd64`` package. You can pass this argument to
  override the default Conan mapping, like: 

..  code-block:: python
    :caption: conanfile.py

    ...
    def system_requirements(self):
        apt = Apt(self, arch_names={"<conan_arch_setting>": "apt_arch_setting"})
        apt.install(["libgl-dev"])

The default mapping Conan uses for *APT* packages architecture is:

..  code-block:: python

      self._arch_names = {"x86_64": "x86_64",
                          "x86": "i?86",
                          "ppc32": "powerpc",
                          "ppc64le": "ppc64le",
                          "armv7": "armv7",
                          "armv7hf": "armv7hl",
                          "armv8": "aarch64",
                          "s390x": "s390x"} if arch_names is None else arch_names


.. _conan_tools_system_package_manager_apt_methods:

Methods
+++++++

* ``install(self, packages, update=False, check=False, recommends=False):``: will try to
  install the list of packages passed as a parameter. If the parameter ``check`` is
  ``True`` it will check if those packages are already installed before installing them.
  If the parameter ``update`` is ``True`` it will try to update the package manager
  database before checking and installing. If the parameter ``recommends`` is ``False`` it
  will add the ``'--no-install-recommends'`` argument to the *apt-get* command call. Its
  behaviour is affected by the value of ``tools.system.package_manager:mode``
  :ref:`configuration<conan_tools_system_package_manager_config>`.
* ``update()`` same behaviour as the one explained in the
  :ref:`section<conan_tools_system_package_manager_methods>` above.
* ``check(packages)`` same behaviour as the one explained in the
  :ref:`section<conan_tools_system_package_manager_methods>` above.


.. _conan_tools_system_package_manager_yum:

conan.tools.system.package_manager.Yum
--------------------------------------

Will invoke the *yum* command. Enabled by default for **Linux** with distribution names:
*pidora*, *scientific*, *xenserver*, *amazon*, *oracle*, *amzn* and *almalinux*.

Constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile, arch_names=None):

* **conanfile**: the current recipe object. Always use ``self``.
* **arch_names**: this argument maps the Conan architecture setting with the package manager
  tool architecture names. It is ``None`` by default, which means that it will use a
  default mapping for the most common architectures. For example, if you are using
  ``x86`` Conan architecture setting, it will map this value to ``i?86`` for *Yum* and
  try to install the ``<package_name>.i?86`` package. 
  
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

Constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile, arch_names=None):

* **conanfile**: the current recipe object. Always use ``self``.
* **arch_names**: this argument maps the Conan architecture setting with the package manager
  tool architecture names. It is ``None`` by default, which means that it will use a
  default mapping for the most common architectures. If you are using
  ``x86`` Conan architecture setting, it will map this value to ``lib32`` for *PacMan* and
  try to install the ``<package_name>-lib32`` package. 

The default mapping Conan uses for *PacMan* packages architecture is:

..  code-block:: python

      self._arch_names = {"x86": "lib32"} if arch_names is None else arch_names

conan.tools.system.package_manager.Zypper
-----------------------------------------

Will invoke the *zypper* command. Enabled by default for **Linux** with distribution
names: *opensuse*, *sles*.

Constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile, arch_names=None):

* **conanfile**: the current recipe object. Always use ``self``.

conan.tools.system.package_manager.Brew
---------------------------------------

Will invoke the *brew* command. Enabled by default for **macOS**.

Constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile, arch_names=None):

* **conanfile**: the current recipe object. Always use ``self``.

conan.tools.system.package_manager.Pkg
--------------------------------------

Will invoke the *pkg* command. Enabled by default for **Linux** with distribution names: *freebsd*.

Constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile, arch_names=None):

* **conanfile**: the current recipe object. Always use ``self``.

conan.tools.system.package_manager.PkgUtil
------------------------------------------

Will invoke the *pkgutil* command. Enabled by default for **Solaris**.

Constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile, arch_names=None):

* **conanfile**: the current recipe object. Always use ``self``.

conan.tools.system.package_manager.Chocolatey
---------------------------------------------

Will invoke the *choco* command. Enabled by default for **Windows**.

Constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile, arch_names=None):

* **conanfile**: the current recipe object. Always use ``self``
