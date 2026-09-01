.. _reference_commands_download:

conan download
==============

.. autocommand::
    :command: conan download -h


Downloads recipe and binaries to the local cache from the specified remote.

..  note::

    Please, be aware that :command:`conan download` unlike :command:`conan install`, will not
    download any of the transitive dependencies of the downloaded package.


The ``conan download`` command can download packages to 1 server repository specified by the ``-r=myremote`` argument.

It has 2 possible and mutually exclusive inputs:

- The ``conan download <pattern>`` pattern-based matching of recipes, with a pattern similar to the ``conan list <pattern>``.
- The ``conan download --list=<pkglist>`` that will upload the artifacts specified in the ``pkglist`` json file



You can use patterns to download specific references just like in other commands like
:command:`conan list` (see the patterns documentation there :ref:`reference_commands_list`) or :command:`conan upload`:

..  code-block:: bash
    
    # download latest revision and packages for all openssl versions in foo remote
    $ conan download "openssl/*" -r foo

.. note::

  :command:`conan download` will download only the latest revision by default. If you want
  to download more revisions other than the latest one you can use wildcards in the
  revisions part of the reference pattern argument

You may also just download recipes (in this case selecting all the revisions in the
pattern, not just the latest one):

..  code-block:: bash
    
    # download all recipe revisions for zlib/1.2.13
    $ conan download "zlib/1.2.13#*" -r foo --only-recipe


If you just want to download the packages belonging to a specific setting, use the ``--package-query`` argument:

.. code-block:: bash

    $ conan download "zlib/1.2.13#*" -r foo --package-query="os=Linux and arch=x86" 


If the ``--format=json`` formatter is specified, the result will be a "PackageList", compatible with other Conan commands, for example the ``conan upload`` command, so it is possible to concatenate a ``download + upload``, using the generated json file. See the :ref:`Packages Lists examples<examples_commands_pkglists>`.


Downloading metadata
--------------------

The metadata files of the recipes and packages are not downloaded by default. It is possible to explicitly retrieve them with the ``conan download --metadata=xxx`` argument.
The main arguments are the same as above, and Conan will download the specified packages, or skip them if they are already in the cache:

.. code-block:: bash

    $ conan download pkg/0.1 -r=default --metadata="*"
    # will download pgkg/0.1 recipe with all the recipe metadata
    # And also all package binaries (latest package revision)
    # with all the binaries metadata


If only one or several metadata folders or sets of files are desired, it can also be specified:


.. code-block:: bash

    $ conan download pkg/0.1 -r=default --metadata="logs/*" --metadata="tests/*"
    # Will download only the logs and tests metadata, but not other potential metadata files

For more information see the :ref:`metadata section<devops_metadata>`.
