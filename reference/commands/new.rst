.. _reference_commands_new:

conan new
=========

conan new
---------

.. code-block:: text

    $ conan new --help
    usage: conan new [-h] [-v [V]] [--logger] [-d DEFINE] [-f] template

    Create a new recipe (with conanfile.py and other files) from either a predefined or a user-defined template

    positional arguments:
      template              Template name, either a predefined built-in or a user-
                            provided one. Available built-in templates: basic,
                            cmake_lib, cmake_exe, meson_lib, meson_exe,
                            msbuild_lib, msbuild_exe, bazel_lib, bazel_exe,
                            autotools_lib, autotools_exe. E.g. 'conan new
                            cmake_lib -d name=hello -d version=0.1'. You can
                            define your own templates too by inputting an absolute
                            path as your template, or a path relative to your
                            conan home folder.

    optional arguments:
      -h, --help            show this help message and exit
      -v [V]                Level of detail of the output. Valid options from less
                            verbose to more verbose: -vquiet, -verror, -vwarning,
                            -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug,
                            -vvv or -vtrace
      --logger              Show the output with log format, with time, type and
                            message.
      -d DEFINE, --define DEFINE
                            Define a template argument as key=value
      -f, --force           Overwrite file if it already exists


The ``conan new`` command creates a new recipe in the current working directory,
plus extra example files such as *CMakeLists.txt* or the *test_package* folder (as necessary),
to either be used as a basis for your own project or aiding in the debugging process.

Note that each template has some required and some [optional] user-defined variables used to customize the resulting files.

The available templates are:

- **basic**:
  Creates a simple recipe with some example code and helpful comments,
  and is a good starting point to avoid writing boilerplate code.

  Its variables are: [name], [version], [description], [require, require...]

- **alias**:
  Creates the minimal recipe needed to define an alias to a target recipe

  Its variables are: name, [version], target

- **cmake_lib**:
  Creates a cmake library target that defines a function called ``name``,
  which will print some information about the compilation environment to stdout.
  You can add requirements to this template in the form of

  ``conan new cmake_lib -d name=ai -d version=1.0 -d requires=math/3.14 -d requires=magic/0.0``

  This will add requirements for both ``math/3.14`` and ``magic/0.0`` to the `requirements()` method,
  will add the necessary ``find_package``s in CMake, and add a call to ``math()`` and ``magic()``
  inside the generated ``ai()`` function.

  Its variables are: name, version, [require, require...]

- **cmake_exe**:
  Creates a cmake executable target that defines a function called ``name``,
  which will print some information about the compilation environment to stdout.
  You can add requirements to this template in the form of

  ``conan new cmake_exe -d name=game -d version=1.0 -d requires=math/3.14 -d requires=ai/1.0``

  This will add requirements for both ``math/3.14`` and ``ai/1.0`` to the `requirements()` method,
  will add the necessary ``find_package``s in CMake, and add a call to ``math()`` and ``ai()``
  inside the generated ``game()`` function.

  Its variables are: name, version, [require, require...]

- **autotools_lib**:
  Creates an Autotools library.

  Its variables are: name, version

- **autotools_exe**:
  Creates an Autotools executable

  Its variables are: name, version

- **bazel_lib**:
  Creates a Bazel library.

  Its variables are: name, version

- **bazel_exe**:
  Creates a Bazel executable

  Its variables are: name, version

- **meson_lib**:
  Creates a Meson library.

  Its variables are: name, version

- **meson_exe**:
  Creates a Meson executable

  Its variables are: name, version

- **msbuild_lib**:
  Creates a MSBuild library.

  Its variables are: name, version

- **msbuild_exe**:
  Creates a MSBuild executable

  Its variables are: name, version


Examples
--------

.. code-block:: bash

    $ conan new basic


Generates a basic *conanfile.py* that does not implement any custom functionality

.. code-block:: bash

    $ conan new basic -d name=mygame -d requires=math/1.0 -d requires=ai/1.3

Generates a *conanfile.py* for ``mygame`` that depends on the packages ``math/1.0`` and ``ai/1.3``


.. code-block:: bash

    $ conan new cmake_exe -d name=game -d version=1.0 -d requires=math/3.14 -d requires=ai/1.0

Generates the necessary files for a CMake executable target.
This will add requirements for both ``math/3.14`` and ``ai/1.0`` to the `requirements()` method,
will add the necessary ``find_package`` in CMake, and add a call to ``math()`` and ``ai()``
inside the generated ``game()`` function.


Custom templates
----------------

There's also the possibility to create your own templates by passing a path to your template file,
both as an absolute path, or relative to your Conan home folder.
