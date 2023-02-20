import argparse
import os
from pathlib import Path
import textwrap

parser = argparse.ArgumentParser()

parser.add_argument("--old", help="old slug like for example /en/latest")
parser.add_argument("--new", help="new slug we want to redirect to like /1")
parser.add_argument("path_html",
                    help="path where the generated html files are")

args = parser.parse_args()

old_slug = args.old
new_slug = args.new
path_html = Path(args.path_html)

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