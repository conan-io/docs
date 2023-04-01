.. _conan_tools_b2_b2deps:

B2Deps
======

The ``B2Deps`` generator produces the necessary file for each dependency to be
able to use the dependency targets directly, and automatically.

It can be used by name in conanfiles:

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):
        generators = "B2Deps"

.. code-block:: text
    :caption: conanfile.txt

    [generators]
    B2Deps

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code:: python

    from conan import ConanFile
    from conan.tools.b2 import B2Deps

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            tc = B2Deps(self)
            tc.generate()


Generated files
---------------

- **conanbuildinfo.jam**: The B2Deps generator will create a common Jamfile that
  defines rules and include the variation specific `conanbuildinfo-XXX.jam`
  files.

- **conanbuildinfo-XXX.jam**: The B2Deps generator will create a variation
  specific Jamfile for each variation that matches the dependency settings.
  Each contains dependency subproject and targets for each dependency and
  components.

.. note::

    The definitions in both the *conanbuildinfo.jam* and
    *conanbuildinfo-XXX.jam* use names that are stable, and paths that are
    relative to ``CONAN_HOME``. Hence the files are stable and portable and can
    be checked into source control, or otherwise transported to other installs.
    And, assuming that the dependencies are installed they will work without
    changes nor needing to be regenerated.

Sub-projects in conanbuildinfo-XXX.jam
--------------------------------------

The B2Deps generator defines sub-projects relative to the location of the
B2 project you generate the Conan configuration. For each package a
sub-project with the package name is created that contains targets you can
use as B2 sources in your projects.

For example with this ``conanfile.txt``:

.. code-block:: text

    [requires]
    lyra/1.6.1
    fmt/9.1.0
    libdeflate/1.17

    [generators]
    B2Deps

You would get three sub-projects defined relative to the ``conanfile.txt``
location:

.. code-block:: text

    project lyra ;
    project fmt ;
    project libdeflate ;

For a root level project those could be referenced with an absolute project
path, for example */lyra*. Or you can use relative project paths as needed,
for example *../lyra* or *subproject/lyra*.

Targets in *conanbuildinfo-XXX.jam*
-----------------------------------

For each package targets in the corresponding package subproject are created
that are specific to the variant built. Each package can have multiple such
targets depending on the components it specifies and libraries it links. For
all packages there is a target with the same name as the package. For example a
*lyra//lyra* target. If the package has components a target for each of
component is defined. And for each system library needing to be link a target is
define.


Reference
---------


.. currentmodule:: conan.tools.b2

.. autoclass:: B2Deps
    :members:
