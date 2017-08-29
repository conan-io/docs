.. _create_command:

conan create
============

.. code-block:: bash

	$  conan create [-h] [-ne] [-tf TEST_FOLDER] [--keep-source] [--cwd CWD]
                    [--manifests [MANIFESTS]]
                    [--manifests-interactive [MANIFESTS_INTERACTIVE]]
                    [--verify [VERIFY]] [--update] [--scope SCOPE]
                    [--profile PROFILE] [-r REMOTE] [--options OPTIONS]
                    [--settings SETTINGS] [--env ENV]
                    [--build [BUILD [BUILD ...]]]
                    reference


Create and test a package. Export, build package and test it with a consumer
project if test_package exists. The consumer project must have a
'conanfile.py' with a 'test()' method, and should be located in a subfolder,
named 'test_package` by default.


.. code-block:: bash

    positional arguments:                                                         
        reference             a full package reference Pkg/version@user/channel, or 
                                just the user/channel if package and version are      
                                defined in recipe                                     
                                                                                    
    optional arguments:                                                           
        -h, --help            show this help message and exit                       
        -ne, --not-export     Do not export the conanfile                           
        -tf TEST_FOLDER, --test_folder TEST_FOLDER                                  
                                alternative test folder name, by default is           
                                "test_package"                                        
        --keep-source, -k     Optional. Do not remove the source folder in local    
                                cache. Use for testing purposes only                  
        --cwd CWD, -c CWD     Use this directory as the current directory           
        --manifests [MANIFESTS], -m [MANIFESTS]                                     
                                Install dependencies manifests in folder for later    
                                verify. Default folder is .conan_manifests, but can be
                                changed                                               
        --manifests-interactive [MANIFESTS_INTERACTIVE], -mi [MANIFESTS_INTERACTIVE]
                                Install dependencies manifests in folder for later    
                                verify, asking user for confirmation. Default folder  
                                is .conan_manifests, but can be changed               
        --verify [VERIFY], -v [VERIFY]                                              
                                Verify dependencies manifests against stored ones     
        --update, -u          check updates exist from upstream remotes             
        --scope SCOPE, -sc SCOPE                                                    
                                Use the specified scope in the install command        
        --profile PROFILE, -pr PROFILE                                              
                                Apply the specified profile to the install command    
        -r REMOTE, --remote REMOTE                                                  
                                look in the specified remote server                   
        --options OPTIONS, -o OPTIONS                                               
                                Options to build the package, overwriting the         
                                defaults. e.g., -o with_qt=true                       
        --settings SETTINGS, -s SETTINGS                                            
                                Settings to build the package, overwriting the        
                                defaults. e.g., -s compiler=gcc                       
        --env ENV, -e ENV     Environment variables that will be set during the     
                                package build, -e CXX=/usr/bin/clang++                
        --build [BUILD [BUILD ...]], -b [BUILD [BUILD ...]]                         
                                Optional, use it to choose if you want to build from  
                                sources: --build Build all from sources, do not use   
                                binary packages. --build=never Default option. Never  
                                build, use binary packages or fail if a binary package
                                is not found. --build=missing Build from code if a    
                                binary package is not found. --build=outdated Build   
                                from code if the binary is not built with the current 
                                recipe or when missing binary package.                
                                --build=[pattern] Build always these packages from    
                                source, but never build the others. Allows multiple   
                                --build parameters.                                   


This is the recommended way to create packages.

``conan create demo/testing`` is equivalent to:

.. code-block:: bash

    $ conan export demo/testing
    $ conan install Hello/0.1@demo/testing --build=Hello
    # package is created now, use test_package to test it
    $ conan test_package demo/testing --test-only