.. _azure_devops:


|azure_logo| Microsoft's Azure DevOps (TFS, VSTS)
=================================================

Thanks to the `JFrog Artifactory Extension for Azure DevOps and TFS`_ it is possible to support
Conan tasks and integrate it with the CI development platform provided by `Microsoft’s Azure DevOps`_
and the `Artifactory binary repository manager`_.

The support for Conan now in the JFrog Artifactory Extension helps you perform the following
tasks in Azure DevOps or TFS:

 * Run Conan commands
 * Resolve Conan dependencies from remote Artifactory servers
 * Push Conan packages to Artifactory
 * Publish BuildInfo metadata
 * Import a Conan configuration

In this section we will show you how to add Conan tasks to your pipelines using the Artifactory/Conan
Extension and push the generated buildinfo metadata to Artifactory where it can be used to track
and automate your builds.

Configuring DevOps Azure to use Artifactory with Conan
------------------------------------------------------

To use the Conan support provided by the JFrog Artifactory Extension you must
`configure a self-hosted agent`_
that will enable Conan builds for your Azure Pipelines environment. Afterwards you can install
the JFrog Artifactory Extension from the Visual Studio Marketplace and follow the installation
instructions in the Overview.

.. image:: ../../images/azure_devops/conan-azure_devops_1.png
   :width: 800 px
   :alt: Azure DevOps

When completed, proceed to create builds and access buildinfo from within Azure DevOps or TFS.

Steps to follow
---------------

In these steps, you will set up Azure DevOps to use Artifactory and add Conan tasks to your
build pipeline. Then you can set up to push the buildinfo from the Conan task to Artifactory.

STEP 1: Configure the Artifactory instance
++++++++++++++++++++++++++++++++++++++++++

Once the Artifactory Extension is installed, you must configure Azure DevOps to access the
Artifactory instance.

To add Artifactory to Azure DevOps:
***********************************

 1. In Azure DevOps, go to Project Settings > Service connections.

 2. Click + New service connection to display the list control, and select Artifactory.

   .. image:: ../../images/azure_devops/conan-azure_devops_2.png
      :width: 800 px
      :alt: Azure DevOps

 3. In the resulting Update Authentication for Artifactory dialog, enter the required server and
    credential information, and click OK.

   .. image:: ../../images/azure_devops/conan-azure_devops_3.png
      :width: 800 px
      :alt: Azure DevOps

STEP 2: Add a Conan task
++++++++++++++++++++++++

Once your Artifactory connection is configured, you may add Conan tasks to your Build or Release pipelines.

To add a Conan task:
********************

 1. Go to the Pipeline Tasks setup screen.

 2. In the Add tasks section, search for “Conan” in the task selection list.

 3. Select the Artifactory Conan task to add it to your pipeline.

   .. image:: ../../images/azure_devops/conan-azure_devops_4.png
      :width: 800 px
      :alt: Azure DevOps

 4. In the new task, select which Conan command to run.

   .. image:: ../../images/azure_devops/conan-azure_devops_5.png
      :width: 800 px
      :alt: Azure DevOps

 5. Configure the Conan command for the task.

   .. image:: ../../images/azure_devops/conan-azure_devops_6.png
      :width: 800 px
      :alt: Azure DevOps

Continue to add Conan tasks as you need for each pipeline.

STEP 3: Configure the Push task buildinfo to Artifactory
++++++++++++++++++++++++++++++++++++++++++++++++++++++++

When the pipeline containing the Conan task executes, the task log shows all the information
about the executed Conan command.

.. image:: ../../images/azure_devops/conan-azure_devops_7.png
   :width: 800 px
   :alt: Azure DevOps

You can configure your Conan task to collect the buildinfo by selecting the Collect buildinfo
checkbox when you create the task.

.. image:: ../../images/azure_devops/conan-azure_devops_8.png
   :width: 800 px
   :alt: Azure DevOps

Once collected, the buildinfo can then be pushed as metadata to Artifactory.

To perform this, create an Artifactory Publish Build Info task to push the metadata to your
Artifactory instance.

.. image:: ../../images/azure_devops/conan-azure_devops_9.png
   :width: 800 px
   :alt: Azure DevOps

After you run the pipeline, you will be able to see the build information for the Conan task
in Artifactory.

.. image:: ../../images/azure_devops/conan-azure_devops_10.png
   :width: 800 px
   :alt: Azure DevOps

.. seealso::

   The documentation for this integration is taken from the `JFrog blog`_.


.. |azure_logo| image:: ../../images/conan-azure_logo.png
                :width: 100 px
                :alt: Azure DevOps
.. _`Microsoft’s Azure DevOps`: `
.. _`JFrog Artifactory Extension for Azure DevOps and TFS`: https://marketplace.visualstudio.com/items?itemName=JFrog.jfrog-artifactory-vsts-extension
.. _`Artifactory binary repository manager`: https://jfrog.com/artifactory/
.. _`configure a self-hosted agent`: https://docs.microsoft.com/en-us/azure/devops/pipelines/agents/agents?view=azure-devops
.. _`JFrog blog`: https://jfrog.com/blog/accelerate-azure-devops-or-tfs-with-jfrog-artifactory-and-conan/