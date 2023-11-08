.. _conan_tools_google_bazel:


Bazel
-----

Available since: `1.37.0 <https://github.com/conan-io/conan/releases/tag/1.37.0>`_

The ``Bazel`` build helper is a wrapper around the command line invocation of bazel. It will abstract the
calls like ``bazel build //main:hello-world`` into Python method calls.

The helper is intended to be used in the ``build()`` method, to call Bazel commands automatically
when a package is being built directly by Conan (create, install)


.. code-block:: python

    from conan import ConanFile
    from conan.tools.google import Bazel

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def build(self):
            bazel = Bazel(self)
            bazel.build(target="//main:hello-world")

It supports the following methods:

constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile, namespace=None):

- ``conanfile``: the current recipe object. Always use ``self``.
- ``namespace``: this argument avoids collisions when you have multiple toolchain calls in the same
  recipe. By setting this argument, the *conanbuild.conf* file used to pass information to the
  toolchain will be named as: *<namespace>_conanbuild.conf*. The default value is ``None`` meaning that
  the name of the generated file is *conanbuild.conf*. This namespace must be also set with the same
  value in the constructor of ``BazelToolchain`` so that it reads the information from the proper file.


build()
+++++++

.. code:: python

    def build(self, args=None, label=None):


Calls the build system. Equivalent to :command:`bazel build {target}` in the build folder.


Properties
++++++++++

Available since: `1.62.0 <https://github.com/conan-io/conan/releases/tag/1.62.0>`_

The following properties affect the ``BazelDeps`` generator:

- ``tools.build:skip_test=<bool>`` (boolean) if ``True``, it runs the ``bazel test <target>``.
