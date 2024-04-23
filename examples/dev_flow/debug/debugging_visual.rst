
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
generated, which by default is the same path where the file is being compiled. The PDBs are created by the ``cl.exe``
compiler with the ``/Zi`` flag, or by the ```link.exe`` when linking a DLL or executable.

.. note::

    PDBs can sometimes be generated for LIB files, for now we will focus only on shared libraries and  work with
    PDBs generated for DLLs.


Locating PDBs
-------------

PDBs are created when compiling a library or executable in Debug mode. They are created by default in the same directory
as the file it is associated with. This means that when using Conan they will be created in the build directory in the
same path as the DLLS.

When using the Visual Studio debugger, it will look for PDBs to load in the following paths:

- The project folder.
- The original path where the associated file was compiled.
- The path where Visual is currently finding the compiled file, in our case the DLL in the package folder.

The PDB has by default the same name as its associated file, so Visual will look for it based on the name of the DLL.


Making the PDBs available for Visual Studio
-------------------------------------------

To make sure that Visual Studio finds the PDBs we created a hook that adds the necessary PDBs to the package folder.
This behavior can't be the default one because PDB files are usually larger than the whole package, which greatly
increases the package sizes.

The hook is implemented as a post-package hook, which will execute after the ``package()`` method of a recipe.
It will find the PDB in the build folder and copy it to the path where the corresponding DLL is located.

For now we will do this only for shared libraries.

To find all the PDBs necessary, the hook will look through all the DLLs in the package folder and find the path where the
PDB was generated using the ``dumpbin \PDBPATH`` command. Then it will copy each PDB to the path where the
corresponding DLL is found.

This hook is located in the `conan-extensions repository <https://github.com/conan-io/conan-extensions>`_.
To use the hook is necessary to install it as explained and then rename it to ``hook_`` as explained
`here <https://docs.conan.io/2/reference/extensions/hooks.html#storage-activation-and-sharing>`_ (link to hooks naming).



