Troubleshooting
==================

ERROR: Missing prebuilt package
--------------------------------

When you are installing packages (with :command:`conan install` or :command:`conan create`) it is possible
that you get an error like the following one:


.. code-block:: text

    WARN: Can't find a 'libzmq/4.2.0@memsharded/testing' package for the specified options and settings:
    - Settings: arch=x86_64, build_type=Release, compiler=gcc, compiler.libcxx=libstdc++, compiler.version=4.9, os=Windows
    - Options: shared=False
    - Package ID: 7fe67dff831b24bc4a8b5db678a51f1be5e44e7c

    ERROR: Missing prebuilt package for 'libzmq/4.2.0@memsharded/testing'
    Try to build it from sources with "--build libzmq" or read "http://docs.conan.io/en/latest/faq.html"


This means that the package recipe ``libzmq/4.2.0@memsharded/testing`` exists, but for some reason
there is no precompiled package for your current settings. Maybe the package creator didn't build
and shared pre-built packages at all and only uploaded the package recipe, or maybe they are only
providing packages for some platforms or compilers. E.g. the package creator built packages
from the recipe for gcc 4.8 and 4.9, but you are using gcc 5.4.

By default, conan doesn't build packages from sources. There are several possibilities:

- You can try to build the package for your settings from sources, indicating some build
  policy as argument, like ``--build libzmq`` or ``--build missing``. If the package recipe and the source
  code work for your settings you will have your binaries built locally and ready for use.

- If building from sources fail, you might want to fork the original recipe, improve it until it
  supports your configuration, and then use it. Most likely contributing back to the original
  package creator is the way to go. But you can also upload your modified recipe and pre-built
  binaries under your own username too.


.. _error_invalid_setting:

ERROR: Invalid setting
------------------------

It might happen sometimes, when you specify a setting not present in the defaults
that you receive a message like this:

.. code-block:: bash

    $ conan install . -s compiler.version=4.19 ...

    ERROR: Invalid setting '4.19' is not a valid 'settings.compiler.version' value.
    Possible values are ['4.4', '4.5', '4.6', '4.7', '4.8', '4.9', '5.1', '5.2', '5.3', '5.4', '6.1', '6.2']
    Read "http://docs.conan.io/en/latest/faq/troubleshooting.html#error-invalid-setting"


This doesn't mean that such architecture is not supported by conan, it is just that it is not present in the actual
defaults settings. You can find in your user home folder ``~/.conan/settings.yml`` a settings file that you
can modify, edit, add any setting or any value, with any nesting if necessary. See :ref:`custom_settings`.

As long as your team or users have the same settings (you can share with them the file), everything will work. The *settings.yml* file is just a
mechanism so users agree on a common spelling for typical settings. Also, if you think that some settings would
be useful for many other conan users, please submit it as an issue or a pull request, so it is included in future
releases.

It is possible that some build helper, like ``CMake`` will not understand the new added settings,
don't use them or even fail.
Such helpers as ``CMake`` are simple utilities to translate from conan settings to the respective
build system syntax and command line arguments, so they can be extended or replaced with your own
one that would handle your own private settings.

ERROR: Setting value not defined
---------------------------------

When you install or create a package, it is possible to see an error like this:

.. code-block:: bash

    ERROR: Hello/0.1@user/testing: 'settings.arch' value not defined

This means that the recipe defined ``settings = "os", "arch", ...`` but a value for the ``arch`` setting was
not provided either in a profile or in the command line. Make sure to specify a value for it in your profile,
or in the command line:

.. code-block:: bash

    $ conan install . -s arch=x86 ...

If you are building a pure C library with gcc/clang, you might encounter an error like this:

.. code-block:: bash

    ERROR: Hello/0.1@user/testing: 'settings.compiler.libcxx' value not defined

Indeed, for building a C library, it is not necessary to define a C++ standard library. And if you provide a value,
you might end with multiple packages for exactly the same binary. What has to be done is to remove such subsetting
in your recipe:


.. code-block:: python

    def configure(self):
        del self.settings.compiler.libcxx


ERROR: Failed to create process
--------------------------------

When conan is installed via pip/PyPI, and python is installed in a path with spaces (like many times in Windows "C:/Program Files..."), conan can fail to launch. This is a known python issue, and can't be fixed from conan.
The current workarounds would be:

- Install python in a path without spaces
- Use virtualenvs. Short guide:

.. code-block:: bash

    $ pip install virtualenvwrapper-win # virtualenvwrapper if not Windows
    $ mkvirtualenv conan
    (conan) $ pip install conan
    (conan) $ conan --help

Then, when you will be using conan, for example in a new shell, you have to activate the virtualenv:

.. code-block:: bash

    $ workon conan
    (conan) $ conan --help

Virtualenvs are very convenient, not only for this workaround, but to keep your system clean and to avoid unwanted interaction between different tools and python projects.


ERROR: Failed to remove folder (Windows)
-----------------------------------------
It is possible that operating conan, some random exceptions (some with complete tracebacks) are produced, related to the impossibility to remove one folder. Two things can happen:

- The user has some file or folder open (in a file editor, in the terminal), so it cannot be removed, and the process fails. Make sure to close files, specially if you are opening or inspecting the local conan cache.
- In Windows, the Search Indexer might be opening and locking the files, producing random, difficult to reproduce and annoying errors. Please **disable the Windows Search Indexer for the conan local storage folder**


ERROR: Error while initializing Options
---------------------------------------

When installing a Conan package and the follow error occurs:

.. code-block:: bash

    ERROR: conanfile.py: Error while initializing options. Please define your default_options as list or multiline string

Probably your Conan version is outdated.
The error is related to `default_options` be used as dictionary and only can be handled by Conan >= 1.8.
To fix this error, update Conan to 1.8 or higher.


ERROR: Error while starting Conan Server with multiple workers
--------------------------------------------------------------

When running ``gunicorn`` to start ``conan_server`` in an empty environment:

.. code-block:: bash

    $ gunicorn -b 0.0.0.0:9300 -w 4 -t 300 conans.server.server_launcher:app

        **********************************************
        *                                            *
        *      ERROR: STORAGE MIGRATION NEEDED!      *
        *                                            *
        **********************************************
        A migration of your storage is needed, please backup first the storage directory and run:

        $ conan_server --migrate

Conan Server will try to create `~/.conan_server/data`, `~/.conan_server/server.conf` and `~/.conan_server/version.txt` at first time.
However, as multiple workers are running at same time, it could result in a conflict.
To fix this error, you should run:

.. code-block:: bash

    $ conan_server --migrate

This command must be executed before to start the workers. It will not migrate anything, but it will populate the conan_server folder.
The original discussion about this error is `here <https://github.com/conan-io/conan/issues/4723>`_.
