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

To install latest Conan 2.0 pre-release version using ``pip``, you need a Python >= 3.6
distribution installed on your machine. Modern Python distros come with pip pre-installed.
However, if necessary you can install pip by following the instructions in `pip docs`_.


Install Conan:

.. code-block:: bash

    $ pip install conan --pre

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

Install from source
-------------------

You can run Conan directly from source code. First, you need to install Python and pip.

Clone (or download and unzip) the git repository and install it.

Conan 2 is still in alpha stage, so you must check the `develop2` branch of the repository:

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

.. _conan_update:

Update
------

If installed via ``pip``, Conan 2.0 pre-release version can be easily updated:

.. code-block:: bash

    $ pip install conan --pre --upgrade  # Might need sudo or --user

The default ``<userhome>/.conan/settings.yml`` file, containing the definition of compiler versions, etc.,
will be upgraded if Conan does not detect local changes, otherwise it will create a ``settings.yml.new`` with the new settings.
If you want to regenerate the settings, you can remove the ``settings.yml`` file manually and it will be created with the new information the first time it is required.

The upgrade shouldn't affect the installed packages or cache information. If the cache becomes inconsistent somehow, you may want to remove its content by deleting it (``<userhome>/.conan``).


.. _`pip docs`: https://pip.pypa.io/en/stable/installing/
