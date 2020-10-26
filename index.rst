Welcome to conan
================

`Conan <https://conan.io>`_ is a software package manager which is intended for C and C++ developers.

Conan is universal and portable. It works in all operating systems including Windows, Linux, OSX, FreeBSD, Solaris, and others, and it can target any platform, including desktop, server, and cross-building for embedded and bare metal devices.
It integrates with other tools like Docker, MinGW, WSL, and with all build systems such as CMake, MSBuild,
integrates with oth`er tools like Docker, MinGW, WSL, and with all build systems: CMake, MSBuild,
Makefiles, Meson, SCons. It can even integrate with any proprietary build systems.

Conan is completely `free and open source <https://github.com/conan-io/conan>`_ and fully
decentralized. It has native integration with JFrog Artifactory, including the free
Artifactory Community Edition for Conan, enabling developers to host their own private packages on their own server.
The `ConanCenter <https://conan.io/center>`_ central repository contains hundreds of popular
open source libraries packages, with many pre-compiled binaries for mainstream compiler versions.

Conan can manage any number of different binaries for different configurations, including different
architectures, compilers, compiler versions, runtimes, C++ standard library, etc. When binaries are not
available for one configuration, they can be built from sources. Conan can create,
upload and download binaries with the same commands and flows in every platform, saving lots of time
in development and continuous integration. The binary compatibility can be configured and customized.

Conan has  a very large and active community, especially in `Github repositories <https://github.com/conan-io/conan>`_
and `Slack #conan channel <https://cpplang-inviter.cppalliance.org/>`_. This community also creates and maintains
packages in ConanCenter. Conan is used in production by thousands of companies, and consequently, it has a
commitment to stability, not breaking while moving forward in Conan 1.X versions.


.. toctree::
   :maxdepth: 2

   introduction
   training_courses
   installation
   getting_started
   using_packages
   creating_packages
   uploading_packages
   developing_packages
   devtools
   versioning
   mastering
   systems_cross_building
   extending
   integrations
   configuration
   howtos
   reference
   videos
   faq
   glossary
   changelog
   conan_v2
