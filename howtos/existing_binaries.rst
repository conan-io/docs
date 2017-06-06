.. _existing_binaries:


Packaging existing binaries
============================

Sometimes, it is necessary to create packages from existing binaries, like binaries from third parties, or previously built by another process or team not using conan, so building from sources is not wanted. For this case, there could be two different approaches:

- If the binary packages are already accesible by some kind of constant, external reference (URL, team shared drive, etc), then it is possible to just use the ``build()`` method to get the binaries into the build folder, and then package them.

- If the binaries don't have such a reference, like local files in user space, or created by a CI job in some temporary folder, then the ``package_files`` command can directly package those files without having to define ``build()`` or ``package()`` recipe methods


Packaging external binaries
------------------------------

In this case, having a complete conan recipe, with the detailed retrieval of the binaries could be the preferred way, because it has better reproducibility, and the original binaries might be traced. Such a recipe would be like:

.. code-block:: python

    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"
        settings = "os", "compiler", "build_type", "arch"

        def build(self):
            if self.settings.os == "Windows" and self.compiler == "Visual Studio":
                url = ("https://<someurl>/downloads/hello_binary%s_%s.zip"
                       % (str(self.settings.compiler.version), str(self.settings.build_type)))
            elif ...:
                url = ...
            else:
                raise Exception("Binary does not exist for these settings")
            tools.download(url, "mydownload.zip")
            tools.unzip("mydownload.zip")
            os.remove("mydownload.zip")

        def package(self):
            self.copy("*") # assume package as-is, but you can also copy specific files or rearrange

        def package_info(self):  # still very useful for package consumers
            self.cpp_info.libs = ["hello"]


Typically, pre-compiled binaries come for different configurations, so the only task that the ``build()`` method has to implement is to map the ``settings`` to the different URLs.

.. note::

  - This is a normal conan package, even if the binaries are being retrieved from somewhere. The **recommended approach** is using ``conan test_package``, and have a small consuming project besides the above recipe, to test locally, then upload the conan package with the binaries to the conan remote with ``conan upload``.
  - The same "building" policies apply. Having a recipe will fail if no conan packages are created, and the ``--build`` argument is not defined. A typical approach for this kind of packages could be to define a ``build_policy="missing"``, specially if the URLs are also under the team control. If they are external (internet), it could be better to create the packages and store them in your own conan server, so builds do not rely on the third party URL being available.


Packaging local binaries
-------------------------

If the files we want to package are just local, creating a ``build()`` method that would copy them from the user folder is not reproducible, so it doesn't add any value.
For this use case, it is possible to use ``conan package_files`` command directly.

A conan recipe is still needed, in this case it will be very simple, just the meta information of the package. A basic recipe can be created with the ``conan new`` command:


.. code-block:: bash

    $ conan new Hello/0.1 --bare
    $ conan export myuser/testing

This will create and store in the local cache the following package recipe:

.. code-block:: python

  class HelloConan(ConanFile):
      name = "Hello"
      version = "0.1"
      settings = "os", "compiler", "build_type", "arch"

      def package_info(self):
          self.cpp_info.libs = self.collect_libs()

The provided ``package_info()`` method will scan the package files to provide the end consumers with the name of the libraries to link with. This method can be further customized to provide other build flags (typically conditioned to the settings). The default ``package_info()`` applies: it will define headers in "include" folder, libraries in "lib" folder, binaries in "bin" folder. If different package layout, it can be defined in ``package_info()`` method.

This package recipe can be also extended to provide support for more configurations (for example, adding options: shared/static, or using different settings), adding dependencies (``requires``), etc.

Then, we will assume that we have in our current directory a "lib" folder with some binary for this "hello" library ``libhello.a``, compatible for example with Windows MinGW (gcc) version 4.9:

.. code-block:: bash

    $ conan package_files Hello/0.1@myuser/testing  -s os=Windows -s compiler=gcc -s compiler.version=4.9 ...


Having a ``test_package`` is still very recommended, to locally test the package before uploading. As we don't want to build the package from sources, the flow would be:

.. code-block:: bash

    $ conan new Hello/0.1@myuser/testing --bare --test
    # customize test_package project
    # customize package recipe if necessary
    $ conan export myuser/testing
    $ cd my/path/to/binaries
    $ conan package_files Hello/0.1@myuser/testing  -s os=Windows -s compiler=gcc -s compiler.version=4.9 ...
    $ conan test_package --build=missing -s os=Windows -s compiler=gcc -s ...

Latest 2 steps can be repeated for any number of configurations.
