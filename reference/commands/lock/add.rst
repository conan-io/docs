conan lock add
==============

.. code-block:: text

    $ conan lock add -h
    usage: conan lock add [-h] [-v [V]] [--logger] [--requires REQUIRES]
                          [--build-requires BUILD_REQUIRES]
                          [--python-requires PYTHON_REQUIRES]
                          [--lockfile-out LOCKFILE_OUT] [--lockfile LOCKFILE]

    Add requires, build-requires or python-requires to an existing or new
    lockfile. The resulting lockfile will be ordered, newer versions/revisions
    first. References can be supplied with and without revisions like "--
    requires=pkg/version", but they must be package references, including at least
    the version, and they cannot contain a version range.

    optional arguments:
      -h, --help            show this help message and exit
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      --logger              Show the output with log format, with time, type and
                            message.
      --requires REQUIRES   Add references to lockfile.
      --build-requires BUILD_REQUIRES
                            Add build-requires to lockfile
      --python-requires PYTHON_REQUIRES
                            Add python-requires to lockfile
      --lockfile-out LOCKFILE_OUT
                            Filename of the created lockfile
      --lockfile LOCKFILE   Filename of the input lockfile
