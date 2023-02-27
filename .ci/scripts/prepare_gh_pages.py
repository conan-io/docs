
# stage('Prepare gh-branch') {
#     dir(output_contents) {
#         // FIXME: this is to not break all links from https://docs.conan.io/en/latest/
#         // we copy all the /1 folder to /en/latest and then replace all html files
#         // there with redirects to https://docs.conan.io/en/latest/1
#         // remove when most of the traffic in the docs is for 2.X docs
#         sh 'mkdir -p en/latest'
#         sh "cp -R {latest_v1_folder}/* en/latest"
#         sh "python ../1/create_redirects.py en/latest --old=en/latest --new=1"

#         // 2 folder is the same as the latest 2.X, copy the generated html files to 2 folder
#         sh "cp -R {latest_v2_version} {latest_v2_folder}"

#         // sh 'cp src/versions.json versions.json'  // TODO: File is not used, remove from 'gh-pages' branch
#         sh "cp {latest_v2_folder}/404.html 404.html"
#         String content = readFile('404.html')
#         String prefixLatest = "{prefix}/{latest_v2_folder}"
#         content = content.replaceAll('href="_', "href=\"{prefixLatest}/_")
#         content = content.replaceAll('src="_', "src=\"{prefixLatest}/_")
#         content = content.replaceAll('alt="_', "alt=\"{prefixLatest}/_")
#         content = content.replaceAll('internal" href="', "internal\" href=\"{prefixLatest}/")
#         content = content.replaceAll('"search.html"', "\"{prefixLatest}/search.html\"")
#         content = content.replaceAll('"genindex.html"', "\"{prefixLatest}/genindex.html\"")
#         writeFile(file: '404.html', text: content)
#     }
# }

import os
import argparse
from pathlib import Path

from common import chdir, run, latest_v1_folder, latest_v2_folder, latest_v2_version
from create_redirects import create_redirects


parser = argparse.ArgumentParser()

parser.add_argument('--sources-folder',
                    help='Folder where the docs were created', required=True)

parser.add_argument('--gh-pages-folder',
                    help='Folder to clone the gh-pages branch to', required=True)

args = parser.parse_args()

output_folder = os.path.join(args.sources_folder, "output")
pages_folder = args.gh_pages_folder

with chdir(output_folder):
    # FIXME: this is to not break all links from https://docs.conan.io/en/latest/
    # we copy all the /1 folder to /en/latest and then replace all html files
    # there with redirects to https://docs.conan.io/en/latest/1
    # remove when most of the traffic in the docs is for 2.X docs
    run('mkdir -p en/latest')
    run(f"cp -R {latest_v1_folder}/* en/latest")
    create_redirects(path_html="en/latest", old_slug="en/latest", new_slug="1")

    # 2 folder is the same as the latest 2.X, copy the generated html files to 2 folder
    run(f"cp -R {latest_v2_version} {latest_v2_folder}")

#run(f"rm -rf {pages_folder}")

with chdir(pages_folder):
    docs_repo_url = 'https://github.com/conan-io/docs.git'
    run(f"git clone --single-branch -b gh-pages --depth 1 {docs_repo_url}")

# sh "cp {latest_v2_folder}/404.html 404.html"
# String content = readFile('404.html')
# String prefixLatest = "{prefix}/{latest_v2_folder}"
# content = content.replaceAll('href="_', "href=\"{prefixLatest}/_")
# content = content.replaceAll('src="_', "src=\"{prefixLatest}/_")
# content = content.replaceAll('alt="_', "alt=\"{prefixLatest}/_")
# content = content.replaceAll('internal" href="', "internal\" href=\"{prefixLatest}/")
# content = content.replaceAll('"search.html"', "\"{prefixLatest}/search.html\"")
# content = content.replaceAll('"genindex.html"', "\"{prefixLatest}/genindex.html\"")
# writeFile(file: '404.html', text: content)

    # run(f"cp {latest_v2_folder}/404.html 404.html")

    # prefix = "https://docs.conan.io"
    # prefix_latest = f"{prefix}/{latest_v2_folder}"

    # with open('404.html', 'r') as file :
    #     filedata = file.read()
