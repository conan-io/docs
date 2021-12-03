.. _conan_v2:

Migrating to 2.0
=================

Conan has started to work on the next major release. We've been gathering feedback
from the community about our features and we think it's time to break some default
behaviors, clean the codebase and add space for new developments. Development is
ongoing and the `Conan 2.0 Tribe <https://conan.io/tribe.html>`_ is having discussions
about it.

Conan 2.0-alpha is already released. You can access its documentation with the right version label.
It can be installed from PyPI with ``pip install conan==2.0.0-alpha1``

This section summarizes some of the necessary changes during Conan 1.X to be ready to upgrade to Conan 2.0:


- Use generators and helpers only from ``conan.tools.xxxx`` space. All the other ones are going to be removed.
- Use always build and host profiles. You can enable it by passing ``-pr:b=default`` in the command line to most commands.
  Do not use ``os_build``, ``arch_build`` anywhere in your recipes or code.
- Use ``self.test_requires()`` to define test requirements instead of the legacy ``self.build_requires(..., force_host_context)``.
- Activate revisions in your Conan configuration.
- Move all your packages to lowercase. Uppercase package names (or versions/user/channel) will not be possible in 2.0.
- Do not use ``self.deps_cpp_info``, ``self.deps_env_info`` or ``self.deps_user_info``. Use the ``self.dependencies`` access to get
  information about dependencies.
- Do not use the ``conan copy`` command to change user/channel. Packages will be immutable, and this command will dissapear in 2.0.
  Package promotions are generally done in the server side, copying packages from one server repository to another repository.
- Do not use dictionary expressions in your recipe ``settings`` definition (like ``settings = {"os": ["Windows", "Linux"]}``. This
  way of limiting supported configurations by one recipe will be removed. Use the ``validate()`` method instead to raise
  ``ConanInvalidConfiguration`` if strictly necessary to fail fast for unsupported configurations.
- If you are using ``editables``, the external template files are going to be removed. Use the ``layout()`` method definition instead.

