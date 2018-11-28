Documentation for Conan C/C++ package manager: https://conan.io

[![Build Status](https://travis-ci.org/conan-io/docs.svg?branch=master)](https://travis-ci.org/conan-io/docs)

How to build
============

- Install python and [pip docs](https://pip.pypa.io/en/stable/installing/).
- Install the requirements (sphinx):

  `$ pip install -r requirements.txt`

- Build the documentation:

  `$ make html`

How to read the built docs
==========================

Open a browser and select the *_build/html/index.html* file.

Example:

`$ firefox _build/html/index.html`

How to contribute
=================

To make any contribution to Conan documentation fork this repository and open a Pull Request.

Style Guidelines
----------------

This guidelines are just general good practices for the formatting and structure of the whole documentation and do not pretend to be a
stopper for any helpful contribution. Any contribution that may include relevant information for Conan users will always be welcomed.

Conan documentation is written in [reStructuredText](http://docutils.sourceforge.net/rst.html) and
follows [reStructuredText Markup Specification](http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html).

[Quick reStructuredText](http://docutils.sourceforge.net/docs/user/rst/quickref.html) is also used for reference.

Any detail not covered by this guidelines will follow the aforementioned rules.

### Section titles

Use section titles in this level of importance:

```
Section Title
=============

Section Title
-------------

Section Title
+++++++++++++

Section Title
^^^^^^^^^^^^^
```

### Text emphasis/highlighting

- **Bold text** to highlight important text:

  ```
  Note the simple scenario of a **header-only** library. Such package...
  ```

- *Italics* to refer to file names, directory names and paths.

  ```
  If you have a look to the *test_package* folder, you will realize that the *example.cpp* and the *CMakeLists.txt* files don't have
  anything special. The *test_package/conanfile.py* file is...
  ```

- ``Command inline literals`` to refer to command line, both full commands and command line arguments, or any extract of a full command.
  ```
  To create a conan package you can use :command:`conan create`.  You can see a :command:`git clone` command... You may call it with the :command:`--keep-source` option to avoid deleting and fetching the source.
  ```

- ``Inline literals`` to refer to code or text inside recipes:

  ```
   ``package()`` -> conanfile.py method
   ``cmake`` -> generator in conanfile.txt
   ``settings`` -> variable inside a ConanFile class in conanfile.py
   ```

  Like this:

  ```
  Note that the ``build_id()`` method uses the ``self.info_build`` object to alter the build hash.
  ```

- Other names like CMake, Autotools, Conan, Visual Studio should not be emphasized, just use a capital letter or follow the convention (like
  first and second capitalized letters for CMake).

### code-blocks

Use code-blocks for code snippets or command line actions and follow the specific language
indentation. Documentation makes an extensive use of bash, python, txt and cmake code-blocks.

```
.. code-block:: python

    from conans import ConanFile

    class EigenConan(ConanFile)
        name = "eigen"
        version = "3.3.4"

        def source():
            tools.get("https://some_url.org")
            ...
```

```
.. code-block:: text

    [requires]
    Poco/1.7.8p3@pocoproject/stable
    zlib/1.2.11@conan/stable
```

```
.. code-block:: bash
   :emphasize-lines: 3

    $ conan source . --source-folder src
    $ conan install --install-folder build_x86 -s arch=x86
    $ conan build . --build-folder build_x86 --source-folder src
    $ conan export-pkg . Hello/0.1@user/stable --build-folder build_x86
```

### Indentation and line length

Make sure all indentation is done with spaces. Normally 2 space indentation for bulleted lists and 4 space indentation for code blocks. In some
cases a 3 space indentation is needed for reStructuredText specifics like toc-trees:

```
.. toctree::
   :maxdepth: 2

   creating_packages/getting_started
   creating_packages/package_repo
```

The **maximum line length for documentation is 140 characters** except for lines inside code-blocks, external links or references.

Do not leave any unnecessary or trailing spaces.

### Text boxes

Also called **Admonitions**, they are eye-catching texts with a clear purpose like warnings, tips or important content.

Use them in the following importance order:

1. caution
2. attention
3. warning
4. important
5. note
6. tip

```
.. warning::

    In the Bintray repositories there are binaries for several mainstream compilers...
```

```
.. tip::

    Using profiles is strongly recommended. Learn more about them...
```

### References

References are commonly used in the documentation and it's always a good way to highlight texts and give an implicit or explicit importance
to something.

#### Internal reference

Use an internal reference when you want to refer to a specific section in this documentation. Most of the sections have a reference mark
just before their names so you can reference it.

```
.. _conan_export_pkg_command:

conan export-pkg
================

...
```

To add a reference to the `conan export-pkg` command from another text:

```
Read more about the :ref:`conan export-pkg<conan_export_pkg_command>` command.
Or reference the :ref:`conan_export_pkg_command` directly.
```

#### External references

Use external references with external URL at the bottom of the file like this:

```
Submit a request to include it in `conan-center`_.
...
...

.. _`conan-center`: https://bintray.com/conan/conan-center
```

In case you want to use explicit external references with a link, make sure it doesn't exceed the maximum line length, otherwise it
should considered to be written as a normal external reference.

```
If you are just evaluating conan, you can create an account on https://bintray.com
```
