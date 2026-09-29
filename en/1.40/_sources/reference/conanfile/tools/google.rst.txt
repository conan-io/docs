.. _conan_tools_google:

conan.tools.google
==================

.. warning::

    These tools are **experimental** and subject to breaking changes.


BazelDeps
---------

Available since: `1.37.0 <https://github.com/conan-io/conan/releases>`_

The ``BazelDeps`` helper will generate one **conandeps/xxxx/BUILD** file per dependency. This dependencies will be
automatically added to the project by adding the following to the project's **WORKSPACE** file:


.. code-block:: text

    load("@//conandeps:dependencies.bzl", "load_conan_dependencies")
    load_conan_dependencies()


The dependencies should be added to the **conanfile.py** file as usual:

.. code-block:: python

    class BazelExampleConan(ConanFile):
        name = "bazel-example"
        ...
        generators = "BazelDeps", "BazelToolchain"
        requires = "boost/1.76.0"

Bazel
-----
The ``Bazel`` build helper is a wrapper around the command line invocation of bazel. It will abstract the
calls like ``bazel build //main:hello-world`` into Python method calls.

The helper is intended to be used in the ``build()`` method, to call Bazel commands automatically
when a package is being built directly by Conan (create, install)


.. code-block:: python

    from conans import ConanFile
    from conan.tools.google import Bazel

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def build(self):
            bazel = Bazel(self)
            bazel.configure()
            bazel.build(label="//main:hello-world")

It supports the following methods:

constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile):

- ``conanfile``: the current recipe object. Always use ``self``.


build()
+++++++

.. code:: python

    def build(self, args=None, label=None):


Calls the build system. Equivalent to :command:`bazel build {label}` in the build folder.
