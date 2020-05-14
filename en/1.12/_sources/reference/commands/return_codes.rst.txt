Return Codes
============

The Conan client returns different exit codes for every command depending on the situation:

Success
-------

Return code: ``0``

Execution terminated successfully

General error
-------------

Return code: ``1``

Execution terminated with a general error, normally caused by a ``ConanException``.

Migration error
---------------

Return code: ``2``

Execution terminated with an error migrating configuration files to new format.

User Ctrl+C
-----------

Return code: ``3``

Execution terminated due to manually stopping the process with ``Ctrl+C`` key combination.

User Ctrl+Break
---------------

Return code: ``4``

Execution terminated due to manually stopping the profess with ``Ctrl+Break`` key combination.

SIGTERM
-------

Return code: ``5``

Execution terminated due to ``SIGTERM`` signal.

Invalid configuration
---------------------

Return code: ``6``

Execution terminated due to an exception caused by a ``ConanInvalidConfiguration``. This exit code
can be considered a success as it is expected for
:ref:`configurations not supported by the recipe <invalid_configuration>`.
