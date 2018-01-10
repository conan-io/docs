.. _introduction:


Introduction
===============
Open Source
------------
Conan is OSS, with an MIT license. Check out the source code and issue tracking (for reporting bugs and for feature requests) at https://github.com/conan-io/conan.

Decentralized package manager
-------------------------------
Conan is a decentralized package manager with a client-server architecture. This means that clients can fetch packages from, as well as upload packages to, different servers (“remotes”), similar to the “git” push-pull model to/from git remotes.

On a high level, the servers are just package storage. They do not build nor create the packages. The packages are created by the client, and if binaries are built from sources, that compilation is also done by the client application.

.. image:: images/systems.png
   :height: 200 px
   :width: 400 px
   :align: center


The different applications in the image above are:

- The **Conan client**: A console/terminal command line application that contains the complex logic for creating and consuming packages. The Conan client has a local cache for package storage and it allows you to fully create and test packages offline. You can **work offline** as long as new packages are not retrieved from the remote servers.
- The **conan_server**: A TCP server that can run easily on your **own server on-premises** to host your private packages. It also is a service application that can run as a daemon or a service behind a web server, (Apache, NGINX), or easily serve as a stand-alone application. Both the Conan client and the conan_server are OSS with an MIT license. If is free software allowing you to customize and redistribute without any legal restrictions.
- JFrog `Artifactory <https://www.jfrog.com/artifactory/>`_: A universal artifact manager that works directly with the Conan client to manage Conan packages and dependencies. It can also be used as an on-premises server. It's powerful features include an intuitive UI, support for multiple authorization protocols, High Availability, and more. It also provides a cloud-based version, allowing you to host your private packages while relieving you from the need of having any on-premises infrastructure.
- JFrog `Bintray <https://bintray.com/>`_: A universal distribution hub that provides a public and free hosting service for OSS Conan packages. Users can create their own repositories under their accounts and organizations, and freely upload their Conan packages to Bintray, without moderation. However, take into account that the packages are public and you must give appropriate credit to respective licenses, especially if the packages contain third party code. Reading or retrieving Conan packages from Bintray, does not require an account. An account is only required when uploading packages. In addition, Bintray provides a central repository called `conan-center <https://bintray.com/conan/conan-center>`_ which is moderated, and packages are reviewed before being accepted to ensure quality. This repository is currently empty as the process has just begun. In the meantime, the `conan-transit <https://bintray.com/conan/conan-transit>`_ repository contains a copy of all the packages that were in the conan.io repository, and were copied. These copies contains unmoderated packages, so the quality and cross-platform support of these packages might vary.



Binary management
-------------------------------
One of the most powerful features of Conan is that it can manage pre-compiled binaries for packages. To define a package, you need a package recipe that is referenced by name, version, user and channel. A package recipe can be a conanfile.py python script that defines how the package is built from sources, what final binary artifacts and package dependencies are included, and more.

.. image:: images/binary_mgmt.png
   :height: 200 px
   :width: 400 px
   :align: center

When a package recipe is used in the Conan client, and a “binary package” is built from the sources, the binary package is compatible with specific settings. These settings may be the operating system in which the package will run, the compiler type and version, or the computer architecture. If the package is rebuilt using the same sources but with different settings, (for example, for a different architecture), a new and different binary will be generated. Please note that the term “binary package” is displayed with quotes because, strictly, it is not necessarily a binary. A header-only library, for example, will contain just the headers in the “binary package”.

All the binary packages generated from a package recipe are managed and stored coherently.  When they are uploaded to a remote, they stay connected. Also, different clients building binaries from the same package recipe (like CI build slaves in different operating systems), will upload their binaries under the same package name to the remotes.

Consumers, i.e. client application users installing existing packages for reuse in their projects will typically retrieve pre-compiled binaries for their systems using existing compatible binaries. If these compatible binaries do not exist, it requires rebuilding from sources, on the client machine, to create a binary package matching their settings.e.


Cross platform, build system agnostic
--------------------------------------

Conan works and is being actively used on Windows, Linux (Ubuntu, Debian, RedHat, ArchLinux, Raspbian), OSX, FreeBSD, and SunOS. As it is portable, it might work on any other platform that runs Python. In the documentation, examples for a specific operating system might be found, such as ``conan install -s compiler="Visual Studio"``, which is specific for Windows users.  When installed on different systems, the reader should modify the commands to include their specific platform and settings (for example, ``conan install -s compiler=gcc``).

Also **Conan works with any build system**. In the documentation, CMake is widely used, because it is portable and well known. But Conan does not depend on CMake at all; it is not a requirement. **Conan is totally orthogonal to the build system**. There are some utilities that improve the usage of popular build systems such as CMake or Autotools, but they are just helpers. Furthermore, it is not necessary that all the packages be built with the same build system. It is possible to depend on packages created with other build systems than the one you are using to build your project.


Got any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write to us</a>
