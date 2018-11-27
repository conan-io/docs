import os
import platform
import subprocess
import sys

commands = ["config", "get", "info", "install", "search", "create", "export-pkg", "export", "new",
            "test", "upload", "build", "package", "source", "alias", "copy", "download", "help",
            "imports", "profile", "remote", "remove", "user"]

folder = {
    "config": "consumer",
    "get": "consumer",
    "info": "consumer",
    "install": "consumer",
    "search": "consumer",
    "create": "creator",
    "export-pkg": "creator",
    "export": "creator",
    "new": "creator",
    "test": "creator",
    "upload": "creator",
    "build": "development",
    "package": "development",
    "source": "development",
    "alias": "misc",
    "copy": "misc",
    "download": "misc",
    "help": "misc",
    "imports": "misc",
    "profile": "misc",
    "remote": "misc",
    "remove": "misc",
    "user": "misc"
}

conan_name = ""
try:
    conan_name = sys.argv[1]
except IndexError:
    conan_name = "conan"

template = """.. _conan_{0}:

conan {0}
======{1}

.. code-block:: bash

    $ {2}
{3}

.. code-block:: text

{4}"""

for command in commands:
    execute = [conan_name, command, "-h"]
    print(execute)
    output = str(subprocess.check_output(execute))
    output = output.rstrip()
    search_string = "conan %s [-h]" % command
    output = search_string + output.split(search_string)[1]
    output = output.split("\\r\\n\\r\\n" if platform.system() == "Windows" else "\n\n", 2)

    underline = ""
    for char in command:
        underline += "="

    small_help = ""
    for line in output[0].replace("\\r", "").replace("\\n", "\n").splitlines():
        if not line.startswith("conan"):
            line = line[1:]
        small_help += "%s\n" % line.rstrip()

    text_help = output[1].replace("\\r", "").replace("\\n", "\n").rstrip()

    arguments_help = ""
    for line in output[2].replace("\\r", "").splitlines():
        arguments_help += ("    %s\n" % line) if line else "\n"

    arguments_help = arguments_help.rstrip()

    text = template.format(command, underline, small_help, text_help, arguments_help)
    text = text.replace("\\'", "\'")

    filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "reference", "commands",
                            folder[command], command)
    print("filepath:", filepath)
    the_file = open("%s.rst" % filepath, "r")
    content = the_file.read()
    the_file.close()

    the_file = open("%s.rst" % filepath, "w")

    separator = "\n\n\n"

    begin = content.find(".. _conan_%s" % command) # To avoid deleting ..spelling:: and other stuff
    prev_content = content[0:begin]
    rest_content = content[begin + 1:]
    if rest_content:
        rest_content = rest_content.split(separator, 1)
        if len(rest_content) > 1:
            the_file.write(prev_content + text + separator + rest_content[1])
        else:
            raise Exception("Separator (two consecutive newlines) not found")
    else:
        the_file.write(text)
    the_file.close()
