import os
from pathlib import Path
import textwrap


def create_redirects(path_html, new_slug):
    """
    Redirect every html page found in sources_path to the new location in new_slug. For
    example if new_slug=1 and sources are under <folder>/en/latest/...

    docs.conan.io/en/latest/index.html --> redirects to --> docs.conan.io/1/index.html
    """

    path_html = Path(path_html)

    if not path_html.exists():
        print("The html directory doesn't exist")
        raise SystemExit(1)


    def replace_html_files(sources_path: Path, new_slug: str):

        redirect_template = textwrap.dedent("""
            <!DOCTYPE HTML>
            <html lang="en-US">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="refresh" content="1; url={destination}">
                    <link rel="canonical" href="{destination}">
                </head>
            </html>
        """)

        html_files = sources_path.glob('**/*.html')

        for html_file in html_files:
            destination = Path(new_slug) / Path(html_file).relative_to(sources_path)
            print(html_file, destination)
            with open(html_file, 'w') as f:
                f.write(redirect_template.format(destination=f"https://docs.conan.io/{destination}"))

    replace_html_files(path_html, new_slug)
