.. _conan_tools_scm_version:

Version
=======

.. warning::

    This tool is **experimental** and subject to breaking changes.


constructor
-----------

.. code-block:: python

    def __init__(self, value: str):


Construct a ``Version`` object from a string. It supports basic version comparison between
objects, like for example:

.. code-block:: python
    
    compiler_lower_than_12 = Version(str(self.settings.compiler.version)) < "12.0"


Please note this is not an implementation of semver, as users may use any
pattern in their versions. It is just a helper to parse "." or "-" and compare taking into
account integers when possible.


Attributes
----------

Available public properties since: `1.52.0 <https://github.com/conan-io/conan/releases/tag/1.52.0>`_

main
+++++

Get all the main digits.

.. code-block:: python

    @property
    def main(self):

For instance:

.. code-block:: python

    v = Version("1.2.3.4-alpha.3+b1")
    assert [str(i) for i in v.main] == ['1', '2', '3', '4', '5']


major
+++++

Get the major digit.

.. code-block:: python

    @property
    def major(self):


For instance:

.. code-block:: python

    v = Version("1.2.3.4-alpha.3+b1")
    assert str(v.major) == "1"



minor
+++++

Get the minor digit.

.. code-block:: python

    @property
    def minor(self):


For instance:

.. code-block:: python

    v = Version("1.2.3.4-alpha.3+b1")
    assert str(v.minor) == "2"


patch
+++++

Get the patch digit.

.. code-block:: python

    @property
    def patch(self):


For instance:

.. code-block:: python

    v = Version("1.2.3.4-alpha.3+b1")
    assert str(v.patch) == "3"


micro
+++++

Get the micro digit.

.. code-block:: python

    @property
    def micro(self):


For instance:

.. code-block:: python

    v = Version("1.2.3.4-alpha.3+b1")
    assert str(v.micro) == "4"


pre
+++

Get the pre-release digit.

.. code-block:: python

    @property
    def pre(self):

For instance:

.. code-block:: python

    v = Version("1.2.3.4-alpha.3+b1")
    assert str(v.pre) == "alpha.3"



build
+++++

Get the build digit.

.. code-block:: python

    @property
    def build(self):

For instance:

.. code-block:: python

    v = Version("1.2.3.4-alpha.3+b1")
    assert str(v.build) == "b1"
