.. _reference_commands_profile:

conan profile
=============

Manage profiles


conan profile detect
--------------------

.. code-block:: text

    $ conan profile detect -h
    usage: conan profile detect [-h] [-v [V]] [--name NAME] [-f]

    Generate a profile using auto-detected values.

    optional arguments:
      -h, --help   show this help message and exit
      -v [V]       Level of detail of the output. Valid options from less verbose
                   to more verbose: -vquiet, -verror, -vwarning, -vnotice,
                   -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
      --name NAME  Profile name, 'default' if not specified
      -f, --force  Overwrite if exists


.. warning::

  The output of ``conan profile detect`` is **not stable**. It can change at any time in future Conan releases
  to adapt to latest tools, latest versions, or other changes in the environment.
  See :ref:`the Conan stability<stability>` section for more information.

.. note::

    **Best practices**
    It is not recommended to use ``conan profile detect`` in production. To guarantee reproducibility,
    it is recommended to define your own profiles, store them in a git repo or in a zip in a server,
    and distribute it to your team and CI machines with ``conan config install``, together with other
    configuration like custom settings, custom remotes definition, etc.


conan profile list
------------------

.. code-block:: text

    $ conan profile list -h
    usage: conan profile list [-h] [-f FORMAT] [-v [V]]

    List all profiles in the cache.

    optional arguments:
      -h, --help            show this help message and exit
      -f FORMAT, --format FORMAT
                            Select the output format: json
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace


conan profile path
------------------

.. code-block:: text

    $ conan profile path -h
    usage: conan profile path [-h] [-v [V]] [-o OPTIONS_HOST]
                              [-o:b OPTIONS_BUILD] [-o:h OPTIONS_HOST]
                              [-pr PROFILE_HOST] [-pr:b PROFILE_BUILD]
                              [-pr:h PROFILE_HOST] [-s SETTINGS_HOST]
                              [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST]
                              [-c CONF_HOST] [-c:b CONF_BUILD] [-c:h CONF_HOST]
                              name

    Show profile path location.

    positional arguments:
      name                  Profile name

    optional arguments:
      -h, --help            show this help message and exit
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      -o OPTIONS_HOST, --options OPTIONS_HOST
                            Define options values (host machine), e.g.: -o
                            Pkg:with_qt=true
      -o:b OPTIONS_BUILD, --options:build OPTIONS_BUILD
                            Define options values (build machine), e.g.: -o:b
                            Pkg:with_qt=true
      -o:h OPTIONS_HOST, --options:host OPTIONS_HOST
                            Define options values (host machine), e.g.: -o:h
                            Pkg:with_qt=true
      -pr PROFILE_HOST, --profile PROFILE_HOST
                            Apply the specified profile to the host machine
      -pr:b PROFILE_BUILD, --profile:build PROFILE_BUILD
                            Apply the specified profile to the build machine
      -pr:h PROFILE_HOST, --profile:host PROFILE_HOST
                            Apply the specified profile to the host machine
      -s SETTINGS_HOST, --settings SETTINGS_HOST
                            Settings to build the package, overwriting the
                            defaults (host machine). e.g.: -s compiler=gcc
      -s:b SETTINGS_BUILD, --settings:build SETTINGS_BUILD
                            Settings to build the package, overwriting the
                            defaults (build machine). e.g.: -s:b compiler=gcc
      -s:h SETTINGS_HOST, --settings:host SETTINGS_HOST
                            Settings to build the package, overwriting the
                            defaults (host machine). e.g.: -s:h compiler=gcc
      -c CONF_HOST, --conf CONF_HOST
                            Configuration to build the package, overwriting the
                            defaults (host machine). e.g.: -c
                            tools.cmake.cmaketoolchain:generator=Xcode
      -c:b CONF_BUILD, --conf:build CONF_BUILD
                            Configuration to build the package, overwriting the
                            defaults (build machine). e.g.: -c:b
                            tools.cmake.cmaketoolchain:generator=Xcode
      -c:h CONF_HOST, --conf:host CONF_HOST
                            Configuration to build the package, overwriting the
                            defaults (host machine). e.g.: -c:h
                            tools.cmake.cmaketoolchain:generator=Xcod


conan profile show
------------------

.. code-block:: text

    $ conan profile show -h
    usage: conan profile show [-h] [-v [V]] [-o OPTIONS_HOST]
                              [-o:b OPTIONS_BUILD] [-o:h OPTIONS_HOST]
                              [-pr PROFILE_HOST] [-pr:b PROFILE_BUILD]
                              [-pr:h PROFILE_HOST] [-s SETTINGS_HOST]
                              [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST]
                              [-c CONF_HOST] [-c:b CONF_BUILD] [-c:h CONF_HOST]

    Show aggregated profiles from the passed arguments.

    optional arguments:
      -h, --help            show this help message and exit
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      -o OPTIONS_HOST, --options OPTIONS_HOST
                            Define options values (host machine), e.g.: -o
                            Pkg:with_qt=true
      -o:b OPTIONS_BUILD, --options:build OPTIONS_BUILD
                            Define options values (build machine), e.g.: -o:b
                            Pkg:with_qt=true
      -o:h OPTIONS_HOST, --options:host OPTIONS_HOST
                            Define options values (host machine), e.g.: -o:h
                            Pkg:with_qt=true
      -pr PROFILE_HOST, --profile PROFILE_HOST
                            Apply the specified profile to the host machine
      -pr:b PROFILE_BUILD, --profile:build PROFILE_BUILD
                            Apply the specified profile to the build machine
      -pr:h PROFILE_HOST, --profile:host PROFILE_HOST
                            Apply the specified profile to the host machine
      -s SETTINGS_HOST, --settings SETTINGS_HOST
                            Settings to build the package, overwriting the
                            defaults (host machine). e.g.: -s compiler=gcc
      -s:b SETTINGS_BUILD, --settings:build SETTINGS_BUILD
                            Settings to build the package, overwriting the
                            defaults (build machine). e.g.: -s:b compiler=gcc
      -s:h SETTINGS_HOST, --settings:host SETTINGS_HOST
                            Settings to build the package, overwriting the
                            defaults (host machine). e.g.: -s:h compiler=gcc
      -c CONF_HOST, --conf CONF_HOST
                            Configuration to build the package, overwriting the
                            defaults (host machine). e.g.: -c
                            tools.cmake.cmaketoolchain:generator=Xcode
      -c:b CONF_BUILD, --conf:build CONF_BUILD
                            Configuration to build the package, overwriting the
                            defaults (build machine). e.g.: -c:b
                            tools.cmake.cmaketoolchain:generator=Xcode
      -c:h CONF_HOST, --conf:host CONF_HOST
                            Configuration to build the package, overwriting the
                            defaults (host machine). e.g.: -c:h
                            tools.cmake.cmaketoolchain:generator=Xcode
