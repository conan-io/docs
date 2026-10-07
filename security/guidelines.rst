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


.. _security_archive_extraction:

Archive extraction and trust model
----------------------------------

Conan extracts ``tar`` archives (``.tar``, ``.tgz``, ``.tar.gz``, ``.txz``, ``.tar.bz2``, etc.) in several places: the
``unzip()`` and ``get()`` tools in recipes, the package and recipe tarballs downloaded from remotes, and
``conan cache restore``. In all of them, **Conan uses the Python** ``tarfile`` **extraction filter** ``fully_trusted`` **by default**.
That means that the archive contents are extracted as they are, without the protections of the ``data`` filter:
absolute paths, paths with ``..`` that escape the destination folder, links pointing outside the destination, device files, and
special permission bits (setuid, setgid, sticky) are not rejected or sanitized. This is also the behavior of Python < 3.14, but Conan
sets it explicitly, so it doesn't change when running Conan with Python >= 3.14, where ``data`` became the Python default.

The reasons for this default are:

- The ``data`` filter is not backwards compatible for binary packages. For example, it strips setuid/setgid/sticky bits, removes group/other write
  permissions and rejects some links. Changing the default could silently alter or break existing packages.
- The content being extracted by Conan is either C/C++ source code that is going to be compiled and executed, or
  binaries that are going to be executed. Extracting such content from an untrusted archive is dangerous
  regardless of the extraction filter, so the only model that makes sense is that **the archives are fully trusted**.

This implies that **a malicious or compromised archive can write files outside of the destination folder**, and
it is the responsibility of the user to only consume archives from trusted sources:

- Only use Conan remotes that you trust, and limit who can upload to them (see the recommendations above).
- Do not run ``conan cache restore`` on archives from untrusted origins.
- In recipes, only use ``get()`` and ``unzip()`` with sources downloaded from trusted locations, and always
  provide a checksum (``sha256``) for downloaded tarballs. Consider the :ref:`Backup sources<conan_backup_sources>` feature.
- For tarballs from less trusted origins, the ``data`` filter can be requested with the ``extract_filter="data"`` argument in ``unzip()`` and ``get()``,
  or globally with the ``tools.files.unzip:filter=data`` conf. Note that it applies only to these recipe helpers, and not to
  the extraction of Conan packages downloaded from remotes or to ``conan cache restore``. It will not make it safe
  to compile or execute the extracted contents.

Issues that only rely on an archive being extracted with the ``fully_trusted`` filter are considered as part of this trust model, not as vulnerabilities.
