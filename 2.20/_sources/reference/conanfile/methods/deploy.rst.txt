.. _reference_conanfile_methods_deploy:

deploy()
========

.. include:: ../../../common/experimental_warning.inc

The ``deploy()`` method is intended to deploy (copy) artifacts from the current package.
It only executes at ``conan install`` time, when the ``--deployer-package`` argument is provided, otherwise ``deploy()`` is ignored.

Artifacts should be deployed to the ``self.deploy_folder``, by default the current folder. A custom destination can be defined with ``--deployer-folder``.
A basic ``deploy()`` method would copy all files from the package folder to the deploy folder:

.. code-block:: python

    from conan import ConanFile
    from conan.tools.files import copy

    class Pkg(ConanFile):

        def deploy(self):
            copy(self, "*", src=self.package_folder, dst=self.deploy_folder)


Refer to the documentation of the :ref:`conan install command<reference_commands_install_generators_deployers>` for more information.

.. note::

    **Best practices**

    - Only "binary" package artifacts can be deployed, copying from the ``self.package_folder``. It is recommended to copy only from the package folder, not other folders.
    - The ``deploy()`` method is intended for final production deployments or the installation of binaries on the machine, as it extracts the files from the Conan cache. It is not intended for normal development operations, nor to build Conan packages against deployed binaries. The recommendation is to build against packages in the Conan cache.
    - The ``self.deploy_folder`` should only be used from within the ``deploy()`` method.
