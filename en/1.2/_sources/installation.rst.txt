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

You can find the package `here <https://aur.archlinux.org/packages/conan/>`_. The easiest way is using **pacaur** tool:

.. code-block:: bash

    $ pacaur -S conan

Or you can also use ``makepkg`` and install it following the `AUR docs: installing packages
<https://wiki.archlinux.org/index.php/Arch_User_Repository>`_.

Just remember to install four Conan dependencies first. They are not in the official repositories but there are in **AUR** repository too:

- python-patch 
- python-node-semver
- python-distro
- python-pluginbase

Install the binaries
--------------------

Go to the conan website and `download the installer for your platform <https://www.conan.io/downloads.html>`_!

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
