.. _introduction:


Introduction
===============
Open Source
------------
Conan is OSS, with an MIT license. Check out the source code and issue tracking (for reporting bugs and for feature requests) at https://github.com/conan-io/conan .

Decentralized package manager
-------------------------------
Conan is a decentralized package manager with a client-server architecture. This means that clients can fetch packages from, as well as upload packages to, different servers (“remotes”), similar to the “git” push-pull model to/from git remotes.

On a high level, the servers are just package storage. They do not build nor create the packages. The packages are created by the client, and if binaries are built from sources, that compilation is also done by the client application.

.. image:: images/systems.png
   :height: 200 px
   :width: 400 px
   :align: center


The different applications in the picture are:

- The **conan client**: this is a console/terminal command line application, containing the heavy logic for package creation and consumption. Conan client has a local cache for package storage, and so it allows you to fully create and test packages offline.  You can also **work offline** so long as no new packages are needed from remote servers. 
- The **conan_server**: this is a TCP server that can be easily run as your **own server on-premises** to host your private packages. It is also a service application that can be run as a daemon or service, behind a web server (apache, nginx), or easily as stand-alone application.  Both the conan client and the conan_server are OSS, MIT license, so you can use them for free in your company, customize them, or redistribute them without any legal issue.
- JFrog `Artifactory <https://www.jfrog.com/artifactory/>`_ offers conan repositories; so it can also be used as an on-premises server. It is a more powerful solution, featuring a WebUI, multiple auth protocols, High Availability, etc. It also has cloud offerings that will allow you to have private packages without having any on-premises infrastructure.
- JFrog `Bintray <https://bintray.com/>`_ provides a public and free hosting service for OSS conan packages. Users can create their own repositories under their accounts and organizations, and freely upload conan packages there, without moderation. You should, however, take into account that those packages will be public, and so they must conform to the respective licenses, especially if the packages contain third party code. Just reading or retrieving conan packages from Bintray, doesn't require an account, an account is only needed to upload packages. Besides that, Bintray provides a central repository called `conan-center <https://bintray.com/conan/conan-center>`_ which is moderated, and packages are reviewed before being accepted to ensure quality. This repository is currently empty, the process has just started. In the meantime, the repository `conan-transit <https://bintray.com/conan/conan-transit>`_ contains a copy of all the packages that were in the conan.io repository, and were copied. Those were non-moderated packages, so quality and cross-platform support of packages might vary.



Binary management
-------------------------------
One of the powerful features of conan is that it can manage pre-compiled binaries for packages. To define a package, referenced by its name, version, user and channel, a package recipe is needed. Such a package recipe is a conanfile.py python script that defines how the package is built from sources, what the final binary artifacts are, the package dependencies, etc.

.. image:: images/binary_mgmt.png
   :height: 200 px
   :width: 400 px
   :align: center

When a package recipe is used in a conan client and a “package binary” is built from sources, that package binary will be compatible with certain settings, such as the OS it was created for, the compiler and compiler version, or the computer architecture. If the package is built again from the same sources but with different settings, (e.g. for a different architecture), a new, different binary will be generated. By the way, “package binary” is in quotes because, strictly, it is not necessarily a binary. A header-only library, for example, will contain just the headers in the “package binary”.

All the package binaries generated from a package recipe are managed and stored coherently.  When they are uploaded to a remote, they stay connected. Also, different clients building binaries from the same package recipe (like CI build slaves in different operating systems), will upload their binaries under the same package name to the remotes.

Consumers, i.e. client application users that are installing existing packages for reuse in their projects, will typically retrieve pre-compiled binaries for their systems, if there exist such compatible binaries, or otherwise require building from sources, on the client machine, to create a package binary matching their settings.


Cross platform, build system agnostic
--------------------------------------

Conan works and is being actively used on Windows, Linux (Ubuntu, Debian, RedHat, ArchLinux, Raspbian), OSX, FreeBSD, and SunOS, and, as it is portable, it might work in any other platform that can run python. In the documentation, examples for a specific OS might be found, such as ``conan install -s compiler="Visual Studio"``, which will be specific for Windows users.  If on a different system, the reader should adapt to their own platform and settings (for example ``conan install -s compiler=gcc``).

Also **conan works with any build system**. In the documentation, CMake will be widely used, because it is portable and well known. But conan does not depend on CMake at all; it is not a requirement. **Conan is totally orthogonal to the build system**. There are some utilities that improve the usage of popular build systems such as CMake or Autotools, but they are just helpers. Furthermore, it is not necessary that all the packages are built with the same build system. It is possible to depend on packages created with other build system than the one you are using to build your project.


Got any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write to us</a>
