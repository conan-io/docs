Extending the binary model
==========================

There are a few mechanisms to extend the default Conan binary model:

Custom settings
---------------

It is possible to add new settings or subsettings in the  *settings.yml* file, something like:

.. code-block:: yaml

    os:
        Windows:
            new_subsetting: [null, "subvalue1", "subvalue2"]
    new_root_setting: [null, "value1", "value2"]


Where the ``null`` value allows leaving the setting undefined in profiles. If not including, it will be mandatory that profiles define a value for them.

The custom settings will be used explicitly or implictly in recipes and packages:

.. code-block:: python

    class Pkg(ConanFile):
        # If we explicilty want this package binaries to vary according to 'new_root_setting'
        settings = "os", "compiler", "build_type", "arch", "new_root_setting"
        # While all packages with 'os=Windows' will implicitly vary according to 'new_subsetting'

.. seealso::

    For the full reference of how ``settings.yml`` file can be customized :ref:`visit the settings section<reference_config_files_customizing_settings>`.
    In practice, it is not necessary to modify the ``settings.yml`` file, and instead, it is possible to provide ``settings_user.yml`` file to extend the existing settings. See :ref:`the settings_user.yml documentation<examples_config_files_settings_user>`.


Custom options
--------------
``Options`` are custom to every recipe, there is no global definition of options like the ``settings.yml`` one.

Package ``conanfile.py`` recipes define their own options, with their own range of valid values and their own defaults:

.. code-block:: python

    class MyPkg(ConanFile):
        ...
        options = {"build_tests": [True, False],
                   "option2": "ANY"}
        default_options = {"build_tests": True,
                            "option1": 42,
                            "z*:shared": True}


The options ``shared``, ``fPIC`` and ``header_only`` have special meaning for Conan, and are considered automatically by most built-in build system integrations.
They are also the recommended default to represent when a library is shared, static or header-only.

.. seealso::

    - :ref:`documentation for options<conan_conanfile_properties_options>` 
    - :ref:`documentation for default_options<conan_conanfile_properties_default_options>`.


Settings vs options vs conf
---------------------------

When to use settings or options or configuration?

- **Settings** are a project-wide configuration, something that typically affects the whole project that
  is being built and affects the resulting package binaries. For example, the operating system or the architecture would be naturally the same for all
  packages in a dependency graph, linking a Linux library to build a Windows app, or
  mixing architectures is impossible.
  Settings cannot be defaulted in a package recipe. A recipe for a given library cannot say that its default is
  ``os=Windows``. The ``os`` will be given by the environment in which that recipe is processed. It is
  a mandatory input to be defined in the input profiles.
- On the other hand, **options** are a package-specific configuration that affects the resulting package binaries. Static or shared library are not
  settings that apply to all packages. Some can be header only libraries while other packages can be just data,
  or package executables. For example, ``shared`` is a common option (the default for specifying if a library can be static or shared), 
  but packages can define and use any options they want.
  Options are defined in the package ``conanfile.py`` recipe, including their supported and default values with ``options`` and ``default_options``.
- Configuration via ``conf`` is intended for configuration that does not affect the resulting package binaries in the general case. For example,
  building one library with the ``tools.cmake.cmaketoolchain:generator=Ninja`` shouldn't result in a binary different than if built with Visual Studio 
  (just a typically faster build thanks to Ninja).

There are some exceptions to the above. For example, settings can be defined per-package using the ``<pattern:>setting=value``, both in profiles and
command line:

.. code-block:: bash

    $ conan install . -s mypkg/*:compiler=gcc -s compiler=clang ..

This will use ``gcc`` for "mypkg" and ``clang`` for the rest of the dependencies (in most cases it is recommended to use the same compiler for the whole dependency graph, but some scenarios when strong binary compatibility is guaranteed, it is possible to mix libraries built with different compilers).

There are situations whereby many packages use the same option value, thereby allowing you to set its value once using patterns, like:

.. code-block:: bash

    $ conan install . -o *:shared=True


Custom configuration
--------------------

As commented above, the Conan ``conf`` configuration system is intended to tune some of the tools and behaviors, but without really affecting the resulting package binaries. Some typical ``conf`` items are activating parallel builds, configuring "retries" when uploading to servers, or changing the CMake generator.
Read more about :ref:`the Conan configuration system in this section<reference_config_files_global_conf>`.

There is also the possibility to define ``user.xxxx:conf=value`` for user-defined configuration, that in the same spirit as core and tools built-in configurations, do not affect the ``package_id`` of binaries.

But there might be some special situations in which it is really desired that some ``conf`` defines different ``package_ids``, creating different package binaries. It is possible to do this in two different places:

- Locally, in the recipe's ``package_id`` method, via the ``self.info.conf`` attribute:

  .. code-block:: python

        def package_id(self):
            # We can get the value from the actual current conf value, or define a new value
            value = self.conf.get("user.myconf:myitem")
            # This ``self.info.conf`` will become part of the ``package_id``
            self.info.conf.define("user.myconf:myitem", value)

- Globally, with the ``tools.info.package_id:confs`` configuration, receiving as argument a list of existing configuration to be part of the package ID, so you can define in profiles:

  .. code-block:: ini

    tools.info.package_id:confs=["tools.build:cxxflags", ...]

  The value of the ``package_id`` will contain the value provided in the ``tools.build:cxxflags`` and other configurations. Note that this value is managed as a string, changing the string, will produce a different result and a different ``package_id``, so if this approach is used, it is very important to be very consistent with the provided values for different configurations like ``tools.build:cxxflags``.

  It is also possible to use regex expressions to match several ``confs``, instead of listing all of them, for example ``.*cmake`` could match any configuration that contains "cmake" in its name (not that this is recommended, see best practices below).

.. note::

    **Best practices**

    In general, defining variability of binaries ``package_id`` via ``conf`` should be reserved for special situations and always managed with care. Passing many different ``confs`` to the ``tools.info.package_id:confs`` can easily result in issues like missing binaries or unnecessarily building too many binaries. If that is the case, consider building higher level abstraction over your binaries with new custom settings or options.


Cross build target settings
---------------------------

The ``self.settings_target`` is a ``conanfile.py`` attribute that becomes relevant in cross-compilation scenarios for the ``tool_requires`` tools in the "build" context. When we have a ``tool_requires`` like CMake, lets say the ``cmake/3.25.3``, the package binary is independent of the possible platform that cross-compiling will target, it is the same ``cmake`` executable for all different target platforms. The ``settings`` for a cross-building from Windows-X64 to Linux-armv8 scenario for the ``cmake`` conanfile recipe would be:

- ``self.settings``: The settings where the current ``cmake/3.25.3`` will run. As it is a tool-require, it will run in the Windows machine, so ``self.settings.os = Windows`` and ``self.settings.arch = x86_64``.
- ``self.settings_build``: The settings of the current build machine that would build this package if necessary. This is also the Windows-x64 machine, so ``self.settings_build.os = Windows`` and ``self.settings_build.arch = x86_64`` too.
- ``self.settings_target``: The settings that the current application outcome will target. In this case it will be ``self.settings_target.os = Linux`` and ``self.settings_target.arch = armv8``

In the ``cmake`` package scenario, as we pointed out, the target is irrelevant. It is not used in the ``cmake`` conanfile recipe at all, and it doesn't affect the ``package_id`` of the ``cmake`` binary package.

But there are situations when the binary package can be different based on the target platform. For example a cross-compiler ``gcc`` that has a different ``gcc`` executable based on the target it will compile for. This is typical in the GNU ecosystem where we can find ``arm-gcc`` toolchains, for example, specific for a given architecture.
This scenario can be reflected by Conan, extending the ``package_id`` with the value of these ``settings_target``:

.. code-block:: python

    def package_id(self):
        self.info.settings_target = self.settings_target
        # If we only want the ``os`` and ``arch`` settings, then we remove the other:
        self.info.settings_target.rm_safe("compiler")
        self.info.settings_target.rm_safe("build_type")
