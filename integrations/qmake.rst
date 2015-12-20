.. _qmake:


QMake
_____

As of version 0.5 of conan, a qmake generator is available that can be configured as follows:

**conanfile.txt**

.. code-block:: text

   ...
   
   [generators]
   qmake
   
It will generate a ``conanbuildinfo.pri`` file that can be used for your qmake builds.



