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
  'quiet' if set by ``tools.build:verbosity`` in your **[conf]**

conf
++++

- ``tools.build:verbosity`` (or ``tools.compilation:verbosity`` as fallback) which accepts ``quiet`` or ``verbose``,
  and sets the ``-verbose`` or ``-quiet`` flags in ``XcodeBuild.install()``

- ``tools.apple:sdk_path`` path for the sdk location, will set the ``SDKROOT`` value with
  preference over composing the value from the ``os.sdk`` and ``os.sdk_version`` settings.

