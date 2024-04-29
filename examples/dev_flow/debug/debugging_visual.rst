.. _examples_dev_flow_debug_visual:


Debugging shared libraries with Visual Studio
=============================================

We previously discussed how to debug dependencies in Visual Studio, but when using Conan to create your project is
possible that the original build folder and build files don't exist. Conan packages don't contain the necessary
information for debugging libraries with Visual Studio by default, this information is stored in PDBs that are generated during the
compilation of the libraries. When using Conan these PDBs are generated in the build folder, which is generated during
the building of the libraries and it's no longer needed afterwards. A case where the build
folder won't be available is when cleaning the cache with ``conan cache clean``.

The goal is to store the necessary PDB files in the package folder to make sure they are always present and don't depend on the
existence of the build folder. To solve this we created a hook that copies the PDBs created in the build folder to the
package folder. This behavior can't be forced by default because PDB files are usually larger than the whole package,
and it would greatly increase the package sizes.


PDBs and how to locate them
---------------------------

A PDB has the information to link the source code of a debuggable object to the Visual Studio debugger. Each PDB is linked to a
specific file (executable or library) and contains the source file name and line numbers to display in the IDE.
When compiling the files in Debug mode the created binary will contain the information of where the PDB will be
generated, which by default is the same path where the file is being compiled. The PDBs are created by the ``cl.exe``
compiler with the ``/Zi`` flag, or by the ``link.exe`` when linking a DLL or executable.

When a DLL is created it contains the information of the path where its corresponding PDB was generated. This can be
manually checked by running the following commands:

  .. code-block:: text

      $ "%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" -find "**\dumpbin.exe"
      C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.16.27023\bin\HostX64\x64\dumpbin.exe

      $ C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.16.27023\bin\HostX64\x64\dumpbin.exe /PDBPATH {dll_path}
      [..]
      Dump of file .\bin\zlib1.dll

      File Type: DLL
        PDB file found at 'C:\Users\{user}\.conan2\p\b\zlib78326f0099328\p\bin\zlib1.pdb'
      [...]

First we locate the ``dumpbin.exe`` path with the ``vswhere`` tool and then we run the command passing a DLL path,
which will return the information of the PDB path. In this case we used a relative path to DLL from the build folder,
but it can be a full path.


PDBs are created when compiling a library or executable in Debug mode. They are created by default in the same directory
as the file it is associated with. This means that when using Conan they will be created in the build directory in the
same path as the DLLS.

When using the Visual Studio debugger, it will look for PDBs to load in the following paths:

- The project folder.
- The original path where the associated file was compiled.
- The path where Visual is currently finding the compiled file, in our case the DLL in the package folder.

The PDB has by default the same name as its associated file, so Visual will look for it based on the name of the DLL.

.. note::

    PDBs can sometimes be generated for LIB files, for now we will focus only on shared libraries and work with
    PDBs generated for DLLs.


Post-package hook for copying PDBs to package folder
----------------------------------------------------

After knowing what is our problem and how Visual uses PDBs we can now explain how we used the conan hooks to solve it.
We developed a hook that will look through all the DLLs in the package folder and get the
location of where its PDB was generated inside the build folder in the conan cache.

As explained above we used the ``dumpbin`` tool which is provided with Visual Studio and can be located for each user
through the ``vswhere`` tool. Using ``dumpbin \PDBPATH`` with a DLL as parameter
we can get the name and path of the PDB which contains the debug information for that DLL. The hook will do this for
every DLL in the package and then copy the PDB next to its PDB so Visual can find and load it.

The hook is implemented as a post-package hook, which means that it will execute after the package is created through the
``package()`` method of a recipe. This avoids any potential issue, as the order will be as follows:

- The ``build()`` method of the recipe is executed, generating the DLLs and PDBs
- The ``package()`` method of the recipe is executed, copying the necessary files to the package folder (in this case the DLLs but not the PDBs)
- The hook is executed copying the PDBs from the build folder next to its DLL for every DLL in the package

The hook is available in the `conan-extensions repository <https://github.com/conan-io/conan-extensions>`_.
Installing the whole repo will work, but we recommend to only install the hooks folder from the conan-extensions repo with:

  .. code-block:: text

      $ conan config install https://github.com/conan-io/conan-extensions.git -sf=extensions/hooks -tf=extensions/hooks

The hook will not work by default, it needs to be renamed so that it starts with ``hook_`` as it's explained in
the :ref:`hooks documentation <reference_extensions_hooks>`. To locate the hook run ``conan config home`` to locate
your local cache path and go to the ``extensions/hooks`` folder to find the ``_hook_copy_pdbs_to_package.py`` and rename it.
