.. _qmake:


QMake
_____

A qmake generator will generate a ``conanbuildinfo.pri`` file that can be used for your qmake builds.
Add ``conan_basic_setup`` to ``CONFIG`` and include the file in your existing ``.pro`` file:

**yourproject.pro**

.. code-block:: text

   # ...
   
   CONFIG += conan_basic_setup
   include(conanbuildinfo.pri)

This will include all the statements in ``conanbuildinfo.pri`` in your 
project.
Include paths, libraries, defines, etc. will be set up for all requirements
you have defined in ``conanfile.txt``.

If you'd rather like to manually add the variables for each dependency,
you can do so by skipping the CONFIG statement and only include 
``conanbuildinfo.pri``:

**yourproject.pro**

.. code-block:: text

   # ...
   
   include(conanbuildinfo.pri)
   
   # you may now modify your variables manually for each library, such as
   # INCLUDEPATH += CONAN_INCLUDEPATH_POCO


.. seealso:: Check the :ref:`Reference/Generators/qmake <qmake_generator>` for the complete reference.

