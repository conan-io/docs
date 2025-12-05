EnvVars
=======

.. warning::

    These tools are still **experimental** (so subject to breaking changes) but with very stable syntax.
    We encourage the usage of it to be prepared for Conan 2.0.


``EnvVars`` is a class that represents an instance of environment variables for a given system.
It is obtained from the generic ``Environment`` class.

This class is used by other tools like the :ref:`conan.tools.gnu<conan_tools_gnu>` autotools helpers and
the :ref:`VirtualBuildEnv<conan_tools_env_virtualbuildenv>` and :ref:`VirtualRunEnv<conan_tools_env_virtualrunenv>`
generator.


Creating launcher files
+++++++++++++++++++++++

``EnvVars`` object can generate launcher (shell or bat scripts) files:

.. code:: python

    def generate(self):
        env1 = Environment()
        env1.define("foo", "var")
        envvars = env1.vars(self)
        envvars.save_script("my_launcher")


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

The ``scope`` argument (``"build"`` by default) can be used to define different scope of environment files, to
aggregate them separately. For example, using a ``scope="run"``, like the ``VirtualRunEnv`` generator does, will
aggregate and create a ``conanrun.bat|sh`` script:

.. code:: python

    def generate(self):
        env1 = Environment(self)
        env1.define("foo", "var")
        envvars = env1.vars(self, scope="run")
        # Will append "my_launcher" to "conanrun.bat|sh"
        envvars.save_script("my_launcher")


You can also use ``scope=None`` argument to avoid appending the script to the aggregated ``conanbuild.bat|sh``:

.. code:: python

    env1 = Environment(self)
    env1.define("foo", "var")
    # Will not append "my_launcher" to "conanbuild.bat|sh"
    envvars = env1.vars(self, scope=None)
    envvars.save_script("my_launcher")



Applying the environment variables
++++++++++++++++++++++++++++++++++

As an alternative to a launcher, environments can be applied in the python environment, but the usage
of the launchers is recommended if possible:

.. code:: python

    from conan.tools.env import Environment

    env1 = Environment(self)
    env1.define("foo", "var")
    envvars = env1.vars(self)
    with envvars.apply():
       # Here os.getenv("foo") == "var"
       ...

Iterating the variables
+++++++++++++++++++++++

You can iterate an ``EnvVars`` object like this:

.. code:: python

    env1 = Environment()
    env1.append("foo", "var")
    env1.append("foo", "var2")
    envvars = env1.vars(self)
    for name, value in envvars.items():
        assert name == "foo":
        assert value == "var var2"
