.. _reference_commands_upload:

conan upload
============

Use this command to upload recipes and binaries to Conan repositories. For more
information on how to work with Conan repositories, please check the :ref:`dedicated
section <conan_repositories>`.

.. code-block:: text

    $ conan upload -h
    usage: conan upload [-h] [-v [V]] [-p PACKAGE_QUERY] -r REMOTE
                        [--only-recipe] [--force] [--check] [-c]
                        reference

    Upload packages to a remote.

    By default, all the matching references are uploaded (all revisions).
    By default, if a recipe reference is specified, it will upload all the revisions for all the
    binary packages, unless --only-recipe is specified. You can use the "latest" placeholder at the
    "reference" argument to specify the latest revision of the recipe or the package.

    positional arguments:
      reference             Recipe reference or package reference, can contain *
                            as wildcard at any reference field. If no revision is
                            specified, it is assumed to be the latest

    optional arguments:
      -h, --help            show this help message and exit
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
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

Read more
---------

- :ref:`Uploading packages tutorial <uploading_packages>`
- :ref:`Working with Conan repositories <conan_repositories>`
- :ref:`Managing remotes with conan remote command <reference_commands_remote>`
