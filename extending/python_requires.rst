.. _python_requires:

Python requires: reusing python code in recipes
===============================================
.. warning::

    This is an EXPERIMENTAL feature released in 1.7. Subject to breaking changes.

The ``python_requires()`` feature allows to reuse python from other conanfile.py recipes easily, even for inheritance approaches.
The code to be reused will be in a *conanfile.py* recipe, and will be managed as any other conan package. Let's create for example
some reusable base class:

.. code-block:: python

    from conans import ConanFile

    class MyBase(ConanFile):
        def source(self):
            self.output.info("My cool source!")
        def build(self):
            self.output.info("My cool build!")
        def package(self):
            self.output.info("My cool package!")
        def package_info(self):
            self.output.info("My cool package_info!")

With this conanfile, we can export it to the local cache to make it available, and also upload to our remote:

.. code-block:: bash

    $ conan export . MyBase/0.1@user/channel
    $ conan upload MyBase/0.1@user/channel -r=myremote

It is not necessary to "create" any package binaries, or to ``upload --all``, because there are no binaries for this recipe.

Now, using the ``python_requires()`` we can write a new package recipe like:

.. code-block:: python

    from conans import python_requires
    
    base = python_requires("MyBase/0.1@user/channel")

    class PkgTest(base.MyBase):
        pass

If we run a ``conan create``, of this recipe, we can see how it is effectively reusing the above code:

.. code-block:: bash

    $ conan create . Pkg/0.1@user/channel

    Pkg/0.1@lasote/testing: Installing package
    Requirements
        Pkg/0.1@lasote/testing from local cache - Cache
    Python requires
        MyConanfileBase/1.1@lasote/testing
    Packages
        Pkg/0.1@lasote/testing:5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9 - Build
    ...
    Pkg/0.1@lasote/testing: Configuring sources 
    Pkg/0.1@lasote/testing: My cool source!
    ...
    Pkg/0.1@lasote/testing: Calling build()
    Pkg/0.1@lasote/testing: My cool build!
    ...
    Pkg/0.1@lasote/testing: Calling package()
    Pkg/0.1@lasote/testing: My cool package!
    ...
    Pkg/0.1@lasote/testing: My cool package_info!


It is not compulsory to extend the reused ``MyBase`` class, it is possible to reuse just functions too:

.. code-block:: python

    from conans import ConanFile

    def my_build(settings):
        # doing custom stuff based on settings

    class MyBase(ConanFile):
        pass

.. code-block:: bash

    $ conan export . MyBuild/0.1@user/channel
    $ conan upload MyBuild/0.1@user/channel -r=myremote

.. code-block:: python

    from conans import ConanFile, python_requires
    
    base = python_requires("MyBuild/0.1@user/channel")

    class PkgTest(ConanFile):
        ...
        def build(self):
            base.my_build(self.settings)


Version ranges are possible with the version ranges notation ``[]``, similar to regular requirements.
Multiple ``python_requires()`` are also possible

.. code-block:: python
    :caption: **conanfile.py**

    from conans import python_requires
    
    base = python_requires("MyBase/[~0.1]@user/channel")
    other = python_requires("Other/1.2@user/channel")

    class Pkg(base.MyBase):
        def source(self):
            other.some_function()

It is possible to structure the code in different files too:

.. code-block:: python
    :caption: **conanfile.py**

    from conans import ConanFile
    import mydata # reuse the strings from here
    class MyConanfileBase(ConanFile):
        exports = "*.py"
        def source(self):
            self.output.info(mydata.src)

.. code-block:: python
    :caption: **mydata.py**

    src = "My cool source!"
    build = "My cool build!"
    pkg = "My cool package!"
    info = "My cool package_info!"

This would be created with the same ``conan export`` and consumed with the same ``base = python_requires("MyBase/0.1@user/channel")`` as above.



There are a few important considerations regarding ``python_requires()``:

- They are required at every step of the conan commands. If you are creating a package that ``python_requires("MyBase/...")``,
  the ``MyBase`` package should be already available in the local cache or to be downloaded from the remotes. Otherwise, conan
  will raise a "missing package" error.
- They do not affect the package binary ID (hash). Depending on different version, or different channel of
  such ``python_requires()`` do not change the package IDs as the normal dependencies do.
- They are imported only once. The python code that is reused is imported only once, the first time it is required.
  Subsequent requirements of that conan recipe will reuse the previously imported module. Global initialization at
  parsing time and global state are discouraged.
- They are transitive. One recipe using ``python_requires()`` can be also consumed with a ``python_requires()`` from
  another package recipe.
- They are not automatically updated with the ``--update`` argument from remotes.
- Different packages can require different versions in their ``python_requires()``. They are private to each recipe,
  so they do not conflict with each other, but it is the responsibility of the user to keep consistency.
- They are not overridden from downstream consumers. Again, as they are private, they are not affected by other packages,
  even consumers

