.. _python_reuse:

How to reuse python code in recipes
=====================================

First, if you feel that you are repeating a lot of python code, and that repeated code could be
useful for other conan users, please propose it in a github issue.

There are several ways to handle python code reuse in package recipes:

- To put common code in files, as explained in :ref:`the reference <split_conanfile>`. This code
  has to be exported into the recipe itself
  
- To create a conan package with the common python code, and then ``require`` it from the recipe.

This howto explains the latter.

A basic python package
-----------------------

Let's begin with a simple python package, a "hello world" functionality that we want to package and reuse:

..  code-block:: python

    def hello():
        print("Hello World from Python!")

To create a package, all we need to do is create the following layout:

..  code-block:: txt

    -| hello.py
     | __init__.py
     | conanfile.py


The ``__init__.py`` is blank.
It is not necessary to compile code, so the package recipe ``conanfile.py`` is quite simple:


..  code-block:: python

    from conans import ConanFile
    
    class HelloPythonConan(ConanFile):
        name = "HelloPy"
        version = "0.1"
        exports = '*'
        build_policy = "missing"
    
        def package(self):
            self.copy('*.py')
    
        def package_info(self):
            self.env_info.PYTHONPATH.append(self.package_folder)


The ``exports`` will copy both the ``hello.py`` and the ``__init__.py`` into the recipe. The ``package()`` method is also obvious: to construct the package just copy the python sources.


The ``package_info()`` adds the current package folder to the ``PYTHONPATH`` conan environment variable. It will not affect the real environment variable unless the end user want it.


It can be seen that this recipe would be practically the same for most python packages, so it could be factored in a ``PythonConanFile`` base class to further simplify it (open a feature request, or better a pull request :) ) 


With this recipe, all we have to do is:


..  code-block:: bash

    $ conan export memsharded/testing
    $ conan search


Of course if you want to share the package with your team, you can ``conan upload`` it to a remote server. But to create and test the package, we can do everything locally.

Now the package is ready for consumption. In another folder, we can create a ``conanfile.txt`` (or a ``conanfile.py`` if we prefer):

..  code-block:: txt

    [requires]
    HelloPy/0.1@memsharded/testing


And install it with the following command:


..  code-block:: bash

    $ conan install -g virtualenv


Creating the above ``conanfile.txt`` might be unnecessary for this simple example, as you can directly run ``conan install HelloPy/0.1@memsharded/testing -g virtualenv``, however, using the file is the canonical way.


The specified ``virtualenv`` generator will create an ``activate`` script (in Windows ``activate.bat``), that basically contains the environment, in this case, the ``PYTHONPATH``. Once we activate it, we are able to find the package in the path and use it:


..  code-block:: bash

    $ activate
    $ python
    Python 2.7.12 (v2.7.12:d33e0cf91556, Jun 27 2016, 15:19:22) [MSC v.1500 32 bit (Intel)] on win32
    ...
    >>> import hello
    >>> hello.hello()
    Hello World from Python!
    >>>


The above shows an interactive session, but you can import also the functionality in a regular python script.


Reusing python code in your recipes
------------------------------------

As the conan recipes are python code itself, it is easy to reuse python packages in them. A basic recipe using the created package would be:

..  code-block:: python

    from conans import ConanFile, tools
    
    class HelloPythonReuseConan(ConanFile):
        requires = "HelloPy/0.1@memsharded/testing"
    
        def build(self):
            with tools.pythonpath(self):
                from hello import hello
                hello()



The ``requires`` section is just referencing the previously created package. The functionality of that package can be used in several methods of the recipe: ``source()``, ``build()``, ``package()`` and ``package_info()``, i.e. all of the methods used for creating the package itself. Note that in other places it is not possible, as it would require the dependencies of the recipe to be already retrieved, and such dependencies cannot be retrieved until the basic evaluation of the recipe has been executed.


In the above example, the code is reused in the ``build()`` method as an example. Note the use of a helper context, which basically activates/deactivates the ``PYTHONPATH`` environment variable with the value assigned in the package. We didn't want to do this activation implicit for all conan packages, but rather make it explicit.


..  code-block:: python

    $ conan install -g txt
    ...
    $ conan build
    Hello World from Python!
