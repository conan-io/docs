.. _examples_config_files_customizing_settings:

Customizing settings
====================


At the :ref:`reference_config_files_settings_yml` reference we learned how the default Conan settings are defined.
In this example we are going to learn how to add custom settings that you really need to use in your recipes.

Adding new settings
-------------------

It is possible to add new settings at the root of the *settings.yml* file, something like:

.. code-block:: yaml

    os:
        Windows:
            subsystem: [null, cygwin, msys, msys2, wsl]
    distro: [null, RHEL6, CentOS, Debian]

If we want to create different binaries from our recipes defining this new setting, we would need to add to
our recipes that:

.. code-block:: python

    class Pkg(ConanFile):
        settings = "os", "compiler", "build_type", "arch", "distro"

The value ``null`` allows for not defining it (which would be a default value, valid for all other distros).
It is possible to define values for it in the profiles:

.. code-block:: text

    [settings]
    os = "Linux"
    distro = "CentOS"
    compiler = "gcc"

And use their values to affect our build if desired:

.. code-block:: python

    class Pkg(ConanFile):
        settings = "os", "compiler", "build_type", "arch", "distro"

        def build(self):
            cmake = CMake(self)
            if self.settings.distro == "CentOS":
                cmake.definitions["SOME_CENTOS_FLAG"] = "Some CentOS Value"
                ...

Adding new sub-settings
-----------------------
The above approach requires modification to all recipes to take it into account. It is also possible to define
kind of incompatible settings, like ``os=Windows`` and ``distro=CentOS``. While adding new settings is totally
possible, it might make more sense for other cases, but for this example it is more adequate to add it as above
sub-setting of the ``Linux`` OS:

.. code-block:: yaml

    os:
        Windows:
            subsystem: [null, cygwin, msys, msys2, wsl]
        Linux:
            distro: [null, RHEL6, CentOS, Debian]

With this definition we could define our profiles as:

.. code-block:: text

    [settings]
    os = "Linux"
    os.distro = "CentOS"
    compiler = "gcc"

And any attempt to define ``os.distro`` for another ``os`` value rather than ``Linux`` will raise an error.

As this is a sub-setting, it will be automatically taken into account in all recipes that declare an ``os`` setting.
Note that having a value of ``distro=null`` possible is important if you want to keep previously created binaries,
otherwise you would be forcing to always define a specific distro value, and binaries created without this sub-setting,
won't be usable anymore.

The sub-setting can also be accessed from recipes:

.. code-block:: python

    class Pkg(ConanFile):
        settings = "os", "compiler", "build_type", "arch"  # Note, no "distro" defined here

        def build(self):
            cmake = CMake(self)
            if self.settings.os == "Linux" and self.settings.os.distro == "CentOS":
                cmake.definitions["SOME_CENTOS_FLAG"] = "Some CentOS Value"


Add new values
--------------

In the same way we have added a new ``distro`` sub-setting, it is possible to add new values to existing settings
and sub-settings. For example, if some compiler version is not present in the range of accepted values, you can add those new values.

You can also add a completely new compiler:

.. code-block:: yaml

    os:
        Windows:
            subsystem: [null, cygwin, msys, msys2, wsl]
       ...
    compiler:
        gcc:
            ...
        mycompiler:
            version: [1.1, 1.2]
        msvc:


This works as the above regarding profiles, and the way they can be accessed from recipes. The main issue with custom compilers is that
the builtin build helpers, like ``CMake``, ``MSBuild``, etc, internally contains code that will check for those values. For example,
the ``MSBuild`` build helper will only know how to manage the ``msvc`` setting and sub-settings, but not the new compiler.
For those cases, custom logic can be implemented in the recipes:

.. code-block:: python

    class Pkg(ConanFile):
        settings = "os", "compiler", "build_type", "arch"

        def build(self):
            if self.settings.compiler == "mycompiler":
                my_custom_compile = ["some", "--flags", "for", "--my=compiler"]
                self.run(["mycompiler", "."] + my_custom_compile)


.. note::

    You can also remove items from *settings.yml* file. You can remove compilers, OS, architectures, etc.
    Do that only in the case you really want to protect against creation of binaries for other platforms other
    than your main supported ones. In the general case, you can leave them, the binary configurations are managed
    in **profiles**, and you want to define your supported configurations in profiles, not by restricting the *settings.yml*


.. note::

    If you customize your *settings.yml*, you can share, distribute and sync this configuration with your team
    and CI machines with the :ref:`conan_config_install` command.
