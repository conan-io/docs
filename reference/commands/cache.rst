.. _reference_commands_cache:

conan cache
===========

conan cache path
----------------

.. code-block:: bash

    $ conan cache path -h
    usage: conan cache path [-h] [-v [V]] [--logger]
                            [--folder {export_source,source,build}]
                            reference

    Shows the path in the Conan cache af a given reference

    positional arguments:
    reference             Recipe reference or Package reference

    optional arguments:
    -h, --help            show this help message and exit
    -v [V]                Level of detail of the output. Valid options from less verbose to more
                            verbose: -vquiet, -verror, -vwarning, -vnotice, -vstatus, -v or
                            -vverbose, -vv or -vdebug, -vvv or -vtrace
    --logger              Show the output with log format, with time, type and message.
    --folder {exports,exports_sources,sources,build,package}
                            Show the path to the specified element. The 'build' and 'package'
                            requires a package reference. If not specified it shows 'exports' path


The ``conan cache path`` returns the path in the cache of a given reference. Depending on the reference, it
could return the path of a recipe, or the path to a package binary. 

Let's say that we have created a package in our current cache with:

.. code-block:: bash
    
    $ conan new cmake_lib -d name=pkg -d version=0.1
    $ conan create .
    ...
    Requirements
        pkg/0.1#cdc0d9d0e8f554d3df2388c535137d77 - Cache

    Requirements
        pkg/0.1#cdc0d9d0e8f554d3df2388c535137d77:2401fa1d188d289bb25c37cfa3317e13e377a351 - Build


And now we are interested in obtaining the path where our ``pkg/0.1`` recipe ``conanfile.py`` has been exported:

.. code-block:: bash

    $ conan cache path pkg/0.1
    <path to conan cache>/p/5cb229164ec1d245/e

    $ ls <path to conan cache>/p/5cb229164ec1d245/e
    conanfile.py  conanmanifest.txt

By default, if the recipe revision is not specified, it means the "latest" revision in the cache. This can 
also be made explicit by the literal ``#latest``, and also any recipe revision can be explicitly defined,
these commands are equivalent to the above:

.. code-block:: bash

    $ conan cache path pkg/0.1#latest
    <path to conan cache>/p/5cb229164ec1d245/e

    # The recipe revision might be different in your case. 
    # Check the "conan create" output to get yours
    $ conan cache path pkg/0.1#cdc0d9d0e8f554d3df2388c535137d77
    <path to conan cache>/p/5cb229164ec1d245/e


Together with the recipe folder, there are a two other folders that are common to all the binaries
produced with this recipe: the "export_source" folder and the "source" folder. Both can be
obtained with:

.. code-block:: bash

    $ conan cache path pkg/0.1 --folder=export_source
    <path to conan cache>/p/5cb229164ec1d245/es

    $ ls <path to conan cache>/p/5cb229164ec1d245/es
    CMakeLists.txt  include/  src/

    $ conan cache path pkg/0.1 --folder=source
    <path to conan cache>/p/5cb229164ec1d245/s

    $ ls <path to conan cache>/p/5cb229164ec1d245/s
    CMakeLists.txt  include/  src/


In this case the contents of the "source" folder are identical to the ones of the "export_source" folder
because the recipe did not implement any ``source()`` method that could retrieve code or do any other operation
over the code, like applying patches.

The recipe revision by default will be ``#latest``, this follows the same rules as above.

Note that these two folders will not exist if the package has not been built from source, like when a precompiled
binary is retrieve from a server.
    

It is also possible to obtain the folders of the binary packages providing the ``package_id``:

.. code-block:: bash

    # Your package_id might be different, it depends on the platform
    # Check the "conan create" output to obtain yours
    $ conan cache path pkg/0.1:2401fa1d188d289bb25c37cfa3317e13e377a351
    <path to conan cache>/p/1cae77d6250c23b7/p

    $ ls <path to conan cache>/p/1cae77d6250c23b7/p
    conaninfo.txt  conanmanifest.txt  include/  lib/

As above, by default it will resolve to the "latest" recipe revision and package revision.
The command above is equal to explicitly defining ``#latest`` or the exact revisions.
All the commands below are equivalent to the above one:

.. code-block:: bash

    $ conan cache path pkg/0.1#latest:2401fa1d188d289bb25c37cfa3317e13e377a351
    <path to conan cache>/p/1cae77d6250c23b7/p

    $ conan cache path pkg/0.1#latest:2401fa1d188d289bb25c37cfa3317e13e377a351#latest
    <path to conan cache>/p/1cae77d6250c23b7/p

    $ conan cache path pkg/0.1#cdc0d9d0e8f554d3df2388c535137d77:2401fa1d188d289bb25c37cfa3317e13e377a351
    <path to conan cache>/p/1cae77d6250c23b7/p


It is possible to access the "build" folder with all the temporary build artifacts:

.. code-block:: bash

    $ conan cache path pkg/0.1:2401fa1d188d289bb25c37cfa3317e13e377a351 --folder=build
    <path to conan cache>/p/1cae77d6250c23b7/b

    ls -al <path to conan cache>/p/1cae77d6250c23b7/b
    build/  CMakeLists.txt  CMakeUserPresets.json  conaninfo.txt  include/  src/

Again, the "build" folder will only exist if the package was built from source.


.. note::

    **Best practices**
    
    - This ``conan cache path`` command is intended for eventual inspection of the cache, but the cache
      package storage must be considered **read-only**. Do not modify, change, remove or add files from the cache.
    - If you are using this command to obtain the path to artifacts and then copying them, consider the usage of a ``deployer``
      instead. In the general case, extracting artifacts from the cache manually is discouraged.
