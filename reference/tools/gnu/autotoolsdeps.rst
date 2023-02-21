.. _conan_tools_gnu_autotoolsdeps:

AutotoolsDeps
=============

The ``AutotoolsDeps`` is the dependencies generator for Autotools. It will generate shell scripts containing
environment variable definitions that the autotools build system can understand.

It can be used by name in conanfiles:

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

    from conan import ConanFile
    from conan.tools.gnu import AutotoolsDeps

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = AutotoolsDeps(self)
            tc.generate()


Generated files
---------------

It will generate the file ``conanautotoolsdeps.sh`` or ``conanautotoolsdeps.bat``:

.. code-block:: bash

    $ conan install conanfile.py # default is Release
    $ source conanautotoolsdeps.sh
    # or in Windows
    $ conanautotoolsdeps.bat

These launchers will define aggregated variables ``CPPFLAGS``, ``LIBS``, ``LDFLAGS``, ``CXXFLAGS``, ``CFLAGS`` that
accumulate all dependencies information, including transitive dependencies, with flags like ``-I<path>``, ``-L<path>``, etc.

At this moment, only the ``requires`` information is generated, the ``tool_requires`` one is not managed by this generator yet.


Customization
-------------

To modify the computed values, you can access the ``.environment`` property that returns an
:ref:`Environment<conan_tools_env_environment_model>` class.


.. code:: python

    from conan import ConanFile
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


Reference
---------

.. currentmodule:: conan.tools.gnu.autotoolsdeps

.. autoclass:: AutotoolsDeps
    :members:

