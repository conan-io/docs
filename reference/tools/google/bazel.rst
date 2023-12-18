.. _conan_tools_google_bazel:

Bazel
=====

.. include:: ../../../common/experimental_warning.inc

The ``Bazel`` build helper is a wrapper around the command line invocation of bazel. It will abstract the
calls like ``bazel <rcpaths> build <configs> <targets>`` into Python method calls.

The helper is intended to be used in the *conanfile.py* ``build()`` method, to call Bazel commands automatically
when a package is being built directly by Conan (create, install)


.. code-block:: python

    from conan import ConanFile
    from conan.tools.google import Bazel

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def build(self):
            bz = Bazel(self)
            bz.build(target="//main:hello-world")


Reference
---------

.. currentmodule:: conan.tools.google

.. autoclass:: Bazel
    :members:


Properties
++++++++++

The following properties affect the ``Bazel`` build helper:

- ``tools.build:skip_test=<bool>`` (boolean) if ``True``, it runs the ``bazel test <target>``.


conf
+++++

``Bazel`` is affected by these :ref:`[conf]<reference_config_files_global_conf>` variables:

- ``tools.google.bazel:bazelrc_path``: List of paths to other bazelrc files to be used as :command:`bazel --bazelrc=rcpath1 ... build`.
- ``tools.google.bazel:configs``: List of Bazel configurations to be used as :command:`bazel build --config=config1 ...`.


.. seealso::

    - :ref:`examples_tools_bazel_toolchain_build_simple_bazel_project`
