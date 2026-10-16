.. _conan_tools_microsoft_nmake:


NMakeDeps
=========

This generator can be used as:

.. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        settings = "os", "compiler", "build_type", "arch"

        requires = "mydep/1.0"
        # attribute declaration
        generators = "NMakeDeps"

        # OR explicit usage in the generate() method
        def generate(self):
            deps = NMakeDeps(self)
            deps.generate()

        def build(self):
            self.run(f"nmake /f makefile")

The generator will create a ``conannmakedeps.bat`` environment script that defines
``CL``, ``LIB`` and ``_LINK_`` environment variables, injecting necessary flags 
to locate and link the dependencies declared in ``requires``.
This generator should most likely be used together with ``NMakeToolchain`` one.


NMakeToolchain
==============

This generator can be used as:

.. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        settings = "os", "compiler", "build_type", "arch"
        generators = "NMakeToolchain"

        def build(self):
            self.run("nmake /f makefile")

Or it can be fully instantiated in the conanfile ``generate()`` method:

.. code:: python

    from conan import ConanFile
    from conan.tools.microsoft import NMakeToolchain

    class Pkg(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = NMakeToolchain(self)
            tc.generate()

        def build(self):
            self.run("nmake /f makefile")

NMakeToolchain generator will create a ``conannmaketoolchain.bat`` environment script injecting flags
deduced from profile (build_type, runtime, cppstd, build flags from conf) into environment variables
NMake can understand: ``CL`` and ``_LINK_``.
It will also generate a ``conanvcvars.bat`` script that activates the correct VS prompt matching the
Conan host settings ``arch``, ``compiler`` and ``compiler.version``, and build settings ``arch``.

constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile):

- ``conanfile``: the current recipe object. Always use ``self``.

Attributes
++++++++++

You can change some attributes before calling the ``generate()`` method if you want to inject more flags:

.. code:: python

    from conan import ConanFile
    from conan.tools.microsoft import NMakeToolchain

    class Pkg(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = NMakeToolchain(self)
            tc.extra_cflags.append("/my_flag")
            tc.extra_defines.append("FOO=BAR")
            tc.generate()

* **extra_cflags** (Defaulted to ``[]``): Additional cflags.
* **extra_cxxflags** (Defaulted to ``[]``): Additional cxxflags.
* **extra_defines** (Defaulted to ``[]``): Additional defines.
* **extra_ldflags** (Defaulted to ``[]``): Additional ldflags.

conf
++++

``NMaketoolchain`` is affected by these ``[conf]`` variables:

- ``tools.build:cflags`` list of extra pure C flags that will be used by ``CL``.
- ``tools.build:cxxflags`` list of extra C++ flags that will be used by ``CL``.
- ``tools.build:defines`` list of preprocessor definitions that will be used by ``CL``.
- ``tools.build:sharedlinkflags`` list of extra linker flags that will be used by ``_LINK_``.
- ``tools.build:exelinkflags`` list of extra linker flags that will be used by ``_LINK_``.
- ``tools.build:compiler_executables`` dict-like Python object which specifies the compiler as key
  and the compiler executable path as value. Those keys will be mapped as follows:

  * ``asm``: will set ``AS`` in *conannmaketoolchain.sh|bat* script.
  * ``c``: will set ``CC`` in *conannmaketoolchain.sh|bat* script.
  * ``cpp``: will set ``CPP`` and ``CXX`` in *conannmaketoolchain.sh|bat* script.
  * ``rc``: will set ``RC`` in *conannmaketoolchain.sh|bat* script.

Customizing the environment
+++++++++++++++++++++++++++

If your ``Makefile`` script needs some other environment variable rather than ``CL`` and ``_LINK_``, you can customize
it before calling the ``generate()`` method.
Call the ``environment()`` method to calculate the mentioned variables and then add the variables that you need.
The ``environment()`` method returns an :ref:`Environment<conan_tools_env_environment_model>` object:

.. code:: python

    from conan import ConanFile
    from conan.tools.microsoft import NMakeToolchain

    class Pkg(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = NMakeToolchain(self)
            env = tc.environment()
            env.define("FOO", "BAR")
            tc.generate(env)

You can also inspect default environment variables NMakeToolchain will inject in *conannmaketoolchain.sh|bat* script:

.. code:: python

    from conan import ConanFile
    from conan.tools.microsoft import NMakeToolchain

    class Pkg(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = NMakeToolchain(self)
            env_vars = tc.vars()
            cl_env_var = env_vars.get("CL")
