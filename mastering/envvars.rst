Environment variables
=======================

There are several use cases for environment variables:

- Conan global configuration environment variables (e.g. ``CONAN_COMPRESSION_LEVEL``). They can be configured in *conan.conf* or as system
  environment variables, and control Conan behavior.
- Package recipes can access environment variables to determine their behavior. A typical example would be when launching CMake. It will
  check for CC and CXX environment variables to define the compiler to use. These variables are mostly transparent for Conan, and just used
  by the package recipes.
- Environment variables can be set in different ways:
   - global, at the OS level, with :command:`export VAR=Value` or in Windows :command:`SET VAR=Value`.
   - In the Conan command line: :command:`conan install -e VAR=Value`.
   - In profile files.
   - In package recipes in the ``self.env_info`` field, so they are activated for dependent recipes.

Defining environment variables
--------------------------------

You can use :ref:`profiles<profiles>` to define environment variables that will apply to your recipes. You can also use :command:`-e` parameter
in :command:`conan install`, :command:`conan info` and :command:`conan create` commands.

.. code-block:: text

    [env]
    CC=/usr/bin/clang
    CXX=/usr/bin/clang++

If you want to override an environment variable that a package has inherited from its requirements, you can use either **profiles** or
:command:`-e` to do it:

.. code-block:: bash

    conan install . -e MyPackage:PATH=/other/path

If you want to define an environment variable, but you want to append the variables declared in your requirements, you can use the ``[]``
syntax:

.. code-block:: bash

    $ conan install . -e PYTHONPATH=[/other/path]

This way the first entry in the PYTHONPATH variable will be */other/path*, but the PYTHONPATH values declared in the requirements
of the project will be appended at the end using the system path separator.

Automatic environment variables inheritance
-------------------------------------------

If your dependencies define some ``env_info`` variables in the ``package_info()`` method, they will be automatically applied before calling
the consumer *conanfile.py* methods ``source()``, ``build()``, ``package()`` and ``imports()``. You can read more about ``env_info`` object
:ref:`here <method_package_info_env_info>`.

For example, if you are creating a package for a tool, you can define the variable ``PATH``:

.. code-block:: python

    class ToolExampleConan(ConanFile):
       name = "my_tool_installer"
       ...

       def package_info(self):
           self.env_info.path.append(os.path.join(self.package_folder, "bin"))


If another Conan recipe requires the `my_tool_installer` in the ``source()``, ``build()``, ``package()`` and ``imports()``, the bin folder of
the ``my_tool_installer`` package will be automatically appended to the system PATH. If ``my_tool_installer`` packages an executable called
``my_tool_executable`` in the *bin* of the package folder, we can directly call the tool because it will be available in the path:

.. code-block:: python

    class MyLibExample(ConanFile):
       name = "my_lib_example"
       ...

       def build(self):
           self.run("my_tool_executable some_arguments")

You could also set ``CC``, ``CXX`` variables if we are packing a compiler to define what compiler to use or any other environment variable.
Read more about tool packages :ref:`here<create_installer_packages>`.
