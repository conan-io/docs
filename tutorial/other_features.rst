.. _other_important_features:

Other important Conan features
==============================

python_requires
---------------

It is possible to reuse code from other recipes using the :ref:`python_requires feature<reference_extensions_python_requires>`.

If you maintain many recipes for different packages that share some common logic and you don't want to repeat the code in every recipe, you can put that common code in a Conan ``conanfile.py``, upload it to your server, and have other recipe conanfiles do a ``python_requires = "mypythoncode/version"`` to depend on it and reuse it.

Packages lists
--------------

It is possible to manage a list of packages, recipes and binaries together with the "packages-list" feature. 
Several commands like ``upload``, ``download``, and ``remove`` allow receiving a list of packages file as an input, and they can do their operations over that list.
A typical use case is to "upload to the server the packages that have been built in the last ``conan create``", which can be done with:

.. code:: bash

    $ conan create . --format=json > build.json
    $ conan list --graph=build.json --graph-binaries=build --format=json > pkglist.json
    $ conan upload --list=pkglist.json -r=myremote -c

See the :ref:`examples in this section<examples_commands_pkglists>`.
