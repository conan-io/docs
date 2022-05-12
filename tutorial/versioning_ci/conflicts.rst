.. _tutorial_versioning_conflicts:

Version conflicts
=================

Explain briefly about potential version conflicts with diamond graphs. Use figure of graph.


.. code-block:: bash

    $  git clone git@github.com:conan-io/examples2.git
    $ cd tutorial/consuming/versioning/conflicts
    $ conan create math --version=1.0
    $ conan create math --version=2.0
    $ conan create engine
    $ conan create ai
    $ conan install game

    > ERROR: Version conflicts
    # TODO: This message will change and improve


The consumer, in this case "game" can decide which is the resolution



