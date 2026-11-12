
.. _devops_versioning_default:


Default versioning approach
----------------------------

When doing changes to the source code of a package, and creating such a package, one good practice is to increase the version
of the package to represent the scope and impact of those changes. The "semver" standard specification defines a ``MAJOR.MINOR.PATCH``
versioning approach with a specific meaning for changing each digit.

Conan implements versioning based on the "semver" specification, but with some extended capabilities that were demanded by the C and C++
ecosystems:

- Conan versions can have any number of digits, like ``MAJOR.MINOR.PATH.MICRO.SUBMICRO...``
- Conan versions can contain also letters, not only digits, and they are also ordered in alphabetical order, so ``1.a.2`` is older tha ``1.b.1`` for example.
- The version ranges can be equally defined for any number of digits, like ``dependency/[>=1.0.0.0 <1.0.0.10]``

Read the :ref:`introduction to versioning<tutorial_versioning>` in the tutorial.

But one very different aspect of C and C++ building model compared to other languages is how the dependencies affect the 
binaries of the consumers requiring them. This is described in the :ref:`Conan binary model<reference_binary_model_dependencies>` reference.

Basically, when some package changes its version, this can have different effects on the "consumers" of this package, requiring such
"consumers" to do a rebuild from source or not to integrate the new dependency changes. This also depends on the package types,
as the logic changes when linking a shared library or a static library. Conan binary model with ``dependency traits``, ``package_type``,
and the ``package_id`` modes is able to represent this logic and compute efficiently what needs to be rebuilt from source.

The default Conan behavior can give some hints of what version changes would be recommended when doing different changes to the packages
source code:

- Not modifying the version typically means that we want Conan automatic
  **recipe revisions** to handle that. A common use case is when the C/C++ source code is not modified at all, and only changes
  to the ``conanfile.py`` recipe are done. As the source code is the same, we might want to keep the same version number, and
  just have a new revision of that version.
- **Patch**: Increasing the **patch** version of a package means that only internal changes were done, in practice it means change to files
  that are not public headers of the package. This "patch" version can avoid having to re-build consumers of this package, for
  example if the current package getting a new "patch" version is a static library, all other packages that implement static
  libraries that depend on this one do not need to be re-built from source, as depending on the same public interface headers
  guarantee the same binary.
- **Minor**: If changes are done to package public headers, in an API source compatible way, then the recommendation would be to increase
  the **minor** verson of a package. That means that other packages that depend on it will be able to compile without issues, 
  but as there were modifications in public headers (that could contain C++ templates or other things that could be inlined in
  the consumer packages), then those consumer packages need to be rebuilt from source to incorporate these changes.
- **Major**: If API breaking changes are done to the package public headers, then increasing the **major** version is recommended. As the
  most common recommended version-range is something like ``dependency/[>1.0 <2]``, where the next major is excluded, that means
  that publishing these new versions will not break existing consumers, because they will not be used at all by those consumers,
  because their version ranges will exclude them. It will be necessary to modify the consumers recipes and source code (to fix
  the API breaking changes) to be able to use the new major version.


Note that while this is close to the standard "semver" definition of version and version ranges, the C/C++ compilation model
needs to introduce a new side effect, that of "needing to rebuild the consumers", following the logic explained above in the
``embed`` and ``non_embed`` cases.


This is just the default recommended versioning approach, but Conan allows to change these defaults, as it implements an extension of the "semver" standard that allows any number of digits,
letters, etc, and it also allows to change the ``package_id`` modes to define how different versions of the dependencies affect
the consumers binaries. See :ref:`how to customize the dependencies package_id modes<reference_binary_model_custom_compatibility_dependencies>`.


.. note::

    **Best practices**

    - It is not recommended to use other package reference fields, as the ``user`` and ``channel`` to represent changes in the source code,
      or other information like the git branch, as this becomes "viral" requiring changes in the ``requires`` of the consumers. Furthermore,
      they don't implement any logic in the build model with respect to which consumers need to be rebuilt.
    - The recommended approach is to use versioning and multiple server repositories to host the different packages, so they don't interfere
      with other builds, read :ref:`the Continuous Integration tutorial<ci_tutorial>` for more details.
