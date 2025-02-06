.. _examples_runners_ssh_basic:

Creating a Conan package using a SSH runner
==============================================

.. include:: ../../../common/experimental_warning.inc

To execute Conan remotely, the host machine must have Python 3 installed and must be accessible by the host machine via SSH protocol.

This tutorial assumes that you are running Conan inside a Python virtual environment, skip the first part if the runner extensions have been already installed.

.. code-block:: bash

    # Install conan with runner dependencies
    $ pip install "conan[runners]"



For this example, we are going to create a simple Conan package and compile it remotely using the SSH runner feature.
    
.. code-block:: bash

    $ cd </my/runner/folder>
    $ mkdir mylib
    $ cd mylib
    $ conan new cmake_lib -d name=mylib -d version=0.1
    $ tree
    .
    ├── CMakeLists.txt
    ├── conanfile.py
    ├── include
    │   └── mylib.h
    ├── src
    │   └── mylib.cpp
    └── test_package
        ├── CMakeLists.txt
        ├── conanfile.py
        └── src
            └── example.cpp


We will also need to create a new profile which will define the SSH runner configuration.

In this case, the runner will be a Windows virtual machine.

``ssh_example`` profile

.. code-block:: text

    [settings]
    os={{detect_api.detect_os()}}
    arch={{detect_api.detect_arch()}}
    build_type=Release
    compiler=msvc
    compiler.cppstd=14
    compiler.runtime=dynamic
    compiler.version=194

    [runner]
    type=ssh
    configfile=False
    host=10.211.55.3


For this example, we are going to start from a clean environment. 

.. code-block:: bash

    $ conan list "mylib/*:*"
    Found 0 pkg/version recipes matching mylib/* in local cache


Let's create our library ``mylib`` using our new runner profile. 

..  note::

    Runners have different levels of verbosity.
    Passing ``-vverbose`` will show each step running in the remote machine in a friendly way.
    Passing ``-vdebug`` will show exactly which commands are remotly being executed.

.. code-block:: bash

    $ conan create . --version 0.1 -pr:a ssh_example -vverbose

If we split and analyze the command output, we can see what is happening and where the commands are being executed.

**1.** Standard conan execution.

.. code-block:: bash

    ======== Exporting recipe to the cache ========
    mylib/0.1: Exporting package recipe: </my/runner/folder>/mylib/conanfile.py
    mylib/0.1: Copied 1 '.py' file: conanfile.py
    mylib/0.1: Copied 1 '.txt' file: CMakeLists.txt
    mylib/0.1: Copied 1 '.h' file: mylib.h
    mylib/0.1: Copied 1 '.cpp' file: mylib.cpp
    mylib/0.1: Exported to cache folder: /<CONAN_HOME>/p/mylib4abd06a04bdaa/e
    mylib/0.1: Exported: mylib/0.1#8760bf5a311f01cc26f3b95428203210 (2025-01-28 12:25:54 UTC)


    ======== Input profiles ========
    Profile host:
    [settings]
    arch=armv8
    build_type=Release
    compiler=msvc
    compiler.cppstd=14
    compiler.runtime=dynamic
    compiler.runtime_type=Release
    compiler.version=194
    os=Windows

    Profile build:
    [settings]
    arch=armv8
    build_type=Release
    compiler=msvc
    compiler.cppstd=14
    compiler.runtime=dynamic
    compiler.runtime_type=Release
    compiler.version=194
    os=Windows

**2.** SSH connection

.. code-block:: bash

    Connected to 10.211.55.3


**3.** Check if the host has a the environment already setup, if not, create it. 

.. code-block:: bash


    10.211.55.3 | Checking python3 version...
    10.211.55.3 | Checking python version...
    10.211.55.3 | Python 3.12.5
    10.211.55.3 | Checking remote OS type...
    10.211.55.3 | nt
    10.211.55.3 | Checking remote home folder...
    10.211.55.3 | C:\Users\<user>
    10.211.55.3 | Checking C:/Users/<user>/.conan2remote folder exists...
    10.211.55.3 | Checking C:/Users/<user>/.conan2remote/conanhome folder exists...
    10.211.55.3 | Checking conan version...
    10.211.55.3 | Conan version 2.12.1
    10.211.55.3 | Updating conancenter remote...
    10.211.55.3 | Checking conan home...
    10.211.55.3 | C:/Users/<user>/.conan2remote/conanhome
    10.211.55.3 | Detecting remote profile...
    10.211.55.3 | [settings]
    10.211.55.3 | arch=armv8
    10.211.55.3 | build_type=Release
    10.211.55.3 | compiler=msvc
    10.211.55.3 | compiler.cppstd=14
    10.211.55.3 | compiler.runtime=dynamic
    10.211.55.3 | compiler.version=194
    10.211.55.3 | os=Windows

..  note::

    The newly created environment will be located under ``~/.conan2remote`` folder, meaning
    that this will never interfere with possible existing Conan installations nor the host cache.

**4.** Copy profiles and setup folder

.. code-block:: bash

    Copying profiles and recipe to host...
    Copying profile 'ssh': /Users/<user>/.conan20/profiles/ssh -> C:/Users/<user>/.conan2remote/conanhome/profiles/ssh
    10.211.55.3 | Creating remote temporary directory...
    10.211.55.3 | C:\Users\<user>\.conan2remote\tmpwxh_dl7h


**7.** Run the conan create inside the remote machine and build "mylib".

.. code-block:: bash

    10.211.55.3 | Running conan create C:/Users/<user>/.conan2remote/tmpwxh_dl7h -pr:a ssh -vverbose...
    10.211.55.3 | 
    10.211.55.3 | ======== Exporting recipe to the cache ========
    10.211.55.3 | mylib/0.1: Exporting package recipe: C:/Users/<user>/.conan2remote/tmph9nsed7h\conanfile.py
    10.211.55.3 | mylib/0.1: Copied 1 '.py' file: conanfile.py
    10.211.55.3 | mylib/0.1: Copied 1 '.txt' file: CMakeLists.txt
    10.211.55.3 | mylib/0.1: Copied 1 '.h' file: mylib.h
    10.211.55.3 | mylib/0.1: Copied 1 '.cpp' file: mylib.cpp
    10.211.55.3 | mylib/0.1: Exported to cache folder: C:\Users\<user>\.conan2remote\conanhome\p\mylib4abd06a04bdaa\e
    10.211.55.3 | mylib/0.1: Exported: mylib/0.1#8760bf5a311f01cc26f3b95428203210 (2025-01-28 12:36:40 UTC)
    10.211.55.3 | 
    10.211.55.3 | ======== Input profiles ========
    10.211.55.3 | Profile host:
    10.211.55.3 | [settings]
    10.211.55.3 | arch=armv8
    10.211.55.3 | build_type=Release
    10.211.55.3 | compiler=msvc
    10.211.55.3 | compiler.cppstd=14
    10.211.55.3 | compiler.runtime=dynamic
    10.211.55.3 | compiler.runtime_type=Release
    10.211.55.3 | compiler.version=194
    10.211.55.3 | os=Windows
    10.211.55.3 | 
    10.211.55.3 | Profile build:
    10.211.55.3 | [settings]
    10.211.55.3 | arch=armv8
    10.211.55.3 | build_type=Release
    10.211.55.3 | compiler=msvc
    10.211.55.3 | compiler.cppstd=14
    10.211.55.3 | compiler.runtime=dynamic
    10.211.55.3 | compiler.runtime_type=Release
    10.211.55.3 | compiler.version=194
    10.211.55.3 | os=Windows
    10.211.55.3 | 
    10.211.55.3 | ======== Computing dependency graph ========
    10.211.55.3 | Graph root
    10.211.55.3 |     cli
    10.211.55.3 | Requirements
    10.211.55.3 |     mylib/0.1#8760bf5a311f01cc26f3b95428203210 - Cache
    10.211.55.3 | 
    10.211.55.3 | ======== Computing necessary packages ========
    10.211.55.3 | mylib/0.1: Forced build from source
    10.211.55.3 | Requirements
    10.211.55.3 |     mylib/0.1#8760bf5a311f01cc26f3b95428203210:178761a61a8a0d586b569b7f49e5bd91016a50ce - Build
    10.211.55.3 | 
    10.211.55.3 | ======== Installing packages ========
    10.211.55.3 | 
    10.211.55.3 | -------- Installing package mylib/0.1 (1 of 1) --------
    10.211.55.3 | ...
    10.211.55.3 | -- Build files have been written to: C:/Users/<user>/.conan2remote/conanhome/p/b/mylib144aae72987c9/b/build
    10.211.55.3 | 
    10.211.55.3 | mylib/0.1: Running CMake.build()
    10.211.55.3 | mylib/0.1: RUN: cmake --build "C:\Users\<user>\.conan2remote\conanhome\p\b\mylib144aae72987c9\b\build" --config Release
    10.211.55.3 | MSBuild version 17.11.2+c078802d4 for .NET Framework
    10.211.55.3 | 
    10.211.55.3 | ...
    10.211.55.3 | ======== Testing the package: Executing test ========
    10.211.55.3 | mylib/0.1 (test package): Running test()
    10.211.55.3 | mylib/0.1 (test package): RUN: ./example
    10.211.55.3 | mylib/0.1: Hello World Release!
    10.211.55.3 | mylib/0.1: __x86_64__ defined
    10.211.55.3 | mylib/0.1: _GLIBCXX_USE_CXX11_ABI 1
    10.211.55.3 | mylib/0.1: __cplusplus201703
    10.211.55.3 | mylib/0.1: __GNUC__11
    10.211.55.3 | mylib/0.1: __GNUC_MINOR__4
    10.211.55.3 | mylib/0.1 test_package

**8.** Copy the package created in the remote machine using the ``pkglist.json`` info from the previous ``conan create`` and restore this new package inside the host cache running a ``conan cache save``.

.. code-block:: bash

    Retrieving remote artifacts into local cache...
    Remote cache tgz: C:/Users/<user>/.conan2remote/tmp468p4lg5/cache.tgz
    Retrieved local cache: /var/folders/3w/9p02bxjd7bzc3hj1_rth4c880000gn/T/tmps4f934qp/cache.tgz
    Restore: mylib/0.1 in mylib4abd06a04bdaa
    Restore: mylib/0.1:178761a61a8a0d586b569b7f49e5bd91016a50ce in b/mylibfd0bad73e2ae9/p
    Restore: mylib/0.1:178761a61a8a0d586b569b7f49e5bd91016a50ce metadata in b/mylibfd0bad73e2ae9/d/metadata


Checking Conan's cache we should see the new package compiled for our remote machine settings, in this case, Windows armv8.

.. code-block:: bash

    $ conan list "mylib/*:*"
    Found 1 pkg/version recipes matching mylib/* in local cache
    Local Cache
      mylib
        mylib/0.1
          revisions
            8760bf5a311f01cc26f3b95428203210 (2025-01-28 12:47:00 UTC)
              packages
                178761a61a8a0d586b569b7f49e5bd91016a50ce
                  revisions
                    01254c6d548599c13465dbbd5b06ee37 (2025-01-28 12:47:16 UTC)
                  info
                    settings
                      arch: armv8
                      build_type: Release
                      compiler: msvc
                      compiler.cppstd: 14
                      compiler.runtime: dynamic
                      compiler.runtime_type: Release
                      compiler.version: 194
                      os: Windows
                    options
                      shared: False



We have managed to compile a package remotely using the new SSH feature without the need of a physical access to the remote machine. 

The workflow remains the same, except from having to add some extra configuration to our profile, the rest of the process is transparent to the user.
