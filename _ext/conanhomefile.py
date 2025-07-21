import os

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective
import subprocess
import shlex

class conanhomefile(nodes.literal_block, nodes.Element):
    pass

def visit_conanhomefile_node(self, node):
    self.visit_literal_block(node)

def depart_conanhomefile_node(self, node):
    self.depart_literal_block(node)

class ConanHomeFileDirective(SphinxDirective):
    has_content = True
    option_spec = {
        'file-path': directives.unchanged_required,
        'language': directives.unchanged,
    }

    def run(self):
        output = subprocess.run(["conan", "config", "home"], stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                text=True, check=True)
        home_folder = output.stdout.strip()

        file_path = os.path.join(home_folder, self.options['file-path'])

        with open(file_path, 'r') as f:
            text = f.read()

        highlight_language = self.options.get('language', 'text')

        new_node = nodes.literal_block(text,
                                       text,
                                       language=highlight_language)
        self.state.nested_parse(self.content, self.content_offset, new_node)
        return [new_node]


def setup(app):
    app.add_node(conanhomefile,
                 html=(visit_conanhomefile_node, depart_conanhomefile_node),
                 latex=(visit_conanhomefile_node, depart_conanhomefile_node),
                 text=(visit_conanhomefile_node, depart_conanhomefile_node))

    app.add_directive('conan-home-file', ConanHomeFileDirective)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
