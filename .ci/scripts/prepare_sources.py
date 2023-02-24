import os
import argparse
from pathlib import Path

from common import chdir, conan_versions, latest_v1_branch, run, branches_to_build

parser = argparse.ArgumentParser()

parser.add_argument('--sources-folder',
                    help='Folder where the docs branches are cloned', required=True)

args = parser.parse_args()

sources_folder = args.sources_folder

branches = branches_to_build()

if branches:
    # we have to clone master always as it has 
    # the templates and styles for the whole docs
    branches.append(latest_v1_branch)
else:
    branches = list(conan_versions.values())

print(f"Prepare docs for: {branches}")

# Prepare sources as worktrees
if not Path(f"{sources_folder}/tmp").is_dir():
    run(f"git clone --bare https://github.com/conan-io/docs.git {sources_folder}/tmp")

with chdir(f"{sources_folder}/tmp"):
    for folder, branch in conan_versions.items():
        if branch in branches and not Path(f"../{folder}").is_dir():
            run(f"git fetch origin {branch}:{branch}")
            run(f"git worktree add ../{folder} {branch}")
