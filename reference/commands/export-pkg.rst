.. _reference_commands_export-pkg:

conan export-pkg
================

.. code-block:: text

    $ conan export-pkg -h
    usage: conan export-pkg [-h] [-f FORMAT] [-v [V]] [-of OUTPUT_FOLDER] [--build-require] [-tf TEST_FOLDER] [-sb] [-r REMOTE | -nr] [--name NAME]              
                        [--version VERSION] [--user USER] [--channel CHANNEL] [-l LOCKFILE] [--lockfile-partial] [--lockfile-out LOCKFILE_OUT]               
                        [--lockfile-packages] [--lockfile-clean] [-o OPTIONS_HOST] [-o:b OPTIONS_BUILD] [-o:h OPTIONS_HOST] [-pr PROFILE_HOST]               
                        [-pr:b PROFILE_BUILD] [-pr:h PROFILE_HOST] [-s SETTINGS_HOST] [-s:b SETTINGS_BUILD] [-s:h SETTINGS_HOST] [-c CONF_HOST]              
                        [-c:b CONF_BUILD] [-c:h CONF_HOST]                                                                                                   
                        path                                                                                                                                 
                                                                                                                                                             
    Create a package directly from pre-compiled binaries.                                                                                                        
                                                                                                                                                                
    positional arguments:                                                                                                                                        
      path                  Path to a folder containing a recipe (conanfile.py)                                                                                  
                                                                                                                                                                
    optional arguments:                                                                                                                                          
      -h, --help            show this help message and exit                                                                                                      
      -f FORMAT, --format FORMAT                                                                                                                                 
                            Select the output format: json                                                                                                       
      -v [V]                Level of detail of the output. Valid options from less verbose to more verbose: -vquiet, -verror, -vwarning, -vnotice, -vstatus, -v  
                            or -vverbose, -vv or -vdebug, -vvv or -vtrace                                                                                        
      -of OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER                                                                                                           
                            The root output folder for generated and build files                                                                                 
      --build-require       Whether the provided reference is a build-require                                                                                    
      -tf TEST_FOLDER, --test-folder TEST_FOLDER                                                                                                                 
                            Alternative test folder name. By default it is "test_package". Use "" to skip the test stage                                         
      -sb, --skip-binaries  Skip installing dependencies binaries                                                                                                
      -r REMOTE, --remote REMOTE                                                                                                                                 
                            Look in the specified remote or remotes server                                                                                       
      -nr, --no-remote      Do not use remote, resolve exclusively in the cache                                                                                  
      --name NAME           Provide a package name if not specified in conanfile                                                                                 
      --version VERSION     Provide a package version if not specified in conanfile                                                                              
      --user USER           Provide a user if not specified in conanfile                                                                                         
      --channel CHANNEL     Provide a channel if not specified in conanfile                                                                                      
      -l LOCKFILE, --lockfile LOCKFILE                                                                                                                           
                            Path to a lockfile. Use --lockfile="" to avoid automatic use of existing 'conan.lock' file                                           
      --lockfile-partial    Do not raise an error if some dependency is not found in lockfile                                                                    
      --lockfile-out LOCKFILE_OUT                                                                                                                                
                            Filename of the updated lockfile                                                                                                     
      --lockfile-packages   Lock package-id and package-revision information                                                                                     
      --lockfile-clean      Remove unused entries from the lockfile                                                                                              
      -o OPTIONS_HOST, --options OPTIONS_HOST                                                                                                                    
                            Define options values (host machine), e.g.: -o Pkg:with_qt=true                                                                      
      -o:b OPTIONS_BUILD, --options:build OPTIONS_BUILD                                                                                                          
                            Define options values (build machine), e.g.: -o:b Pkg:with_qt=true                                                                   
      -o:h OPTIONS_HOST, --options:host OPTIONS_HOST                                                                                                             
                            Define options values (host machine), e.g.: -o:h Pkg:with_qt=true                                                                    
      -pr PROFILE_HOST, --profile PROFILE_HOST                                                                                                                   
                            Apply the specified profile to the host machine                                                                                      
      -pr:b PROFILE_BUILD, --profile:build PROFILE_BUILD                                                                                                         
                            Apply the specified profile to the build machine                                                                                     
      -pr:h PROFILE_HOST, --profile:host PROFILE_HOST                                                                                                            
                            Apply the specified profile to the host machine                                                                                      
      -s SETTINGS_HOST, --settings SETTINGS_HOST                                                                                                                 
                            Settings to build the package, overwriting the defaults (host machine). e.g.: -s compiler=gcc                                        
      -s:b SETTINGS_BUILD, --settings:build SETTINGS_BUILD                                                                                                       
                            Settings to build the package, overwriting the defaults (build machine). e.g.: -s:b compiler=gcc                                     
      -s:h SETTINGS_HOST, --settings:host SETTINGS_HOST                                                                                                          
                            Settings to build the package, overwriting the defaults (host machine). e.g.: -s:h compiler=gcc                                      
      -c CONF_HOST, --conf CONF_HOST                                                                                                                             
                            Configuration to build the package, overwriting the defaults (host machine). e.g.: -c tools.cmake.cmaketoolchain:generator=Xcode     
      -c:b CONF_BUILD, --conf:build CONF_BUILD                                                                                                                   
                            Configuration to build the package, overwriting the defaults (build machine). e.g.: -c:b tools.cmake.cmaketoolchain:generator=Xcode  
      -c:h CONF_HOST, --conf:host CONF_HOST                                                                                                                      
                            Configuration to build the package, overwriting the defaults (host machine). e.g.: -c:h tools.cmake.cmaketoolchain:generator=Xcode   
                                                                                                                                                             

The ``conan export-pkg`` command creates a package binary directly from pre-compiled binaries in a user folder. This command can be useful in different cases:

- When creating a package for some closed source or pre-compiled binaries provided by a vendor. In this case, it is not necessary that the ``conanfile.py`` recipe contains a ``build()`` method, and providing the ``package()`` and ``package_info()`` method are enough to package those pre-compiled binaries. In this case the ``build_policy = "never"`` could make sense to indicate it is not possible to ``conan install --build=this_pkg``, as it doesn't know how to build from sources when it is a dependency.
- When testing some recipe locally in the :ref:`local development flow<local_package_development_flow>`, it can be used to quickly put the locally built binaries in the cache to make them available to other packages for testing, without needing to go through a full ``conan create`` that would be slower.

In general, it is expected that when ``conan export-pkg`` executes, the possible Conan dependencies that were necessary to build this package had already been installed via ``conan install``, so it is not necessary to download dependencies at ``export-pkg`` time. But if for some reason this is not the case, the command defines ``--remote`` and ``--no-remote`` arguments, similar to other commands, as well as the ``--skip-binaries`` optimization that could save some time installing dependencies binaries if they are not strictly necessary for the current ``export-pkg``. But this is the responsibility of the user, as it is possible that such binaries are actually necessary, for example, if a ``tool_requires = "cmake/x.y"`` is used and the ``package()`` method implements a ``cmake.install()`` call, this will definitely need the binaries for the dependencies installed in the current machine to execute.


.. seealso::

    - Check the :ref:`JSON format output <reference_commands_graph_info_json_format>` for this command.
    - Read the tutorial about the :ref:`local package development flow <local_package_development_flow>`.
