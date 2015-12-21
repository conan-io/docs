.. _building_hello_world:

Building a Hello World package
==============================

We will build a package out of a "hello world" library available on github.
It is a very simple project, consisting of some source code files and a CMakeLists.txt
that builds a library and an executable. It can be built and run without conan.

First, let's create a folder for our project and get the source code:

.. code-block:: bash

   $ mkdir hellopack
   $ cd hellopack
   $ git clone https://github.com/memsharded/hello.git

(you can also just download and copy the source code to a "hello" subfolder)
   

Now we will write our **conanfile.py** in the **root "hellopack"** folder.
It is the script that defines how this package is built and used:

.. code-block:: python
   
   from conans import ConanFile, CMake
   
   class HelloConan(ConanFile):
       name = "Hello"
       version = "0.1"
       settings = "os", "compiler", "build_type", "arch"
:

.. code-block:: bash

   $ conan search


How can we know if the package builds properly? We can invoke the install command, passing
the full name of the package (we will use the default settings from conan.conf, but you can change
them if you want):

.. code-block:: bash

   $ conan install Hello/0.1@demo/testing
   ...
   ERROR: Can't find a 'Hello/0.1@demo/testing' package for the specified options and settings.
   ...


It failed, because there is no binary package that matches our settings. In fact, there aren't
any binary packages, we have just written and exported the conanfile.py which can create them. Now we will
try again, instructing conan to build the package from sources:

.. code-block:: bash

   $ conan install Hello/0.1@demo/testing --build Hello
   
   
Check :ref:`commands` for full details about the **install --build** options.

Now, try a ``conan search`` again in order to ensure that the package has just been created:

.. code-block:: bash

   $ conan search
   
So the package is there, but we still need to check if the package is actually properly created and
that there are no missing headers, libs or flags.

The best way to do that is to require this package from another test project that actually consumes it.
You could depend on this package explicitely from another project with a **conanfile.txt** file,
just as shown in :ref:`Getting started<getting_started>`. The ``Hello/0.1@demo/testing`` packages
will be built on demand, when the consumer project requires a specific package configuration.

In the next section we will see how it is possible to further automate the creation and testing of
multiple packages.
   



Any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write us</a>
