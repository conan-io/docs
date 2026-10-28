.. _python_requires:

Python requires
===============

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.


.. note::

    This syntax supersedes the :ref:`legacy python_requires()<python_requires_legacy>` syntax. 
    The most important changes are:

    - These new python_requires affect the consumers ``package_id``. So different binaries can
      be managed, and CI systems can re-build affected packages according to package ID modes and
      versioning policies.
    - The syntax defines a *class attribute* instead of a module function call, so recipes are
      cleaner and more aligned with other types of requirements.
    - The new python_requires will play better with lockfiles and deterministic dependency graphs.
    - They are able to extend base classes more naturally without conflicts of ConanFile classes. 



Introduction
------------

The ``python_requires`` feature is a very convenient way to share files and code between
different recipes. A python requires is similar to any other recipe, it is the way it is
required from the consumer what makes the difference. 

A very simple recipe that we want to reuse could be:

.. code-block:: python
    
    from conans import ConanFile

    myvar = 123

    def myfunct():
        return 234

    class Pkg(ConanFile):
        pass
     
And then we will make it available to other packages with ``conan export``. Note that we are 
not calling ``conan create``, because this recipe doesn't have binaries. It is just the python
code that we want to reuse.

.. code-block:: bash

    $ conan export . pyreq/0.1@user/channel


We can reuse the above recipe functionality with:

.. code-block:: python
    
    from conans import ConanFile

    class Pkg(ConanFile):
        python_requires = "pyreq/0.1@user/channel"

        def build(self):  
            v = self.python_requires["pyreq"].module.myvar  # v will be 123
            f = self.python_requires["pyreq"].module.myfunct()  # f will be 234
            self.output.info("%s,%s" % (v, f))

.. code-block:: bash

    $ conan create . pkg/0.1@user/channel
    ...
    pkg/0.1@user/channel: 123, 234


It is also possible to require more than one python-require, and use the package name
to address the functionality:

.. code-block:: python
    
    from conans import ConanFile

    class Pkg(ConanFile):
        python_requires = "pyreq/0.1@user/channel", "other/1.2@user/channel"

        def build(self):  
            v = self.python_requires["pyreq"].module.myvar  # v will be 123
            f = self.python_requires["other"].module.otherfunc("some-args")


Extending base classes
----------------------

A common use case would be to reuse methods of a base class. So we could write a recipe like:

.. code-block:: python

    from conans import ConanFile

    class MyBase(object):
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

And make it available for reuse with:

.. code-block:: bash

    $ conan export . user/channel


Note that there are 2 classes, ``MyBase`` is the one intended for inheritance, and do not
extend ``ConanFile``. The other ``PyReq`` is the one that defines the current package being
exported.

Now, other packages, could ``python_require`` it, and inherit from ``MyBase`` class with:

.. code-block:: python
    
    from conans import ConanFile

    class Pkg(ConanFile):
        python_requires = "pyreq/0.1@user/channel"
        python_requires_extend = "pyreq.MyBase"


So creating the package we can see how the methods from the base class are reused:

.. code-block:: bash

    $ conan create . pkg/0.1@user/channel
    ...
    pkg/0.1@user/channel: My cool source!
    pkg/0.1@user/channel: My cool build!
    pkg/0.1@user/channel: My cool package!
    pkg/0.1@user/channel: My cool package_info!
    ...

If there is extra logic needed to extend from a base class, like composing the base class settings
with the current recipe, the ``init()`` method can be used for it:

.. code-block:: python

    class PkgTest(ConanFile):
        license = "MIT"
        settings = "arch", # tuple!
        python_requires = "base/1.1@user/testing"
        python_requires_extend = "base.MyConanfileBase"

        def init(self):
            base = self.python_requires["base"].module.MyConanfileBase
            self.settings = base.settings + self.settings  # Note, adding 2 tuples = tuple
            self.license = base.license  # License is overwritten


For more information about the ``init()`` method visit :ref:`method_init`


Limitations
+++++++++++

There are a few limitations that should be taken into account:

- ``name`` and ``version`` fields shouldn't be inherited. ``set_name()`` and ``set_version()``
  might be used.
- ``short_paths`` cannot be inherited from a ``python_requires``. Make sure to specify it directly
  in the recipes that need the paths shortened in Windows.
- ``exports``, ``exports_sources`` shouldn't be inherited from a base class, but explictly defined
  directly in the recipes. A reusable alternative might be using the ``SCM`` component.
- ``build_policy`` shouldn't be inherited from a base class, but explictly defined
  directly in the recipes.


Reusing files
-------------

It is possible to access the files exported by a recipe that is used with ``python_requires``.
We could have this recipe, together with a *myfile.txt* file containing the "Hello" text.

.. code-block:: python

    from conans import ConanFile

    class PyReq(ConanFile):
        exports = "*"

.. code-block:: bash

    $ echo "Hello" > myfile.txt
    $ conan export . pyreq/0.1@user/channel


Now the recipe has been exported, we can access its path (the place where *myfile.txt* is) with the
``path`` attribute:

.. code-block:: python

    import os
    from conans import ConanFile, load

    class Pkg(ConanFile):
        python_requires = "pyreq/0.1@user/channel"

        def build(self):
            pyreq_path = self.python_requires["pyreq"].path
            myfile_path = os.path.join(pyreq_path, "myfile.txt")
            content = load(myfile_path)  # content = "Hello"
            self.output.info(content)
            # we could also copy the file, instead of reading it


Note that only ``exports`` work for this case, but not ``exports_sources``.

PackageID
---------

The ``python-requires`` will affect the ``package_id`` of the packages using those dependencies.
By default, the policy is ``minor_mode``, which means:

- Changes to the **patch** version of a python-require will not affect the package ID. So depending
  on ``"pyreq/1.2.3"`` or ``"pyreq/1.2.4"`` will result in identical package ID (both will be mapped
  to ``"pyreq/1.2.Z"`` in the hash computation). Bump the patch version if you want to change your
  common code, but you don't want the consumers to be affected or to fire a re-build of the dependants.
- Changes to the **minor** or **major** version will produce a different package ID. So if you depend
  on ``"pyreq/1.2.3"``, and you bump the version to ``"pyreq/1.3.0"``, then, you will need to build
  new binaries that are using that new python-require. Bump the minor or major version if you want to
  make sure that packages requiring this python-require will be built using these changes in the code.
- Both changing the **minor** and **major** requires a new package ID, and then a build from source.
  You could use changes in the **minor** to indicate that it should be source compatible, and consumers
  wouldn't need to do changes, and changes in the **major** for source incompatible changes.

As with the regular ``requires``, this default can be customized. First you can customize it at attribute
global level, modifying the *conan.conf* ``[general]`` variable ``default_python_requires_id_mode``, which can take the values
``unrelated_mode``, ``semver_mode``, ``patch_mode``, ``minor_mode``, ``major_mode``, ``full_version_mode``,
``full_recipe_mode`` and ``recipe_revision_mode``. 


For example, if you want to make the package IDs never be affected by any change in the versions of
python-requires, you could do:

.. code-block:: text
   :caption: *conan.conf* configuration file

   [general]
   default_python_requires_id_mode=unrelated_mode


Read more about these modes in :ref:`package_id_mode`.

It is also possible to customize the effect of ``python_requires`` per package, using the ``package_id()``
method:

  .. code-block:: python

    from conans import ConanFile

    class Pkg(ConanFile):
        python_requires ="pyreq/[>=1.0]"
        def package_id(self):
            self.info.python_requires.patch_mode()


Resolution of python-requires
-----------------------------

There are few things that should be taken into account when using ``python-requires``:

- Python requires recipes are loaded by the interpreter just once, and they are common to
  all consumers. Do not use any global state in the ``python-requires`` recipes.
- Python requires are private to the consumers. They are not transitive. Different consumers
  can require different versions of the same python-require.
- ``python-requires`` can use version ranges expressions.
- ``python-requires`` can ``python-require`` other recipes too, but this should probably be limited
  to very few cases, we recommend to use the simplest possible structure.
- ``python-requires`` can conflict if they require other recipes and create conflicts in different
  versions.
- ``python-requires`` cannot use regular ``requires`` or ``build_requires``.
- It is possible to use ``python-requires`` without user and channel.
- ``python-requires`` can use native python ``import`` to other python files, as long as these are
  exported together with the recipe.
- ``python-requires`` should not create packages, but use ``export`` only.
- ``python-requires`` can be used as editable packages too.
- ``python-requires`` are locked in lockfiles.
