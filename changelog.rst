Changelog
=========

For a more detailed description of the major changes that Conan 2.0 brings, compared with Conan 1.X, please read :ref:`whatsnew`

2.0.1 (03-Mar-2023)
-------------------

- Feature: Add `--insecure` alias to `--verify-ssl` in config install. `#13270 <https://github.com/conan-io/conan/pull/13270>`_ . Docs `here <https://github.com/conan-io/docs/pull/3035>`__
- Feature: Add `.conanignore` support to `conan config install`. `#13269 <https://github.com/conan-io/conan/pull/13269>`_ . Docs `here <https://github.com/conan-io/docs/pull/3036>`__
- Feature: Make verbose tracebacks on exception be shown for ``-vv`` and ``-vvv``, instead of custom env-var used in 1.X. `#13226 <https://github.com/conan-io/conan/pull/13226>`_
- Fix: Minor improvements to :command:`conan install` and 2.0-readiness error messages. `#13299 <https://github.com/conan-io/conan/pull/13299>`_
- Fix: Remove ``vcvars.bat`` VS telemetry env-var, to avoid Conan hanging. `#13293 <https://github.com/conan-io/conan/pull/13293>`_
- Fix: Remove legacy ``CMakeToolchain`` support for ``CMakePresets`` schema2 for ``CMakeUserPresets.json``. `#13288 <https://github.com/conan-io/conan/pull/13288>`_ . Docs `here <https://github.com/conan-io/docs/pull/3049>`__
- Fix: Remove ``--logger`` json logging and legacy traces. `#13287 <https://github.com/conan-io/conan/pull/13287>`_ . Docs `here <https://github.com/conan-io/docs/pull/3050>`__
- Fix: Fix typo in `conan remote auth` help. `#13285 <https://github.com/conan-io/conan/pull/13285>`_ . Docs `here <https://github.com/conan-io/docs/pull/3039>`__
- Fix: Raise arg error if ``conan config list unexpected-arg``. `#13282 <https://github.com/conan-io/conan/pull/13282>`_
- Fix: Do not auto-detect ``compiler.runtime_type`` for ``msvc``, rely on profile plugin. `#13277 <https://github.com/conan-io/conan/pull/13277>`_
- Fix: Fix conanfile.txt options parsing error message. `#13266 <https://github.com/conan-io/conan/pull/13266>`_
- Fix: Improve error message for unified patterns in options. `#13264 <https://github.com/conan-io/conan/pull/13264>`_
- Fix: Allow ``conan remote add --force`` to force re-definition of an existing remote name. `#13249 <https://github.com/conan-io/conan/pull/13249>`_
- Fix: Restore printing of profiles for build command. `#13214 <https://github.com/conan-io/conan/pull/13214>`_
- Fix: Change :command:`conan build` argument description for "path" to indicate it is only for conanfile.py and explicitly state that it does not work with conanfile.txt. `#13211 <https://github.com/conan-io/conan/pull/13211>`_ . Docs `here <https://github.com/conan-io/docs/pull/3046>`__
- Fix: Better error message when dependencies ``options`` are defined in ``requirements()`` method. `#13207 <https://github.com/conan-io/conan/pull/13207>`_
- Fix: Fix broken links to docs from error messages and readme. `#13186 <https://github.com/conan-io/conan/pull/13186>`_
- Bugfix: Ensure that `topics` are always serialized as lists. `#13298 <https://github.com/conan-io/conan/pull/13298>`_
- Bugfix: Ensure that `provides` are always serialized as lists. `#13298 <https://github.com/conan-io/conan/pull/13298>`_
- Bugfix: Fixed the detection of certain visual c++ installations. `#13284 <https://github.com/conan-io/conan/pull/13284>`_
- Bugfix: Fix supported ``cppstd`` values for ``msvc`` compiler. `#13278 <https://github.com/conan-io/conan/pull/13278>`_
- Bugfix: CMakeDeps generate files for ``tool_requires`` with the same ``build_type`` as the "host" context. `#13267 <https://github.com/conan-io/conan/pull/13267>`_
- Bugfix: Fix definition of patterns for dependencies options in configure(). `#13263 <https://github.com/conan-io/conan/pull/13263>`_
- Bugfix: Fix CMakeToolchain error when output folder in different Win drive. `#13248 <https://github.com/conan-io/conan/pull/13248>`_
- Bugfix: Do not raise errors if a ``test_requires`` is not used by components ``.requires``. `#13191 <https://github.com/conan-io/conan/pull/13191>`_

2.0.0 (22-Feb-2023)
-------------------

- Feature: Change default profile cppstd for apple-clang to gnu17. `#13185 <https://github.com/conan-io/conan/pull/13185>`_ 
- Feature: New ``conan remote auth`` command to force authentication in the remotes `#13180 <https://github.com/conan-io/conan/pull/13180>`_ 
- Fix: Allow defining options trait in ``test_requires(..., options={})`` `#13178 <https://github.com/conan-io/conan/pull/13178>`_ 
- Fix: Unifying Conan commands help messages. `#13176 <https://github.com/conan-io/conan/pull/13176>`_ 
- Bugfix: Fix MesonToolchain wrong cppstd in apple-clang `#13172 <https://github.com/conan-io/conan/pull/13172>`_ 
- Feature: Improved global Conan output messages (create, install, export, etc.) `#12746 <https://github.com/conan-io/conan/pull/12746>`_ 

2.0.0-beta10 (16-Feb-2023)
--------------------------

- Feature: Add basic html output to `conan list` command. `#13135 <https://github.com/conan-io/conan/pull/13135>`_
- Feature: Allow ``test_package`` to process ``--build`` arguments (computing --build=never for the main, non test_package graph). `#13117 <https://github.com/conan-io/conan/pull/13117>`_
- Feature: Add `--force` argument to remote add. `#13112 <https://github.com/conan-io/conan/pull/13112>`_
- Feature: Validate if the input configurations exist, to avoid typos. `#13110 <https://github.com/conan-io/conan/pull/13110>`_
- Feature: Allow defining ``self.folders.build_folder_vars`` in recipes ``layout()``. `#13109 <https://github.com/conan-io/conan/pull/13109>`_
- Feature: Block settings assignment. `#13099 <https://github.com/conan-io/conan/pull/13099>`_
- Feature: Improve `conan editable` ui. `#13093 <https://github.com/conan-io/conan/pull/13093>`_
- Feature: Provide the ability for users to extend Conan generated CMakePresets. `#13090 <https://github.com/conan-io/conan/pull/13090>`_
- Feature: Add error messages to help with the migration of recipes to 2.0, both from ConanCenter and from user repos. `#13074 <https://github.com/conan-io/conan/pull/13074>`_
- Feature: Remove option.fPIC for shared in :command:`conan new` templates. `#13066 <https://github.com/conan-io/conan/pull/13066>`_
- Feature: Add `conan cache clean` subcommand to clean build and source folders. `#13050 <https://github.com/conan-io/conan/pull/13050>`_
- Feature: Implement customizable ``CMakeToolchain.presets_prefix`` so presets name prepend this. `#13015 <https://github.com/conan-io/conan/pull/13015>`_
- Feature: Add `[system_tools]` section to profiles to use your own installed tools instead of the packages declared in the requires. `#10166 <https://github.com/conan-io/conan/pull/10166>`_
- Fix: Fixes in powershell escaping. `#13084 <https://github.com/conan-io/conan/pull/13084>`_
- Fix: Define ``CMakeToolchain.presets_prefix="conan"`` by default, to avoid conflict with other users presets. `#13015 <https://github.com/conan-io/conan/pull/13015>`_

2.0.0-beta9 (31-Jan-2023)
-------------------------

- Feature: Add package names in Conan cache hash paths. `#13011 <https://github.com/conan-io/conan/pull/13011>`_
- Feature: Implement ``tools.build:download_source`` conf to force the installation of sources in :command:`conan install` or ``conan graph info``. `#13003 <https://github.com/conan-io/conan/pull/13003>`_
- Feature: Users can define their own settings in `settings_user.yml` that will be merged with the Conan `settings.yml`. `#12980 <https://github.com/conan-io/conan/pull/12980>`_
- Feature: List disabled remotes too. `#12937 <https://github.com/conan-io/conan/pull/12937>`_
- Fix: PkgConfiDeps is using the wrong ``dependencies.host`` from dependencies instead of ``get_transitive_requires()`` computation. `#13013 <https://github.com/conan-io/conan/pull/13013>`_
- Fix: Fixing transitive shared linux libraries in CMakeDeps. `#13010 <https://github.com/conan-io/conan/pull/13010>`_
- Fix: Fixing issues with test_package output folder. `#12992 <https://github.com/conan-io/conan/pull/12992>`_
- Fix: Improve error messages for wrong methods. `#12962 <https://github.com/conan-io/conan/pull/12962>`_
- Fix: Fix fail in parallel packages download due to database concurrency issues. `#12930 <https://github.com/conan-io/conan/pull/12930>`_
- Fix: Enable authentication against disabled remotes. `#12913 <https://github.com/conan-io/conan/pull/12913>`_
- Fix: Improving system_requirements. `#12912 <https://github.com/conan-io/conan/pull/12912>`_
- Fix: Change tar format to PAX, which is the Python3.8 default. `#12899 <https://github.com/conan-io/conan/pull/12899>`_

2.0.0-beta8 (12-Jan-2023)
-------------------------

- Feature: Add `unix_path_package_info_legacy` function for those cases in which it is used in `package_info` in recipes that require compatibility with Conan 1.x. In Conan 2, path conversions should not be performed in the `package_info` method. `#12886 <https://github.com/conan-io/conan/pull/12886>`_
- Feature: New serialization json and printing for ``conan list``. `#12883 <https://github.com/conan-io/conan/pull/12883>`_
- Feature: Add requirements to `conan new cmake_{lib,exe}` `#12875 <https://github.com/conan-io/conan/pull/12875>`_
- Feature: Allow ``--no-remotes`` to force temporal disabling of remotes `#12808 <https://github.com/conan-io/conan/pull/12808>`_
- Feature: Add barebones template option to conan new. `#12802 <https://github.com/conan-io/conan/pull/12802>`_
- Feature: Avoid requesting package configuration if PkgID is passed. `#12801 <https://github.com/conan-io/conan/pull/12801>`_
- Feature: Implemented `conan list *#latest` and `conan list *:*#latest`. Basically, this command can show the latest RREVs and PREVs for all the matching references. `#12781 <https://github.com/conan-io/conan/pull/12781>`_
- Feature: Allow chaining of `self.output` write methods `#12780 <https://github.com/conan-io/conan/pull/12780>`_
- Fix: Make ``graph info`` filters to work on json output too `#12836 <https://github.com/conan-io/conan/pull/12836>`_
- Bugfix: Fix bug to pass a valid GNU triplet when using AutotoolsToolchain and cross-building on Windows. `#12881 <https://github.com/conan-io/conan/pull/12881>`_
- Bugfix: Ordering if same ref.name but different versions. `#12801 <https://github.com/conan-io/conan/pull/12801>`_

2.0.0-beta7 (22-Dec-2022)
-------------------------

- Feature: Raise an error when a generator is both defined in generators attribute and instantiated in generate() method `#12722 <https://github.com/conan-io/conan/pull/12722>`_
- Feature: `test_requires` improvements, including allowing it in conanfile.txt `#12699 <https://github.com/conan-io/conan/pull/12699>`_
- Feature: Improve errors for when required_conan_version has spaces between the operator and the version `#12695 <https://github.com/conan-io/conan/pull/12695>`_
- Feature: ConanAPI cleanup and organization `#12666 <https://github.com/conan-io/conan/pull/12666>`_

2.0.0-beta6 (02-Dec-2022)
-------------------------

- Feature: Use ``--confirm`` to not request confirmation when removing instead of ``--force`` `#12636 <https://github.com/conan-io/conan/pull/12636>`_
- Feature: Simplify loading conaninfo.txt for search results `#12616 <https://github.com/conan-io/conan/pull/12616>`_
- Feature: Renamed ConanAPIV2 to ConanAPI `#12615 <https://github.com/conan-io/conan/pull/12615>`_
- Feature: Refactor ConanAPI `#12615 <https://github.com/conan-io/conan/pull/12615>`_
- Feature: Improve conan cache path command `#12554 <https://github.com/conan-io/conan/pull/12554>`_
- Feature: Improve #latest and pattern selection from remove/upload/download `#12572 <https://github.com/conan-io/conan/pull/12572>`_
- Feature: Add build_modules to provided deprecated warning to allow migration from 1.x `#12578 <https://github.com/conan-io/conan/pull/12578>`_
- Feature: Lockfiles alias support `#12525 <https://github.com/conan-io/conan/pull/12525>`_

2.0.0-beta5 (11-Nov-2022)
-------------------------

- Feature: Improvements in the remotes management and API `#12468 <https://github.com/conan-io/conan/pull/12468>`_
- Feature: Implement env_info and user_info as fake attributes in Conan 2.0 `#12351 <https://github.com/conan-io/conan/pull/12351>`_
- Feature: Improve settings.rm_safe() `#12379 <https://github.com/conan-io/conan/pull/12379>`_
- Feature: New RecipeReference equality `#12506 <https://github.com/conan-io/conan/pull/12506>`_
- Feature: Simplifying compress and uncompress of .tgz files `#12378 <https://github.com/conan-io/conan/pull/12378>`_
- Feature: conan source command does not require a default profile `#12475 <https://github.com/conan-io/conan/pull/12475>`_
- Feature: Created a proper LockfileAPI, with detailed methods (update, save, etc), instead of several loose methods `#12502 <https://github.com/conan-io/conan/pull/12502>`_
- Feature: The conan export can also produce lockfiles, necessary for users doing a 2 step (export + install--build) process `#12502 <https://github.com/conan-io/conan/pull/12502>`_
- Feature: Drop compat_app `#12484 <https://github.com/conan-io/conan/pull/12484>`_
- Fix: Fix transitive propagation of transitive_headers=True `#12508 <https://github.com/conan-io/conan/pull/12508>`_
- Fix: Fix transitive propagation of transitive_libs=False for static libraries `#12508 <https://github.com/conan-io/conan/pull/12508>`_
- Fix: Fix test_package for python_requires `#12508 <https://github.com/conan-io/conan/pull/12508>`_

2.0.0-beta4 (11-Oct-2022)
-------------------------

- Feature: Do not allow doing conan create/export with uncommitted changes using revision_mode=scm `#12267 <https://github.com/conan-io/conan/pull/12267>`_
- Feature: Simplify conan inspect command, removing path subcommand `#12263 <https://github.com/conan-io/conan/pull/12263>`_
- Feature: Add --deploy argument to graph info command `#12243 <https://github.com/conan-io/conan/pull/12243>`_
- Feature: Pass graph object to deployers instead of ConanFile `#12243 <https://github.com/conan-io/conan/pull/12243>`_
- Feature: Add included_files method to conan.tools.scm.Git `#12246 <https://github.com/conan-io/conan/pull/12246>`_
- Feature: Improve detection of clang libcxx `#12251 <https://github.com/conan-io/conan/pull/12251>`_
- Feature: Remove old profile variables system in favor of Jinja2 syntax in profiles `#12152 <https://github.com/conan-io/conan/pull/12152>`_
- Fix: Update command to follow Conan 2.0 conventions about CLI output `#12235 <https://github.com/conan-io/conan/pull/12235>`_
- Fix: Fix aggregation of test trait in diamonds `#12080 <https://github.com/conan-io/conan/pull/12080>`_

2.0.0-beta3 (12-Sept-2022)
--------------------------

- Feature: Decouple test_package from create. `#12046 <https://github.com/conan-io/conan/pull/12046>`_
- Feature: Warn if special chars in exported refs. `#12053 <https://github.com/conan-io/conan/pull/12053>`_
- Feature: Improvements in MSBuildDeps traits. `#12032 <https://github.com/conan-io/conan/pull/12032>`_
- Feature: Added support for CLICOLOR_FORCE env var, that will activate the colors in the output if the value is declared and different to 0. `#12028 <https://github.com/conan-io/conan/pull/12028>`_
- Fix: Call source() just once for all configurations. `#12050 <https://github.com/conan-io/conan/pull/12050>`_
- Fix: Fix deployers not creating output_folder. `#11977 <https://github.com/conan-io/conan/pull/11977>`_
- Fix: Fix build_id() removal of require. `#12019 <https://github.com/conan-io/conan/pull/12019>`_
- Fix: If Conan fails to load a custom command now it fails with a useful error message. `#11720 <https://github.com/conan-io/conan/pull/11720>`_
- Bugfix: If the 'os' is not specified in the build profile and a recipe, in Windows, wanted to run a command. `#11728 <https://github.com/conan-io/conan/pull/11728>`_

2.0.0-beta2 (27-Jul-2022)
-------------------------

- Feature: Add traits support in MSBuildDeps. `#11680 <https://github.com/conan-io/conan/pull/11680>`_
- Feature: Add traits support in XcodeDeps. `#11615 <https://github.com/conan-io/conan/pull/11615>`_
- Feature: Let dependency define package_id modes. `# <https://github.com/conan-io/conan/pull/11441>`_
- Feature: Add ``conan.conanrc`` file to setup the conan user home. `#11675 <https://github.com/conan-io/conan/pull/11675>`_
- Feature: Add ``core.cache:storage_path`` to declare the absolute path where you want to store the Conan packages. `#11672 <https://github.com/conan-io/conan/pull/11672>`_ 
- Feature: Add tools for checking max cppstd version. `#11610 <https://github.com/conan-io/conan/pull/11610>`_ 
- Feature: Add a ``post_build_fail`` hook that is called when a build fails. `#11593 <https://github.com/conan-io/conan/pull/11593>`_ 
- Feature: Add ``pre_generate`` and ``post_generate`` hook, covering the generation of files around the ``generate()`` method call. `#11593 <https://github.com/conan-io/conan/pull/11593>`_ 
- Feature: Brought ``conan config list`` command back and other conf improvements. `#11575 <https://github.com/conan-io/conan/pull/11575>`_ 
- Feature: Added two new arguments for all commands -v for controlling the verbosity of the output and --logger to output the contents in a json log format for log processors. `#11522 <https://github.com/conan-io/conan/pull/11522>`_ 

2.0.0-beta1 (20-Jun-2022)
-------------------------

- Feature: New graph model to better support C and C++ binaries relationships, compilation, and linkage.
- Feature: New documented public Python API, for user automation
- Feature: New build system integrations, more flexible and powerful, and providing transparent integration when possible, like ``CMakeDeps`` and ``CMakeToolchain``
- Feature: New custom user commands, that can be built using the public PythonAPI and can be shared and installed with ``conan config install``
- Feature: New CLI interface, with cleaner commands and more structured output
- Feature: New deployers mechanism to copy artifacts from the cache to user folders, and consume those copies while building.
- Feature: Improved ``package_id`` computation, taking into account the new more detailed graph model.
- Feature: Added ``compatibility.py`` extension mechanism to allow users to define binary compatibility globally.
- Feature: Simpler and more powerful ``lockfiles`` to provide reproducibility over time.
- Feature: Better configuration with ``[conf]`` and better environment management with the new ``conan.tools.env`` tools.
- Feature: Conan cache now can store multiple revisions simultaneously.
- Feature: New extensions plugins to implement profile checking, package signing, and build commands wrapping.
- Feature: Used the package immutability for an improved update, install and upload flows.
