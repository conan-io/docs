.. _artifacts.properties:

artifacts.properties
====================

This file is used to send custom headers in the PUT requests that :command:`conan upload` command does:

**.conan/artifacts.properties**

.. code-block:: text

   custom_header1=Value1
   custom_header2=45

Artifactory users can use this file to set file properties for the uploaded files. The variables should have the prefix
``artifact_property``. You can use ``;`` to set multiple values to a property:


**.conan/artifacts.properties**

.. code-block:: text

   artifact_property_build.name=Build1
   artifact_property_build.number=23
   artifact_property_build.timestamp=1487676992
   artifact_property_custom_multiple_var=one;two;three;four
