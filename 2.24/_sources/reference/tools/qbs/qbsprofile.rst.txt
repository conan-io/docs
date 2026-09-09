.. _conan_tools_qbsprofile:

QbsProfile
===========

The ``QbsProfile`` generator produces the settings file that contains toolchain information.
This file can be imported into Qbs. The ``QbsProfile`` generator can be used like:

.. code-block:: python

    from conan import ConanFile

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        requires = "hello/0.1"
        generators = "QbsProfile"


It is also possible to use ``QbsProfile`` manually in the ``generate()`` method:

.. code-block:: python

    from conan import ConanFile
    from conan.tools.qbs import QbsProfile

    class App(ConanFile):
        settings = "os", "arch", "compiler", "build_type"
        requires = "hello/0.1"

        def generate(self):
            profile = QbsProfile(self)
            profile.generate()

Now we can generate the file using the ``conan install`` command.

.. code-block:: text

    $ conan install . --output-folder=build --build missing

And import it into Qbs:

.. code-block:: text

    $ qbs config import qbs_settings.txt --settings-dir qbs

Note that to acutually use the imported file, Qbs should be called with ``--settings-dir``:

.. code-block:: text

    $ qbs resolve --settings-dir qbs

Those commands are called automatically when using the ``Qbs`` helper class.
.. seealso::

    - Check the :ref:`Qbs helper <_conan_tools_qbs_helper>` for details.

Reference
---------

.. currentmodule:: conan.tools.qbs.qbsprofile

.. autoclass:: QbsProfile
    :members: