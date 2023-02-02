.. _tutorial_versioning_conflicts:

Version conflicts
=================

In a dependency graph, when different packages depends on different versions of the
same package, this is called a dependency version conflict. It is relatively easy
to produce one. Let's see it with a practical example, start cloning 
the `examples2.0 repository <https://github.com/conan-io/examples2>`_:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/versioning/conflicts/versions

In this folder we have a small project, consisting in several packages: ``matrix`` (a math library),
``engine/1.0```video game engine that depends on ``matrix/1.0``, ``intro/1.0``, a package implementing
the intro credits and functionality for the videogame that depends on ``matrix/1.1`` and finally the
``game`` recipe that depends simultaneously on ``engine/1.0`` and ``intro/1.0``. All these packages
are actually empty, but they are enough to produce the conflicts.

Let's create the dependencies:

.. code-block:: bash
    
    $ conan create matrix --version=1.0
    $ conan create matrix --version=1.1  # note this is 1.1!
    $ conan create engine --version=1.0 # depends on matrix/1.0
    $ conan create intro --version=1.0 # depends on matrix/1.1

And when we try to install ``game``, we will get the error:

.. code-block:: bash
    
    $ conan install game
    Requirements
        engine/1.0#0fe4e6890766f7b8e21f764f0049aec7 - Cache
        intro/1.0#d639998c2e55cf36d261ab319801c322 - Cache
        matrix/1.0#905c3f0babc520684c84127378fefdd0 - Cache
    Graph error
        Version conflict: intro/1.0->matrix/1.1, game/1.0->matrix/1.0.
    ERROR: Version conflict: intro/1.0->matrix/1.1, game/1.0->matrix/1.0.

This is a version conflict, and Conan will not decide automatically how to
resolve the conflict, but the user should explicitly resolve such conflict.


Resolving conflicts
-------------------

Of course, the most direct and straightforward way to solve such a conflict is
going to the dependencies ``conanfile.py`` and upgrading their ``requirements()``
so they point now the tha same version. However this might not be practical in
some cases, or it might be even impossible to fix the dependencies. For that
case there could be different strategies:

- Override/Force


