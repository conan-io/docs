import os

from common import run


"""
    get the branches we have to build the docs for, there are two scenarios:

    1. We changed something in the .ci scripts or change the _themes folder in the master
    branch -> regenerate every branch of the docs.

    2. If we did not touch those folders just regenerate the branch we pushed

    returns None if we have to build all branches or the branch name that we have to build
"""
current_branch = os.getenv("BRANCH_NAME")

current_commit = run("git rev-parse HEAD", capture=True).strip()

previous_commit = run("git rev-parse HEAD^1", capture=True).strip()

diff = run(f"git diff --name-only {previous_commit}..{current_commit}", capture=True)

changed_ci = any([line.startswith(".ci") for line in diff.splitlines()])
changed_theme = any([line.startswith("_themes") for line in diff.splitlines()])

if not changed_ci and not (changed_theme and current_branch == "master"):
    print(f"--branches={current_branch}")
