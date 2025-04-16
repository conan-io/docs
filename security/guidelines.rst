.. _security_guidelines:


Security guidelines
===================

- Avoid tokens and passwords in URLs, can be in logs
- Users shouldn't have write permissions on the server
- Use write permissions tokens on the server only for very specific jobs
- Enable dependencies checking, with :ref:`conan_audit <security_audit>`
- Own the SWLC of dependencies, and specially binaries: build third parties from ``conan-center-index`` fork
- Backup sources as a mechanism for air-gapped and restricted networks
