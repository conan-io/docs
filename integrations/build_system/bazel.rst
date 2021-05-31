.. _bazel:


|bazel_logo| Bazel
__________________

If you are using **Bazel** as your library build system, you can use the **Bazel** build helper.
This helper has a .build()`` method available to ease the call to Meson build system.

If you want to declare Conan dependencies in your project, you must do it, as usual, in the
**conanfile.py** file. For example:

.. code-block:: python

    class BazelExampleConan(ConanFile):
        name = "bazel-example"
        ....
        build_requires = "boost/1.76.0"

Then, tell Bazel to use that dependencies by adding this to the **WORKSPACE** file:

.. code-block:: text

    load("@//conandeps:dependencies.bzl", "load_conan_dependencies")
    load_conan_dependencies()

After that, just update the BUILD files where you need to use the new dependency:

.. code-block:: text

    cc_binary(
        name = "hello-world",
        srcs = ["hello-world.cc"],
        deps = [
            "@boost//:boost",
        ],
    )


.. |bazel_logo| image:: ../../images/conan-bazel_logo.png
