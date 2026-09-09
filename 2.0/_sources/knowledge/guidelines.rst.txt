Core guidelines
===============


Good practices
--------------

- **build() should be simple, prepare the builds in generate() instead**: 
  The recipes' ``generate()`` method purpose is to prepare the build as much as possible.
  Users calling ``conan install`` will execute this method, and the generated files should
  allow users to do "native" builds (calling directly "cmake", "meson", etc.) as easy as possible.
  Thus, avoiding as much as possible any logic in the ``build()`` method, and moving it to
  the ``generate()`` method helps developers achieve the same build locally as the one that 
  would be produced by a ``conan create`` build in the local cache.
- **Always use your own profiles in production**, instead of relying on the auto-detected profile,
  as the output of such auto detection can vary over time, resulting in unexpected results.
  Profiles (and many other configuration), can be managed with ``conan config install``.
- **Developers should not be able to upload to "development" and "production" repositories** in the server.
  Only CI builds have write permissions in the server. Developers should only have read permissions and 
  at most to some "playground" repositories used to work and share things with colleagues,
  but which packages are never used, moved or copied to the development or production repositories.
- **The test_package purpose is to validate the correct creation of the package, not for functional testing**. The ``test_package`` purpose is to check that the package has been correctly created (that is, 
  that it has correctly packaged the headers, the libraries, etc, in the right folders), not that
  the functionality of the package is correct. Then, it should be kept as simple as possible, like
  building and running an executable that uses the headers and links against a packaged library
  should be enough. Such execution should be as simple as possible too. Any kind of 
  unit and functional tests should be done in the ``build()`` method.
- **All input sources must be common for all binary configurations**: All the "source" inputs, including the ``conanfile.py``, the ``conandata.yml``, the ``exports`` and ``exports_source``, the ``source()`` method, patches applied in the ``source()`` method, cannot be conditional to anything, platform, OS or compiler, as they are shared among all configurations. Furthermore, the line endings for all these things should be the same, it is recommended to use always just line-feeds in all platforms, and do not convert or checkout to ``crlf`` in Windows, as that will cause different recipe revisions.
- **Keep ``python_requires`` as simple as possible**. Avoid transitive ``python_requires``, keep them
  as reduced as possible, and at most, require them explicitly in a "flat" structure, without
  ``python_requires`` requiring other ``python_requires``. Avoid inheritance (via ``python_requires_extend``)
  if not strictly necessary, and avoid multiple inheritance at all costs, as it is extremely
  complicated, and it does not work the same as the built-in Python one.
- At the moment the **Conan cache is not concurrent**. Avoid any kind of concurrency or parallelism,
  for example different parallel CI jobs should use different caches (with CONAN_HOME env-var). This might
  change in the future and we will work on providing concurrency in the cache, but until then,
  use isolated caches for concurrent tasks.
- **Avoid 'force' and 'override' traits as a versioning mechanism.** The ``force`` and ``override`` traits to 
  solve conflicts are not recommended as a general versioning solution, just as a temporary workaround to solve 
  a version conflict. Its usage should be avoided whenever possible, and updating versions or version ranges in 
  the graph to avoid the conflicts without overrides and forces is the recommended approach.
- **Please, do not abuse 'tool_requires'**. Those are intended only for executables like ``cmake`` and ``ninja`` running in the "build"
  context, not for libraries or library-like dependencies, that must use ``requires`` or ``test_requires``.

Forbidden practices
-------------------

- **Conan is not re-entrant**: Calling the Conan process from Conan itself cannot be done. That includes calling
  Conan from recipe code, hooks, plugins, and basically every code that already executes when
  Conan is called. Doing it will result in undefined behavior. For example it is not valid
  to run ``conan search`` from a ``conanfile.py``. This includes indirect calls, like running
  Conan from a build script (like ``CMakeLists.txt``) while this build script is already being
  executed as a result of a Conan invocation. For the same reason **Conan Python API cannot be used from recipes**: The Conan Python API can only be called from Conan custom commands or from user Python scripts, 
  but never from ``conanfile.py`` recipes, hooks, extensions, plugins, or any other code
  executed by Conan.
- **Settings and configuration (conf) are read-only in recipes**: The settings and configuration cannot be defined or assigned values in recipes. Something like ``self.settings.compiler = "gcc"`` in recipes shouldn't be done. That is undefined behavior and can crash at any time, or just be ignored. Settings and configuration can only be defined in profiles, in command line arguments or in the ``profile.py`` plugin.
- **Recipes reserved names**: Conan ``conanfile.py`` recipes user attributes and methods should always start with ``_``.
  Conan reserves the "public" namespace for all attributes and methods, and ``_conan`` for
  private ones. Using any non-documented Python function, method, class, attribute, even if
  it is "public" in the Python sense, is undefined behavior if such element is not documented
  in this documentation.
- **Conan artifacts are immutable**: Conan packages and artifacts, once they are in the Conan cache, they are assumed to be immutable.
  Any attempt to modify the exported sources, the recipe, the conandata.yml or any of the exported
  or the packaged artifacts, is undefined behavior. For example, it is not possible to modify the 
  contents of a package inside the  ``package_info()`` method or the ``package_id()`` method, those
  methods should never modify, delete or create new files inside the packages. If you need to modify
  some package, you might use your own custom ``deployer``.
- **Conan cache paths are internal implementation detail**: The Conan cache paths are an internal implementation detail. Conan recipes provide abstractions
  like ``self.build_folder`` to represent the necessary information about folders, and commands
  like ``conan cache path`` to get information of the current folders. The Conan cache might 
  be checked while debugging, as read-only, but it is not allowed to edit, modify or delete 
  artifacts or files from the Conan cache by any other means that Conan command line or public API.
- **Sources used in recipes must be immutable**. Once a recipe is exported to the Conan cache, it is expected that the sources are immutable, that is, that retrieving the sources in the future will always retrieve the exact same sources. It is not allowed to use moving targets like a ``git`` branch or a download of a file that is continuously rewritten in the server. ``git`` checkouts must be of an immutable tag or a commit, and ``download()/get()`` must use checksums to verify the server files doesn't change. Not using immutable sources will be undefined behavior.
