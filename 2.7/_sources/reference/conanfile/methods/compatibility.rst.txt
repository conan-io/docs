.. _reference_conanfile_methods_compatibility:

compatibility()
===============

.. warning::

    This is a **preview** feature


The ``compatibility()`` method implements the same binary compatibility mechanism than the
:ref:`compatibility plugin<reference_extensions_binary_compatibility>`, but at the recipe
level. In general, the global compatibility plugin should be good for most cases, and only
require the recipe method for exceptional cases.

This method can be used in a *conanfile.py* to define packages that are compatible between
each other. If there are no binaries available for the requested settings and options,
this mechanism will retrieve the compatible package's binaries if they exist. This method
should return a list of compatible configurations.

For example, if we want that binaries
built with gcc versions 4.8, 4.7 and 4.6 to be considered compatible with the ones compiled
with 4.9 we could declare a ``compatibility()`` method like this:

..  code-block:: python

    def compatibility(self):
        if self.settings.compiler == "gcc" and self.settings.compiler.version == "4.9":
            return [{"settings": [("compiler.version", v)]}
                    for v in ("4.8", "4.7", "4.6")]

The format of the list returned is as shown below:

..  code-block:: python

        [
            {
                "settings": [(<setting>, <value>), (<setting>, <value>), ...], 
                "options": [(<option>, <value>), (<option>, <value>), ...]
            },
            {
                "settings": [(<setting>, <value>), (<setting>, <value>), ...], 
                "options": [(<option>, <value>), (<option>, <value>), ...]
            },
            ...
        ]


.. seealso::

    Read the :ref:`binary model reference<reference_binary_model>` for a full view of the Conan binary model.
