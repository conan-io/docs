<a id="integrations-python"></a>

# Python

<a id="integrations-python-conan-py-build"></a>

## conan-py-build

[conan-py-build](https://github.com/conan-io/conan-py-build) is a
[PEP 517](https://peps.python.org/pep-0517/) build backend that lets Conan
manage the C/C++ side of Python packages that ship compiled extensions (via
[pybind11](https://pybind11.readthedocs.io/),
[nanobind](https://nanobind.readthedocs.io/), the Python C API, etc.).

Once it’s declared as the `build-backend` in `pyproject.toml`, commands
like `pip wheel`, `pip install` or `python -m build` will:

- Read the dependencies and build steps from a regular Conan `conanfile.py`.
- Resolve and install those dependencies with Conan, downloading precompiled
  binaries from ConanCenter or building them from source.
- Run the recipe’s `build()`/`package()` methods with any build system Conan
  can drive (CMake, Meson, etc.).
- Copy what `package()` staged into the resulting wheel, alongside the pure
  Python part of the package.

This removes the need for a separate, ad-hoc step to fetch and build C/C++
dependencies before packaging, and keeps that logic in the same
`conanfile.py` format used for regular C/C++ packages. It also supports
profiles and lockfiles for reproducible builds, dynamic versioning, PEP 621
entry points, and integrates with `auditwheel`/`delocate-wheel`/`delvewheel`
and [cibuildwheel](https://cibuildwheel.pypa.io/) to produce self-contained
wheels with bundled shared libraries.

#### SEE ALSO
- Build a simple Python extension using Conan
  [example](https://docs.conan.io/2//examples/extensions/python/build_backend/build_python_extension_with_conan.html.md#examples-extensions-python-build-backend-build-python-extension-with-conan).
- [conan-py-build documentation](https://conan-py-build.conan.io), for
  the full getting started guide, configuration reference, and more
  examples (Meson, nanobind, cibuildwheel).
- [Introducing conan-py-build](https://blog.conan.io/cpp/conan/python/2026/05/05/Introducing-conan-py-build.html)
  blog post.

<a id="integrations-python-pyenv"></a>

## PyEnv

The [PyEnv](https://docs.conan.io/2//reference/tools/system/pyenv.html.md#conan-tools-system-pyenv) tool installs executable Python
packages with `pip` inside a dedicated virtual environment, isolating them
from the system Python and from the Conan package itself. It’s meant for
Python CLI tools needed during a recipe’s build, such as a build system or
code generator invoked from `build()`, not for Python libraries imported
by the recipe.

#### SEE ALSO
- [PyEnv reference](https://docs.conan.io/2//reference/tools/system/pyenv.html.md#conan-tools-system-pyenv), for the full API and
  a recipe example.
