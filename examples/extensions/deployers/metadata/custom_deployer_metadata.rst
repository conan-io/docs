.. _examples_extensions_deployers_metadata:

Copy metadata from all your dependencies
========================================

Please, first clone the sources to recreate this project. You can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ in GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/examples/extensions/deployers/metadata


In this example we are going to see how to create and use a custom deployer.
This deployer copies all the metadata files from your dependencies and puts them into a specific output folder.

.. note::

    To better understand this example, it is highly recommended to have previously read the :ref:`Deployers <reference_extensions_deployer_direct_deploy>` reference
    and the :ref:`metadata <devops_metadata>` feature.


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

For our example, we have 3 simple recipes:

.. graphviz::

    digraph {
        rankdir=LR;
        app -> pkg1 -> pkg2;
    }

We first run the first

.. code-block:: bash

    $ conan create pkg2
    $ conan create pkg1
    $ conan install . --deployer=metadata_deploy


Inspecting the resulting files we can see that it copied the metadata of our direct dependency ``pkg1``,
and also of the transitive ``pkg2`` dependency, to a ``dependencies_metadata`` folder.
With this code in mind, extra processing could be done to accomplish more specific needs.

Note that you can pass the ``--deployer-folder`` argument to change the base folder output path for the deployer.

Code tour
---------

The **metadata_deploy.py** file has the following code:

.. code-block:: python
    :caption: **metadata_deploy.py**

    import os
    import shutil

    def deploy(graph, output_folder, **kwargs):
        # Note the kwargs argument is mandatory to be robust against future changes.
        conanfile = graph.root.conanfile
        for name, dep in conanfile.dependencies.items():
            shutil.copytree(dep.package_metadata_folder,
                            os.path.join(output_folder, "dependencies_metadata", "packages", dep.ref.name, dep.pref.package_id))
            shutil.copytree(dep.recipe_metadata_folder,
                            os.path.join(output_folder, "dependencies_metadata", "recipes", dep.ref.name))


deploy()
++++++++

The ``deploy()`` method is called by Conan, and gets both a dependency graph and an output folder path as arguments.
It iterates all the dependencies of our recipe and copies every recipe and package metadata folder to their respective folders
under ``dependencies_metadata`` using ``shutil.copytree``.


.. note::

   If your custom deployer needs access to the full dependency graph, including those libraries that might be skipped,
   use the ``tools.graph:skip_binaries=False`` conf.
