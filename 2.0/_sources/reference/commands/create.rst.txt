conan create
============

.. autocommand::
    :command: conan create -h


The ``conan create`` command creates a package from the recipe specified in ``path``.

This command will first :command:`export` the recipe to the local cache and then build
and create the package. If a ``test_package`` folder (you can change the folder name with
the ``-tf`` argument) is found, the command will run the consumer project to ensure that
the package has been created correctly. Check :ref:`testing Conan packages
<tutorial_creating_test>` section to know more about how to test your Conan packages.

.. tip::

    Sometimes you want to **skip/disable the test stage**. In that case you can skip/disable
    the test package stage by passing an empty value as the ``-tf`` argument:

    .. code-block:: bash

        $ conan create . --test-folder=


Using conan create with build requirements
------------------------------------------

The ``--build-require`` argument allows to create the package using the configuration and
settings of the "build" context, as it was a ``build_require``. This feature allows to
create packages in a way that is consistent with the way they will be used later. 

.. code-block:: bash

    $ conan create . --name=cmake --version=3.23.1 --build-require  


Conan create output
-------------------

The ``conan create ... --format=json`` creates a json output containing the full dependency graph information.
This json is the same as the one created with ``conan graph info`` (see the :ref:`graph info json format<reference_commands_graph_info_json_format>`)
with extended information about the binaries, like a more complete ``cpp_info`` field.
This resulting json is the dependency graph of the package recipe being created, excluding all the ``test_package`` and other possible dependencies of the ``test_package/conanfile.py``. These dependencies only exist in the ``test_package`` functionality, and as such, are not part of the "main" product or package. If you are interested in capturing the dependency graph including the ``test_package`` (most likely not necessary in most cases), then you can do it running the ``conan test`` command separately.

The same happens for lockfiles created with ``--lockfile-out`` argument. The lockfile will only contain the created package and its transitive dependencies versions, but it will not contain the ``test_package`` or the transitive dependencies of the ``test_package/conanfile.py``. It is possible to capture a lockfile which includes those with the ``conan test`` command (though again, this might not be really necessary)

.. note::

  **Best practice**

  In general, having ``test_package/conanfile.py`` with dependencies other than the tested
  one should be avoided. The ``test_package`` functionality should serve as a simple check
  to ensure the package is correctly created. Adding extra dependencies to
  ``test_package`` might indicate that the check is not straightforward or that its
  functionality is being misused. If, for any reason, your ``test_package`` has additional
  dependencies, you can control their build using the ``--build-test`` argument.


.. seealso::

    - Read more about creating packages in the :ref:`dedicated
      tutorial<tutorial_creating_packages>`
