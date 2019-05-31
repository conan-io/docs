import os
import platform
import subprocess
import sys

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
    "editable": "development",
    "workspace": "development",


    "alias": "misc",
    "copy": "misc",
    "download": "misc",
    "help": "misc",
    "imports": "misc",
    "inspect": "misc",
    "profile": "misc",
    "remote": "misc",
    "remove": "misc",
    "user": "misc"
}

experimental = ["inspect"]
commands = folder.keys()


conan_name = ""
try:
    conan_name = sys.argv[1]
except IndexError:
    conan_name = "conan"

template = """.. _conan_{0}:

conan {0}
======{1}
{2}
.. code-block:: bash

    $ {3}
{4}

.. code-block:: text

{5}"""


for command in commands:
    execute = [conan_name, command, "-h"]
    print(execute)
    output = str(subprocess.check_output(execute))
    output = output.rstrip()
    search_string = "conan %s [-h]" % command
    output = search_string + output.split(search_string)[1]
    output = output.split("\\r\\n\\r\\n" if platform.system() == "Windows" else "\\n\\n", 2)

    underline = ""
    for char in command:
        underline += "="

    small_help = ""
    for line in output[0].replace("\\r", "").replace("\\n", "\n").splitlines():
        if not line.startswith("conan"):
            line = line[1:]
        small_help += "%s\n" % line.rstrip()

    text_help = output[1].replace("\\r", "").replace("\\n", "\n").rstrip()

    if output[2].startswith("positional arguments"):
        args_text = output[2]
    else:
        tmp = output[2].split("positional arguments")
        text_help += "\n\n" + tmp[0].replace("\\r", "").replace("\\n", "\n").rstrip()
        args_text = "positional arguments" + tmp[1]

    arguments_help = ""
    for line in args_text.replace("\\r", "").replace("\\n", "\n").splitlines():
        if line == "'" or line == "\"":
            continue
        arguments_help += ("    %s\n" % line) if line else "\n"

    arguments_help = arguments_help.rstrip()
    print(arguments_help)

    text_experimental = """
.. warning::

      This is an **experimental** feature subject to breaking changes in future releases.

""" if command in experimental else ""
    text = template.format(command, underline, text_experimental, small_help, text_help,
                           arguments_help)
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
