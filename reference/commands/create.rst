.. _reference_commands_create:

conan create
============

.. autocommand::
    :command: conan create -h


The ``conan create`` command creates a package from the recipe specified in ``path``.

This command will first :command:`export` the recipe to the local cache and then build
and create the package. If a ``test_package`` folder (you can change the folder name with
the ``-tf`` argument or with the ``test_package_folder`` recipe attribute) is found, the command will run the consumer project to ensure that
the package has been created correctly. Check :ref:`testing Conan packages
<tutorial_creating_test>` section to know more about how to test your Conan packages.

.. tip::

    Sometimes you want to **skip/disable the test stage**. In that case you can skip/disable
    the test package stage by passing an empty value as the ``-tf`` argument:

    .. code-block:: bash

        $ conan create . --test-folder=""

    You might also want to do ``conan create . --build=missing`` so the package is not built
    if a binary already exists in the servers. If you want to also avoid the ``test_package``
    step when the binary already exists, you can apply the ``conan create . --build=missing --test-missing``,
    and it will only launch the test-package when the binary is built from source.


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


Methods execution order
-----------------------

The ``conan create`` executes :ref:`methods <reference_conanfile_methods>` of a *conanfile.py* in the following order:

#. Export recipe to the cache
    #. ``init()``
    #. ``set_name()``
    #. ``set_version()``
    #. ``export()``
    #. ``export_sources()``
#. Compute dependency graph
    #. ``ìnit()``
    #. ``config_options()``
    #. ``configure()``
    #. ``requirements()``
    #. ``build_requirements()``
#. Compute necessary packages
    #. ``validate_build()``
    #. ``validate()``
    #. ``package_id()``
    #. ``layout()``
    #. ``system_requirements()``
#. Install packages
    #. ``source()``
    #. ``build_id()``
    #. ``generate()``
    #. ``build()``
    #. ``package()``
    #. ``package_info()``

Steps ``generate()``,  ``build()``, ``package()`` from *Install packages* step will not be called if the package
is not being built from sources.

After that, if you have a folder named *test_package* in your project or you call the ``conan create`` command with the
``--test-folder`` flag, the command will invoke the methods of the *conanfile.py* file inside the folder in the following order:

#. Launch test_package
    #. (test package) ``init()``
    #. (test package) ``set_name()``
    #. (test package) ``set_version()``
#. Compute dependency graph
    #. (test package) ``config_options()``
    #. (test package) ``configure()``
    #. (test package) ``requirements()``
    #. (test package) ``build_requirements()``
    #. ``ìnit()``
    #. ``config_options()``
    #. ``configure()``
    #. ``requirements()``
    #. ``build_requirements()``
#. Compute necessary packages
    #. ``validate_build()``
    #. ``validate()``
    #. ``package_id()``
    #. ``layout()``
    #. (test package) ``validate_build()``
    #. (test package) ``validate()``
    #. (test package) ``package_id()``
    #. (test package) ``layout()``
    #. ``system_requirements()``
    #. (test package) ``system_requirements()``
#. Install packages
    #. ``build_id()``
    #. ``generate()``
    #. ``build()``
    #. ``package_info()``
#. Test the package
    #. (test package) ``build()``
    #. (test package) ``test()``

The functions with *(test package)* belong to the *conanfile.py* in the *test_package* folder. The steps
``build_id()``, ``generate()``, ``build()`` inside the *Install packages* step will be skipped if the project is
already installed. Typically, it should be installed just as it was installed in the previous "install packages" step.


Build modes
-----------

The ``conan create --build=<xxxx>`` build modes are very similar to the ``conan install`` ones documented in :ref:`Build Modes<reference_commands_build_modes>`,
with some differences.

By default, ``conan create`` defines the ``--build=current_pkg/current_version`` to force the build
from source for the current revision. This assumes that the source code (recipe, C/C++ code) was
changed and it will create a new revision. If that is not the case, then the ``--build=missing:current_pkg/current_version``
would be recommended to avoid rebuilding from source an already existing binary.

When a ``--build=xxx`` argument is defined in the command line, then the automatically defined
``--build=current_pkg/current_version`` is no longer passed, and it should be passed as a explicit argument too.

.. note::

    **Best practices**

    Having more than a ``package_revision`` for a given ``recipe_revision`` and ``package_id`` is discouraged
    in most cases, as it implies unnecessarily rebuilding from sources binaries that were already existing. For that
    reason, using ``conan create`` repeatedly over the same recipe without any source changes that would cause a
    new ``recipe_revision`` is discouraged, and using ``conan create . --build=missing:[pattern]`` would be the
    recommended approach.


.. seealso::

    - Read more about creating packages in the :ref:`dedicated
      tutorial<tutorial_creating_packages>`
    - Read more about :ref:`testing Conan packages <tutorial_creating_test>`
