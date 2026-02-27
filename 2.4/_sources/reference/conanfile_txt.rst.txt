.. _conanfile_txt_reference:

conanfile.txt
=============

The ``conanfile.txt`` file is a simplified version of ``conanfile.py``, aimed at simple consumption of dependencies, but it
cannot be used to create a package. Also, it is not necessary to have a ``conanfile.txt`` for consuming dependencies, 
a ``conanfile.py`` is perfectly suited for simple consumption of dependencies.

It also provides a simplified functionality, for example it is not possible to express conditional requirements in
``conanfile.txt``, and it will be necessary to use a ``conanfile.py`` for that. Read :ref:`consuming_packages_flexibility_of_conanfile_py`
for more information about this.

[requires]
----------

List of requirements, specifying the full reference. Equivalent to ``self.requires(<ref>)`` in ``conanfile.py``. 

.. code-block:: text

    [requires]
    poco/1.9.4
    zlib/1.2.11


This section supports references with version-ranges too:

.. code-block:: text

    [requires]
    poco/[>1.0,<1.9]
    zlib/1.2.11

And specific recipe revisions can be pinned too:

.. code-block:: text

    [requires]
    zlib/1.2.13#revision1
    boost/1.70.0#revision2

[tool_requires]
---------------

List of tool requirements (executable tools) specifying the full reference.
Equivalent to ``self.tool_requires()`` in ``conanfile.py``.

.. code-block:: text

    [tool_requires]
    7zip/16.00
    cmake/3.23.0

This section also supports version ranges and pinned recipe revisions, as above.

In practice the ``[tool_requires]`` will be always installed (same as ``[requires]``) as installing from a *conanfile.txt* means that
something is going to be built, so the tool requirements are indeed needed.
Note however, that by default ``tool_requires`` live in the "build" context, they cannot be libraries to built with, just executable
tools, and for example, using the ``CMakeDeps`` generator, they will not create CMake config files for them (an exception is possible,
but it requires using a ``conanfile.py``, read the :ref:`CMakeDeps reference<conan_tools_cmakedeps>` for more information).


[test_requires]
---------------

List of test requirements specifying the full reference.
Equivalent to ``self.test_requires()`` in ``conanfile.py``.

.. code-block:: text

    [test_requires]
    gtest/1.12.1

This section also supports version ranges and pinned recipe revisions, as above.
The behavior of ``test_requires`` is totally equivalent to the ``[requires]`` section above, as the only difference is that
``test_requires`` are not propagated to consumers, but as a ``conanfile.txt`` is never creating a package that can be consumed, it is
irrelevant. It is provided to maintain the equivalence with ``conanfile.py``


[generators]
------------

List of built-in generators to be used, equivalent to the ``conanfile.py`` ``generators = "CMakeDeps", ...`` attribute.

.. code-block:: text

    [requires]
    poco/1.9.4
    zlib/1.2.13

    [generators]
    CMakeDeps
    CMakeToolchain



[options]
---------

List of options scoped for each package with a pattern like **package_name*:option = Value**.

.. code-block:: text

    [requires]
    poco/1.9.4
    zlib/1.2.11

    [generators]
    CMakeDeps
    CMakeToolchain

    [options]
    poco*:shared=True
    openssl*:shared=True

For example using ``*:shared=True`` will define ``shared=True`` for all packages in the dependency graph that have this
option defined.

    
[layout]
--------


You can specify one name of a predefined layout. The available values are:

- cmake_layout
- vs_layout
- bazel_layout (experimental)


.. code-block:: text

    [layout]
    cmake_layout


.. seealso::

    Read :ref:`consuming_packages_flexibility_of_conanfile_py` for more information about conanfile.txt vs conanfile.py.
