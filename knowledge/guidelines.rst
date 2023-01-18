Core guidelines
===============

This section summarizes some of the good and bad practices.

Good  and bad practices
-----------------------

- The recipes ``generate()`` method purpose is to prepare the build as much as possible.
  Users calling ``conan install`` will execute this method, and the generated files should
  allow users to do "native" builds (calling directly "cmake", "meson", etc.) as easy as possible.
  Thus, avoiding as much as possible any logic in the ``build()`` method, and moving it to
  the ``generate()`` method helps developers achieve the same build locally as the one that 
  would be produced by a ``conan create`` build in the local cache.
- Use always your own profiles in production, instead of relying on the auto-detected profile,
  as the output of such auto detection can vary over time, resulting in unexpected results.
  Profiles (and many other configuration), can be managed with ``conan config install``.
- Developers should not be able to upload to "development" and "production" repositories in the server. only
  CI builds has write permissions in the server. Developers should only have read permissions and 
  at most to some "playground" repositories used to work, share things with colleagues, but that
  never used, moved, copied to development or production repositories.
- The ``test_package`` purpose is to check that the package has been correctly created (that is, 
  that it has correctly packaged the headers, the libraries, etc, in the right folders), not that
  the functionality of the package is correct. Then, it should be kept as simple as possible, like
  building and running an executable that uses the headers and links against a packaged library
  should be enough. Such execution should be as simple as possible too. To run any kind of 
  unit and functional tests, that should be done in the ``build()`` method.
- Keep ``python_requires`` as simple as possible. Avoid transitive ``python_requires``, keep them
  as reduced as possible, and at most, require them explicitly in a "flat" structure, without
  ``python_requires`` requiring other ``python_requires``. Avoid inheritance (via ``python_requires_extend``)
  if not strictly necessary, and avoid multiple inheritance at all costs, as it is extremely
  complicated, and it does not work the same as the built-in Python one.


Forbidden practices
-------------------

- Calling the Conan process from Conan itself cannot be done. That includes calling
  Conan from recipe code, hooks, plugins, and basically every code that already executes when
  Conan is called. Doing it will result in undefined behavior. For example it is not valid
  to run ``conan search`` from a ``conanfile.py``. This includes indirect calls, like running
  Conan from a build script (like ``CMakeLists.txt``) while this build script is already being
  executed as a result of a Conan invocation.
- The Conan Python API can only be called from Conan custom commands or from user Python scripts, 
  but never from ``conanfile.py`` recipes, hooks, extensions, plugins, or any other code
  executed by Conan.
- Conan ``conanfile.py`` recipes user attributes and methods should always start with ``_``.
  Conan reserves the "public" namespace for all attributes and methods, and ``_conan`` for
  private ones. Using any non-documented Python function, method, class, attribute, even if
  it is "public" in the Python sense, is undefined behavior if such element is not documented
  in this documentation.
