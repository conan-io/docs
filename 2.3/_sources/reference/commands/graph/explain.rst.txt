.. _reference_graph_explain:

conan graph explain
===================

.. autocommand::
    :command: conan graph explain -h

The ``conan graph explain`` tries to give a more detailed explanation for a package that might be missing with the configuration provided and show the differences between the expected binary package and the available ones.
It helps to understand what is missing from the package requested, whether it is different options, different settings or different dependencies.

**Example**:

Imagine that we want to install the `lib/1.0.0` that depends on `dep/2.0.0` but we don't have a binary yet, as the latest CI run only generated a binary for lib/1.0.0 using the previous version of `dep`.
When we try to install the refere `lib/1.0.0` it says:

.. code-block:: text

    $ conan install --requires=lib/1.0.0
    ...
    ERROR: Missing prebuilt package for 'lib/1.0.0'

Now we can try to find a explanation for this:

.. code-block:: text

    $ conan graph explain --requires=lib/1.0.0
    requires: dep/1.Y.Z
    diff
      dependencies
        expected: dep/2.Y.Z
        existing: dep/1.Y.Z
        explanation: This binary has same settings and options, but different dependencies

In the same way, it can report when a package has a different option value and the output is also available in JSON format:

.. code-block:: text

    $conan graph explain --requires=lib/1.0.0 -o shared=True --format=json
    ...
    {
        "closest_binaries": {
            "lib/1.0.0": {
                "revisions": {
                    "dc0e384f0551386cd76dc29cc964c95e": {
                        "timestamp": 1692672717.68,
                        "packages": {
                            "b647c43bfefae3f830561ca202b6cfd935b56205": {
                                "info": {
                                    "settings": {
                                        "arch": "x86_64",
                                        "build_type": "Release",
                                        "compiler": "gcc",
                                        "compiler.version": "11",
                                        "os": "Linux"
                                    },
                                    "options": {
                                        "shared": "False"
                                    }
                                },
                                "diff": {
                                    "platform": {},
                                    "options": {
                                        "expected": [
                                            "shared=True"
                                        ],
                                        "existing": [
                                            "shared=False"
                                        ]
                                    },
                                    "settings": {},
                                    "dependencies": {},
                                    "explanation": "This binary was built with same settings but different options."
                                },
                                "remote": "conancenter"
                            }
                        }
                    }
                }
            }
        }
    }
