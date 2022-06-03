.. _conan_conanfile_model_conf_info:


self.conf_info
--------------

Allow to declare, remove and modify configurations that are passed to the dependant recipes.

.. currentmodule:: conans.model.conf

.. automethod:: Conf.define

    .. code-block:: python

        def package_info(self):
            # Setting values
            self.conf_info.define("tools.microsoft.msbuild:verbosity", "Diagnostic")
            self.conf_info.define("tools.system.package_manager:sudo", True)
            self.conf_info.define("tools.microsoft.msbuild:max_cpu_count", 2)
            self.conf_info.define("user.myconf.build:ldflags", ["--flag1", "--flag2"])
            self.conf_info.define("tools.microsoft.msbuildtoolchain:compile_options", {"ExceptionHandling": "Async"})

.. automethod:: Conf.get

    .. code-block:: python

        def package_info(self):
            self.conf_info.get("tools.microsoft.msbuild:verbosity")  # == "Diagnostic"
            # Getting default values from configurations that don't exist yet
            self.conf_info.get("user.myotherconf.build:cxxflags", default=["--flag3"])  # == ["--flag3"]
            # Getting values and ensuring the gotten type is the passed one otherwise an exception will be raised
            self.conf_info.get("tools.system.package_manager:sudo", check_type=bool)  # == True
            self.conf_info.get("tools.system.package_manager:sudo", check_type=int)  # ERROR! It raises a ConanException



.. automethod:: Conf.pop

    .. code-block:: python

        def package_info(self):
            value = self.conf_info.pop("tools.system.package_manager:sudo")

.. automethod:: Conf.append

    .. code-block:: python

        def package_info(self):
            # Modifying configuration list-like values
            self.conf_info.append("user.myconf.build:ldflags", "--flag3")  # == ["--flag1", "--flag2", "--flag3"]


.. automethod:: Conf.prepend


    .. code-block:: python

        def package_info(self):
            self.conf_info.prepend("user.myconf.build:ldflags", "--flag0")  # == ["--flag0", "--flag1", "--flag2", "--flag3"]

.. automethod:: Conf.update


    .. code-block:: python

        def package_info(self):
            # Modifying configuration dict-like values
            self.conf_info.update("tools.microsoft.msbuildtoolchain:compile_options", {"ExpandAttributedSource": "false"})


.. automethod:: Conf.remove


    .. code-block:: python

        def package_info(self):
            # Remove
            self.conf_info.remove("user.myconf.build:ldflags", "--flag1")  # == ["--flag0", "--flag2", "--flag3"]


.. automethod:: Conf.unset


    .. code-block:: python

        def package_info(self):
            # Unset any value
            self.conf_info.unset("tools.microsoft.msbuildtoolchain:compile_options")
