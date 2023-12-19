Requirements
++++++++++++

Attribute form of the dependencies simple declarations, like ``requires``, ``tool_requires``. 
For more advanced way to define requirements, use the ``requirements()``, ``build_requirements()`` methods instead.

requires
--------

List or tuple of strings for regular dependencies in the host context, like a library.



.. code-block:: python

    class MyLibConan(ConanFile):
        requires = "hello/1.0", "otherlib/2.1@otheruser/testing"


You can specify version ranges, the syntax is using brackets:

.. _version_ranges_reference:


..  code-block:: python

    class HelloConan(ConanFile):
        requires = "pkg/[>1.0 <1.8]"


Accepted expressions would be:

.. list-table::
    :widths: 25 25 50
    :header-rows: 1

    * - Expression
      - Versions in range
      - Versions outside of range
    * - [>=1.0 <2]
      - 1.0.0, 1.0.1, 1.1, 1.2.3
      - 0.2, 2.0, 2.1, 3.0
    * - [<3.2.1]
      - 0.1, 1.2, 2.4, 3.1.1
      - 3.2.2
    * - [>2.0]
      - 2.1, 2.2, 3.1, 14.2
      - 1.1, 1.2, 2.0


If pre-releases are activated, like defining configuration ``core.version_ranges:resolve_prereleases=True``:

.. list-table::
    :widths: 25 25 50
    :header-rows: 1

    * - Expression
      - Versions in range
      - Versions outside of range
    * - [>=1.0 <2]
      - 1.0.0-pre.1, 1.0.0, 1.0.1, 1.1, 1.2.3
      - 0.2, 2.0-pre.1, 2.0, 2.1, 3.0
    * - [<3.2.1]
      - 0.1, 1.2, 1.8-beta.1, 2.0-alpha.2, 2.4, 3.1.1
      - 3.2.1-pre.1, 3.2.1, 3.2.2, 3.3
    * - [>2.0]
      - 2.1-pre.1, 2.1, 2.2, 3.1, 14.2
      - 1.1, 1.2, 2.0-pre.1, 2.0

.. seealso::

    - Check :ref:`tutorial_version_ranges_expressions` version_ranges tutorial section


tool_requires
--------------

List or tuple of strings for dependencies. Represents a build tool like "cmake". If there is
an existing pre-compiled binary for the current package, the binaries for the tool_require
won't be retrieved. They cannot conflict.

.. code-block:: python

    class MyPkg(ConanFile):
        tool_requires = "tool_a/0.2", "tool_b/0.2@user/testing"


This is the declarative way to add ``tool_requires``. Check the :ref:`tool_requires()<reference_conanfile_methods_build_requirements_tool_requires>`
conanfile.py method to learn a more flexible way to add them.


.. _reference_conanfile_attributes_build_requires:


build_requires
--------------

`build_requires` are used in Conan 2.0 to provide compatibility with the Conan 1.X syntax,
but their use is discouraged in Conan 2 and will be deprecated in future 2.X releases.
Please use `tool_requires` instead of `build_requires` in your Conan 2 recipes.


test_requires
--------------

List or tuple of strings for dependencies in the host context only. Represents a test tool
like "gtest". Used when the current package is built from sources.
They don't propagate information to the downstream consumers. If there is
an existing pre-compiled binary for the current package, the binaries for the test_require
won't be retrieved. They cannot conflict.

.. code-block:: python

    class MyPkg(ConanFile):
        test_requires = "gtest/1.11.0", "other_test_tool/0.2@user/testing"


This is the declarative way to add ``test_requires``.
Check the :ref:`test_requires() method<reference_conanfile_methods_build_requirements_test_requires>`
to learn a more flexible way to add them.

python_requires
---------------

This class attribute allows to define a dependency to another Conan recipe and reuse its code.
Its basic syntax is:

.. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        python_requires = "pyreq/0.1@user/channel"  # recipe to reuse code from

        def build(self):
            self.python_requires["pyreq"].module # access to the whole conanfile.py module
            self.python_requires["pyreq"].module.myvar  # access to a variable
            self.python_requires["pyreq"].module.myfunct()  # access to a global function
            self.python_requires["pyreq"].path # access to the folder where the reused file is


Read more about this attribute in :ref:`reference_extensions_python_requires`


python_requires_extend
----------------------

This class attribute defines one or more classes that will be injected in runtime as base classes of
the recipe class. Syntax for each of these classes should be a string like ``pyreq.MyConanfileBase``
where the ``pyreq`` is the name of a ``python_requires`` and ``MyConanfileBase`` is the name of the class
to use.

.. code-block:: python

    from conan import ConanFile

    class Pkg(ConanFile):
        python_requires = "pyreq/0.1@user/channel", "utils/0.1@user/channel"
        python_requires_extend = "pyreq.MyConanfileBase", "utils.UtilsBase"  # class/es to inject
