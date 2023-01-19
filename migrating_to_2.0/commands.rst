
Commands
========

There is no "compatible with 2.X" commands introduced in Conan 1.X.
You will need to adapt to the new commands once you migrate to Conan 2.0


Changes to expect
-----------------


conan install
^^^^^^^^^^^^^

Almost the same command, the major change is the way to specify (or complete if not defined) the fields of the reference.
Remember that in Conan 1.X you have to specify the build profile or activate the conf ``core:default_build_profile=default``.

.. code-block:: shell

    $ conan install . [--name=mylib] [--version=1.0] [-pr:b=build_profile] [-pr:h=host_profile]

In addition the ``--install-folder`` has been replaced with ``--output-folder``. You might need to provide both arguments in Conan 1.X as some legacy generated files (``conaninfo.txt``, ``conanbuildinfo.txt``, etc) are not affected by ``--output-folder``.


conan install
^^^^^^^^^^^^^

In addition the ``--build-folder`` has been replaced with ``--output-folder``. Still in most cases you shouldn't be using it, but relying on the defined `layout()` in the recipe.


conan create
^^^^^^^^^^^^

Same changes as `conan install`:

.. code-block:: shell

    $ conan create . [--name=mylib] [--version=1.0] [-pr:b=build_profile] [-pr:h=host_profile]

.. _conan_v2_graph_info:

conan graph info
^^^^^^^^^^^^^^^^

This is the substitute of the old "conan info". The syntax is very similar to ``conan install`` and ``conan create``

.. code-block:: shell

    $ conan graph info . [--name=mylib] [--version=1.0] [-pr:b=build_profile] [-pr:h=host_profile]


conan search
^^^^^^^^^^^^

The ``conan search`` will search, by default, in all the remotes (not in the local cache):

.. code-block:: shell

    $ conan search "zlib*"

    myremote:
      zlib
        zlib/1.2.11
    conancenter:
      zlib-ng
        zlib-ng/2.0.2
        zlib-ng/2.0.5
        zlib-ng/2.0.6
      zlib
        zlib/1.2.11
        zlib/1.2.8

If you want to explore the local cache there is a command ``conan list recipes <pattern>``.


.. _conan_v2_remote_login:

conan remote login
^^^^^^^^^^^^^^^^^^

This is the substitute of the old "conan user".

.. code-block:: shell

     $ conan remote login [-h] [-f FORMAT] [-v [V]] [--logger] [-p [PASSWORD]] remote username


conan upload
^^^^^^^^^^^^

The default behavior has changed from requiring `--all` to include the binary packages to `--recipe-only` for just the recipe 

.. code-block:: shell

     $ conan upload [-h] [-v [V]] [--logger] [-p PACKAGE_QUERY] -r REMOTE
                    [--only-recipe] [--force] [--check] [-c]
                    reference


.. _conan_v2_unified_arguments:

Unified patterns in command arguments
-------------------------------------

The arguments in Conan 1.X where we specified recipe names require now a valid reference pattern.
A valid reference pattern contains the ``*`` character or at least the ``name/version`` part of a reference
(``name/version@user/channel``).

There are some examples:

- The ``--build`` argument when referring to a package:

.. code-block:: shell
   :caption: **From:**

    conan install . --build zlib

.. code-block:: shell
   :caption: **To:**

    conan install . --build zlib*
    conan install . --build zlib/1.2.11
    conan install . --build zlib/1.*

- The ``--options`` and ``--settings`` arguments when used scoped:

.. code-block:: shell
   :caption: **From:**

    conan install . -s zlib:arch=x86 -o zlib:shared=True

.. code-block:: shell
   :caption: **To:**

    conan install . -s zlib*:arch=x86 -o zlib*:shared=True
    conan install . -s zlib/1.2.11@user/channel:arch=x86 -o zlib/1.2.11:shared=True

Commands with have been removed
-------------------------------

Removed "conan package"
^^^^^^^^^^^^^^^^^^^^^^^

The ``conan package`` command has been removed. If you are developing a recipe and want to test that the package method
is correct, we recommend using the ``conan export-pkg .`` instead and exploring the package folder in the cache to check
if everything is ok.


Removed "conan copy"
^^^^^^^^^^^^^^^^^^^^

Do not use the ``conan copy`` command to change user/channel. Packages will be immutable,
and this command will disappear in 2.0. Package promotions are generally done on the
server-side, copying packages from one server repository to another repository.


Removed "conan user"
^^^^^^^^^^^^^^^^^^^^

This has been replaced with :ref:<conan_v2_remote_login>

Removed "conan config set"
^^^^^^^^^^^^^^^^^^^^^^^^^^

we are no longer implementing file-editing commands in 2.0. A bit overkill `conan config set` to edit one file. Which should very rarely happen,
the file is updated with `conan config install`. Alternatively, you can use the command line and profiles to pass these values.

Custom commands
---------------

You can build custom commands on top of the Conan Python API.
WIP documentation.
