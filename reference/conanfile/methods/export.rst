.. _reference_conanfile_methods_export:

export()
========



.. note::

    **Best practices**

    The recipe files must be configuration independent. Those files are common for all configurations,
    then, it is not possible to do conditional ``export()`` to different settings, options, or
    platforms. Do not try to do any kind of conditional export. If necessary export all the files necessary for 
    all configurations at once.
