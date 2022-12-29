.. _conan2_migration_guide:


Conan migration guide to 2.0
============================

Conan 2.0-beta `is already released <https://pypi.org/project/conan/#history>`_, you can install the latest Conan Alpha
version from PyPI doing:

    .. code-block:: bash

        $ pip install conan --pre


If you want to migrate to 2.0, there are several things you will need to change:

  - The **recipes** have to be updated to be compatible with Conan 2.0. There are 2.0 features ported to Conan 1.X
    so you can get a compatible recipe with 2.0 using Conan 1.X.
  - The **conan commands** have also changed, but there are no "compatible" commands introduced in Conan 1.X. We will review
    the more relevant changes.
  - **General changes** not related to the recipes nor the Conan commands, "build profiles", lowercase references... etc.

If you are looking for precompiled binaries, there is a very short list in a separate remote which can be added (please, check the `Conan 2.0 documentation <https://docs.conan.io/en/2.0/index.html>`_ for more information)

    .. code-block:: bash

      $ conan remote add conanv2 https://conanv2beta.jfrog.io/artifactory/api/conan/conan --index 0

.. toctree::
   :maxdepth: 2

   migrating_to_2.0/recipes
   migrating_to_2.0/properties
   migrating_to_2.0/commands
   migrating_to_2.0/general
