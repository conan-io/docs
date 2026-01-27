.. _reference_commands_require:

conan require
=============

.. include:: ../../common/experimental_warning.inc

.. autocommand::
    :command: conan require -h


The :command:`conan require` command helps to add any requirement as a version range or remove it from your *conanfile.py*. 


.. important::

    This command is only a UX utility. It's not aimed at replacing editing the conanfile, and it's not expected to cover
    all the use cases, i.e., conditional requirements, requirements with different traits, etc. For all those mentioned
    scenarios, we recommend editing the conanfile.py as usual.


conan require add
-----------------

.. autocommand::
    :command: conan require add -h

Add a new requirement to your local *conanfile.py* as a version range.

By default, it looks for the recipe name in any of your remotes. When a remote contains any result for the recipe
required, the latest version is used and written as a version range between the version found and the next major one
(if possible, as versions based on commits do not have that major version):

.. code-block:: bash

    $ conan require add fmt
    Connecting to remote 'conancenter' anonymously
    Found 21 pkg/version recipes matching fmt/* in conancenter
    Added 'fmt/[>=12.1.0 <13]' as a new requires.

It admits several arguments as new requirements:

.. code-block:: bash

    $ conan require add fmt zlib
    Connecting to remote 'conancenter' anonymously
    Found 21 pkg/version recipes matching fmt/* in conancenter
    Found 5 pkg/version recipes matching zlib/* in conancenter
    Added 'fmt/[>=12.1.0 <13]' as a new requires.
    Added 'zlib/[>=1.3.1 <2]' as a new requires.

Or even, you can directly put the requirement version:

.. code-block:: bash

    $ conan require add boost/1.89.0
    Added 'boost/[>=1.89.0 <2]' as a new requires.


Tool and test requirements are also supported:

.. code-block:: bash

    $ conan require add --tool cmake --test gtest
    Connecting to remote 'conancenter' anonymously
    Found 54 pkg/version recipes matching cmake/* in conancenter
    Found 10 pkg/version recipes matching gtest/* in conancenter
    Added 'cmake/[>=4.2.2 <5]' as a new tool_requires.
    Added 'gtest/cci.20210126' as a new test_requires.

Use ``--no-remote`` to resolve versions only from the local cache:

.. code-block:: bash

    $ conan require add boost --no-remote
    Found 2 pkg/version recipes matching boost/* in local cache
    Added 'boost/[>=1.89.0 <2]' as a new requires.


Use ``--folder`` to point to a different recipe location:

.. code-block:: text

    $ conan require add fmt --folder=path/to/conanfile.py


conan require remove
--------------------

.. autocommand::
    :command: conan require remove -h

Remove any requirement from your *conanfile.py*:

.. code-block:: bash

    $ conan require remove fmt zlib
    Removed fmt dependency as requires.
    Removed zlib dependency as requires.

Tool and test requirements are also supported:

.. code-block:: bash

    $ conan require remove --tool cmake --test gtest
    Removed cmake dependency as tool_requires.
    Removed gtest dependency as test_requires.

Use ``--folder`` to point to a different recipe location:

.. code-block:: text

    $ conan require remove fmt --folder=path/to/conanfile.py
