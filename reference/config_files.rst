.. _config_files:

Configuration files
===================

These are the most important configuration files, used to customize conan.

conan.conf
----------

This is the typical ``~/.conan/conan.conf`` file:

.. code-block:: text

   [storage]
   # This is the default path, but you can write your own
   path: ~/.conan/data
   
   [settings_defaults]
   arch=x86_64
   build_type=Release
   compiler=Visual Studio
   compiler.runtime=MD
   compiler.version=14
   os=Windows

Here you can configure the path where all the packages will be stored (on Windows, it is recomended to assign it to
some unit, e.g. map it to X: in order to avoid hitting the 260 chars path name length limit).

You can also adjust the "path" setting using the environment variable **CONAN_USER_HOME**. 
Check the :ref:`how to control the cache<custom_cache>` section.


The remotes are managed in the order in which they are listed. The first one is assumed to be the default
for uploads. For downloads they are also accessed sequentially, until a matching binary package is found.

The settings defaults are the setting values used whenever you issue a ``conan install`` command over a
``conanfile`` in one of your projects **for the first time**. After that, the settings and options will
be cached in the project ``conaninfo.txt`` file. The initial values for these default settings are
auto-detected the first time you run a ``conan`` command.

settings.yml
------------
The ``settings`` are predefined, so only a few, like "os" or "compiler", are possible. They are
defined in your ``~/.conan/settings.yml`` file. Also, the possible values they can take are restricted
in the same file. This is done to ensure matching naming and spelling between users, and settings
that commonly make sense to most users. Anyway, you can add/remove/modify those settings and their
possible values in the ``settings.yml`` file, according to your needs, just be sure to share changes with
colleagues or consumers of your packages.

.. note::
   
   The ``settings.yml`` file is not perfect nor definitive, surely incomplete. Please send us any suggestion (or
   better a PR) with settings and values that could make sense for other users.
   
registry.txt
------------
This file is generally automatically managed, and it has also access via the ``conan remote``
command but just in case you might need to change it. It contains information about the known
remotes and from which remotes are each package retrieved:


.. code-block:: text

    conan.io https://server.conan.io True
    local http://localhost:9300 True
    
    Hello/0.1@demo/testing local
    
    
The first section of the file is listing ``remote-name``: ``remote-url`` ``verify_ssl``. Adding, removing or changing
those lines, will add, remove or change the respective remote. If verify_ssl, conan client will verify the SSL certificates
for that remote server.

The second part of the file contains a list of conan-package-reference: remote-name. This is
a reference to which remote was that package retrieved from, which will act also as the default
for operations on that package.

Be careful when modifying the remotes, as the information of the packages has to remain consistent,
e.g. if removing a remote, all package references referencing that remote has to be removed too.


short_paths.conf
----------------

Deprecated. This file is no longer used. If one of your packages hit the Windows path length limit
of 260 chars, just add ``short_paths=True`` to the conanfile.py, and it will automatically handle it.



.. _profiles:

profiles
--------

A profile text file has to be located in ``.conan/profiles/`` directory.
It's a text file that contains a predefined set of ``settings``, ``environment variables``` and ``scopes`` and has this structure:

.. code-block:: txt

   [settings]
   setting=value
   
   [env]
   env_var=value
   
   [scopes]
   scope=value


Profiles are useful for change global settings without specifying multiple "-s" parameters in ``conan install`` or ``conan test`` command.

For example, if you are working with Linux and you usually work with ``gcc`` compiler, but you have installed ``clang`` 
compiler and want to install some package for ``clang`` compiler, you could do:

- Create a ``.conan/profiles/clang`` file:

.. code-block:: txt

   [settings]
   compiler=clang
   compiler.version=3.5
   compiler.libcxx=libstdc++11
   
   [env]
   CC=/usr/bin/clang
   CXX=/usr/bin/clang++

   
- Execute conan install command passing the ``--profile`` or ``-pr`` parameter:


.. code-block:: bash

   conan install --profile clang

   

Without profiles you would have needed to set the CC and CXX variables in the environment to point to your clang compiler and use ``-s`` parameters to specify the settings:


.. code-block:: bash
   
   export CC=/usr/bin/clang
   export CXX=/usr/bin/clang++
   conan install -s compiler=clang -s compiler.version=3.5 -s compiler.libcxx=libstdc++11


A profile can also be used in ``conan test_package`` command:

.. code-block:: bash

   $ conan test_package --profile clang


Profiles can also be used with ``conan build`` command, but (by the moment) limited to the environment variables, settings and profiles will be ignored and taken from the **conaninfo.txt**:

.. code-block:: bash

   $ conan build --profile clang



Package settings and env vars
.............................

Profiles also support **package settings** and **package environment variables** definition, so you can override some settings or env vars for some specific package:


- Create a ``.conan/profiles/zlib_with_clang`` file:

.. code-block:: txt

   [settings]
   zlib:compiler=clang
   zlib:compiler.version=3.5
   zlib:compiler.libcxx=libstdc++11
   compiler=gcc
   compiler.version=4.9
   compiler.libcxx=libstdc++11
   
   [env]
   zlib:CC=/usr/bin/clang
   zlib:CXX=/usr/bin/clang++
   
- Your build tool will locate **clang** compiler only for the **zlib** package and **gcc** (default one) for the rest of your dependency tree.
