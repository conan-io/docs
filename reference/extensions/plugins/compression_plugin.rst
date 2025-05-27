.. _reference_extensions_compression_plugin:

Compression plugin
------------------

.. include:: ../../../common/experimental_warning.inc

The ``compression.py`` plugin is a Conan extension that allows users to
customize the compression and extraction processes for all files managed by Conan.

To activate it, place the plugin at: ``extensions/plugins/compression.py``.

This plugin provides flexibility in how Conan packages are compressed and
extracted, making it especially useful in scenarios such as:

- Replacing the default ``gzip`` compression algorithm with a more efficient one like ``zstd`` or ``xz``.
- Embedding custom metadata into the compressed archive.
- Modifying the internal structure of the package content.
- Modifying the file or directory permissions inside the compressed archive.
- Manage symbolic links inside archives.

These capabilities can help organizations reduce bandwidth and storage usage,
or enforce specific packaging policies.

.. important::

    Once this plugin is enabled, all operations involving ``conan upload`` and
    ``conan download`` will use the user-defined compression and extraction functions.
    This implies that **all users** within the same organization **must install** the
    plugin to avoid incompatibilities during extraction. 

    You can distribute and synchronize your configuration by packaging it and installing it via ``conan config install``.

Plugin Interface
++++++++++++++++

To implement a custom compression plugin, define the following two functions in ``compression.py``:

.. code-block:: python

    def tar_extract(archive_path: str, dest_dir: str, conf=None, ref=None, *args, **kwargs) -> None:
        ...

    def tar_compress(archive_path: str, files: dict[str,str], recursive=False, conf=None, ref=None, *args, **kwargs) -> None:
        ...


- ``archive_path``: Path to the final archive file. This value is immutable.

.. important::

    Even if you use a different compression algorithm, the output file must retain
    the ``.tgz`` extension. This is required for Conan to correctly handle archives.
    Changing the extension will **break** the workflow.

- ``files``: Dictionary of files to be compressed in the form ``{name_in_tar: absolute_path}``.
- ``recursive``: Whether to include subdirectories when adding files.
- ``conf``: Conan configuration object with user-defined options. It can be used to retrieve custom settings, such as compression level in the following way:

  .. code-block:: python

    compresslevel = conf.get("core.gzip:compresslevel", check_type=int) if conf else None


  Also, the ``conf`` object can be used to retrieve other custom configuration options that might be relevant for the compression process.

- ``ref``: Optional Conan reference (e.g., package or recipe reference) useful for logging.



Example: Compression Plugin Using xz
++++++++++++++++++++++++++++++++++++

This example shows how to implement a plugin using the ``xz`` compression format:

.. code-block:: python

    import os
    import tarfile
    from conan.api.output import ConanOutput

    def tar_compress(archive_path, files, recursive, conf=None, *args, **kwargs):
        name = os.path.basename(archive_path)
        ConanOutput().info(f"Compressing {name} using compression plugin (xz)")
        compresslevel = conf.get("core.gzip:compresslevel", check_type=int) if conf else None
        tar_kwargs = {"preset": compresslevel} if compresslevel else {}
        with tarfile.open(archive_path, f"w:xz", **tar_kwargs) as txz:
            for filename, abs_path in sorted(files.items()):
                txz.add(abs_path, filename, recursive=True)
    
    def tar_extract(archive_path, dest_dir, conf=None, *args, **kwargs):
        ConanOutput().info(f"Decompressing {os.path.basename(archive_path)} using compression plugin (xz)")
        with open(archive_path, mode='rb') as file_handler:
            txz = tarfile.open(fileobj=file_handler)
            txz.extraction_filter = (lambda member, path: member)
            txz.extractall(path=dest_dir)
            txz.close()

