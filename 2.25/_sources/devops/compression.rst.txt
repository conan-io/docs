.. _devops_package_compression:

Package compression format
==========================

Conan compresses different artifacts before uploading them to the servers for faster uploads and downloads,
and lower storage needs. Specifically for C and C++ packages that could contain hundreds of different files,
for example multiple header files, it is very inefficient to upload and store them one by one.

For this reason Conan creates some compressed artifacts like ``conan_export.tgz``, ``conan_sources.tgz`` and
``conan_package.tgz``, for the recipe extra files, the exported sources and the final package binary 
respectively. These are the files that are uploaded to the servers, together with the ``conanfile.py``, the
``conanmanifest.txt`` and the ``conaninfo.txt`` files. 

The compression happens when a locally created artifact is being uploaded with the ``conan upload`` command.
If the recipe and package artifacts have been downloaded from the server, the compressed artifacts are cached
and it is not necessary to compress them again. Furthermore, uploading them to a server that contains those
artifacts will skip the actual upload transfer when the ``revisions`` match, or even avoid the transfer when
uploading to a repository without the revision, but the file already exists in the server if the server has
file de-duplication capabilities, like Artifactory.

These artifacts are automatically extracted when a package is downloaded or installed. 

.. warning::

    The different compressed artifacts are an internal implementation detail, and it is not allowed to 
    manipulate, change, remove or alter them.

Conan has traditionally used only the built-in ``tgz`` format to compress the artifacts, and allowed the
``core.gzip:compresslevel`` to select different compression levels (a tradeoff between speed and compression ratio).

From Conan 2.25 it is possible to (experimentally) select other compression formats that might be more efficient.


Using ``xz`` or ``zstd`` compression formats
--------------------------------------------

.. include:: ../common/experimental_warning.inc

From Conan 2.25 it is possible to choose between ``gz``, ``xz`` and ``zst`` compression formats with the
configuration: ``core.upload:compression_format``.
This configuration can be defined in the ``global.conf`` file. Recall that this file can also be distributed
to all developers and CI machines easily with ``conan config install/install-pkg``.

The compressed artifacts will be named after the compression format, with extensions such as ``conan_package.txz``,
``conan_package.tzst`` or ``conan_package.tgz``.

The ``core:compresslevel`` allows to select the compression level for the different algorithms. It supersedes
the previous ``core.gzip:compresslevel``.

.. important::

    The ``zstd`` compression is using Python>=3.14 built-in features. It requires then Python>=3.14, both
    for compressing and uploading, and for consuming recipes and packages that were compressed with 
    ``zstd``. Conan will fail with an error message in both cases if Python<3.14.

    Previous Conan versions (Conan<2.25), only understand ``.tgz`` artifacts and ``gz`` compression, and
    will fail to process artifacts compressed with other formats, 
    Make sure that all your Conan clients have updated to >=2.25 before using this feature. 
    