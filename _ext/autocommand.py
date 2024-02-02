from docutils import nodes
from docutils.parsers.rst import directives

from sphinx.util.docutils import SphinxDirective
import subprocess


class autocommand(nodes.literal_block, nodes.Element):
    pass


def visit_autocommand_node(self, node):
    self.visit_literal_block(node)


def depart_autocommand_node(self, node):
    self.depart_literal_block(node)


class AutocommandDirective(SphinxDirective):
    has_content = True
    option_spec = {
        'command': directives.unchanged_required,
    }

    def run(self):
        output = subprocess.run(self.options['command'])

        output.check_returncode()

        text = f"$ {self.options['command']}\n{output.stdout}\n"

        new_node = nodes.literal_block(self.options['command'], text,
                                       language='text',
                                       classes=["command-help"],
                                       force=False,
                                       highlight_args={})
        return [new_node]


def setup(app):
    app.add_node(autocommand,
                 html=(visit_autocommand_node, depart_autocommand_node),
                 latex=(visit_autocommand_node, depart_autocommand_node),
                 text=(visit_autocommand_node, depart_autocommand_node))

    app.add_directive('autocommand', AutocommandDirective)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
