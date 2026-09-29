.. _artifacts.properties:

artifacts.properties
====================

This is a file in the Conan cache that is useful to define a set of key-value pairs that will
be sent together with the packages uploaded in the :command:`conan upload` command.
This information is sent as custom headers in the PUT request and, if the server has the
capability, as `matrix params`_.


**.conan/artifacts.properties**

.. code-block:: text

   custom_header1=Value1
   custom_header2=45
   build.name=BuildJob


Artifactory users can benefit from this capability to set file properties for the uploaded files.
If the Artifactory version doesn't support matrix params yet (available since `Artifactory 7.3.2`_) it will use
the properties from the file that are prefixed with ``artifact_property_``:


**.conan/artifacts.properties**

.. code-block:: text

   artifact_property_build.name=Build1
   artifact_property_build.number=23
   artifact_property_build.timestamp=1487676992
   artifact_property_custom_multiple_var=one;two;three;four


Take into account that some reverse proxies will block headers that contain a period in
their name, for example `Nginx`_, as they consider it to be a security issue (you can bypass
this check adding the `ignore_invalid_headers` to your Nginx configuration).


.. _matrix params: https://www.ietf.org/rfc/rfc3986.txt
.. _Artifactory 7.3.2: https://www.jfrog.com/confluence/display/JFROG/Artifactory+Release+Notes#ArtifactoryReleaseNotes-Artifactory7.3.2
.. _Nginx: https://trac.nginx.org/nginx/ticket/629
