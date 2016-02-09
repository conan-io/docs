.. _qbs:


Qt Build System (qbs)
_____________________

As of version 0.7 of conan, a Qt Build System (qbs) generator is available
that can be configured as follows:

**conanfile.txt**

.. code-block:: text

   ...
   
   [generators]
   qbs
   
It will generate a ``conanbuildinfo.qbs`` file that can be used for your 
qbs builds.
Add ``conanbuildinfo.qbs`` as a reference on the project level and a Depends
item with the name ``conanbuildinfo``:

**yourproject.qbs**

.. code-block:: qbs

   import qbs

   Project {
      references: ["conanbuildinfo.qbs"]
      Product {
           type: "application"
           consoleApplication: true
           files: [
               "conanfile.txt",
               "main.cpp",
           ]
           Depends { name: "cpp" }
           Depends { name: "ConanBasicSetup" }
      }
   }

This will include the product called ``ConanBasicSetup`` which holds all
the necessary settings for all your dependencies.

If you'd rather like to manually add each dependency, just replace 
``ConanBasicSetup`` with the dependency you would like to include.
You may also specify multiple dependencies:

**yourproject.qbs**

.. code-block:: qbs

   import qbs

   Project {
      references: ["conanbuildinfo.qbs"]
      Product {
           type: "application"
           consoleApplication: true
           files: [
               "conanfile.txt",
               "main.cpp",
           ]
           Depends { name: "cpp" }
           Depends { name: "catch" }
           Depends { name: "Poco" }
      }
   }


The contents of ``conanbuildinfo.qbs`` could look like this:

**conanbuildinfo.qbs**

.. code-block:: qbs

   import qbs 1.0

   Project {
      Product {
           name: "ConanBasicSetup"
           Export {
               Depends { name: "cpp" }
               cpp.includePaths: ["/home/username/.conan/data/hellopackage/0.1/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/include",
                   "/home/username/.conan/data/Catch/1.3.2/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/include"]
               cpp.libraryPaths: ["/home/username/.conan/data/hellopackage/0.1/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/lib",
                   "/home/username/.conan/data/Catch/1.3.2/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/lib"]
               cpp.systemIncludePaths: ["/home/username/.conan/data/hellopackage/0.1/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/bin",
                   "/home/username/.conan/data/Catch/1.3.2/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/bin"]
               cpp.dynamicLibraries: ["hellopackage"]
               cpp.defines: []
               cpp.cppFlags: []
               cpp.cFlags: []
               cpp.linkerFlags: []
           }
      }

      Product {
           name: "Catch"
           Export {
               Depends { name: "cpp" }
               cpp.includePaths: ["/home/username/.conan/data/Catch/1.3.2/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/include"]
               cpp.libraryPaths: ["/home/username/.conan/data/Catch/1.3.2/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/lib"]
               cpp.systemIncludePaths: ["/home/username/.conan/data/Catch/1.3.2/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/bin"]
               cpp.dynamicLibraries: []
               cpp.defines: []
               cpp.cppFlags: []
               cpp.cFlags: []
               cpp.linkerFlags: []
           }
      }
      // Catch root path: /home/username/.conan/data/Catch/1.3.2/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed

      Product {
           name: "hellopackage"
           Export {
               Depends { name: "cpp" }
               cpp.includePaths: ["/home/username/.conan/data/hellopackage/0.1/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/include"]
               cpp.libraryPaths: ["/home/username/.conan/data/hellopackage/0.1/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/lib"]
               cpp.systemIncludePaths: ["/home/username/.conan/data/hellopackage/0.1/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed/bin"]
               cpp.dynamicLibraries: ["hellopackage"]
               cpp.defines: []
               cpp.cppFlags: []
               cpp.cFlags: []
               cpp.linkerFlags: []
           }
      }
      // hellopackage root path: /home/username/.conan/data/hellopackage/0.1/maintainer/master/package/0692fb2bd888ba708ca65670557c56d2e16851ed
   }
