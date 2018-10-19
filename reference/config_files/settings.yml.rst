.. _settings_yml:


settings.yml
============

The ``settings`` are predefined, so only a few, like "os" or "compiler", are possible. They are
defined in your ``~/.conan/settings.yml`` file. Also, the possible values they can take are restricted
in the same file. This is done to ensure matching naming and spelling between users, and settings
that commonly make sense to most users. Anyway, you can add/remove/modify those settings and their
possible values in the ``settings.yml`` file, according to your needs, just be sure to share changes with
colleagues or consumers of your packages.

If you want to distribute a unified ``settings.yml`` file you can use the :ref:`conan config install command<conan_config_install>`.


.. note::
   
   The ``settings.yml`` file is not perfect nor definitive, surely incomplete. Please send us any suggestion (or
   better yet, a PR) with settings and values that could make sense for other users.
