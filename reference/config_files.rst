.. _config_files:

Configuration files
===================

The most important configuration files to make conan more customized.

conan.conf
----------

This is the typical ``~/.conan/conan.conf`` file:

.. code-block:: text

   [storage]
   # This is the default path, but you can write your own
   path: ~/.conan/data
   
   [remotes]
   conan.io: https://server.conan.io
   local: http://localhost:9300
   
   [settings_defaults]
   arch=x86_64
   build_type=Release
   compiler=Visual Studio
   compiler.runtime=MD
   compiler.version=14
   os=Windows

You can configure here the path where all the packages will be stored (recomended to assign to
some unit as X: in windows to minimize the issue of long path names)

The remotes are managed in order, the first one is assumed to be the default for uploads. Downloads
will check them in order too, until a matching binary package is found.

The settings defaults are the setting values used **every first time** you issue a ``conan install``
over a ``conanfile`` file in one of your projects. After that, the settings and options will be cached in the project
``conaninfo.txt`` file. The initial values for these default settings is auto-detected the first time
you run a ``conan`` command.

settings.yml
------------
The ``settings`` are predefined, so only a few as "os" or "compiler" are possible. They are
defined in your ``~/.conan/settings.yml`` file. Also the possible values they can take are restricted
in the same file. This is done to ensure matching naming and spelling between users, and settings
that commonly make sense to most users. You can anyway add/remove/modify those settings and their
possible values in the ``settings.yml`` file, if that matches your needs, just be sure to share
that with your colleagues or consumers of your packages.

.. note::
   
   The ``settings.yml`` file is not perfect nor definitive, surely incomplete. Please send us any suggestion (or
   better a PR) with settings and values that could make sense for other users
