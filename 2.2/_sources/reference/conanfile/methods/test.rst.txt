.. _reference_conanfile_methods_test:


test()
======

The ``test()`` method is only used for **test_package/conanfile.py**.
It will execute immediately after ``build()`` has been called, and its goal is to run some executable or tests on binaries to prove the package is correctly created.
Note that it is intended to be used as a test of the package: the headers are found, the libraries are found,
it is possible to link, etc. But it is **not intended** to run unit, integration or functional tests.

It usually takes the form of:

.. code:: python

    def test(self):
        if can_run(self):
            cmd = os.path.join(self.cpp.build.bindir, "example")
            self.run(cmd, env="conanrun")


.. seealso::
    
    See :ref:`the "testing packages" tutorial<tutorial_creating_test>` for more information.
