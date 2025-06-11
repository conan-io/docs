.. _examples_config_files_settings_user:

Customize your settings: create your settings_user.yml
======================================================

Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/examples/config_files/settings_user


In this example we are going to see how to customize your settings without overwriting the original **settings.yml** file.

.. note::

    To understand better this example, it is highly recommended to read previously the reference
    about :ref:`reference_config_files_settings_yml`.


Locate the settings_user.yml
----------------------------

First of all, let's have a look at the proposed ``source/settings_user.yml``:

.. code-block:: yaml
    :caption: **settings_user.yml**

    os:
        webOS:
            sdk_version: [null, "7.0.0", "6.0.1", "6.0.0"]
    arch: ["cortexa15t2hf"]
    compiler:
        gcc:
            version: ["13.0-rc"]


As you can see, we don't have to rewrite all the settings because they will be merged with the already defined in
**settings.yml**.

Then, what are we adding through that ``settings_user.yml`` file?

* New OS: ``webOS``, and its sub-setting: ``sdk_version``.
* New ``arch`` available: ``cortexa15t2hf``.
* New gcc version: ``13.0-rc``.

Now, it's time to copy the file ``source/settings_user.yml`` into your ``[CONAN_HOME]/`` folder:

.. code-block:: bash

    $ conan config install sources/settings_user.yml
    Copying file settings_user.yml to /Users/myuser/.conan2/.


Use your new settings
---------------------

After having copied the ``settings_user.yml``, you should be able to use them for your recipes. Add this simple one
into your local folder:

.. code-block:: python
    :caption: **conanfile.py**

    from conan import ConanFile

    class PkgConan(ConanFile):
        name = "pkg"
        version = "1.0"
        settings = "os", "compiler", "build_type", "arch"


Then, create several Conan packages (not binaries, as it does not have any source file for sure) to see
that it's working correctly:


.. code-block:: bash
    :caption: **Using the new OS and its sub-setting**
    :emphasize-lines: 11,12,34

    $ conan create . -s os=webOS -s os.sdk_version=7.0.0
    ...
    Profile host:
    [settings]
    arch=x86_64
    build_type=Release
    compiler=apple-clang
    compiler.cppstd=gnu98
    compiler.libcxx=libc++
    compiler.version=12.0
    os=webOS
    os.sdk_version=7.0.0

    Profile build:
    [settings]
    arch=x86_64
    build_type=Release
    compiler=apple-clang
    compiler.cppstd=gnu98
    compiler.libcxx=libc++
    compiler.version=12.0
    os=Macos
    ...
    -------- Installing (downloading, building) binaries... --------
    pkg/1.0: Copying sources to build folder
    pkg/1.0: Building your package in /Users/myuser/.conan2/p/t/pkg929d53a5f06b1/b
    pkg/1.0: Aggregating env generators
    pkg/1.0: Package 'a0d37d10fdb83a0414d7f4a1fb73da2c210211c6' built
    pkg/1.0: Build folder /Users/myuser/.conan2/p/t/pkg929d53a5f06b1/b
    pkg/1.0: Generated conaninfo.txt
    pkg/1.0: Generating the package
    pkg/1.0: Temporary package folder /Users/myuser/.conan2/p/t/pkg929d53a5f06b1/p
    pkg/1.0 package(): WARN: No files in this package!
    pkg/1.0: Package 'a0d37d10fdb83a0414d7f4a1fb73da2c210211c6' created
    pkg/1.0: Created package revision 6a947a7b5669d6fde1a35ce5ff987fc6
    pkg/1.0: Full package reference: pkg/1.0#637fc1c7080faaa7e2cdccde1bcde118:a0d37d10fdb83a0414d7f4a1fb73da2c210211c6#6a947a7b5669d6fde1a35ce5ff987fc6
    pkg/1.0: Package folder /Users/myuser/.conan2/p/pkgb3950b1043542/p

.. code-block:: bash
    :caption: **Using new gcc compiler version**
    :emphasize-lines: 9,32

    $ conan create . -s compiler=gcc -s compiler.version=13.0-rc -s compiler.libcxx=libstdc++11
    ...
    Profile host:
    [settings]
    arch=x86_64
    build_type=Release
    compiler=gcc
    compiler.libcxx=libstdc++11
    compiler.version=13.0-rc
    os=Macos

    Profile build:
    [settings]
    arch=x86_64
    build_type=Release
    compiler=apple-clang
    compiler.cppstd=gnu98
    compiler.libcxx=libc++
    compiler.version=12.0
    os=Macos
    ...
    -------- Installing (downloading, building) binaries... --------
    pkg/1.0: Copying sources to build folder
    pkg/1.0: Building your package in /Users/myuser/.conan2/p/t/pkg918904bbca9dc/b
    pkg/1.0: Aggregating env generators
    pkg/1.0: Package '44a4588d3fe63ccc6e7480565d35be38d405718e' built
    pkg/1.0: Build folder /Users/myuser/.conan2/p/t/pkg918904bbca9dc/b
    pkg/1.0: Generated conaninfo.txt
    pkg/1.0: Generating the package
    pkg/1.0: Temporary package folder /Users/myuser/.conan2/p/t/pkg918904bbca9dc/p
    pkg/1.0 package(): WARN: No files in this package!
    pkg/1.0: Package '44a4588d3fe63ccc6e7480565d35be38d405718e' created
    pkg/1.0: Created package revision d913ec060e71cc56b10768afb9620094
    pkg/1.0: Full package reference: pkg/1.0#637fc1c7080faaa7e2cdccde1bcde118:44a4588d3fe63ccc6e7480565d35be38d405718e#d913ec060e71cc56b10768afb9620094
    pkg/1.0: Package folder /Users/myuser/.conan2/p/pkg789b624c93fc0/p

.. code-block:: bash
    :caption: **Using the new OS and the new architecture**
    :emphasize-lines: 5,11,33

    $ conan create . -s os=webOS -s arch=cortexa15t2hf
    ...
    Profile host:
    [settings]
    arch=cortexa15t2hf
    build_type=Release
    compiler=apple-clang
    compiler.cppstd=gnu98
    compiler.libcxx=libc++
    compiler.version=12.0
    os=webOS

    Profile build:
    [settings]
    arch=x86_64
    build_type=Release
    compiler=apple-clang
    compiler.cppstd=gnu98
    compiler.libcxx=libc++
    compiler.version=12.0
    os=Macos
    ...
    -------- Installing (downloading, building) binaries... --------
    pkg/1.0: Copying sources to build folder
    pkg/1.0: Building your package in /Users/myuser/.conan2/p/t/pkgde9b63a6bed0a/b
    pkg/1.0: Aggregating env generators
    pkg/1.0: Package '19cf3cb5842b18dc78e5b0c574c1e71e7b0e17fc' built
    pkg/1.0: Build folder /Users/myuser/.conan2/p/t/pkgde9b63a6bed0a/b
    pkg/1.0: Generated conaninfo.txt
    pkg/1.0: Generating the package
    pkg/1.0: Temporary package folder /Users/myuser/.conan2/p/t/pkgde9b63a6bed0a/p
    pkg/1.0 package(): WARN: No files in this package!
    pkg/1.0: Package '19cf3cb5842b18dc78e5b0c574c1e71e7b0e17fc' created
    pkg/1.0: Created package revision f5739d5a25b3757254dead01b30d3af0
    pkg/1.0: Full package reference: pkg/1.0#637fc1c7080faaa7e2cdccde1bcde118:19cf3cb5842b18dc78e5b0c574c1e71e7b0e17fc#f5739d5a25b3757254dead01b30d3af0
    pkg/1.0: Package folder /Users/myuser/.conan2/p/pkgd154182aac59e/p


As you could observe, each command has created a different package. That was completely right because we were using
different settings for each one. If you want to see all the packages created, you can use the :ref:`reference_commands_list` command:


.. code-block:: bash
    :caption: List all the *pkg/1.0*'s packages

    $ conan list pkg/1.0:*
    Local Cache
      pkg
        pkg/1.0
          revisions
            637fc1c7080faaa7e2cdccde1bcde118 (2023-02-16 06:42:10 UTC)
              packages
                19cf3cb5842b18dc78e5b0c574c1e71e7b0e17fc
                  info
                    settings
                      arch: cortexa15t2hf
                      build_type: Release
                      compiler: apple-clang
                      compiler.cppstd: gnu98
                      compiler.libcxx: libc++
                      compiler.version: 12.0
                      os: webOS
                44a4588d3fe63ccc6e7480565d35be38d405718e
                  info
                    settings
                      arch: x86_64
                      build_type: Release
                      compiler: gcc
                      compiler.libcxx: libstdc++11
                      compiler.version: 13.0-rc
                      os: Macos
                a0d37d10fdb83a0414d7f4a1fb73da2c210211c6
                  info
                    settings
                      arch: x86_64
                      build_type: Release
                      compiler: apple-clang
                      compiler.cppstd: gnu98
                      compiler.libcxx: libc++
                      compiler.version: 12.0
                      os: webOS
                      os.sdk_version: 7.0.0


Try any other custom setting!

.. seealso::

    - :ref:`reference_config_files_profiles`.
    - :ref:`creating_packages_configure_options_settings`
