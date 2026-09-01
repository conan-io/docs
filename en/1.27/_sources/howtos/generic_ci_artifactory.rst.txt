

Use a generic CI with Conan and Artifactory
===========================================

Uploading the BuildInfo
-----------------------

If you are using :ref:`Jenkins with Conan and Artifactory<jenkins_integration>`, along with the
`Jenkins Artifactory Plugin <https://www.jfrog.com/confluence/display/JFROG/Jenkins+Artifactory+Plug-in>`_,
any Conan package downloaded or uploaded during your build will be automatically recorded in
the BuildInfo json file, that will be automatically uploaded to the specified Artifactory instance.

However, using the `conan_build_info` command, you can gather and upload that information using other
CI infrastructure. There are two possible ways of using this commmand:

Extracting build-info from the Conan trace log
##############################################

1. Before calling Conan the first time in your build, set the environment variable `CONAN_TRACE_FILE` to a
   file path. The generated file will contain the `BuildInfo json <https://www.jfrog.com/confluence/display/JFROG/Build+Integration#BuildIntegration-BuildInfoJSON>`_.

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

4.  Call the command `conan_build_info` passing the path to the generated Conan traces file and a parameter ``--output`` to
    indicate the output file. You can also, delete the traces.log` file` otherwise while the `CONAN_TRACE_FILE` is present, any
    Conan command will keep appending actions.

.. code-block:: bash

    $ conan_build_info /tmp/traces.log --output /tmp/build_info.json
    $ rm /tmp/traces.log

5. Edit the `build_info.json` file to append ``name`` (build name), ``number`` (build number) and the ``started`` (started date) and
   any other field that you need according to the `Build Info json format <https://github.com/jfrog/build-info>`_.

   The ``started`` field has to be in the format: ``yyyy-MM-dd'T'HH:mm:ss.SSSZ``

   To edit the file you can import the json file using the programming language you are using in your framework, groovy, java, python...


6. Push the json file to Artifactory, using the REST-API:

.. code-block:: bash

    curl -X PUT -u<username>:<password> -H "Content-type: application/json" -T /tmp/build_info.json "http://host:8081/artifactory/api/build"

Generating build info from lockfiles information 
################################################

.. warning::

    This is an **experimental** feature subject to breaking changes in future releases.
    
To maintain compatibility with the current implementation of the ``conan_build_info`` command, this
version must be invoked using the argument ``--v2`` before any subcommand.

1. To begin associating the build information to the uploaded packages the first thing
is calling to the ``start`` subcommand of ``conan_build_info``. This will set the
`artifact_property_build.name` and `artifact_property_build.name` properties in the
:ref:`artifacts.properties<artifacts.properties>`.

.. code-block:: bash

    $ conan_build_info --v2 start MyBuildName 42

2. Call Conan using :ref:`lockfiles<versioning_lockfiles>` to create information for the 
`Build Info json format <https://github.com/jfrog/build-info>`_.

.. code-block:: bash

    $ cd mypackage
    $ conan create . mypackage/1.0@user/stable # We create one package
    $ cd .. && cd consumer
    $ conan install . # Consumes mypackage, generates a lockfile
    $ conan create . consumer/1.0@user/stable --lockfile conan.lock
    $ conan upload "*" -c -r local # Upload all packages to local remotes

3. Create build information based on the contents of the generated `conan.lock` lockfile and the
information retrieved from the remote (the authentication is for the remote where you uploaded the
packages).

.. code-block:: bash

    $ conan_build_info --v2 create buildinfo.json --lockfile conan.lock --user admin --password password


4. Publish the build information to Artifactory with the ``publish`` subcommand:

Using user and password

.. code-block:: bash

    $ conan_build_info --v2 publish buildinfo.json --url http://localhost:8081/artifactory --user admin --password password

or an API key:

.. code-block:: bash

    $ conan_build_info --v2 publish buildinfo.json --url http://localhost:8081/artifactory --apikey apikey

5. If the whole process has finished and you don't want to continue associating the build number and
build name to the files uploaded to Artifactory then you can use the ``stop`` subcommand:

.. code-block:: bash

    $ conan_build_info --v2 stop

It is also possible to merge different build info files using the ``update`` subcommand. This is
useful in CI when `many slaves <https://github.com/conan-io/examples/tree/master/features/lockfiles/ci>`_ 
are generating different build info files.

.. code-block:: bash

    $ conan_build_info --v2 update buildinfo1.json buildinfo2.json --output-file mergedbuildinfo.json

You can check the complete :ref:`conan_build_info reference<conan_build_info>`.