.. _conan_1_0:


Testing conan 1.0.0-beta
==========================

Conan 1.0 is really close. And we need your help to polish and tune it, before it is released. Once it is released, there will be a strong commitment on not breaking, and changing things will require more time. So we have released a 1.0.0-beta version, you can install and try now:

.. code-block:: bash

    $ pip install conan==1.0.0b1 --upgrade

There has been a few things that will break existing usage (compared to 0.30). Most of them are in the command line arguments, so they be relatively easy to fix. The most important one is that now most command requires the path to the conanfile folder or file, instead of using ``--path`` and ``--file`` arguments. Especifically, “conan export” and “conan create” will be the ones most affected:

.. code-block:: bash

    $ conan create . user/channel
    $ conan create . Pkg/0.1@user/channel
    $ conan export . user/channel
    $ conan export . Pkg/0.1@user/channel
    # instead of --path=myfolder --file=myconanfile.py, now you can do:
    $ conan export myfolder/myconanfile.py Pkg/0.1@user/channel

This behavior aligns with the ``conan source``, ``conan build``, ``conan package`` commands, that all use the same arguments to locate the “conanfile.py” containing the logic to be run.

Now all commands read: ``command <origin-conanfile> ….``

There are other few minor deprecations and removals you should be aware of:

- scopes were completely removed in conan 0.30.X
- ``self.conanfile_directory`` has been removed. Use ``self.source_folder``, ``self.build_folder``, etc. instead
- ``self.cpp_info``, ``self.env_info`` and ``self.user_info`` scope has been reduced to only the ``package_info()`` method
- ``gcc`` and ``ConfigureEnvironment`` were already removed in conan 0.30.1
- ``werror`` doesn't exist anymore. Now it is the builtin behavior.
- Command ``test_package`` has been removed. Use ``conan create`` and ``conan test`` instead.
- ``CMake`` helper only allows now (from conan 0.29). the ``CMake(self)`` syntax
- ``conan package_files`` command was replaced in conan 0.28 by ``conan export-pkg`` command.

There are a few improvements that you could also test (though the focus would be on possible regressions, of course):

- Cross-compilation support with new default settings in settings.yml: ``os_build``, ``arch_build``, ``os_target``, ``arch_target``
- Model and utilities for Windows subsystems: Cygwin, Mingw, WLS.

.. note::

  Conan 1.0 will be released in just 2 weeks. Please try the current beta, don't hesitate to ask any questions and report any issue as soon as possible.

  Thanks very much for your continuous support and feedback!
