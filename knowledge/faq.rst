.. _faq:

FAQ
===

.. seealso::

    There is a great community behind Conan with users helping each other in `Cpplang Slack`_.
    Please join us in the ``#conan`` channel!

Troubleshooting
---------------

ERROR: Missing prebuilt package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When installing packages (with :command:`conan install` or :command:`conan create`) it is possible
that you get an error like the following one:

.. code-block:: text

    ERROR: Missing binary: zlib/1.2.11:b1d267f77ddd5d10d06d2ecf5a6bc433fbb7eeed

    zlib/1.2.11: WARN: Can't find a 'zlib/1.2.11' package binary 'b1d267f77ddd5d10d06d2ecf5a6bc433fbb7eeed' for the configuration:
    [settings]
    arch=x86_64
    build_type=Release
    compiler=apple-clang
    compiler.cppstd=gnu11
    compiler.libcxx=libc++
    compiler.version=14
    os=Macos
    [options]
    fPIC=True
    shared=False

    ERROR: Missing prebuilt package for 'zlib/1.2.11'. You can try:
        - List all available packages using 'conan list "{ref}:*" -r=remote'
        - Explain missing binaries: replace 'conan install ...' with 'conan graph explain ...'
        - Try to build locally from sources using the '--build=zlib/1.2.11' argument

    More Info at 'https://docs.conan.io/en/2/knowledge/faq.html#error-missing-prebuilt-package'

This means that the package recipe ``zlib/1.2.11`` exists, but for some reason there is no
precompiled package for your current settings or options. Maybe the package creator didn't build and
shared pre-built packages at all and only uploaded the package recipe, or they are only
providing packages for some platforms or compilers. E.g. the package creator built
packages from the recipe for apple-clang 11, but you are using apple-clang 14.
Also you may want to check your `package ID mode` as it may
have an influence on the packages available for it.

By default, Conan doesn't build packages from sources. There are several possibilities to
overcome this error:

- You can try to build the package for your settings from sources, indicating some build
  policy as argument, like :command:`--build zlib*` or :command:`--build missing`. If the
  package recipe and the source code work for your settings you will have your binaries
  built locally and ready for use.

- If building from sources fails, and you are using the `conancenter` remote, you can open
  an issue in `the Conan Center Index repository
  <https://github.com/conan-io/conan-center-index>`_



.. _error_invalid_setting:

ERROR: Invalid setting
^^^^^^^^^^^^^^^^^^^^^^

It might happen sometimes, when you specify a setting not present in the defaults
that you receive a message like this:

.. code-block:: bash

    $ conan install . -s compiler.version=4.19 ...

    ERROR: Invalid setting '4.19' is not a valid 'settings.compiler.version' value.
    Possible values are ['4.4', '4.5', '4.6', '4.7', '4.8', '4.9', '5.1', '5.2', '5.3', '5.4', '6.1', '6.2']


This doesn't mean that such compiler version is not supported by Conan, it is just that it is not present in the actual
defaults settings. You can find in your user home folder ``~/.conan2/settings.yml`` a settings file that you
can modify, edit, add any setting or any value, with any nesting if necessary. See :ref:`reference_config_files_settings_yml` to learn
how you can customize your settings to model your binaries at your will.

As long as your team or users have the same settings (``settings.yml`` and ``settings_user.yml`` an be easily shared with the
``conan config install`` command), everything will work. The *settings.yml* file is just a
mechanism so users agree on a common spelling for typical settings. Also, if you think that some settings would
be useful for many other conan users, please submit it as an issue or a pull request, so it is included in future
releases.

It is possible that some built-in helper or integrations, like ``CMake`` or ``CMakeToolchain`` will not understand the new added settings,
don't use them or even fail if you added some new unexpected value to existing settings. 
Such helpers as ``CMake`` are simple utilities to translate from conan settings to the respective
build system syntax and command line arguments, so they can be extended or replaced with your own
one that would handle your own private settings.

.. _`Cpplang Slack`: https://cppalliance.org/slack/


ERROR: AuthenticationException:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error can happen, if there are no or false authentication credentials in the HTTP request from conan. To get more information try enabling the debug level for HTTP connections:

.. code-block:: python

    import http.client
    http.client.HTTPConnection.debuglevel = 1
    
One source of error can be the ``.netrc`` file, which is `honored by the requests library <https://requests.readthedocs.io/en/latest/user/quickstart/#custom-headers>`_.

.. _faq_different_revisions:

ERROR: Obtaining different revisions in Linux and Windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Git will (by default) checkout files in Windows systems using ``CRLF`` line endings, effectively producing different files than in Linux that files will use ``LF`` line endings. As files are different, the Conan recipe revision will be different from the revisions computed in other platforms such as Linux, resulting in missing the respective binaries in the other revision.

Conan will not normalize or change in any way the source files, it is not its responsibility and there are risks of breaking things. The source control is the application changing the files, so that is a more correct place to handle this. It is necessary to instruct Git to do the checkout with the same line endings. This can be done several ways, for example, by adding a ``.gitattributes`` file to the project repository with something like:

.. code-block:: ini

    * text eol=lf


Other approach would be to change the ``.gitconfig`` to change it globally. Modern editors (even Notepad) in Windows can perfectly work with files with ``LF``, it is no longer necessary to change the line endings.


.. _faq_different_options_values:


Defining options for dependencies in conanfile.py recipes doesn't work
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Conan expands the dependency graph depth-first, this is important to be able to implement many of the very special C/C++ propagation
logic (headers, static and shared libraries, applications, tool-requires, test-requires, conflicts, overrides, etc.).

This means that when a ``conanfile.py`` declares something like:

.. code-block:: python

  class MyPkg(ConanFile):
      name = "mypkg"
      version = "0.1"
      default_options = {"zlib/*:shared": True}
      # Or
      def requirements(self):
          self.requires("zlib/1.3", options={"shared": True})


it cannot be always honored, and the ``zlib`` dependency might end with different ``shared=False`` option value.
This in-recipe options values definition for dependencies only works if:

- There are no other packages depending on ``zlib`` in the graph
- There are other packages depending on ``zlib`` in the graph, but ``mypkg/0.1`` is the first require (the first branch
  in the dependency graph) that is required. That means that ``requires = "mypkg/0.1", "zlib/1.3"`` will work and will have 
  ``zlib`` as shared, but ``requires = "zlib/1.3", "mypkg/0.1"`` will expand first ``zlib`` with its default, which is 
  ``shared=False`` and when the ``mypkg/0.1`` is computed it will be too late to change ``zlib`` to be ``shared=True``.

In case there are some recipe that won't work at all with some option of the dependency, the recommendation is to define
a ``validate()`` method in the recipe to guarantee that it will raise an error if for some reason the upstream dependency
doesn't have the right options values.

Conan might be able to show some (not guaranteed to be exhaustive) of these issues in the output of the Conan commands,
please read it carefully.


.. code-block::

    Options conflicts
        liba/0.1:myoption=1 (current value)
            libc/0.1->myoption=2
        It is recommended to define options values in profiles, not in recipes

In general, it is more recommended to define options values in profile files, not in recipes.
Recipe defined options always have precedence over options defined in profiles.


.. _faq_version_conflicts_version_ranges:

Getting version conflicts even when using version ranges
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is possible that when installing dependencies, there are version conflict error messages like:

.. code-block::

  ...
  Version conflict: Conflict between math/1.0.1 and math/1.0 in the graph

This :ref:`tutorial about version conflicts<tutorial_versioning_conflicts>` summarizes how different versions of the same package dependency can conflict in a dependency graph and how to resolve those conflicts.

However, there are some situations in which the conflict is not that evident, for example when there are some mixed version ranges and fixed dependencies, something like:

.. code-block::  python

    def requirements(self):
      self.requires("libb/1.0")  # requires liba/[>=1.0 <2]
      self.requires("libc/1.0")  # requires liba/1.0

And it happens that ``libb/1.0`` has a transitive requirement to ``liba/[>=1.0 <2]``, and ``libc/1.0`` requires ``liba/1.0``, and there exist the ``liba/1.1`` or higher packages. In this case, Conan might also throw a "version conflict" error.

The root cause is that resolving the joint compatibility for all the possible constraints that version-ranges define in a graph is a known NP-hard problem, known as SAT-solver. Evaluating each hypothesis in this NP-hard problem in Conan is very expensive, because it usually requires to look for a version/revision in all remotes defined, then download such version/revision compressed files, unzip them, load and Python-parse and evaluate them and finally to do all the graph computation processing, which involves a full propagation down the already expanded graph to propagate the C/C++ requirement traits that can produce the conflicts. This would make the problem intractable in practice, that would require to wait for many hours to finish.

So instead of doing that, Conan uses a "greedy" algorithm that does not require backtracking, but still will try to reconcile version-ranges with fixed versions when possible. The most important point to know about this is that Conan implements a "depth-first" graph expansion, evaluating the ``requires`` in the order they are declared. Knowing this can help to solve this conflict. In the case above the error happens because ``libb/1.0`` is expanded first, it finds a requirement of ``liba/[>=1.0 <2]``, and as no other constraint to ``liba`` has been found before, it freely resolves to the latest ``liba/1.1``. When later ``libc/1.0`` is expanded, it finds a requirement to ``liba/1.0``, but it is already too late, as it will conflict with the previous ``liba/1.1``. Going back in the previous hypothesis is the "backtracking" part that converts the problem in NP-hard, so the algorithm stops there and raises the conflict.

This can be solved just by swapping the order of ``requires``:

.. code-block::  python

    def requirements(self):
      self.requires("libc/1.0")  # requires liba/1.0
      self.requires("libb/1.0")  # requires liba/[>=1.0 <2]
      
If ``libc/1.0`` is expanded first, it resolves to ``liba/1.0``. When later ``libb/1.0`` is expanded, its transitive requirement ``liba/[>=1.0 <2]`` can be successfully satisfied by the previous ``libb/1.0``, so it can resolve the graph successfully.

The general best practices are:

- For the same dependency, try to use the same approach everywhere: use version ranges everywhere, or fixed versions everywhere for that specific dependency.
- Keep the versions aligned. If using a version range try to use the same version range everywhere.
- Declare first dependencies that use fixed version, not version ranges
- Use the ``conan graph info ... --format=html > graph.html`` graphical interactive output to understand and navigate conflicts.
