System package manager
----------------------

The Conan packages can be deployed using a system package manager. Usually this process is done by creating a folder structure with the
needed files and bundling all of them into the file format specific to the system package manager of choice, like *.rpm* or *.deb*. This
method is very convenient for deployment and distribution as it is natively integrated in the system. However, there are some limitations:

- It might require to create a specific package for each of supported distro, or at least use the lowest version (see concerns about
  ``glibc`` below), see the section :ref:`custom_settings`, which explains how to customize Conan settings to model different Linux
  distributions in order to create different packages for them.

- If you want to target different distros, then you need to create one package per supported distro (likely one for
  `Ubuntu <https://ubuntu.com>`_, one for `Arch Linux <https://www.archlinux.org>`_, etc.), and formats or guidelines for each distro might differ significantly

Check out the sections :ref:`makeself <deployment_makeself>`, :ref:`AppImage <deployment_appimage>`, 
:ref:`Flatpak <deployment_flatpak>` and :ref:`Snap <deployment_snap>` for information on how to create distribution-agnostic packages.
