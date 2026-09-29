.. _reference_commands_upload:

conan upload
============

Use this command to upload recipes and binaries to Conan repositories. For more
information on how to work with Conan repositories, please check the :ref:`dedicated
section <conan_repositories>`.

.. autocommand::
    :command: conan upload -h


The ``conan upload`` command can upload packages to 1 server repository specified by the ``-r=myremote`` argument.

It has 2 possible and mutually exclusive inputs:
- The ``conan upload <pattern>`` pattern-based matching of recipes, with a pattern similar to the ``conan list <pattern>``.
- The ``conan upload --list=<pkglist>`` that will upload the artifacts specified in the ``pkglist`` json file


If the ``--format=json`` formatter is specified, the result will be a "PackageList", compatible with other Conan commands, for example the ``conan remove`` command, so it is possible to concatenate different commands using the generated json file. See the :ref:`Packages Lists examples<examples_commands_pkglists>`.

The ``--dry-run`` argument will prepare the packages for upload, zip files if necessary, check in the server to see what needs to be uploaded and what is already in the server, but it will not execute the actual upload. 

Using the ``core.upload:parallel`` conf, it is possible to upload packages in parallel.
By default, or when set to a value less than ``2``, no parallelization will take place,
and any other value will be the number of parallel threads to utilize.

.. seealso::

    - :ref:`Uploading packages tutorial <uploading_packages>`
    - :ref:`Working with Conan repositories <conan_repositories>`
    - :ref:`Managing remotes with conan remote command <reference_commands_remote>`
    - :ref:`Uploading metadata files<devops_metadata>`.
