
.. _examples_dev_flow_debug_visual:


Debugging shared libraries with Visual Studio
=============================================

Conan packages don't contain the necessary information for debugging libraries with Visual Studio by default.
This information is stored in PDBs that are generated during the compilation of the libraries. When using Conan these
PDBs are generated in the build folder, which isn't always available, making impossible to debug the dependencies.

The goal is to have the necessary PDB files in the package folder, so that Visual is able to debug through the
dependencies of a project. To solve this we created a hook that copies the PDBs created in the build folder to the
package folder. This behavior can't be forced by default because PDB files are usually larger than the whole package,
and it would greatly increase the package sizes.


PDBs and how to locate them
---------------------------

A PDB has the information to link the source code of a debuggable object to the Visual Studio debugger. Each PDB is linked to a
specific file (executable or library) and contains the source file name and line numbers to display in the IDE.
When compiling the files in Debug mode the created binary will contain the information of where the PDB will be
generated, which by default is the same path where the file is being compiled. The PDBs are created by the ``cl.exe``
compiler with the ``/Zi`` flag, or by the ``link.exe`` when linking a DLL or executable.

.. note::

    PDBs can sometimes be generated for LIB files, for now we will focus only on shared libraries and work with
    PDBs generated for DLLs.

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

With the information above we developed a hook that will look through all the DLLs in the package folder and get the
location of where its PDB was generated. To do this we used the ``dumpbin`` tool which is provided with Visual Studio
and can be located for each user through the ``vswhere`` tool. Using ``dumpbin \PDBPATH`` with a DLL as parameter
we can get the name and path of the PDB which contains the debug information for that DLL. The hook will do this for
every DLL in the package and then copy the PDB next to its PDB so Visual can find and load it.

The hook is implemented as a post-package hook, which will execute after the package is created through the
``package()`` method of a recipe.

The hook is available in the `conan-extensions repository <https://github.com/conan-io/conan-extensions>`_. Running
``conan config install https://github.com/conan-io/conan-extensions.git```will install all the available extensions,
including this hook. To install the hook independently (complete).
The hook will not work by default, it needs to be renamed so that it starts with ``hook_`` as it's explained in
the :ref:`hooks documentation <reference_extensions_hooks>`.
