.. spelling::

  isysroot


.. _tools:

Tools
=====

Under the tools module there are several functions and utilities that can be used in Conan package recipes:

.. code-block:: python
   :emphasize-lines: 2

    from conans import ConanFile
    from conans import tools

    class ExampleConan(ConanFile):
        ...

.. _tools_cpu_count:

tools.cpu_count()
-----------------

.. code-block:: python

    def tools.cpu_count()

Returns the number of CPUs available, for parallel builds. If processor detection is not enabled, it will safely return 1. When
running in Docker, it reads cgroup to detect the configured number of CPUs. It Can be overwritten with the environment variable
:ref:`env_vars_conan_cpu_count` and configured in the :ref:`conan_conf`.

.. _tools_vcvars_command:

tools.vcvars_command()
----------------------

.. code-block:: python

    def vcvars_command(settings, arch=None, compiler_version=None, force=False, vcvars_ver=None,
                       winsdk_version=None)

Returns, for given settings, the command that should be called to load the Visual Studio environment variables for a certain Visual Studio
version. It wraps the functionality of `vcvarsall <https://docs.microsoft.com/en-us/cpp/build/building-on-the-command-line?view=vs-2017>`_
but does not execute the command, as that typically have to be done in the same command as the compilation, so the variables are loaded for
the same subprocess. It will be typically used in the ``build()`` method, like this:

.. code-block:: python

    from conans import tools

    def build(self):
        if self.settings.build_os == "Windows":
            vcvars = tools.vcvars_command(self.settings)
            build_command = ...
            self.run("%s && configure %s" % (vcvars, " ".join(args)))
            self.run("%s && %s %s" % (vcvars, build_command, " ".join(build_args)))

The ``vcvars_command`` string will contain something like ``call "%vsXX0comntools%../../VC/vcvarsall.bat"`` for the corresponding Visual
Studio version for the current settings.

This is typically not needed if using CMake, as the ``cmake`` generator will handle the correct Visual Studio version.

If **arch** or **compiler_version** is specified, it will ignore the settings and return the command to set the Visual Studio environment
for these parameters.

Parameters:
    - **settings** (Required): Conanfile settings. Use ``self.settings``.
    - **arch** (Optional, Defaulted to ``None``): Will use ``settings.arch``.
    - **compiler_version** (Optional, Defaulted to ``None``): Will use ``settings.compiler.version``.
    - **force** (Optional, Defaulted to ``False``): Will ignore if the environment is already set for a different Visual Studio version.
    - **winsdk_version** (Optional, Defaulted to ``None``): Specifies the version of the Windows SDK to use.
    - **vcvars_ver** (Optional, Defaulted to ``None``): Specifies the Visual Studio compiler toolset to use.

.. note::

    When cross-building from x64 to x86 the toolchain by default is ``x86``. If you want to use ``amd64_x86`` instead, set the environment
    variable ``PreferredToolArchitecture=x64``.

.. _tools_vcvars_dict:

tools.vcvars_dict()
-------------------

.. code-block:: python

    vcvars_dict(settings, arch=None, compiler_version=None, force=False, filter_known_paths=False,
                vcvars_ver=None, winsdk_version=None, only_diff=True)

Returns a dictionary with the variables set by the :ref:`tools_vcvars_command` that can be directly applied to
:ref:`tools_environment_append`.

The values of the variables ``INCLUDE``, ``LIB``, ``LIBPATH`` and ``PATH`` will be returned as a list. When used with
:ref:`tools_environment_append`, the previous environment values that these variables may have will be appended automatically.

.. code-block:: python

    from conans import tools

    def build(self):
        env_vars = tools.vcvars_dict(self.settings)
        with tools.environment_append(env_vars):
            # Do something

Parameters:
    - Same as :ref:`tools_vcvars_command`.
    - **filter_known_paths** (Optional, Defaulted to ``False``): When True, the function will only keep the ``PATH`` entries that follows
      some known patterns, filtering all the non-Visual Studio ones. When False, it will keep the ``PATH`` will all the system entries.
    - **only_diff** (Optional, Defaulted to ``True``): When True, the command will return only the variables set by ``vcvarsall`` and not
      the whole environment. If `vcvars` modifies an environment variable by appending values to the old value (separated by ``;``), only
      the new values will be returned, as a list.

.. tools_vcvars:

tools.vcvars()
--------------

.. code-block:: python

    vcvars(settings, arch=None, compiler_version=None, force=False, filter_known_paths=False)

.. note::

    This context manager tool has no effect if used in a platform different from Windows.

This is a context manager that allows to append to the environment all the variables set by the :ref:`tools_vcvars_dict`. You can replace
:ref:`tools_vcvars_command` and use this context manager to get a cleaner way to activate the Visual Studio environment:

.. code-block:: python

    from conans import tools

    def build(self):
        with tools.vcvars(self.settings):
            do_something()

.. _tools_build_sln_command:

tools.build_sln_command() [DEPRECATED]
--------------------------------------

.. warning::

    This tool is deprecated and will be removed in Conan 2.0. Use :ref:`MSBuild()<msbuild>` build helper instead.

.. code-block:: python

    def build_sln_command(settings, sln_path, targets=None, upgrade_project=True, build_type=None,
                          arch=None, parallel=True, toolset=None, platforms=None, verbosity=None,
                          definitions=None)

Returns the command to call `devenv` and `msbuild` to build a Visual Studio project. It's recommended to use it with
:ref:`tools_vcvars_command`, so that the Visual Studio tools will be in path.

.. code-block:: python

    from conans import tools

    def build(self):
        build_command = build_sln_command(self.settings, "myfile.sln", targets=["SDL2_image"])
        command = "%s && %s" % (tools.vcvars_command(self.settings), build_command)
        self.run(command)

Parameters:
    - **settings** (Required): Conanfile settings. Use "self.settings".
    - **sln_path** (Required):  Visual Studio project file path.
    - **targets** (Optional, Defaulted to ``None``):  List of targets to build.
    - **upgrade_project** (Optional, Defaulted to ``True``): If ``True``, the project file will be upgraded if the project's VS version is
      older than current. When :ref:`env_vars_conan_skip_vs_project_upgrade` environment variable is set to ``True``/``1``, this parameter
      will be ignored and the project won't be upgraded.
    - **build_type** (Optional, Defaulted to ``None``): Override the build type defined in the settings (``settings.build_type``).
    - **arch** (Optional, Defaulted to ``None``): Override the architecture defined in the settings (``settings.arch``).
    - **parallel** (Optional, Defaulted to ``True``): Enables Visual Studio parallel build with ``/m:X`` argument, where X is defined by
      :ref:`env_vars_conan_cpu_count` environment variable or by the number of cores in the processor by default.
    - **toolset** (Optional, Defaulted to ``None``): Specify a toolset. Will append a ``/p:PlatformToolset`` option.
    - **platforms** (Optional, Defaulted to ``None``): Dictionary with the mapping of archs/platforms from Conan naming to another one. It
      is useful for Visual Studio solutions that have a different naming in architectures. Example: ``platforms={"x86":"Win32"}`` (Visual
      solution uses "Win32" instead of "x86"). This dictionary will update the following default one:

      .. code-block:: python

          msvc_arch = {'x86': 'x86',
                       'x86_64': 'x64',
                       'armv7': 'ARM',
                       'armv8': 'ARM64'}

    - **verbosity** (Optional, Defaulted to ``None``): Specifies verbosity level (``/verbosity:`` parameter).
    - **definitions** (Optional, Defaulted to ``None``): Dictionary with additional compiler definitions to be applied during the build.
      Use value of None to set compiler definition with no value.

.. _tools_msvc_build_command:

tools.msvc_build_command() [DEPRECATED]
---------------------------------------

.. warning::

    This tool is deprecated and will be removed in Conan 2.0. Use :ref:`MSBuild()<msbuild>`.get_command() instead.

.. code-block:: python

    def msvc_build_command(settings, sln_path, targets=None, upgrade_project=True, build_type=None,
                           arch=None, parallel=True, force_vcvars=False, toolset=None, platforms=None)

Returns a string with a joint command consisting in setting the environment variables via ``vcvars.bat`` with the above
:ref:`tools_vcvars_command` function, and building a Visual Studio project with the :ref:`tools_build_sln_command` function.

Parameters:
    - Same parameters as the above :ref:`tools_build_sln_command`.
    - **force_vcvars**: Optional. Defaulted to False. Will set ``tools.vcvars_command(force=force_vcvars)``.

.. _tools_unzip:

tools.unzip()
-------------

.. code-block:: python

    def unzip(filename, destination=".", keep_permissions=False, pattern=None)

Function mainly used in ``source()``, but could be used in ``build()`` in special cases, as when retrieving pre-built binaries from the
Internet.

This function accepts ``.tar.gz``, ``.tar``, ``.tzb2``, ``.tar.bz2``, ``.tgz``, ``.txz``, ``tar.xz``, and ``.zip`` files, and decompresses
them into the given destination folder (the current one by default).

It also accepts gzipped files, with extension ``.gz`` (not matching any of the above), and it will unzip them into a file with the same name
but without the extension, or to a filename defined by the ``destination`` argument.

.. code-block:: python

    from conans import tools

    tools.unzip("myfile.zip")
    # or to extract in "myfolder" sub-folder
    tools.unzip("myfile.zip", "myfolder")

You can keep the permissions of the files using the ``keep_permissions=True`` parameter.

.. code-block:: python

    from conans import tools

    tools.unzip("myfile.zip", "myfolder", keep_permissions=True)

Use ``pattern=None`` if you want to filter specific files and paths to decompress from the archive.

.. code-block:: python

    from conans import tools

    # Extract only files inside relative folder "small"
    tools.unzip("bigfile.zip", pattern="small/*")
    # Extract only txt files
    tools.unzip("bigfile.zip", pattern="*.txt")

Parameters:
    - **filename** (Required): File to be unzipped.
    - **destination** (Optional, Defaulted to ``"."``): Destination folder for unzipped files.
    - **keep_permissions** (Optional, Defaulted to ``False``): Keep permissions of files. **WARNING:** Can be dangerous if the zip
      was not created in a NIX system, the bits could produce undefined permission schema. Use only this option if you are sure that
      the zip was created correctly.
    - **pattern** (Optional, Defaulted to ``None``): Extract from the archive only paths matching the pattern. This should be a Unix
      shell-style wildcard. See `fnmatch <https://docs.python.org/3/library/fnmatch.html>`_ documentation for more details.

.. _tools_untargz:

tools.untargz()
---------------

.. code-block:: python

    def untargz(filename, destination=".", pattern=None)

Extract *.tar.gz* files (or in the family). This is the function called by the previous ``unzip()`` for the matching extensions, so
generally not needed to be called directly, call ``unzip()`` instead unless the file had a different extension.

.. code-block:: python

    from conans import tools

    tools.untargz("myfile.tar.gz")
    # or to extract in "myfolder" sub-folder
    tools.untargz("myfile.tar.gz", "myfolder")
    # or to extract only txt files
    tools.untargz("myfile.tar.gz", pattern="*.txt")

Parameters:
    - **filename** (Required): File to be unzipped.
    - **destination** (Optional, Defaulted to ``"."``): Destination folder for *untargzed* files.
    - **pattern** (Optional, Defaulted to ``None``): Extract from the archive only paths matching the pattern. This should be a Unix
      shell-style wildcard. See `fnmatch <https://docs.python.org/3/library/fnmatch.html>`_ documentation for more details.

.. _tools_get:

tools.get()
-----------

.. code-block:: python

    def get(url, md5='', sha1='', sha256='', destination=".", filename="", keep_permissions=False,
            pattern=None, requester=None, output=None, verify=True, retry=None, retry_wait=None,
            overwrite=False, auth=None, headers=None)

Just a high level wrapper for download, unzip, and remove the temporary zip file once unzipped. You can pass hash checking parameters:
``md5``, ``sha1``, ``sha256``. All the specified algorithms will be checked. If any of them doesn't match, it will raise a
``ConanException``.

.. code-block:: python

    from conans import tools

    tools.get("http://url/file", md5='d2da0cd0756cd9da6560b9a56016a0cb')
    # also, specify a destination folder
    tools.get("http://url/file", destination="subfolder")

Parameters:
    - **url** (Required): URL to download.
    - **md5** (Optional, Defaulted to ``""``): MD5 hash code to check the downloaded file.
    - **sha1** (Optional, Defaulted to ``""``): SHA-1 hash code to check the downloaded file.
    - **sha256** (Optional, Defaulted to ``""``): SHA-256 hash code to check the downloaded file.
    - **filename** (Optional, Defaulted to ```""``): Specify the name of the compressed file if it cannot be deduced from the URL.
    - **keep_permissions** (Optional, Defaulted to ``False``): Propagates the parameter to :ref:`tools_unzip`.
    - **pattern** (Optional, Defaulted to ``None``): Propagates the parameter to :ref:`tools_unzip`.
    - **requester** (Optional, Defaulted to ``None``): HTTP requests instance
    - **output** (Optional, Defaulted to ``None``): Stream object.
    - **verify** (Optional, Defaulted to ``True``): When False, disables https certificate validation.
    - **retry** (Optional, Defaulted to ``2``): Number of retries in case of failure. Default is overriden by ``general.retry``
      in the *conan.conf* file or an env variable ``CONAN_RETRY``.
    - **retry_wait** (Optional, Defaulted to ``5``): Seconds to wait between download attempts. Default is overriden by ``general.retry_wait``
      in the *conan.conf* file or an env variable ``CONAN_RETRY_WAIT``.
    - **overwrite**: (Optional, Defaulted to ``False``): When ``True`` Conan will overwrite the destination file if it exists. Otherwise it
      will raise.
    - **auth** (Optional, Defaulted to ``None``): A tuple of user, password can be passed to use HTTPBasic authentication. This is passed
      directly to the ``requests`` Python library. Check here other uses of the **auth** parameter:
      https://requests.readthedocs.io/en/master/user/authentication/#basic-authentication
    - **headers** (Optional, Defaulted to ``None``): A dictionary with additional headers.

.. _tools_get_env:

tools.get_env()
---------------

.. code-block:: python

    def get_env(env_key, default=None, environment=None)

Parses an environment and cast its value against the **default** type passed as an argument. Following Python conventions, returns
**default** if **env_key** is not defined.

This is a usage example with an environment variable defined while executing Conan:

.. code-block:: bash

    $ TEST_ENV="1" conan <command> ...

.. code-block:: python

    from conans import tools

    tools.get_env("TEST_ENV") # returns "1", returns current value
    tools.get_env("TEST_ENV_NOT_DEFINED") # returns None, TEST_ENV_NOT_DEFINED not declared
    tools.get_env("TEST_ENV_NOT_DEFINED", []) # returns [], TEST_ENV_NOT_DEFINED not declared
    tools.get_env("TEST_ENV", "2") # returns "1"
    tools.get_env("TEST_ENV", False) # returns True (default value is boolean)
    tools.get_env("TEST_ENV", 2) # returns 1
    tools.get_env("TEST_ENV", 2.0) # returns 1.0
    tools.get_env("TEST_ENV", []) # returns ["1"]

Parameters:
    - **env_key** (Required): environment variable name.
    - **default** (Optional, Defaulted to ``None``): default value to return if not defined or cast value against.
    - **environment** (Optional, Defaulted to ``None``): ``os.environ`` if ``None`` or environment dictionary to look for.

.. _tools_download:

tools.download()
----------------

.. code-block:: python

    def download(url, filename, verify=True, out=None, retry=None, retry_wait=None, overwrite=False,
                 auth=None, headers=None, requester=None, md5='', sha1='', sha256='')

Retrieves a file from a given URL into a file with a given filename. It uses certificates from a list of known verifiers for https
downloads, but this can be optionally disabled.

You can pass hash checking parameters: ``md5``, ``sha1``, ``sha256``. All the specified algorithms will be checked.
If any of them doesn't match, it will raise a ``ConanException``.

.. code-block:: python

    from conans import tools

    tools.download("http://someurl/somefile.zip", "myfilename.zip")

    # to disable verification:
    tools.download("http://someurl/somefile.zip", "myfilename.zip", verify=False)

    # to retry the download 2 times waiting 5 seconds between them
    tools.download("http://someurl/somefile.zip", "myfilename.zip", retry=2, retry_wait=5)

    # Use https basic authentication
    tools.download("http://someurl/somefile.zip", "myfilename.zip", auth=("user", "password"))

    # Pass some header
    tools.download("http://someurl/somefile.zip", "myfilename.zip", headers={"Myheader": "My value"})

    # Download and check file checksum
    tools.download("http://someurl/somefile.zip", "myfilename.zip", md5="e5d695597e9fa520209d1b41edad2a27")

Parameters:
    - **url** (Required): URL to download
    - **filename** (Required): Name of the file to be created in the local storage
    - **verify** (Optional, Defaulted to ``True``): When False, disables https certificate validation.
    - **out**: (Optional, Defaulted to ``None``): An object with a ``write()`` method can be passed to get the output. ``stdout`` will use
      if not specified.
    - **retry** (Optional, Defaulted to ``1``): Number of retries in case of failure. Default is overriden by ``general.retry``
      in the *conan.conf* file or an env variable ``CONAN_RETRY``.
    - **retry_wait** (Optional, Defaulted to ``5``): Seconds to wait between download attempts. Default is overriden by ``general.retry_wait``
      in the *conan.conf* file or an env variable ``CONAN_RETRY_WAIT``.
    - **overwrite**: (Optional, Defaulted to ``False``): When ``True``, Conan will overwrite the destination file if exists. Otherwise it
      will raise an exception.
    - **auth** (Optional, Defaulted to ``None``): A tuple of user and password to use HTTPBasic authentication. This is used directly in the
      ``requests`` Python library. Check other uses here: https://requests.readthedocs.io/en/master/user/authentication/#basic-authentication
    - **headers** (Optional, Defaulted to ``None``): A dictionary with additional headers.
    - **requester** (Optional, Defaulted to ``None``): HTTP requests instance
    - **md5** (Optional, Defaulted to ``""``): MD5 hash code to check the downloaded file.
    - **sha1** (Optional, Defaulted to ``""``): SHA-1 hash code to check the downloaded file.
    - **sha256** (Optional, Defaulted to ``""``): SHA-256 hash code to check the downloaded file.

.. _tools_ftp_download:

tools.ftp_download()
--------------------

.. code-block:: python

    def ftp_download(ip, filename, login="", password="")

Retrieves a file from an FTP server. This doesn't support SSL, but you might implement it yourself using the standard Python FTP library.

.. code-block:: python

    from conans import tools

    def source(self):
        tools.ftp_download('ftp.debian.org', "debian/README")
        self.output.info(load("README"))

Parameters:
    - **ip** (Required): The IP or address of the ftp server.
    - **filename** (Required): The filename, including the path/folder where it is located.
    - **login** (Optional, Defaulted to ``""``): Login credentials for the ftp server.
    - **password** (Optional, Defaulted to ``""``): Password credentials for the ftp server.

.. _tools_replace_in_file:

tools.replace_in_file()
-----------------------

.. code-block:: python

    def replace_in_file(file_path, search, replace, strict=True, encoding=None)

This function is useful for a simple "patch" or modification of source files. A typical use would be to augment some library existing
*CMakeLists.txt* in the ``source()`` method of a *conanfile.py*, so it uses Conan dependencies without forking or modifying the original
project:

.. code-block:: python

    from conans import tools

    def source(self):
        # get the sources from somewhere
        tools.replace_in_file("hello/CMakeLists.txt", "PROJECT(MyHello)",
            '''PROJECT(MyHello)
               include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
               conan_basic_setup()''')

Parameters:
    - **file_path** (Required): File path of the file to perform the replace in.
    - **search** (Required): String you want to be replaced.
    - **replace** (Required): String to replace the searched string.
    - **strict** (Optional, Defaulted to ``True``): If ``True``, it raises an error if the searched string is not found, so nothing is
      actually replaced.
    - **encoding** (Optional, Defaulted to ``None``): Specifies the input and output files text encoding. The ``None`` value has a special
      meaning - perform the encoding detection by checking the BOM (byte order mask), if no BOM is present tries to use: ``utf-8``, ``cp1252``.
      In case of ``None``, the output file is saved to the ``utf-8``

.. _tools_replace_path_in_file:

tools.replace_path_in_file()
----------------------------

.. code-block:: python

    def replace_path_in_file(file_path, search, replace, strict=True, windows_paths=None,
                             encoding=None)

Replace a path in a file with another string. In Windows, it will match the path even if the casing and the path separator doesn't match.

.. code-block:: python

    from conans import tools

    def build(self):
        tools.replace_path_in_file("hello/somefile.cmake", "c:\Some/PATH/to\File.txt","PATTERN/file.txt")

Parameters:
    - **file_path** (Required): File path of the file to perform the replace in.
    - **search** (Required): String with the path you want to be replaced.
    - **replace** (Required): String to replace the searched path.
    - **strict** (Optional, Defaulted to ``True``): If ``True``, it raises an error if the search string
      is not found and nothing is actually replaced.
    - **windows_paths** (Optional, Defaulted to ``None``): Controls whether the casing of the path and the different
      directory separators are taken into account:

      - ``None``: Only when Windows operating system is detected.
      - ``False``: Deactivated, it will match exact patterns (like :ref:`tools_replace_in_file`).
      - ``True``: Always activated, irrespective of the detected operating system.

    - **encoding** (Optional, Defaulted to ``None``): Specifies the input and output files text encoding. The ``None`` value has a special
      meaning - perform the encoding detection by checking the BOM (byte order mask), if no BOM is present tries to use: ``utf-8``, ``cp1252``.
      In case of ``None``, the output file is saved to the ``utf-8``


.. _tools_run_environment:

tools.run_environment()
-----------------------

.. code-block:: python

    def run_environment(conanfile)

Context manager that sets temporary environment variables set by :ref:`run_environment_reference`.

.. _tools_check_with_algorithm_sum:

tools.check_with_algorithm_sum()
--------------------------------

.. code-block:: python

    def check_with_algorithm_sum(algorithm_name, file_path, signature)

Useful to check that some downloaded file or resource has a predefined hash, so integrity and security are guaranteed. Something that could
be typically done in ``source()`` method after retrieving some file from the internet.

Parameters:
    - **algorithm_name** (Required): Name of the algorithm to be checked.
    - **file_path** (Required): File path of the file to be checked.
    - **signature** (Required): Hash code that the file should have.

There are specific functions for common algorithms:

.. code-block:: python

    def check_sha1(file_path, signature)
    def check_md5(file_path, signature)
    def check_sha256(file_path, signature)

For example:

.. code-block:: python

    from conans import tools

    tools.check_sha1("myfile.zip", "eb599ec83d383f0f25691c184f656d40384f9435")

Other algorithms are also possible, as long as are recognized by python ``hashlib`` implementation, via ``hashlib.new(algorithm_name)``.
The previous is equivalent to:

.. code-block:: python

    from conans import tools

    tools.check_with_algorithm_sum("sha1", "myfile.zip",
                                    "eb599ec83d383f0f25691c184f656d40384f9435")

.. _tools_patch:

tools.patch()
-------------

.. code-block:: python

    def patch(base_path=None, patch_file=None, patch_string=None, strip=0, output=None, fuzz=False)

Applies a patch from a file or from a string into the given path. The patch should be in diff (unified diff) format. To be used mainly in
the ``source()`` method.

.. code-block:: python

    from conans import tools

    tools.patch(patch_file="file.patch")
    # from a string:
    patch_content = " real patch content ..."
    tools.patch(patch_string=patch_content)
    # to apply in subfolder
    tools.patch(base_path=mysubfolder, patch_string=patch_content)

If the patch to be applied uses alternate paths that have to be stripped like this example:

.. code-block:: diff

    --- old_path/text.txt\t2016-01-25 17:57:11.452848309 +0100
    +++ new_path/text_new.txt\t2016-01-25 17:57:28.839869950 +0100
    @@ -1 +1 @@
    - old content
    + new content

Then, the number of folders to be stripped from the path can be specified:

.. code-block:: python

    from conans import tools

    tools.patch(patch_file="file.patch", strip=1)

If the patch to be applied differs from the source (fuzzy) the patch will fail by default, however,
you can force it using the ``fuzz`` option:

.. code-block:: python

    from conans import tools

    tools.patch(patch_file="file.patch", fuzz=True)


Parameters:
    - **base_path** (Optional, Defaulted to ``None``): Base path where the patch should be applied.
    - **patch_file** (Optional, Defaulted to ``None``): Patch file that should be applied.
    - **patch_string** (Optional, Defaulted to ``None``): Patch string that should be applied.
    - **strip** (Optional, Defaulted to ``0``): Number of folders to be stripped from the path.
    - **output** (Optional, Defaulted to ``None``): Stream object.
    - **fuzz** (Optional, Defaulted to ``False``): Accept fuzzy patches.

.. _tools_environment_append:

tools.environment_append()
--------------------------

.. code-block:: python

    def environment_append(env_vars)

This is a context manager that allows to temporary use environment variables for a specific piece of code in your conanfile:

.. code-block:: python

    from conans import tools

    def build(self):
        with tools.environment_append({"MY_VAR": "3", "CXX": "/path/to/cxx", "CPPFLAGS": None}):
            do_something()

The environment variables will be overridden if the value is a string, while it will be prepended if the value is a list.
Additionally, if value is ``None``, the given environment variable is unset (In the previous example, ``CPPFLAGS`` environment
variable will be unset), and in case variable wasn't set prior to the invocation, it has no effect on the given variable (``CPPFLAGS``).
When the context manager block ends, the environment variables will recover their previous state.

Parameters:
    - **env_vars** (Required): Dictionary object with environment variable name and its value.

.. _tools_chdir:

tools.chdir()
-------------

.. code-block:: python

    def chdir(newdir)

This is a context manager that allows to temporary change the current directory in your conanfile:

.. code-block:: python

    from conans import tools

    def build(self):
        with tools.chdir("./subdir"):
            do_something()

Parameters:
    - **newdir** (Required): Directory path name to change the current directory.

.. _tools_pythonpath:

tools.pythonpath()
------------------

.. warning::

    This way of reusing python code from other recipes can be improved via :ref:`python_requires`.

This tool is automatically applied in the conanfile methods unless :ref:`apply_env<apply_env>` is deactivated, so any ``PYTHONPATH``
inherited from the requirements will be automatically available.

.. code-block:: python

    def pythonpath(conanfile)

This is a context manager that allows to load the ``PYTHONPATH`` for dependent packages, create packages with Python code and reuse that
code into your own recipes.

For example:

.. code-block:: python

    from conans import tools

    def build(self):
        with tools.pythonpath(self):
            from module_name import whatever
            whatever.do_something()

When the :ref:`apply_env<apply_env>` is activated (default) the above code could be simplified as:

.. code-block:: python

    from conans import tools

    def build(self):
        from module_name import whatever
        whatever.do_something()

For that to work, one of the dependencies of the current recipe, must have a ``module_name`` file or folder with a ``whatever`` file or
object inside, and should have declared in its ``package_info()``:

.. code-block:: python

    from conans import tools

    def package_info(self):
        self.env_info.PYTHONPATH.append(self.package_folder)

Parameters:
    - **conanfile** (Required): Current ``ConanFile`` object.

.. _tools_no_op:

tools.no_op()
-------------

.. code-block:: python

    def no_op()

Context manager that performs nothing. Useful to condition any other context manager to get a cleaner code:

.. code-block:: python

    from conans import tools

    def build(self):
        with tools.chdir("some_dir") if self.options.myoption else tools.no_op():
            # if not self.options.myoption, we are not in the "some_dir"
            pass

.. _tools_human_size:

tools.human_size()
------------------

.. code-block:: python

    def human_size(size_bytes)

Will return a string from a given number of bytes, rounding it to the most appropriate unit: GB, MB, KB, etc. It is mostly used by the Conan
downloads and unzip progress.

.. code-block:: python

    from conans import tools

    tools.human_size(1024)
    >> 1.0KB

Parameters:
    - **size_bytes** (Required): Number of bytes.

.. _tools_osinfo:
.. _tools_systempackagetool:

tools.OSInfo and tools.SystemPackageTool
----------------------------------------

These are helpers to install system packages. Check :ref:`method_system_requirements`.

.. _cross_building_reference:

tools.cross_building()
----------------------

.. code-block:: python

    def cross_building(settings, self_os=None, self_arch=None, skip_x64_x86=False)

Reading the settings and the current host machine it returns ``True`` if we are cross building a Conan package:

.. code-block:: python

    from conans import tools

    if tools.cross_building(self.settings):
        # Some special action

Parameters:
    - **settings** (Required): Conanfile settings. Use ``self.settings``.
    - **self_os** (Optional, Defaulted to ``None``): Current operating system where the build is being done.
    - **self_arch** (Optional, Defaulted to ``None``): Current architecture where the build is being done.
    - **skip_x64_x86** (Optional, Defaulted to ``False``): Do not consider building for ``x86`` host from ``x86_64`` build machine
      as cross building, in case of host and build machine use the same operating system. Normally, in such case build machine may
      execute binaries produced for the target machine, and special cross-building handling may not be needed.

.. _tools_get_gnu_triplet:

tools.get_gnu_triplet()
-----------------------

.. code-block:: python

    def get_gnu_triplet(os_, arch, compiler=None)

Returns string with GNU like ``<machine>-<vendor>-<op_system>`` triplet.

Parameters:
    - **os_** (Required): Operating system to be used to create the triplet.
    - **arch** (Required): Architecture to be used to create the triplet.
    - **compiler** (Optional, Defaulted to ``None``): Compiler used to create the triplet (only needed for Windows).

.. _tools_run_in_windows_bash:

tools.run_in_windows_bash()
---------------------------

.. code-block:: python

    def run_in_windows_bash(conanfile, bashcmd, cwd=None, subsystem=None, msys_mingw=True, env=None, with_login=True)

Runs a UNIX command inside a bash shell. It requires to have "bash" in the path.
Useful to build libraries using ``configure`` and ``make`` in Windows. Check :ref:`Windows subsytems <windows_subsystems>` section.

You can customize the path of the bash executable using the environment variable ``CONAN_BASH_PATH`` or the :ref:`conan_conf` ``bash_path``
variable to change the default bash location.

.. code-block:: python

    from conans import tools

    command = "pwd"
    tools.run_in_windows_bash(self, command) # self is a conanfile instance

Parameters:
    - **conanfile** (Required): Current ``ConanFile`` object.
    - **bashcmd** (Required): String with the command to be run.
    - **cwd** (Optional, Defaulted to ``None``): Path to directory where to apply the command from.
    - **subsystem** (Optional, Defaulted to ``None`` will autodetect the subsystem): Used to escape the command according to the specified
      subsystem.
    - **msys_mingw** (Optional, Defaulted to ``True``): If the specified subsystem is MSYS2, will start it in MinGW mode (native windows
      development).
    - **env** (Optional, Defaulted to ``None``): You can pass a dictionary with environment variable to be applied **at first place** so they
      will have more priority than others.
    - **with_login** (Optional, Defaulted to ``True``): Pass the ``--login`` flag to :command:`bash` command. This might come handy when you
      don't want to create a fresh user session for running the command.

.. _tools_get_cased_path:

tools.get_cased_path()
----------------------

.. code-block:: python

    get_cased_path(abs_path)

This function converts a case-insensitive absolute path to a case-sensitive one. That is, with the real cased characters. Useful when using
Windows subsystems where the file system is case-sensitive.

.. _tools_detected_os:

tools.detected_os()
-------------------

.. code-block:: python

    detected_os()

It returns the recognized OS name e.g "Macos", "Windows". Otherwise it will return the value from ``platform.system()``.

.. _tools_remove_from_path:

tools.remove_from_path()
------------------------

.. code-block:: python

    remove_from_path(command)

This is a context manager that allows you to remove a tool from the ``PATH``. Conan will locate the executable (using :ref:`tools_which`)
and will remove from the ``PATH`` the directory entry that contains it. It's not necessary to specify the extension.

.. code-block:: python

    from conans import tools

    with tools.remove_from_path("make"):
        self.run("some command")

.. _tools_unix_path:

tools.unix_path()
-----------------

.. code-block:: python

    def unix_path(path, path_flavor=None)

Used to translate Windows paths to MSYS/CYGWIN Unix paths like ``c/users/path/to/file``.

Parameters:
    - **path** (Required): Path to be converted.
    - **path_flavor** (Optional, Defaulted to ``None``, will try to autodetect the subsystem): Type of Unix path to be returned. Options are
      ``MSYS``, ``MSYS2``, ``CYGWIN``, ``WSL`` and ``SFU``.

.. _tools_escape_windows_cmd:

tools.escape_windows_cmd()
--------------------------

.. code-block:: python

    def escape_windows_cmd(command)

Useful to escape commands to be executed in a windows bash (msys2, cygwin etc).

- Adds escapes so the argument can be unpacked by ``CommandLineToArgvW()``.
- Adds escapes for *cmd.exe* so the argument survives to ``cmd.exe``'s substitutions.

Parameters:
    - **command** (Required): Command to execute.

.. _tools_sha1sum_sha256sum_md5sum:

tools.sha1sum(), sha256sum(), md5sum()
--------------------------------------

.. code-block:: python

    def def md5sum(file_path)
    def sha1sum(file_path)
    def sha256sum(file_path)

Return the respective hash or checksum for a file.

.. code-block:: python

    from conans import tools

    md5 = tools.md5sum("myfilepath.txt")
    sha1 = tools.sha1sum("myfilepath.txt")

Parameters:
    - **file_path** (Required): Path to the file.

.. _tools_md5:

tools.md5()
-----------

.. code-block:: python

    def md5(content)

Returns the MD5 hash for a string or byte object.

.. code-block:: python

    from conans import tools

    md5 = tools.md5("some string, not a file path")

Parameters:
    - **content** (Required): String or bytes to calculate its md5.

.. _tools_save:

tools.save()
------------

.. code-block:: python

    def save(path, content, append=False, encoding="utf-8")

Utility function to save files in one line. It will manage the open and close of the file and creating directories if necessary.

.. code-block:: python

    from conans import tools

    tools.save("otherfile.txt", "contents of the file")

Parameters:
    - **path** (Required): Path to the file.
    - **content** (Required): Content that should be saved into the file.
    - **append** (Optional, Defaulted to ``False``): If ``True``, it will append the content.
    - **encoding** (Optional, Defaulted to ``utf-8``): Specifies the output file text encoding.

.. _tools_load:

tools.load()
------------

.. code-block:: python

    def load(path, binary=False, encoding="auto")

Utility function to load files in one line. It will manage the open and close of the file, and load binary encodings. Returns the content of
the file.

.. code-block:: python

    from conans import tools

    content = tools.load("myfile.txt")

Parameters:
    - **path** (Required): Path to the file.
    - **binary** (Optional, Defaulted to ``False``): If ``True``, it reads the the file as binary code.
    - **encoding** (Optional, Defaulted to ``auto``): Specifies the input file text encoding. The ``auto`` value has a special
      meaning - perform the encoding detection by checking the BOM (byte order mask), if no BOM is present tries to use: ``utf-8``, ``cp1252``.
      The value is ignored in case of ``binary`` set to the ``True``.

.. _tools_mkdir_rmdir:

tools.mkdir(), tools.rmdir()
----------------------------

.. code-block:: python

    def mkdir(path)
    def rmdir(path)

Utility functions to create/delete a directory. The existence of the specified directory is checked, so ``mkdir()`` will do nothing if the
directory already exists and ``rmdir()`` will do nothing if the directory does not exists.

This makes it safe to use these functions in the ``package()`` method of a *conanfile.py* when ``no_copy_source=True``.

.. code-block:: python

    from conans import tools

    tools.mkdir("mydir") # Creates mydir if it does not already exist
    tools.mkdir("mydir") # Does nothing

    tools.rmdir("mydir") # Deletes mydir
    tools.rmdir("mydir") # Does nothing

Parameters:
    - **path** (Required): Path to the directory.

.. _tools_which:

tools.which()
-------------

.. code-block:: python

    def which(filename)

Returns the path to a specified executable searching in the ``PATH`` environment variable. If not found, it returns ``None``.

This tool also looks for filenames with following extensions if no extension provided:

- ``.com``, ``.exe``, ``.bat`` ``.cmd`` for Windows.
- ``.sh`` if not Windows.

.. code-block:: python

    from conans import tools

    abs_path_make = tools.which("make")

Parameters:
    - **filename** (Required): Name of the executable file. It doesn't require the extension of the executable.

.. _tools_unix2dos:

tools.unix2dos()
----------------

.. code-block:: python

    def unix2dos(filepath)

Converts line breaks in a text file from Unix format (LF) to DOS format (CRLF).

.. code-block:: python

    from conans import tools

    tools.unix2dos("project.dsp")

Parameters:
    - **filepath** (Required): The file to convert.

.. _tools_dos2unix:

tools.dos2unix()
----------------

.. code-block:: python

    def dos2unix(filepath)

Converts line breaks in a text file from DOS format (CRLF) to Unix format (LF).

.. code-block:: python

    from conans import tools

    tools.dos2unix("dosfile.txt")

Parameters:
    - **filepath** (Required): The file to convert.

.. tools_tocuh:

tools.touch()
-------------

.. code-block:: python

    def touch(fname, times=None)

Updates the timestamp (last access and last modification times) of a file. This is similar to Unix' ``touch`` command except that this one
fails if the file does not exist.

Optionally, a tuple of two numbers can be specified, which denotes the new values for the last access and last modified times respectively.

.. code-block:: python

    from conans import tools
    import time

    tools.touch("myfile")                            # Sets atime and mtime to the current time
    tools.touch("myfile", (time.time(), time.time()) # Similar to above
    tools.touch("myfile", (time.time(), 1))          # Modified long, long ago

Parameters:
    - **fname** (Required): File name of the file to be touched.
    - **times** (Optional, Defaulted to ``None``: Tuple with 'last access' and 'last modified' times.

.. _tools_relative_dirs:

tools.relative_dirs()
---------------------

.. code-block:: python

    def relative_dirs(path)

Recursively walks a given directory (using ``os.walk()``) and returns a list of all contained file paths relative to the given directory.

.. code-block:: python

    from conans import tools

    tools.relative_dirs("mydir")

Parameters:
    - **path** (Required): Path of the directory.

.. _tools_vswhere:

tools.vswhere()
---------------

.. code-block:: python

    def vswhere(all_=False, prerelease=False, products=None, requires=None, version="",
                latest=False, legacy=False, property_="", nologo=True)

Wrapper of ``vswhere`` tool to look for details of Visual Studio installations. Its output is always a list with a dictionary for each
installation found.

.. code-block:: python

    from conans import tools

    vs_legacy_installations = tool.vswhere(legacy=True)

Parameters:
    - **all_** (Optional, Defaulted to ``False``): Finds all instances even if they are incomplete and may not launch.
    - **prerelease** (Optional, Defaulted to ``False``): Also searches prereleases. By default, only releases are searched.
    - **products** (Optional, Defaulted to ``None``): List of one or more product IDs to find. Defaults to Community, Professional, and
      Enterprise. Specify ``["*"]`` by itself to search all product instances installed.
    - **requires** (Optional, Defaulted to ``None``): List of one or more workload or component IDs required when finding instances. See
      https://docs.microsoft.com/en-us/visualstudio/install/workload-and-component-ids?view=vs-2017 listing all workload and component IDs.
    - **version** (Optional, Defaulted to ``""``): A version range of instances to find. Example: ``"[15.0,16.0)"`` will find versions 15.*.
    - **latest** (Optional, Defaulted to ``False``): Return only the newest version and last installed.
    - **legacy** (Optional, Defaulted to ``False``): Also searches Visual Studio 2015 and older products. Information is limited. This
      option cannot be used with either ``products`` or ``requires`` parameters.
    - **property_** (Optional, Defaulted to ``""``): The name of a property to return. Use delimiters ``.``, ``/``, or ``_`` to separate
      object and property names. Example: ``"properties.nickname"`` will return the "nickname" property under "properties".
    - **nologo** (Optional, Defaulted to ``True``): Do not show logo information.

.. _tools_vs_comntools:

tools.vs_comntools()
--------------------

.. code-block:: python

    def vs_comntools(compiler_version)

Returns the value of the environment variable ``VS<compiler_version>.0COMNTOOLS`` for the compiler version indicated.

.. code-block:: python

    from conans import tools

    vs_path = tools.vs_comntools("14")

Parameters:
    - **compiler_version** (Required): String with the version number: ``"14"``, ``"12"``...

.. tools_vs_installation_path:

tools.vs_installation_path()
----------------------------

.. code-block:: python

    def vs_installation_path(version, preference=None)

Returns the Visual Studio installation path for the given version. It uses :ref:`tools_vswhere` and :ref:`tools_vs_comntools`. It will also
look for the installation paths following :ref:`env_vars_conan_vs_installation_preference` environment variable or the preference parameter
itself. If the tool is not able to return the path it will return ``None``.

.. code-block:: python

    from conans import tools

    vs_path_2017 = tools.vs_installation_path("15", preference=["Community", "BuildTools", "Professional", "Enterprise"])

Parameters:
    - **version** (Required): Visual Studio version to locate. Valid version numbers are strings: ``"10"``, ``"11"``, ``"12"``, ``"13"``,
      ``"14"``, ``"15"``...
    - **preference** (Optional, Defaulted to ``None``): Set to value of :ref:`env_vars_conan_vs_installation_preference` or defaulted to
      ``["Enterprise", "Professional", "Community", "BuildTools"]``. If only set to one type of preference, it will return the installation
      path only for that Visual type and version, otherwise ``None``.

.. _tools_replace_prefix_in_pc_file:

tools.replace_prefix_in_pc_file()
---------------------------------

.. code-block:: python

    def replace_prefix_in_pc_file(pc_file, new_prefix)

Replaces the ``prefix`` variable in a package config file *.pc* with the specified value.

.. code-block:: python

    from conans import tools

    lib_b_path = self.deps_cpp_info["libB"].rootpath
    tools.replace_prefix_in_pc_file("libB.pc", lib_b_path)

**Parameters:**
    - **pc_file** (Required): Path to the pc file
    - **new_prefix** (Required): New prefix variable value (Usually a path pointing to a package).

.. seealso::

    Check section :ref:`pc_files` to know more.

.. _tools_collect_libs:

tools.collect_libs()
--------------------

.. code-block:: python

    def collect_libs(conanfile, folder=None)

Returns a sorted list of library names from the libraries (files with extensions *.so*, *.lib*, *.a* and *.dylib*) located inside the
``conanfile.cpp_info.libdirs`` (by default) or the **folder** directory relative to the package folder. Useful to collect not
inter-dependent libraries or with complex names like ``libmylib-x86-debug-en.lib``.

.. code-block:: python

    from conans import tools

    def package_info(self):
        self.cpp_info.libdirs = ["lib", "other_libdir"]  # Deafult value is 'lib'
        self.cpp_info.libs = tools.collect_libs(self)

For UNIX libraries staring with **lib**, like *libmath.a*, this tool will collect the library name **math**.

**Parameters:**
    - **conanfile** (Required): A ``ConanFile`` object to get the ``package_folder`` and ``cpp_info``.
    - **folder** (Optional, Defaulted to ``None``): String indicating the subfolder name inside ``conanfile.package_folder`` where
      the library files are.

.. warning::

    This tool collects the libraries searching directly inside the package folder and returns them in no specific order. If libraries are
    inter-dependent, then ``package_info()`` method should order them to achieve correct linking order.

.. _tools_pkgconfig:

tools.PkgConfig()
-----------------

.. code-block:: python

    class PkgConfig(library, pkg_config_executable="pkg-config", static=False, msvc_syntax=False, variables=None, print_errors=True)

Wrapper of the ``pkg-config`` tool.

.. code-block:: python

    from conans import tools

    with environment_append({'PKG_CONFIG_PATH': tmp_dir}):
        pkg_config = PkgConfig("libastral")
        print(pkg_config.cflags)
        print(pkg_config.cflags_only_I)
        print(pkg_config.variables)

Parameters of the constructor:
    - **library** (Required): Library (package) name, such as ``libastral``.
    - **pkg_config_executable** (Optional, Defaulted to ``"pkg-config"``): Specify custom pkg-config executable (e.g., for
      cross-compilation).
    - **static** (Optional, Defaulted to ``False``): Output libraries suitable for static linking (adds ``--static`` to ``pkg-config``
      command line).
    - **msvc_syntax** (Optional, Defaulted to ``False``): MSVC compatibility (adds ``--msvc-syntax`` to ``pkg-config`` command line).
    - **variables** (Optional, Defaulted to ``None``): Dictionary of pkg-config variables (passed as
      ``--define-variable=VARIABLENAME=VARIABLEVALUE``).
    - **print_errors** (Optional, Defaulted to ``True``): Output error messages (adds --print-errors)

**Properties:**

+-----------------------------+---------------------------------------------------------------------+
| PROPERTY                    | DESCRIPTION                                                         |
+=============================+=====================================================================+
| .cflags                     | get all pre-processor and compiler flags                            |
+-----------------------------+---------------------------------------------------------------------+
| .cflags_only_I              | get -I flags                                                        |
+-----------------------------+---------------------------------------------------------------------+
| .cflags_only_other          | get cflags not covered by the cflags-only-I option                  |
+-----------------------------+---------------------------------------------------------------------+
| .libs                       | get all linker flags                                                |
+-----------------------------+---------------------------------------------------------------------+
| .libs_only_L                | get -L flags                                                        |
+-----------------------------+---------------------------------------------------------------------+
| .libs_only_l                | get -l flags                                                        |
+-----------------------------+---------------------------------------------------------------------+
| .libs_only_other            | get other libs (e.g., -pthread)                                     |
+-----------------------------+---------------------------------------------------------------------+
| .provides                   | get which packages the package provides                             |
+-----------------------------+---------------------------------------------------------------------+
| .requires                   | get which packages the package requires                             |
+-----------------------------+---------------------------------------------------------------------+
| .requires_private           | get packages the package requires for static linking                |
+-----------------------------+---------------------------------------------------------------------+
| .variables                  | get list of variables defined by the module                         |
+-----------------------------+---------------------------------------------------------------------+

.. _tools_git:

tools.Git()
-----------

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

.. code-block:: python

    class Git(folder=None, verify_ssl=True, username=None, password=None,
              force_english=True, runner=None):

Wrapper of the ``git`` tool.

Parameters of the constructor:
    - **folder** (Optional, Defaulted to ``None``): Specify a subfolder where the code will be cloned. If not specified it will clone in the
      current directory.
    - **verify_ssl** (Optional, Defaulted to ``True``): Verify SSL certificate of the specified **url**.
    - **username** (Optional, Defaulted to ``None``): When present, it will be used as the login to authenticate with the remote.
    - **password** (Optional, Defaulted to ``None``): When present, it will be used as the password to authenticate with the remote.
    - **force_english** (Optional, Defaulted to ``True``): The encoding of the tool will be forced to use ``en_US.UTF-8`` to ease the output
      parsing.
    - **runner** (Optional, Defaulted to ``None``): By default ``subprocess.check_output`` will be used to invoke the ``git`` tool.

Methods:
    - **run(command)**: Run any "git" command, e.g., ``run("status")``
    - **get_url_with_credentials(url)**: Returns the passed URL but containing the ``username`` and ``password`` in the URL to authenticate
      (only if ``username`` and ``password`` is specified)
    - **clone(url, branch=None, args="", shallow=False)**: Clone a repository. Optionally you can specify a branch. Note: If you want to clone a repository and the
      specified **folder** already exist you have to specify a ``branch``. Additional ``args`` may be specified (e.g. git config variables). Use ``shallow`` to
      perform a shallow clone (with `--depth 1` - only last revision is being cloned, such clones are usually done faster and take less disk space). In this case,
      ``branch`` may specify any valid git reference - e.g. branch name, tag name, sha256 of the revision, expression like `HEAD~1` or `None` (default branch,
      e.g. `master`).
    - **checkout(element, submodule=None)**: Checkout a branch, commit or tag given by ``element``. Argument ``submodule`` can get values in
      ``shallow`` or ``recursive`` to instruct what to do with submodules.
    - **get_remote_url(remote_name=None)**: Returns the remote URL of the specified remote. If not ``remote_name`` is specified ``origin``
      will be used.
    - **get_qualified_remote_url()**: Returns the remote url (see ``get_remote_url()``) but with forward slashes if it is a local folder.
    - **get_revision(), get_commit()**: Gets the current commit hash.
    - **get_branch()**: Gets the current branch.
    - **get_tag()**: Gets the current checkout tag (:command:`git describe --exact-match --tags`) and returns ``None`` if not in a tag.
    - **excluded_files()**: Gets a list of the files and folders that would be excluded by *.gitignore* file.
    - **is_local_repository()**: Returns `True` if the remote is a local folder.
    - **is_pristine()**: Returns `True` if there aren't modified or uncommitted files in the working copy.
    - **get_repo_root()**: Returns the root folder of the working copy.
    - **get_commit_message()**: Returns the latest log message

.. _tools_svn:

tools.SVN()
-----------

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

.. code-block:: python

    class SVN(folder=None, verify_ssl=True, username=None, password=None,
              force_english=True, runner=None):

Wrapper of the ``svn`` tool.

Parameters of the constructor:
    - **folder** (Optional, Defaulted to ``None``): Specify a subfolder where the code will be cloned. If not specified it will clone in the
      current directory.
    - **verify_ssl** (Optional, Defaulted to ``True``): Verify SSL certificate of the specified **url**.
    - **username** (Optional, Defaulted to ``None``): When present, it will be used as the login to authenticate with the remote.
    - **password** (Optional, Defaulted to ``None``): When present, it will be used as the password to authenticate with the remote.
    - **force_english** (Optional, Defaulted to ``True``): The encoding of the tool will be forced to use ``en_US.UTF-8`` to ease the output
      parsing.
    - **runner** (Optional, Defaulted to ``None``): By default ``subprocess.check_output`` will be used to invoke the ``svn`` tool.

Methods:
    - **version()**: Retrieve version from the installed SVN client.
    - **run(command)**: Run any "svn" command, e.g., ``run("status")``
    - **get_url_with_credentials(url)**: Return the passed url but containing the ``username`` and ``password`` in the URL to authenticate
      (only if ``username`` and ``password`` is specified)
    - **checkout(url, revision="HEAD")**: Checkout the revision number given by ``revision`` from the specified ``url``.
    - **update(revision="HEAD")**: Update working copy to revision number given by ``revision``.
    - **get_remote_url()**: Returns the remote url of working copy.
    - **get_qualified_remote_url()**: Returns the remote url of the working copy with the
      `peg revision <http://svnbook.red-bean.com/en/1.7/svn.advanced.pegrevs.html>`_ appended to it.
    - **get_revision()**: Gets the current revision number from the repo server.
    - **get_last_changed_revision(use_wc_root=True)**: Returns the revision number corresponding to the last changed item in the working
      folder (``use_wc_root=False``) or in the working copy root (``use_wc_root=True``).
    - **get_branch()**: Tries to deduce the branch name from the
      `standard SVN layout <http://svnbook.red-bean.com/en/1.7/svn.branchmerge.maint.html>`_. Will raise if cannot resolve it.
    - **get_tag()**: Tries to deduce the tag name from the `standard SVN layout <http://svnbook.red-bean.com/en/1.7/svn.branchmerge.maint.html>`_ and
      returns the current tag name. Otherwise it will return ``None``.
    - **excluded_files()**: Gets a list of the files and folders that are marked to be ignored.
    - **is_local_repository()**: Returns `True` if the remote is a local folder.
    - **is_pristine()**: Returns `True` if there aren't modified or uncommitted files in the working copy.
    - **get_repo_root()**: Returns the root folder of the working copy.
    - **get_revision_message()**: Returns the latest log message


.. warning::

    SVN allows to checkout a subdirectory of the remote repository, take into account that the return value of some of these functions may
    depend on the root of the working copy that has been checked out.

.. _tools_is_apple_os:

tools.is_apple_os()
-------------------

.. code-block:: python

    def is_apple_os(os_)

Returns ``True`` if OS is an Apple one: macOS, iOS, watchOS or tvOS.

Parameters:
    - **os_** (Required): OS to perform the check. Usually this would be ``self.settings.os``.

.. _tools_to_apple_arch:

tools.to_apple_arch()
---------------------

.. code-block:: python

    def to_apple_arch(arch)

Converts Conan style architecture into Apple style architecture.

Parameters:
    - **arch** (Required): arch to perform the conversion. Usually this would be ``self.settings.arch``.

.. _tools_apple_sdk_name:

tools.apple_sdk_name()
----------------------

.. code-block:: python

    def apple_sdk_name(settings)

Returns proper SDK name suitable for OS and architecture you are building for (considering simulators).

Parameters:
    - **settings** (Required): Conanfile settings.


.. _tools_apple_deployment_target_env:

tools.apple_deployment_target_env()
-----------------------------------

.. code-block:: python

    def apple_deployment_target_env(os_, os_version)

Environment variable name which controls deployment target: ``MACOSX_DEPLOYMENT_TARGET``, ``IOS_DEPLOYMENT_TARGET``,
``WATCHOS_DEPLOYMENT_TARGET`` or ``TVOS_DEPLOYMENT_TARGET``.

Parameters:
    - **os_** (Required): OS of the settings. Usually ``self.settings.os``.
    - **os_version** (Required): OS version.

.. _tools_apple_deployment_target_flag:

tools.apple_deployment_target_flag()
------------------------------------

.. code-block:: python

    def apple_deployment_target_flag(os_, os_version)

Compiler flag name which controls deployment target. For example: ``-mappletvos-version-min=9.0``

Parameters:
    - **os_** (Required): OS of the settings. Usually ``self.settings.os``.
    - **os_version** (Required): OS version.

.. _tools_xcrun:

tools.XCRun()
-------------

.. code-block:: python

    class XCRun(object):

        def __init__(self, settings, sdk=None):

XCRun wrapper used to get information for building.

Properties:
    - **sdk_path**: Obtain SDK path (a.k.a. Apple sysroot or -isysroot).
    - **sdk_version**: Obtain SDK version.
    - **sdk_platform_path**: Obtain SDK platform path.
    - **sdk_platform_version**: Obtain SDK platform version.
    - **cc**: Path to C compiler (CC).
    - **cxx**: Path to C++ compiler (CXX).
    - **ar**: Path to archiver (AR).
    - **ranlib**: Path to archive indexer (RANLIB).
    - **strip**: Path to symbol removal utility (STRIP).

.. _tools_latest_vs_version_installed:

tools.latest_vs_version_installed()
-----------------------------------

.. code-block:: python

    def latest_vs_version_installed()

Returns a string with the major version of latest Microsoft Visual Studio available on machine. If no Microsoft Visual Studio installed,
it returns ``None``.

.. _tools.apple_dot_clean:

tools.apple_dot_clean()
-----------------------

.. code-block:: python

    def apple_dot_clean(folder)

Remove recursively all ``._`` files inside ``folder``, these files are created by Apple OS when the
underlying filesystem cannot store metadata associated to files (they could appear when unzipping
a file that has been created in Macos). This tool will remove only the ``._`` files that are
accompanied with a file without that prefix (it will remove ``._file.txt`` only
if ``file.txt`` exists).

Parameters:
    - **folder** (Required): root folder to start deleting ``._`` files.

.. _tools_version:

tools.Version()
---------------

.. code-block:: python

    from conans import tools

    v = tools.Version("1.2.3-dev23")
    assert v < "1.2.3"

This is a helper class to work with semantic versions, built on top of ``semver.SemVer`` class
with loose parsing. It exposes all the version components as properties and offers total
ordering through compare operators.

Build the ``tools.Version`` object using any valid string or any object that converts to
string, the constructor will raise if the string is not a valid loose semver.

Properties:
   - **major**: component ``major`` of semver version
   - **minor**: component ``minor`` of semver version (defaults to ``"0"``)
   - **patch**: component ``patch`` of semver version (defaults to ``"0"``)
   - **prerelease**: component ``prerelease`` of semver version (defaults to ``""``)
   - **build**: component ``build`` of semver version (defaults to ``""``). Take into account
     that ``build`` component doesn't affect precedence between versions.

.. _tools.to_android_abi:

tools.to_android_abi()
----------------------

.. code-block:: python

    def to_android_abi(arch)

Converts Conan style architecture into Android NDK style architecture.

Parameters:
    - **arch** (Required): Arch to perform the conversion. Usually this would be ``self.settings.arch``.

.. _tools.check_min_cppstd:

tools.check_min_cppstd()
------------------------

.. code-block:: python

    def check_min_cppstd(conanfile, cppstd, gnu_extensions=False)

Validates if the applied cppstd setting (from `compiler.cppstd` settings or deducing the default from `compiler` and `compiler.version`) is at least the value specified in the `cppstd` argument.
It raises a ``ConanInvalidConfiguration`` when is not supported.

.. code-block:: python

    from conans import tools, ConanFile

    class Recipe(ConanFile):
        ...

        def configure(self):
            tools.check_min_cppstd(self, "17")

* If the current cppstd does not support C++17, ``check_min_cppstd`` will raise an ``ConanInvalidConfiguration`` error.
* If ``gnu_extensions`` is True, it is required that the applied ``cppstd`` supports the gnu extensions.
  (e.g. gnu17), otherwise, an :ref:`ConanInvalidConfiguration<conditional_settings_options_requirements>` will be raised. The ``gnu_extensions`` is checked in any OS.

Parameters:
    - **conanfile** (Required): ConanFile instance. Usually ``self``.
    - **cppstd** (Required): C++ standard version which must be supported.
    - **gnu_extensions** (Optional): GNU extension is required.

.. _tools.valid_min_cppstd:

tools.valid_min_cppstd()
------------------------

.. code-block:: python

    def valid_min_cppstd(conanfile, cppstd, gnu_extensions=False)

Validate the current cppstd from settings or compiler, if it is supported by the required cppstd version.
It returns ``True`` when is valid, otherwise, ``False``.

.. code-block:: python

    from conans import tools, ConanFile

    class Recipe(ConanFile):
        ...

        def configure(self):
            if not tools.valid_min_cppstd(self, "17"):
                self.output.error("C++17 is required.")

* The ``valid_min_cppstd`` works exactly like ``check_min_cppstd``, however, it does not raise ``ConanInvalidConfiguration`` error.

Parameters:
    - **conanfile** (Required): ConanFile instance. Usually ``self``.
    - **cppstd** (Required): C++ standard version which must be supported.
    - **gnu_extensions** (Optional): GNU extension is required.
