.. _package_tools:

Tools for package creators
==========================

With some python (or just pure shell or bash) scripting, we could easily automate the whole package
creation and testing process, for many different configurations. For example you could put the
following script in the package root folder. Name it *build.py*:

.. code-block:: python

    import os, sys
    import platform

    def system(command):
        retcode = os.system(command)
        if retcode != 0:
            raise Exception("Error while executing:\n\t %s" % command)

    if __name__ == "__main__":
        params = " ".join(sys.argv[1:])
   
        if platform.system() == "Windows":
            system('conan create . demo/testing -s compiler="Visual Studio" -s compiler.version=14 %s' % params)
            system('conan create . demo/testing -s compiler="Visual Studio" -s compiler.version=12 %s' % params)
            system('conan create . demo/testing -s compiler="gcc" -s compiler.version=4.8 %s' % params)
        else:
            pass

This is a pure python script, not related to conan, and should be run as such:

.. code:: bash

   $ python build.py

We have developed another FOSS tool for package creators, **Conan Package Tools** to ease the 
task of generating multiple binary packages from a package recipe.
It offers a simple way to define the different configurations and to call :command:`conan test`.
Also offers CI integration like **Travis CI, Appveyor and Bamboo**, for cloud based automated
binary package creation, testing and uploading.

This tool enables the creation of hundreds of binary packages in the cloud with a simple
``$ git push``.

- Make easier the **generation of multiple conan packages** with different configurations.
- Automated/remote package generation in **Travis/Appveyor** server with distributed builds in CI
  jobs for big/slow builds.
- **Docker**: Automatic generation of packages for several versions of ``gcc`` and ``clang`` in
  Linux, also in Travis CI.
- Automatic creation of OSX packages with apple-clang, also in Travis-CI.
- **Visual Studio**: Automatic configuration of command line environment with detected settings.

It's available in pypi:

.. code-block:: bash

    $ pip install conan_package_tools 

Read the README.md in the `Conan Package Tools repository <https://github.com/conan-io/conan-package-tools>`_.
