.. _reference_commands_custom_generators:

Custom Conan generators
=======================

In the case that you need to use a build system or tool that is not supported by Conan
off-the-shelf, you could create your own custom integrations using a custom generator.
This can be done in two different ways.

Custom generators as python_requires
------------------------------------

One way of having your own custom generators in Conan is by using them as
:ref:`python_requires<reference_extensions_python_requires>`. You could declare a
*MyGenerator* class with all the logic to generate some files inside the *mygenerator/1.0*
`python_requires` package:

.. code-block:: python

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


    class PyReq(ConanFile):
        name = "mygenerator"
        version = "1.0"
        package_type = "python-require"


And then use it in the generate method of your own packages like this:

.. code-block:: python

    from conan import ConanFile


    class MyPkg(ConanFile):
        name = "pkg"
        version = "1.0"

        python_requires = "mygenerator/1.0"
        requires = "zlib/1.2.11"

        def generate(self):
            mygenerator = self.python_requires["mygenerator"].module.MyGenerator
            mygenerator.generate(self)

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
