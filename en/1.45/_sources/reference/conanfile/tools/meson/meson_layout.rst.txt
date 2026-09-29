.. _meson_layout:

meson_layout
------------

.. warning::

    These tools are **experimental** and subject to breaking changes.
    This layout is ongoing work, will need more feedback and development to be complete.


For example, this would implement the standard Meson project layout:

.. code:: python

    from conan.tools.meson import meson_layout

    def layout(self):
        meson_layout(self)


If you want to try it, use the ``conan new hello/0.1 --template=meson_lib`` template.

The current layout implementation is very simple, if you use Meson, please give feedback of the expected layout for
different platforms:

.. code:: python

    def meson_layout(conanfile):
        conanfile.folders.build = "build-{}".format(str(conanfile.settings.build_type).lower())
        conanfile.cpp.build.bindirs = ["."]
        conanfile.cpp.build.libdirs = ["."]