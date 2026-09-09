.. _integration_compilers:

Compilers
=========


Conan can work with any compiler, the most common ones are already declared in the default :ref:`settings.yml<settings_yml>`:

- `sun-cc`
- `gcc`
- `Visual Studio`
- `clang`
- `apple-clang`
- `qcc`
- `intel`
- `intel-cc`

.. note ::

    Remember that you can :ref:`customize Conan <extending>` to extend the supported compilers, build systems, etc.


.. important::

    If you work with a compiler like ``intel`` that uses ``Visual Studio`` in Windows environments
    and ``gcc`` in Linux environments and you are wondering how to manage the compatibility between the packages generated
    with ``intel`` and the generated with the pure base compiler (``gcc`` or ``Visual Studio``) check the
    :ref:`Compatible Packages<compatible_packages>` and :ref:`Compatible Compilers<compatible_compilers>` sections.

.. important::

    If you are working with the new Intel oneAPI compilers, then you should use ``intel-cc`` one and have a look at :ref:`Working with Intel compilers<howto_intel_compiler>` section.
