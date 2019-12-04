.. _python_requires:

Python requires: reusing conanfile.py code 
==========================================

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.


.. note::

    This syntax supersedes the legacy ``python_requires()`` syntax. The most important changes
    are:

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
different recipes. A *Python Requires* is similar to any other recipe, it is the way it is
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


How python-requires are resolved
------------------------------------
- Global import, reused
- Version ranges
- private
- Conflicts
- No user/channel
- Can import other python files
- Can editable

