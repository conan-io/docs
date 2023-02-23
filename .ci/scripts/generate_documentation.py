import argparse
import json
import os
from pathlib import Path
from common import run, chdir, conan_versions, latest_v2_folder, latest_v1_folder, latest_v2_branch

parser = argparse.ArgumentParser()

parser.add_argument("--branch", help="Docs branch to generate docs for", required=True)
parser.add_argument('--sources-folder', help='Folder where the docs branches are cloned', required=True)
parser.add_argument('--with-pdf', default=False, action='store_true')

args = parser.parse_args()

branch = args.branch
with_pdf = args.with_pdf
sources_folder = args.sources_folder

conan_versions[latest_v2_folder] = latest_v2_branch

with open(os.path.join(sources_folder, 'versions.json'), 'w') as versions_json:
    json.dump(conan_versions, versions_json, indent=4)

branch_folder = [k for k, v in conan_versions.items() if v == branch][0]

with chdir(f"{sources_folder}"):
    run(f"rm -fr {branch_folder}/_themes/conan")
    run(f"cp -a {latest_v1_folder}/_themes/. {branch_folder}/_themes/")

    # clone conan sources for autodoc
    if branch_folder.startswith("2"):
        # the branch in the docs for 2.0 has the same name that the one in Conan
        conan_branch = branch
        conan_repo_url = 'https://github.com/conan-io/conan.git'

        # clone sources
        run(f"rm -rf {branch_folder}/conan_sources")
        run(f"git clone --single-branch -b {conan_branch} --depth 1 {conan_repo_url} {branch_folder}/conan_sources")

        # for some reason even adding this to autodoc_mock_imports
        # does not work, se we have to install the real dependency
        # TODO: move this to jenkins
        # run('pip3 install colorama')

    # generate html
    run(f"sphinx-build -W -b html -d {branch_folder}/_build/.doctrees {branch_folder}/ gh-pages/{branch_folder}")

    # generate pdf
    if with_pdf:
        run(f"sphinx-build -W -b latex -d {branch_folder}/_build/.doctrees {branch_folder}/ {branch_folder}/_build/latex")
        run(f"make -C {branch_folder}/_build/latex all-pdf")
        run(f"cp {branch_folder}/_build/latex/conan.pdf gh-pages/{branch_folder}/conan.pdf")
