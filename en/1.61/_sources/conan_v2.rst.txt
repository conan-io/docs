.. _conan2_migration_guide:


Conan migration guide to 2.0
============================

.. tip::

    Conan 2.0 `is already released <https://pypi.org/project/conan/#history>`_, you can
    install the latest Conan version from PyPI doing:

        .. code-block:: bash

            $ pip install conan


If you want to migrate to 2.0, there are several things you will need to change:

  - The **recipes** have to be updated to be compatible with Conan 2.0. There are 2.0
    features ported to Conan 1.X so you can get a compatible recipe with 2.0 using Conan
    1.X. Please be aware that although the recipes can be compatible between Conan 1.X and
    2.0, the generated Conan binary packages won't be compatible between versions.
  - The **conan commands** have also changed, but there are no "compatible" commands introduced in Conan 1.X. We will review
    the more relevant changes.
  - **General changes** not related to the recipes nor the Conan commands, "build profiles", lowercase references... etc.


.. note::

    There are already lots of recipes prepared for v2, some of them with generated binaries, in `ConanCenter <https://conan.io/center>`_,
    follow the `Conan 2.0 and ConanCenter Support thread <https://conan.io/cci-v2.html>`_ for more information.

.. toctree::
   :maxdepth: 2

   migrating_to_2.0/recipes
   migrating_to_2.0/properties
   migrating_to_2.0/commands
   migrating_to_2.0/general
   migrating_to_2.0/config_files
