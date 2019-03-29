Sharing the settings and other configuration
============================================

If you are using Conan in a company or in an organization, sometimes you need to share the *settings.yml* file, the *profiles*, or even
the *remotes* or any other Conan local configuration with the team.

You can use the :command:`conan config install`.

If you want to try this feature without affecting your current configuration, you can declare the ``CONAN_USER_HOME`` environment variable
and point to a different directory.

Read more in the section :ref:`conan_config_install`.
