.. _deployment_flatpak:

Flatpak
-------

`Flatpak <https://flatpak.org/>`_ (former ``xdg-app``) is a package management system to distribute desktop applications for Linux. It is based on `OSTree <https://ostree.readthedocs.io/en/latest/manual/introduction/>`_. 
Flatpak is `RedHat <https://www.redhat.com>`_ initiative.

Unlike :ref:`AppImage <deployment_appimage>`, usually applications are distributed via `flathub <https://flathub.org>`_ store, and require a special runtime to install applications on target machines.

The major advantage of ``Flatpak`` is sandboxing: each application runs in its own isolated environment. ``Flatpak`` provides fine-grained control to system resources 
(e.g. network, bluetooth, host filesystem, etc.). ``Flatpak`` also offers a set of runtimes for various Linux desktop applications, e.g. 
`Freedesktop <https://www.freedesktop.org/wiki/>`_, `GNOME <https://www.gnome.org/>`_ and `KDE <https://kde.org/>`_.

The `packaging process <http://docs.flatpak.org/en/latest/first-build.html>`__ is:

- Install the flatpak runtime, flatpak-builder and SDK.
- Create a manifest ``<app-id>.json``
- Run the ``flatpak-builder`` in order to produce the application
- `Publish <http://docs.flatpak.org/en/latest/publishing.html>`__ the application for further distribution

With help of conan's :ref:`json generator<deployable_json_generator>`, the `manifest <http://docs.flatpak.org/en/latest/manifests.html>`_ creation could be easily automated. For example, the custom script could generate ``build-commands`` and ``sources`` entries within the manifest file:

.. code-block:: python

	app_id = "org.flatpak.%s" % self._name
	manifest = {
	    "app-id": app_id,
	    "runtime": "org.freedesktop.Platform",
	    "runtime-version": "18.08",
	    "sdk": "org.freedesktop.Sdk",
	    "command": "conan-entrypoint.sh",
	    "modules": [
	        {
	            "name": self._name,
	            "buildsystem": "simple",
	            "build-commands": ["install -D conan-entrypoint.sh /app/bin/conan-entrypoint.sh"],
	            "sources": [
	                {
	                    "type": "file",
	                    "path": "conan-entrypoint.sh"
	                }
	            ]
	        }
	    ]
	}
	sources = []
	build_commands = []
	for root, _, filenames in os.walk(temp_folder):
	    for filename in filenames:
	        filepath = os.path.join(root, filename)
	        unique_name = str(uuid.uuid4())
	        source = {
	            "type": "file",
	            "path": filepath,
	            "dest-filename": unique_name
	        }
	        build_command = "install -D %s /app/%s" % (unique_name, os.path.relpath(filepath, temp_folder))
	        sources.append(source)
	        build_commands.append(build_command)

	manifest["modules"][0]["sources"].extend(sources)
	manifest["modules"][0]["build-commands"].extend(build_commands)

Alternatively, ``flatpak`` allows distributing the `single-file <http://docs.flatpak.org/en/latest/single-file-bundles.html>`_ package. Such package, however, cannot be run or installed on its own, it's needed to be imported to the local repository on another machine.
