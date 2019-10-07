.. _deployment:

How to deploy C++ applications with conan
=========================================

For the time being, it's frequently asked how to deploy C++ application which is built with help of `conan <https://conan.io>`_, 
and how to generate a deployable artifact after the build.
If you have a project with all the dependencies managed with Conan and you want to deploy it the process is:

- Extract the needed artifacts to a local directory. Check out the section :ref:`using_deploy_generator` and :ref:`using_json_generator` in order to get information on how to extract build artifacts.  
- Convert the artifacts (typically executables, shared libraries and assets) to a different deploy format. In the following sections, we are going to review some of the deploy technologies.

sections :ref:`using_deploy_generator` and :ref:`using_json_generator` in order to get information on how to extract build articats 
to a local directory for further deployment process.

system package manager
----------------------

There is an option is to use system package manager, like making **.rpm** or ***.deb** package(s). However, there are few limitations:

- it might be needed to (re)compile application N times for each of supported distro, or at least use the lowest version (see concerns about ``glibc`` below), see the section :ref:`custom_settings`, which explains how to customize conan settings (``settings.yml``) to model different Linux distributions in order to compile N different builds for them
- scalability problem - If you want to target different distros, then you need to create one package per supported distro (likely one for `Ubuntu <https://ubuntu.com/>`_, one for `Arch Linux <https://www.archlinux.org/>`_, etc.), and formats or guidelines for each distro might differ significantly

makeself.io
-----------

`makeself <https://makeself.io>`_ is a small command-line utility to generate self-extracting archives.
**makeself** is pretty popular and used for instance by 
`VirtualBox <https://www.virtualbox.org/wiki/Linux_Downloads>`_ and 
`CMake <https://cmake.org/download/>`_.
Such archives are usually used to create installers, and they often have ``.run``, ``.bin`` or ``.sh`` extensions.
Makeself created archives are just small startup scripts concatenated with tarballs.
When you run such self-extracting archive:

- small script (shim) extracts the embedded archive into the temporary directory
- script passes the execution to the entry point within the unpacked archive
- application is being run
- finally, the temporary directory removed

Therefore, it transparently appears just like a normal application execution. 
Check out the `guide <http://xmodulo.com/how-to-create-a-self-extracting-archive-or-installer-in-linux.html>`_ on how to make self-extracting archive via makeself.

AppImage
--------

`AppImage <https://appimage.org/>`_ is a format for Linux portable applications. Major advantages:

- doesn't require root permissions
- doesn't require applications to be installed (the only needed thing is **chmod +x**!)
- doesn't require installation of runtime or daemon into the system

Under the hood, **AppImage** uses filesystem in user-space 
(`FUSE <https://github.com/libfuse/libfuse>`_).
The `packaging process <https://docs.appimage.org/packaging-guide/manual.html#>`__ is pretty straightforward 
and could be easily automated:

- create a directory like ``MyApp.AppDir``
- download the `AppImage runtime <https://github.com/AppImage/AppImageKit/releases>`_ (**AppRun** file) and put to the directory 
- put all dependencies, like libraries (``.so``), resources (e.g. images) inside the directory
- fill some brief metadata (name, category) to the ``myapp.desktop`` configuration file
- run **appimagetool** against the directory

As a result, **MyApp-x86_64.AppImage** file will be produced, which is a regular Linux ELF file:

.. code-block:: console

    $ file MyApp-x86_64.AppImage
    MyApp-x86_64.AppImage: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 2.6.18, stripped

Such a file could be easily distributed just by copying, so it could be uploaded to the FTP server, moved to the flash drive, etc.

Snap
----

`Snap <https://snapcraft.io/>`_ is the package management system available for the wide range of Linux distributions.
Unlike ``AppImage``, ``Snap`` requires daemon installed in the system in order to operate. Under the hood, **Snap** is based on `SquashFS <https://github.com/plougher/squashfs-tools>`_.

The `packaging process <https://snapcraft.io/docs/creating-a-snap>`__ is:

- `install <https://snapcraft.io/docs/snapcraft-overview>`_ the snapcraft
- run ``snapcraft init``
- edit the ``snap/snapcraft.yml`` `manifest <https://snapcraft.io/docs/snapcraft-format>`_
- run ``snapcraft`` in order to produce the snap
- `publish <https://forum.snapcraft.io/t/releasing-your-app/6795>`__ and upload snap, so it could be installed on other systems

Flatpak
-------

`Flatpak <https://flatpak.org/>`_ is another package management system. Under the hood, **Flatpak** is based on `OSTree <https://ostree.readthedocs.io/en/latest/manual/introduction/>`_.

The `packaging process <http://docs.flatpak.org/en/latest/first-build.html>`__ is:

- install the flatpak runtime and SDK
- create a manifest ``<app-id>.json``
- run the ``flatpak-builder`` in order to produce the application
- `publish <http://docs.flatpak.org/en/latest/publishing.html>`__ the application for further distribution

Alternatively, ``flatpak`` allows distributing the `single-file <http://docs.flatpak.org/en/latest/single-file-bundles.html>`_ package. Such package, however, cannot be run or installed on its own, it's needed to be imported to the local repository on another machine.

Others
------

There are enterprise solutions for deployment, which are recommended to be used for production environments, such as 
`ansible <https://www.ansible.com/>`_, `chef <https://www.chef.io/application-deployment/>`_ and `puppet <https://puppet.com/>`_.
