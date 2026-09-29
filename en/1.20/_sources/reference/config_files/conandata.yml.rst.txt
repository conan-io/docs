.. _conandata_yml:

conandata.yml
=============

This YAML file can be used to in the recipe to declare specific information to be used inside the recipe. This file is specific to each
recipe *conanfile.py* and it should be placed next to it. The file is automatically exported with the recipe (no need to add it to
:ref:`exports_attribute` attribute) and its content is loaded into the :ref:`conandata_attribute` attribute of the recipe.

This file can be used, for example, to declare a list of sources links and checksums for the recipe or a list patches to apply to them, but you can use it to store any data you want to extract from the recipe.
For example:

.. code-block:: YAML

    sources:
      1.70.0:
        url: "https://dl.bintray.com/boostorg/release/1.70.0/source/boost_1_70_0.tar.bz2"
        sha256: "430ae8354789de4fd19ee52f3b1f739e1fba576f0aded0897c3c2bc00fb38778"
      1.71.0:
        url: "https://dl.bintray.com/boostorg/release/1.71.0/source/boost_1_71_0.tar.bz2"
        sha256: "d73a8da01e8bf8c7eda40b4c84915071a8c8a0df4a6734537ddde4a8580524ee"
    patches:
      1.70.0:
        patches: "0001-beast-fix-moved-from-executor.patch,bcp_namespace_issues.patch"
      1.71.0:
        patches: "bcp_namespace_issues.patch,boost_build_qcc_fix_debug_build_parameter.patch"
