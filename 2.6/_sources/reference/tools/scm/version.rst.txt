.. _conan_tools_scm_version:

Version
=======

This is a helper class to work with versions, it splits the version string based on dots and hyphens.
It exposes all the version components as properties and offers total ordering through compare operators.

.. code-block:: python
   :caption: Comparing versions

    compiler_lower_than_12 = Version(self.settings.compiler.version) < "12.0"

    is_legacy = Version(self.version) < 2


.. autoclass:: conan.tools.scm::Version


Attributes
----------

The ``Version`` class offers ways to access the different parts of the version number:

main
++++

Get all the main digits.

.. code-block:: python

    v = Version("1.2.3.4-alpha.3+b1")
    assert [str(i) for i in v.main] == ['1', '2', '3', '4', '5']

major
+++++

Get the major digit.

.. code-block:: python

    v = Version("1.2.3.4-alpha.3+b1")
    assert str(v.major) == "1"

minor
+++++

Get the minor digit.

.. code-block:: python

    v = Version("1.2.3.4-alpha.3+b1")
    assert str(v.minor) == "2"


patch
+++++

Get the patch digit.

.. code-block:: python

    v = Version("1.2.3.4-alpha.3+b1")
    assert str(v.patch) == "3"


micro
+++++

Get the micro digit.

.. code-block:: python

    v = Version("1.2.3.4-alpha.3+b1")
    assert str(v.micro) == "4"


pre
+++

Get the pre-release digit.

.. code-block:: python

    v = Version("1.2.3.4-alpha.3+b1")
    assert str(v.pre) == "alpha.3"

build
+++++

Get the build digit.

.. code-block:: python

    v = Version("1.2.3.4-alpha.3+b1")
    assert str(v.build) == "b1"
