<a id="tutorial-versioning"></a>

# Versioning

This section of the tutorial introduces several concepts about versioning of packages.

First, explicit version updates and how to define versions of packages is explained.

Then, it will be introduced how `requires` with version ranges can
help to automate updating to the latest versions.

There are some situations when recipes or source code are changed, but the version of the
package is not increased. For those situations, Conan uses automatic `revisions` to
be able to provide traceability and reproducibility of those changes.

Lockfiles are a common mechanism in package managers to be able to reproduce the same
dependency graph later in time, even when new versions or revisions of dependencies are uploaded.
Conan also provides lockfiles to be able to guarantee this reproducibility.

Finally, when different branches of a dependency graph `requires` different versions of the
same package, that is called a “version conflict”. The tutorial will also introduce these
errors and how to address them.

# Table of contents

* [Versions](https://docs.conan.io/2//tutorial/versioning/versions.html.md)
  * [Automating versions](https://docs.conan.io/2//tutorial/versioning/versions.html.md#automating-versions)
  * [Requiring the new versions](https://docs.conan.io/2//tutorial/versioning/versions.html.md#requiring-the-new-versions)
* [Version ranges](https://docs.conan.io/2//tutorial/versioning/version_ranges.html.md)
  * [Semantic versioning](https://docs.conan.io/2//tutorial/versioning/version_ranges.html.md#semantic-versioning)
  * [Range expressions](https://docs.conan.io/2//tutorial/versioning/version_ranges.html.md#range-expressions)
* [Revisions](https://docs.conan.io/2//tutorial/versioning/revisions.html.md)
  * [Creating different revisions](https://docs.conan.io/2//tutorial/versioning/revisions.html.md#creating-different-revisions)
  * [Using revisions](https://docs.conan.io/2//tutorial/versioning/revisions.html.md#using-revisions)
  * [Uploading revisions](https://docs.conan.io/2//tutorial/versioning/revisions.html.md#uploading-revisions)
  * [Package revisions](https://docs.conan.io/2//tutorial/versioning/revisions.html.md#package-revisions)
* [Lockfiles](https://docs.conan.io/2//tutorial/versioning/lockfiles.html.md)
  * [Multi-configuration lockfiles](https://docs.conan.io/2//tutorial/versioning/lockfiles.html.md#multi-configuration-lockfiles)
  * [Evolving lockfiles](https://docs.conan.io/2//tutorial/versioning/lockfiles.html.md#evolving-lockfiles)
* [Dependencies conflicts](https://docs.conan.io/2//tutorial/versioning/conflicts.html.md)
  * [Resolving conflicts](https://docs.conan.io/2//tutorial/versioning/conflicts.html.md#resolving-conflicts)
  * [Overriding options](https://docs.conan.io/2//tutorial/versioning/conflicts.html.md#overriding-options)

#### NOTE
The Conan 2 Essentials training course is available for free at the JFrog Academy,
which covers the same topics as this documentation but in a more interactive way.
You can access it [here](https://academy.jfrog.com/path/conan-cc-package-manager/conan-2-essentials?utm_source=Conan+Docs).
