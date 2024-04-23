
.. _examples_dev_flow_debug_visual:


Debugging shared libraries with Visual Studio
=============================================

Libraries can’t always be debugged with Visual Studio when installing them through Conan as shared libraries. When a
Conan recipe is compiled with msvc with a Debug configuration it creates symbol files or PDBs that contain the debug
information necessary for Visual Studio for each library.
These files are generated in the original build folder where the library was compiled, so cleaning the cache or sharing
the recipe package will cause the debug information to be missing.


PDBs
----

A PDB has the information to link the source code of a debuggable object to the Visual Studio debugger. Each PDB is linked to a
specific file (executable or library) and contains the source file name and line numbers to display in the IDE.
When compiling the files in Debug mode the created binary will contain the information of where the PDB will be
generated, which by default is the same path where the file is being compiled.

.. note::

    - PDBs can sometimes be generated for LIB files, but in this case we want the debugger to work for shared
libraries so we will only use those generated for DLLs.


Where are PDBs located?
-----------------------

PDBs are created when compiling a library or executable in Debug mode. They are created by default in the same directory
as the file it is associated with. This means that when using Conan they will be created in the build directory.

Visual Studio will try to load PDB files from the following paths:
- The project folder.
- The original path where the associated file was compiled.
- The path where Visual is currently finding the compiled file.

The PDB has by default the same name as its associated file, so Visual will look for it based on the name of the file.


Solution
--------

As a solution for this we created a hook that adds the necessary PDBs to the package folder. This can’t be the default behavior because PDB files are usually larger than the whole package, which will increase the package size too much.

The hook is implemented as a post-package hook, which will execute after the package() method of a recipe. It will find the PDB in the build folder and copy it to the path where the corresponding DLL is located.

This solution is based on two assumptions:
We only need the PDBs of DLLs for Visual to be able to debug.
The PDBs will have the same name as the DLL they are associated with.

To find all the PDBs necessary the hook will look through all the DLLs in the package folder and find the path where the PDB was generated through the dumpbin tool (with /pdbpath). Then it will copy those PDBs to the same path where the corresponding DLL is found.

This hook is located in the conan-extensions repository (link to the docu page). By default is not active, to use it, it should be renamed to "hook _" (link to hooks naming).


Example of where the .pdb is moved to in zlib?