.. _security_guidelines:


Security guidelines
===================

This is an incomplete and preliminary, not exhaustive security related recommendations when using Conan:

- Avoid using tokens and passwords in URLs, they can easily be leaked in logs. For example, if the ``source()`` method
  of recipes implement a ``git clone``, do not use git credentials in the URL, but instead use ssh-keys configured in the system.
  Same for downloading tarballs with ``tools.get()`` and ``tools.download()``.
- In general, developers shouldn't have write permissions on servers, just read permissions to download and install packages.
  Only the CI should have write/upload permissions. As an exception, it might be possible to use some "playground" repository that
  developers use to share packages for debugging and testing purposes with other colleagues, but that "playground" repository should
  be isolated from the normal testing and production repositories.
- Use tokens with limited permissions in CI. If a job only needs read permissions, use a token with read-permissions only. Use write
  credentials exclusively in the "upload" parts of the CI pieplines.
- Enable dependencies vulnerability checking with ``conan audit``, check :ref:`the conan audit docs<security_audit>`
- In many production cases, it is very recommended to fully own the SW lifecycle (SWLC) of the dependencies, including the third
  party dependencies. For this reason, the :ref:`Using ConanCenter packages in production environments <devops_consuming_conan_center>` section recommends building your own binaries
  from source and storing those binaries in your own private server, without downloading packages directly from ConanCenter.
  The :ref:`local-recipes-index feature<devops_local_recipes_index>` was designed to help in this process.
- To avoid being disrupted by internet outages and possible tampering of tarballs downloaded from the internet, the
  :ref:`Backup sources<conan_backup_sources>` feature can be used.
