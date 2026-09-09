conan.tools.files downloads
===========================

.. _conan_tools_files_get:

conan.tools.files.get()
-----------------------

.. currentmodule:: conan.tools.files.files

.. autofunction:: get


.. important::

    ``get()`` calls internally ``unzip()``. 
    Please read the note in :ref:`conan_tools_files_unzip` regarding Python 3.14 breaking changes and 
    the new tar archive extract filters.


conan.tools.files.ftp_download()
--------------------------------

.. currentmodule:: conan.tools.files.files

.. autofunction:: ftp_download


Usage:

.. code-block:: python

    from conan.tools.files import ftp_download

    def source(self):
        ftp_download(self, 'ftp.debian.org', "debian/README")
        self.output.info(load("README"))



conan.tools.files.download()
----------------------------

.. currentmodule:: conan.tools.files.files

.. autofunction:: download


Usage:

.. code-block:: python

    download(self, "http://someurl/somefile.zip", "myfilename.zip")

    # to disable verification:
    download(self, "http://someurl/somefile.zip", "myfilename.zip", verify=False)

    # to retry the download 2 times waiting 5 seconds between them
    download(self, "http://someurl/somefile.zip", "myfilename.zip", retry=2, retry_wait=5)

    # Use https basic authentication
    download(self, "http://someurl/somefile.zip", "myfilename.zip", auth=("user", "password"))

    # Pass some header
    download(self, "http://someurl/somefile.zip", "myfilename.zip", headers={"Myheader": "My value"})

    # Download and check file checksum
    download(self, "http://someurl/somefile.zip", "myfilename.zip", md5="e5d695597e9fa520209d1b41edad2a27")

    # to add mirrors
    download(self, ["https://ftp.gnu.org/gnu/gcc/gcc-9.3.0/gcc-9.3.0.tar.gz",
                    "http://mirror.linux-ia64.org/gnu/gcc/releases/gcc-9.3.0/gcc-9.3.0.tar.gz"],
                    "gcc-9.3.0.tar.gz",
                   sha256="5258a9b6afe9463c2e56b9e8355b1a4bee125ca828b8078f910303bc2ef91fa6")

conf
^^^^
It uses these :ref:`configuration entries <reference_config_files_global_conf>`:

- ``tools.files.download:retry``: number of retries in case some error occurs.
- ``tools.files.download:retry_wait``: seconds to wait between retries.
