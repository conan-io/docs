.. _python_reuse:

How to reuse Python code in recipes
===================================

.. warning::

    To reuse Python code, from Conan 1.7 there is a new ``python_requires()`` feature.
    See: :ref:`Python requires: reusing Python code in recipes<python_requires>`
    This "how to" might be deprecated and removed in the future. It is left here for reference only.


First, if you feel that you are repeating a lot of Python code, and that repeated code could be
useful for other Conan users, please propose it in a github issue.

There are several ways to handle Python code reuse in package recipes:

- To put common code in files, as explained :ref:`below <split_conanfile>`. This code
  has to be exported into the recipe itself.
  
- To create a Conan package with the common Python code, and then ``require`` it from the recipe.

This howto explains the latter.

A basic Python package
-----------------------

Let's begin with a simple Python package, a "hello world" functionality that we want to package and reuse:

.. code-block:: python

    def hello():
        print("Hello World from Python!")

To create a package, all we need to do is create the following layout:

.. code-block:: text

    -| hello.py
     | __init__.py
     | conanfile.py


The ``__init__.py`` is blank.
It is not necessary to compile code, so the package recipe ``conanfile.py`` is quite simple:


.. code-block:: python

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


The ``exports`` will copy both the ``hello.py`` and the ``__init__.py`` into the recipe. The ``package()`` method is also obvious: to
construct the package just copy the Python sources.

The ``package_info()`` adds the current package folder to the ``PYTHONPATH`` Conan environment variable. It will not affect the real
environment variable unless the end user desires it.


It can be seen that this recipe would be practically the same for most Python packages, so it could be factored in a ``PythonConanFile``
base class to further simplify it. (Open a feature request, or better a pull request. :) ) 


With this recipe, all we have to do is:


.. code-block:: bash

    $ conan export . memsharded/testing

Of course if you want to share the package with your team, you can :command:`conan upload` it to a remote server. But to create and test the
package, we can do everything locally.

Now the package is ready for consumption. In another folder, we can create a *conanfile.txt* (or a *conanfile.py* if we prefer):

.. code-block:: text

    [requires]
    HelloPy/0.1@memsharded/testing


And install it with the following command:


.. code-block:: bash

    $ conan install . -g virtualenv

Creating the above ``conanfile.txt`` might be unnecessary for this simple example, as you can directly run
:command:`conan install HelloPy/0.1@memsharded/testing -g virtualenv`, however, using the file is the canonical way.

The specified ``virtualenv`` generator will create an ``activate`` script (in Windows *activate.bat*), that basically contains the
environment, in this case, the ``PYTHONPATH``. Once we activate it, we are able to find the package in the path and use it:

.. code-block:: bash

    $ activate
    $ python
    Python 2.7.12 (v2.7.12:d33e0cf91556, Jun 27 2016, 15:19:22) [MSC v.1500 32 bit (Intel)] on win32
    ...
    >>> import hello
    >>> hello.hello()
    Hello World from Python!
    >>>

The above shows an interactive session, but you can import also the functionality in a regular Python script.

Reusing Python code in your recipes
-----------------------------------

Requiring a Python Conan package
++++++++++++++++++++++++++++++++

As the Conan recipes are Python code itself, it is easy to reuse Python packages in them. A basic recipe using the created package would be:

.. code-block:: python

    from conans import ConanFile

    class HelloPythonReuseConan(ConanFile):
        requires = "HelloPy/0.1@memsharded/testing"

        def build(self):
            from hello import hello
            hello()



The ``requires`` section is just referencing the previously created package. The functionality of that package can be used in several
methods of the recipe: ``source()``, ``build()``, ``package()`` and ``package_info()``, i.e. all of the methods used for creating the
package itself. Note that in other places it is not possible, as it would require the dependencies of the recipe to be already retrieved,
and such dependencies cannot be retrieved until the basic evaluation of the recipe has been executed.

.. code-block:: bash

    $ conan install .
    ...
    $ conan build .
    Hello World from Python!

Sharing a Python module
+++++++++++++++++++++++

Another approach is sharing a Python module and exporting within the recipe.

.. _split_conanfile:

Let's write for example a ``msgs.py`` file and put it besides the ``conanfile.py``:

.. code-block:: python

    def build_msg(output):
        output.info("Building!")

And then the main ``conanfile.py`` would be:

.. code-block:: python

   from conans import ConanFile
   from msgs import build_msg

   class ConanFileToolsTest(ConanFile):
       name = "test"
       version = "1.9"
       exports = "msgs.py"  # Important to remember!

       def build(self):
           build_msg(self.output)
           # ...

It is important to note that such ``msgs.py`` file **must be exported** too when exporting the package, because package recipes must be
self-contained.

The code reuse can also be done in the form of a base class, something like a file ``base_conan.py``

.. code-block:: python

    from conans import ConanFile

    class ConanBase(ConanFile):
        # common code here

And then:

.. code-block:: python

    from conans import ConanFile
    from base_conan import ConanBase

    class ConanFileToolsTest(ConanBase):
        name = "test"
        version = "1.9"
        exports = "base_conan.py"
