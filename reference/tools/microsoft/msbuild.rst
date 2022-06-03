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

    $ <vcvars-cmd> && msbuild "MyProject.sln" /p:Configuration=<conf> /p:Platform=<platform>

Where:

- ``<vcvars-cmd>`` calls the Visual Studio prompt that matches the current recipe ``settings``.
- ``<conf>`` is the configuration, typically ``Release``, or ``Debug``, which is obtained from ``settings.build_type``,
  but this is configurable.
- ``<platform>`` is the architecture, a mapping from the ``settings.arch`` to the common 'x86', 'x64', 'ARM', 'ARM64'.


Customization
---------------

conf
++++

``MSBuild`` is affected by these ``[conf]`` variables:

- ``tools.microsoft.msbuild:verbosity`` accepts one of ``"Quiet", "Minimal", "Normal", "Detailed", "Diagnostic"`` to be passed
  to the ``MSBuild.build()`` call as ``msbuild .... /verbosity:XXX``.
- ``tools.microsoft.msbuild:max_cpu_count`` maximum number of CPUs to be passed to the ``MSBuild.build()``
  call as ``msbuild .... /m:N``.



Reference
---------

.. currentmodule:: conan.tools.microsoft

.. autoclass:: MSBuild
    :members: command, build
