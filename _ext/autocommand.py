from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective
import subprocess
import shlex

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
        'language': directives.unchanged,
    }

    def run(self):
        command_str = self.options['command']
        command_list = shlex.split(command_str)

        try:
            output = subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=True)
            command_output = output.stdout
        except subprocess.CalledProcessError as e:
            command_output = f"Error executing: {' '.join(command_list)}\n{e.output}"

        text = f"$ {' '.join(command_list)}\n{command_output}\n"

        highlight_language = self.options.get('language', 'text')

        new_node = nodes.literal_block(text,
                                       text,
                                       language=highlight_language)
        self.state.nested_parse(self.content, self.content_offset, new_node)
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
