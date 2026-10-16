# conan.tools.files downloads

<a id="conan-tools-files-get"></a>

## conan.tools.files.get()

### get(conanfile, url, md5=None, sha1=None, sha256=None, destination='.', filename='', keep_permissions=False, pattern=None, verify=True, retry=None, retry_wait=None, auth=None, headers=None, strip_root=False, extract_filter=None, excludes=None)

High level download and decompressing of a tgz, zip or other compressed format file.
Just a high level wrapper for download, unzip, and remove the temporary zip file once unzipped.
You can pass hash checking parameters: `md5`, `sha1`, `sha256`. All the specified
algorithms will be checked. If any of them doesn’t match, it will raise a `ConanException`.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **destination** – (Optional defaulted to `.`) Destination folder
  * **filename** – (Optional defaulted to ‘’) If provided, the saved file will have the specified name,
    otherwise it is deduced from the URL
  * **url** – forwarded to `tools.file.download()`.
  * **md5** – forwarded to `tools.file.download()`.
  * **sha1** – forwarded to `tools.file.download()`.
  * **sha256** – forwarded to `tools.file.download()`.
  * **keep_permissions** – forwarded to `tools.file.unzip()`.
  * **pattern** – forwarded to `tools.file.unzip()`.
  * **verify** – forwarded to `tools.file.download()`.
  * **retry** – forwarded to `tools.file.download()`.
  * **retry_wait** – S forwarded to `tools.file.download()`.
  * **auth** – forwarded to `tools.file.download()`.
  * **headers** – forwarded to `tools.file.download()`.
  * **strip_root** – forwarded to `tools.file.unzip()`.
  * **extract_filter** – forwarded to `tools.file.unzip()`.
  * **excludes** – forwarded to `tools.file.unzip()`.

#### IMPORTANT
`get()` calls internally `unzip()`.
Please read the note in [conan.tools.files.unzip()](https://docs.conan.io/2//reference/tools/files/basic.html.md#conan-tools-files-unzip) regarding Python 3.14 breaking changes and
the new tar archive extract filters.

## conan.tools.files.ftp_download()

### ftp_download(conanfile, host, filename, login='', password='', secure=False)

Ftp download of a file. Retrieves a file from an FTP server.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **host** – IP or host of the FTP server.
  * **filename** – Path to the file to be downloaded.
  * **login** – Authentication login.
  * **password** – Authentication password.
  * **secure** – Set to True to use FTP over TLS/SSL (FTPS). Defaults to False for regular FTP.

Usage:

```python
from conan.tools.files import ftp_download

def source(self):
    ftp_download(self, 'ftp.debian.org', "debian/README")
    self.output.info(load("README"))
```

## conan.tools.files.download()

### download(conanfile, url, filename, verify=True, retry=None, retry_wait=None, auth=None, headers=None, md5=None, sha1=None, sha256=None)

Retrieves a file from a given URL into a file with a given filename. It uses certificates from
a list of known verifiers for https downloads, but this can be optionally disabled.

You can pass hash checking parameters: `md5`, `sha1`, `sha256`. All the specified
algorithms will be checked. If any of them doesn’t match, the downloaded file will be removed
and it will raise a `ConanException`.

* **Parameters:**
  * **conanfile** – The current recipe object. Always use `self`.
  * **url** – URL to download. It can be a list, which only the first one will be downloaded, and
    the follow URLs will be used as mirror in case of download error.  Files accessible
    in the local filesystem can be referenced with a URL starting with `file:///`
    followed by an absolute path to a file (where the third `/` implies `localhost`).
  * **filename** – Name of the file to be created in the local storage
  * **verify** – When False, disables https certificate validation
  * **retry** – Number of retries in case of failure. Default is overridden by
    “tools.files.download:retry” conf
  * **retry_wait** – Seconds to wait between download attempts. Default is overriden by
    “tools.files.download:retry_wait” conf.
  * **auth** – A tuple of user and password to use HTTPBasic authentication
  * **headers** – A dictionary with additional headers
  * **md5** – MD5 hash code to check the downloaded file
  * **sha1** – SHA-1 hash code to check the downloaded file
  * **sha256** – SHA-256 hash code to check the downloaded file

Usage:

```python
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
```

### conf

It uses these [configuration entries](https://docs.conan.io/2//reference/config_files/global_conf.html.md#reference-config-files-global-conf):

- `tools.files.download:retry`: number of retries in case some error occurs.
- `tools.files.download:retry_wait`: seconds to wait between retries.
