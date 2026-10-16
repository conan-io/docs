AutotoolsDeps
=============

.. warning::

    These tools are still **experimental** (so subject to breaking changes) but with very stable syntax.
    We encourage the usage of it to be prepared for Conan 2.0.


The ``AutotoolsDeps`` is the dependencies generator for Autotools. It will generate shell scripts containing
environment variable definitions that the autotools build system can understand.

.. important::

    This class will require very soon to define both the "host" and "build" profiles. It is very recommended to
    start defining both profiles immediately to avoid future breaking. Furthermore, some features, like trying to
    cross-compile might not work at all if the "build" profile is not provided.


The ``AutotoolsDeps`` generator can be used by name in conanfiles:

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):
        generators = "AutotoolsDeps"

.. code-block:: text
    :caption: conanfile.txt

    [generators]
    AutotoolsDeps

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code:: python

    from conans import ConanFile
    from conan.tools.gnu import AutotoolsDeps

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = AutotoolsDeps(self)
            tc.generate()

The ``AutotoolsDeps`` will generate after a ``conan install`` command the *conanautotoolsdeps.sh* or *conanautotoolsdeps.bat* files:

.. code-block:: bash

    $ conan install conanfile.py # default is Release
    $ source conanautotoolsdeps.sh
    # or in Windows
    $ conanautotoolsdeps.bat

This generator will define aggregated variables ``CPPFLAGS``, ``LIBS``, ``LDFLAGS``, ``CXXFLAGS``, ``CFLAGS`` that
accumulate all dependencies information, including transitive dependencies, with flags like ``-I<path>``, ``-L<path>``, etc.

At this moment, only the ``requires`` information is generated, the ``tool_requires`` one is not managed by this generator yet.


Attributes
++++++++++

* **environment** : :ref:`Environment<conan_tools_env_environment_model>` object containing the computed variables. If you need
  to modify some of the computed values you can access to the ``environment`` object.

.. code:: python

    from conans import ConanFile
    from conan.tools.gnu import AutotoolsDeps

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = AutotoolsDeps(self)
            tc.environment.remove("CPPFLAGS", "undesired_value")
            tc.environment.append("CPPFLAGS", "var")
            tc.environment.define("OTHER", "cat")
            tc.environment.unset("LDFLAGS")
            tc.generate()
