.. _conan_custom_commands:

Custom commands
=================



Create a new command
---------------------


.. code-block:: python
    :caption: cmd_hello.py

    from conan.api.conan_api import ConanAPIV2
    from conans.cli.command import conan_command
    from conans.cli.output import ConanOutput


    @conan_command(group="Custom commands")
    def hello(conan_api: ConanAPIV2, parser, *args, **kwargs):
        """
        Simple command to print "Hello World!" line
        """
        ConanOutput().info("Hello World!")


Scoping
----------


.. code-block:: python
    :caption: greetings/cmd_bye.py

    from conan.api.conan_api import ConanAPIV2
    from conans.cli.command import conan_command
    from conans.cli.output import ConanOutput


    @conan_command(group="Custom commands")
    def bye(conan_api: ConanAPIV2, parser, *args, **kwargs):
        """
        Simple command to print "Hello World!" line
        """
        ConanOutput().info("Bye World!")




Formatters
-----------


.. code-block:: python
    :caption: cmd_cache_folder.py

    import json
    import os

    from conan.api.conan_api import ConanAPIV2
    from conans.cli.command import conan_command


    def output_mycommand_cli(info):
        return f"Conan cache folder is: {info.get('cache_folder')}"


    def output_mycommand_json(info):
        return json.dumps(info)


    @conan_command(group="custom commands",
                   formatters={"cli": output_mycommand_cli,
                               "json": output_mycommand_json})
    def cache_folder(conan_api: ConanAPIV2, parser, *args, **kwargs):
        """
        Prints the location of the cache folder
        """
        return {"cache_folder": os.path.basename(conan_api.cache_folder)}
