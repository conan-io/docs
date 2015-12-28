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

Here you can configure the path where all the packages will be stored (on Windows, it is recomended to assign it to
some unit, e.g. map it to X: in order to avoid hitting the 260 chars path name length limit).

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
