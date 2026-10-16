.. _reference_tools_intel:

conan.tools.intel
=================

IntelCC
-------

This tool helps you to manage the Intel oneAPI `DPC++/C++ <https://software.intel.com/content/www/us/en/develop/documentation/oneapi-dpcpp-cpp-compiler-dev-guide-and-reference/top.html>`_ and
`Classic <https://software.intel.com/content/www/us/en/develop/documentation/cpp-compiler-developer-guide-and-reference/top.html>`_ ecosystem in Conan.

.. warning::

    This generator is **experimental** and subject to breaking changes.

.. warning::

    macOS is not supported for the Intel oneAPI DPC++/C++ (icx/icpx or dpcpp) compilers. For macOS or Xcode support, you'll have to use the Intel C++ Classic Compiler.

.. note::

    Remember, you need to have installed previously the `Intel oneAPI software <https://www.intel.com/content/www/us/en/developer/tools/oneapi/toolkits.html>`_.


This generator creates a ``conanintelsetvars.sh|bat`` wrapping the Intel script ``setvars.sh|bat`` that sets the Intel oneAPI
environment variables needed. That script is the first step to start using the Intel compilers because it's setting some
important variables in your local environment.

When your profile specifies ``compiler=intel-cc``, Conan automatically invokes the ``IntelCC`` generator.
You don't need to declare it explicitly in your conanfile.

.. note::

    If you explicitly set ``tools.intel:installation_path=""`` configuration
    (empty string), Conan will **not generate** the ``conanintelsetvars``
    script. In this case, you are expected to have already activated the Intel
    oneAPI environment manually.


At first, ensure you are using a *profile* like this one:

.. tabs::

   .. code-tab:: text Linux profile

        [settings]
        os=Linux
        arch=x86_64
        compiler=intel-cc
        compiler.mode=icx
        compiler.version=2026.0
        compiler.libcxx=libstdc++
        compiler.cppstd=gnu17
        build_type=Release

        [conf]
        tools.intel:installation_path=/opt/intel/oneapi

   .. code-tab:: text Windows profile

        [settings]
        os=Windows
        arch=x86_64
        compiler=intel-cc
        compiler.mode=icx
        compiler.version=2026.0
        compiler.runtime=dynamic
        compiler.cppstd=17
        build_type=Release

        [conf]
        tools.intel:installation_path=C:\Program Files (x86)\Intel\oneAPI


Compiler mode
+++++++++++++

Conan selects the appropriate compiler executables based on the ``compiler.mode`` setting:

- **icx mode**: Uses ``icx``/``icpx`` on Linux, or ``icx-cl`` on Windows (for MSVC compatibility)
- **dpcpp mode**: Uses ``icx``/``dpcpp``
- **classic mode**: Uses ``icc``/``icpc``

You typically don't need to specify ``tools.build:compiler_executables`` in your profile.
If you do specify it, it will take precedence over the auto-detected values.


.. _oneapi_sycl_support:

SYCL support
++++++++++++

.. warning::

    The ``dpcpp`` compiler is **deprecated** by Intel. The recommended way to compile SYCL code
    is to use ``icpx`` with the ``-fsycl`` flag.

To enable SYCL compilation, use the ``compiler.mode=icx`` setting and add the ``-fsycl`` flag
via the build configuration:


.. tabs::

   .. code-tab:: text Linux profile

        [settings]
        os=Linux
        arch=x86_64
        compiler=intel-cc
        compiler.mode=icx
        compiler.version=2026.0
        compiler.libcxx=libstdc++
        compiler.cppstd=gnu17
        build_type=Release

        [conf]
        tools.build:cxxflags=["-fsycl"]
        tools.build:exelinkflags=["-fsycl"]
        tools.build:sharedlinkflags=["-fsycl"]
        tools.intel:installation_path=/opt/intel/oneapi

   .. code-tab:: text Windows profile

        [settings]
        os=Windows
        arch=x86_64
        compiler=intel-cc
        compiler.mode=icx
        compiler.version=2026.0
        compiler.runtime=dynamic
        compiler.cppstd=17
        build_type=Release

        [conf]
        tools.build:cxxflags=["-fsycl"]
        tools.build:exelinkflags=["-fsycl"]
        tools.build:sharedlinkflags=["-fsycl"]
        tools.intel:installation_path=C:\Program Files (x86)\Intel\oneAPI


Custom configurations
++++++++++++++++++++++

Apply different installation paths and command arguments simply by changing the ``[conf]`` entries. For instance:

.. code-block:: text
    :caption: intelprofile

    [settings]
    ...
    compiler=intel-cc
    compiler.mode=icx
    compiler.version=2026.0
    compiler.libcxx=libstdc++
    build_type=Release

    [conf]
    tools.intel:installation_path=/opt/intel/oneapi
    tools.intel:setvars_args=--config="full/path/to/your/config.txt" --force

Run again a :command:`conan install . -pr intelprofile`, then the ``conanintelsetvars.sh`` script (if we are using Linux OS)
will contain something like:

.. code-block:: bash
    :caption: conanintelsetvars.sh

    . "/opt/intel/oneapi/setvars.sh" --config="full/path/to/your/config.txt" --force


The ``IntelCC`` generator can also be fully instantiated in the conanfile ``generate()`` method:

.. code-block:: python
    :caption: *conanfile.py*

    from conan import ConanFile
    from conan.tools.intel import IntelCC

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"

        def generate(self):
            intelcc = IntelCC(self)
            intelcc.generate()


Reference
---------

.. currentmodule:: conan.tools.intel

.. autoclass:: IntelCC
    :members:


conf
++++

``IntelCC`` uses these :ref:`configuration entries <reference_config_files_global_conf>`:

- ``tools.intel:installation_path``: **(required)** argument to tell Conan the
  installation path, if it's not defined, Conan will try to find it out
  automatically. If it is explicitly set to the empty string (``""``), Conan
  will **skip the generation** of the ``conanintelsetvars`` script, assuming the
  Intel environment has already been activated manually.
- ``tools.intel:setvars_args``: **(optional)** it is used to pass whatever we want as arguments to our `setvars.sh|bat` file.
  You can check out all the possible ones from the Intel official documentation.
