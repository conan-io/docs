.. _introduction:

Introduction
============

Conan is a dependency and package manager for C and C++ languages. It is `free and open-source <https://github.com/conan-io/conan>`_, and it works in all platforms: Windows, Linux, OSX, FreeBSD, Solaris, etc. and can be used to develop for all targets including embedded, mobile (iOS, Android), bare metal. It also integrates with all build systems like CMake, Visual Studio (MSBuild), Makefiles, SCons, etc., including proprietary ones.

It is specifically designed and optimized for accelerating the development and Continuous Integration of C and C++ projects. With full binary management, it can create and reuse any number of different binaries (for different configurations, like architectures, compiler versions, etc) for any number of different versions of a package, using exactly the same process in all platforms. As it is decentralized, it is easy to run your own server to host your own packages and binaries privately, without needing to share them. The free `JFrog Artifactory Community Edition (CE) <https://conan.io/downloads.html>`_ is the recommended Conan server to host your own packages privately under your control.

Conan is mature and stable, with a strong commitment to forward compatibility (non-breaking policy), with a complete team dedicated full time to its improvement and support. It is backed and used by a great community, from open source contributors and package creators in `ConanCenter <https://conan.io/center>`_ to thousands of teams and companies using it.


Open Source
-----------

Conan is Free and Open Source, with a permissive MIT license. Check out the source code and issue tracking (for questions and support, reporting bugs and suggesting feature requests and improvements) at https://github.com/conan-io/conan

Decentralized package manager
-----------------------------

Conan is a decentralized package manager with a client-server architecture. This means that clients can fetch packages from, as well as upload packages to, different servers (“remotes”), similar to the “git” push-pull model to/from git remotes.

On a high level, the servers are just a package storage. They do not build nor create the packages. The packages are created by the client, and if binaries are built from sources, that compilation is also done by the client application.


.. image:: images/conan-systems.png
   :height: 400 px
   :width: 500 px
   :align: center


The different applications in the image above are:

- The Conan client: this is a console/terminal command-line application, containing the heavy logic for package creation and consumption. Conan client has a local cache for package storage, and so it allows you to fully create and test packages offline. You can also work offline as long as no new packages are needed from remote servers.
- `JFrog Artifactory Community Edition (CE) <https://conan.io/downloads.html>`_ is the recommended Conan server to host your own packages privately under your control. It is a free community edition of JFrog Artifactory for Conan packages, including a WebUI, multiple auth protocols (LDAP), Virtual and Remote repositories to create advanced topologies, a Rest API and generic repositories to host any artifact.
- The conan_server is a small server distributed together with the Conan client. It is a simple open-source implementation, it provides the basic functionality but no WebUI or other advanced features.
- `ConanCenter <https://conan.io/center>`_ is a central public repository where the community contributes packages for popular open-source libraries, like Boost, Zlib, OpenSSL, Poco, etc.

Binary management
-----------------

One of the most powerful features of Conan is that it can create and manage pre-compiled binaries for any possible platform and configuration. Using pre-compiled binaries and avoiding repeatedly building from source, save a lot of time to developers and Continuous Integration servers, while also improving the reproducibility and traceability of artifacts.

A package is defined by a "conanfile.py", a file that defines the package dependencies, the sources, how to build the binaries from sources, etc. One package “conanfile.py” recipe can generate any arbitrary number of binaries, one for each different platform and configuration: operating system, architecture, compiler, build type, etc. Those binaries can be created and uploaded to a server with the same commands in all platforms, having a single source of truth for all packages and not requiring a different solution for every different operating system.


.. image:: images/conan-binary_mgmt.png
   :height: 200 px
   :width: 400 px
   :align: center

Installation of packages from servers is also very efficient. Only the necessary binaries for the current platform and configuration are downloaded, not all of them. If the compatible binary is not available, the package can be built from sources in the client too.


All platforms, all build systems and compilers
----------------------------------------------

Conan works on Windows, Linux (Ubuntu, Debian, RedHat, ArchLinux, Raspbian), OSX, FreeBSD, and SunOS, and, as it is portable, it might work in any other platform that can run 
Python. It can target any existing platform, from bare metal, to desktop, mobile, embedded, servers, cross-building.

Conan works with any build system too. There are built-in integrations with most popular ones, like CMake, Visual Studio (MSBuild), Autotools and Makefiles, SCons, etc. But it is not a requirement to use any of them. It is not even necessary that all packages use the same build system, every package can use their own build system, and depend on other packages using different build systems. It is also possible to integrate with any build system, including proprietary ones.

Likewise, Conan can manage any compiler and any version. There are defaults definitions for the most popular ones: gcc, cl.exe, clang, apple-clang, intel, with different configurations of versions, runtimes, C++ standard library, etc. This model is also extensible to any custom configuration.



.. _stability:

Stable
------

From Conan 1.0, there is a commitment to stability, not breaking user space while evolving the tool and the platform. This means:

- Moving forward to following minor versions 1.1, 1.2, …, 1.X should never break existing recipes, packages or command line flows
- If something is breaking, it will be considered a bug and reverted
- Bug fixes will not be considered breaking, recipes and packages relying on the incorrect behavior of such bugs will be considered already broken.
- Only documented features are considered part of the public interface of Conan. Private implementation details, and everything not included in the documentation is subject to change.
- Configuration and automatic tools detection, like the detection of the default profile might be subject to change. Users are encouraged to define their configurations in profiles for repeatability. New installations of Conan might use different configurations.

The compatibility is always considered forward. New APIs, tools, methods, helpers can be added in following 1.X versions. Recipes and packages created with these features will be backwards incompatible with earlier Conan versions.

This means that public repositories, like ConanCenter assume the use of the latest version of the Conan client, and using an older version may result in failure of packages and recipes created with a newer version of the client.

Conan needs Python 3  to run. It has supported Python 2 until 1 January 2020, when it was officially deprecated by the Python maintainers. From Conan 1.22.0 release, Python 2 support is not guaranteed. See the :ref:`deprecation notice <python2>` for more details

If you have any question regarding Conan updates, stability, or any clarification about this definition of stability, please report in the documentation issue tracker: https://github.com/conan-io/docs.



Community
---------

Conan is being used in production by hundreds of companies like Audi, Continental, Plex, Electrolux and Mercedes-Benz and many thousands of developers around the world. 

But an essential part of Conan is that many of those users will contribute back, creating an amazing and helpful community:

- The https://github.com/conan-io/conan project has more than 3.5K stars in Github and counts with contributions of nearly 200 different users (this is just the client tool).
- Many other users contribute recipes for ConanCenter via the https://github.com/conan-io/conan-center-index repo, creating packages for popular Open Source libraries.
- More than one thousand of Conan users hang around the `CppLang Slack #conan channel <https://cpplang-inviter.cppalliance.org/>`_, and help responding to questions, discussing problems and approaches..


Have any questions? Please check out our :ref:`FAQ section <faq>` or |write_us|.

.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write to us</a>
