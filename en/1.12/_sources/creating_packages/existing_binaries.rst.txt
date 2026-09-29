.. _existing_binaries:

Packaging Existing Binaries
===========================

There are specific scenarios in which it is necessary to create packages from existing binaries, for example from 3rd
parties or binaries previously built by another process or team that are not using Conan. Under these circumstances building from sources is
not what you want. You should package the local files in the following situations:

 - When you cannot build the packages from sources (when only pre-built binaries are available).
 - When you are developing your package locally and you want to export the built artifacts to the local
   cache.
   As you don't want to rebuild again (clean copy) your artifacts, you don't want to call
   :command:`conan create`.
   This method will keep your build cache if you are using an IDE or calling locally to the
   :command:`conan build` command.

Packaging Pre-built Binaries
----------------------------

Running the ``build()`` method, when the files you want to package are local, results in no added value as the files
copied from the user folder cannot be reproduced. For this scenario, run :command:`conan export-pkg` command directly.

A Conan recipe is still required, but is very simple and will only include the package meta information. A basic recipe can be created with the :command:`conan new` command:

.. code-block:: bash

    $ conan new Hello/0.1 --bare

This will create and store the following package recipe in the local cache:

.. code-block:: python

    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"
        settings = "os", "compiler", "build_type", "arch"

        def package(self):
            self.copy("*")

        def package_info(self):
            self.cpp_info.libs = self.collect_libs()

The provided ``package_info()`` method scans the package files to provide end-users with
the name of the libraries to link to. This method can be further customized to provide additional build
flags (typically dependent on the settings). The default ``package_info()`` applies as follows: it
defines headers in the "include" folder, libraries in the "lib" folder, and binaries in the "bin" folder. A different
package layout can be defined in the ``package_info()`` method.

This package recipe can be also extended to provide support for more configurations (for example,
adding options: shared/static, or using different settings), adding dependencies (``requires``),
and more.

Based on the above, We can assume that our current directory contains a *lib* folder with a number binaries for this
"hello" library *libhello.a*, compatible for example with Windows MinGW (gcc) version 4.9:

.. code-block:: bash

    $ conan export-pkg . Hello/0.1@myuser/testing  -s os=Windows -s compiler=gcc -s compiler.version=4.9 ...

Having a *test_package* folder is still highly recommended for testing the package locally before
upload. As we don't want to build the package from the sources, the flow would be:

.. code-block:: bash

    $ conan new Hello/0.1 --bare --test
    # customize test_package project
    # customize package recipe if necessary
    $ cd my/path/to/binaries
    $ conan export-pkg PATH/TO/conanfile.py Hello/0.1@myuser/testing  -s os=Windows -s compiler=gcc -s compiler.version=4.9 ...
    $ conan test PATH/TO/test_package/conanfile.py Hello/0.1@myuser/testing -s os=Windows -s compiler=gcc -s ...

The last two steps can be repeated for any number of configurations.

Downloading and Packaging Pre-built Binaries
--------------------------------------------

In this scenario, creating a complete Conan recipe, with the detailed retrieval of the binaries could be
the preferred method, because it is reproducible, and the original binaries might be traced.
Follow our sample recipe for this purpose:

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
            tools.get(url)

        def package(self):
            self.copy("*") # assume package as-is, but you can also copy specific files or rearrange

        def package_info(self):  # still very useful for package consumers
            self.cpp_info.libs = ["hello"]

Typically, pre-compiled binaries come for different configurations, so the only task that the
``build()`` method has to implement is to map the ``settings`` to the different URLs.

.. note::

    - This is a standard Conan package even if the binaries are being retrieved from elsewhere.
      The **recommended approach** is to use :command:`conan create`, and include a small consuming project
      in addition to the above recipe, to test locally and then proceed to upload the Conan package with the binaries to
      the Conan remote with :command:`conan upload`.

    - The same building policies apply. Having a recipe fails if no Conan packages are
      created, and the :command:`--build` argument is not defined. A typical approach for this kind of
      packages could be to define a :command:`build_policy="missing"`, especially if the URLs are also
      under the team control. If they are external (on the internet), it could be better to create the
      packages and store them on your own Conan server, so that the builds do not rely on third party URL
      being available.
