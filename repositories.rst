Repositories
============

Official repositories
---------------------

These repositories are maintained by the Conan team and are shipped with it by
default.

**conan-center**: https://bintray.com/conan/conan-center

.. pull-quote::

    Contains trusted packages and is curated by the Conan team. This repository
    is the place where you can share your packages with the community. Check the
    :ref:`conan-center guide<conan_center_flow>` for more information.

**conan-transit**: https://bintray.com/conan/conan-transit

.. pull-quote::

    Contains the legacy packages left over from before the move to Bintray. This
    repository only exists for backwards compatibility and the packages there
    **will never be updated**.


Third-party repositories
------------------------

These are popular third-party repositories which are not affiliated with the
Conan team.

**bincrafters**: https://bintray.com/bincrafters/public-conan

.. pull-quote::

    The `Bincrafters <https://bincrafters.github.io>`_ team builds binary
    software packages for the OSS community.

    Use the following command to add *bincrafters* to Conan:

    ::

        $ conan remote add bincrafters https://api.bintray.com/conan/bincrafters/public-conan

Repository management
---------------------

See the :ref:`"conan remote" command reference<remote_command>` for information
on how to add, remove and list remote repositories. Also see the
:ref:`"conan search" command reference<search_command>` for information on how
to find packages in remote repositories or the local cache.
