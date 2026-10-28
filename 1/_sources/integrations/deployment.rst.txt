.. _integration_deployment:

Deployment
==========

If you have a project with all the dependencies managed by Conan and you want to deploy into a specific format, the process is the
following:

  - Extract the needed artifacts to a local directory either using the :ref:`deploy generator <deployable_deploy_generator>` or the
    :ref:`json generator <deployable_json_generator>`.
  - Convert the artifacts (typically executables, shared libraries and assets) to a different deploy format. You will find the specific steps
    for some of the most common deploy technologies below.

.. toctree::
   :maxdepth: 2

   deployment/system_package_manager
   deployment/makeself
   deployment/appimage
   deployment/snap
   deployment/flatpak

