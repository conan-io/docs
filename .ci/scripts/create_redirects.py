import os
from pathlib import Path
import textwrap


def create_redirects(path_html, old_slug, new_slug):
    """
    Redirect every html page found in sources_path from being located under the old_slug
    subfolder to the new location in new_slug. For example if old_slug=en/latest and new_slug=1

    docs.conan.io/en/latest/index.html --> redirects to --> docs.conan.io/1/index.html
    """

    path_html = Path(path_html)

    if not path_html.exists():
        print("The html directory doesn't exist")
        raise SystemExit(1)


    def replace_html_files(sources_path: Path, old_slug: str, new_slug: str):

        redirect_template = textwrap.dedent("""
            <!DOCTYPE HTML>
            <html lang="en-US">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="refresh" content="1; url={destination}">
                </head>
            </html>
        """)

        html_files = sources_path.glob('**/*.html')

        for html_file in html_files:
            origin = Path(old_slug) / Path(html_file).relative_to(
                sources_path).parent
            destination = Path(new_slug) / Path(html_file).relative_to(
                sources_path)
            redirect = Path(os.path.relpath(destination, origin))
            with html_file.open('w') as f:
                f.write(redirect_template.format(destination=redirect))


    replace_html_files(path_html, old_slug, new_slug)
