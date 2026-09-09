.. _conan_tools_microsoft_msbuild:


MSBuild
========

The ``MSBuild`` build helper is a wrapper around the command line invocation of MSBuild. It abstracts the
calls like ``msbuild "MyProject.sln" /p:Configuration=<conf> /p:Platform=<platform>`` into Python method ones.

This helper can be used like:

.. code:: python

    from conan import ConanFile
    from conan.tools.microsoft import MSBuild

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def build(self):
            msbuild = MSBuild(self)
            msbuild.build("MyProject.sln")


The ``MSBuild.build()`` method internally implements a call to ``msbuild`` like:

.. code:: bash

    $ <vcvars-cmd> && msbuild "MyProject.sln" /p:Configuration=<configuration> /p:Platform=<platform>

Where:

- ``<vcvars-cmd>`` calls the Visual Studio prompt that matches the current recipe ``settings``.
- ``configuration``, typically Release, Debug, which will be obtained from ``settings.build_type``
  but this can be customized with the ``build_type`` attribute.
- ``<platform>`` is the architecture, a mapping from the ``settings.arch`` to the common 'x86', 'x64', 'ARM', 'ARM64'.
  This can be customized with the ``platform`` attribute.


Customization
---------------

attributes
++++++++++

You can customize the following attributes in case you need to change them:

- **build_type** (default ``settings.build_type``): Value for the ``/p:Configuration``.
- **platform** (default based on ``settings.arch`` to select one of these values: (``'x86', 'x64', 'ARM', 'ARM64'``):
  Value for the ``/p:Platform``.

Example:

.. code:: python

    from conan import ConanFile
    from conan.tools.microsoft import MSBuild
    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        def build(self):
            msbuild = MSBuild(self)
            msbuild.build_type = "MyRelease"
            msbuild.platform = "MyPlatform"
            msbuild.build("MyProject.sln")


conf
++++

``MSBuild`` is affected by these ``[conf]`` variables:

- ``tools.build:verbosity`` accepts one of ``quiet`` or ``verbose`` to be passed
  to the ``MSBuild.build()`` call as ``msbuild .... /verbosity:{Quiet,Detailed}``.
- ``tools.microsoft.msbuild:max_cpu_count`` maximum number of CPUs to be passed to the ``MSBuild.build()``
  call as ``msbuild .... /m:N``.



Reference
---------

.. currentmodule:: conan.tools.microsoft

.. autoclass:: MSBuild
    :members: command, build
