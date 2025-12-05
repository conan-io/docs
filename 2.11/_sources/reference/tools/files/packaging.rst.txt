.. _conan_tools_files_packaging:

conan.tools.files AutoPackager
==============================

.. warning::

    This feature is **deprecated**, and will be removed in future Conan 2.X version. 
    It was used to automatically deduce what to ``copy()`` in the ``package()`` method.

    The recommended approach is to use explicit ``copy()`` calls in the ``package()`` method, as explained
    in the rest of the documentation.
