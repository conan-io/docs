.. _install:

Install
=======

Conan can be installed in many Operating Systems. It has been extensively used and tested in Windows, Linux (different distros), OSX, and is
also actively used in FreeBSD and Solaris SunOS. There are also several additional operating systems on which it has been reported to work.

There are three ways to install Conan:

1. The preferred and **strongly recommended way to install Conan** is from PyPI, the Python Package Index, using the ``pip`` command.
2. There are other available installers for different systems, which might come with a bundled python interpreter, so that you don't have to
   install python first. Note that some of **these installers might have some limitations**, especially those created with pyinstaller
   (such as Windows exe & Linux deb).
3. Running Conan from sources.

Install with pip (recommended)
------------------------------

To install Conan using ``pip``, you need Python>=3.6 distribution installed on your machine.

.. warning::

    **Python 2 has been deprecated on January 1st, 2020 by the Python maintainers** and from Conan 1.49 it will not be possible to run Conan with Python 2.7, and at least Python>=3.6 will be required. See :ref:`python2` for details.

Install Conan:

.. code-block:: bash

    $ pip install conan

.. important::

    **Please READ carefully**

    - Make sure that your **pip** installation matches your **Python>=3.6** version. Lower Python versions will not work.
    - In **Linux**, you may need **sudo** permissions to install Conan globally.
    - We strongly recommend using **virtualenvs** (virtualenvwrapper works great) for everything related to Python.
      (check https://virtualenvwrapper.readthedocs.io/en/stable/, or https://pypi.org/project/virtualenvwrapper-win/ in Windows)
      With Python 3, the built-in module ``venv`` can also be used instead (check https://docs.python.org/3/library/venv.html).
      If not using a **virtualenv** it is possible that conan dependencies will conflict with previously existing dependencies,
      especially if you are using Python for other purposes.
    - In **OSX**, especially the latest versions that may have **System Integrity Protection**, pip may fail. Try using virtualenvs, or
      install with another user ``$ pip install --user conan``.
    - Some Linux distros, such as Linux Mint, require a restart (shell restart, or logout/system if not enough) after
      installation, so Conan is found in the path.


Known installation issues with pip
++++++++++++++++++++++++++++++++++

- When Conan is installed with :command:`pip install --user <username>`, usually a new directory is created for it. However, the directory
  is not appended automatically to the `PATH` and the :command:`conan` commands do not work. This can usually be solved restarting the session of
  the terminal or running the following command:

  .. code-block:: bash

      $ source ~/.profile

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

Alternatively, build and install Conan manually using ``makepkg`` and ``pacman`` as described in `the Arch Wiki <https://wiki.archlinux.org/index.php/Arch_User_Repository#Installing_and_upgrading_packages>`_.
Conan build files can be downloaded from AUR: https://aur.archlinux.org/packages/conan/.
Make sure to first install the three Conan dependencies which are also found in AUR:

- python-patch-ng
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
      install    Installs the requirements specified in a recipe (conanfile.py or conanfile.txt).
      config     Manages Conan configuration.
      get        Gets a file or list a directory of a given reference or package.
      info       Gets information about the dependency graph of a recipe.
      ...

.. tip::

    If you are using Bash, there is a bash autocompletion project created by the community for Conan commands:
    https://gitlab.com/akim.saidani/conan-bashcompletion

Install from source
-------------------

You can run Conan directly from source code. First, you need to install Python and
pip.

Clone (or download and unzip) the git repository and install it with:

.. code-block:: bash

    # clone folder name matters, to avoid imports issues
    $ git clone https://github.com/conan-io/conan.git conan_src
    $ cd conan_src
    $ python -m pip install -e .

Test your ``conan`` installation.

.. code-block:: bash

    $ conan

You should see the Conan commands help.

.. _conan_update:

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

Python 2 Removal Notice
-----------------------

From version 1.49, Conan will not work with Python 2. This is because security vulnerabilities of Conan dependencies that haven't been addressed in Python 2, so the only alternative moving forward is to finally remove Python 2 suport.

Python 2 was officially declared End Of Life 2 years and a half now, and Conan 1.22 already declared Python 2 as not supported. Extra blockers have been added in previous Conan releases to make everyone aware. Now the security vulnerabilities that are out of our scope, makes impossible to move forward support for Python 2. Please upgrade to Python>=3.6 to continue using Conan>=1.49. 



If you have any issue installing Conan, please report in the `Conan issue tracker`_ or write us to info@conan.io.

.. _`pip docs`: https://pip.pypa.io/en/stable/installing/

.. _`Conan issue tracker`: https://github.com/conan-io/conan/issues/3334
