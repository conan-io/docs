.. _conanfile_txt_reference:

conanfile.txt
=============

Reference for *conanfile.txt* sections: requires, generators, etc.

Sections
--------

[requires]
++++++++++

List of requirements, specifying the full reference.

.. code-block:: text

    [requires]
    poco/1.9.4
    zlib/1.2.11


This section supports references with :ref:`version ranges<version_ranges>`:

.. code-block:: text

    [requires]
    poco/[>1.0,<1.9]
    zlib/1.2.11

[build_requires]
++++++++++++++++

List of build requirements specifying the full reference.

.. code-block:: text

    [build_requires]
    7zip/16.00

This section supports references with :ref:`version ranges<version_ranges>`.

In practice the ``[build_requires]`` will be always installed (same as ``[requires]``) as installing from a *conanfile.txt* means that
something is going to be built, so the build requirements are indeed needed.

It is useful and conceptually cleaner to have them in separate sections, so users of this *conanfile.txt* might quickly identify some
dev-tools that they have already installed on their machine, differentiating them from the required libraries to link with.

[generators]
++++++++++++

List of :ref:`generators<generators_reference>`.

.. code-block:: text

    [requires]
    poco/1.9.4
    zlib/1.2.11

    [generators]
    xcode
    cmake
    qmake

[options]
+++++++++

List of :ref:`options<options_txt>` scoped for each package like **package_name:option = Value**.

.. code-block:: text

    [requires]
    poco/1.9.4
    zlib/1.2.11

    [generators]
    cmake

    [options]
    poco:shared=True
    openssl:shared=True

[imports]
+++++++++

List of files to be imported to a local directory. Read more: :ref:`imports<imports_txt>`.

.. code-block:: text

    [requires]
    poco/1.9.4
    zlib/1.2.11

    [generators]
    cmake

    [options]
    poco:shared=True
    openssl:shared=True

    [imports]
    bin, *.dll -> ./bin # Copies all dll files from packages bin folder to my local "bin" folder
    lib, *.dylib* -> ./bin # Copies all dylib files from packages lib folder to my local "bin" folder

The first item is the subfolder of the packages (could be the root "." one), the second is the pattern to match. Both relate to the local
cache. The third (after the arrow) item, is the destination folder, living in user space, not in the local cache.

The ``[imports]`` section also support the same arguments as the equivalent ``imports()`` method in *conanfile.py*, separated with an ``@``.

.. note::

    If your previous folders use an ``@`` in the path name, use a trailing (even if empty) ``@`` so the parser correctly gets the folders paths,
    e.g: ``lib, * -> /home/jenkins/workspace/conan_test@2/g/install/lib @``


- **root_package** (Optional, Defaulted to *all packages in deps*): fnmatch pattern of the package name ("OpenCV", "Boost") from which files
  will be copied.
- **folder**: (Optional, Defaulted to ``False``). If enabled, it will copy the files from the local cache to a subfolder named as the
  package containing the files. Useful to avoid conflicting imports of files with the same name (e.g. License).
- **ignore_case**: (Optional, Defaulted to ``False``). If enabled will do a case-insensitive pattern matching.
- **excludes**: (Optional, Defaulted to ``None``). Allows defining a list of patterns (even a single pattern) to be excluded from the copy,
  even if they match the main ``pattern``.
- **keep_path** (Optional, Defaulted to ``True``): Means if you want to keep the relative path when you copy the files from the **src**
  folder to the **dst** one. Useful to ignore (``keep_path=False``) path of *library.dll* files in the package it is imported from.

Example to collect license files from dependencies into a *licenses* folder, excluding (just an example) *.html* and *.jpeg* files:

.. code-block:: text

    [imports]
    ., license* -> ./licenses @ folder=True, ignore_case=True, excludes=*.html *.jpeg

Comments
++++++++

A comment starts with a hash character (`#`) and ends at the end of the physical line.
Comments are ignored by the syntax; they are not tokens.
