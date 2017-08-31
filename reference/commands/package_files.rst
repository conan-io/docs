.. _conan_package_files_command:

conan package_files
===================

.. code-block:: bash

	$  conan package_files [-h] [--package_folder PACKAGE_FOLDER]
                           [--source_folder SOURCE_FOLDER]
                           [--build_folder BUILD_FOLDER] [--profile PROFILE]
                           [--options OPTIONS] [--settings SETTINGS] [-f]
                           reference


Creates a package binary from given precompiled artifacts in user folder,      
skipping the package recipe build() method. If source_folder or build_folder   
is specified, then it will call the package() method to extract the artifacts. 
If source_folder nor build_folder is not specified, then it will run an exact  
copy of the package, as they are layout in the given folder, without running   
or even requiring to define a package() method.                                

.. code-block:: bash

    positional arguments:                                                          
    reference             package recipe reference e.g.,                         
                            MyPackage/1.2@user/channel                             
                                                                                
    optional arguments:                                                            
    -h, --help            show this help message and exit                        
    --package_folder PACKAGE_FOLDER, -pf PACKAGE_FOLDER                          
                            Get binaries from this path, relative to current or    
                            absolute                                               
    --source_folder SOURCE_FOLDER, -sf SOURCE_FOLDER                             
                            Get artifacts from this path, relative to current or   
                            absolute. If specified, artifacts will be              
                            extracted/copied calling the package() method          
    --build_folder BUILD_FOLDER, -bf BUILD_FOLDER                                
                            Get artifacts from this path, relative to current or   
                            absolute If specified, artifacts will be               
                            extracted/copied calling the package() method          
    --profile PROFILE, -pr PROFILE                                               
                            Profile for this package                               
    --options OPTIONS, -o OPTIONS                                                
                            Options for this package. e.g., -o with_qt=true        
    --settings SETTINGS, -s SETTINGS                                             
                            Settings for this package e.g., -s compiler=gcc        
    -f, --force           Overwrite existing package if existing
                                                                               


Note that this is **not** the normal or recommended flow for creating conan packages, as packages created this way will not have a reproducible build from sources. This command is intended only when it is not possible to build the packages from sources.

To create packages this way, a recipe must already exist for it in the local cache. Typically this recipe will be simple, without ``build()`` and ``package()`` methods, though the ``package_info()`` method is still necessary to be able to automatically provide information for consumers. The command ``conan new <ref> --bare`` will create a simple recipe that could be used in combination with the ``package_files`` command. Check this :ref:`How to package existing binaries <existing_binaries>`.

This command will use the ``package()`` method or not, depending on arguments:

- If ``source_folder`` or ``build_folder``, or both arguments are given, it will understand that a final package is not available, and artifacts have to be extracted from source and build folders. In this case, the conanfile.py ``package()`` method will be used over those folders, to extract the artifacts and define the final layout of the package, which will be directly stored in conan cache

- If ``source_folder``, ``build_folder`` are not given, it will assume that there is already a final package available, with the final and correct layout. This can be defined by the user build, or maybe it is a local package created with the ``conan package`` command. In this case, the copy will be direct, the ``package()`` method will not be used, and the package layout from user folder will be copied as-is to the conan cache.


**Examples**:

- Create a package from a directory containing the binaries for Windows/x86/Release:

Having these files:

.. code-block:: text

    Release_x86/lib/libmycoollib.a
    Release_x86/lib/other.a
    Release_x86/include/mylib.h
    Release_x86/include/other.h

Run:

.. code-block:: bash

    $ conan package_files Hello/0.1@user/stable -s os=Windows -s arch=x86 -s build_type=Release --package_folder=Release_x86


- Create a package from a user folder build and sources folders:

Given this files in the current folder
.. code-block:: text

    sources/include/mylib.h
    sources/src/file.cpp
    build/lib/mylib.lib
    build/lib/mylib.tmp
    build/file.obj

And assuming the ``Hello/0.1@user/stable`` recipe has a ``package()`` method like this:

.. code-block:: python

    def package(self):
        self.copy("*.h", dst="include", src="include")
        self.copy("*.lib", dst="lib", keep_path=False)

Then, the following code will create a package in the conan local cache:

.. code-block:: bash

    $ conan package_files Hello/0.1@user/stable -pr=myprofile --source_folder=sources --build_folder=build

And such package will contain just the files:

.. code-block:: text

    include/mylib.h
    lib/mylib.lib
