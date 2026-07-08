.. _integrations_python:

Python
======

.. _integrations_python_conan_py_build:

conan-py-build
--------------

`conan-py-build <https://github.com/conan-io/conan-py-build>`_ is a
`PEP 517 <https://peps.python.org/pep-0517/>`_ build backend that lets Conan
manage the C/C++ side of Python packages that ship compiled extensions (via
`pybind11 <https://pybind11.readthedocs.io/>`_,
`nanobind <https://nanobind.readthedocs.io/>`_, the Python C API, etc.).

Once it's declared as the ``build-backend`` in ``pyproject.toml``, commands
like ``pip wheel``, ``pip install`` or ``python -m build`` will:

- Read the dependencies and build steps from a regular Conan ``conanfile.py``.
- Resolve and install those dependencies with Conan, downloading precompiled
  binaries from ConanCenter or building them from source.
- Run the recipe's ``build()``/``package()`` methods with any build system Conan
  can drive (CMake, Meson, etc.).
- Copy what ``package()`` staged into the resulting wheel, alongside the pure
  Python part of the package.

.. tip::

    See it in action: :ref:`build a simple Python package with a C++ extension
    (pybind11 + fmt) using conan-py-build<examples_extensions_python_build_backend_build_python_extension_with_conan>`.

This removes the need for a separate, ad-hoc step to fetch and build C/C++
dependencies before packaging, and keeps that logic in the same
``conanfile.py`` format used for regular C/C++ packages. It also supports
profiles and lockfiles for reproducible builds, dynamic versioning, PEP 621
entry points, and integrates with ``auditwheel``/``delocate-wheel``/``delvewheel``
and `cibuildwheel <https://cibuildwheel.pypa.io/>`_ to produce self-contained
wheels with bundled shared libraries.

.. seealso::

    - Build a simple Python extension using Conan
      :ref:`example<examples_extensions_python_build_backend_build_python_extension_with_conan>`.
    - `conan-py-build documentation <https://conan-py-build.conan.io>`_, for
      the full getting started guide, configuration reference, and more
      examples (Meson, nanobind, cibuildwheel).
    - `Introducing conan-py-build <https://blog.conan.io/cpp/conan/python/2026/05/05/Introducing-conan-py-build.html>`_
      blog post.
