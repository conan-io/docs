.. _config_files:

Configuration files
===================

The most important configuration files to make conan more customized.

conan.conf
----------




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
