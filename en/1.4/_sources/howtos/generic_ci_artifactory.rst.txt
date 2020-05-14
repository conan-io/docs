

Use a generic CI with Conan and Artifactory
===========================================

Uploading the BuildInfo
-----------------------

If you are using :ref:`Jenkins with Conan and Artifactory<jenkins_integration>`, with the
`Jenkins Artifactory Plugin <https://www.jfrog.com/confluence/display/RTF/Jenkins+Artifactory+Plug-in>`_,
any Conan package downloaded or uploaded during your build will be automatically recorded in
the BuildInfo json file, that will be automatically uploaded to the specified Artifactory instance.

However, you can gather and upload that information using other CI infrastructure with the following steps:


1. Before calling Conan the first time in your build, set the environment variable `CONAN_TRACE_FILE` to a
   file path. The generated file will contain the `BuildInfo json <https://www.jfrog.com/confluence/display/RTF/Build+Integration#BuildIntegration-BuildInfoJSON>`_.

2. You also need to create the :ref:`artifacts.properties<artifacts.properties>` file in your Conan home containing the build
   information. All this properties will be automatically associated to all the published artifacts.

.. code-block:: text

   artifact_property_build.name=MyBuild
   artifact_property_build.number=23
   artifact_property_build.timestamp=1487676992


3. Call Conan as many times as you need.  For example, if you are testing a Conan package and uploading it at the end, you will run
   something similar to:


.. code-block:: bash

    $ conan create . user/stable # Will retrieve the dependencies and create the package
    $ conan upload mypackage/1.0@user/stable -r artifactory

4.  Call the command `conan_build_info` passing the path to the generated conan traces file and a parameter ``--output`` to
    indicate the output file. You can also, delete the traces.log` file` otherwise while the `CONAN_TRACE_FILE` is present, any
    Conan command will keep appending actions.

.. code-block:: bash

    $ conan_build_info /tmp/traces.log --output /tmp/build_info.json
    $ rm /tmp/traces.log

5. Edit the `build_info.json` file to append ``name`` (build name), ``number`` (build number) and the ``started`` (started date) and
   any other field that you need according to the `Build Info json format <https://github.com/JFrogDev/build-info>`_.

   The ``started`` field has to be in the format: ``yyyy-MM-dd'T'HH:mm:ss.SSSZ``

   To edit the file you can import the json file using the programming language you are using in your framework, groovy, java, python...


6. Push the json file to Artifactory, using the REST-API:

.. code-block:: bash

    curl -X PUT -u<username>:<password> -H "Content-type: application/json" -T /tmp/build_info.json "http://host:8081/artifactory/api/build"
