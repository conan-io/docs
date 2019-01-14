Miscellanea
===========

Additional documentation of Python classes to be used in recipes

Version
-------

.. code-block:: python

    class Version(str)

Represents a version string providing useful comparison methods following semantic versioning criteria.

.. code-block:: python

    Version("1.2.1-dev") > Version("1.2.0")

Properties
++++++++++

as_list
^^^^^^^

Return the version as a list of items splitting the string by points.

.. code-block:: bash

    >>> Version("1.2.3").as_list
    [1, 2, 3]
    >>> Version("1.2.3b").as_list
    [1, 2, '3b']

build
^^^^^

Return the build number of the version if any. Build number is separated by `+` in semantic versioning.

.. code-block:: bash

    >>> Version("1.2.3+93").build
    '93'
    >>> Version("1.2+32983").build
    '32983'

base
^^^^

Return only the base part of version if any (without build).

.. code-block:: bash

    >>> Version("1.2.3+93").base
    '1.2.3'
    >>> Version("1.2+32983").base
    '1.2'

Methods
+++++++

major()
^^^^^^^

.. code-block:: python

    def major(self, fill=True)

Get the major item from the version string.

.. code-block:: bash

    >>> Version("1.2.3+9328043").major()
    '1.Y.Z'
    >>> Version("1.2.3+9328043").major(fill=False)
    '1'

Parameters:
    - **fill** (Optional, Defaulted to `True`): Fill full version format with ``<major>.Y.Z``

minor()
^^^^^^^

.. code-block:: python

    def minor(self, fill=True)

Get the major and minor items from the version string.

.. code-block:: bash

    >>> Version("1.2.3+9328043").minor()
    '1.2.Z'
    >>> Version("1.2.3+9328043").minor(fill=False)
    '1.2'

Parameters:
    - **fill** (Optional, Defaulted to `True`): Fill full version format with ``<major>.<minor>.Z``

patch()
^^^^^^^

.. code-block:: python

    def patch()

Get the major and minor items from the version string.

.. code-block:: bash

    >>> Version("1.2.3+9328043").minor()
    '1.2.3'

stable()
^^^^^^^^

.. code-block:: python

    def stable()

Get the stable version in a `<major>.Y.Z format, otherwise return the version `0.Y.Z` is not considered stable in semantic versioning. If
version is not stable it will return the actual version.

.. code-block:: bash

    >>> Version("1.2.3+9328043").stable()
    '1.Y.Z'
    >>> Version("0.2.3+9328043").major(fill=False)
    '0.2.3+9328043'

pre()
^^^^^

.. code-block:: python

    def pre()

Get version with the pre-release part.

.. code-block:: bash

    >>> Version("1.2.3-alpha").pre()
    '1.2.3-alpha'
    >>> Version("0.2.3-alpha+9328043").pre()
    '1.2.3-alpha'

compatible()
^^^^^^^^^^^^

.. code-block:: python

    def compatible(self, other)

Compare two Version classes and determine if they are semantic version compatible. This will check for same major, minor and patch items and
discard additional items. Useful to check compatibility with major/minor versions with `<major>.Y.Z` format.

.. code-block:: bash

    >>> Version("1.2.3").compatible("1.3.0")
    False
    >>> Version("1.2.3").compatible(Version("1.2.2"))
    False
    >>> Version("1.2.3").compatible(Version("1.2.2").minor())
    True
