conan lock merge
================

.. code-block:: text

    $ conan lock merge -h
    usage: conan lock merge [-h] [-v [V]] [--lockfile LOCKFILE]
                            [--lockfile-out LOCKFILE_OUT]

    Merge 2 or more lockfiles.

    optional arguments:
      -h, --help            show this help message and exit
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      --lockfile LOCKFILE   Path to lockfile to be merged
      --lockfile-out LOCKFILE_OUT
                            Filename of the created lockfile