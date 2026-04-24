import os
import sys

from common import run, conan_versions, latest_v2_branch


"""
    Get the branches we have to build the docs for, there are two scenarios:

    1. We changed something in the .ci scripts or change the _themes folder in the master
    branch -> regenerate every branch of the docs.

    2. If we did not touch those folders just regenerate the branch we pushed

    With --latest-v2-only, print just the latest v2 branch (used to decide which
    branches get their PDF regenerated when a global rebuild is triggered).
"""

if "--latest-v2-only" in sys.argv:
    print(latest_v2_branch)
    sys.exit(0)

current_branch = os.getenv("BRANCH_NAME")

current_commit = run("git rev-parse HEAD", capture=True).strip()

previous_commit = run("git rev-parse HEAD^1", capture=True).strip()

diff = run(f"git diff --name-only {previous_commit}..{current_commit}", capture=True)

changed_ci = any([line.startswith(".ci") for line in diff.splitlines()])
changed_theme = any([line.startswith("_themes") for line in diff.splitlines()])

if not changed_ci and not (changed_theme and current_branch == "master"):
    print(current_branch)
else:
    for branch in conan_versions.values():
        print(branch)
