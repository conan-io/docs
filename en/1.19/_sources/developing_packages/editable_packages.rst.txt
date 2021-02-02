.. _editable_packages:

Packages in editable mode
=========================

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

When working in big projects with several functionalities interconnected it is recommended to avoid
the one-and-only huge project approach in favor of several libraries, each one specialized
in a set of common tasks, even maintained by dedicated teams. This approach helps to isolate
and reusing code helps with compiling times and reduces the likelihood of including files that
not correspond to the API of the required library.

Nevertheless, in some case, it is useful to work in several libraries at the same time and see how
the changes in one of them are propagated to the others. Following the
:ref:`local workflow<package_dev_flow>` an user can execute the commands :command:`conan source`,
:command:`conan install`, :command:`conan build` and :command:`conan package`, but in order to
get the changes ready for a consumer library, it is needed the :command:`conan create` that will
actually trigger a build to generate the binaries in the cache or to run :command:`conan export-pkg`
to copy locally built artifacts into the conan cache and make them available to consumers.

With the editable packages, you can tell Conan where to find the headers and the artifacts ready for
consumption in your local working directory. There is no need to package.

Let's see this feature over an example where a developer is creating a ``CoolApp`` but at the same
time they want to work on ``cool/version@user/dev`` library which is tightly coupled to the app.

The package ``cool/version@user/dev`` is already working, the developer has the sources in a
local folder and they are using whatever method to build and develop locally and can perform
a :command:`conan create . cool/version@user/dev` to create the package.

Also, there is a *conanfile.txt* (or a more complex recipe) for the application ``CoolApp`` that
has ``cool/version@user/dev`` among its requirements. When building this application, the
resources of ``cool`` are used from the Conan local cache.

Put a package in editable mode
------------------------------

To avoid creating the package ``cool/version@user/dev`` in the cache for every change, we are going
to put that package in editable mode, creating **a link from the reference in the cache to the local
working directory**:

.. code-block:: bash

    $ conan editable add <path/to/local/dev/libcool> cool/version@user/dev
    # you could do "cd <path/to/local/dev/libcool> && conan editable add . cool/version@user/dev"


That is it. Now, every usage of ``cool/version@user/dev``, by any other Conan package or project,
will be redirected to the ``<path/to/local/dev/libcool>`` user folder instead of using the package
from the conan cache.

The Conan package recipes define a package "layout" in their ``package_info()`` methods. The default one,
if nothing is specified is equivalent to:

.. code-block:: python

    def package_info(self):
        # default behavior, doesn't need to be explicitly defined in recipes
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.bindirs = ["bin"]
        self.cpp_info.resdirs = ["res"]

That means that conan will use the path ``path/to/local/dev/libcool/include`` for locating the headers of
the ``cool`` package, the ``path/to/local/dev/libcool/lib`` to locate the libraries of the package, and so on.

That might not be very useful, as typically while editing the source code and doing incremental builds, the
development layout is different from that final "package" layout. While it is possible to run a
:command:`conan package` local command to execute the packaging in the user folder, and that will achieve that
final layout, that is not very elegant. Conan provides several ways to customize the layout for editable packages.

Editable packages layouts
-------------------------

The custom layout of a package while it is in editable mode can be defined in different ways:

Recipe defined layout
++++++++++++++++++++++

A recipe can define a custom layout when it is not living in the local cache, in its ``package_info()`` method,
something like:

.. code-block:: python

    from conans import ConanFile
    
    class Pkg(ConanFile):
        settings = "build_type"
        def package_info(self):
            if not self.in_local_cache:
                d = "include_%s" % self.settings.build_type
                self.cpp_info.includedirs = [d.lower()]

That will map the include directories to ``path/to/local/dev/libcool/include_debug`` when working with ``build_type=Debug``
conan setting, and to ``path/to/local/dev/libcool/include_release`` if ``build_type=Release``. In the same way, other 
directories (libdirs, bindirs, etc) can be customized, with any logic, different for different OS, build systems, etc.

.. code-block:: python

    from conans import ConanFile
    
    class Pkg(ConanFile):
        settings = "os", "compiler", "arch", "build_type"
        def package_info(self):
            if not self.in_local_cache:
                if self.settings.compiler == "Visual Studio":
                    # NOTE: Use the real layout used in your VS projects, this is just an example
                    self.cpp_info.libdirs = ["%s_%s" % (self.settings.build_type, self.settings.arch)]

That will define the libraries directories to ``path/to/local/dev/libcool/Release_x86_64``, for example.
That is only an example, the real layout used by VS would be different.

Layout files
+++++++++++++

Instead of changing the recipe file to match the local layout, it's possible to define the
layout in a separate file. This is especially useful if you have a large number of libraries
with the same structure so you can write it once and use it for several packages.

Layout files are *ini* files, but before parsing them Conan uses the Jinja2 template
engine passing the ``settings``, ``options`` and current ``reference`` objects, so you
can add logic to the files:

   .. code-block:: ini

       [includedirs]
       src/core/include
       src/cmp_a/include

       [libdirs]
       build/{{settings.build_type}}/{{settings.arch}}

       [bindirs]
       {% if options.shared %}
       build/{{settings.build_type}}/shared
       {% else %}
       build/{{settings.build_type}}/static
       {% endif %}

       [resdirs]
       {% for item in ["cmp1", "cmp2", "cmp3"] %}
       src/{{ item }}/resouces/{% if item != "cmp3" %}{{ settings.arch }}{% endif %}
       {% endfor %}

You can have a look at the `Jinja2 documentation <https://palletsprojects.com/p/jinja/>`_ to know more
about its powerful syntax.


This file can use the package reference to customize logic for a specific package:

   .. code-block:: ini

       [includedirs]
       src/include

       [cool/version@user/dev:includedirs]
       src/core/include

This layout will define the ``src/core/include`` include directory for the ``cool`` package, and
``src/include`` for other packages in editable mode.

In every case the directories that will be affected by the editable mode will be ``includedirs``,
``libdirs``, ``bindirs``, ``resdirs``, ``srcdirs`` and ``builddirs``, all of them declared in the
:ref:`cpp_info_attributes_reference` dictionary; the rest of values in that dictionary won't
be modified. So ``cflags``, ``defines``, library names in ``libs`` defined in ``package_info()``
will still be used.

By default all folders paths are relative to the directory where the *conanfile.py*
of the editable package is (which is the path used to create the link), though they also allow absolute
paths.

Specifying layout files
+++++++++++++++++++++++

Layout files are specified in the :command:`conan editable add` command, as an extra argument:

.. code-block:: bash

    $ conan editable add . cool/version@user/dev --layout=win_layout

That ``win_layout`` file will be first looked for relative to the current directory (the
path can be absolute too). If it is found, that will be used. It is possible to add those
layouts in the source repositories, so they are always easy to find after a clone.

If the specified layout is not found relative to the current directory, it will be looked
for in the conan cache, in the ``.conan/layouts`` folder. This is very convenient to have
a single definition of layouts that can be shared with the team and installed with
``conan config install``.

If no argument is specified, the :command:`conan editable add` command will try to use a `.conan/layouts/default`
layout from the local cache.

You can switch layout files by passing a different argument to new calls to :command:`conan editable add`.

Evaluation order and priority
+++++++++++++++++++++++++++++

It is important to understand the evaluation order and priorities regarding the definitions of layouts:

- The first thing that will always execute is the recipe ``package_info()``. That will define
  the flags, definitions, as well as some values for the layout folders: ``includedirs``, ``libdirs``, etc.
- If a layout file is defined, either explicitly or using the implicit ``.conan/layouts/default``,
  conan will look for matches, based on its package reference.
- If a match is found, either because of global definitions like ``[includedirs]``
  or because a match like ``[pkg/version@user/channel:includedirs]``, then the layout folders
  (includedirs, libdirs, resdirs, builddirs, bindirs), will be invalidated and replaced by the ones
  defined in the file.
- If a specific match like ``[pkg/version@user/channel:includedirs]`` is found, it is expected to
  have defined also its specific ``[pkg/version@user/channel:libdirs]``, etc. The global layout
  folders specified without package reference won't be applied once a match is found.
- It no match is found, the original values for the layout folders defined in ``package_info()`` will
  be respected.
- The layout file to be used is defined at :command:`conan editable add` time. If a ``.conan/layouts/default`` file
  is added after the :command:`conan editable add`, it will not be used at all.


Using a package in editable mode
--------------------------------

Once a reference is in editable mode it is used **system wide** (for every set of ``settings`` and
``options``) by Conan (by every Conan client that uses the same cache), no changes are
required in the consumers. Every :command:`conan install` command that requires our editable
``cool/version@user/dev`` package will use the paths to the local directory and the changes
made to this project will be taken into account by the packages using its headers or linking
against it. 

To summarize, consumption of packages in editable mode is transparent to their consumers.
To try that it is working, the following flow should work:

- Get sources of ``cool/version@user/dev``: :command:`git/svn clone... && cd folder`
- Put package in editable mode: :command:`conan editable add . cool/version@user/dev --layout=mylayout`
- Work with it and build using any tool. Check that your local layout is reflected in the layout
  file *mylayout* specified in the previous step.
- Go to the consumer project: ``CoolApp``
- Build it using any local flow: :command:`conan install` and build
- Go back to ``cool/version@user/dev`` source folder, do some changes, and just build. No Conan commands necessary
- Go to the consumer project: ``CoolApp`` and rebuild. It should get the changes from the ``cool`` library.

In that way, it is possible to be developing both the ``cool`` library and the ``CoolApp`` application, at the same
time, without any Conan command.

.. note::

    When a package is in editable mode, most of the commands will not work. It is not possible to :command:`conan upload`,
    :command:`conan export` or :command:`conan create` when a package is in editable mode.

Revert the editable mode
------------------------

In order to revert the editable mode just remove the link using:

.. code-block:: bash

    $ conan editable remove cool/version@user/dev

It will remove the link (the local directory won't be affected) and all the packages consuming this
requirement will get it from the cache again.

.. warning::

   Packages that are built consuming an editable package in its graph upstreams can generate binaries
   and packages incompatible with the released version of the editable package. Avoid uploading
   these packages without re-creating them with the in-cache version of all the libraries.
