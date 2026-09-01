.. _conan_tools_env_environment_model:

Environment
===========

.. warning::

    This is a **very experimental** feature and it will have breaking changes in future releases.


``Environment`` is a class that helps defining modifications to the environment variables.
This class is used by other tools like the :ref:`conan.tools.gnu<conan_tools_gnu>` autotools helpers and
the :ref:`VirtualBuildEnv<conan_tools_env_virtualbuildenv>` and :ref:`VirtualRunEnv<conan_tools_env_virtualrunenv>`
generator.

Constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile):

- ``conanfile``: the current recipe object. Always use ``self``.


Variable declaration
++++++++++++++++++++

.. code:: python

    from conan.tools.env import Environment

    env = Environment(self)
    env.define("MYVAR1", "MyValue1")  # Overwrite previously existing MYVAR1 with new value
    env.append("MYVAR2", "MyValue2")  # Append to existing MYVAR2 the new value
    env.prepend("MYVAR3", "MyValue3") # Prepend to existing MYVAR3 the new value
    env.remove("MYVAR3", "MyValue3")  # Remove the MyValue3 from MYVAR3
    env.unset("MYVAR4")               # Remove MYVAR4 definition from environment


    # And the equivalent with paths
    env.define_path("MYPATH1", "path/one")  # Overwrite previously existing MYPATH1 with new value
    env.append_path("MYPATH2", "path/two")  # Append to existing MYPATH2 the new value
    env.prepend_path("MYPATH3", "path/three") # Prepend to existing MYPATH3 the new value

The "normal" variables (the ones declared with ``define``, ``append`` and ``prepend``) will be appended with a space,
by default, but the ``separator`` argument can be provided to define a custom one.

The "path" variables (the ones declared with ``define_path``, ``append_path`` and ``prepend_path``) will be appended
with the default system path separator, either ``:`` or ``;``, but it also allows defining which one.


Composition
+++++++++++

Environments can be composed:

.. code:: python

    from conan.tools.env import Environment

    env1 = Environment(self)
    env1.define(...)
    env2 = Environment(self)
    env2.append(...)

    env1.compose(env2) # env1 has priority, and its modifications will prevail


Creating launcher files
+++++++++++++++++++++++

Environments can generate launcher files:

.. code:: python

    def generate(self):
        env1 = Environment(self)
        env1.define("foo", "var")
        env1.save_script("my_launcher")


Although it potentially could be used in other methods, this functionality is intended to work in the ``generate()``
method.

It will generate automatically a ``my_launcher.bat`` for Windows systems or ``my_launcher.sh`` otherwise.

Also, by default, Conan will automatically append that launcher file path to a list that will be used to
create a ``conanbuild.bat|sh`` file aggregating all the launchers in order. The ``conanbuild.sh/bat`` launcher
will be created after the execution of the ``generate()`` method.

The ``conanbuild.bat/sh`` launcher will be executed by default before calling every ``self.run()`` command. This
would be typically done in the ``build()`` method.

You can change the default launcher with the ``env`` argument:

.. code:: python

    ...
    def build(self):
        # This will automatically wrap the "foo" command with the correct launcher:
        # my_launcher.sh && foo
        self.run("foo", env=["my_launcher"])

The ``group`` argument (``"build"`` by default) can be used to define different groups of environment files, to
aggregate them separately. For example, using a ``group="run"``, like the ``VirtualRunEnv`` generator does, will
aggregate and create a ``conanrun.bat|sh`` script:

.. code:: python

    def generate(self):
        env1 = Environment(self)
        env1.define("foo", "var")
        # Will append "my_launcher" to "conanrun.bat|sh"
        env1.save_script("my_launcher", group="run")


You can also use ``group=None`` argument to avoid appending the script to the aggregated ``conanbuild.bat|sh``:

.. code:: python

    env1 = Environment(self)
    env1.define("foo", "var")
    # Will not append "my_launcher" to "conanbuild.bat|sh"
    env1.save_script("my_launcher", group=None)



Applying the environment
++++++++++++++++++++++++

As an alternative to a launcher, environments can be applied in the python environment, but the usage
of the launchers is recommended if possible:

.. code:: python

    from conan.tools.env import Environment

    env1 = Environment(self)
    env1.define("foo", "var")
    with env1.apply():
       # Here os.getenv("foo") == "var"
       ...

Iterating the Environment object
++++++++++++++++++++++++++++++++

You can iterate an Environment object like this:

.. code:: python

    env1 = Environment()
    env1.append("foo", "var")
    env1.append("foo", "var2")
    for name, value in env.items():
        assert name == "foo":
        assert value == "var var2"


Other Environment usage
++++++++++++++++++++++++

There are some other places where this ``Environment`` is used internally by Conan:

- In recipes ``package_info()`` method, in new ``self.buildenv_info`` and ``self.runenv_info``.
- In generators like ``AutootoolsDeps``, ``AutotoolsToolchain``, that need to define environment.
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

