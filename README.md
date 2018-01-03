Documentation for conan C/C++ package manager. https://conan.io

Built and served by readthedocs: 

[![Documentation Status](https://readthedocs.org/projects/conanio/badge/?version=latest)](http://conanio.readthedocs.io/en/latest/?badge=latest)


How to build
============

- Install python and [pip docs](https://pip.pypa.io/en/stable/installing/).
- Install the requirements (sphinx):

     `$ pip install -r requirements.txt`

- Build the documentation:

    `$ make html`

How to read the built docs
==========================

Open a browser and select the _build/html/index.html file. E.j:

`$ firefox _build/html/index.html`


How to contribute
=================

Fork this repository and open a Pull Request.

Style Guidelines
----------------

Style Guidelines
-----------------------
Conan documentation is written in [reStructuredText](http://docutils.sourceforge.net/rst.html) and
follow [reStructuredText Markup Specification](http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html).

Any text style not covered by this guidelines will follow the aforementioned rules.

### Section titles

```
Section Title
=============

Section Title
-------------

Section Title
`````````````

Section Title
'''''''''''''

Section Title
.............

Section Title
~~~~~~~~~~~~~

Section Title
*************

Section Title
+++++++++++++

Section Title
^^^^^^^^^^^^^
```
### Text emphasis/highlighting

- **Bold text** to highlight important texts:

  ```
  Note the simple scenario of a **header-only** library. Such package...
  ```

- *Italics* to refer to file names, directory names and paths.

  ```
  If you have a look to the *test_package* folder, you will realize that the *example.cpp* and the
  *CMakeLists.txt* files don't have anything special. The *test_package/conanfile.py* file is...
  ```

- Inline literals with $ to refer to command line commands.
  ```
  To create a conan package you can use the ``$ conan create`` command.  You can see a ``$ git clone`` command...
  ```

- Inline literals to refer to code or text inside recipies:

  ```
   ``package()`` -> conanfile.py method
   ``cmake`` -> generator in conanfile.txt
   ``settings`` -> variable inside a ConanFile class in conanfile.py
   ```

  Like this:

  ```
  Note that the ``build_id()`` method uses the ``self.info_build`` object to alter the build hash.
  ```

- Other names like CMake, Autotools, Conan, Visual Studio should not be emphasized, just use a
  capital letter or follow the convention (like first and second capitalized letters for CMake).

### code blocks

Use code blocks for code snippets or command line actions and follow the specific language
identation:

```
.. code-block:: python

```

Identation and line lenght

Bulleted lists
  with numbers
  without numbers

text boxes
 warning tip note important

References

  internal reference
  external references
