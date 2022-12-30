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
      template              Template name, either a predefined built-in or a user-provided one.
                            Available built-in templates:
                            basic, alias, cmake_lib, cmake_exe, meson_lib, meson_exe,
                            msbuild_lib, msbuild_exe, bazel_lib, bazel_exe, autotools_lib, autotools_exe.
                            E.g. 'conan new cmake_lib -d name=hello -d version=0.1'.
                            You can define your own templates too by referencing an absolute path to your template,
                            or a path relative to your conan home folder.

    optional arguments:
      -h, --help            show this help message and exit
      -v [V]                Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror, -vwarning, -vnotice, -vstatus, -v or -vverbose, -vv or -vdebug, -vvv or -vtrace
      --logger              Show the output with log format, with time, type and message.
      -d DEFINE, --define DEFINE
                            Define a template argument as key=value
      -f, --force           Overwrite file if it already exists


The ``conan new`` command creates a new recipe in the current working directory,
plus extra example files such as *CMakeLists.txt* or the *test_package* folder (as necessary),
to be used as a basis for your own project.

Each template has some required and some [optional] user-defined variables used to customize the resulting files. These are:

 * ``basic``: [name], [version], [description], [require, require...]
 * ``alias``: name, [version], target
 * ``cmake_lib``: name, version
 * ``cmake_exe``: name, version
 * ``autotools_lib``: name, version
 * ``autotools_exe``: name, version
 * ``bazel_lib``: name, version
 * ``bazel_exe``: name, version
 * ``meson_lib``: name, version
 * ``meson_exe``: name, version
 * ``msbuild_lib``: name, version
 * ``msbuild_exe``: name, version


Examples
--------

.. code-block:: bash

    $ conan new basic


Generates a basic *conanfile.py* that does not implement any custom functionality

.. code-block:: bash

    $ conan new basic -d name=mygame -d requires=math/1.0 -d requires=ai/1.3

Generates a *conanfile.py* for ``mygame`` that depends on the packages ``math/1.0`` and ``ai/1.3``




