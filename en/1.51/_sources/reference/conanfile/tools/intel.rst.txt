.. _conan_tools_intel:


conan.tools.intel
===================


IntelCC
--------

Available since: `1.41.0 <https://github.com/conan-io/conan/releases>`_

This tool helps you to manage the new Intel oneAPI `DPC++/C++ <https://software.intel.com/content/www/us/en/develop/documentation/oneapi-dpcpp-cpp-compiler-dev-guide-and-reference/top.html>`_ and
`Classic <https://software.intel.com/content/www/us/en/develop/documentation/cpp-compiler-developer-guide-and-reference/top.html>`_ ecosystem in Conan.

.. warning::

    This generator is **experimental** and subject to breaking changes.

.. warning::

    macOS is not supported for the Intel oneAPI DPC++/C++ (icx/icpx or dpcpp) compilers. For macOS or Xcode support, you'll have to use the Intel C++ Classic Compiler.

.. note::

    Remember, you need to have installed previously the `Intel oneAPI software <https://www.intel.com/content/www/us/en/developer/tools/oneapi/toolkits.html>`_.

.. note::

    If you are using ``CMakeToolchain`` or ``MSBuildToolchain``, you don't need to use this generator. See :ref:`intel-cc compiler section<howto_intel_compiler>` for more information.


This generator creates a ``conanintelsetvars.sh|bat`` wrapping the Intel script ``setvars.sh|bat`` that set the Intel oneAPI environment variables needed.
That script is the first step to start using the Intel compilers because it's setting some important variables in your local environment.

In summary, the ``IntelCC`` generator:

#. Reads your profile ``[settings]`` and ``[conf]``.
#. Uses that information to generate a ``conanintelsetvars.sh|bat`` script with the command to load the Intel ``setvars.sh|bat`` script.
#. Then, you or the chosen generator will be able to run that script and use any Intel compiler to compile the project.

.. note::

    You can launch the ``conanintelsetvars.sh|bat`` before calling your intel compiler to build a project.
    Also, Conan will automatically call it in the conanfile ``build(self)`` method when running any command with ``self.run``.


At first, ensure you are using a *profile* like this one:

.. code-block:: text
    :caption: intelprofile

    [settings]
    ...
    compiler=intel-cc
    compiler.mode=dpcpp
    compiler.version=2021.3
    compiler.libcxx=libstdc++
    build_type=Release
    [options]

    [tool_requires]
    [env]
    CC=dpcpp
    CXX=dpcpp

    [conf]
    tools.intel:installation_path=/opt/intel/oneapi


The ``IntelCC`` generator can be used by name in conanfiles:

.. code-block:: python
    :caption: conanfile.py

    class Pkg(ConanFile):
        generators = "IntelCC"


.. code-block:: text
    :caption: conanfile.txt

    [generators]
    IntelCC

And it can also be fully instantiated in the conanfile ``generate()`` method:

.. code-block:: python
    :caption: conanfile.py

    from conan import ConanFile
    from conan.tools.intel import IntelCC

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            intelcc = IntelCC(self)
            intelcc.generate()


Now, running the command :command:`conan install . -pr intelprofile` will generate the ``conanintelsetvars.sh|bat`` script which will run the
Intel *setvars* script and load all the variables into your local environment.


Custom configurations
++++++++++++++++++++++

You can apply different installation paths and command arguments simply by changing the ``[conf]`` entries. For instance:

.. code-block:: text
    :caption: intelprofile

    [settings]
    ...
    compiler=intel-cc
    compiler.mode=dpcpp
    compiler.version=2021.3
    compiler.libcxx=libstdc++
    build_type=Release
    [options]

    [tool_requires]
    [env]
    CC=dpcpp
    CXX=dpcpp

    [conf]
    tools.intel:installation_path=/opt/intel/oneapi
    tools.intel:setvars_args=--config="full/path/to/your/config.txt" --force

If we run again a :command:`conan install . -pr intelprofile` then the ``conanintelsetvars.sh`` script (if we are using Linux OS) will contain something like:

.. code-block:: bash
    :caption: conanintelsetvars.sh

    . "/opt/intel/oneapi/setvars.sh" --config="full/path/to/your/config.txt" --force


conf
++++

These are the two different entries for ``IntelCC``:

- ``tools.intel:installation_path``: **(required)** argument to tells Conan the installation path, if it's not defined, Conan will try to find it out automatically.
- ``tools.intel:setvars_args``: **(optional)** it is used to pass whatever we want as arguments to our `setvars.sh|bat` file. You can check out all the possible ones from the Intel official documentation.
