.. _qmake:


QMake
_____

From 0.5 there is a qmake generator available that can be used as:

**conanfile.txt**

.. code-block:: text

   ...
   
   [generators]
   qmake
   
It will generate a ``conanbuildinfo.pri`` file that could be used for your qmake builds.



