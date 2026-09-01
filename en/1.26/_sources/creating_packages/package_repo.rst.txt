.. _package_repo:

Recipe and Sources in the Same Repo
===================================

Sometimes it is more convenient to have the recipe and source code together in the same repository.
This is true especially if you are developing and packaging your own library, and not one from a third-party.

There are two different approaches:

- Using the :ref:`exports sources attribute <exports_sources_attribute>` of the conanfile to
   export the source code together with the recipe. This way the recipe is self-contained and will
   not need to fetch the code from external origins when building from sources. It can be considered
   a "snapshot" of the source code.
-  Using the :ref:`scm attribute <scm_attribute>` of the conanfile to capture the remote and
   commit of your repository automatically.


Exporting the Sources with the Recipe: ``exports_sources``
----------------------------------------------------------

This could be an appropriate approach if we want the package recipe to live in the same repository
as the source code it is packaging.

First, let's get the initial source code and create the basic package recipe:

.. code-block:: bash

    $ conan new hello/0.1 -t -s

A *src* folder will be created with the same "hello" source code as in the previous example. You
can have a look at it and see that the code is straightforward.

Now let's have a look at *conanfile.py*:

.. code-block:: python

    from conans import ConanFile, CMake

    class HelloConan(ConanFile):
        name = "hello"
        version = "0.1"
        license = "<Put the package license here>"
        url = "<Package recipe repository url here, for issues about the package>"
        description = "<Description of hello here>"
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False]}
        default_options = {"shared": False}
        generators = "cmake"
        exports_sources = "src/*"

        def build(self):
            cmake = CMake(self)
            cmake.configure(source_folder="src")
            cmake.build()

            # Explicit way:
            # self.run('cmake "%s/src" %s' % (self.source_folder, cmake.command_line))
            # self.run("cmake --build . %s" % cmake.build_config)

        def package(self):
            self.copy("*.h", dst="include", src="src")
            self.copy("*.lib", dst="lib", keep_path=False)
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.dylib*", dst="lib", keep_path=False)
            self.copy("*.so", dst="lib", keep_path=False)
            self.copy("*.a", dst="lib", keep_path=False)

        def package_info(self):
            self.cpp_info.libs = ["hello"]

There are two important changes:

- Added the ``exports_sources`` field, indicating to Conan to copy all the files from the local *src*
  folder into the package recipe.
- Removed the ``source()`` method, since it is no longer necessary to retrieve external sources.

Also, you can notice the two CMake lines:

.. code-block:: cmake

    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    conan_basic_setup()

They are not added in the package recipe, as they can be directly added to the *src/CMakeLists.txt*
file.

And simply create the package for user and channel **demo/testing** as described previously:

.. code-block:: bash

    $ conan create . demo/testing
    ...
    hello/0.1@demo/testing test package: Running test()
    Hello world Release!

.. _scm_feature:

Capturing the Remote and Commit: ``scm``
----------------------------------------

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

You can use the :ref:`scm attribute <scm_attribute>` with the ``url`` and ``revision`` field set to ``auto``.
When you export the recipe (or when :command:`conan create` is called) the exported recipe will capture the
remote and commit of the local repository:

.. code-block:: python
   :emphasize-lines: 8-10

    import os
    from conans import ConanFile, CMake, tools

    class HelloConan(ConanFile):
        scm = {
            "type": "git",  # Use "type": "svn", if local repo is managed using SVN
            "subfolder": "hello",
            "url": "auto",
            "revision": "auto",
            "password": os.environ.get("SECRET", None)
        }
        ...

You can commit and push the *conanfile.py* to your origin repository, which will always preserve the ``auto``
values. When the file is exported to the Conan local cache (except you have uncommitted changes, read below),
these data will be stored in the *conanfile.py* itself (Conan will modify the file) or in a special file
:ref:`conandata_yml` that will be stored together with the recipe, depending on the value of the configuration
parameter :ref:`scm_to_conandata<conan_conf>`.

 * If the ``scm_to_conandata`` is not activated (default behavior in Conan v1.x) Conan will store a modified
   version of the *conanfile.py* with the values of the fields in plain text:

   .. code-block:: python
    :emphasize-lines: 8-10

        import os
        from conans import ConanFile, CMake, tools

        class HelloConan(ConanFile):
            scm = {
                "type": "git",
                "subfolder": "hello",
                "url": "https://github.com/conan-io/hello.git",
                "revision": "437676e15da7090a1368255097f51b1a470905a0",
                "password": "MY_SECRET"
            }
            ...

   So when you :ref:`upload the recipe <uploading_packages>` to a Conan remote, the recipe will contain
   the "resolved" URL and commit.

 * If ``scm_to_conandata`` is activated, the value of these fields (except ``username`` and ``password``) will
   be stored in the :ref:`conandata_yml` file that will be automatically exported with the recipe.

Whichever option you choose, the data resolved will be asigned by Conan to the corresponding field when the recipe
file is loaded, and they will be available for all the methods defined in the recipe. Also, if building the package
from sources, Conan will fetch the code in the captured url/commit before running the method ``source()`` in the
recipe (if defined).

As SCM attributes are evaluated in the local directory context (see :ref:`scm attribute <scm_attribute>`),
you can write more complex functions to retrieve the proper values, this source *conanfile.py* will
be valid too:

.. code-block:: python
   :emphasize-lines: 7, 8

    import os
    from conans import ConanFile, CMake, tools

    def get_remote_url():
         """ Get remote url regardless of the cloned directory """
         here = os.path.dirname(__file__)
         svn = tools.SVN(here)
         return svn.get_remote_url()

    class HelloConan(ConanFile):
         scm = {
            "type": "svn",
            "subfolder": "hello",
            "url": get_remote_url(),
            "revision": "auto"
         }
        ...

.. tip::

   When doing a :command:`conan create` or :command:`conan export`, Conan will capture the sources of the local scm project folder in the local cache.

   This allows building packages making changes to the source code without the need of committing them and pushing them to the remote
   repository. This convenient to speed up the development of your packages when cloning from a local repository.

   So, if you are using the ``scm`` feature, with some ``auto`` field for `url` and/or `revision` and you
   have uncommitted changes in your repository a warning message will be printed:

   .. code-block:: bash

     $ conan export . hello/0.1@demo/testing

      hello/0.1@demo/testing: WARN: There are uncommitted changes, skipping the replacement of 'scm.url'
      and 'scm.revision' auto fields. Use --ignore-dirty to force it.
      The 'conan upload' command will prevent uploading recipes with 'auto' values in these fields.

   As the warning message explains, the ``auto`` fields won't be replaced unless you specify ``--ignore-dirty``,
   and by default, the :command:`conan upload` will block the upload of the recipe. This prevents recipes
   to be uploaded with incorrect scm values exported.
   You can use :command:`conan upload --force` to force uploading the recipe with the ``auto`` values un-replaced.
