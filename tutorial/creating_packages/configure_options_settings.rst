Configure settings and options in recipes
=========================================

.. important::

    In this example, we retrieve the CMake Conan package from a Conan repository with
    packages compatible with Conan 2.0. To run this example successfully you should add this
    remote to your Conan configuration (if did not already do it) doing:
    ``conan remote add conanv2 https://conanv2beta.jfrog.io/artifactory/api/conan/conan --index 0``

We already explained what :ref:`Conan settings and options
are<settings_and_options_difference>` and how to use them to build your projects for
different configurations like Debug, Release, with static or shared libraries, etc. In
this section, we explain how to configure these settings and options for example, in the
case that a certain setting or option does not apply to a Conan recipe. We will also give a
short introduction on how Conan models binary compatibility and how that relates to
options and settings.

Please, first clone the sources to recreate this project. You can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/configure_options_settings

You will notice some changes in the `conanfile.py` file from the previous recipe.
Let's check the relevant parts:

.. code-block:: python
    :emphasize-lines: 12,16,20,27,30,35

    ...
    from conan.tools.build import check_min_cppstd
    ...

    class helloRecipe(ConanFile):
        name = "hello"
        version = "1.0"

        ...
        options = {"shared": [True, False], 
                   "fPIC": [True, False],
                   "with_fmt": [True, False]}

        default_options = {"shared": False, 
                           "fPIC": True,
                           "with_fmt": True}
        ...

        def config_options(self):
            if self.settings.os == "Windows":
                del self.options.fPIC
            #del self.settings.compiler.cppstd
            #del self.settings.compiler.libcxx

        def configure(self):
            if self.options.shared:
                del self.options.fPIC
        ...


You can see that we added a ``configure()`` method to the recipe. Let's explain what's the
objective of this method and how it's different from the ``config_options()`` method we
already had defined in our recipe:

* ``configure()``: this method is useful to modify the available options or settings of
  the recipe depending on the value of one option. For example, in this case, we **delete
  the fPIC option**, because it should only be True if we are building the library as
  shared. In fact, some build systems will add this flag automatically when building a
  shared library.


* ``config_options()``: this method is executed before the ``configure()`` method. In
  fact, options are not given a value yet in this method. This method is used to
  constraint the available options in a package, before they are given a value. So when a
  value is tried to be assigned it will raise an error. In this case we are **deleting the
  fPIC option** in Windows because that option does not exist for that operating system.

Be aware that deleting an option in the ``config_options()`` or in the ``configure()`` has
not the same result. Deleting it in the ``config_options()`` is like if we never had
declared it in the recipe and it will raise an exception saying that the option does not
exist. Nevertheless, if we delete it in the ``configure()`` method we can pass the option
but it will just have no effect.


- Que quiere decir borrar un setting o una opción?




Read more
---------

- 