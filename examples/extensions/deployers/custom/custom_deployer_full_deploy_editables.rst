.. _examples_extensions_deployers_full_deploy_editables:

Customize the full_deploy deployer: handling editable packages
==============================================================

The built-in :ref:`full_deploy<reference_extensions_deployer_full_deploy>` deployer copies the ``package_folder`` of every
dependency to the deployer output folder. This is what it does with the different kinds of dependencies:

- Packages in the Conan cache: the package contents are copied.
- Dependencies with ``package_folder=None``, which happens when the binary is skipped because it is not necessary: they are
  not deployed, as there is no folder to copy.
- Packages in :ref:`editable mode<editable_packages>`: the ``package_folder`` is the local project root folder, where
  the ``conanfile.py`` of the editable is. There is no actual "package" there, but ``full_deploy`` copies the whole folder, including
  sources, build artifacts and anything else in it.

Deploying editables is not recommended in general. Deployers are intended
to be customized. For real production needs, it is recommended to use your own deployer, and install it with
``conan config install`` or ``conan config install-pkg``.

This is the implementation of the built-in ``full_deploy``, slightly simplified, with some
extra code to handle editables. Copy it to a ``my_full_deploy.py`` file:

.. code-block:: python
    :caption: **my_full_deploy.py**

    import os
    import shutil

    from conan.errors import ConanException
    from conan.tools.files import rmdir


    def deploy(graph, output_folder, **kwargs):
        conanfile = graph.root.conanfile
        conanfile.output.info(f"Custom full deployer to {output_folder}")
        symlinks = conanfile.conf.get("tools.deployer:symlinks", check_type=bool, default=True)
        for dep in conanfile.dependencies.values():
            # Skipped binaries, there is nothing to deploy
            if dep.package_folder is None:
                continue
            # Editable packages: the package_folder is the local project folder, not a package.
            # Raise a ConanException instead of "continue" to fail when there are editables
            if dep.recipe == "Editable":
                conanfile.output.warning(f"Skipping deploy of editable package {dep}")
                continue

            folder_name = os.path.join("full_deploy", dep.context, dep.ref.name, str(dep.ref.version))
            build_type = dep.info.settings.get_safe("build_type")
            arch = dep.info.settings.get_safe("arch")
            if build_type:
                folder_name = os.path.join(folder_name, build_type)
            if arch:
                folder_name = os.path.join(folder_name, arch)

            new_folder = os.path.join(output_folder, folder_name)
            rmdir(conanfile, new_folder)
            try:
                shutil.copytree(dep.package_folder, new_folder, symlinks=symlinks)
            except Exception as e:
                raise ConanException(f"full_deploy: The copy of '{dep}' files failed: {e}.\n"
                                     f"You can use 'tools.deployer:symlinks' conf to disable symlinks")
            # Generators running after the deployer will point to the deployed folder
            dep.set_deploy_folder(new_folder)

Then it can be used as any other deployer:

.. code-block:: bash

    $ conan install . --deployer=my_full_deploy

Some notes about the code:

- ``dep.package_folder`` can be ``None`` for skipped binaries, so any deployer needs to check it.
- ``dep.recipe == "Editable"`` is a valid way to detect editable packages. It can also be used to
  implement other behaviors, like deploying only the artifacts defined in the ``cpp_info`` of the editable package
  (``dep.cpp_info.includedirs``, ``dep.cpp_info.libdirs``, etc.) instead of the whole folder.
- Generators like ``CMakeDeps`` do not need conditionals for editables: the ``layout()`` method makes ``cpp_info`` work
  transparently for packages in the cache and editable packages.
