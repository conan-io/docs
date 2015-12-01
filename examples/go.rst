Go Programming Language and Conan
=================================

Conan is a generic package manager. In the :ref:`getting started <getting_started>` section we saw how to use conan and manage a C/C++ library like POCO.

But conan just provided some tools related with C/C++ (like some generators and the cpp_info) to give better user experience, the general basis of Conan can be used with other programming language.

Conan is a generic package manager, so let's see what can we do with Go lang.


The source code
---------------

You can just clone the following example repository:

.. code-block:: bash

   $ git clone https://github.com/lasote/conan-goserver-example

Or alternatively, manually create the folder and copy the following files inside:

.. code-block:: bash

   $ mkdir conan-goserver-example
   $ cd conan-goserver-example
   $ mkdir src
   $ mkdir src/server
   

The files are:

**"src/server/main.go"** is a small http server that will answer "Hello world!" if we connect to it.

.. code-block:: go

	package main

	import "github.com/go-martini/martini"
	
	func main() {
	  m := martini.Classic()
	  m.Get("/", func() string {
	    return "Hello world!"
	  })
	  m.Run()
	}

         
Declaring and installing dependencies
-------------------------------------

Create also a ``conanfile.txt`` with the following content:

**conanfile.txt**

.. code-block:: text

	[requires]
	go-martini/1.0@lasote/stable
	
	[imports]
	src, * -> ./deps/src 


Out project requires a package **go-martini/1.0@lasote/stable** and we indicate that all **src contents** from all our requirements have to be copied to **./deps/src**

The package go-martini_ depends on go-inject_, so conan will handle automatically go-inject dependency.

.. code-block:: bash

   $ conan install

This command will download our packages and will copy the contents in **./deps/src** folder


Running our server
------------------

Just add **deps** folder to GOPATH:

.. code-block:: bash
	
	# Linux / Macos
	$ export GOPATH=${GOPATH}:${PWD}/deps
	
	# Windows
	$ SET GOPATH=%GOPATH%;%CD%/deps
	
	
And run the server:

.. code-block:: bash
	
	$ cd src/server
	$ go run main.go


Open your browser and go to `localhost:3000`__


.. code-block:: html

	Hello World!


Generating Go packages
----------------------

Create a *conan* package for a Go library is very simple. In a Go project you compile all the code
from sources in the project itself, including all its dependencies.

So we don't need to take care of settings at all. Architecture, compiler, operating system...
are only relevant for pre-compiled binaries, source code packages are settings agnostic.

Let's take a look to ``conanfile.py`` of **go inject** library:


**conanfile.py**

.. code-block:: python

    from conans import ConanFile


    class InjectConan(ConanFile):
        name = "go-inject"
        version = "1.0"
    
        def source(self):
            self.run("git clone https://github.com/codegangsta/inject.git")
            self.run("cd inject && git checkout v1.0-rc1")  # TAG v1.0-rc1
    
        def package(self):
            self.copy(pattern='*', dst='src/github.com/codegangsta/inject', src="inject", keep_path=True)
    
    
If you have read the :ref:`Building a hello world package <building_hello_world>`, the previous code may look quite simple for you.

We want to pack the **version 1.0** of **go inject** library, so the **version** variable is **"1.0"**

In the **source** method we declare how to obtain the source code of the library, in this case, just cloning the github repository and doing a checkout to **v1.0-rc1** tag.

In the **package** method we are just copying all the sources to a folder named "src/github.com/codegangsta/inject".

This way, we can keep importing the library in the same way:

.. code-block:: python

    import "github.com/codegangsta/inject"
    

We can export and upload the package to a **conan server** and we are done with it:


.. code-block:: bash

    $ conan export lasote/stable  # Or any other user/channel
    $ conan upload go-inject/1.0@lasote/stable --all
    

Now look at the **go martini** conanfile:


.. code-block:: python

    from conans import ConanFile


    class InjectConan(ConanFile):
        name = "go-martini"
        version = "1.0"
        requires = 'go-inject/1.0@lasote/stable'
    
        def source(self):
            self.run("git clone https://github.com/go-martini/martini.git")
            self.run("cd martini && git checkout v1.0")  # TAG v1.0
    
        def package(self):
            self.copy(pattern='*', dst='src/github.com/go-martini/martini', src="martini", keep_path=True)
 
 
It is very similar. The only difference is the **requires** variable. It defines **'go-inject/1.0@lasote/stable'** library as a requirement.
    

.. code-block:: bash

    $ conan export lasote/stable  # Or any other user/channel
    $ conan upload go-martini/1.0@lasote/stable  --all
    
    
Now we are able to use them in an easy way and without the problems of versioning with github checkouts. 



Got any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write us</a>
   
   
.. _go-martini: https://conan.io/source/go-martini/1.0/lasote/stable
.. _go-inject: https://conan.io/source/go-inject/1.0/lasote/stable
.. _localhost: http://localhost:3000
__ localhost_

