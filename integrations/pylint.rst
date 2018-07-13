.. _pylint_integration:

Linting conanfile.py
====================

``conan create`` command verifies the recipe file using pylint.

However if you have IDE which has support for Python and may do linting automatically,
there are false warnings caused by the fact that Conan populates some
fields of recipe dynamically based on context.

Conan provides a plugin which makes pylint aware of these dynamic fields and their types.
To using it when running pylint outside Conan just add to your ``.pylintrc`` file:

.. code-block:: ini

    [MASTER]
    load-plugins=conans.pylint_plugin

