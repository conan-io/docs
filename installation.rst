.. _install:

Install
=======

Conan can be installed on many operating systems. It has been extensively used and tested on Windows, Linux (different distributions),
and OS X, and is also actively used on FreeBSD and Solaris SunOS. There are also several additional operating systems on which it has been reported to work.

There are three ways to install conan:

1. The preferred and **strongly recommended way to install Conan** is from PyPI, the Python Package Index,
   using the ``pip`` command.
2. There are other available installers for different systems, which might come with a bundled
   python interpreter, so that you don't have to install python first. Please note that **some of these installers might have some limitations**, especially those created with pyinstaller (such as Windows exe & Linux deb).
3. Running Conan from sources.

Install with pip (recommended)
--------------------------------

To install Conan using ``pip``, you need a Python 2.7 or 3.X distribution installed in your machine. Modern Python distributions come
with pip pre-installed, however, if necessary you can install pip by following the instructions in `pip docs`_

Install conan:

::

    $ pip install conan

.. note::

    **IMPORTANT: Please READ carefully**:

    - Please make sure that your **pip** installation matches your **Python (2.7 or 3.X)** version.
    - In Linux, if you want to install it globally, you might need **sudo** permissions.
    - We strongly recommend using **virtualenvs** (virtualenvwrapper works great) for everything Python related
    - In **Windows** the *Indexing service* can interact badly with the conan local cache. It is strongly recommended to exclude the ``<userhome>/.conan`` folder from Indexing Service. Important in CI machines.
    - In **Windows** and with Python 2.7, you might need to use **32bits** Python distribution (which is the Windows default one), instead of 64bits.
    - In **OSX**, especially in the latest versions that might have **System Integrity Protection**, pip might fail. Try with virtualenvs, or install with other user ``$ pip install --user conan``
    - If you are on Windows, and using a Python version below 3.5, you might have problems if pPython is installed in a path with spaces such as "C:/Program Files(x86)/Python". This is a known limitation of Python, not Conan. To overcome this limitation, install Python in a path without spaces, use a virtualenv in another location or upgrade your Python installation.
    - In some Linux distros, like Linux Mint, it is possible that you need a restart (shell restart, or logout/system if not enough) after installation, so conan is found in the path.


Install using Brew (OS X)
-------------------------
There is a Brew recipe, so in OS X, you can install Conan as follows:

::

    $ brew update
    $ brew install conan
    
    
Install using AUR (Arch Linux)
------------------------------
You can find the package `here <https://aur.archlinux.org/packages/conan/>`_.
The easiest way is using **pacaur** tool:

::

    $ pacaur -S conan


You can also use ``makepkg`` and install it as described in `AUR docs: installing packages <https://wiki.archlinux.org/index.php/Arch_User_Repository>`_.

Make sure to first install the following four Conan dependencies. They are not in the official
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

    You can also use the latest version's links to download the latest installer:

    .. code-block:: text

        http://downloads.conan.io/latest_debian
        http://downloads.conan.io/latest_windows


Initial configuration
---------------------

Let's check if conan is correctly installed. In your console, run the following:

.. code-block:: bash

    $ conan

You will see something like:

.. code-block:: bash

    Conan commands. Type $conan "command" -h for help
        alias          Creates and export an alias recipe
        build          Utility command to run your current project 'conanfile.py' build() method.
        config         Manages conan configuration information
        copy           Copy conan recipes and packages to another user/channel.
        ...


Install from source
-------------------

You can run conan directly from source code. First you need to install Python 2.7 or Python 3 and
pip.

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
