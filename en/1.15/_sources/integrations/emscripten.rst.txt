.. _emscripten:

|emscripten_logo| Emscripten
____________________________

It should be possible to build packages for `Emscripten <https://emscripten.org/>`__ (`asm.js <http://asmjs.org/>`_) via the following conan profile:

.. code-block:: text

  include(default)
  [settings]
  os=Emscripten
  arch=asm.js
  compiler=clang
  compiler.version=6.0
  compiler.libcxx=libc++
  [options]
  [build_requires]
  emsdk_installer/1.38.29@bincrafters/stable
  [env]

And the following conan profile is required for the `WASM <https://webassembly.org/>`_ (Web Assembly):

.. code-block:: text

  include(default)
  [settings]
  os=Emscripten
  arch=wasm
  compiler=clang
  compiler.version=6.0
  compiler.libcxx=libc++
  [options]
  [build_requires]
  emsdk_installer/1.38.29@bincrafters/stable
  [env]

These profile above are using the `emsdk_installer/1.38.29@bincrafters/stable <https://github.com/bincrafters/conan-emsdk_installer>`_ conan package.
It will automatically download the `Emscripten SDK <https://github.com/emscripten-core/emsdk>`_ and set up required environment variables (like ``CC``, ``CXX``, etc.).

.. note::
   In order to use ``emsdk_installer`` package, you need to add it to the remotes:
   
   .. code-block:: bash

      $ conan remote add bincrafters https://api.bintray.com/conan/bincrafters/public-conan 

.. note:: 

   Alternatively, it's always possible to use an existing ``emsdk`` installation and manually specify required environment variables within the `[env]` section of the conan profile.

.. note:: 

   In addition to the above, Windows users may need to specify ``CONAN_MAKE_PROGRAM``,
   for instance from the existing MinGW installation (e.g. ``C:\MinGW\bin\mingw32-make.exe``), or use make from the ``mingw_installer/1.0@conan/stable``.

.. note:: 

   In addition to the above, Windows users may need to specify ``CONAN_CMAKE_GENERATOR``, e.g. to ``MinGW Makefiles``, because default one is Visual Studio.
   Other options (e.g. Ninja) work as well.

As specified, ``os`` has been set to the ``Emscripten``, and ``arch`` has been set to either ``asm.js`` or ``wasm`` (only these two are currently supported).
And ``compiler`` setting has been set to match the one used by ``Emscripten`` - Clang 6.0 with libc++ standard library.


Running the code inside the browser
-----------------------------------

.. note:: 

   Emscripten requires Python 2.7.12 or above, make sure that you have an up-to-date Python version installed.

.. note:: 

   Running demo on Windows may require pywin32 module. Install it by running ``pip install pywin32``.

In order to demonstrate how to use conan with Emscripten, let's check out the example project:

.. code-block:: bash

   $ git clone --depth 1 git@github.com:conan-io/examples.git

Change the directory to the Emscripten demo:

.. code-block:: bash

   $ cd features
   $ cd emscripten

This is an extremely simple demo, which just imports the famous `zlib <https://www.zlib.net/>`_ library and outputs its version into the browser.

In order to build it for the Emscripten run:

.. code-block:: bash

   $ ./build.sh

or (on Windows):

.. code-block:: bash

   $ ./build.cmd

Please note that running the above command may take a while to download and build required dependencies.
This script will execute several conan commands:

.. code-block:: bash

   $ conan remove conan-hello-emscripten/* -f
   $ conan create . conan/testing  -k -p emscripten.profile --build missing
   $ conan install conanfile.txt  -pr emscripten.profile

First one removes any traces of previous demo installations, just to ensure that environment is clean.
Then, it builds the simple demo (it uses ``CMakeLists.txt`` and ``main.cpp`` files from the current directory).
The following local profile is used (file ``emscripten.profile`` within the current directory):

.. code-block:: text

  include(default)
  [settings]
  os=Emscripten
  arch=wasm
  compiler=clang
  compiler.version=6.0
  compiler.libcxx=libc++
  [options]
  [build_requires]
  emsdk_installer/1.38.29@bincrafters/stable
  ninja_installer/1.8.2@bincrafters/stable
  [env]

Finally, it installs the demo importing ithe required files (``.html``, ``.js`` and ``.wasm``) into the ``bin`` subdirectory.

Then we can run the code inside the browser via `emrun <https://emscripten.org/docs/compiling/Running-html-files-with-emrun.html>`_ helper:

.. code-block:: bash

   $ ./run.sh

or (on Windows):

.. code-block:: bash

   $ ./run.cmd

The command above uses :ref:`virtualenv generator<virtual_environment_generator>` generator in order to get ``emrun`` command available in the ``PATH``.
And as the result, Web Browser should be opened (or new tab in Web Browser will be opened, if it was already run), and the following output should be displayed:

.. code-block:: bash

   $ Using zlib version: 1.2.11

It confirms the fact we have just built ``zlib`` into JavaScript and run it inside the Web Browser.

.. |emscripten_logo| image:: ../images/emscripten_logo.png
                     :width: 180px
