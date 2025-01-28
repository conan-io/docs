.. _install:

Install
=======

Conan can be installed in many Operating Systems. It has been extensively used and tested in Windows, Linux (different distros), OSX, and is
also actively used in FreeBSD and Solaris SunOS. There are also several additional operating systems on which it has been reported to work.

There are three ways to install Conan:

1. The preferred and **strongly recommended way to install Conan** is from PyPI, the Python Package Index, using the ``pip`` command.
2. There are other available installers for different systems, which might come with a bundled python interpreter, so that you don't have to
   install python first. Note that some of **these installers might have some limitations**, specially those created with pyinstaller
   (such as Windows exe & Linux deb).
3. Running Conan from sources.

Install with pip (recommended)
------------------------------

To install Conan using ``pip``, you need Python 2.7 or 3.X distribution installed on your machine. Modern Python distros come
with pip pre-installed. However, if necessary you can install pip by following the instructions in `pip docs`_.

.. warning::

    Python 2 will soon be deprecated by the Python maintainers. It is strongly recommended to use Python 3 with Conan, especially if need to manage non-ascii filenames or file contents.
    Conan still supports Python 2, however some of the dependencies have started to be supported only by Python 3. See :ref:`python2` for details.

Install Conan:

.. code-block:: bash

    $ pip install conan

.. important::

    **Please READ carefully**

    - Make sure that your **pip** installation matches your **Python (2.7 or 3.X)** version.
    - In **Linux**, you may need **sudo** permissions to install Conan globally.
    - We strongly recommend using **virtualenvs** (virtualenvwrapper works great) for everything related to Python.
    - In **Windows** and Python 2.7, you may need to use **32bit** python distribution (which is the Windows default), instead
      of 64 bit.
    - In **OSX**, especially the latest versions that may have **System Integrity Protection**, pip may fail. Try using virtualenvs, or
      install with another user ``$ pip install --user conan``.
    - If you are using Windows and Python <3.5, you may have issues if Python is installed in a path with spaces, such as
      "C:/Program Files(x86)/Python". This is a known Python limitation, and is not related to Conan. Try installing Python in a path without spaces, use a
      virtualenv in another location or upgrade your Python installation.
    - Some Linux distros, such as Linux Mint, require a restart (shell restart, or logout/system if not enough) after
      installation, so Conan is found in the path.
    - Windows, Python 3 installation can fail installing the ``wrapt`` dependency because of a bug in **pip**. Information about this issue and
      workarounds is available here: https://github.com/GrahamDumpleton/wrapt/issues/112.
    - Conan works with Python 2.7, but not all features are available when not using Python 3.x starting with version 1.6

Install from brew (OSX)
-----------------------

There is a brew recipe, so in OSX, you can install Conan as follows:

.. code-block:: bash

    $ brew update
    $ brew install conan

Install from AUR (Arch Linux)
-----------------------------

The easiest way to install Conan on Arch Linux is by using one of the `Arch User Repository (AUR) helpers <https://wiki.archlinux.org/index.php/AUR_helpers>`_, e.g., **yay**, **aurman**, or **pakku**.
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

Check if Conan is installed correctly. Run the following command in your console:

.. code-block:: bash

    $ conan

The response should be similar to:

.. code-block:: bash

    Consumer commands
      install    Installs the requirements specified in a conanfile (.py or .txt).
      config     Manages configuration. Edits the conan.conf or installs config files.
      get        Gets a file or list a directory of a given reference or package.
      info       Gets information about the dependency graph of a recipe.
      ...

Install from source
-------------------

You can run Conan directly from source code. First, you need to install Python 2.7 or Python 3 and
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

Update
------

If installed via ``pip``, Conan can be easily updated:

.. code-block:: bash

    $ pip install conan --upgrade  # Might need sudo or --user

If installed via the installers (*.exe*, *.deb*), download the new installer and execute it.

The default *<userhome>/.conan/settings.yml* file, containing the definition of compiler versions, etc.,
will be upgraded if Conan does not detect local changes, otherwise it will create a *settings.yml.new* with the new settings. 
If you want to regenerate the settings, you can remove the *settings.yml* file manually and it will be created with the new information the first time it is required.

The upgrade shouldn't affect the installed packages or cache information. If the cache becomes inconsistent somehow, you may want to remove its content by deleting it (*<userhome>/.conan*).

.. _python2:

Python 2 Deprecation Notice
---------------------------

All features of Conan until version 1.6 are fully supported in both Python 2 and Python 3. However, new features in upcoming Conan releases
that are only available in Python 3 or more easily available in Python 3 will be implemented and tested only in Python 3, and versions of
Conan using Python 2 will not have access to that feature. This will be clearly described in code and documentation.

If and when Conan 2.x is released (Not expected in 2018) the level of compatibility with Python 2 may be reduced further.

We encourage you to upgrade to Python 3 as soon as possible. However, if this is impossible for you or your team, we would like to know it.
Please give feedback in the `Conan issue tracker`_ or write us to info@conan.io.

.. _`pip docs`: https://pip.pypa.io/en/stable/installing/

.. _`Conan issue tracker`: https://github.com/conan-io/conan/issues/3334
