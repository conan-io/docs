.. _conan_tools_scm_git:

Git
===

The ``Git`` helper is a thin wrapper over the ``git`` command. It can be used for different purposes:
- Obtaining the current tag in the ``set_version()`` method to assign it to ``self.version``
- Clone sources in third-party or open source package recipes in the ``source()`` method (in general, doing a ``download()`` or ``get()`` to fetch release tarballs will be preferred)
- Capturing the "scm" coordinates (url, commit) of your own package sources in the ``export()`` method, to be able to reproduce a build from source later, retrieving the code in the ``source()`` method. See the :ref:`example of git-scm capture<examples_tools_scm_git_capture>`.

The ``Git()`` constructor receives the current folder as argument, but that can be changed if necessary, for example, to clone the sources of some repo in ``source()``:


.. code-block:: python

     def source(self):
        git = Git(self)  # by default, the current folder "."
        git.clone(url="<repourl>", target="target") # git clone url target
        # we need to cd directory for next command "checkout" to work
        git.folder = "target"                       # cd target
        git.checkout(commit="<commit>")             # git checkout commit


An alternative, equivalent approach would be:

.. code-block:: python

     def source(self):
        git = Git(self, "target")
        # Cloning in current dir, not a children folder
        git.clone(url="<repourl>", target=".")
        git.checkout(commit="<commit>")



.. currentmodule:: conan.tools.scm.git

.. autoclass:: Git
    :members:
