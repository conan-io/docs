.. _developing_packages:

Developing packages locally
===========================

As we learned in :ref:`previous sections <tutorial_creating_packages>` of the tutorial,
the most straightforward way to work when developing a Conan package is to run a
:command:`conan create`. This means that every time it is run, Conan performs a series of
costly operations in the Conan cache, such as downloading, decompressing, copying sources,
and building the entire library from scratch. Sometimes, especially with large libraries,
while we are developing the recipe, these operations cannot be performed every time.

This section will first show the **Conan local development flow**, that is, working on
packages in your local project directory without having to export the contents of the
package to the Conan cache first.

We will also cover how other packages can consume packages under development using the
**editable mode**.

Finally, we will explain the **Conan package layouts** in depth, the key feature that
makes it possible to work with Conan packages in the Conan cache or locally without making
any changes.

.. toctree::
   :maxdepth: 1

   developing_packages/local_package_development_flow
   developing_packages/editable_packages
   developing_packages/package_layout
