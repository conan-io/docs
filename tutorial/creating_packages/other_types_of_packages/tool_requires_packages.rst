Tool requires packages
======================

In the ":ref:`Using build tools as Conan packages <consuming_packages_tool_requires>`" section we learned how to use
a tool require to build (or help building) our project or Conan package.
In this section we are going to learn how to create a recipe for a tool require.

Please, first clone the sources to recreate this project. You can find them in the
`examples2.0 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/tutorial/creating_packages/other_packages/tool_requires


A simple tool require recipe
----------------------------

Let's see a recipe that even being very simple, covers most of the ``tool-require`` use-cases:

.. code-block:: python
    :caption: conanfile.py

    import os
    import stat
    from conan import ConanFile
    from conan.tools.files import save


    class my_tool(ConanFile):
        name = "my_tool"
        version = "1.0"
        package_type = "application"

        settings = "os", "arch"

        def package(self):
            extension = "sh" if self.settings_build.os != "Windows" else "bat"
            app_path = os.path.join(self.package_folder, "bin", "say_hello.{}".format(extension))
            save(self, app_path, 'echo "Hello!!!"')
            os.chmod(app_path, os.stat(app_path).st_mode | stat.S_IEXEC)

        def package_info(self):
            self.buildenv_info.define("MYVAR", "23")


There are few relevant things in this recipe:

1. It declares ``package_type = "application"``, this is optional but convenient, it will indicate conan that the current
   package doesn't contain headers or libraries to be linked. The consumers will know that this package is an application.

2. The ``package()`` method is packaging the executables into the ``bin/`` folder, that is declared by default as a bindir:
   ``self.cpp_info.bindirs = ["bin"]``.

3. We are using ``self.buildenv_info`` to define environment variables that will be available in the consumer.

As the application is a simple shell script we are granting execution permissions to the script, this is usually not
needed if you are building a real executable.

Let's create a binary package for the tool_require:

.. code-block:: bash

    $ conan create .
    ...
    my_tool/1.0: Calling package()
    my_tool/1.0 package(): Packaged 1 '.sh' file: say_hello.sh
    my_tool/1.0 package(): Packaged 1 '.bat' file: say_hello.bat
    my_tool/1.0: Full package reference: my_tool/1.0#a05ef273264042c2082499a3061fb8df:82339...2e7c91ab18a1#dd38aae...37c60cbc


We can create a consumer recipe to test if we can run the ``say_hello`` application of the ``tool_require``.


.. code-block:: python
    :caption: consumer.py

    from conan import ConanFile


    class MyConsumer(ConanFile):
        name = "my_library"
        version = "1.0"
        settings = "os", "arch", "compiler", "build_type"
        tool_requires = "my_tool/1.0"

        def build(self):
            if self.settings_build.os != "Windows"
                self.run("say_hello.sh")
                self.run("echo MYVAR=$MYVAR")
            else:
                self.run("say_hello.bat")
                self.run("echo MYVAR=%MYVAR%")


In this simple recipe we are declaring a ``tool_require`` to ``my_tool/1.0`` and we are calling directly the packaged
application ``say_hello`` in the ``build()`` method, also printing the value of the ``MYVAR`` env variable.

If we build the consumer:


.. code-block:: bash


    $ conan build consumer.py

    -------- Installing packages ----------

    Installing (downloading, building) binaries...
    my_tool/1.0: Already installed!

    -------- Finalizing install (deploy, generators) ----------
    consumer.py (my_library/1.0): Aggregating env generators
    consumer.py (my_library/1.0): Calling build()
    consumer.py (my_library/1.0): RUN: say_hello.sh
    Capturing current environment in ../deactivate_conanbuildenv-release-x86_64.sh
    Configuring environment variables
    Hello!!!
    ...
    MYVAR=23

We can see the ``Hello!!!`` message, and the "23" value assigned to ``MYVAR`` but, why are these automatically available?

- The generators ``VirtualBuildEnv`` and ``VirtualRunEnv`` are automatically used.
- The ``VirtualRunEnv`` is reading the ``tool-requires`` and is creating a launcher like ``conanbuildenv-release-x86_64.sh`` appending
  all ``cpp_info.bindirs`` to the ``PATH``, all the ``cpp_info.libdirs`` to the ``LD_LIBRARY_PATH`` environment variable and
  declaring each variable of ``self.buildenv_info``.
- Every time conan executes the ``self.run``, by default, activates the ``conanbuild.sh`` file before calling any command.
  The ``conanbuild.sh`` is including the ``conanbuildenv-release-x86_64.sh``, so the application is in the PATH
  and the enviornment variable "MYVAR" has the value declared in the tool-require.


More complex recipes
--------------------

- Toolchains (compilers) ?
- Usage of `self.rundenv_info` ?
- settings_target ?
