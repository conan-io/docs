.. _install:

Install
=======

Conan can be installed on many operating systems. It has been extensively used and tested on Windows, Linux (different distributions),
and OS X, and is also actively used on FreeBSD and Solaris SunOS. There are also several additional operating systems on which it has been reported to work.

There are three ways to install Conan:

1. The preferred and **strongly recommended way to install Conan** is from PyPI, the Python Package Index,
   using the ``pip`` command.
2. There are other available installers for different systems, which might come with a bundled
   python interpreter, so that you don't have to install python first. Please note that **some of these installers might have some limitations**, especially those created with pyinstaller (such as Windows exe & Linux deb).
3. Running Conan from sources.

Install with pip (recommended)
------------------------------

To install Conan using ``pip``, you need a Python 2.7 or 3.X distribution installed in your machine. Modern Python distributions come
with pip pre-installed, however, if necessary you can install pip by following the instructions in `pip docs`_

Install Conan:

::

    $ pip install conan

.. note::

    **IMPORTANT: Please READ carefully**:

    - Please make sure that your **pip** installation matches your **Python (2.7 or 3.X)** version.
    - In Linux, if you want to install it globally, you might need **sudo** permissions.
    - We strongly recommend using **virtualenvs** (virtualenvwrapper works great) for everything Python related.
    - In **Windows**, you might need to use the **32bits** Python distributio, instead of 64bits.
    - In **OS X**, especially in the latest versions that might have **System Integrity Protection**, pip might fail. Try using virtualenvs, or install with other user ``$ pip install --user conan``.
    - If you are on Windows, and using a Python version below 3.5, you might have problems if Python is installed in a path with spaces such as "C:/Program Files(x86)/Python". This is a known limitation of Python, not Conan. To overcome this limiation, install Python in a path without spaces, use a virtualenv in another location or upgrade your Python installation.


Install using Brew (OS X)
-------------------------
There is a Brew recipe, so in OS X, you can install Conan as follows:

::

    $ brew update
    $ brew install conan
    
    
Install using AUR (Arch Linux)
------------------------------
You can find the package `here <https://aur.archlinux.org/packages/conan/>`_.
The easiest way is to using **pacaur** tool as follows:

::

    $ pacaur -S conan


You can also use ``makepkg`` and install it as described in `AUR docs: installing packages <https://wiki.archlinux.org/index.php/Arch_User_Repository>`_.

Make sure to first install the following six Conan dependencies. They are not in the official
repositories but are available in the **AUR** repository:

- python-patch 
- python-monotonic
- python-fasteners
- python-node-semver
- python-distro
- python-pluginbase


Install the binaries
--------------------

Go to the Conan website and `download the installer for your platform <https://www.conan.io/downloads>`_.

Execute the installer. You don't need to install python.

.. note::

    You can also use the latest version links to download the latest installer:

    :: 
    
        http://downloads.conan.io/latest_debian
        http://downloads.conan.io/latest_windows


Initial configuration
---------------------

Let's check if conan is correctly installed. In your console, run the following:

.. code-block:: bash

   $ conan

You will see something like:

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

As you can see, upon first execution, Conan performs a basic detection of your installed tools and
saves the details in the **conan.conf** file (under your user home directory **~/.conan/conan.conf**).
These auto-detected settings are just a convenience and act as a default for your Conan commands.
You can change them at any time in this file or override them on the command line with new values.
You can also delete them from **conan.conf**, in which case you will have to fully specify them for
new projects.


Install from source
-------------------

You can run Conan directly from source code. First you need to install Python 2.7 and pip.
From version 0.9, Conan also has "experimental/testing" support for Python3.

Clone (or download and unzip) the git repository and install its requirements:

.. code-block:: bash

    $ git clone https://github.com/conan-io/conan.git
    $ cd conan
    $ pip install -r conans/requirements.txt

Create a script to run Conan and add it to your ``PATH``.

.. code-block:: text

    #!/usr/bin/env python

    import sys

    conan_repo_path = "/home/your_user/conan" # ABSOLUTE PATH TO CONAN REPOSITORY FOLDER

    sys.path.append(conan_repo_path)
    from conans.client.command import main
    main(sys.argv[1:])

Test your ``conan`` script.

.. code-block:: bash

    $ conan

You should see the Conan commands help.


.. _`pip docs`: https://pip.pypa.io/en/stable/installing/
