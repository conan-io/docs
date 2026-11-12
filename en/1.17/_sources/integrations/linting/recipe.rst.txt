Linting the recipe
==================


conanfile.py
------------

The ``conan create`` command verifies the recipe file using pylint.

However, if you have an IDE that supports Python and may do linting automatically,
there are false warnings caused by the fact that Conan dynamically populates some
fields of the recipe based on context.

Conan provides a plugin which makes pylint aware of these dynamic fields and their types.
To use it when running pylint outside Conan, just add the following to your ``.pylintrc`` file:

.. code-block:: ini

    [MASTER]
    load-plugins=conans.pylint_plugin


Custom rules
------------

Using the :ref:`Conan hooks<hooks>` feature you can perform sanity checks to your recipe.

Take a look at the `official hooks repository <https://github.com/conan-io/hooks>`_
to see several examples of how to implement a linter for your recipe.