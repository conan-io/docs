.. _reference_commands_require:

conan require
=============

.. include:: ../../common/experimental_warning.inc

.. autocommand::
    :command: conan require -h


The :command:`conan require` command helps to add any requirement as a version range or remove it from your *conanfile.py*. 


conan require add
-----------------

.. autocommand::
    :command: conan require add -h

Add a new requirement to your local *conanfile.py* as a version range:

.. code-block:: text

    $ conan require add fmt
    Connecting to remote 'conancenter' anonymously
    Found 21 pkg/version recipes matching fmt/* in conancenter
    Added 'fmt/[>=12.1.0 <13]' as a new requires.



conan require remove
--------------------

.. autocommand::
    :command: conan require remove -h

Remove any requirement from your *conanfile.py*:

.. code-block:: text

    $ conan require remove fmt
    Removed fmt dependency as requires.
