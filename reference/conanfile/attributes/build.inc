Build
+++++


generators
----------

List or tuple of strings with names of generators.

.. code-block:: python

    class MyLibConan(ConanFile):
        generators = "CMakeDeps", "CMakeToolchain"


The generators can also be instantiated explicitly in the <MISSING PAGE> generate() method.


.. code-block:: python

    from conan.tools.cmake import CMakeToolchain

    class MyLibConan(ConanFile):
        ...

        def generate(self):
            tc = CMakeToolchain(self)
            tc.generate()


build_policy
------------

Controls when the current package is built during a ``conan install``.
The allowed values are:
    
- ``"missing"``: Conan builds it from source if there is no binary available.
- ``"never"``: This package cannot be built from sources, it is always created with
  ``conan export-pkg``
- ``None`` (default value): This package won't be built unless the policy is specified
  in the command line (e.g ``--build=foo*``)

   .. code-block:: python
      :emphasize-lines: 2

       class PocoTimerConan(ConanFile):
           build_policy = "missing"


win_bash
--------

When ``True`` it enables the new run in a subsystem bash in Windows mechanism.

.. code-block:: python

    from conan import ConanFile

    class FooRecipe(ConanFile):
        ...
        win_bash = True


It can also be declared as a ``property`` based on any condition:

.. code-block:: python

    from conan import ConanFile

    class FooRecipe(ConanFile):
        ...


        @property
        def win_bash(self):
            return self.settings.arch == "armv8"

win_bash_run
------------

When ``True`` it enables running commands in the ``"run"`` scope, to run them inside a bash shell.

.. code-block:: python

    from conan import ConanFile

    class FooRecipe(ConanFile):

        ...

        win_bash_run = True
        def build(self):
            self.run(cmd, scope="run")  # will run <cmd> inside bash
