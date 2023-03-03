conan export
============

.. code-block:: text

    $ conan export -h
    usage: conan export [-h] [-f FORMAT] [-v [V]] [--name NAME]
                        [--version VERSION] [--user USER] [--channel CHANNEL]
                        [-r REMOTE | -nr] [-l LOCKFILE]
                        [--lockfile-out LOCKFILE_OUT] [--lockfile-partial]
                        [--build-require]
                        path

    Export a recipe to the Conan package cache.

    positional arguments:
      path                  Path to a folder containing a recipe (conanfile.py)

    optional arguments:
      -h, --help            show this help message and exit
      -f FORMAT, --format FORMAT
                            Select the output format: json
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      --name NAME           Provide a package name if not specified in conanfile
      --version VERSION     Provide a package version if not specified in
                            conanfile
      --user USER           Provide a user if not specified in conanfile
      --channel CHANNEL     Provide a channel if not specified in conanfile
      -r REMOTE, --remote REMOTE
                            Look in the specified remote or remotes server
      -nr, --no-remote      Do not use remote, resolve exclusively in the cache
      -l LOCKFILE, --lockfile LOCKFILE
                            Path to a lockfile.
      --lockfile-out LOCKFILE_OUT
                            Filename of the updated lockfile
      --lockfile-partial    Do not raise an error if some dependency is not found
                            in lockfile
      --build-require       Whether the provided reference is a build-require


The ``conan export`` command exports the recipe specified in ``path`` to the Conan package cache.
