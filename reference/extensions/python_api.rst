.. _reference_python_api:

Python API
==========

.. warning::

  The full Python API is **experimental**.
  See :ref:`the Conan stability<stability>` section for more information.


The Python API is a set of Python classes that allow you to interact with Conan programmatically.
It's designed to be used as part of the custom commands extension point,
or in Python scripts or applications, providing a more flexible and powerful way to work with Conan than the command line interface.

It is organized in submodules, each one providing a specific set of functionalities.

Note that only the **documented** public members of these classes are guaranteed to be stable,
and the rest of the members are considered private and can change without notice.

.. toctree::
   :maxdepth: 1

   python_api/ConanAPI
   python_api/AuditAPI
   python_api/CacheAPI
   python_api/CommandAPI
   python_api/ConfigAPI
   python_api/DownloadAPI
   python_api/ExportAPI
   python_api/GraphAPI
   python_api/InstallAPI
   python_api/ListAPI
   python_api/LockfileAPI
   python_api/NewAPI
   python_api/ProfilesAPI
   python_api/RemotesAPI
   python_api/RemoveAPI
   python_api/ReportAPI
   python_api/UploadAPI

.. include:: ../../common/subapi_instantiation_warning.inc

There are also some model classes that represent the data structures used in the API.
Note that as with the API, only the **documented** public members are guaranteed to be stable,
and the rest of the members are considered private and can change without notice.

.. toctree::
   :maxdepth: 3

   python_api/model
