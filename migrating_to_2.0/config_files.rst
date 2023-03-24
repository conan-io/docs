Configuration files
-------------------


Profiles
========

Profiles in Conan 2.0 drop the textual replacement of variables.

This profile will not work in 2.0:

.. code-block:: text
    :caption: profile

    MYVAR = FreeBSD
    [settings]
    os = $MYVAR

The profile below is the 2.0 equivalent, now supporting Jinja syntax. This enables more dynamic content and customization possibilities.

.. code-block:: text
    :caption: profile.jinja

    {% set a = "FreeBSD" %}
    [settings]
    os = {{ a }}


The ``.jinja`` extension in the profile name is necessary in 1.X but will not be necessary in 2.0



conan.conf
==========

The ``conan.conf`` file is superseded by the ``global.conf`` file. Use only new ``conan config list``
items in the ``global.conf`` file.

remotes.txt
===========

This file has been removed in Conan 2.0 as a definition of remotes. The ``remotes.json`` file is the
one to be used in 2.0 (remotes.txt will be completely ignored).
