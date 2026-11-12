.. _hooks_reference:

Hooks [EXPERIMENTAL]
======================

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.

The Conan hooks are Python functions that are intended to extend the Conan functionalities and let users customize the client behavior at
determined execution points.

Hook interface
----------------

Here you can see a complete example of all the hook functions available and the different parameters for each of them depending on the
context:

.. code-block:: python

    def pre_export(output, conanfile, conanfile_path, reference, **kwargs):
        assert conanfile
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % str(reference))

    def post_export(output, conanfile, conanfile_path, reference, **kwargs):
        assert conanfile
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % str(reference))

    def pre_source(output, conanfile, conanfile_path, **kwargs):
        assert conanfile
        output.info("conanfile_path=%s" % conanfile_path)
        if conanfile.in_local_cache:
            output.info("reference=%s" % str(kwargs["reference"]))

    def post_source(output, conanfile, conanfile_path, **kwargs):
        assert conanfile
        output.info("conanfile_path=%s" % conanfile_path)
        if conanfile.in_local_cache:
            output.info("reference=%s" % str(kwargs["reference"]))

    def pre_build(output, conanfile, **kwargs):
        assert conanfile
        if conanfile.in_local_cache:
            output.info("reference=%s" % str(kwargs["reference"]))
            output.info("package_id=%s" % kwargs["package_id"])
        else:
            output.info("conanfile_path=%s" % kwargs["conanfile_path"])

    def post_build(output, conanfile, **kwargs):
        assert conanfile
        if conanfile.in_local_cache:
            output.info("reference=%s" % str(kwargs["reference"]))
            output.info("package_id=%s" % kwargs["package_id"])
        else:
            output.info("conanfile_path=%s" % kwargs["conanfile_path"])

    def pre_package(output, conanfile, conanfile_path, **kwargs):
        assert conanfile
        output.info("conanfile_path=%s" % conanfile_path)
        if conanfile.in_local_cache:
            output.info("reference=%s" % str(kwargs["reference"]))
            output.info("package_id=%s" % kwargs["package_id"])

    def post_package(output, conanfile, conanfile_path, **kwargs):
        assert conanfile
        output.info("conanfile_path=%s" % conanfile_path)
        if conanfile.in_local_cache:
            output.info("reference=%s" % str(kwargs["reference"]))
            output.info("package_id=%s" % kwargs["package_id"])

    def pre_upload(output, conanfile_path, reference, remote, **kwargs):
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % str(reference))
        output.info("remote.name=%s" % remote.name)

    def post_upload(output, conanfile_path, reference, remote, **kwargs):
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % str(reference))
        output.info("remote.name=%s" % remote.name)

    def pre_upload_recipe(output, conanfile_path, reference, remote, **kwargs):
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % str(reference))
        output.info("remote.name=%s" % remote.name)

    def post_upload_recipe(output, conanfile_path, reference, remote, **kwargs):
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % str(reference))
        output.info("remote.name=%s" % remote.name)

    def pre_upload_package(output, conanfile_path, reference, package_id, remote, **kwargs):
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % str(reference))
        output.info("package_id=%s" % package_id)
        output.info("remote.name=%s" % remote.name)

    def post_upload_package(output, conanfile_path, reference, package_id, remote, **kwargs):
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % str(reference))
        output.info("package_id=%s" % package_id)
        output.info("remote.name=%s" % remote.name)

    def pre_download(output, reference, remote, **kwargs):
        output.info("reference=%s" % str(reference))
        output.info("remote.name=%s" % remote.name)

    def post_download(output, conanfile_path, reference, remote, **kwargs):
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % str(reference))
        output.info("remote.name=%s" % remote.name)

    def pre_download_recipe(output, reference, remote, **kwargs):
        output.info("reference=%s" % str(reference))
        output.info("remote.name=%s" % remote.name)

    def post_download_recipe(output, conanfile_path, reference, remote, **kwargs):
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % str(reference))
        output.info("remote.name=%s" % remote.name)

    def pre_download_package(output, conanfile_path, reference, package_id, remote, **kwargs):
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % str(reference))
        output.info("package_id=%s" % package_id)
        output.info("remote.name=%s" % remote.name)

    def post_download_package(output, conanfile_path, reference, package_id, remote, **kwargs):
        output.info("conanfile_path=%s" % conanfile_path)
        output.info("reference=%s" % str(reference))
        output.info("package_id=%s" % package_id)
        output.info("remote.name=%s" % remote.name)

Functions of the hooks are intended to be self-descriptive regarding to the execution of them. For example, the ``pre_package()`` function
is called just before the ``package()`` method of the recipe is executed.

For download/upload functions, the ``pre_download()``/``pre_upload()`` function is executed first in an
:command:`conan download`/:command:`conan upload` command. Then **pre** and **post** ``download_recipe()``/``upload_recipe()`` and its
subsequent **pre**/**post** ``download_package()``/``upload_package()`` if that is the case. Finally the general
``post_download()``/``post_upload()`` function is called to wrap up the whole execution.

.. important::

    **Pre** and **post** ``download_recipe()``/``download_package()`` are also executed when installing new recipes/packages from remotes
    using :command:`conan create` or :command:`conan install`.

Function parameters
-------------------

Here you can find the description for each parameter:

- **output**: :ref:`Output object<conanfile_output>` to print formatted messages during execution with the name of the hook and the
  function executed, e.g., ``[HOOK - complete_hook] post_download_package(): This is the remote name: default``.

- **conanfile**: It is a regular ``ConanFile`` object loaded from the recipe that received the Conan command. It has its normal attributes
  and dynamic objects such as ``build_folder``, ``package_folder``...

- **conanfile_path**: Path to the *conanfile.py* file whether it is in local cache or in user space.

- **reference**: Named tuple with attributes ``name``, ``version``, ``user``, and ``channel``. Its representation will be a reference like:
  ``box2d/2.1.0@user/channel``

- **package_id**: String with the computed package ID.

- **remote**: Named tuple with attributes ``name``, ``url`` and ``verify_ssl``.

+-------------------------------------+---------------------------------------------------------------------------------------------------------------+
| | Availability of parameters for    | **Hook Functions***                                                                                           |
| | each Hook function depending on   +--------------+--------------+-------------+---------------+------------------------+--------------------------+
| | the context                       | ``export()`` | ``source()`` | ``build()`` | ``package()`` | | ``upload()``         | | ``download()``         |
|                                     |              |              |             |               | | ``upload_recipe()``  | | ``download_recipe()``  |
|                                     |              |              |             |               | | ``upload_package()`` | | ``download_package()`` |
+----------------+--------------------+--------------+--------------+-------------+---------------+------------------------+--------------------------+
| **Parameters** | ``conanfile``      | Yes          | Yes          | Yes         | Yes           | No                     | post                     |
|                +--------------------+--------------+--------------+-------------+---------------+------------------------+--------------------------+
|                | ``conanfile_path`` | pre / post   | Yes          | user space  | pre / post    | Yes                    | post                     |
|                +--------------------+--------------+--------------+-------------+---------------+------------------------+--------------------------+
|                | ``reference``      | Yes          | cache        | cache       | cache         | Yes                    | Yes                      |
|                +--------------------+--------------+--------------+-------------+---------------+------------------------+--------------------------+
|                | ``package_id``     | No           | No           | cache       | Yes           | Yes                    | Yes                      |
|                +--------------------+--------------+--------------+-------------+---------------+------------------------+--------------------------+
|                | ``remote``         | No           | No           | No          | No            | Yes                    | Yes                      |
+----------------+--------------------+--------------+--------------+-------------+---------------+------------------------+--------------------------+

\*Hook functions are indicated without ``pre`` and ``post`` prefixes for simplicity.

Table legend:
  - **Yes**: Availability in ``pre`` and ``post`` functions in any context.
  - **No**: Not available.
  - **pre / post**: Availability in both ``pre`` and ``post`` functions with **different values**. e.g. ``conanfile_path`` pointing to user
    space in ``pre`` and to local cache in ``post``.
  - **post**: Only available in ``post`` function.
  - **cache**: Only available when the context of the command executed is the local cache. e.g. :command:`conan create`,
    :command:`conan install`...
  - **user space**: Only available when the context of the command executed is the user space. e.g. :command:`conan build`

.. note::

    Path to the different folders of the Conan execution flow may be accessible as usual through the ``conanfile`` object. See
    :ref:`folders_attributes_reference` to learn more.

Some of this parameters does not appear in the signature of the function as they may not be always available (Mostly depending on the recipe
living in the local cache or in user space). However, they can be checked with the ``kwargs`` parameter.

.. important::

    Hook functions should have a ``**kwargs`` parameter to keep compatibility of new parameters that may be introduced in future versions
    of Conan.
