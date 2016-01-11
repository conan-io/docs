.. _install:

Install
=======

To install the conan client you can use one of the provided installers, or run it
directly from source code.

Install the binaries
--------------------

Go to the conan website and `download the installer for your platform <https://www.conan.io/downloads>`_!

Execute the installer. You don't need to install python.

.. note::

    You can use the latest version's links to download the latest installer:

    :: 
    
        http://downloads.conan.io/latest_debian
        http://downloads.conan.io/latest_windows
        http://downloads.conan.io/latest_macos


Install with pip
----------------

- Install pip following `pip docs`_

- Install conan:

::

    $ pip install conan


Initial configuration
---------------------

Let's check if conan is correctly installed. Execute in your console:

.. code-block:: bash

   $ conan

You will see something similar to:

.. code-block:: bash

   It seems to be the first time you run conan
   Auto detecting your dev setup to initialize conan.conf
   Found Visual Studio 9
   Found Visual Studio 12
   Found Visual Studio 14
   Found gcc 4.8
   Found clang 3.7
   Default conan.conf settings
           os=Windows
           arch=x86_64
           compiler=Visual Studio
           compiler.version=14
           compiler.runtime=MD
           build_type=Release
   *** You can change them in ~/.conan/conan.conf ***
   *** Or override with -s compiler='other' -s ...s***

As you can see, on first execution, conan performs a basic detection of your installed tools and
saves the details in the **conan.conf** file (under your user home directory **~/.conan/conan.conf**).
These auto-detected settings are just a convenience and act as a default for your conan commands.
You can change them at any time in this file or override them on the command line with new values.
You can also delete them from **conan.conf**, in which case you will have to fully specify them for
new projects.


Install from source
-------------------

You can run conan directly from source code. First you need to install Python 2.7 and pip.

Clone (or download and unzip) the git repository and install its requirements:

.. code-block:: bash

    $ git clone https://github.com/conan-io/conan.git
    $ cd conan
    $ pip install -r conans/requirements.txt

Create a script to execute conan and add it to your ``PATH``.

.. code-block:: text

    #!/usr/bin/env python

    import sys

    conan_repo_path = "/home/your_user/conan" # ABSOLUTE PATH TO CONAN REPOSITORY FOLDER

    sys.path.append(conan_repo_path)
    from packet.client.command import main
    main(sys.argv[1:])

Test your ``conan`` script.

.. code-block:: bash

    $ conan

You should see the conan commands help.


.. _`pip docs`: https://pip.pypa.io/en/stable/installing/
