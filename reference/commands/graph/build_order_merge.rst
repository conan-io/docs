.. _reference_graph_build_order_merge:

conan graph build-order-merge
=============================


.. code-block:: text

    $ conan graph build-order-merge -h
    usage: conan graph build-order-merge [-h] [-f FORMAT] [-v [V]]
                                         [--file [FILE]]

    Merge more than 1 build-order file.

    optional arguments:
      -h, --help            show this help message and exit
      -f FORMAT, --format FORMAT
                            Select the output format: json
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      --file [FILE]         Files to be merged

This command merges 2 or more outputs in json format from :ref:`conan graph build-order<reference_graph_build_order>`.
