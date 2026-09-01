.. examples_extensions_deployers_sources:

Copy sources from all your dependencies
=======================================



Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/examples/extensions/deployers/sources


In this example we are going to see how to create and use a custom deployer.
This deployer copies all the source files from your dependencies and puts them into a specific output folder

.. note::

    To better understand this example, it is highly recommended to have previously read the :ref:`Deployers <reference_extensions_deployer_direct_deploy>` reference.


Locate the deployer
-------------------

In this case, the deployer is located in the same directory as our example conanfile,
but as shown in :ref:`Deployers <reference_extensions_deployer_direct_deploy>` reference,
Conan will look for the specified deployer in a few extra places in order, namely:

#. Absolute paths
#. Relative to cwd
#. In the ``[CONAN_HOME]/extensions/deployers`` folder
#. Built-in deployers


Run it
------

For our example, we have a simple recipe that lists both ``zlib`` and ``mcap`` as requirements.
With the help of the ``tools.build:download_source=True`` conf, we can force the invocation of its ``source()`` method,
which will ensure that sources are available even if no build needs to be carried out.

Now, you should be able to use the new deployer in both ``conan install`` and ``conan graph`` commands for any given recipe:

.. code-block:: bash

    $ conan graph info . -c tools.build:download_source=True --deployer=sources_deploy


Inspecting the command output we can see that it copied the sources of our direct dependencies ``zlib`` and ``mcap``,
**plus** the sources of our transitive dependencies, ``zstd`` and ``lz4`` to a ``dependencies_sources`` folder.
After this is done, extra preprocessing could be done to accomplish more specific needs.

Note that you can pass the ``--deployer-folder`` argument to change the base folder output path for the deployer.

Code tour
---------

The **source_deploy.py** file has the following code:



.. code-block:: python
    :caption: **sources_deploy.py**

    from conan.tools.files import copy
    import os


    def deploy(graph, output_folder, **kwargs):
        # Note the kwargs argument is mandatory to be robust against future changes.
        for name, dep in graph.root.conanfile.dependencies.items():
            if dep.folders is None or dep.folders.source_folder is None:
                raise ConanException(f"Sources missing for {name} dependency.\n"
                                      "This deployer needs the sources of every dependency present to work, either building from source, "
                                      "or by using the 'tools.build:download_source' conf.")
            copy(graph.root.conanfile, "*", dep.folders.source_folder, os.path.join(output_folder, "dependency_sources", str(dep)))


deploy()
++++++++

The ``deploy()`` method is called by Conan, and gets both a dependency graph and an output folder path as arguments.
It iterates all the dependencies of our recipe and copies every source file to their respective folders
under ``dependencies_sources`` using :ref:`conan.tools.copy<conan_tools_files_copy>`.


.. note::

    If you're using this deployer as an example for your own, remember that
    ``tools.build:download_source=True`` is necessary so that ``dep.folders.source_folder`` is defined for the dependencies.
    Without the conf, said variable will not be defined for those dependencies that do not need to be built from sources
    nor in those commands that do not require building, such as :command:`conan graph`.

.. note::

   If your custom deployer needs access to the full dependency graph, including those libraries that might be skipped,
   use the ``tools.graph:skip_binaries=False`` conf. This is useful for collecting, for example, all the licenses in your graph.
