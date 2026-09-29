.. _manage_shared:

How to manage shared libraries
==============================

The shared libraries, `.DLL` in windows, `.dylib` in OSX and `.so` in Linux, are loaded at runtime,
that means that the application executable needs to know where are the required shared libraries when
it runs.

On Windows, the dynamic linker, will search in the same directory then in the `PATH` directories.
On OSX, it will search in the directories declared in `DYLD_LIBRARY_PATH` as on Linux will use the `LD_LIBRARY_PATH`.

Furthermore in OSX and Linux there is another mechanism to locate the shared libraries: The RPATHs.

.. toctree::
   :maxdepth: 2

   manage_shared_libraries/env_vars
   manage_shared_libraries/rpaths
