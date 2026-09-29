.. _conan_tools_google_bazel:


Bazel
-----

Available since: `1.37.0 <https://github.com/conan-io/conan/releases/tag/1.37.0>`_

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


It supports the following methods:

constructor
+++++++++++

.. code:: python

    def __init__(self, conanfile, namespace=None):

- ``conanfile``: the current recipe object. Always use ``self``.
- ``namespace``: Deprecated since Conan 1.62. It only keeps backward compatibility.


build()
+++++++

.. code-block:: python

    def build(self, args=None, label=None, target="//...", clean=True):


Equivalent to run the :command:`bazel <rcpaths> build <configs> <args> <targets>` command in the build folder.

The parameters are:

* ``args`` (defaulted to ``None``): List of extra arguments to add to the Bazel build command.
* ``label`` (defaulted to ``None``): Deprecated since Conan 1.62, superseded by ``target`` one. The Bazel target name.
* ``target`` (defaulted to ``//...``): The Bazel target name. By default, it runs all the targets under your WORKSPACE.
* ``clean`` (defaulted to ``True``): Runs a :command:`bazel clean` command before running every :command:`bazel build`.
  It helps to keep your Bazel cache up to date.

test()
+++++++

Available since: `1.62.0 <https://github.com/conan-io/conan/releases/tag/1.62.0>`_

.. code-block:: python

    def test(self, target=None):


Equivalent to :command:`bazel test <target>` in the build folder.

The parameters are:

* ``args`` (defaulted to ``None``): List of extra arguments to add to the Bazel build command.
* ``target`` (defaulted to ``//...``): The Bazel target name. By default, it runs all the targets under your WORKSPACE.


Properties
++++++++++

Available since: `1.62.0 <https://github.com/conan-io/conan/releases/tag/1.62.0>`_

The following properties affect the ``Bazel`` build helper:

- ``tools.build:skip_test=<bool>`` (boolean) if ``True``, it runs the ``bazel test <target>``.


conf
+++++

``Bazel`` is affected by these :ref:`[conf]<global_conf>` variables:

- ``tools.google.bazel:bazelrc_path``: List of paths to other bazelrc files to be used as :command:`bazel --bazelrc=rcpath1 ... build`.
- ``tools.google.bazel:configs``: List of Bazel configurations to be used as :command:`bazel build --config=config1 ...`.
