.. _deployment_appimage:

AppImage
--------

`AppImage <https://appimage.org/>`_ (former ``klik``, ``PortableLinuxApps``) is a format for Linux portable applications. Its major advantages are:

- It does not require root permissions.
- It does not require to install any application (it uses :command:`chmod +x`).
- It does not require the installation of runtime or a daemon into the system.

AppImage might be used to distribute desktop applications, command-line tools and system services (daemons).

AppImage uses filesystem in user-space 
(`FUSE <https://github.com/libfuse/libfuse>`_). It allows to easily mount the images and inspect their contents.

The main steps of the `packaging process <https://docs.appimage.org/packaging-guide/manual.html#>`__ are pretty straightforward 
and could be easily automated:

- Create a directory like ``MyApp.AppDir``
- Download the `AppImage runtime <https://github.com/AppImage/AppImageKit/releases>`_ (**AppRun** file) and put it into the directory.
- Copy all dependency files, like libraries (*.so*), resources (e.g. images) inside the directory.
- Fill the *myapp.desktop* configuration file with some brief metadata of your application: name, category...
- Run :command:`appimagetool`.

The copy step can be automatically done with Conan using the :ref:`json generator<deployable_json_generator>` and a custom script or just using
the :ref:`deploy generator <deployable_deploy_generator>`.

The result of the previous steps will give you a *MyApp-x86_64.AppImage* file, which is a regular Linux ELF file:

.. code-block:: console

    $ file MyApp-x86_64.AppImage
    MyApp-x86_64.AppImage: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 2.6.18, stripped

Finally, that file file could be easily distributed just by copying and uploading it to a Web or a FTP server, moving it to the flash drive, etc..
