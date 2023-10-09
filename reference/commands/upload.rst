.. _reference_commands_upload:

conan upload
============

Use this command to upload recipes and binaries to Conan repositories. For more
information on how to work with Conan repositories, please check the :ref:`dedicated
section <conan_repositories>`.

.. code-block:: text

    $ conan upload -h
    usage: conan upload [-h] [-v [V]] [-f FORMAT] [-p PACKAGE_QUERY] -r REMOTE
                        [--only-recipe] [--force] [--check] [-c] [--dry-run]
                        [-l LIST] [-m METADATA]
                        [pattern]

    Upload packages to a remote.

    By default, all the matching references are uploaded (all revisions).
    By default, if a recipe reference is specified, it will upload all the revisions for all the
    binary packages, unless --only-recipe is specified. You can use the "latest" placeholder at the
    "reference" argument to specify the latest revision of the recipe or the package.

    positional arguments:
      pattern               A pattern in the form
                            'pkg/version#revision:package_id#revision', e.g:
                            zlib/1.2.13:* means all binaries for zlib/1.2.13. If
                            revision is not specified, it is assumed latest one.

    optional arguments:
      -h, --help            show this help message and exit
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      -f FORMAT, --format FORMAT
                            Select the output format: json
      -p PACKAGE_QUERY, --package-query PACKAGE_QUERY
                            Only upload packages matching a specific query. e.g:
                            os=Windows AND (arch=x86 OR compiler=gcc)
      -r REMOTE, --remote REMOTE
                            Upload to this specific remote
      --only-recipe         Upload only the recipe/s, not the binary packages.
      --force               Force the upload of the artifacts even if the revision
                            already exists in the server
      --check               Perform an integrity check, using the manifests,
                            before upload
      -c, --confirm         Upload all matching recipes without confirmation
      --dry-run             Do not execute the real upload (experimental)
      -l LIST, --list LIST  Package list file
      -m METADATA, --metadata METADATA
                            Upload the metadata, even if the package is already in
                            the server and not uploaded


The ``conan upload`` command can upload packages to 1 server repository specified by the ``-r=myremote`` argument.

It has 2 possible and mutually exclusive inputs:
- The ``conan upload <pattern>`` pattern-based matching of recipes, with a pattern similar to the ``conan list <pattern>``.
- The ``conan upload --list=<pkglist>`` that will upload the artifacts specified in the ``pkglist`` json file


If the ``--format=json`` formatter is specified, the result will be a "PackageList", compatible with other Conan commands, for example the ``conan remove`` command, so it is possible to concatenate different commands using the generated json file. See the :ref:`Packages Lists examples<examples_commands_pkglists>`.

The ``--dry-run`` argument will prepare the packages for upload, zip files if necessary, check in the server to see what needs to be uploaded and what is already in the server, but it will not execute the actual upload. 


Read more
---------

- :ref:`Uploading packages tutorial <uploading_packages>`
- :ref:`Working with Conan repositories <conan_repositories>`
- :ref:`Managing remotes with conan remote command <reference_commands_remote>`
