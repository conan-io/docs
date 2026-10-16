.. _conan_tools_env_environment_model:

Environment
===========

.. warning::

    These tools are still **experimental** (so subject to breaking changes) but with very stable syntax.
    We encourage the usage of it to be prepared for Conan 2.0.

Available since: `1.35.0 <https://github.com/conan-io/conan/releases/tag/1.35.0>`_

``Environment`` is a generic class that helps defining modifications to the environment variables.
This class is used by other tools like the :ref:`conan.tools.gnu<conan_tools_gnu>` autotools helpers and
the :ref:`VirtualBuildEnv<conan_tools_env_virtualbuildenv>` and :ref:`VirtualRunEnv<conan_tools_env_virtualrunenv>`
generator. It is important to highlight that this is a generic class, to be able to use it, a specialization
for the current context (shell script, bat file, path separators, etc), a ``EnvVars`` object needs to be obtained
from it.


Variable declaration
++++++++++++++++++++

.. code:: python

    from conan.tools.env import Environment

    def generate(self):
        env = Environment()
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

    env1 = Environment()
    env1.define(...)
    env2 = Environment()
    env2.append(...)

    env1.compose_env(env2) # env1 has priority, and its modifications will prevail


Obtaining environment variables
++++++++++++++++++++++++++++++++

You can obtain an ``EnvVars`` object with the ``vars()`` method like this:

.. code:: python

    from conan.tools.env import Environment

    def generate(self):
        env = Environment()
        env.define("MYVAR1", "MyValue1")
        envvars = env.vars(self, scope="build")
        # use the envvars object

The default ``scope`` is equal ``"build"``, which means that if this ``envvars`` generate a script to
activate the variables, such script will be automatically added to the ``conanbuild.sh|bat`` one, for
users and recipes convenience. Conan generators use ``build`` and ``run`` scope, but it might be possible
to manage other scopes too.


Environment definition
++++++++++++++++++++++

There are some other places where ``Environment`` can be defined and used:

- In recipes ``package_info()`` method, in new ``self.buildenv_info`` and ``self.runenv_info``, this
  environment will be propagated via ``VirtualBuildEnv`` and ``VirtualRunEnv`` respectively to packages
  depending on this recipe.
- In generators like ``AutootoolsDeps``, ``AutotoolsToolchain``, that need to define environment for the
  current recipe.
- In profiles new :ref:`profiles_buildenv` section.


The definition in ``package_info()`` is as follow, taking into account that both ``self.buildenv_info`` and ``self.runenv_info``
are objects of ``Environment()`` class.

.. code:: python

    from conan import ConanFile

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
