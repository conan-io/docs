.. _developing_packages:

Developing packages locally
===========================

As we learned in :ref:`previous sections <tutorial_creating_packages>` in the tutorial,
the most straightforward way of working when developing a Conan package is to run a
:command:`conan create`. This means that everytime it is run, Conan performs the a series
of costly operations in the Conan cache like downloading, decompressing and copying
sources and also building the entire library from scratch, etc. Sometimes sometimes,
especially with big libraries, while we are developing the recipe, we cannot afford to
perform these operations every time.

This section will first show the **Conan local developement flow**, that is to say, working
on packages in your local project directory, without having to export the contents of the
package to the Conan cache first.

We will also cover how you other packages can consume those packages under developement
using the **editable mode**.

Finally we will explain the **Conan package layouts** in depth, that is the key feature that
makes possible working with Conan packages in the Conan cache or locally without having to
do any changes.

.. toctree::
   :maxdepth: 1

   developing_packages/local_package_developement_flow
   developing_packages/editable_packages
   developing_packages/package_layout
