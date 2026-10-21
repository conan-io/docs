.. _conan_tools_gnu_mingw:

is_mingw
========

.. currentmodule:: conan.tools.gnu

.. autofunction:: is_mingw

The helper detects a MinGW toolchain from the recipe settings:

* ``os`` is ``"Windows"``;
* ``os.subsystem`` is **not** ``"cygwin"`` (Cygwin uses a POSIX layer
  rather than a MinGW runtime);
* ``compiler`` is ``"gcc"``, **or** it is ``"clang"`` with no
  ``compiler.runtime`` set. ``clang-cl`` declares ``compiler.runtime``
  and is therefore not classified as MinGW; see the
  `Different flavors of Clang on Windows
  <https://blog.conan.io/2022/10/13/Different-flavors-Clang-compiler-Windows.html>`_
  blog post for the rationale.

Pass ``build_context=True`` to inspect ``settings_build`` instead of the
host settings (mirrors :ref:`is_msvc <conan_tools_microsoft_helpers>`).

Example:

.. code-block:: python

    from conan import ConanFile
    from conan.tools.gnu import is_mingw

    class Pkg(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            if is_mingw(self):
                # MinGW-specific branch: Autotools-style build, MinGW
                # import-library naming, etc.
                ...
