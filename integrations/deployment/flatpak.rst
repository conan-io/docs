.. _deployment_flatpak:

Flatpak
-------

`Flatpak <https://flatpak.org/>`_ (former ``xdg-app``) is a package management system to distribute desktop applications for Linux. It is based on `OSTree <https://ostree.readthedocs.io/en/latest/manual/introduction/>`_. 
Flatpak is `RedHat <https://www.redhat.com>`_ initiative.

Unlike :ref:`AppImage <deployment_appimage>`, usually applications are distributed via `flathub <https://flathub.org>`_ store, and require a special runtime to install applications on target machines.

The major advantage of ``Flatpak`` is sandboxing: each application runs in its own isolated environment. ``Flatpak`` provides fine-grained control to system resources 
(e.g. network, bluetooth, host filesystem, etc.). ``Flatpak`` also offers a set of runtimes for various Linux desktop applications, e.g. 
`Freedesktop <https://www.freedesktop.org/wiki/>`_, `GNOME <https://www.gnome.org/>`_ and `KDE <https://kde.org/>`_.

The `packaging process <http://docs.flatpak.org/en/latest/first-build.html>`__ is:

- Install the flatpak runtime, flatpak-builder and SDK.
- Create a manifest ``<app-id>.json``
- Run the ``flatpak-builder`` in order to produce the application
- `publish <http://docs.flatpak.org/en/latest/publishing.html>`__ the application for further distribution

Alternatively, ``flatpak`` allows distributing the `single-file <http://docs.flatpak.org/en/latest/single-file-bundles.html>`_ package. Such package, however, cannot be run or installed on its own, it's needed to be imported to the local repository on another machine.
