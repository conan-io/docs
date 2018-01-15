Logging
=========

.. _logging_and_debugging:

How to log and debug a conan execution
------------------------------------------

You can use the :ref:`conan_trace_file` environment variable to log and debug several conan command execution.
Set the ``CONAN_TRACE_FILE`` environment variable pointing to a log file.

Example:

.. code-block:: bash

	export CONAN_TRACE_FILE=/tmp/conan_trace.log # Or SET in windows
	conan install zlib/1.2.8@lasote/stable
	

The `/tmp/conan_trace.log` file:

.. code-block:: json

	{"_action": "COMMAND", "name": "install", "parameters": {"all": false, "build": null, "env": null, "file": null, "generator": null, "manifests": null, "manifests_interactive": null, "no_imports": false, "options": null, "package": null, "profile": null, "reference": "zlib/1.2.8@lasote/stable", "remote": null, "scope": null, "settings": null, "update": false, "verify": null, "werror": false}, "time": 1485345289.250117}
	{"_action": "REST_API_CALL", "duration": 1.8255090713500977, "headers": {"Authorization": "**********", "X-Client-Anonymous-Id": "**********", "X-Client-Id": "lasote2", "X-Conan-Client-Version": "0.19.0-dev"}, "method": "GET", "time": 1485345291.092218, "url": "https://server.conan.io/v1/conans/zlib/1.2.8/lasote/stable/download_urls"}
	{"_action": "DOWNLOAD", "duration": 0.4136989116668701, "time": 1485345291.506399, "url": "https://conanio-production.s3.amazonaws.com/storage/zlib/1.2.8/lasote/stable/export/conanmanifest.txt"}
	{"_action": "DOWNLOAD", "duration": 0.10367798805236816, "time": 1485345291.610335, "url": "https://conanio-production.s3.amazonaws.com/storage/zlib/1.2.8/lasote/stable/export/conanfile.py"}
	{"_action": "DOWNLOAD", "duration": 0.059114933013916016, "time": 1485345291.669744, "url": "https://conanio-production.s3.amazonaws.com/storage/zlib/1.2.8/lasote/stable/export/conan_export.tgz"}
	{"_action": "DOWNLOADED_RECIPE", "_id": "zlib/1.2.8@lasote/stable", "duration": 2.40762996673584, "files": {"conan_export.tgz": "/home/laso/.conan/data/zlib/1.2.8/lasote/stable/export/conan_export.tgz", "conanfile.py": "/home/laso/.conan/data/zlib/1.2.8/lasote/stable/export/conanfile.py", "conanmanifest.txt": "/home/laso/.conan/data/zlib/1.2.8/lasote/stable/export/conanmanifest.txt"}, "remote": "conan.io", "time": 1485345291.670017}
	{"_action": "REST_API_CALL", "duration": 0.4844989776611328, "headers": {"Authorization": "**********", "X-Client-Anonymous-Id": "**********", "X-Client-Id": "lasote2", "X-Conan-Client-Version": "0.19.0-dev"}, "method": "GET", "time": 1485345292.160912, "url": "https://server.conan.io/v1/conans/zlib/1.2.8/lasote/stable/packages/c6d75a933080ca17eb7f076813e7fb21aaa740f2/download_urls"}
	{"_action": "DOWNLOAD", "duration": 0.06388187408447266, "time": 1485345292.225308, "url": "https://conanio-production.s3.amazonaws.com/storage/zlib/1.2.8/lasote/stable/package/c6d75a933080ca17eb7f076813e7fb21aaa740f2/conaninfo.txt?Signature=c1KAOqvxtCUnnQOeYizZ9bgcwwY%3D&Expires=1485352492&AWSAccessKeyId=AKIAJXMWDMVCDMAZQK5Q"}
	{"_action": "REST_API_CALL", "duration": 0.8182470798492432, "headers": {"Authorization": "**********", "X-Client-Anonymous-Id": "**********", "X-Client-Id": "lasote2", "X-Conan-Client-Version": "0.19.0-dev"}, "method": "GET", "time": 1485345293.044904, "url": "https://server.conan.io/v1/conans/zlib/1.2.8/lasote/stable/packages/c6d75a933080ca17eb7f076813e7fb21aaa740f2/download_urls"}
	{"_action": "DOWNLOAD", "duration": 0.07849907875061035, "time": 1485345293.123831, "url": "https://conanio-production.s3.amazonaws.com/storage/zlib/1.2.8/lasote/stable/package/c6d75a933080ca17eb7f076813e7fb21aaa740f2/conanmanifest.txt"}
	{"_action": "DOWNLOAD", "duration": 0.06638002395629883, "time": 1485345293.190465, "url": "https://conanio-production.s3.amazonaws.com/storage/zlib/1.2.8/lasote/stable/package/c6d75a933080ca17eb7f076813e7fb21aaa740f2/conaninfo.txt"}
	{"_action": "DOWNLOAD", "duration": 0.3634459972381592, "time": 1485345293.554206, "url": "https://conanio-production.s3.amazonaws.com/storage/zlib/1.2.8/lasote/stable/package/c6d75a933080ca17eb7f076813e7fb21aaa740f2/conan_package.tgz"}
	{"_action": "DOWNLOADED_PACKAGE", "_id": "zlib/1.2.8@lasote/stable:c6d75a933080ca17eb7f076813e7fb21aaa740f2", "duration": 1.3279249668121338, "files": {"conan_package.tgz": "/home/laso/.conan/data/zlib/1.2.8/lasote/stable/package/c6d75a933080ca17eb7f076813e7fb21aaa740f2/conan_package.tgz", "conaninfo.txt": "/home/laso/.conan/data/zlib/1.2.8/lasote/stable/package/c6d75a933080ca17eb7f076813e7fb21aaa740f2/conaninfo.txt", "conanmanifest.txt": "/home/laso/.conan/data/zlib/1.2.8/lasote/stable/package/c6d75a933080ca17eb7f076813e7fb21aaa740f2/conanmanifest.txt"}, "remote": "conan.io", "time": 1485345293.554466}
		
In the traces we can see:

1. A command ``install`` execution.
2. A rest api call to get some ``download_urls``.
3. Three files downloaded (corresponding to the previously retrieved urls).
4. ``DOWNLOADED_RECIPE`` tells us that the recipe retrieving is finished. We can see that the whole retrieve process took 2.4 seconds.
5. conan client has computed the needed binary package SHA and now will get it. So will request and download the package ``package_id`` file to perform some checks like outdated binaries.
6. Another rest api call to get some more ``download_urls``, for the package files and download them.
7. Finally we get a ``DOWNLOADED_PACKAGE`` telling us that the package has beed downloaded. It took 1.3 seconds.


If we execute conan install again:

.. code-block:: bash

	export CONAN_TRACE_FILE=/tmp/conan_trace.log # Or SET in windows
	conan install zlib/1.2.8@lasote/stable
	

The `/tmp/conan_trace.log` file only three lines will be appended:

.. code-block:: json

	{"_action": "COMMAND", "name": "install", "parameters": {"all": false, "build": null, "env": null, "file": null, "generator": null, "manifests": null, "manifests_interactive": null, "no_imports": false, "options": null, "package": null, "profile": null, "reference": "zlib/1.2.8@lasote/stable", "remote": null, "scope": null, "settings": null, "update": false, "verify": null, "werror": false}, "time": 1485346039.817543}
	{"_action": "GOT_RECIPE_FROM_LOCAL_CACHE", "_id": "zlib/1.2.8@lasote/stable", "time": 1485346039.824949}
	{"_action": "GOT_PACKAGE_FROM_LOCAL_CACHE", "_id": "zlib/1.2.8@lasote/stable:c6d75a933080ca17eb7f076813e7fb21aaa740f2", "time": 1485346039.827915}

1. A command ``install`` execution.
2. A ``GOT_RECIPE_FROM_LOCAL_CACHE`` because we already have it available in local cache.
3. A ``GOT_PACKAGE_FROM_LOCAL_CACHE`` because the package is cached too.



How to log the build process
------------------------------------------

You can log your command executions ``self.run`` in a file named ``conan_run.log`` using the environment variable CONAN_LOG_RUN_FILE.
Check for more details here: :ref:`conan_log_run_to_file`.

You can also use the variable :ref:`conan_print_run_commands` to log extra information about the commands being executed.


Package the log files
+++++++++++++++++++++++++++

The `conan_run.log`` file will be available in your ``build`` folder so you can package it the same way you package a library file:

.. code-block:: python

        def package(self):
            self.copy(pattern="conan_run.log", dst="", keep_path=False)
            

