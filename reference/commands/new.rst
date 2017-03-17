
.. _conan_new:

conan new
=========

.. code-block:: bash

   $ conan new [-h] [-t] [-i] [-c] name


Creates a new package recipe template with a ``conanfile.py`` and optionally, ``test_package``
package testing files.

.. code-block:: bash

	positional arguments:
	  name          Package name, e.g.: Poco/1.7.3@user/testing

	optional arguments:
	  -h, --help    show this help message and exit
	  -t, --test    Create test_package skeleton to test package
	  -i, --header  Create a headers only package template
	  -c, --pure_c  Create a C language package only package,
	                deleting "self.settings.compiler.libcxx" setting in the configure method


**Examples**:


- Create a new ``conanfile.py`` for a new package **mypackage/1.0@myuser/stable**

.. code-block:: bash

   $ conan new mypackage/1.0@myuser/stable


- Create also a ``test_package`` folder skeleton:

.. code-block:: bash

   $ conan new mypackage/1.0@myuser/stable -t

