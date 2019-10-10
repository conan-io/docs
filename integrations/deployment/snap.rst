Snap
____

`Snap <https://snapcraft.io/>`_ is the package management system available for the wide range of Linux distributions.
Unlike AppImage, Snap requires a daemon installed in the system in order to operate. Under the hood, **Snap** is based on
`SquashFS <https://github.com/plougher/squashfs-tools>`_.

The `packaging process <https://snapcraft.io/docs/creating-a-snap>`__ could be summed up in the following steps:

- `Install <https://snapcraft.io/docs/snapcraft-overview>`_ the snapcraft
- Run ``snapcraft init``
- Edit the ``snap/snapcraft.yml`` `manifest <https://snapcraft.io/docs/snapcraft-format>`_
- Run ``snapcraft`` in order to produce the snap
- `Publish <https://forum.snapcraft.io/t/releasing-your-app/6795>`__ and upload snap, so it could be installed on other systems.