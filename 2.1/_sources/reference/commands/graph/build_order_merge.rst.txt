conan graph build-order-merge     
=============================

.. autocommand::
    :command: conan graph build-order-merge -h


As described in the ``conan graph build-order`` command, there are 2 types of order ``recipe`` and ``configuration``.
Only build-orders of the same type can be merged together, otherwise the command will return an error.

Note that only build-orders that haven't been reduced with ``--reduce`` can be merged.

The result of merging the different input files can be also reduced with the ``conan graph build-order-merge --reduce``
argument, and the behavior will be the same, leave only the elements that need to be built from source.
 