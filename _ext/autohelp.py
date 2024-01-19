from docutils import nodes
from docutils.parsers.rst import directives

from sphinx.util.docutils import SphinxDirective
import subprocess


class autohelp(nodes.literal_block, nodes.Element):
    pass


def visit_autohelp_node(self, node):
    self.visit_literal_block(node)


def depart_autohelp_node(self, node):
    self.depart_literal_block(node)


class AutohelpDirective(SphinxDirective):
    has_content = True
    option_spec = {
        'command': directives.unchanged_required,
    }

    def run(self):
        command = f"{self.options['command']} -h"

        output = subprocess.getoutput(command)

        text = f"$ {command}\n{output}\n"

        new_node = nodes.literal_block(command, text,
                                       language='text',
                                       classes=[],
                                       force=False,
                                       highlight_args={})
        return [new_node]


def setup(app):
    app.add_node(autohelp,
                 html=(visit_autohelp_node, depart_autohelp_node),
                 latex=(visit_autohelp_node, depart_autohelp_node),
                 text=(visit_autohelp_node, depart_autohelp_node))

    app.add_directive('autohelp', AutohelpDirective)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
