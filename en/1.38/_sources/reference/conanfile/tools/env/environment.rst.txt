Environment
===========

.. warning::

    This is a **very experimental** feature and it will have breaking changes in future releases.


``Environment`` is a class that helps defining modifications to the environment variables.
This class is used by other tools like the :ref:`conan.tools.gnu<conan_tools_gnu>` autotools helpers and
the :ref:`VirtualEnv<conan_tools_env_virtualenv>` generator.

It allows different operations like:

.. code:: python

    from conan.tools.env import Environment

    env = Environment()
    env.define("MYVAR1", "MyValue1")  # Overwrite previously existing MYVAR1 with new value
    env.append("MYVAR2", "MyValue2")  # Append to existing MYVAR2 the new value
    env.prepend("MYVAR3", "MyValue3") # Prepend to existing MYVAR3 the new value
    env.unset("MYVAR4")               # Remove MYVAR4 definition from environment

    # And the equivalent with paths
    env.define_path("MYPATH1", "path/one")  # Overwrite previously existing MYPATH1 with new value
    env.append_path("MYPATH2", "path/two")  # Append to existing MYPATH2 the new value
    env.prepend_path("MYPATH3", "path/three") # Prepend to existing MYPATH3 the new value

Normal variables will be appended by default with space, but ``separator`` argument can be provided to define
a custom one.
Path variables will be appended with the default system path separator, either ``:`` or ``;``, but it also
allows defining which one.

Environments can compose:

.. code:: python

    from conan.tools.env import Environment

    env1 = Environment()
    env1.define(...)
    env2 = Environment()
    env2.append(...)

    env1.compose(env2) # env1 has priority, and its modifications will prevail

Environments can generate launcher files:

.. code:: python

    env1 = Environment()
    env1.define("foo", "var")

    env1.save_bat("my_launcher.bat")
    env1.save_sh("my_launcher.sh")

And then be used in the ``self.run`` command through the ``env`` argument:

.. code:: python

    ...
    # This will automatically wrap the "foo" command with the correct launcher:
    # my_launcher.sh && foo
    self.run("foo", env=["my_launcher"])


Environments can be applied in the python environment:

.. code:: python

    from conan.tools.env import Environment

    env1 = Environment()
    env1.define("foo", "var")
    with env1.apply():
       # Here os.getenv("foo") == "var"
       ...


There are some places where this ``Environment`` is used:

- In recipes ``package_info()`` method, in new ``self.buildenv_info`` and ``self.runenv_info``.
- In other generators like ``AutootoolsDeps`` and ``AutotoolsToolchain`` that need to define environment
- In profiles new ``[buildenv]`` and ``[runenv]`` sections.


The definition in ``package_info()`` is as follow, taking into account that both ``self.buildenv_info`` and ``self.runenv_info``
are objects of ``Environment()`` class.


.. code:: python

    from conans import ConanFile

    class App(ConanFile):
        name = "mypkg"
        version = "1.0"
        settings = "os", "arch", "compiler", "build_type"

        def package_info(self):
            # This is information needed by consumers to build using this package
            self.buildenv_info.append("MYVAR", "MyValue")
            self.buildenv_info.prepend_path("MYPATH", "some/path/folder")

            # This is information needed by consumers to run apps that depends on this package
            # at runtime
            self.runenv_info.define("MYPKG_DATA_DIR", os.path.join(self.package_folder,
                                                                   "datadir"))


