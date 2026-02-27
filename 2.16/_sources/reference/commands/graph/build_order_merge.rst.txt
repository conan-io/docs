conan graph build-order-merge     
=============================

.. autocommand::
    :command: conan graph build-order-merge -h


As described in the ``conan graph build-order`` command, there are 2 types of order ``recipe`` and ``configuration``.
Only build-orders of the same type can be merged together, otherwise the command will return an error.

Note that only build-orders that haven't been reduced with ``--reduce`` can be merged.

The result of merging the different input files can be also reduced with the ``conan graph build-order-merge --reduce``
argument, and the behavior will be the same, leave only the elements that need to be built from source.
 

When 2 or more "build-order" files are merged, the resulting merge contains a ``profiles`` section like:

.. code-block:: json

    "profiles": {
        "build_order_win": {
            "args": "-pr:h=\"profile1\" -s:h=\"os=Windows\" ..."
        },
        "build_order_nix": {
            "args": "-pr:h=\"profile2\" -s:h=\"os=Linux\" ..."
        }
    }

With the ``build_order_win`` and ``build_order_nix`` being the "build-order" filenames that were used as inputs to the merge, and which will be referenced in the ``filenames`` field of every ``package`` in the build order. This way, it is easier to obtain the necessary command line arguments to build a specific package binary in the build-order when building multiple configurations.
          