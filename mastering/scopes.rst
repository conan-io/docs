Scopes
========


.. warning::

    Scopes might be deprecated in the future. Probably everything you can do with scopes can be done more easily with environment variables. Please try to avoid the use of scopes, and if you are already using them, please contact us to report your use case and get advice about other solutions.

Scopes vs options
_________________

In the previous example we added an option ``shared`` to our conanfile.py to control if the library has to be static or shared.

For the Poco package, if we specify ``shared=True`` or ``shared=False`` in the ``conan install`` command we get different binary packages.
When we declare new options we open the possibility of having multiple packages for the same recipe, as it happens with the settings.


First, we are going to see how to control the build of tests with an **option** (generally not a good idea). Adding a new option ``build_tests`` we can control when to run the tests:

**conanfile.py**

.. code-block:: python
   :emphasize-lines: 3

     class PocoTimerConan(ConanFile):
        ...
        options = {"build_tests": [True, False]}  # NOT A GOOD APPROACH
        default_options = "build_tests=False"
        ...

        def build(self):
            cmake = CMake(self)
            flag_build_tests = "-DBUILD_TEST=1" if self.options.build_tests else ""
            self.run('cmake "%s" %s %s' % (self.conanfile_directory, cmake.command_line, flag_build_tests))
            self.run('cmake --build . %s' % cmake.build_config)



**CMakeLists.txt**

.. code-block:: cmake

   option(BUILD_TEST OFF)
   if(BUILD_TEST)
       include(CTest)
       enable_testing()
       # ...
   endif()


Then we could use ``conan install -o Poco:build_test=False/True`` to activate or deactivate the execution of tests.


But, what happens if we are creating a conan package?

If we install our package specifying different values for the option "build_test", we will generate/require different conan packages,
but the library (binary artifact) will be the same, so, why different conan packages?

Conan has **scope variables** to control the conanfile.py without generating different packages no matter what is the value of the scope variable.


Now using scope variables:


**conanfile.py**

.. code-block:: python
   :emphasize-lines: 3

     class PocoTimerConan(ConanFile):
        ...

        def build(self):
            cmake = CMake(self)
            flag_build_tests = "-DBUILD_TEST=1" if self.scope.build_tests else ""
            self.run('cmake "%s" %s %s' % (self.conanfile_directory, cmake.command_line, flag_build_tests))
            self.run('cmake --build . %s' % cmake.build_config)


Then we could use ``conan install --scope build_test=False/True`` to activate or deactivate the tests launch.


``dev`` scope
----------------


There is a special scope variable called ``dev`` that is automatically set to True if you are using **conanfile.py** in your project.

If we export the recipe and install it from a local or remote repository, the variable ``dev`` will be False.

It's especially useful to require some testing packages (just for running the tests) or anything that does not affect the built artifact.

In the following example we will require the ``catch`` package for unit testing our project:

.. code-block:: python
   :emphasize-lines: 6,10

     class PocoTimerConan(ConanFile):
        ...

        def config(self):
           if self.scope.dev:
              self.requires("catch/1.3.0@TyRoXx/stable")

        def build(self):
            cmake = CMake(self)
            flag_build_tests = "-DBUILD_TEST=1" if self.scope.dev and self.scope.build_tests else ""
            self.run('cmake "%s" %s %s' % (self.conanfile_directory, cmake.command_line, flag_build_tests))
            self.run('cmake --build . %s' % cmake.build_config)


It guarantees that when you build a conan package with your project, no one that requires it (from its conanfile.txt or its conanfile.py) will require the ``catch`` library, because it's not needed.


There is also a simplified way to require development packages:


.. code-block:: python
   :emphasize-lines: 5

     class PocoTimerConan(ConanFile):
        ...

        def config(self):
            self.requires("catch/1.3.0@TyRoXx/stable", dev=True)


An extra shortcut for this syntax would be to use the new ``dev_requires`` attribute:

.. code-block:: python
   :emphasize-lines: 2

     class PocoTimerConan(ConanFile):
        dev_requires = "catch/1.3.0@TyRoXx/stable"



Defining scopes
-----------------

Setting a scope variable in a requirement is very similar to options:


.. code-block:: bash

   $ conan install --scope Poco:somescope=somevalue


If we want to set it in our project conanfile we don't specify the package namespace:

.. code-block:: bash

   $ conan install --scope somescope=somevalue


There is an special namespace called ``ALL`` that will apply to all our requirements and our conanfile:


.. code-block:: bash

   $ conan install --scope ALL:somescope=somevalue

Note that if defining specific values for a certain package, the specific value will have
precedence:

.. code-block:: bash

   $ conan install --scope ALL:somescope=somevalue Poco:somescope=othervalue

In this case, the scope ``somescope`` of Poco will have the value ``othervalue``.


At this point you almost have your library prepared for being a conan package. In next section
we will create our own packages using ``conanfile.py``.
