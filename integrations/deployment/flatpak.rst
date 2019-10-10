Flatpak
_______

`Flatpak <https://flatpak.org/>`_ is a package management system to distribute desktop applications for Linux. It is based on `OSTree <https://ostree.readthedocs.io/en/latest/manual/introduction/>`_.

The `packaging process <http://docs.flatpak.org/en/latest/first-build.html>`__ is:

- Install the flatpak runtime and SDK.
- Create a manifest ``<app-id>.json``
- Run the ``flatpak-builder`` in order to produce the application
- `publish <http://docs.flatpak.org/en/latest/publishing.html>`__ the application for further distribution

Alternatively, ``flatpak`` allows distributing the `single-file <http://docs.flatpak.org/en/latest/single-file-bundles.html>`_ package. Such package, however, cannot be run or installed on its own, it's needed to be imported to the local repository on another machine.