.. _tutorial_versioning_conflicts:

Dependencies conflicts
======================

In a dependency graph, when different packages depends on different versions of the
same package, this is called a dependency version conflict. It is relatively easy
to produce one. Let's see it with a practical example, start cloning 
the `examples2 repository <https://github.com/conan-io/examples2>`_:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/versioning/conflicts/versions

In this folder we have a small project, consisting in several packages: ``matrix`` (a math library),
``engine/1.0`` video game engine that depends on ``matrix/1.0``, ``intro/1.0``, a package implementing
the intro credits and functionality for the videogame that depends on ``matrix/1.1`` and finally the
``game`` recipe that depends simultaneously on ``engine/1.0`` and ``intro/1.0``. All these packages
are actually empty, but they are enough to produce the conflicts.

.. graphviz::
    :align: center

    digraph conflict {
        node [fillcolor="lightskyblue", style=filled, shape=box]
        rankdir="BT"
        "game/1.0" -> "engine/1.0" -> "matrix/1.0";
        "game/1.0" -> "intro/1.0" -> "matrix/1.1";
        "matrix/1.0" [fillcolor="orange"];
        "matrix/1.1" [fillcolor="orange"];
    }

|

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
so they point now to the same version. However this might not be practical in
some cases, or it might be even impossible to fix the dependencies conanfiles. 

For that case, it should be the consuming ``conanfile.py`` the one that can resolve
the conflict (in this case, ``game``) by explicitly defining which version of the
dependency should be used, with the following syntax:

.. code-block:: python
    :caption: game/conanfile.py
    :emphasize-lines: 8

    class Game(ConanFile):
        name = "game"
        version = "1.0"
        
        def requirements(self):
            self.requires("engine/1.0")
            self.requires("intro/1.0")
            self.requires("matrix/1.1", override=True)

This is called an ``override``. The ``game`` package do not directly depend on ``matrix``, this
``requires`` declaration will not introduce such a a direct dependency. But the ``matrix/1.1``
version will be propagated upstream in the dependency graph, overriding the ``requires`` of
packages that do depend on any ``matrix`` version, forcing the consistency of the graph, as all
upstream packages will now depend on ``matrix/1.1``:

.. code-block:: bash

    $ conan install game
    ...
    Requirements
        engine/1.0#0fe4e6890766f7b8e21f764f0049aec7 - Cache
        intro/1.0#d639998c2e55cf36d261ab319801c322 - Cache
        matrix/1.1#905c3f0babc520684c84127378fefdd0 - Cache

.. graphviz::
    :align: center

    digraph conflict {
        node [fillcolor="lightskyblue", style=filled, shape=box]
        rankdir="BT"
        "game/1.0" -> "engine/1.0" -> "matrix/1.1";
        "game/1.0" -> "intro/1.0" -> "matrix/1.1";
        {
            rank = same;
            edge[ style=invis];
            "matrix/1.1" -> "matrix/1.0" ;
            rankdir = LR;
        }
    }

|

.. note::

    In this case, a new binary for ``engine/1.0`` was not necessary, but in some situations the above could
    fail with a ``engine/1.0`` "binary missing error". Because previously ``engine/1.0`` binaries were
    built against ``matrix/1.0``. If the ``package_id`` rules and configuration define that ``engine`` should
    be rebuilt when minor versions of the dependencies change, then it will be necessary to build a new
    binary for ``engine/1.0`` that builds and links against the new ``matrix/1.1`` dependency.


What happens if ``game`` had a direct dependency to ``matrix/1.2``? Lets create the version:


.. code-block:: bash
    
    $ conan create matrix --version=1.2

Now lets modify ``game/conanfile.py`` to introduce this as a direct dependency:

.. code-block:: python
    :caption: game/conanfile.py

    class Game(ConanFile):
        name = "game"
        version = "1.0"
        
        def requirements(self):
            self.requires("engine/1.0")
            self.requires("intro/1.0")
            self.requires("matrix/1.2")


.. graphviz::
    :align: center

    digraph conflict {
        node [fillcolor="lightskyblue", style=filled, shape=box]
        rankdir="BT"
        "game/1.0" -> "engine/1.0" -> "matrix/1.0";
        "game/1.0" -> "intro/1.0" -> "matrix/1.1";
        "game/1.0" -> "matrix/1.2";
        "matrix/1.0" [fillcolor="orange"];
        "matrix/1.1" [fillcolor="orange"];
        "matrix/1.2" [fillcolor="orange"];
        {
            rank = same;
            edge[ style=invis];
            "matrix/1.1" -> "matrix/1.2" ;
            rankdir = LR;
        }
    }

|

So installing it will raise a conflict error again:

.. code-block:: bash

    $ conan install game
    ...
    ERROR: Version conflict: engine/1.0->matrix/1.0, game/1.0->matrix/1.2.

As this time, we want to respect the direct dependency between ``game`` and ``matrix``, we will
define the ``force=True`` requirement trait, to indicate that this dependency version will also
be forcing the overrides upstream:

.. code-block:: python
    :caption: game/conanfile.py

    class Game(ConanFile):
        name = "game"
        version = "1.0"
        
        def requirements(self):
            self.requires("engine/1.0")
            self.requires("intro/1.0")
            self.requires("matrix/1.2", force=True)


And that will now solve again the conflict (as commented above, note that in real applications this could mean that binaries
for ``engine/1.0`` and ``intro/1.0`` would be missing, and need to be built to link against the new forced
``matrix/1.2`` version):

.. code-block:: bash

    $ conan install game
    Requirements
        engine/1.0#0fe4e6890766f7b8e21f764f0049aec7 - Cache
        intro/1.0#d639998c2e55cf36d261ab319801c322 - Cache
        matrix/1.2#905c3f0babc520684c84127378fefdd0 - Cache

.. graphviz::
    :align: center

    digraph conflict {
        node [fillcolor="lightskyblue", style=filled, shape=box]
        rankdir="BT"
        "game/1.0" -> "engine/1.0" -> "matrix/1.2";
        "game/1.0" -> "intro/1.0" -> "matrix/1.2";
        "game/1.0" -> "matrix/1.2";
        {
            rank = same;
            edge[ style=invis];
            "matrix/1.2" -> "matrix/1.0" -> "matrix/1.1" ;
            rankdir = LR;
        }
    }

|

.. note::

    **Best practices**

    - Resolving version conflicts by overrides/forces should in general be the exception and avoided when possible, applied as a temporary workaround. The real solution is to move forward the dependencies ``requires`` so they naturally converge to the same versions of upstream dependencies.
    - Version-ranges can also produce some version conflicts, even if Conan tries to reduce them. This :ref:`FAQ about version conflicts<faq_version_conflicts_version_ranges>` discusses the graph resolution algorithm and strategies to minimize the conflicts.



Overriding options
------------------

It is possible that when there are diamond structures in a dependency graph, like the one seen above, different
recipes might be defining different values for the upstream ``options``. In this case, this is not directly 
causing a conflict, but instead the first value to be defined is the one that will be prioritized and will
prevail.

In the above example, if ``matrix/1.0`` can be both a static and a shared library, and ``engine`` decides to
define that it should be a static library (not really necessary, because that is already the default):

.. code-block:: python
    :caption: engine/conanfile.py
    
    class Engine(ConanFile):
        name = "engine"
        version = "1.0"
        # Not strictly necessary because this is already the matrix default
        default_options = {"matrix*:shared": False}


.. warning::

    Defining options values in recipes does not have strong guarantees, please check 
    :ref:`this FAQ about options values for dependencies<faq_different_options_values>`. The recommended way
    to define options values is in profile files.

And also ``intro`` recipe would do the same, but instead define that it wants a shared library, and adds a
``validate()`` method, because for some reason the ``intro`` package can only be built against shared libraries
and otherwise crashes:

.. code-block:: python
    :caption: intro/conanfile.py

    class Intro(ConanFile):
        name = "intro"
        version = "1.0"
        default_options = {"matrix*:shared": True}

        def requirements(self):
            self.requires("matrix/1.0")

        def validate(self):
            if not self.dependencies["matrix"].options.shared:
                raise ConanInvalidConfiguration("Intro package doesn't work with static matrix library")

Then, this will cause an error, because as the first one to define the option value is ``engine`` (it is 
declared first in the ``game`` conanfile ``requirements()`` method).
In the examples2 repository, go to the "options" folder, and create the different packages:


.. code-block:: text

    $ cd ../options
    $ conan create matrix
    $ conan create matrix -o matrix/*:shared=True
    $ conan create engine
    $ conan create intro
    $ conan install game  # FAILS!
    ...
    -------- Installing (downloading, building) binaries... --------
    ERROR: There are invalid packages (packages that cannot exist for this configuration):
    intro/1.0: Invalid: Intro package doesn't work with static matrix library


Following the same principle, the downstream consumer recipe, in this case ``game`` conanfile.py
can define the options values, and those will be prioritized:

.. code-block:: python
    :caption: game/conanfile.py

    class Game(ConanFile):
        name = "game"
        version = "1.0"
        default_options = {"matrix*:shared": True}
        
        def requirements(self):
            self.requires("engine/1.0")
            self.requires("intro/1.0")


And that will force now ``matrix`` being a shared library, no matter if ``engine`` defined ``shared=False``,
because the downstream consumers always have priority over the upstream dependencies.

.. code-block:: bash

    $ conan install game 
    ...
    -------- Installing (downloading, building) binaries... --------
    matrix/1.0: Already installed!
    matrix/1.0: I am a shared-library library!!!
    engine/1.0: Already installed!
    intro/1.0: Already installed!

.. note::

    **Best practices**

    As a general rule, avoid modifying or defining values for dependencies ``options`` in consumers ``conanfile.py``.
    The declared ``options`` defaults should be good for the majority of cases, and variations from those defaults
    can be defined better in profiles better.
