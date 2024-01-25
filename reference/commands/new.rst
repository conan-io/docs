.. _reference_commands_new:

conan new
=========

Create a new recipe (with a conanfile.py and other associated files) from either a predefined or a user-defined template.

conan new
---------

.. code-block:: text

    $ conan new -h
    usage: conan new [-h] [-v [V]] [-d DEFINE] [-f] template

    Create a new example recipe and source files from a template.

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
      -d DEFINE, --define DEFINE
                            Define a template argument as key=value, e.g., -d
                            name=mypkg
      -f, --force           Overwrite file if it already exists


The ``conan new`` command creates a new recipe in the current working directory,
plus extra example files such as *CMakeLists.txt* or the *test_package* folder (as necessary),
to either be used as a basis for your own project or aiding in the debugging process.

Note that each template has some required and some [optional] user-defined variables used to customize the resulting files.

The available templates are:

- **basic**:
  Creates a simple recipe with some example code and helpful comments,
  and is a good starting point to avoid writing boilerplate code.

  Its variables are: [name], [version], [description], [requires1, requires2, ...], [tool_requires1, tool_requires2, ...]

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

  Its variables are: name, version, [requires1, requires2, ...], [tool_requires1, tool_requires2, ...]

- **cmake_exe**:
  Creates a cmake executable target that defines a function called ``name``,
  which will print some information about the compilation environment to stdout.
  You can add requirements to this template in the form of

  ``conan new cmake_exe -d name=game -d version=1.0 -d requires=math/3.14 -d requires=ai/1.0``

  This will add requirements for both ``math/3.14`` and ``ai/1.0`` to the `requirements()` method,
  will add the necessary ``find_package``s in CMake, and add a call to ``math()`` and ``ai()``
  inside the generated ``game()`` function.

  Its variables are: name, version, [requires1, requires2, ...], [tool_requires1, tool_requires2, ...]

- **autotools_lib**:
  Creates an Autotools library.

  Its variables are: ``name``, ``version``

- **autotools_exe**:
  Creates an Autotools executable

  Its variables are: ``name``, ``version``

- **bazel_lib**:
  **Bazel integration BazelDeps, BazelToolchain, Bazel is experimental**. 
  Creates a Bazel library.

  Its variables are: ``name``, ``version``

- **bazel_exe**:
  **Bazel integration BazelDeps, BazelToolchain, Bazel is experimental**.
  Creates a Bazel executable

  Its variables are: ``name``, ``version``

- **meson_lib**:
  Creates a Meson library.

  Its variables are: ``name``, ``version``

- **meson_exe**:
  Creates a Meson executable

  Its variables are: ``name``, ``version``

- **msbuild_lib**:
  Creates a MSBuild library.

  Its variables are: ``name``, ``version``

- **msbuild_exe**:
  Creates a MSBuild executable

  Its variables are: ``name``, ``version``


.. warning::

  The output of the predefined built-in templates is **not stable**. It might
  change in future releases to adapt to the latest tools or good practices.


Examples
--------

.. code-block:: text

    $ conan new basic


Generates a basic *conanfile.py* that does not implement any custom functionality

.. code-block:: text

    $ conan new basic -d name=mygame -d requires=math/1.0 -d requires=ai/1.3

Generates a *conanfile.py* for ``mygame`` that depends on the packages ``math/1.0`` and ``ai/1.3``


.. code-block:: text

    $ conan new cmake_exe -d name=game -d version=1.0 -d requires=math/3.14 -d requires=ai/1.0

Generates the necessary files for a CMake executable target.
This will add requirements for both ``math/3.14`` and ``ai/1.0`` to the ``requirements()`` method,
will add the necessary ``find_package`` in CMake, and add a call to ``math()`` and ``ai()``
inside the generated ``game()`` function.


Custom templates
----------------

There's also the possibility to create your own templates. Templates in the Conan home should be 
located in the ``templates/command/new`` folder, and each template should create a new folder, being
the name of the folder the name of the template. If we create the ``templates/command/new/mytemplate``
folder, the command will be called with:


.. code-block:: text

    $ conan new mytemplate


As other files in the Conan home, you can manage these templates with ``conan config install``, putting them
in a git repo or http server and sharing them with your team. It is also possible to use templates from 
any folder, just passing the full path to the template in the ``conan new <full_path>``, but in general it
is more convenient to manage them in the Conan home.

The folder can contain as many files as desired. Both the filenames and the contents of the files can be
templatized using Jinja2 syntax. The command ``-d/--define`` arguments will define the ``key=value`` inputs
to the templates. 

There are some special ``-d/--defines`` names. The ``name`` one is always mandatory. The ``conan_version``
definition will always be automatically defined. The ``requires`` and ``tool_requires`` definitions, if existing, 
will be automatically converted to lists. The ``package_name`` will always be defined, by default equals to ``name``.

The file contents will be like (Jinja2 syntax):

.. code-block:: python

   class Conan(ConanFile):
      name = "{{name}}"
      version = "{{version}}"
      license = "{{license}}"


And it will require passing these values:

.. code-block:: text

    $ conan new mytemplate -d name=pkg -d version=0.1 -d license=MIT


For variable filenames, the filenames themselves can have Jinja2 syntax. For example if we store a file with
named literally ``templates/command/new/mytemplate/{{name}}``, with the brackets in the filename, when running

.. code-block:: text

    $ conan new mytemplate -d name=file.txt


a filename called ``file.txt`` will be created.

If there are files in the template to not be rendered with Jinja2, like image files, then their names should be
added to a file called ``not_templates`` inside the template directory, one filename per line.
