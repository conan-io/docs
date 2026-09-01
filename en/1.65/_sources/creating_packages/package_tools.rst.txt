.. _package_tools:

Package Creator Tools
=====================

Using Python (or just pure shell or bash) scripting, allows you to easily automate the whole package
creation and testing process, for many different configurations. For example you could put the
following script in the package root folder. Name it *build.py*:

.. code-block:: python

    import os, sys
    import platform

    def system(command):
        retcode = os.system(command)
        if retcode != 0:
            raise Exception("Error while executing:\n\t %s" % command)

    if __name__ == "__main__":
        params = " ".join(sys.argv[1:])

        if platform.system() == "Windows":
            system('conan create . demo/testing -s compiler="Visual Studio" -s compiler.version=14 %s' % params)
            system('conan create . demo/testing -s compiler="Visual Studio" -s compiler.version=12 %s' % params)
            system('conan create . demo/testing -s compiler="gcc" -s compiler.version=4.8 %s' % params)
        else:
            pass

This is a pure Python script, not related to Conan, and should be run as such:

.. code:: bash

   $ python build.py
