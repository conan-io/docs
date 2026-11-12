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
self-extracting archive for the further deployment:

.. code-block:: console

    TMPDIR=`dirname $(mktemp -u -t tmp.XXXXXXXXXX)`
    curl "https://github.com/megastep/makeself/releases/download/release-2.4.0/makeself-2.4.0.run" --output $TMPDIR/makeself.run -L
    chmod +x $TMPDIR/makeself.run
    $TMPDIR/makeself.run --target $TMPDIR/makeself
    $TMPDIR/makeself/makeself.sh $PREFIX md5.run "conan-generated makeself.sh" "./conan-entrypoint.sh"

The ``PREFIX`` variable in the example points to the directory where binary artifacts are situated. The ``md5.run`` is an output SFX archive:

.. code-block:: console

    $ file md5.run
    md5.run: POSIX shell script executable (binary data)

The ``conan-entry-point.sh`` is a simple script which sets requires variables (like ``PATH`` or ``LD_LIBRARY_PATH``):

.. code-block:: bash

    #!/usr/bin/env bash
    set -ex
    export PATH=$PATH:$PWD/bin
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PWD/lib
    pushd $(dirname $PWD/md5)
    $(basename $PWD/md5)
    popd

Check out the complete example on `GitHub <https://github.com/conan-io/examples/tree/master/features>`_.
