Linting the recipe
==================

IDE
---
If you have an IDE that supports Python and may do linting automatically,
there are false warnings caused by the fact that Conan dynamically populates some
fields of the recipe based on context.

Conan provides a plugin which makes pylint aware of these dynamic fields and their types.
To use it when running pylint outside Conan, just add the following to your ``.pylintrc`` file:

.. code-block:: ini

    [MASTER]
    load-plugins=conans.pylint_plugin


Hook
----

There is also a "recipe_linter" hook in the `official hooks repository <https://github.com/conan-io/hooks>`_ 
that can be activated to run automatic linter checks on the recipes when they are exported to the conan
cache (``export``, ``create`` and ``export-pkg`` commands). Read the hook documentation for details.
You could also write your own custom linter hook to provide your own recipe quality checks.
