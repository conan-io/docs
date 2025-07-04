.. _conanfile_txt_reference:

conanfile.txt
=============

Sections
--------

[requires]
__________

List of requirements, specifing the full reference.


.. code-block:: text

    [requires]
    Poco/1.9.0@pocoproject/stable
    zlib/1.2.11@conan/stable


Also support :ref:`version ranges<version_ranges>`:


.. code-block:: text

    [requires]
    Poco/[>1.0,<1.8]@pocoproject/stable
    zlib/1.2.11@conan/stable

[build_requires]
________________

List of build requirements, specifing the full reference.


.. code-block:: text

    [build_requires]
    7z_installer/1.0@conan/stable

Also support :ref:`version ranges<version_ranges>`

In practice the ``[build_requires]`` will be always installed, the same as ``[requires]``.
Installing from a *conanfile.txt* means that something is going to be built, so the build
requirements are indeed needed.

Still, it is useful and conceptually cleaner to have them in separate sections, so users of
this *conanfile.txt* might quickly identify some dev-tools that they have already installed
on their machine, differentiating them from the required libraries to link with.


[generators]
____________

List of :ref:`generators<generators_reference>`


.. code-block:: text

    [requires]
    Poco/1.9.0@pocoproject/stable
    zlib/1.2.11@conan/stable

    [generators]
    xcode
    cmake
    qmake


[options]
_________


List of :ref:`options<options_txt>`. Always specifying **package_name:option = Value**


.. code-block:: text

    [requires]
    Poco/1.9.0@pocoproject/stable
    zlib/1.2.11@conan/stable

    [generators]
    cmake

    [options]
    Poco:shared=True
    OpenSSL:shared=True


[imports]
_________

List of files to be imported to a local directory. Read more: :ref:`imports<imports_txt>`.


.. code-block:: text

    [requires]
    Poco/1.9.0@pocoproject/stable
    zlib/1.2.11@conan/stable

    [generators]
    cmake

    [options]
    Poco:shared=True
    OpenSSL:shared=True

    [imports]
    bin, *.dll -> ./bin # Copies all dll files from packages bin folder to my local "bin" folder
    lib, *.dylib* -> ./bin # Copies all dylib files from packages lib folder to my local "bin" folder

The first item is the subfolder of the packages (could be the root "." one), the second is the pattern to match. Both relate to the local
cache. The third (after the arrow) item, is the destination folder, living in user space, not in the local cache.

The ``[imports]`` section also support the same arguments as the equivalent ``imports()`` method in *conanfile.py*, separated with an ``@``.

- **root_package** (Optional, Defaulted to *all packages in deps*): fnmatch pattern of the package name ("OpenCV", "Boost") from which files
  will be copied.
- **folder**: (Optional, Defaulted to ``False``). If enabled, it will copy the files from the local cache to a subfolder named as the
  package containing the files. Useful to avoid conflicting imports of files with the same name (e.g. License).
- **ignore_case**: (Optional, Defaulted to ``False``). If enabled will do a case-insensitive pattern matching.
- **excludes**: (Optional, Defaulted to ``None``). Allows defining a list of patterns (even a single pattern) to be excluded from the copy,
  even if they match the main ``pattern``.
- **keep_path** (Optional, Defaulted to ``True``): Means if you want to keep the relative path when you copy the files from the **src**
  folder to the **dst** one. Useful to ignore (``keep_path=False``) path of *library.dll* files in the package it is imported from.

Example to collect license files from dependencies, into a *licenses* folder, excluding (just an example) html and jpeg files:

.. code-block:: text

    [imports]
    ., license* -> ./licenses @ folder=True, ignore_case=True, excludes=*.html *.jpeg

