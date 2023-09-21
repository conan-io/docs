.. _devops_artifactory_backup_sources_repo:

Creating an Artifactory backup repo for your sources
====================================================

For the backup repository, we'll create a generic Artifactory repo using the free Community Edition version.

For this, in the repositories section of the administration tab,
we'll create a new generic repository, and in this example we'll imaginatively give it the name of *backup-sources*.

Next, as we want this to be a public read repo, we'll allow anonymous read access to our repo.
See the official Artifactory documentation for a step-by-step guide on how to: https://jfrog.com/help/r/how-to-grant-an-anonymous-user-access-to-specific-repositories/artifactory-how-to-grant-an-anonymous-user-access-to-specific-repositories

Now, to be able to upload contents, we'll also create a new user from the User Management section, called *backup uploader*,
and from the Access Tokens section, we'll generate a reference token associated with the user

.. image:: images/create_reference_token.png

And last but not least, from the Permissions section we'll give the user manage access to the new repository,
which will automatically give it every other permission available. Feel free to modify them according to your needs.

.. image:: images/permissions_add_backup_access.png

With this, access to our remote backup is now configured to allow anonymous read but authenticated upload.

You can now go back to read :ref:`how to configure the Conan client to use this feature<backup_sources_setup_necessary_configs>`

