.. _examples_tools_scm_git_capture:

Capturing Git scm information
=============================

There are 2 main strategies to handle source code in recipes:

- **Third-party code**: When the ``conanfile.py`` recipe is packaging third party code, like an open source library, it is typically better to use the ``source()`` method to download or clone the sources of that library. This is the approach followed by the ``conan-center-index`` repository for ConanCenter.
- **Your own code**: When the ``conanfile.py`` recipe is packaging your own code, it is typically better to have the ``conanfile.py`` in the same repository as the sources. Then, there are 2 alternatives for achieving reproducibility:

  - Using the ``exports_sources`` (or ``export_source()`` method) to capture a copy of the sources together with the recipe in the Conan package. This is very simple and pragmatic and would be recommended for the majority of cases.
  - For cases when it is not possible to store the sources beside the Conan recipe, for example when the package is to be consumed for someone that shouldn't have access to the source code at all, then the current **scm capture** method would be the way.


In the **scm capture** method, instead of capturing a copy of the code itself, the "coordinates" for that code are captured instead, in the ``Git`` case, the ``url`` of the repository and the ``commit``. If the recipe needs to build from source, it will use that information to get a clone, and if the user who tries that is not authorized, the process will fail. They will still be able to use the pre-compiled binaries that we distribute, but not build from source or have access to the code.

Let's see how it works with an example. Please, first clone the sources to recreate this project. You can find them in the
`examples2 repository <https://github.com/conan-io/examples2>`_ on GitHub:

.. code-block:: bash

    $ git clone https://github.com/conan-io/examples2.git
    $ cd examples2/examples/tools/scm/git/capture_scm


There we will find a small "hello" project, containing this ``conanfile.py``:

.. code-block:: python

    from conan import ConanFile
    from conan.tools.cmake import CMake, cmake_layout
    from conan.tools.scm import Git


    class helloRecipe(ConanFile):
        name = "hello"
        version = "0.1"

        # Binary configuration
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False], "fPIC": [True, False]}
        default_options = {"shared": False, "fPIC": True}
        generators = "CMakeDeps", "CMakeToolchain"

        def export(self):
            git = Git(self, self.recipe_folder)
            # save the url and commit in conandata.yml
            git.coordinates_to_conandata()

        def source(self):
            # we recover the saved url and commit from conandata.yml and use them to get sources
            git = Git(self)
            git.checkout_from_conandata_coordinates()

        ...


We need this code to be in its own Git repository, to see how it works in the real case, so
please create a folder outside of the ``examples2`` repository, and copy the contents of the current folder there, then:

.. code-block:: text

    $ mkdir /home/myuser/myfolder # or equivalent in other OS
    $ cp -R . /home/myuser/myfolder # or equivalent in other OS
    $ cd /home/myuser/myfolder # or equivalent in other OS

    # Initialize the git repo
    $ git init .
    $ git add .
    $ git commit . -m wip
    # Finally create the package
    $ conan create .
    ...
    ======== Exporting recipe to the cache ========
    hello/0.1: Exporting package recipe: /myfolder/conanfile.py
    hello/0.1: Calling export()
    hello/0.1: RUN: git status . --short --no-branch --untracked-files
    hello/0.1: RUN: git rev-list HEAD -n 1 --full-history -- "."
    hello/0.1: RUN: git remote -v
    hello/0.1: RUN: git branch -r --contains cb7815a58529130b49da952362ce8b28117dee53
    hello/0.1: RUN: git fetch origin --dry-run --depth=1 cb7815a58529130b49da952362ce8b28117dee53
    hello/0.1: WARN: Current commit cb7815a58529130b49da952362ce8b28117dee53 doesn't exist in remote origin
    This revision will not be buildable in other computer
    hello/0.1: RUN: git rev-parse --show-toplevel
    hello/0.1: Copied 1 '.py' file: conanfile.py
    hello/0.1: Copied 1 '.yml' file: conandata.yml
    hello/0.1: Exported to cache folder: /.conan2/p/hello237d6f9f65bba/e
    ...
    ======== Installing packages ========
    hello/0.1: Calling source() in /.conan2/p/hello237d6f9f65bba/s
    hello/0.1: Cloning git repo
    hello/0.1: RUN: git clone "<hidden>"  "."
    hello/0.1: Checkout: cb7815a58529130b49da952362ce8b28117dee53
    hello/0.1: RUN: git checkout cb7815a58529130b49da952362ce8b28117dee53

Let's explain step by step what is happening:

- When the recipe is exported to the Conan cache, the ``export()`` method executes, ``git.coordinates_to_conandata()``,
  which stores the Git URL and commit in the ``conandata.yml`` file by internally calling ``git.get_url_and_commit()``.
  See the :ref:`Git reference<conan_tools_scm_git>` for more information about these methods.
- This obtains the URL of the repo pointing to the local ``<local-path>/capture_scm`` and the commit ``8e8764c40bebabbe3ec57f9a0816a2c8e691f559``
- It warns that this information will **not** be enough to re-build from source this recipe once the package is uploaded to the server and is tried to be built from source in other computer, which will not contain the path pointed by ``<local-path>/capture_scm``. This is expected, as the repository that we created doesn't have any remote defined. If our local clone had a remote defined and that remote contained the ``commit`` that we are building, the ``scm_url`` would point to the remote repository instead, making the build from source fully reproducible.
- The ``export()`` method stores the ``url`` and ``commit`` information in the ``conandata.yml`` for future reproducibility.
- When the package needs to be built from sources and it calls the ``source()`` method,
  it recovers the information from the ``conandata.yml`` file inside the ``git.checkout_from_conandata_coordinates()`` method,
  which internally calls ``git.clone()`` with it to retrieve the sources.
  In this case, it will be cloning from the local checkout in ``<local-path>/capture_scm``, but if it had a remote defined, it will clone from it.


.. warning::

    To achieve reproducibility, it is very important for this **scm capture** technique that the current checkout is not dirty
    If it was dirty, it would be impossible to guarantee future reproducibility of the build, so ``git.get_url_and_commit()`` can raise errors,
    and require to commit changes. If more than 1 commit is necessary, it would be recommended to squash those commits before pushing changes to upstream repositories.

If we do now a second ``conan create .``, as the repo is dirty we would get:

.. code-block:: text

    $ conan create .
    hello/0.1: Calling export()
    ERROR: hello/0.1: Error in export() method, line 19
        scm_url, scm_commit = git.get_url_and_commit()
        ConanException: Repo is dirty, cannot capture url and commit: .../capture_scm

This could be solved by cleaning the repo with ``git clean -xdf``, or by adding a ``.gitignore`` file to the repo with the following contents
(which might be a good practice anyway for source control):

.. code-block:: text
    :caption: .gitignore

    test_package/build
    test_package/CMakeUserPresets.json





Credentials management
----------------------

In the example above, credentials were not necessary, because our local repo didn't require them. But in real world scenarios, the credentials can be required.

The first important bit is that ``git.get_url_and_commit()`` will capture the url of the ``origin`` remote. This url must not encode tokens, users or passwords, for several reasons. First because that will make the process not repeatable, and different builds, different users would get different urls, and consequently different recipe revisions. The ``url`` should always be the same. The recommended approach is to manage the credentials in an orthogonal way, for example using ssh keys. The provided example contains a Github action that does this:

.. code-block:: yaml
    :caption: .github/workflows/hello-demo.yml

    name: Build "hello" package capturing SCM in Github actions
    run-name: ${{ github.actor }} checking hello-ci Git scm capture
    on: [push]
    jobs:
    Build:
        runs-on: ubuntu-latest
        steps:
        - name: Check out repository code
            uses: actions/checkout@v3
            with:
            ssh-key: ${{ secrets.SSH_PRIVATE_KEY }}
        - uses: actions/setup-python@v4
            with:
            python-version: '3.10' 
        - uses: webfactory/ssh-agent@v0.7.0
            with:
            ssh-private-key: ${{ secrets.SSH_PRIVATE_KEY }}
        - run: pip install conan
        - run: conan profile detect
        - run: conan create .

This ``hello-demo.yml`` takes care of the following:

- The checkout ``actions/checkout@v3`` action receives the ``ssh-key`` to checkout as ``git@`` instead of ``https``
- The ``webfactory/ssh-agent@v0.7.0`` action takes care that the ssh key is also activated during the execution of the following tasks, not only during the checkout.
- It is necessary to setup the ``SSH_PRIVATE_KEY`` secret in the Github interface, as well as the ``deploy key`` for the repo (with the private and public parts of the ssh-key)

In this way, it is possible to keep completely separated the authentication and credentials from the recipe functionality, without any risk to leaking credentials.


.. note::

    **Best practices**

    - Do not use an authentication mechanism that encodes information in the urls. This is risky, can easily disclose credentials in logs. It is recommended to use system mechanisms like ssh keys.
    - Doing ``conan create`` is not recommended for local development, but instead running ``conan install`` and building locally, to avoid too many unnecessary commits. Only when everything works locally, it is time to start checking the ``conan create`` flow.
