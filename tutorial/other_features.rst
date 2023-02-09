.. _other_important_features:

Other important Conan features
==============================

python_requires
---------------

It is possible to reuse code from other recipes using the :ref:`python_requires feature<reference_extensions_python_requires>`.

If you maintain many recipes for different packages that share some common logic and you don't want to repeat the code in every recipe, you can put that common code in a Conan ``conanfile.py``, upload it to your server, and have other recipe conanfiles do a ``python_requires = "mypythoncode/version"`` to depend on it and reuse it.
