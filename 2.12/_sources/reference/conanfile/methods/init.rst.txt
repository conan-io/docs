.. _reference_conanfile_methods_init:


init()
======

This is an optional method for initializing conanfile values, designed for inheritance from ``python_requires``.
Assuming we have a ``base/1.1`` recipe:

.. code-block:: python
    :caption: base/conanfile.py

    from conan import ConanFile

    class MyConanfileBase:
        license = "MyLicense"
        settings = "os", # tuple!


    class PyReq(ConanFile):
        name = "base"
        version = "1.1"
        package_type = "python-require"


We could reuse and inherit from it with:

.. code-block:: python
    :caption: pkg/conanfile.py

    from conan import ConanFile

    class Pkg(ConanFile):
        license = "MIT"
        settings = "arch", # tuple!
        python_requires = "base/1.1"
        python_requires_extend = "base.MyConanfileBase"

        def init(self):
            base = self.python_requires["base"].module.MyConanfileBase
            self.settings = base.settings + self.settings  # Note, adding 2 tuples = tuple
            self.license = base.license  # License is overwritten


The final ``Pkg`` conanfile will have both ``os`` and ``arch`` as settings, and ``MyLicense`` as license.

To extend the ``options`` of the base class, it is necessary to call the ``self.options.update()`` method:


.. code-block:: python
    :caption: base/conanfile.py

    from conan import ConanFile

    class BaseConan:
        options = {"base": [True, False]}
        default_options = {"base": True}

    class PyReq(ConanFile):
        name = "base"
        version = "1.0.0"
        package_type = "python-require"


When the ``init()`` is called, the ``self.options`` object is already initialized. Then, updating the
``self.default_options`` is useless, and it is necessary to update the ``self.options`` with both the
base class options and the base class default options values:

.. code-block:: python
    :caption: pkg/conanfile.py

    from conan import ConanFile

    class DerivedConan(ConanFile):
        name = "derived"
        python_requires = "base/1.0.0"
        python_requires_extend = "base.BaseConan"
        options = {"derived": [True, False]}
        default_options = {"derived": False}

        def init(self):
            base = self.python_requires["base"].module.BaseConan
            # Note we pass the base options and default_options
            self.options.update(base.options, base.default_options) 


This method can also be useful if you need to unconditionally initialize class attributes like
``license`` or ``description`` or any other from datafiles other than
`conandata.yml`. For example, you can have a `json` file containing the information about the
``license``, ``description`` and ``author`` for the library:


.. code-block:: json
    :caption: data.json

    {"license": "MIT", "description": "This is my awesome library.", "author": "Me"}

Then, you can load that information from the ``init()``  method:

.. code-block:: python

    import os
    import json
    from conan import ConanFile
    from conan.tools.files import load


    class Pkg(ConanFile):
        exports = "data.json" # Important that it is exported with the recipe

        def init(self):
            data = load(self, os.path.join(self.recipe_folder, "data.json"))
            d = json.loads(data)
            self.license = d["license"]
            self.description = d["description"]
            self.author = d["author"]


.. note::

    **Best practices**

    - Try to keep your ``python_requires`` as simple as possible, and do not reuse attributes from them (the main need for the ``init()`` method), trying to avoid the complexity of this ``init()`` method. In general inheritance can have more issues than composition (or in other words "use composition over inheritance" as a general programming good practice), so try to avoid it if possible.
    - Do not abuse ``init()`` for other purposes other than listed here, nor use the Python private ``ConanFile.__init__`` constructor.
    - The ``init()`` method executes at recipe load time. It cannot contain conditionals on settings, options, conf, or use any dependencies information other than the above ``python_requires``.
