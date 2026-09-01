.. _running_packages:

Running and deploying packages
================================
Executables and applications including shared libraries can also be distributed, deployed and run with Conan. This might have
some advantages compared to deploying with other systems:

- A unified development and distribution tool, for all systems and platforms
- Manage any number of different deployment configurations in the same way you manage them for development
- Use a Conan server remote to store all your applications and runtimes for all Operating Systems, platforms and targets

There are different approaches:

Using virtual environments
---------------------------

We can create a package that contains an executable, for example from the default package template created by :command:`conan new`:

.. code-block:: bash

    $ conan new Hello/0.1

The source code used contains an executable called ``greet``, but it is not packaged by default. Let's modify the recipe
``package()`` method to also package the executable:

.. code-block:: python

    def package(self):
        self.copy("*greet*", src="hello/bin", dst="bin", keep_path=False)


Now we create the package as usual, but if we try to run the executable it won't be found:

.. code-block:: bash

    $ conan create . user/testing
    ...
    Hello/0.1@user/testing package(): Copied 1 '.h' files: hello.h
    Hello/0.1@user/testing package(): Copied 1 '.exe' files: greet.exe
    Hello/0.1@user/testing package(): Copied 1 '.lib' files: hello.lib

    $ greet
    > ... not found...


By default, Conan does not modify by default the environment, it will just create the package in the local cache, and that is not
in the system PATH, so the ``greet`` executable is not found.

The ``virtualrunenv`` generator generates files that add the package's default binary locations to the necessary paths:

- It adds the dependencies ``lib`` subfolder to the ``DYLD_LIBRARY_PATH`` environment variable (for OSX shared libraries)
- It adds the dependencies ``lib`` subfolder to the ``LD_LIBRARY_PATH`` environment variable (for Linux shared libraries)
- It adds the dependencies ``bin`` subfolder to the ``PATH`` environment variable (for executables)

So if we install the package, specifying such ``virtualrunenv`` like:

.. code-block:: bash

    $ conan install Hello/0.1@user/testing -g virtualrunenv

This will generate a few files that can be called to activate and deactivate the required environment variables

.. code-block:: bash

    $ activate_run.sh # $ source activate_run.sh in Unix/Linux
    $ greet
    > Hello World!
    $ deactivate_run.sh # $ source deactivate_run.sh in Unix/Linux

Imports
--------
It is possible to define a custom conanfile (either .txt or .py), with an ``imports`` section, that can retrieve from local
cache the desired files. This approach requires a user conanfile.
For more details see example below :ref:`runtime packages<repackage>`


Deployable packages
--------------------
With the ``deploy()`` method, a package can specify which files and artifacts to copy to user space or to other
locations in the system. Let's modify the example recipe adding the ``deploy()`` method:

.. code-block:: python

    def deploy(self):
        self.copy("*", dst="bin", src="bin")

And run :command:`conan create`

.. code-block:: bash

    $ conan create . user/testing

With that method in our package recipe, it will copy the executable when installed directly:

.. code-block:: bash

    $ conan install Hello/0.1@user/testing
    ...
    > Hello/0.1@user/testing deploy(): Copied 1 '.exe' files: greet.exe
    $ bin\greet.exe
    > Hello World!

The deploy will create a *deploy_manifest.txt* file with the files that have been deployed.

Sometimes it is useful to adjust the package ID of the deployable package in order to deploy it regardless of the compiler it was compiled
with:

.. code-block:: python

    def package_id(self):
        del self.info.settings.compiler

.. seealso::

    Read more about the :ref:`deploy() <method_deploy>` method.

Running from packages
---------------------

If a dependency has an executable that we want to run in the conanfile, it can be done directly in code
using the ``run_environment=True`` argument. It internally uses a ``RunEnvironment`` helper. 
For example, if we want to execute the ``greet`` app while building the ``Consumer`` package:

.. code-block:: python

    from conans import ConanFile, tools, RunEnvironment

    class ConsumerConan(ConanFile):
        name = "Consumer"
        version = "0.1"
        settings = "os", "compiler", "build_type", "arch"
        requires = "Hello/0.1@user/testing"

        def build(self):
            self.run("greet", run_environment=True)


Now run :command:`conan install` and :command:`conan build` for this consumer recipe:

.. code-block:: bash

    $ conan install . && conan build .
    ...
    Project: Running build()
    Hello World!

Instead of using the environment, it is also possible to explicitly access the path of the dependencies:

.. code-block:: python

    def build(self):
        path = os.path.join(self.deps_cpp_info["Hello"].rootpath, "bin")
        self.run("%s/greet" % path)

Note that this might not be enough if shared libraries exist. Using the ``run_environment=True`` helper above 
is a more complete solution.

Finally, there is another approach: the package containing the executable can add its *bin* folder directly to the ``PATH``.
In this case the **Hello** package conanfile would contain:

.. code-block:: python

    def package_info(self):
        self.cpp_info.libs = ["hello"]
        self.env_info.PATH = os.path.join(self.package_folder, "bin")

We may also define ``DYLD_LIBRARY_PATH`` and ``LD_LIBRARY_PATH`` if they are required for the executable.

The consumer package is simple, as the ``PATH`` environment variable contains the ``greet`` executable:

.. code-block:: python

    def build(self):
        self.run("greet")


.. _repackage:

Runtime packages and re-packaging
----------------------------------
It is possible to create packages that contain only runtime binaries, getting rid of all build-time dependencies.
If we want to create a package from the above "Hello" one, but only containing the executable (remember that the above
package also contains a library, and the headers), we could do:

.. code-block:: python

    from conans import ConanFile

    class HellorunConan(ConanFile):
        name = "HelloRun"
        version = "0.1"
        build_requires = "Hello/0.1@user/testing"
        keep_imports = True

        def imports(self):
            self.copy("greet*", src="bin", dst="bin")

        def package(self):
            self.copy("*")


This recipe has the following characteristics:

- It includes the ``Hello/0.1@user/testing`` package as ``build_requires``.
  That means that it will be used to build this `HelloRun` package, but once the `HelloRun` package is built,
  it will not be necessary to retrieve it.
- It is using ``imports()`` to copy from the dependencies, in this case, the executable
- It is using the ``keep_imports`` attribute to define that imported artifacts during the ``build()`` step (which
  is not define, then using the default empty one), are kept and not removed after build
- The ``package()`` method packages the imported artifacts that will be created in the build folder.

To create and upload this package to a remote:

.. code-block:: bash

    $ conan create . user/testing
    $ conan upload HelloRun* --all -r=my-remote


Installing and running this package can be done using any of the methods presented above. For example:

.. code-block:: bash

    $ conan install HelloRun/0.1@user/testing -g virtualrunenv
    # You can specify the remote with -r=my-remote
    # It will not install Hello/0.1@...
    $ activate_run.sh # $ source activate_run.sh in Unix/Linux
    $ greet
    > Hello World!
    $ deactivate_run.sh # $ source deactivate_run.sh in Unix/Linux
