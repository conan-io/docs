.. _tutorial_versioning_lockfiles:

Lockfiles
=========

- Create hello/1.0
- Chat/1.0 install --lockfile-out=conan.lock
- Create hello/1.1
- Chat/1.0 install --lockfile



Multi-configuration lockfiles
-----------------------------
- Add conditional dep
- conan lock augment


Evolving lockfiles
------------------

- force addition of hello/1.1
- merge lockfiles, but more correct to augment
- clean


Read more
- lock package binaries: not recommended
- CI links