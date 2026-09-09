.. spelling::

  codegangsta


.. _go_package_manager:

Conan: A Go package manager
===========================

The source code
---------------

You can just clone the following example repository:

.. code-block:: bash

    $ git clone https://github.com/lasote/conan-goserver-example

Or, alternatively, manually create the folder and copy the following files inside:

.. code-block:: bash

    $ mkdir conan-goserver-example
    $ cd conan-goserver-example
    $ mkdir src
    $ mkdir src/server

The files are:

*src/server/main.go* is a small http server that will answer "Hello world!" if we connect to it.

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

Create a *conanfile.txt*, with the following content:

.. code-block:: text
   :caption: *conanfile.txt*

    [requires]
    go-martini/1.0@lasote/stable

    [imports]
    src, * -> ./deps/src

Our project requires a package, **go-martini/1.0@lasote/stable**, and we indicate that all **src contents** from all our requirements have
to be copied to *./deps/src*.

The package go-martini depends on go-inject, so Conan will handle automatically the go-inject dependency.

.. code-block:: bash

    $ conan install .

This command will download our packages and will copy the contents in the *./deps/src* folder.

Running our server
------------------

Just add the **deps** folder to ``GOPATH``:

.. code-block:: bash

    # Linux / Macos
    $ export GOPATH=${GOPATH}:${PWD}/deps

    # Windows
    $ SET GOPATH=%GOPATH%;%CD%/deps

And run the server:

.. code-block:: bash

    $ cd src/server
    $ go run main.go

Open your browser and go to `localhost:9300`

.. code-block:: html

    Hello World!

Generating Go packages
----------------------

Creating a Conan package for a Go library is very simple. In a Go project, you compile all the code from sources in the project itself,
including all of its dependencies.

So we don't need to take care of settings at all. Architecture, compiler, operating system, etc. are only relevant for pre-compiled
binaries. Source code packages are settings agnostic.

Let's take a look at the *conanfile.py* of the **go inject** library:

.. code-block:: python
   :caption: *conanfile.py*

    from conans import ConanFile

    class InjectConan(ConanFile):
        name = "go-inject"
        version = "1.0"

        def source(self):
            self.run("git clone https://github.com/codegangsta/inject.git")
            self.run("cd inject && git checkout v1.0-rc1")  # TAG v1.0-rc1

        def package(self):
            self.copy(pattern='*', dst='src/github.com/codegangsta/inject', src="inject", keep_path=True)

If you have read the :ref:`Building a hello world package <packaging_getting_started>`, the previous code may look quite simple to you.

We want to pack **version 1.0** of the **go inject** library, so the **version** variable is **"1.0"**. In the ``source()`` method, we
declare how to obtain the source code of the library, in this case just by cloning the github repository and making a checkout of the
**v1.0-rc1** tag. In the ``package()`` method, we are just copying all the sources to a folder named "src/github.com/codegangsta/inject".

This way, we can keep importing the library in the same way:

.. code-block:: python

    import "github.com/codegangsta/inject"

We can export and upload the package to a remote and we are done:

.. code-block:: bash

    $ conan export . lasote/stable  # Or any other user/channel
    $ conan upload go-inject/1.0@lasote/stable --all

Now look at the **go martini** conanfile:

.. code-block:: python
   :caption: *conanfile.py*

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

It is very similar. The only difference is the ``requires`` variable. It defines the **go-inject/1.0@lasote/stable** library, as a
requirement.

.. code-block:: bash

    $ conan export . lasote/stable  # Or any other user/channel
    $ conan upload go-martini/1.0@lasote/stable  --all

Now we are able to use them easily and without the problems of versioning with github checkouts.


.. _localhost: http://localhost:9300
