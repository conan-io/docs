.. _migrate_to_new_environment_management:

Manage environment variables in your recipes
============================================

Automatic environment variables inheritance
-------------------------------------------

If your dependencies define some ``env_info`` variables in the ``package_info`` method they will be automatically
applied before calling the consumer conanfile.py methods ``source``, ``build``, ``package`` and ``imports``. You can read
more about ``env_info`` object :ref:`here <environment_information>`.

For example, if you are creating a package for a tool, you can define the variable ``PATH``


.. code-block:: python

   class ToolExampleConan(ConanFile):
       name = "my_tool_installer"
       ...

       def package_info(self):
           self.env_info.path.append(os.path.join(self.package_folder, "bin"))


If other conan recipe require the `my_tool_installer` one, in the ``source``, ``build``, ``package`` and ``imports`` methods
will have automatically appended to the system PATH the bin folder of the ``my_tool_installer`` package.
If ``my_tool_installer`` packages an executable called ``my_tool_executable`` in the ``bin`` of the package folder we can
directly call the tool, because it will be available in the path:

.. code-block:: python

   class MyLibExample(ConanFile):
       name = "my_lib_example"
       ...

       def build(self):
           self.run("my_tool_executable some_arguments")


You could also set ``CC``, ``CXX`` variables if we are packing a compiler to define what compiler to use or any other
environment variable. Read more about tool packages :ref:`here<create_installer_packages>`.



Environment variables overriding
--------------------------------

You can use :ref:`profiles<profiles>` to define environment variables that will apply to your recipes.
Also you can use the ``-e`` parameter in ``conan install``, ``conan info`` and ``conan test_package`` commands.

If you want to override an environment variable that a package has been inherited from its requirements, you can
use both ``profiles`` or ``-e`` to do it:

.. code-block:: bash

    conan install -e MyPackage:PATH=/other/path



Building autotools projects
---------------------------

Use the ``AutoToolsBuildEnvironment`` helper together with ``tools.environment_append`` to prepare the environment
variables needed to build a project with ``configure`` and ``make`` scripts generated with autotools:

    Example:

    .. code-block:: python
       :emphasize-lines: 13, 14

       from conans import ConanFile, AutoToolsBuildEnvironment

       class ExampleConan(ConanFile):
          ...
          def build(self):
             env_build = AutoToolsBuildEnvironment(self)
             with tools.environment_append(env_build.vars):
                self.run("./configure")
                self.run("make")

    You can read more in the section :ref:`Building with Autotools<building_with_autotools>`.


.. note::

    **ConfigureEnvironment** helper class has been deprecated. It was used to:

    1. Create a command line command to declare the environment variables inherited from the requirements (self.deps_env_info):

        This is not needed anymore, the environment variables inherited from the requirements ``self.deps_env_info`` objects are
        automatically set before the ``source``, ``build``, ``package`` and ``imports`` methods. See the section above.

    2. Create a command line to set environment variables before calling the build system, usually before calling ``configure`` or ``make``:

        The new ``AutoToolsBuildEnvironment`` and ``VisualStudioBuildEnvironment`` with the ``tool.environment_append`` offers
        cleaner and more flexible solution.



Building autotools projects in Windows with MinGW
--------------------------------------------------

You can use the new ``AutoToolsBuildEnvironment`` and the ``tool.run_in_windows_bash`` to build an Autotools projects with MinGW.
The ``run_in_windows_bash`` will open a ``bash`` shell automatically. (Needs MSYS/CYGWIN available in the path).

 .. code-block:: python
   :emphasize-lines: 9, 14

   from conans import ConanFile, AutoToolsBuildEnvironment

   class ExampleConan(ConanFile):

      ...

      def _run_cmd(self, command):
        if self.settings.os == "Windows":
            tools.run_in_windows_bash(self, command)
        else:
            self.run(command)

      def build(self):
         env_build = AutoToolsBuildEnvironment(self)
         with tools.environment_append(env_build.vars):
            self._run_cmd("./configure")
            self._run_cmd("make")

Read more in :ref:`Building with autotools section <building_with_autotools>`.


