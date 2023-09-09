.. _devops_artifactory_new_anonymous_repo

Creating a public read repo
===========================
For the backup repository, we'll create a generic Artifactory repo using the free Community Edition version.


Next, as we want this to be a public read repo, we'll allow anonymous read access to our repo.

See the official Artifactory documentation for a step-by-step guide on how to: https://jfrog.com/help/r/how-to-grant-an-anonymous-user-access-to-specific-repositories/artifactory-how-to-grant-an-anonymous-user-access-to-specific-repositories

We'll also create another user,


Let's create the backup repository with Artifactory CE. From the UI, create a generic repo to store the files, we'll imaginatively call it "source-backups".
<IMAGE>

Next, we want to allow anonymous read access for our backups
(We'll touch on the :ref:`source_credentials.json<reference_config_files_source_credentials>` feature for restricting upload access,
if you also want restricted read access, follow those same steps for reading). Create a new user, we'll call it "backup reader",
and from the "Access" tab, give it read permissions to our "source-backups" repo.
<IMAGE>
**CHECK, anonymous read is done the other way around!**

As for uploading permissions, we'll do the same now. Create a new user, this time "backup uploader", and give it "Manage" permisisons.
<IMAGE>
We can now create an access token for our "backup uploader" user and store it. This token needs to go into the `source_credentials.json` file
of our machine/CI worker.
<IMAGE>
