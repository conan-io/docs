conan.tools.files downloads
===========================

.. warning::

    These tools are **experimental** and subject to breaking changes.



conan.tools.files.get()
-----------------------

Available since: `1.35.0 <https://github.com/conan-io/conan/releases/tag/1.35.0>`_

.. code-block:: python

    def get(conanfile, url, md5='', sha1='', sha256='', destination=".", filename="",
            keep_permissions=False, pattern=None, verify=True, retry=None, retry_wait=None,
            auth=None, headers=None, strip_root=False)

High level download and decompressing of a tgz, zip or other compressed format file.
Just a high level wrapper for download, unzip, and remove the temporary zip file once unzipped. You can pass hash checking parameters:
``md5``, ``sha1``, ``sha256``. All the specified algorithms will be checked. If any of them doesn't match, it will raise a
``ConanException``.

Parameters:

- **url**, **filename**, **md5**, **sha1**, **sha256**, **verify**, **retry**, **retry_wait**, **auth**, **headers**: forwarded to ``download()``
- **keep_permissions**, **pattern**, **strip_root**: forwarded to ``tools.unzip()`` (legacy, will be updated).


Examples:

.. code-block:: python

    from conan.tools.files import get

    def source(self):
        get(self, "http://url/file", md5='d2da0cd0756cd9da6560b9a56016a0cb')
        # also, specify a destination folder
        get(self, "http://url/file", destination="subfolder")


conan.tools.files.ftp_download()
--------------------------------

Available since: `1.35.0 <https://github.com/conan-io/conan/releases/tag/1.35.0>`_

.. code-block:: python

    def ftp_download(conanfile, ip, filename, login='', password='')


Ftp download of a file. Retrieves a file from an FTP server. This doesn't support SSL,
but you might implement it yourself using the standard Python FTP library.

Parameters:

- **conanfile**: Conanfile object, use always ``self``
- **ip** (Required): The IP or address of the ftp server.
- **filename** (Required): The filename, including the path/folder where it is located.
- **login** (Optional, Defaulted to ``""``): Login credentials for the ftp server.
- **password** (Optional, Defaulted to ``""``): Password credentials for the ftp server.

Examples:

.. code-block:: python

    from conan.tools.files import ftp_download

    def source(self):
        ftp_download(self, 'ftp.debian.org', "debian/README")
        self.output.info(load("README"))


conan.tools.files.download()
----------------------------

Available since: `1.35.0 <https://github.com/conan-io/conan/releases/tag/1.35.0>`_

Download a file

.. code-block:: python

    def download(conanfile, url, filename, verify=True, retry=None, retry_wait=None,
                 auth=None, headers=None, md5='', sha1='', sha256='')

Retrieves a file from a given URL into a file with a given filename. It uses certificates from a list of known verifiers for https
downloads, but this can be optionally disabled.

You can pass hash checking parameters: ``md5``, ``sha1``, ``sha256``. All the specified algorithms will be checked.
If any of them doesn't match, the downloaded file will be removed and it will raise a ``ConanException``.


Parameters:

- **conanfile** (Required): Conanfile object, use ``self`` always
- **url** (Required): URL to download. It can be a list, which only the first one will be downloaded, and the follow URLs will be used as mirror in case of download error.
                      Since Conan `1.51.0 <https://github.com/conan-io/conan/releases/tag/1.51.0>`_, files accessible in the local filesystem can be referenced with a URL starting with ``file:///`` followed by an absolute path to a file
                      (where the third ``/`` implies ``localhost``).
- **filename** (Required): Name of the file to be created in the local storage
- **verify** (Optional, Defaulted to ``True``): When False, disables https certificate validation.
- **retry** (Optional, Defaulted to ``1``): Number of retries in case of failure.
- **retry_wait** (Optional, Defaulted to ``5``): Seconds to wait between download attempts.
- **auth** (Optional, Defaulted to ``None``): A tuple of user and password to use HTTPBasic authentication. This is used directly in the ``requests`` Python library. Check other uses here: https://requests.readthedocs.io/en/master/user/authentication/#basic-authentication
- **headers** (Optional, Defaulted to ``None``): A dictionary with additional headers.
- **md5** (Optional, Defaulted to ``""``): MD5 hash code to check the downloaded file.
- **sha1** (Optional, Defaulted to ``""``): SHA-1 hash code to check the downloaded file.
- **sha256** (Optional, Defaulted to ``""``): SHA-256 hash code to check the downloaded file.

Configuration:

- ``tools.files.download:retry``: number of retries in case some error occurs.
- ``tools.files.download:retry_wait``: seconds to wait between retries.


Examples:

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

    # Retrieve file that is visible in the local filesystem
    tools.download("file:///C:/Users/MyUser/Downloads/somefile.zip", "myfilename.zip", md5="e5d695597e9fa520209d1b41edad2a27")
    tools.download("file:///home/myuser/downloads/somefile.zip", "myfilename.zip", md5="e5d695597e9fa520209d1b41edad2a27")

    # to add mirrors
    download(self, ["https://ftp.gnu.org/gnu/gcc/gcc-9.3.0/gcc-9.3.0.tar.gz",
                    "http://mirror.linux-ia64.org/gnu/gcc/releases/gcc-9.3.0/gcc-9.3.0.tar.gz",
                    "file:///home/myuser/localmirror/gcc-9.3.0/gcc-9.3.0.tar.gz"],
                    "gcc-9.3.0.tar.gz",
                   sha256="5258a9b6afe9463c2e56b9e8355b1a4bee125ca828b8078f910303bc2ef91fa6")
