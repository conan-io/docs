.. _version_ranges:


Version ranges
==============

Version range expressions are supported, both in ``conanfile.txt`` and in ``conanfile.py`` requirements.

The syntax is using brackets. The square brackets are the way to specify conan that is a version range. Otherwise, versions are plain strings, they can be whatever you want them to be (up to limitations of length and allowed characters). 

..  code-block:: python

   class HelloConan(ConanFile):
      requires = "Pkg/[>1.0,<1.8]@user/stable"


So when specifying ``Pkg/[expression]@user/stable`` it means that ``expression`` will be evaluated as a version range. Otherwise it will be understand as plain text, so ``requires = "Pkg/version@user/stable"`` always means to use the version ``version`` literally.

There are some packages that do not follow semver, a popular one would be the OpenSSL package with versions as ``1.0.2n``. They cannot be used with version-ranges, to require such packages you always have to use explicit versions (without brackets).

The process to manage plain versions vs version-ranges is also different. The second one requires a "search" in the remote, which is orders of magnitude slower than direct retrieval of the reference (plain versions), so take it into account if you plan to use it for very large projects.


Expressions are those defined and implemented by https://pypi.org/project/node-semver/,
but using a comma instead of spaces. Accepted expressions would be:

..  code-block:: python

   >1.1,<2.1    # In such range
   2.8          # equivalent to =2.8
   ~=3.0        # compatible, according to semver
   >1.1 || 0.8  # conditions can be OR'ed

Version range expressions are evaluated at the time of building the dependency graph, from
downstream to upstream dependencies. No joint-compatibility of the full graph is computed, instead,
version ranges are evaluated when dependencies are first retrieved.

This means, that if a package A depends on another package B (A->B), and A has a requirement for
``C/[>1.2,<1.8]``, this requirement is evaluated first and it can lead to get the version ``C/1.7``. If
package B has the requirement to ``C/[>1.3,<1.6]``, this one will be overwritten by the downstream one,
it will output a version incompatibility error. But the "joint" compatibility of the graph will not
be obtained. Downstream packages or consumer projects can impose their own requirements to comply
with upstream constraints, in this case a override dependency to ``C/[>1.3,<1.6]`` can be easily defined
in the downstream package or project.

The order of search for matching versions is as follows:

- First, the local conan storage is searched for matching versions, unless the :command:`--update` flag is provided to :command:`conan install`.
- If a matching version is found, it is used in the dependency graph as a solution.
- If no matching version is locally found, it starts to search in the remotes, in order. If some remote is specified with :command:`-r=remote`,
  then only that remote will be used.
- If the :command:`--update` parameter is used, then the existing packages in the local conan cache will not be used, and the same search of the
  previous steps is carried out in the remotes. If new matching versions are found, they will be retrieved, so subsequent calls to
  :command:`install` will find them locally and use them.
