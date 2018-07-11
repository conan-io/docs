.. _install:

Install
=======

Conan can be installed in many Operating Systems. It has been extensively used and tested in Windows, Linux (different distros), OSX, and is
also actively used in FreeBSD and Solaris SunOS. There are also several additional operating systems on which it has been reported to work.

There are three ways to install conan:

1. The preferred and **strongly recommended way to install Conan** is from PyPI, the Python Package Index, using the ``pip`` command.
2. There are other available installers for different systems, which might come with a bundled python interpreter, so that you don't have to
   install python first. Please note that some of **these installers might have some limitations**, specially those created with pyinstaller
   (such as Windows exe & Linux deb).
3. Running conan from sources.

Install with pip (recommended)
------------------------------

To install Conan using ``pip``, you need a python 2.7 or 3.X distribution installed in your machine. Modern python distros come 
with pip pre-installed. However, if necessary you can install pip by following the instructions in `pip docs`_.

.. warning::

    Python 2 will by deprecated soon by the Python maintainers. It is strongly recommended to use Python 3 for conan, especially if need to manage non-ascii filenames or file contents.
    Conan still supports Python 2, but some of the dependencies have started to be Python 3 only too. The roadmap for deprecating Python 2 support in Conan will be defined soon.

Install conan:

.. code-block:: bash

    $ pip install conan

.. important::

    **Please READ carefully**

    - Make sure that your **pip** installation matches your **python (2.7 or 3.X)** one.
    - In Linux if you want to install it globally, you might need **sudo** permissions.
    - We strongly recommend using **virtualenvs** (virtualenvwrapper works great) for everything python related
    - In **Windows** and with Python 2.7, you might need to use **32bits** python distribution (which is the Windows default one), instead
      of 64 bits.
    - In **OSX**, specially latest versions that might have **System Integrity Protection**, pip might fail. Try with virtualenvs, or
      install with other user ``$ pip install --user conan``.
    - If you are in Windows, and using python <3.5, you might have problems if python is installed in a path with spaces, like
      "C:/Program Files(x86)/Python". This is a known python's limitation, not Conan's. Install python in a path without spaces, use a
      virtualenv in another location or upgrade your python installation.
    - In some Linux distros, like Linux Mint, it is possible that you need a restart (shell restart, or logout/system if not enough) after
      installation, so Conan is found in the path.
    - Windows, Python 3 installation can fail installing the ``wrapt`` dependency because a bug in **pip**. Information about the issue and 
      workarounds is here: https://github.com/GrahamDumpleton/wrapt/issues/112. 

Install from brew (OSX)
-----------------------

There is a brew recipe, so in OSX, you can install Conan as follows:

.. code-block:: bash

    $ brew update
    $ brew install conan

Install from AUR (Arch Linux)
-----------------------------

The easiest way to install Conan on Arch Linux is by using one of the `Arch User Repository (AUR) helpers <https://wiki.archlinux.org/index.php/AUR_helpers#Active>`_, eg. **yay**, **aurman**, or **pakku**.
For example, the following command installs Conan using ``yay``:

.. code-block:: bash

    $ yay -S conan

Alternatively, build and install Conan manually using ``makepkg`` and ``pacman`` as described in `the Arch Wiki <https://wiki.archlinux.org/index.php/Arch_User_Repository#Installing_packages>`_.
Conan build files can be downloaded from AUR: https://aur.archlinux.org/packages/conan/.
Make sure to first install the three Conan dependencies which are also found in AUR:

- python-patch 
- python-node-semver
- python-pluginbase


Install the binaries
--------------------

Go to the conan website and `download the installer for your platform <https://conan.io/downloads.html>`_!

Execute the installer. You don't need to install python.


Initial configuration
---------------------

Let's check if conan is correctly installed. In your console, run the following:

.. code-block:: bash

    $ conan

You will see something similar to:

.. code-block:: bash

    Consumer commands
      install    Installs the requirements specified in a conanfile (.py or .txt).
      config     Manages configuration. Edits the conan.conf or installs config files.
      get        Gets a file or list a directory of a given reference or package.
      info       Gets information about the dependency graph of a recipe.
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
