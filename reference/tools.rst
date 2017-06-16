.. _tools:


Tools
=====

Under the tools module there are several functions and utilities that can be used in conan package
recipes:

.. code-block:: python
   :emphasize-lines: 2

    from conans import ConanFile
    from conans import tools

    class ExampleConan(ConanFile):
        ...


.. _cpu_count:

tools.cpu_count()
-----------------
Returns the number of CPUs available, for parallel builds. If processor detection is not enabled, it will safely return 1.
Can be overwritten with the environment variable ``CONAN_CPU_COUNT`` and configured in the :ref:`conan.conf file<conan_conf>`.


tools.vcvars_command()
----------------------

This function returns, for given settings, the command that should be called to load the Visual
Studio environment variables for a certain Visual Studio version. It does not execute
the command, as that typically have to be done in the same command as the compilation,
so the variables are loaded for the same subprocess. It will be typically used in the ``build()``
method, like this:

.. code-block:: python

    from conans import tools
    
    def build(self):
        if self.settings.os == "Windows":
            vcvars = tools.vcvars_command(self.settings)    
            build_command = ...
            self.run("%s && configure %s" % (vcvars, " ".join(args)))
            self.run("%s && %s %s" % (vcvars, build_command, " ".join(build_args)))

The ``vcvars_command`` string will contain something like ``call "%vsXX0comntools%../../VC/vcvarsall.bat"`` for the
corresponding Visual Studio version for the current settings.

This is typically not needed if using ``CMake``, as the cmake generator will handle the correct
Visual Studio version.


.. _build_sln_commmand:

tools.build_sln_command()
-------------------------

Returns the command to call `devenv` and `msbuild` to build a Visual Studio project.
It's recommended to use it along with ``vcvars_command()``, so that the Visual Studio tools will be in path.

.. code-block:: python

    build_command = build_sln_command(self.settings, "myfile.sln", targets=["SDL2_image"])
    command = "%s && %s" % (tools.vcvars_command(self.settings), build_command)
    self.run(command)

Arguments:

 * **settings**  Conanfile settings, pass "self.settings"
 * **sln_path**  Visual Studio project file path
 * **targets**   List of targets to build
 * **upgrade_project** True/False. If True, the project file will be upgraded if the project's VS version is older than current


.. _msvc_build_command:

tools.msvc_build_command()
------------------------------

Returns a string with a joint command consisting in setting the environment variables via ``vcvars.bat`` with the above ``tools.vcvars_command()`` function, and building a Visual Studio project with the ``tools.build_sln_command()`` function.

Arguments:

    Exactly the same arguments as the above ``tools.build_sln_command()``


tools.unzip()
-------------

Function mainly used in ``source()``, but could be used in ``build()`` in special cases, as
when retrieving pre-built binaries from the Internet.

This function accepts ``.tar.gz``, ``.tar``, ``.tzb2``, ``.tar.bz2``, ``.tgz`` and ``.zip`` files, 
and decompress them into the given destination folder (the current one by default).

.. code-block:: python

    from conans import tools
    
    tools.unzip("myfile.zip")
    # or to extract in "myfolder" sub-folder
    tools.unzip("myfile.zip", "myfolder")


For the ``.zip`` files you can keep the permissions using the ``keep_permissions=True`` parameter.
WARNING: It can be dangerous if the zip file was not created in a NIX system, it could produce undefined permission schema.
So, use only this option if you are sure that the zip file was created correctly:

.. code-block:: python

    from conans import tools

    tools.unzip("myfile.zip", "myfolder", keep_permissions=True)



tools.untargz()
---------------

Extract tar gz files (or in the family). This is the function called by the previous ``unzip()``
for the matching extensions, so generally not needed to be called directly, call ``unzip()`` instead
unless the file had a different extension.

.. code-block:: python

    from conans import tools
    
    tools.untargz("myfile.tar.gz")
    # or to extract in "myfolder" sub-folder
    tools.untargz("myfile.tar.gz", "myfolder")

tools.get()
-----------

Just a high level wrapper for download, unzip, and remove the temporary zip file once unzipped. Its implementation
is very straightforward:

.. code-block:: python

    def get(url):
        filename = os.path.basename(url)
        download(url, filename)
        unzip(filename)
        os.unlink(filename)


tools.download()
----------------

Retrieves a file from a given URL into a file with a given filename. It uses certificates from a
list of known verifiers for https downloads, but this can be optionally disabled.
You can also specify the number of retries in case of fail with ``retry`` parameter and the seconds to wait before download attempts
with ``retry_wait``.

.. code-block:: python

    from conans import tools
    
    tools.download("http://someurl/somefile.zip", "myfilename.zip")
    # to disable verification:
    tools.download("http://someurl/somefile.zip", "myfilename.zip", verify=False)
    # to retry the download 2 times waiting 5 seconds between them
    tools.download("http://someurl/somefile.zip", "myfilename.zip", retry=2, retry_wait=5)



tools.ftp_download()
------------------------

Retrieves a file from an FTP server. Right now it doesn't support SSL, but you might implement it yourself using the standard python FTP library, and also if you need some special functionality.

``def ftp_download(ip, filename, login='', password='')``

- ip: The IP or address of the ftp server
- filename: The filename, including the path/folder where it is located
- login/password: optional credentials to the ftp server

Example: 

.. code-block:: python

    def source(self):
        tools.ftp_download('ftp.debian.org', "debian/README")
        self.output.info(load("README"))


tools.replace_in_file()
-----------------------

This function is useful for a simple "patch" or modification of source files. A typical use would
be to augment some library existing ``CMakeLists.txt`` in the ``source()`` method, so it uses
conan dependencies without forking or modifying the original project:

.. code-block:: python

    from conans import tools
    
    def source(self):
        # get the sources from somewhere
       tools.replace_in_file("hello/CMakeLists.txt", "PROJECT(MyHello)", '''PROJECT(MyHello)
    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()''')


tools.check_with_algorithm_sum()
--------------------------------

Useful to check that some downloaded file or resource has a predefined hash, so integrity and
security are guaranteed. Something that could be typically done in ``source()`` method after
retrieving some file from the internet.

There are specific methods for common algorithms:

- ``check_sha1(file_path, signature)``
- ``check_md5(file_path, signature)``
- ``check_sha256(file_path, signature)``

.. code-block:: python

    from conans import tools
    
    tools.check_sha1("myfile.zip", "eb599ec83d383f0f25691c184f656d40384f9435")

Other algorithms are also possible, as long as are recognized by python ``hashlib`` implementation,
via ``hashlib.new(algorithm_name)``. The previous is equivalent to:

.. code-block:: python

    from conans import tools

    tools.check_with_algorithm_sum("sha1", "myfile.zip",
                                    "eb599ec83d383f0f25691c184f656d40384f9435")


tools.patch()
-------------

Applies a patch from a file or from a string into the given path. The patch should be in diff (unified diff)
format. To be used mainly in the ``source()`` method.

.. code-block:: python

    from conans import tools

    tools.patch(patch_file="file.patch")
    # from a string:
    patch_content = " real patch content ..."
    tools.patch(patch_string=patch_content)
    # to apply in subfolder
    tools.patch(base_path=mysubfolder, patch_string=patch_content)
    
If the patch to be applied uses alternate paths that have to be stripped, like:

.. code-block:: diff

    --- old_path/text.txt\t2016-01-25 17:57:11.452848309 +0100
    +++ new_path/text_new.txt\t2016-01-25 17:57:28.839869950 +0100
    @@ -1 +1 @@
    - old content
    + new content

Then it can be done specifying the number of folders to be stripped from the path:

.. code-block:: diff

    patch(patch_file="file.patch", strip=1)


.. _environment_append_tool:

tools.environment_append()
--------------------------

This is a context manager that allows to temporary use environment variables for a specific piece of code
in your conanfile:


.. code-block:: python

    from conans import tools
    
    def build(self):
        with tools.environment_append({"MY_VAR": "3", "CXX": "/path/to/cxx"}):
            do_something()

When the context manager block ends, the environment variables will be unset.


tools.chdir()
-------------

This is a context manager that allows to temporary change the current directory in your conanfile:

.. code-block:: python

    from conans import tools

    def build(self):
        with tools.chdir("./subdir"):
            do_something()


tools.pythonpath()
------------------
This is a context manager that allows to load the PYTHONPATH for dependent packages, create packages
with python code, and reuse that code into your own recipes.

.. code-block:: python

    from conans import tools
    
    def build(self):
        with tools.pythonpath(self):
            from module_name import whatever
            whatever.do_something()
            
For that to work, one of the dependencies of the current recipe, must have a ``module_name``
file or folder with a ``whatever`` file or object inside, and should have declared in its
``package_info()``:

.. code-block:: python

    from conans import tools
    
    def package_info(self):
        self.env_info.PYTHONPATH.append(self.package_folder)

  
tools.human_size()
------------------

Will return a string from a given number of bytes, rounding it to the most appropriate unit: Gb, Mb, Kb, etc.
It is mostly used by the conan downloads and unzip progress, but you can use it if you want too.

.. code-block:: python

    from conans import tools
    
    tools.human_size(1024)
    >> 1Kb


.. _osinfo_reference:

    
tools.OSInfo and tools.SystemPackageTool
----------------------------------------
These are helpers to install system packages. Check :ref:`system_requirements`


.. _cross_building_reference:

tools.cross_building
--------------------

Reading the settings and the current host machine it returns True if we are cross building a conan package:

.. code-block:: python

    if tools.cross_building(self.settings):
        # Some special action



.. _run_in_windows_bash_tool:

tools.run_in_windows_bash
-------------------------

Runs an unix command inside the msys2 environment. It requires to have MSYS2 in the path.
Useful to build libraries using ``configure`` and ``make`` in Windows. Check :ref:`Building with Autotools <building_with_autotools>` section.

You can customize the path of the bash executable using the environment variable ``CONAN_BASH_PATH`` or the :ref:`conan.conf<conan_conf>` ``bash_path`` variable to change the default bash location.


.. code-block:: python

    from conans import tools

    command = "pwd"
    tools.run_in_windows_bash(self, command) # self is a conanfile instance


tools.unix_path
---------------

Used to translate Windows paths to MSYS/CYGWIN unix paths like c/users/path/to/file


tools.escape_windows_cmd
------------------------

Useful to escape commands to be executed in a windows bash (msys2, cygwin etc).

- Adds escapes so the argument can be unpacked by CommandLineToArgvW()
- Adds escapes for cmd.exe so the argument survives cmd.exe's substitutions.


tools.sha1sum(), sha256sum(), md5sum(), md5()
---------------------------------------------
Return the respective hash or checksum for a file:

.. code-block:: python

    sha1 = tools.sha1sum("myfilepath.txt")
    md5 = tools.md5("some string, not a file path")


tools.save(), tools.load()
----------------------------
Utility methods to load and save files, in one line. They will manage the open and close of the file, encodings and creating directories if necessary

.. code-block:: python

    content = tools.load("myfile.txt")
    tools.save("otherfile.txt", "contents of the file")
