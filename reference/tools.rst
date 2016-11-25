.. _tools:


Tools
=====

Under the tools module there are several functions and utilities that can be used in conan package
recipes


vcvars_command()
----------------

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

    
unzip()
-------

Function mainly used in ``source()``, but could be used in ``build()`` in special cases, as
when retrieving pre-built binaries from the Internet.

This function accepts ``.tar.gz``, ``.tar``, ``.tzb2``, ``.tar.bz2``, ``.tgz`` and ``.zip`` files, 
and decompress them into the given destination folder (the current one by default).

.. code-block:: python

    from conans import tools
    
    tools.unzip("myfile.zip")
    # or to extract in "myfolder" sub-folder
    tools.unzip("myfile.zip", "myfolder")

    
untargz()
---------
Extract tar gz files (or in the family). This is the function called by the previous ``unzip()``
for the matching extensions, so generally not needed to be called directly, call ``unzip()`` instead
unless the file had a different extension.

.. code-block:: python

    from conans import tools
    
    tools.untargz("myfile.tar.gz")
    # or to extract in "myfolder" sub-folder
    tools.untargz("myfile.tar.gz", "myfolder")

get()
-----
Just a high level wrapper for download, unzip, and remove the temporary zip file once unzipped. Its implementation
is very straightforward:

.. code-block:: python

    def get(url):
        filename = os.path.basename(url)
        download(url, filename)
        unzip(filename)
        os.unlink(filename)


download()
----------
Retrieves a file from a given URL into a file with a given filename. It uses certificates from a
list of known verifiers for https downloads, but this can be optionally disabled.

.. code-block:: python

    from conans import tools
    
    tools.download("http://someurl/somefile.zip", "myfilename.zip")
    # to disable verification:
    tools.download("http://someurl/somefile.zip", "myfilename.zip", verify=False)
    
    
replace_in_file()
-----------------

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

check_with_algorithm_sum()
--------------------------

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


patch()
-------

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

environment_append()
--------------------

This is a context manager that allows to temporary use environment variables for a specific piece of code
in your conanfile:


.. code-block:: python

    from conans import tools
    
    def build(self):
        with tools.environment_append({"MY_VAR": "3", "CXX": "/path/to/cxx"}):
            do_something()

When the context manager block ends, the environment variables will be unset.


build_sln_command()
-------------------

Returns the command to call `devenv` and `msbuild` to build a Visual Studio project.
It's recommended to use it along with ConfigureEnvironment, so that the Visual Studio tools 
will be in path.

.. code-block:: python

  
    build_command = build_sln_command(self.settings, "myfile.sln", targets=["SDL2_image"])
    env = ConfigureEnvironment(self)
    command = "%s && %s" % (env.command_line_env, build_command)
    self.run(command)

Arguments:

 * **settings**  Conanfile settings, pass "self.settings"
 * **sln_path**  Visual Studio project file path
 * **targets**   List of targets to build
 * **upgrade_project** True/False. If True, the project file will be upgraded if the project's VS version is older than current


pythonpath()
------------
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

  
human_size()
------------

Will return a string from a given number of bytes, rounding it to the most appropriate unit: Gb, Mb, Kb, etc.
It is mostly used by the conan downloads and unzip progress, but you can use it if you want too.

.. code-block:: python

    from conans import tools
    
    tools.human_size(1024)
    >> 1Kb

    
OSInfo and SystemPackageTool
----------------------------
These are helpers to install system packages. Check :ref:`system_requirements`







