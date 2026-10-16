conan export
============

.. autocommand::
    :command: conan export -h


The ``conan export`` command exports the recipe specified in ``path`` to the Conan package cache.


Output Formats
--------------

The :command:`conan export` command accepts two types of formats for the ``--format`` argument:

* ``json``: Creates a JSON file containing the information of the exported recipe reference.
* ``pkglist``: Generates a JSON file in the :ref:`pkglist<other_important_features_pkglist>`
  format, which can be utilized as input for various commands such as :command:`upload`,
  :command:`download`, and :command:`remove`.
