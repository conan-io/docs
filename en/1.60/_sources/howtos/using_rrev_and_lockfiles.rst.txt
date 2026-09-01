Using recipe revisions and lockfiles
====================================

If you don't want to deploy and maintain your own Artifactory instance, you can isolate your project from
changes in upstream remotes, for example ConanCenter, using :ref:`recipe revisions<package_revisions>`
and :ref:`lockfiles<versioning_lockfiles>` (please, read linked Conan documentation for more detailed
explanation).

Recipe revisions and lockfiles can be used to define exactly the binary you want to use in
your project. Even if the recipe is modified and new binaries are generated for the same configurations,
existing binaries will exist, you just need to instruct Conan to use them even if new ones are available.

Recipe Revisions
----------------

Recipe Revisions are the way to tell Conan to use a specific snapshot of the recipe. It
is a hash added to the reference and can be used in Conan at the same place as regular
revisions:

* In the command line:


.. code-block:: shell

   conan install openssl/3.0.1@#1955937e88f13a02aa4fdae98c3f9fb8

* In a `conanfile.txt` file:

.. code-block:: text

   [requires]
   openssl/3.0.1@#1955937e88f13a02aa4fdae98c3f9fb8

* In a `conanfile.py` file:

.. code-block:: python

   def requirements(self):
       self.requires("openssl/3.0.1@#1955937e88f13a02aa4fdae98c3f9fb8")

If you use explicit recipe revisions in your project you can be sure that Conan will always use
the same recipe revision of those references. You might get new binaries if the same
configuration (same packageID) is built again for the same recipe revision, but that is not
going to be a compatibility problem.

This might not be enough for some projects, where you want
to be sure nothing is modified, not just the revisions you are listing explicitly but also any
other transitive dependency, this is what lockfiles are for.

Lockfiles
---------

Lockfiles are files where all the information about requirements is written: recipe
revisions, package IDs and package revisions. You can create a lockfile with all the
dependencies for your project once you are happy with them, and use that same lockfile
with every Conan command. Conan will always build the same graph (the locked one) and
will always retrieve the same recipes and binaries.


.. warning::

   Lockfiles have a few known limitation that can not be fixed in Conan 1.x, there are exciting improvements
   coming with Conan 2.0. Please read the documentation linked below for more details.

Then, it would be up to you to generate a new lockfile if you want to introduce new revisions
for existing references.

The two basic commands you need to know (:ref:`full docs here<versioning_lockfiles>`):

* Create lockfile from `conanfile.txt` file:

.. code-block:: shell

   conan lock create conanfile.txt --lockfile-out=locks/project.lock

* Consume a lockfile:

.. code-block:: shell

   conan install conanfile.txt --lockfile=locks/project.lock

If your project is managing several configurations, you would probably like to have a look to :ref:`base lockfiles<versioning_lockfiles_configurations_base_lockfiles>`
and :ref:`lockfile bundles<versioning_lockfiles_bundle>` in the documentation.
