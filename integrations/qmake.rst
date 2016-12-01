.. _qmake:


QMake
_____

As of version 0.5 of conan, a qmake generator is available that can be 
configured as follows:

**conanfile.txt**

.. code-block:: text

   ...
   
   [generators]
   qmake
   
It will generate a ``conanbuildinfo.pri`` file that can be used for your 
qmake builds.
Add ``conan_basic_setup`` to ``CONFIG`` and include the file in your existing 
.pro file:

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


The contents of ``conanbuildinfo.pri`` could look like this:

**conanfile.pri**

.. code-block:: text

   CONAN_INCLUDEPATH += /home/username/.conan/data/Catch/1.3.2/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/include \
       /home/username/.conan/data/hellolibrary/0.1/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/include
   CONAN_LIBS += -L/home/username/.conan/data/Catch/1.3.2/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/lib \
       -L/home/username/.conan/data/hellolibrary/0.1/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/lib
   CONAN_BINDIRS += /home/username/.conan/data/Catch/1.3.2/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/bin \
       /home/username/.conan/data/hellolibrary/0.1/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/bin
   CONAN_LIBS += -lhellolibrary
   CONAN_DEFINES += 
   CONAN_QMAKE_CXXFLAGS += 
   CONAN_QMAKE_CFLAGS += 
   CONAN_QMAKE_LFLAGS += 
   CONAN_QMAKE_LFLAGS += 

   CONAN_INCLUDEPATH_CATCH += /home/username/.conan/data/Catch/1.3.2/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/include
   CONAN_LIBS_CATCH += -L/home/username/.conan/data/Catch/1.3.2/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/lib
   CONAN_BINDIRS_CATCH += /home/username/.conan/data/Catch/1.3.2/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/bin
   CONAN_LIBS_CATCH += 
   CONAN_DEFINES_CATCH += 
   CONAN_QMAKE_CXXFLAGS_CATCH += 
   CONAN_QMAKE_CFLAGS_CATCH += 
   CONAN_QMAKE_LFLAGS_CATCH += 
   CONAN_QMAKE_LFLAGS_CATCH += 
   CONAN_CATCH_ROOT = /home/username/.conan/data/Catch/1.3.2/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed

   CONAN_INCLUDEPATH_HELLOLIBRARY += /home/username/.conan/data/hellolibrary/0.1/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/include
   CONAN_LIBS_HELLOLIBRARY += -L/home/username/.conan/data/hellolibrary/0.1/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/lib
   CONAN_BINDIRS_HELLOLIBRARY += /home/username/.conan/data/hellolibrary/0.1/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/bin
   CONAN_LIBS_HELLOLIBRARY += -lhellolibrary
   CONAN_DEFINES_HELLOLIBRARY += 
   CONAN_QMAKE_CXXFLAGS_HELLOLIBRARY += 
   CONAN_QMAKE_CFLAGS_HELLOLIBRARY += 
   CONAN_QMAKE_LFLAGS_HELLOLIBRARY += 
   CONAN_QMAKE_LFLAGS_HELLOLIBRARY += 
   CONAN_HELLOLIBRARY_ROOT = /home/username/.conan/data/hellolibrary/0.1/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed

   CONFIG(conan_basic_setup) {
       INCLUDEPATH += $$CONAN_INCLUDEPATH
       LIBS += $$CONAN_LIBS
       BINDIRS += $$CONAN_BINDIRS
       LIBS += $$CONAN_LIBS
       DEFINES += $$CONAN_DEFINES
       QMAKE_CXXFLAGS += $$CONAN_QMAKE_CXXFLAGS
       QMAKE_CFLAGS += $$CONAN_QMAKE_CFLAGS
       QMAKE_LFLAGS += $$CONAN_QMAKE_LFLAGS
   }

Note that both ``CONAN_INCLUDEPATH`` and dependency specific variables such as
``CONAN_INCLUDEPATH_POCO`` are defined so that you may choose to include all or
only some include paths for your requirements.
