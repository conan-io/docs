.. _plugins_reference:

Plugins
=======

The Conan plugins are Python functions that are intended to extend the Conan functionalities and let users customize the client behavior at
determined execution points.

Storage, activation and sharing
-------------------------------

Plugins are Python files stored under *~/.conan/plugins* folder and their file name should be the same used for activation.

The activation of the plugins is done in the *conan.conf* section named ``[plugins]``. The plugin names listed under this section will be
considered activated.

.. code-block:: text
   :caption: *conan.conf*

    ...
    [plugins]
    attribute_checker
    conan-center

They can be easily activated and deactivated from the command line using the :command:`conan config set` command:

.. code-block:: bash

    $ conan config set plugins.attribute_checker  # Activates 'attribute_checker'

    $ conan config rm plugins.attribute_checker  # Deactivates 'attribute_checker'

There is also an environment varibale ``CONAN_PLUGINS`` to list the active plugins. Plugins listerd in *conan.conf* will be loaded into
this variable and values in the environment variable will be used to load the plugins.

Plugins are considered part of the Conan client configuration and can be shared as usual with the :ref:`conan_config_install` command.

Plugin structure
----------------

Here you can see a complete example of all the plugin functions available and the different parameters for each of them depending on the
context:

.. code-block:: python

    def pre_export(output, conanfile, conanfile_path, reference, **kwargs):
        assert conanfile
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % reference.full_repr())

    def post_export(output, conanfile, conanfile_path, reference, **kwargs):
        assert conanfile
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % reference.full_repr())

    def pre_source(output, conanfile, conanfile_path, **kwargs):
        assert conanfile
        output.info("conanfile_path=%s" % conanfile_path)
        if conanfile.in_local_cache:
            output.info("reference=%s" % kwargs["reference"].full_repr())

    def post_source(output, conanfile, conanfile_path, **kwargs):
        assert conanfile
        output.info("conanfile_path=%s" % conanfile_path)
        if conanfile.in_local_cache:
            output.info("reference=%s" % kwargs["reference"].full_repr())

    def pre_build(output, conanfile, **kwargs):
        assert conanfile
        if conanfile.in_local_cache:
            output.info("reference=%s" % kwargs["reference"].full_repr())
            output.info("package_id=%s" % kwargs["package_id"])
        else:
            output.info("conanfile_path=%s" % kwargs["conanfile_path"])

    def post_build(output, conanfile, **kwargs):
        assert conanfile
        if conanfile.in_local_cache:
            output.info("reference=%s" % kwargs["reference"].full_repr())
            output.info("package_id=%s" % kwargs["package_id"])
        else:
            output.info("conanfile_path=%s" % kwargs["conanfile_path"])

    def pre_package(output, conanfile, conanfile_path, **kwargs):
        assert conanfile
        output.info("conanfile_path=%s" % conanfile_path)
        if conanfile.in_local_cache:
            output.info("reference=%s" % kwargs["reference"].full_repr())
            output.info("package_id=%s" % kwargs["package_id"])

    def post_package(output, conanfile, conanfile_path, **kwargs):
        assert conanfile
        output.info("conanfile_path=%s" % conanfile_path)
        if conanfile.in_local_cache:
            output.info("reference=%s" % kwargs["reference"].full_repr())
            output.info("package_id=%s" % kwargs["package_id"])

    def pre_upload(output, conanfile_path, reference, remote, **kwargs):
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % reference.full_repr())
        output.info("remote.name=%s" % remote.name)

    def post_upload(output, conanfile_path, reference, remote, **kwargs):
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % reference.full_repr())
        output.info("remote.name=%s" % remote.name)

    def pre_upload_recipe(output, conanfile_path, reference, remote, **kwargs):
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % reference.full_repr())
        output.info("remote.name=%s" % remote.name)

    def post_upload_recipe(output, conanfile_path, reference, remote, **kwargs):
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % reference.full_repr())
        output.info("remote.name=%s" % remote.name)

    def pre_upload_package(output, conanfile_path, reference, package_id, remote, **kwargs):
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % reference.full_repr())
        output.info("package_id=%s" % package_id)
        output.info("remote.name=%s" % remote.name)

    def post_upload_package(output, conanfile_path, reference, package_id, remote, **kwargs):
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % reference.full_repr())
        output.info("package_id=%s" % package_id)
        output.info("remote.name=%s" % remote.name)

    def pre_download(output, reference, remote, **kwargs):
        output.info("reference=%s" % reference.full_repr())
        output.info("remote.name=%s" % remote.name)

    def post_download(output, conanfile_path, reference, remote, **kwargs):
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % reference.full_repr())
        output.info("remote.name=%s" % remote.name)

    def pre_download_recipe(output, reference, remote, **kwargs):
        output.info("reference=%s" % reference.full_repr())
        output.info("remote.name=%s" % remote.name)

    def post_download_recipe(output, conanfile_path, reference, remote, **kwargs):
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % reference.full_repr())
        output.info("remote.name=%s" % remote.name)

    def pre_download_package(output, conanfile_path, reference, package_id, remote, **kwargs):
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % reference.full_repr())
        output.info("package_id=%s" % package_id)
        output.info("remote.name=%s" % remote.name)

    def post_download_package(output, conanfile_path, reference, package_id, remote, **kwargs):
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % reference.full_repr())
        output.info("package_id=%s" % package_id)
        output.info("remote.name=%s" % remote.name)

Functions of the plugins are intended to be self-descriptive regarding to the execution of them. For example, the ``pre_package()`` function
is called just before the ``package()`` method os the recipe is executed.

For donwload/upload functions, the ``pre_download()``/``pre_upload()`` function is executed first in an
:command:`conan download`/:command:`conan upload` command. Then **pre** and **post** ``download_recipe()``/``upload_recipe()`` and its
subsequent **pre**/**post** ``download_package()``/``upload_package()`` if that is the case. Finally the general
``post_download()``/``post_upload()`` function is called to wrapp up the whole execution.

.. important::

    **Pre** and **post** ``download_reicpe()``/``download_package()`` are also executed when installed new recipes from remotes when using
    :command:`conan create` or :command:`conan install`.

Function paramenters
--------------------

Here you can find the description for each paramenter:

- **output**: :ref:`Output object<conanfile_output>` to print formatted messages during execution with the name of the plugin and the
  function executed, e.g., ``[PLUGIN - complete_plugin] post_download_package(): This is the remote name: default``.

- **conanfile**: It is a regular ``ConanFile`` object loaded from the recipe that received the Conan command. It has its normal attributes
  and dynamic objects such as ``build_folder``, ``package_folder``...

- **conanfile_path**: Path to the *conanfile.py* file wheter it is in local cache or in user space.

- **reference**: Named tuple with attributes ``name``, ``version``, ``user, and ``channel``.

- **package_id**: String with the computed pacakge ID.

- **remote**: Named tupke with attributes ``name``, ``url`` and ``verify_ssl``.

Some of this parameters does not appear in the signature of the function as they may not be available always (Mostly depending on the recipe
living in the local cache or in user space). However, they can be checked with the ``kwargs`` parameter.

.. important::

    Plugin functions should have a ``**kwargs`` parameter to keep compatibility of new parameters that may be introduced in future versions
    of Conan.

Importing from a module
-----------------------

The plugin interface should always be placed inside a Python file with the name of the plugin and stored in the *plugins* folder. However,
you can use fuctionalities from imported modules if you have them installed in your system or if they are installed with Conan:

.. code-block:: python
   :caption: example_plugin.py

    import requests
    from conans import tools

    def post_export(output, conanfile, conanfile_path, reference, **kwargs):
        cmakelist_path = os.path.join(os.path.dirname(conanfile_path), "CMakeLists.txt")
        tools.replace_in_file(cmakelist_path, "PROJECT(MyProject)", "PROJECT(MyProject CPP)")
        r = requests.get('https://api.github.com/events')

You can also import functionalities from a relative module:

.. code-block:: text

    plugins
    |   my_plugin.py
    |
    \---custom_module
            custom.py
            __init__.py

Inside the *custom.py* from my *custom_module* there is:

.. code-block:: python

    def my_printer(output):
        output.info("my_printer(): CUSTOM MODULE")

And it can be used in plugin importing the module:

.. code-block:: python

    from custom_module.custom import my_printer


    def pre_export(output, conanfile, conanfile_path, reference, **kwargs):
        my_printer(output)
