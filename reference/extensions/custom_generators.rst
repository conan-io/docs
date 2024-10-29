.. _reference_commands_custom_generators:

Custom Conan generators
=======================

In the case that you need to use a build system or tool that is not supported by Conan
off-the-shelf, you could create your own custom integrations using a custom generator.
This can be done in three different ways.

Custom generators as python_requires
------------------------------------

One way of having your own custom generators in Conan is by using them as
:ref:`python_requires<reference_extensions_python_requires>`. You could declare a
*MyGenerator* class with all the logic to generate some files inside the *mygenerator/1.0*
`python_requires` package:

.. code-block:: python
    :caption: mygenerator/conanfile.py

    from conan import ConanFile
    from conan.tools.files import save


    class MyGenerator:
        def __init__(self, conanfile):
            self._conanfile = conanfile

        def generate(self):
            deps_info = ""
            for dep, _ in self._conanfile.dependencies.items():
                deps_info += f"{dep.ref.name}, {dep.ref.version}\n"
            save(self._conanfile, "deps.txt", deps_info)


    class PyReq(ConanFile):
        name = "mygenerator"
        version = "1.0"
        package_type = "python-require"


And then ``conan create mygenerator`` and use it in the generate method of your own packages like this:

.. code-block:: python
    :caption: pkg/conanfile.py

    from conan import ConanFile


    class MyPkg(ConanFile):
        name = "pkg"
        version = "1.0"

        python_requires = "mygenerator/1.0"
        requires = "zlib/1.2.11", "bzip2/1.0.8"

        def generate(self):
            mygenerator = self.python_requires["mygenerator"].module.MyGenerator(self)
            mygenerator.generate()

Then, doing a ``conan install pkg`` on this ``pkg`` recipe, will create a ``deps.txt`` text file containing:

.. code-block:: text

    zlib, 1.2.11
    bzip2, 1.0.8


This has the advantage that you can version your own custom generators as packages and
also that you can share those generators as Conan packages.

Using global custom generators
------------------------------

You can also use your custom generators globally if you store them in the
``[CONAN_HOME]/extensions/generators`` folder. You can place them directly in that folder
or install with the ``conan config install`` command.

.. code-block:: python
    :caption: [CONAN_HOME]/extensions/generators/mygen.py
    
    from conan.tools.files import save


    class MyGenerator:
        def __init__(self, conanfile):
            self._conanfile = conanfile

        def generate(self):
            deps_info = ""
            for dep, _ in self._conanfile.dependencies.items():
                deps_info = f"{dep.ref.name}, {dep.ref.version}"
            save(self._conanfile, "deps.txt", deps_info)

Then you can use them by name in the recipes or in the command line using the *-g*
argument:

.. code-block:: bash

    conan install --requires=zlib/1.2.13 -g MyGenerator


.. _reference_commands_custom_generators_tool_requires:

Generators from tool_requires
-----------------------------

.. include:: ../../common/experimental_warning.inc

A direct dependency tool requires can also be used to provide custom generators.
The following example shows how to create a custom generator that generates a file with the
dependencies of the package, just like the example above, but using a ``tool_require`` instead of a ``python_require``
to inject the generator into the recipe, by adding them to the ``self.generators_info`` list inside the ``package_info`` method.

.. code-block:: python
    :caption: mygenerator/conanfile.py

    from conan import ConanFile
    from conan.tools.files import save

    class MyGenerator:
        def __init__(self, conanfile):
            self._conanfile = conanfile

        def generate(self):
            deps_info = ""
            for dep, _ in self._conanfile.dependencies.items():
                deps_info = f"{dep.ref.name}, {dep.ref.version}"
            save(self._conanfile, "deps.txt", deps_info)

    class MyToolReq(ConanFile):
        name = "mygenerator-tool"
        version = "1.0"

        def package_info(self):
            self.generators_info.append(MyGenerator)

And then having a ``tool_requires`` in your recipe for the ``mygenerator-tool`` package will automatically
inject the generator into the recipe.

.. note::

    Note that built-in generators can also be injected using tool_requires,
    by adding them by name: ``self.generators_info.append("CMakeDeps")``.
    ``tool_require``ing this package will inject the ``CMakeDeps`` generator into the recipe
    just as if it was declared in its ``generators`` attribute.
