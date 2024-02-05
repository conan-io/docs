.. _reference_config_files_global_conf:

global.conf
===========

The **global.conf** file is located in the Conan user home directory, e.g., *[CONAN_HOME]/global.conf*. If it does not
already exist, a default one is automatically created.

Introduction to configuration
-----------------------------

*global.conf* is aimed to save some core/tools/user configuration variables that will be used by Conan. For instance:

* Package ID modes.
* General HTTP(python-requests) configuration.
* Number of retries when downloading/uploading recipes.
* Related tools configurations (used by toolchains, helpers, etc.)
* Others (required Conan version, CLI non-interactive, etc.)

Let's briefly explain the three types of existing configurations:

* ``core.*``: aimed to configure values of Conan core behavior (download retries, package ID modes, etc.).
  Only definable in *global.conf* file.
* ``tools.*``: aimed to configure values of Conan tools (toolchains, build helpers, etc.) used in your recipes.
  Definable in both *global.conf* and :ref:`profiles <reference_config_files_profiles>`.
* ``user.*``: aimed to define personal user configurations. They can define whatever user wants.
  Definable in both *global.conf* and :ref:`profiles <reference_config_files_profiles>`.

To list all the possible configurations available, run :command:`conan config list`:


.. autocommand::
    :command: conan config list


User/Tools configurations
-------------------------

Tools and user configurations can be defined in both the *global.conf* file and
:ref:`Conan profiles <reference_config_files_profiles_conf>`. They look like:


.. code-block:: text
    :caption: *global.conf*

    tools.build:verbosity=verbose
    tools.microsoft.msbuild:max_cpu_count=2
    tools.microsoft.msbuild:vs_version = 16
    tools.build:jobs=10
    # User conf variable
    user.confvar:something=False

.. important::

    Profiles values will have priority over globally defined ones in global.conf.


These are some hints about configuration items scope and naming:

- ``core.xxx`` and ``tools.yyy`` are Conan built-ins, users cannot define their own ones in these scopes.
- ``core.xxx`` can be defined in ``global.conf`` only, but not in profiles.
- ``tools.yyy`` can be defined in ``global.conf``, in profiles ``[conf]`` section and cli ``-c`` arguments
- ``user.zzz`` can be defined everywhere, and they are totally at the user discretion, no established naming convention. However this would be more or less expected:
  - For open source libraries, specially those in conancenter, ``user.packagename:conf`` might be expected, like the ``boost`` recipe defining ``user.boost:conf`` conf
  - For private usage, the recommendation could be to use something like ``user.orgname:conf`` for global org configuration across all projects, ``user.orgname.project:conf`` for project or package configuration, though ``user.project:conf`` might be also good if the project name is unique enough.


Configuration file template
---------------------------


It is possible to use **jinja2** template engine for *global.conf*. When Conan loads this file, it immediately parses
and renders the template, which must result in a standard tools-configuration text.

  .. code:: jinja

     # Using all the cores automatically
     tools.build:jobs={{os.cpu_count()}}
     # Using the current OS
     user.myconf.system:name = {{platform.system()}}

Conan also injects ``detect_api`` (non-stable, read the reference) to the jinja rendering context. You can use it like this:

  .. code:: jinja

    user.myteam:myconf1={{detect_api.detect_os()}}
    user.myteam:myconf2={{detect_api.detect_arch()}}

For more information on how to use it, please check :ref:`the detect_api section
<reference_config_files_profiles_detect_api>` in the profiles reference.

The Python packages passed to render the template are ``os`` and ``platform`` for all platforms and ``distro`` in Linux platforms.
Additionally, the variables ``conan_version`` and ``conan_home_folder`` are also available.


Configuration data types
------------------------


All the values will be interpreted by Conan as the result of the python built-in `eval()` function:

.. code-block:: text

    # String
    tools.build:verbosity=verbose
    # Boolean
    tools.system.package_manager:sudo=True
    # Integer
    tools.microsoft.msbuild:max_cpu_count=2
    # List of values
    user.myconf.build:ldflags=["--flag1", "--flag2"]
    # Dictionary
    tools.microsoft.msbuildtoolchain:compile_options={"ExceptionHandling": "Async"}


Configuration data operators
----------------------------

It's also possible to use some extra operators when you're composing tool configurations in your *global.conf* or
any of your profiles:

* ``+=`` == ``append``: appends values at the end of the existing value (only for lists).
* ``=+`` == ``prepend``: puts values at the beginning of the existing value (only for lists).
* ``*=`` == ``update``: updates the specified keys only, leaving the rest unmodified (only for dictionaries)
* ``=!`` == ``unset``: gets rid of any configuration value.

.. code-block:: text
    :caption: *global.conf*

    # Define the value => ["-f1"]
    user.myconf.build:flags=["-f1"]

    # Append the value ["-f2"] => ["-f1", "-f2"]
    user.myconf.build:flags+=["-f2"]

    # Prepend the value ["-f0"] => ["-f0", "-f1", "-f2"]
    user.myconf.build:flags=+["-f0"]

    # Unset the value
    user.myconf.build:flags=!

    # Define the value => {"a": 1, "b": 2}
    user.myconf.build:other={"a": 1, "b": 2}

    # Update b = 4 => {"a": 1, "b": 4}
    user.myconf.build:other*={"b": 4}


Configuration patterns
----------------------

You can use package patterns to apply the configuration in those dependencies which are matching:

.. code-block:: text

    *:tools.cmake.cmaketoolchain:generator=Ninja
    zlib:tools.cmake.cmaketoolchain:generator=Visual Studio 16 2019

This example shows you how to specify a general ``generator`` for all your packages except for `zlib` which is defining
`Visual Studio 16 2019` as its generator.

Besides that, it's quite relevant to say that **the order matters**. So, if we change the order of the
configuration lines above:

.. code-block:: text

    zlib:tools.cmake.cmaketoolchain:generator=Visual Studio 16 2019
    *:tools.cmake.cmaketoolchain:generator=Ninja

The result is that you're specifying a general `generator` for all your packages, and that's it. The `zlib` line has no
effect because it's the first one evaluated, and after that, Conan is overriding that specific pattern with the most
general one, so it deserves to pay special attention to the order.


Information about built-in confs
================================

This section provides extra information about specific confs.

Networking confs
----------------

.. _reference_config_files_global_conf_ssl_certificates:

Configuration of client certificates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Conan supports client TLS certificates. You can configure the path to your existing *Cacert* file and/or your client
certificate (and the key) using the following configuration variables:

* ``core.net.http:cacert_path``: Path containing a custom Cacert file.
* ``core.net.http:client_cert``: Path or tuple of files containing a client certificate (and the key). See more details in
  `Python requests and Client Side Certificates <https://requests.readthedocs.io/en/latest/user/advanced/#client-side-certificates>`_

For instance:

.. code-block:: text
    :caption: **[CONAN_HOME]/global.conf**

    core.net.http:cacert_path=/path/to/cacert.pem
    core.net.http:client_cert=('/path/client.cert', '/path/client.key')


.. seealso::

    * :ref:`Managing configuration in your recipes (self.conf_info) <conan_conanfile_model_conf_info>`


* ``tools.files.download:verify``: Setting ``tools.files.download:verify=False`` constitutes a security risk if enabled,
  as it disables certificate validation. Do not use it unless you understand the implications
  (And even then, properly scoping the conf to only the required recipes is a good idea)
  or if you are using it for development purposes


UX confs
--------

.. _reference_config_files_global_conf_skip_warnings:

Skip warnings
~~~~~~~~~~~~~

There are several warnings that Conan outputs in certain cases which can be omitted via the ``core:skip_warnings`` conf,
by adding the warning tag to its value.

Those warnings are:

  - ``deprecated``: Messages for deprecated features such as legacy generators
  - ``network``: Messages related to network issues, such as retries
