import os
import argparse
from pathlib import Path

from common import run, latest_v1_folder, latest_v2_folder, latest_v2_version
from create_redirects import create_redirects


parser = argparse.ArgumentParser()

parser.add_argument('--sources-folder',
                    help='Folder where the docs were created', required=True)

parser.add_argument('--gh-pages-folder',
                    help='Folder to clone the gh-pages branch to', required=True)

args = parser.parse_args()

output_folder = os.path.join(args.sources_folder, "output")
pages_folder = args.gh_pages_folder

docs_repo_url = 'https://github.com/conan-io/docs.git'
run(f"git clone --single-branch -b gh-pages --depth 1 {docs_repo_url} {pages_folder}")

# FIXME: this is to not break all links from https://docs.conan.io/en/latest/
# we copy all the /1 folder to /en/latest and then replace all html files
# there with redirects to https://docs.conan.io/en/latest/1
# remove when most of the traffic in the docs is for 2.X docs

# First check if we generated any docs in `latest_v1_folder`
path_latest_v1 = Path(os.path.join(output_folder, latest_v1_folder))
if path_latest_v1.exists():
    run(f"mkdir -p {output_folder}/en/latest")
    run(f"cp -R {output_folder}/{latest_v1_folder}/* {output_folder}/en/latest")
    create_redirects(path_html=f"{output_folder}/en/latest", new_slug="1")

# 2 folder is the same as the latest 2.X, copy the generated html files to 2 folder
path_latest_v2 = Path(os.path.join(output_folder, latest_v2_version))
if path_latest_v2.exists():
    run(f"cp -R {output_folder}/{latest_v2_version} {output_folder}/{latest_v2_folder}")

    # regenerate 404 file
    run(f"cp {output_folder}/{latest_v2_folder}/404.html {pages_folder}/404.html")

    path_404 = f"{pages_folder}/404.html"

    with open(path_404, 'r') as file_404 :
        contents_404 = file_404.read()

    prefix = 'https://docs.conan.io'
    prefix_latest = f"{prefix}/{latest_v2_folder}"

    contents_404 = contents_404.replace('href="_', f"href=\"{prefix_latest}/_")
    contents_404 = contents_404.replace('src="_', f"src=\"{prefix_latest}/_")
    contents_404 = contents_404.replace('alt="_', f"alt=\"{prefix_latest}/_")
    contents_404 = contents_404.replace('internal" href="', f"internal\" href=\"{prefix_latest}/")
    contents_404 = contents_404.replace('"search.html"', f"\"{prefix_latest}/search.html\"")
    contents_404 = contents_404.replace('"genindex.html"', f"\"{prefix_latest}/genindex.html\"")

    with open(path_404, 'w') as file:
        file.write(contents_404)        

run(f"cp -R {output_folder}/* {pages_folder}")

#run(f"rm -rf {pages_folder}")



# gh-pages prepared to push
