.. _reference_extensions_python_requires:

Python requires
===============


Introduction
------------

The ``python_requires`` feature is a very convenient way to share files and code between
different recipes. A python require is a special recipe that does not create packages and
it is just intended to be reused by other recipes.

A very simple recipe that we want to reuse could be:

.. code-block:: python
    
    from conan import ConanFile

    myvar = 123

    def myfunct():
        return 234

    class Pkg(ConanFile):
        name = "pyreq"
        version = "0.1"
        package_type = "python-require"

     
And then we will make it available to other packages with ``conan create .``. Note that a ``python-require``
package does not create binaries, it is just the recipe part.

.. code-block:: bash

    $ conan create .
    # It will only export the recipe, but will NOT create binaries
    # python-requires do NOT have binaries


We can reuse the above recipe functionality declaring the dependency in the ``python_requires``
attribute and we can access its members using ``self.python_requires["<name>"].module``:

.. code-block:: python
    
    from conan import ConanFile

    class Pkg(ConanFile):
        name = "pkg"
        version = "0.1"
        python_requires = "pyreq/0.1"

        def build(self):  
            v = self.python_requires["pyreq"].module.myvar  # v will be 123
            f = self.python_requires["pyreq"].module.myfunct()  # f will be 234
            self.output.info(f"{v}, {f}")


.. code-block:: bash

    $ conan create . 
    ...
    pkg/0.1: 123, 234


Python requires can also use version ranges, and this can be recommended in many cases if those ``python-requires``
need to evolve over time:

.. code-block:: python
    
    from conan import ConanFile

    class Pkg(ConanFile):
        python_requires = "pyreq/[>=1.0 <2]"


It is also possible to require more than 1 ``python-requires`` with ``python_requires = "pyreq/0.1", "other/1.2"``

Extending base classes
----------------------

A common use case would be to declare a base class with methods we want to reuse in several
recipes via inheritance. We'd write this base class in a python-requires package: 

.. code-block:: python

    from conan import ConanFile

    class MyBase:
        def source(self):
            self.output.info("My cool source!")
        def build(self):
            self.output.info("My cool build!")
        def package(self):
            self.output.info("My cool package!")
        def package_info(self):
            self.output.info("My cool package_info!")

    class PyReq(ConanFile):
        name = "pyreq"
        version = "0.1"
        package_type = "python-require"


And make it available for reuse with:

.. code-block:: bash

    $ conan create .


Note that there are two classes in the recipe file:

 * ``MyBase`` is the one intended for inheritance and doesn't extend ``ConanFile``.
 * ``PyReq`` is the one that defines the current package being exported, it is the recipe
   for the reference ``pyreq/0.1``.


Once the package with the base class we want to reuse is available we can use it in other
recipes to inherit the functionality from that base class. We'd need to declare the
``python_requires`` as we did before and we'd need to tell Conan the base classes to use
in the attribute ``python_requires_extend``. Here our recipe will inherit from the
class ``MyBase``:


.. code-block:: python
    
    from conan import ConanFile

    class Pkg(ConanFile):
        name = "pkg"
        version = "0.1"
        python_requires = "pyreq/0.1"
        python_requires_extend = "pyreq.MyBase"


The resulting inheritance is equivalent to declare our ``Pkg`` class as ``class Pkg(pyreq.MyBase, ConanFile)``.
So creating the package we can see how the methods from the base class are reused:

.. code-block:: bash

    $ conan create .
    ...
    pkg/0.1: My cool source!
    pkg/0.1: My cool build!
    pkg/0.1: My cool package!
    pkg/0.1: My cool package_info!
    ...


In general, base class attributes are not inherited, and should be avoided as much as possible.
There are method alternatives to some of them like ``export()`` or ``set_version()``.
For exceptional situations, see the ``init()`` method documentation for more information to extend inherited attributes.

It is possible to re-implement some of the base class methods, and also to call the base class 
method explicitly, with the Python ``super()`` syntax:

.. code-block:: python
    
    from conan import ConanFile

    class Pkg(ConanFile):
        name = "pkg"
        version = "0.1"
        python_requires = "pyreq/0.1"
        python_requires_extend = "pyreq.MyBase"

        def source(self):
            super().source()  # call the base class method
            self.output.info("MY OWN SOURCE") # Your own implementation

It is not mandatory to call the base class method, a full overwrite without calling ``super()`` is possible. Also the call order can be changed, and calling your own code, then ``super()`` is possible.

            
Reusing files
-------------

It is possible to access the files exported by a recipe that is used with ``python_requires``.
We could have this recipe, together with a *myfile.txt* file containing the "Hello" text.

.. code-block:: python

    from conan import ConanFile

    class PyReq(ConanFile):
        name = "pyreq"
        version = "1.0"
        package_type = "python-require"
        exports = "*"


.. code-block:: bash

    $ echo "Hello" > myfile.txt
    $ conan create .


Now that the python-require has been created, we can access its path (the place where *myfile.txt* is) with the
``path`` attribute:

.. code-block:: python

    import os

    from conan import ConanFile
    from conan.tools.files import load

    class Pkg(ConanFile):
        python_requires = "pyreq/0.1"

        def build(self):
            pyreq_path = self.python_requires["pyreq"].path
            myfile_path = os.path.join(pyreq_path, "myfile.txt")
            content = load(self, myfile_path)  # content = "Hello"
            self.output.info(content)
            # we could also copy the file, instead of reading it


Note that only ``exports`` works for this case, but not ``exports_sources``.


Testing python-requires
-----------------------

It is possible to test with ``test_package`` a ``python_require``, by adding a ``test_package/conanfile.py``:

.. code-block:: python
    :caption: conanfile.py

    from conan import ConanFile

    def mynumber():
        return 42

    class PyReq(ConanFile):
        name = "pyreq"
        version = "1.0"
        package_type = "python-require"


.. code-block:: python
    :caption: test_package/conanfile.py

    from conan import ConanFile

    class Tool(ConanFile):
        def test(self):
            pyreq = self.python_requires["pyreq"].module
            mynumber = pyreq.mynumber()
            self.output.info("{}!!!".format(mynumber))


Note that the ``test_package/conanfile.py`` does not need any type of declaration of the ``python_requires``, this is done
automatically and implicitly. We can now create and test it with:

.. code-block:: bash
    
    $ conan create .
    ...
    pyreq/0.1 (test package): 42!!!


Effect in package_id
--------------------

The ``python_requires`` will affect the ``package_id`` of the **consumer packages** using those dependencies.
By default, the policy is ``minor_mode``, which means:

- Changes to the **patch** version of the **revision** of a python-require will not affect the package ID. So depending
  on ``"pyreq/1.2.3"`` or ``"pyreq/1.2.4"`` will result in identical package ID (both will be mapped
  to ``"pyreq/1.2.Z"`` in the hash computation). Bump the patch version if you want to change your
  common code, but you don't want the consumers to be affected or to fire a re-build of the dependants.
- Changes to the **minor** version will produce a different package ID. So if you depend
  on ``"pyreq/1.2.3"``, and you bump the version to ``"pyreq/1.3.0"``, then, you will need to build
  new binaries that are using that new python-require. Bump the minor or major version if you want to
  make sure that packages requiring this python-require will be built using these changes in the code.

In most cases using a version-range ``python_requires = "pyreq/[>=1.0 <2.0]"`` is the right approach, because that means
the **major** version bumps are not included because they would require changes in the consumers themselves. It is then
possible to release a new major version of the ``pyreq/2.0``, and have consumers gradually change their requirements to
``python_requires = "pyreq/[>=2.0 <3.0]"``, fix the recipes, and move forward without breaking the whole project.

As with the regular ``requires``, this default can be customized with the ``core.package_id:default_python_mode`` configuration. 

It is also possible to customize the effect of ``python_requires`` per package, using the ``package_id()``
method:

  .. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        python_requires ="pyreq/[>=1.0]"
        def package_id(self):
            self.info.python_requires.patch_mode()



Resolution of python_requires
-----------------------------

There are few important things that should be taken into account when using ``python_requires``:

- Python requires recipes are loaded by the interpreter just once, and they are common to
  all consumers. Do not use any global state in the ``python_requires`` recipes.
- Python requires are private to the consumers. They are not transitive. Different consumers
  can require different versions of the same ``python-require``. Being private, they cannot
  be overridden from downstream in any way.
- ``python_requires`` cannot use regular ``requires`` or ``tool_requires``.
- ``python_requires`` cannot be "aliased".
- ``python_requires`` can use native python ``import`` to other python files, as long as these are
  exported together with the recipe.
- ``python_requires`` can be used as editable packages too.
- ``python_requires`` are locked in lockfiles, to guarantee reproducibility, in the same way that other ``requires`` and ``tool_requires`` are locked.


.. note:: 

  **Best practices**

  - Even if ``python-requires`` can ``python_requires`` transitively other ``python-requires`` recipes, this is discouraged. Multiple level inheritance and reuse can become quite complex and difficult to manage, it is recommended to keep the hierarchy flat. 
  - Do not try to mix Python inheritance with ``python_requires_extend`` inheritance mechanisms, they are incompatible and can break.
  - Do not use multiple inheritance for ``python-requires``
