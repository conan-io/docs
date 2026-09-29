conan.tools.files checksums
===========================

.. important::

    Some of the features used in this section are still **under development**, while they are
    recommended and usable and we will try not to break them in future releases, some breaking
    changes might still happen if necessary to prepare for the *Conan 2.0 release*.


conan.tools.files.check_md5()
-----------------------------

Available since: `1.46.0 <https://github.com/conan-io/conan/releases/tag/1.46.0>`_

.. code-block:: python

    def check_md5(conanfile, file_path, signature)

Check that the specified md5sum of the ``file_path`` matches with ``signature``. If doesn't match it will raise a
``ConanException``.

Parameters:
    - **conanfile**: Conanfile object.
    - **file_path** (Required): Path of the file to check.
    - **signature** (Required): Expected md5sum.



conan.tools.files.check_sha1()
------------------------------

Available since: `1.46.0 <https://github.com/conan-io/conan/releases/tag/1.46.0>`_

.. code-block:: python

    def check_sha1(conanfile, file_path, signature)

Check that the specified sha1 of the ``file_path`` matches with ``signature``. If doesn't match it will raise a
``ConanException``.

Parameters:
    - **conanfile**: Conanfile object.
    - **file_path** (Required): Path of the file to check.
    - **signature** (Required): Expected sha1sum.



conan.tools.files.check_sha256()
--------------------------------

Available since: `1.46.0 <https://github.com/conan-io/conan/releases/tag/1.46.0>`_

.. code-block:: python

    def check_sha256(conanfile, file_path, signature)

Check that the specified sha256 of the ``file_path`` matches with ``signature``. If doesn't match it will raise a
``ConanException``.

Parameters:
    - **conanfile**: Conanfile object.
    - **file_path** (Required): Path of the file to check.
    - **signature** (Required): Expected sha256sum.