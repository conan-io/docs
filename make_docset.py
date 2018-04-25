BUILD_DIR = "_build"

import doc2dash.__main__
import doc2dash.parsers

from doc2dash.parsers.intersphinx import (InterSphinxParser, inv_entry_to_path,
                                          ParserEntry)


class InterSphinxWithUserGuide(InterSphinxParser):
    def convert_type(self, inv_type):
        #print("Processing type {}".format(inv_type))
        if inv_type == "std:doc":
            return "Guide"
        elif inv_type == "std:cmdoption":
            return "Option"
        elif inv_type == "std:label":
            return "Label"
        return super(InterSphinxWithUserGuide, self).convert_type(inv_type)

    def create_entry(self, dash_type, key, inv_entry):
        #print(dash_type, key, inv_entry)  # for debugging
        entry_name = inv_entry[3]
        if dash_type == "Guide":
            if inv_entry[2].startswith("reference/config_files/"):
                dash_type = "File"
            elif inv_entry[2].startswith("reference/generators/"):
                dash_type = "Plugin"
            elif inv_entry[2].startswith("reference/commands/"):
                dash_type = "Command"
                entry_name = inv_entry[3].replace("conan ", "")
            elif inv_entry[2].startswith("reference/build_helpers/"):
                dash_type = "Class"
            path_str = inv_entry_to_path(inv_entry)
            return ParserEntry(name=entry_name, type=dash_type, path=path_str)
        elif dash_type == "Label":
            if inv_entry[2].startswith("reference/conanfile/methods"):
                if key.startswith("method_package_info_"):
                    return None
                dash_type = "Method"
                entry_name = key.replace("method_", "")
            elif inv_entry[2].startswith("reference/conanfile/attributes"):
                dash_type = "Attribute"
                entry_name = key.replace("attribute_", "")
            elif inv_entry[2].startswith("reference/conanfile/other"):
                if key.startswith("attribute"):
                    dash_type = "Attribute"
                    entry_name = key.replace("attribute_", "")
                elif key.startswith("method"):
                    dash_type = "Method"
                    entry_name = key.replace("method_", "")
                else:
                    return None
            elif inv_entry[2].startswith("reference/reference/env_vars"):
                dash_type = "Environment"
            else:
                return None
            path_str = inv_entry_to_path(inv_entry)
            return ParserEntry(name=entry_name, type=dash_type, path=path_str)
        return super(InterSphinxWithUserGuide, self).create_entry(
            dash_type, key, inv_entry)


doc2dash.parsers.DOCTYPES = [InterSphinxWithUserGuide]

try:
    # pylint: disable=E1120
    doc2dash.__main__.main([
        "-f", "-nConan", "-i_static/conan.png", "-d{}/dash".format(BUILD_DIR),
        "-Iindex.html", "{}/html".format(BUILD_DIR)
    ])
except SystemExit as e:
    if e.code != 0:
        raise

CSS_CUSTOMIZATION = """
div[role=navigation] {display:none}
.wy-nav-content-wrap {margin-left: 0}
footer {display:none}
nav {display:none !important}
"""

print("Patching CSS...")

with open(
        "{}/dash/Conan.docset/Contents/Resources/Documents/_static/css/theme.css".
        format(BUILD_DIR), "a") as f:
    f.write(CSS_CUSTOMIZATION)
