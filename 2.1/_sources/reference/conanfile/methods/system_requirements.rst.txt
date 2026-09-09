.. _reference_conanfile_methods_system_requirements:


system_requirements()
=====================

The ``system_requirements()`` method can be used to call the system package managers to install packages at the system level. In general, this should be reduced to a minimum, system packages are not modeled dependencies, but it can be sometimes convenient to automate the installation of some system packages that are necessary for some Conan packages. For example, when creating a recipe to package the ``opencv`` library, we could realize that it needs in Linux the ``gtk`` libraries, but it might be undesired to create a package for them, because we want to make sure we use the system ones. We code


.. code-block:: python
    
    from conan import ConanFile
    from conan.tools.system.package_manager import Apt

    class OpenCV(ConanFile):
        name = "opencv"
        version = "4.0"
        
        def system_requirements(self):
            apt = Apt(self)
            apt.install(["libgtk-3-dev"], update=True, check=True)

For full reference of the built-in helpers for different system package managers read the :ref:`tools.system.package_manager documentation<conan_tools_system_package_manager>`.


Collecting system requirements
------------------------------

When ``system_requirements()`` uses some built-in ``package_manager`` helpers, it is possible to collect information about the installed or required system requirements.
If we have the following ``conanfile.py``:

.. code-block:: python

    from conan import ConanFile
    from conan.tools.system.package_manager import Apt

    class MyPkg(ConanFile):
        settings = "arch"

        def system_requirements(self):
            apt = Apt(self)
            apt.install(["pkg1", "pkg2"])

It is possible to display the installed system packages (with the default ``tools.system.package_manager:mode`` requirements will be checked, but not installed) with:

.. code-block:: bash

    # Assuming apt is the default or using explicitly
    #   -c tools.system.package_manager:tool=apt-get 
    $ conan install . --format=json
   "graph": {
        "nodes": [
            {
                "ref": "",
                "id": 0,
                "settings": {
                    "arch": "x86_64"
                },
                "system_requires": {
                    "apt-get": {
                        "install": [
                            "pkg1",
                            "pkg2"
                        ],
                        "missing": []
                    }
                },


A similar result can be obtained without even installing binaries, we could use the ``report`` or ``report-installed`` modes. The ``report`` mode displays the ``install``
packages, those are the packages that are required to be installed, irrespective of whether they are actually installed or not. The ``report`` mode does not check the system for those package, so it could even be ran in another OS:

.. code-block:: bash

    $ conan graph info . -c tools.system.package_manager:mode=report --format=json
    ...
    "system_requires": {
        "apt-get": {
            "install": [
                "pkg1",
                "pkg2"
            ]
        }
    }

On the other hand, the ``report-installed`` mode will do a check if the package is installed in the system or not, but not failing nor raising any error if it is not found:

.. code-block:: bash

    $ conan graph info . -c tools.system.package_manager:mode=report-installed --format=json
    ...
    "system_requires": {
        "apt-get": {
            "install": [
                "pkg1",
                "pkg2"
            ],
            "missing": [
                "pkg1",
                "pkg2"
            ]
        }
    }
