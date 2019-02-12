.. _lockfile:


Locking mechanism for version ranges
====================================

Lock mechanism in conan is provided to accomplish build reproducibility.

To better understand the problem lets analyse the following example:

- We are responsible for package ``XYZ``.
- Conan recipe ``XYZ`` depends on ``A`` in version range ``[>=1.0]``.
- Recipe ``A`` exists in version 1.0.
- We are packaging ``XYZ`` and sending to our customers.
- In meantime there is a new version of recipe ``A``,  1.1.
- We want to recreate an exact build that was sent to our customers.

If we will build ``XYZ`` without of any preparation we cannot tell
if package ``A`` has been chosen in version 1.0 or 1.1. We can use ``--update``
argument to be sure that the newest package is used (1.1).
But how to ensure version 1.0? This is where version ranges lock mechanism 
has its use.

As resolution of version ranges may happens at many places
the solution is command agnostic. The arguments from this page can
be applied to all conan commands. For more information about arguments
you can execute:

.. code-block:: bash

    conan --help



Lockfile
--------

Conan is using a file (by default it is ``conan.lock``) where pinned versions
of dependencies are stored. Later in this document it is called lockfile.
This file has similar structure to what's found in Microsoft Windows INI files.
Lockfile by default is meant to be in current directory where conan
is executed. This is where conan will try to find it.

The place and name of lockfile can be change by passing ``--lockfile PATH``
argument to conan.

.. code-block:: bash

    conan --lockfile ~/my_precious_build info .


Locking
-------

To create lockfile you have to pass ``--lock`` argument to conan.

.. code-block:: bash

    conan --lock info .

If no ``--lockfile`` will be passed then ``conan.lock`` will be used (created).
Note that ``--lock`` is command agnostic. Therefore it's up to you to
use a command that fits you the best (resolves dependencies).

Example if I want to create lockfile at explicit path:

.. code-block:: bash

    conan --lock --lockfile ~/my_precious_build install .

Note that if lockfile already exists then it will be updated.
If you want to recreate it from scratch then you should remove that file first.

It is important to say that not only dependencies from your package are being
saved but all graph of dependencies. Thanks to that you don't need
to worry about transitive dependencies.

Reproduce the resolution of versions from lockfile
--------------------------------------------------

Conan will try to use lockfile, by default it will try to find ``conan.lock``
in current directory. If you have lockfile but you don't want to use it then
you should pass ``--skip-lockfile`` argument.

.. code-block:: bash

    $ ls conan.lock
    conan.lock
    $ conan --skip-lockfile install . --update 

If dependency graph is not independent
--------------------------------------

Situation where dependency graph is changing because of options, environment, 
setting, profile etc. is common. But there are couple of solutions that
you can apply in this situation.

First of all lockfile is meant to be used with the same environment, options,
settings, profile, ...  as it was created. So it may be required to create separated
lockfiles per case. Although there is one more option.
You can update the lockfile. By executing conan with  ``--lock`` argument
when lockfile already exist. It will not be recreated, but updated.


Example of full workflow
------------------------

Let's solve the problem from first paragraph  of this page:

.. code-block:: bash

    $ cd Project_A
    $ conan create . A/1.0@myuser/stable
    $ cd ../Project_XYZ
    $ conan --lock --lockfile important_build.lock install .
    # I ship my project XYZ
    $ cd ../Project_A
    $ conan create . A/1.1@myuser/stable
    $ cd ../Project_XYZ
    $ conan --lockfile important_build.lock install .
    # I can assume that version 1.0 is used.
