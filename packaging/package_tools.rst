Tools for package creators
===================

We have developed another FOSS tool for package creators, **conan package tools** to ease the 
task of generating multiple binary packages from a package recipe. 
It offers a simple way to define the different configurations and to call "conan test"
Also offers CI integration like **Travis CI, Appveyor and Bamboo**, for cloud based automated
binary package creation, testing and uploading.

This tool enables the creation of hundreds of binary packages in the cloud with a simple ``git push``.
   

- Make easier the **generation of multiple conan's packages** with different configurations.
- Automated/remote package generation in **Travis/Appveyor** server with distributed builds in CI jobs for big/slow builds.
- **Docker**: Automatic generation of packages for gcc 4.6, 4.8, 4.9, 5.2 and 5.3 in any Linux, also in Travis CI.
- Automatic creation of OSX packages, also in Travis-CI.
- **Visual Studio**: Automatic configuration of command line environment with detected settings.

Its available in pypi:

.. code-block:: bash

    pip install conan_package_tools 
    

Read the README.md in the `Conan Package Tools repository <https://github.com/conan-io/conan-package-tools>`_
    
