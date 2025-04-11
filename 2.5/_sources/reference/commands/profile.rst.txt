.. _reference_commands_profile:

conan profile
=============

Manage profiles


conan profile detect
--------------------

.. autocommand::
    :command: conan profile detect -h


.. warning::

  The output of ``conan profile detect`` is **not stable**. It can change at any time in future Conan releases
  to adapt to latest tools, latest versions, or other changes in the environment.
  See :ref:`the Conan stability<stability>` section for more information.

You can create a new auto-detected profile for your configuration using:

..  code-block:: text
    :caption: *auto-detected profile*

    $ conan profile detect
    Found apple-clang 14.0
    apple-clang>=13, using the major as version
    Detected profile:
    [settings]
    arch=x86_64
    build_type=Release
    compiler=apple-clang
    compiler.cppstd=gnu17
    compiler.libcxx=libc++
    compiler.version=14
    os=Macos

    WARN: This profile is a guess of your environment, please check it.
    WARN: Defaulted to cppstd='gnu17' for apple-clang.
    WARN: The output of this command is not guaranteed to be stable and can change in future Conan versions.
    WARN: Use your own profile files for stability.
    Saving detected profile to /Users/barbarians/.conan2/profiles/default


Be aware that if the profile already exists you have to use ``--force`` to overwrite it. Otherwise it will fail

..  code-block:: text
    :caption: *force overwriting already existing default profile*

    $ conan profile detect
    ERROR: Profile '/Users/carlosz/.conan2/profiles/default' already exists
    $ conan profile detect --force
    Found apple-clang 14.0
    ...
    Saving detected profile to /Users/carlosz/.conan2/profiles/default

.. note::

    **Best practices**
    It is not recommended to use ``conan profile detect`` in production. To guarantee reproducibility,
    it is recommended to define your own profiles, store them in a git repo or in a zip in a server,
    and distribute it to your team and CI machines with ``conan config install``, together with other
    configuration like custom settings, custom remotes definition, etc.


conan profile list
------------------

.. autocommand::
    :command: conan profile list -h


..  code-block:: text
    :caption: *force overwriting already existing default profile*

    $ conan profile list
    Profiles found in the cache:
    default
    ios_base
    ios_simulator
    clang_15


conan profile path
------------------

.. autocommand::
    :command: conan


Use to get the profile location in your ``[CONAN_HOME]`` folder:

.. code-block:: text

    $ conan profile path default
    /Users/barbarians/.conan2/profiles/default


conan profile show
------------------

.. autocommand::
    :command: conan profile show -h


Use :command:`conan profile show` to compute the resulting build and host profiles from
the command line arguments. For example, combining different options and settings with the
default profile or with any other profile using the ``pr:b`` or ``pr:h`` arguments:

.. code-block:: text
    :emphasize-lines: 5,12
    
    $ conan profile show -s:h build_type=Debug -o:h shared=False
    Host profile:
    [settings]
    arch=x86_64
    build_type=Debug
    compiler=apple-clang
    compiler.cppstd=gnu17
    compiler.libcxx=libc++
    compiler.version=14
    os=Macos
    [options]
    shared=False
    [conf]


    Build profile:
    [settings]
    arch=x86_64
    build_type=Release
    compiler=apple-clang
    compiler.cppstd=gnu17
    compiler.libcxx=libc++
    compiler.version=14
    os=Macos
    [conf]

It's also useful to show the result of the evaluation of :ref:`jinja2 templates in the
profiles<reference_config_files_profiles_rendering>`. For example, a profile like this:

..  code-block:: text
    :caption: *myprofile*

    [settings]
    os = {{ {"Darwin": "Macos"}.get(platform.system(), platform.system()) }}

Check the evaluated profile:

..  code-block:: text

    $ conan profile show -pr:h=myprofile     
    Host profile:
    [settings]
    os=Macos
    [conf]
    ...


The command can also output a json with the results:

.. code-block:: text

    $ conan profile show --format=json
    
    {
    "host": {
        "settings": {
            "arch": "armv8",
            "build_type": "Release",
            "compiler": "apple-clang",
            "compiler.cppstd": "gnu17",
            "compiler.libcxx": "libc++",
            "compiler.version": "15",
            "os": "Macos"
        },
        "package_settings": {},
        "options": {},
        "tool_requires": {},
        "conf": {},
        "build_env": ""
    },
    "build": {
        "settings": {
            "arch": "armv8",
            "build_type": "Release",
            "compiler": "apple-clang",
            "compiler.cppstd": "gnu17",
            "compiler.libcxx": "libc++",
            "compiler.version": "15",
            "os": "Macos"
        },
        "package_settings": {},
        "options": {},
        "tool_requires": {},
        "conf": {},
        "build_env": ""
    }
    }

.. seealso::

    - Read more about :ref:`profiles<reference_config_files_profiles>`
