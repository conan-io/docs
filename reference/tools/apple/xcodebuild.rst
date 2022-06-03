.. _conan_tools_apple_xcodebuild:

XcodeBuild
----------

The ``XcodeBuild`` build helper is a wrapper around the command line invocation of Xcode. It
will abstract the calls like ``xcodebuild -project app.xcodeproj -configuration <config>
-arch <arch> ...``

The ``XcodeBuild`` helper can be used like:

.. code:: python

    from conan import conanfile
    from conan.tools.apple import XcodeBuild

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def build(self):
            xcodebuild = XcodeBuild(self)
            xcodebuild.build("app.xcodeproj")

Reference
+++++++++

.. currentmodule:: conan.tools.apple.xcodebuild

.. autoclass:: XcodeBuild
    :members: __init__

.. currentmodule:: conan.tools.apple.xcodebuild

.. automethod:: XcodeBuild.build

The ``Xcode.build()`` method internally implements a call to ``xcodebuild`` like:

.. code:: bash

    $ xcodebuild -project app.xcodeproj -configuration <configuration> -arch <architecture> <sdk> <verbosity> -target <target>/-alltargets

Where:

- ``configuration`` is the configuration, typically *Release* or *Debug*, which will be obtained
  from ``settings.build_type``.
- ``architecture`` is the build architecture, a mapping from the ``settings.arch`` to the
  common architectures defined by Apple 'i386', 'x86_64', 'armv7', 'arm64', etc.
- ``sdk`` is set based on the values of the ``os.sdk`` and ``os.sdk_version`` defining the
  ``SDKROOT`` Xcode build setting according to them. For example, setting ``os.sdk=iOS``
  and `os.sdk_version=8.3`` will pass ``SDKROOT=iOS8.3`` to the build system. In case you
  defined the ``tools.apple:sdk_path`` in your **[conf]** this value will
  take preference and will directly pass ``SDKROOT=<tools.apple:sdk_path>`` so **take into
  account** that for this case the skd located in that path should set your ``os.sdk`` and
  ``os.sdk_version`` settings values.
- ``verbosity`` is the verbosity level for the build and can take value 'verbose' or
  'quiet' if set by ``tools.apple.xcodebuild:verbosity`` in your **[conf]**

conf
++++

- ``tools.apple.xcodebuild:verbosity`` verbosity value for the build, can be 'verbose' or 'quiet'
- ``tools.apple:sdk_path`` path for the sdk location, will set the ``SDKROOT`` value with
  preference over composing the value from the ``os.sdk`` and ``os.sdk_version`` settings.

.. _conan_tools_apple_fix_apple_shared_install_name:

conan.tools.apple.fix_apple_shared_install_name()
-------------------------------------------------

.. currentmodule:: conan.tools.apple

.. autofunction:: fix_apple_shared_install_name

This tool will search for all the *dylib* files in the  *conanfile.package_folder* and fix
both the ``LC_ID_DYLIB`` and ``LC_LOAD_DYLIB`` fields on those files using the
*install_name_tool* utility available in macOS.

* For ``LC_ID_DYLIB`` which is the field containing the install name of the library, it
  will change the install name to one that uses the ``@rpath``. For example, if the
  install name is ``/path/to/lib/libname.dylib``, the new install name will be
  ``@rpath/libname.dylib``. This is done by executing internally something like: 

.. code-block:: bash
  
  install_name_tool /path/to/lib/libname.dylib -id @rpath/libname.dylib

* For ``LC_LOAD_DYLIB`` which is the field containing the path to the library
  dependencies, it will change the path of the dependencies to one that uses the
  ``@rpath``. For example, if the path is ``/path/to/lib/dependency.dylib``, the new path
  will be ``@rpath/dependency.dylib``. This is done by executing internally something
  like:

.. code-block:: bash
  
  install_name_tool /path/to/lib/libname.dylib -change /path/to/lib/dependency.dylib @rpath/dependency.dylib

This tool is typically needed by recipes that use Autotools as the build system and in the
case that the correct install names are not fixed in the library being packaged. Use this
tool, if needed, in the conanfile's ``package()`` method like:

.. code-block:: python

    from conan.tools.apple import fix_apple_shared_install_name
    class HelloConan(ConanFile):
      ...
      def package(self):
          autotools = Autotools(self)
          autotools.install()
          fix_apple_shared_install_name(self)