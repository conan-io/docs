.. _existing_binaries:

Packaging existing binaries
===========================

Sometimes, it is necessary to create packages from existing binaries, like binaries from third
parties, or previously built by another process or team not using conan, so building from sources is
not wanted. You would want to package local files in two situations:

 - When it is not possible to build the packages from sources (only pre-built binaries available).
 - When you are developing your package locally and want to export the built artifacts to the local
   cache.
   As you don't want to rebuild again (clean copy) your artifacts, you don't want to call
   :command:`conan create`.
   This way you can keep your build cache if you are using an IDE or calling locally to the
   :command:`conan build` command.

Packaging pre-built binaries
----------------------------

If the files we want to package are just local, creating a ``build()`` method that would copy them
from the user folder is not reproducible, so it doesn't add any value. For this use case, it is
possible to use :command:`conan export-pkg` command directly.

A conan recipe is still needed, in this case it will be very simple, just the meta information of
the package. A basic recipe can be created with the :command:`conan new` command:

.. code-block:: bash

    $ conan new Hello/0.1 --bare

This will create and store in the local cache the following package recipe:

.. code-block:: python

    class HelloConan(ConanFile):
        name = "Hello"
        version = "0.1"
        settings = "os", "compiler", "build_type", "arch"

        def package(self):
            self.copy("*")

        def package_info(self):
            self.cpp_info.libs = self.collect_libs()

The provided ``package_info()`` method will scan the package files to provide the end consumers with
the name of the libraries to link with. This method can be further customized to provide other build
flags (typically conditioned to the settings). The default ``package_info()`` applies: it will
define headers in "include" folder, libraries in "lib" folder, binaries in "bin" folder. A different
package layout can be defined in ``package_info()`` method.

This package recipe can be also extended to provide support for more configurations (for example,
adding options: shared/static, or using different settings), adding dependencies (``requires``),
etc.

Then, we will assume that we have in our current directory a *lib* folder with some binary for this
"hello" library *libhello.a*, compatible for example with Windows MinGW (gcc) version 4.9:

.. code-block:: bash

    $ conan export-pkg . Hello/0.1@myuser/testing  -s os=Windows -s compiler=gcc -s compiler.version=4.9 ...

Having a *test_package* folder is still very recommended, to locally test the package before
uploading. As we don't want to build the package from sources, the flow would be:

.. code-block:: bash

    $ conan new Hello/0.1 --bare --test
    # customize test_package project
    # customize package recipe if necessary
    $ cd my/path/to/binaries
    $ conan export-pkg PATH/TO/conanfile.py Hello/0.1@myuser/testing  -s os=Windows -s compiler=gcc -s compiler.version=4.9 ...
    $ conan test PATH/TO/test_package/conanfile.py Hello/0.1@myuser/testing -s os=Windows -s compiler=gcc -s ...

The last 2 steps can be repeated for any number of configurations.

Downloading and Packaging pre-built binaries
--------------------------------------------

In this case, having a complete conan recipe, with the detailed retrieval of the binaries could be
the preferred way, because it has better reproducibility, and the original binaries might be traced.
Such a recipe would be like:

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

    - This is a normal conan package, even if the binaries are being retrieved from somewhere.
      The **recommended approach** is using :command:`conan create`, and have a small consuming project
      besides the above recipe, to test locally, then upload the conan package with the binaries to
      the conan remote with :command:`conan upload`.

    - The same building policies apply. Having a recipe will fail if no conan packages are
      created, and the :command:`--build` argument is not defined. A typical approach for this kind of
      packages could be to define a :command:`build_policy="missing"`, especially if the URLs are also
      under the team control. If they are external (internet), it could be better to create the
      packages and store them in your own conan server, so builds do not rely on the third party URL
      being available.
