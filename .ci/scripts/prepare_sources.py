import argparse
import json
import os
import subprocess
import shutil
from contextlib import contextmanager


@contextmanager
def chdir(dir_path):
    current = os.getcwd()
    os.makedirs(dir_path, exist_ok=True)
    os.chdir(dir_path)
    try:
        yield
    finally:
        os.chdir(current)


def run(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    out = out.decode("utf-8")
    err = err.decode("utf-8")
    ret = process.returncode

    output = err + out
    print("Running: {}".format(cmd))
    print("----- OUTPUT -------")
    print(output)
    print("----END OUTPUT------")
    if ret != 0:
        raise Exception("Failed cmd: {}\n{}".format(cmd, output))
    return output


def replace(file_path, text, replace):
    with open(file_path, "r") as f:
        content = f.read()
    content2 = content.replace(text, replace)
    assert content != content2
    with open(file_path, "w") as f:
        f.write(content2)


def load(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    return content


parser = argparse.ArgumentParser()

# parser.add_argument("--old", help="old slug like for example /en/latest")
# parser.add_argument("--new", help="new slug we want to redirect to like /1")
# parser.add_argument("path_html",
#                     help="path where the generated html files are")

# args = parser.parse_args()

# old_slug = args.old
# new_slug = args.new
# path_html = Path(args.path_html)

latest_v2_folder = "2"
latest_v1_folder = "1"

with open('.ci/scripts/conan_versions.json') as f:
    versions = json.load(f)

print(versions)

# Prepare sources as worktrees
deployment_path = "docs_deployment"

run(f"git clone --bare https://github.com/conan-io/docs.git {deployment_path}/tmp")

with chdir(f"{deployment_path}/tmp"):
    for folder, branch in versions.items():
        if folder != latest_v2_folder:
            run(f"git fetch origin {branch}:{branch}")
            run(f"git worktree add ../{folder} {branch}")

with chdir(f"{deployment_path}"):
    os.mkdir("gh-pages")
