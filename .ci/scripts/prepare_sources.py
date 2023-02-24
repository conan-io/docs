import os
import argparse
from pathlib import Path

from common import chdir, conan_versions, latest_v1_branch, run

parser = argparse.ArgumentParser()

parser.add_argument('--sources-folder',
                    help='Folder where the docs branches are cloned', required=True)

parser.add_argument('--branches', action='append',
                    help='List of branches (separated by a space) to generate docs for.\
                          If not specified it will re-generate all branches in docs repo.')

args = parser.parse_args()

sources_folder = args.sources_folder
branches = args.branches

# we have to clone master always as it has the templates and styles for the whole docs
if branches:
    branches.append(latest_v1_branch)
else:
    branches = list(conan_versions.values())

print("Prepare docs for: {branches}")

# Prepare sources as worktrees
if not Path(f"{sources_folder}/tmp").is_dir():
    run(f"git clone --bare https://github.com/conan-io/docs.git {sources_folder}/tmp")

with chdir(f"{sources_folder}/tmp"):
    for folder, branch in conan_versions.items():
        if branch in branches and not Path(f"../{folder}").is_dir():
            run(f"git fetch origin {branch}:{branch}")
            run(f"git worktree add ../{folder} {branch}")
