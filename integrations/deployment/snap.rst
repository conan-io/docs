.. _deployment_snap:

Snap
----

`Snap <https://snapcraft.io/>`_ is the package management system available for the wide range of Linux distributions.
Unlike :ref:`AppImage <deployment_appimage>`, Snap requires a daemon (``snapd``) installed in the system in order to operate. Under the hood, **Snap** is based on
`SquashFS <https://github.com/plougher/squashfs-tools>`_. 
``Snap`` is `Canonical <https://canonical.com>`_ initiative. Usually, applications are distributed via `snapcraft <https://snapcraft.io/store>`_ store, but it's not mandatory.
``Snap`` provides fine-grained control to system resources (e.g. camera, removable media, network, etc.).
The major advantage is `plug-in system <https://snapcraft.io/docs/supported-plugins>`_, which allows to easily integrate ``Snap`` with different languages and build systems (e.g. CMake, autotools, etc.).

The `packaging process <https://snapcraft.io/docs/creating-a-snap>`__ could be summed up in the following steps:

- `Install <https://snapcraft.io/docs/snapcraft-overview>`_ the snapcraft
- Run ``snapcraft init``
- Edit the ``snap/snapcraft.yml`` `manifest <https://snapcraft.io/docs/snapcraft-format>`_
- Run ``snapcraft`` in order to produce the snap
- `Publish <https://forum.snapcraft.io/t/releasing-your-app/6795>`__ and upload snap, so it could be installed on other systems.

In order to integrate with build process managed with help of the conan, the following steps could be used:

- Use :ref:`deploy generator <deployable_deploy_generator>` (or :ref:`json generator<deployable_json_generator>` with custom script) to prepare the assets
- Use the `dump plug-in <https://snapcraft.io/docs/dump-plugin>`_ of snapcraft to simply copy the files deployed on previous step into the ``snap``
