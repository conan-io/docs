
General changes
===============



Host and Build profiles
-----------------------


Use always :ref:`build and host profiles <build_profiles_and_host_profiles>`.

Conan 1.x uses one profile by default, to start using two profiles, please do the following:

- Pass ``-pr:b=default`` in the command line to most commands.
- Or set the variable ``core:default_build_profile=default`` at the :ref:`global.conf<global_conf>` file to apply it
  always, automatically.

Do not use ``os_build``, ``arch_build`` anywhere in your recipes or code.


- Revisions

Conan 2.0 uses :ref:`revisions<package_revisions>` by default and the local cache 2.0 will
store multiple recipe and package revisions for your Conan packages (Conan 1.X supports
only one revision). To start working with revisions enabled in Conan 1.X, please enable
them in your Conan configuration:

.. code-block:: bash

    $ conan config set general.revisions_enabled=True


Lowercase references
--------------------

Move all your packages to lowercase. Uppercase package names (or versions/user/channel) will not be allowed in 2.0.


Default Package ID mode
-----------------------

Work in progress


Compatible packages
-------------------

Work in progress


Extensions
----------

Work in progress

Hooks
^^^^^

- Hooks folder has been updated to ``~/.conan2/extensions/hook``;
- Any hook file must be named with ``hook_`` as prefix and ``.py`` as suffix;
- Only ``ConanFile`` is passed as parameter;
- Pre and Post Download are no longer supported in Conan 2.x
- Added Pre and Post Generator

Environment Variables
---------------------

Work in progress
