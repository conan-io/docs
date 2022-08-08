.. _conan_tools_scm_version:

Version
=======

.. warning::

    This tool is **experimental** and subject to breaking changes.

Available since: `1.46.0 <https://github.com/conan-io/conan/releases/tag/1.46.0>`_

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