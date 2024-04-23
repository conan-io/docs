import argparse
import os
import re

from common import run, latest_v1_folder, latest_v2_folder, latest_v2_version, conan_versions

parser = argparse.ArgumentParser()

parser.add_argument('--gh-pages-folder',
                    help='Folder where the GitHub pages files are', required=True)

parser.add_argument('--branch',
                    help='Branch', required=True)

args = parser.parse_args()

branch = args.branch
output_folder = os.path.join(args.gh_pages_folder)
if branch.startswith("release/2"):
    branch_folder = [k for k, v in conan_versions.items() if v == branch][0]

    ignore_files = {"404.html", "search.html"}

    if branch_folder != latest_v2_version:
        latest_v2_tree = set()
        print(f"{output_folder}/{latest_v2_folder}")
        for root, dirs, files in os.walk(f"{output_folder}/{latest_v2_folder}"):
            for file in files:
                if file.endswith(".html"):
                    latest_v2_tree.add(os.path.join(root, file))
        for root, dirs, files in os.walk(f"{output_folder}/{branch_folder}"):
            for file in files:
                if file.endswith(".html") and file not in ignore_files:
                    path = os.path.join(root, file)
                    as_latest_path = path.replace(os.path.join(output_folder, branch_folder),
                                                  os.path.join(output_folder, latest_v2_folder))
                    if as_latest_path in latest_v2_tree:
                        with open(path, 'r') as f:
                            content = f.read()
                        commented_tag = r'<!--@ OUTDATED_VERSION_PLACEHOLDER_BEGIN @(.*)@ OUTDATED_VERSION_PLACEHOLDER_END @-->'
                        match = re.search(commented_tag, content, re.DOTALL)
                        if match:
                            latest_link = path.replace(os.path.join(output_folder, branch_folder), "")
                            print(f"Replacing in file: {path} to point to {latest_link}")
                            new_tag = match.group(1)
                            new_tag = re.sub(r'/@LATEST_DOC_PAGE_URL@', latest_link, new_tag)
                            print(new_tag)
                            content = content.replace(match.group(0), new_tag)
                            with open(path, 'w') as f:
                                f.write(content)
