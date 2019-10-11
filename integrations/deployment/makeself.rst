.. _deployment_makeself:

Makeself
--------

`Makeself <https://makeself.io>`_ is a small command-line utility to generate self-extracting archives for Unix. It is pretty popular and it
is used by `VirtualBox <https://www.virtualbox.org/wiki/Linux_Downloads>`_ and `CMake <https://cmake.org/download/>`_ projects.

Makeself creates archives that are just small startup scripts (*.run*, *.bin* or *.sh*) concatenated with tarballs.

When you run such self-extracting archive:

- A small script (shim) extracts the embedded archive into the temporary directory
- Script passes the execution to the entry point within the unpacked archive
- application is being run
- The temporary directory removed

Therefore, it transparently appears just like a normal application execution. 
Check out the `guide <http://xmodulo.com/how-to-create-a-self-extracting-archive-or-installer-in-linux.html>`_ on how to make
self-extracting archive with Makeself.

With help of :ref:`deploy generator <deployable_deploy_generator>`, it's only needed to invoke ``makeself.sh`` in order to generate 
self-extracting archive for the further deployment.
