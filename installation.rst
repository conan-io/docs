.. _install:

Install
=======

Conan can be installed in many Operating Systems. It has been extensively used and tested in Windows, Linux (different distros), OSX, and is
also actively used in FreeBSD and Solaris SunOS. There are also several additional operating systems on which it has been reported to work.

There are different ways to install Conan:

1. The preferred and **strongly recommended way to install Conan** is from PyPI, the Python Package Index, using the ``pip`` command.
2. Use a system installer, or create your own self-contained Conan executable, to not require Python in your system.
3. Running Conan from sources.

Install with pip (recommended)
------------------------------

To install latest Conan 2 version using ``pip``, you need a Python >= 3.6
distribution installed on your machine. Modern Python distros come with pip pre-installed.
However, if necessary you can install pip by following the instructions in `pip docs`_.


Install Conan:

.. code-block:: bash

    $ pip install conan

.. important::

    **Please READ carefully**

    - Make sure that your **pip** installation matches your **Python (>= 3.6)** version.
    - In **Linux**, you may need **sudo** permissions to install Conan globally.
    - We strongly recommend using **virtualenvs** (virtualenvwrapper works great) for everything related to Python.
      (check https://virtualenvwrapper.readthedocs.io/en/stable/, or https://pypi.org/project/virtualenvwrapper-win/ in Windows)
      With Python 3, the built-in module ``venv`` can also be used instead (check https://docs.python.org/3/library/venv.html).
      If not using a **virtualenv** it is possible that conan dependencies will conflict with previously existing dependencies,
      especially if you are using Python for other purposes.
    - In **OSX**, especially the latest versions that may have **System Integrity Protection**, pip may fail. Try using virtualenvs, or
      install it to the Python user install directory with ``$ pip install --user conan``.
    - Some Linux distros, such as Linux Mint, require a restart (shell restart, or logout/system if not enough) after
      installation, so Conan is found in the path.


Known installation issues with pip
++++++++++++++++++++++++++++++++++

When Conan is installed with :command:`pip install --user conan`, a new directory is usually created for it. However, the directory is not appended automatically to the `PATH` and the :command:`conan` commands do not work. This can usually be solved by restarting the session of the terminal or running the following command:

  .. code-block:: bash

      $ source ~/.profile


.. _conan_update:

Update
++++++

If installed via ``pip``, Conan version can be updated with:

.. code-block:: bash

    $ pip install conan --upgrade  # Might need sudo or --user

The upgrade shouldn't affect the installed packages or cache information. If the cache becomes inconsistent somehow, you may want to remove its content by deleting it (``<userhome>/.conan2``).


Install with pipx
-----------------

In certain scenarios, attempting to install with ``pip`` may yield the following error:

.. code-block:: bash

    error: externally-managed-environment

    x This environment is externally managed
        To install Python packages system-wide, try apt install
        python3-xyz, where xyz is the package you are trying to
        install.
    ...

This is because some modern Linux distributions have started marking their Python
installations as "externally managed", which means that the system's package manager is
responsible for managing Python packages. Installing packages globally or even in the user
space can interfere with system operations and potentially break system tools (check
`PEP-668 <https://peps.python.org/pep-0668/>`_ for more detailed information).

For those cases, it's recommended to use ``pipx`` to install Conan. ``pipx`` creates a virtual
environment for each Python application, ensuring that dependencies do not conflict. The
advantage is that it isolates Conan and its dependencies from the system Python and avoids
potential conflicts with system packages while providing a clean environment for Conan to
run.

To install Conan with ``pipx``:

1. Ensure ``pipx`` is installed on your system. If it isn't, check the installation
   guidelines `in the pipx documentation <https://pypa.github.io/pipx/installation/>`_. For
   Debian-based distributions, you can install ``pipx`` using the system package manager:

.. code-block:: bash

    $ apt-get install pipx
    $ pipx ensurepath

(Note: The package name might vary depending on the distribution)

2. Restart your terminal and then install Conan using ``pipx``: 

.. code-block:: bash

    $ pipx install conan

3. Now you can use Conan as you typically would.


Use a system installer or create a self-contained executable
------------------------------------------------------------

There will be a number of existing installers in `Conan downloads`_ for OSX Brew, Debian, Windows, Linux Arch, that will not require Python first.

We also distribute `Conan binaries`_ for Windows, Linux, and macOS in a compressed file
that you can uncompress in your system and run directly.

.. warning::

    If you are using **macOS**, please be aware of the Gatekeeper feature that may
    quarantine the compressed binaries if downloaded directly using a web browser. To
    avoid this issue, download them using a tool such as `curl`, `wget`, or similar.


If there is no installer for your platform, you can create your own Conan executable, with the ``pyinstaller.py`` utility in the repo. This process is able to create a self-contained Conan executable that contains all it needs,
including the Python interpreter, so it wouldn't be necessary to have Python installed in the system.

You can do it with: 

.. code-block:: bash

  $ git clone https://github.com/conan-io/conan conan_src
  $ cd conan_src
  $ git checkout develop2 # or to the specific tag you want to
  $ pip install -e . 
  $ python pyinstaller.py


It is important to install the dependencies and the project first with ``pip install -e .`` which configures the project as "editable", that is, to run from the current source folder. After creating the executable, it can be uninstalled with pip.

This has to run in the same platform that will be using the executable, pyinstaller does not cross-build. The resulting executable can be just copied and put in the system PATH of the running machine to be able to run Conan.


Install from source
-------------------

You can run Conan directly from source code. First, you need to install Python and pip.

Clone (or download and unzip) the git repository and install it.

Conan 2 is still in beta stage, so you must check the `develop2` branch of the repository:

.. code-block:: bash

    # clone folder name matters, to avoid imports issues
    $ git clone https://github.com/conan-io/conan.git conan_src
    $ cd conan_src
    $ git fetch --all
    $ git checkout -b develop2 origin/develop2
    $ python -m pip install -e .

And test your ``conan`` installation:

.. code-block:: bash

    $ conan

You should see the Conan commands help.


.. _`pip docs`: https://pip.pypa.io/en/stable/installing/
.. _`Conan downloads`: https://conan.io/downloads
.. _`Conan binaries`: https://github.com/conan-io/conan/releases/latest
