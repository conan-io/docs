.. _reference_conanfile_methods_deploy:

deploy()
========

.. include:: ../../../common/experimental_warning.inc

The ``deploy()`` method is intended to deploy (copy) artifacts from the current package

.. code-block:: python

    from conan import ConanFile
    from conan.tools.files import copy

    class Pkg(ConanFile):

        def deploy(self):
            copy(self, "*", src=self.package_folder, dst=self.deploy_folder)


The ``deploy()`` method only executes at ``conan install`` time, when the ``--deployer-package`` argument is provided, otherwise it is completely ignored.

Artifacts will be copied to the output folder called ``self.deploy_folder``, by default it is the current folder, but the ``--deployer-folder`` can define a custom folder destinaton too.


See the documentation of the :ref:`conan install command<reference_commands_install_generators_deployers>` for mor information.

.. note::

    **Best practices**

    - Only "binary" package artifacts can be deployed, copying from the ``self.package_folder``. It is not recommended to try to copy only from the package folder, not other folders.
    - The ``deploy()`` method is intended for final, production deployment or installation of binaries in the machine, extracting them out of Conan. It is not intended for normal development operations, nor to build Conan packages against deployed binaries. The recommendation is to build against packages in the Conan cache.
    - The ``self.deploy_folder`` should only be used from the ``deploy()`` method, not any other method should use it.
