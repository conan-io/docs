"""
Sphinx Read the Docs theme.

From https://github.com/ryan-roemer/sphinx-bootstrap-theme.
"""

from os import path
from sys import version_info as python_version

from docutils import nodes
from sphinx import version_info as sphinx_version
from sphinx.locale import _
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util.logging import getLogger


__version__ = '2.0.0'
__version_full__ = __version__

logger = getLogger(__name__)


def get_html_theme_path():
    """Return list of HTML theme paths."""
    cur_dir = path.abspath(path.dirname(path.dirname(__file__)))
    return [cur_dir]


def config_initiated(app, config):
    theme_options = config.html_theme_options or {}
    if theme_options.get('canonical_url'):
        logger.warning(
            _('The canonical_url option is deprecated, use the html_baseurl option from Sphinx instead.')
        )


def extend_html_context(app, pagename, templatename, context, doctree):
     # Add ``sphinx_version_info`` tuple for use in Jinja templates
     context['sphinx_version_info'] = sphinx_version


class CopySectionIdsToTitles(SphinxPostTransform):
    """Mirror each <section id="..."> onto its first inner title node so the
    HTML writer emits <hN id="..."> too. Pagefind builds sub-results from
    headings carrying an id; Sphinx places ids only on the wrapping section."""
    default_priority = 900
    builders = ('html',)

    def run(self, **kwargs):
        for section in self.document.findall(nodes.section):
            section_ids = section.get('ids') or []
            if not section_ids:
                continue
            for child in section.children:
                if isinstance(child, nodes.title):
                    existing = set(child.get('ids') or [])
                    for sid in section_ids:
                        if sid not in existing:
                            child['ids'].append(sid)
                    break


# See http://www.sphinx-doc.org/en/stable/theming.html#distribute-your-theme-as-a-python-package
def setup(app):
    if python_version[0] < 3:
        logger.error("Python 2 is not supported with sphinx_rtd_theme, update to Python 3.")

    app.require_sphinx('5.0')
    if app.config.html4_writer:
        logger.error("'html4_writer' is not supported with sphinx_rtd_theme.")

    # Since Sphinx 6, jquery isn't bundled anymore and we need to ensure that
    # the sphinxcontrib-jquery extension is enabled.
    # See: https://dev.readthedocs.io/en/latest/design/sphinx-jquery.html
    if sphinx_version >= (6, 0, 0):
        # Documentation of Sphinx guarantees that an extension is added and
        # enabled at most once.
        # See: https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.setup_extension
        app.setup_extension("sphinxcontrib.jquery")
        # However, we need to call the extension's callback since setup_extension doesn't do it
        # See: https://github.com/sphinx-contrib/jquery/issues/23
        from sphinxcontrib.jquery import add_js_files as jquery_add_js_files
        jquery_add_js_files(app, app.config)

    # Register the theme that can be referenced without adding a theme path
    app.add_html_theme('sphinx_rtd_theme', path.abspath(path.dirname(__file__)))

    # Add Sphinx message catalog for newer versions of Sphinx
    # See http://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.add_message_catalog
    rtd_locale_path = path.join(path.abspath(path.dirname(__file__)), 'locale')
    app.add_message_catalog('sphinx', rtd_locale_path)
    app.connect('config-inited', config_initiated)

    # sphinx emits the permalink icon for headers, so choose one more in keeping with our theme
    app.config.html_permalinks_icon = "\uf0c1"

    # Extend the default context when rendering the templates.
    app.connect("html-page-context", extend_html_context)

    # Ensure each section's id is also on its heading, so Pagefind can build
    # sub-results with the heading text as title. Harmless for non-Pagefind
    # builds. Requires conan_theme to be in conf.py's extensions list.
    app.add_post_transform(CopySectionIdsToTitles)

    return {'parallel_read_safe': True, 'parallel_write_safe': True}
