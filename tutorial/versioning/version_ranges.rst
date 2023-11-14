.. _tutorial_versioning_version_ranges:

Version ranges
==============

In the previous section, we ended with several versions of the ``pkg`` package.
Let's remove them and create the following simple project:

.. code-block:: python
    :caption: pkg/conanfile.py

    from conan import ConanFile

    class pkgRecipe(ConanFile):
        name = "pkg"

.. code-block:: python
    :caption: app/conanfile.py

    from conan import ConanFile

    class appRecipe(ConanFile):
        name = "app"
        requires = "pkg/1.0"

Let's create ``pkg/1.0`` and install ``app``, to see it requires ``pkg/1.0``:

.. code-block:: bash

    $ conan remove "pkg*" -c
    $ conan create pkg --version=1.0
    ... pkg/1.0 ...
    $ conan install app
    ...
    Requirements
        pkg/1.0

Then, if we create a new version of ``pkg/1.1``, it will not automatically be used by ``app``:

.. code-block:: bash

    $ conan create pkg --version=1.1
    ... pkg/1.0 ...
    # Note how this still uses the previous 1.0 version
    $ conan install app
    ...
    Requirements
        pkg/1.0

So we could modify ``app`` conanfile to explicitly use the new ``pkg/1.1`` version, but instead of that,
let's use the following version-range expression (introduced by the ``[expression]`` brackets):

.. code-block:: python
    :caption: app/conanfile.py

    from conan import ConanFile

    class appRecipe(ConanFile):
        name = "app"
        requires = "pkg/[>=1.0 <2.0]"

When we now install the dependencies of ``app``, it will automatically use the latest version in the
range, even if we create a new one, without needing to modify the ``app`` conanfile:

.. code-block:: bash

    # this will now use the newer 1.1
    $ conan install app
    ...
    Requirements
        pkg/1.1

    $ conan create pkg --version=1.2
    ... pkg/1.2 ...
    # Now it will automatically use the newest 1.2
    $ conan install app
    ...
    Requirements
        pkg/1.2

This holds as long as the newer version lies within the defined range, if we create a ``pkg/2.0`` version,
``app`` will not use it:

.. code-block:: bash
    
    $ conan create pkg --version=2.0
    ... pkg/2.0 ...
    # Conan will use the latest in the range
    $ conan install app
    ...
    Requirements
        pkg/1.2


Version ranges can be defined in several places:

- In ``conanfile.py`` recipes ``requires``, ``tool_requires``, ``test_requires``, ``python_requires``
- In ``conanfile.txt`` files in ``[requires]``, ``[tool_requires]``, ``[test_requires]`` sections
- In command line arguments like ``--requires=`` and ``--tool_requires``.
- In profiles ``[tool_requires]`` section


Semantic versioning
-------------------

The semantic versioning specification or `semver <https://semver.org/>`_, specifies that packages should
be versioned using always 3 dot-separated digits like ``MAJOR.MINOR.PATCH``, with very specific meanings for each digit.

Conan extends the semver specification to any number of digits, and also allows to include letters in it.
This was done because during 1.X a lot of experience and feedback from users was gathered, and it became evident
than in C++ the versioning scheme is often more complex, and users were demanding more flexibility, allowing
versions like ``1.2.3.a.8`` if necessary.

The ordering of versions when necessary (for example to decide which is the latest version in a version range)
is done by comparing individually each dot-separated entity in the version, from left to right. Digits will be
compared numerically, so 2 < 11, and entries containing letters will be compared alphabetically (even if they
also contain some numbers).

Similarly to the semver specification, Conan can manage **prereleases** and **builds** in the form: 
``VERSION-prerelease+build``.
Conan will also order pre-releases and builds according to the same rules, and each one of them can also
contain an arbitrary number of items, like ``1.2.3-pre.1.2.1+build.45.a``.
Note that the semver standard does not apply any ordering to builds, but Conan does, with the same logic that
is used to order the main version and the pre-releases.


.. important::

    Note that the ordering of pre-releases can be confusing at times. A pre-release happens earlier in
    time than the release it is qualifying. So ``1.1-alpha.1`` is older than ``1.1``, not newer.


.. _tutorial_version_ranges_expressions:

Range expressions
-----------------

Range expressions can have comparison operators for the lower and higher bounds, separated with a space.
Also, lower bounds and upper bounds in isolation are permitted, though they are generally not recommended
under normal versioning schemes, specially the lower bound only. ``requires = "pkg/[>=1.0 <2.0]"`` will 
include versions like 1.0, 1.2.3 and 1.9, but will not include 0.3, 2.0 or 2.1 versions.


The tilde ``~`` operator can be used to define an "approximately" equal version range. ``requires = "pkg/[~1]"``
will include versions 1.3 and 1.8.1, but will exclude versions like 0.8 or 2.0. Likewise
``requires = "pkg/[~2.5]"`` will include 2.5.0 and 2.5.3, but exclude 2.1, 2.7, 2.8.

The caret ``^`` operator is very similar to the tilde, but allowing variability over the last defined digit.
``requires = "pkg/[^1.2]"`` will include 1.2.1, 1.3 and 1.51, but will exclude 1.0, 2, 2.0.

It is also possible to apply multiple conditions with the OR operator, like ``requires = "pkg/[>1 <2.0 || ^3.2]"``
but this kind of complex expressions is not recommended in practice and should only be used in very extreme cases.

Finally, note that pre-releases are not resolved by default. The way to include them in the range is to
explicitly enable them with either the ``include_prerelease`` option (``requires = "pkg/[>1 <2, include_prerelease]"``),
or via the ``core.version_ranges:resolve_prereleases=True`` configuration. In this example, 1.0-pre.1 and 1.5.1-pre1 will be included,
but 2.0-pre1 would be excluded.

.. note::

   While it is possible to hardcode the ``include_prerelease`` in the ``requires`` version range, it is not recommended generally.
   Pre-releases should be opt-in, and controlled by the user, who decides if they want to use pre-releases. 
   Also, note that the ``include_prereleases`` receives no argument, hence it's not possible to deactivate prereleases with ``include_prerelease=False``.

For more information about valid range expressions go to :ref:`Requires reference <version_ranges_reference>`
