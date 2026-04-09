import argparse
import json
import os
import shutil

from common import chdir, conan_versions, latest_v2_folder, latest_v1_folder, latest_v2_branch, run

parser = argparse.ArgumentParser()

parser.add_argument("--branch", help="Docs branch to generate docs for", required=True)
parser.add_argument('--sources-folder',
                    help='Folder where the docs branches are cloned', required=True)
parser.add_argument('--with-pdf', default=False, action='store_true')

args = parser.parse_args()

branch = args.branch
with_pdf = args.with_pdf
sources_folder = args.sources_folder
output_folder = "output"

conan_versions[latest_v2_folder] = latest_v2_branch


branch_folder = [k for k, v in conan_versions.items() if v == branch][0]

print(f"branch_folder: {branch_folder}")

def replace_in_file(file_path, old, new):
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        modified_content = content.replace(old, new)

        with open(file_path, 'w') as file:
            file.write(modified_content)
    except IOError as e:
        print(f"Error replacing in file {file_path}: {e}")


def copy_md_mirrors(html_dir, md_dir):
    """Copy generated .md files into the HTML output directory,
    placing them alongside their .html counterparts."""
    for root, dirs, files in os.walk(md_dir):
        for filename in files:
            if not filename.endswith(".md"):
                continue
            md_path = os.path.join(root, filename)
            rel_path = os.path.relpath(md_path, md_dir)
            dest_path = os.path.join(html_dir, rel_path)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(md_path, dest_path)


def generate_llms_full_txt(html_dir, md_dir):
    """Concatenate all generated .md files into a single llms-full.txt
    for bulk ingestion by IDEs, RAG systems, and LLM agents."""
    output_path = os.path.join(html_dir, "llms-full.txt")
    md_files = []
    for root, dirs, files in os.walk(md_dir):
        dirs.sort()
        for filename in sorted(files):
            if filename.endswith(".md"):
                md_files.append(os.path.join(root, filename))

    with open(output_path, "w") as out:
        for md_path in md_files:
            rel_path = os.path.relpath(md_path, md_dir)
            with open(md_path, "r") as f:
                content = f.read()
            out.write(f"--- {rel_path} ---\n\n")
            out.write(content)
            out.write("\n\n")

    print(f"llms-full.txt generated with {len(md_files)} files")


with chdir(f"{sources_folder}"):

    replace_in_file(os.path.join(branch_folder, "conf.py"), "language = None", "language = 'en'")

    with open(os.path.join(branch_folder, 'versions.json'), 'w') as versions_json:
        json.dump(conan_versions, versions_json, indent=4)

    if branch_folder != latest_v1_folder:
        run(f"rm -fr {branch_folder}/_themes/conan")
        run(f"rm -fr {branch_folder}/_templates")
        run(f"cp -a {latest_v1_folder}/_themes/. {branch_folder}/_themes/")
        run(f"cp -a {latest_v1_folder}/_templates/. {branch_folder}/_templates/")

    # clone conan sources for autodoc
    if branch_folder.startswith("2"):
        # the branch in the docs for 2.0 has the same name that the one in Conan
        conan_branch = branch
        conan_repo_url = 'https://github.com/conan-io/conan.git'

        # clone sources
        run(f"rm -rf {branch_folder}/conan_sources")
        run(f"git clone --single-branch -b {conan_branch} --depth 1 {conan_repo_url} {branch_folder}/conan_sources")

        run(f"pip install -e {branch_folder}/conan_sources")

        # for some reason even adding this to autodoc_mock_imports
        # does not work, se we have to install the real dependency
        # TODO: move this to jenkins
        # run('pip3 install colorama')

    # generate html
    run(f"sphinx-build -W -b html -d {branch_folder}/_build/.doctrees {branch_folder}/ {output_folder}/{branch_folder}")

    # generate markdown mirrors for LLM consumption (llms.txt spec)
    if branch_folder.startswith("2"):
        md_output = f"{output_folder}/{branch_folder}_md"
        try:
            run(f"sphinx-build -b markdown -d {branch_folder}/_build/.doctrees {branch_folder}/ {md_output}")
            copy_md_mirrors(html_dir=f"{output_folder}/{branch_folder}", md_dir=md_output)
            generate_llms_full_txt(html_dir=f"{output_folder}/{branch_folder}", md_dir=md_output)
            print(f"Markdown mirrors and llms-full.txt generated for {branch_folder}")
        except Exception as e:
            print(f"Warning: markdown mirror generation failed for {branch_folder}: {e}")

    # generate pdf
    if with_pdf:
        run(f"sphinx-build -W -b latex -d {branch_folder}/_build/.doctrees {branch_folder}/ {branch_folder}/_build/latex")
        run(f"make -C {branch_folder}/_build/latex all-pdf")
        run(f"cp {branch_folder}/_build/latex/conan.pdf {output_folder}/{branch_folder}/conan.pdf")

    if branch_folder.startswith("2"):
        run(f"pip uninstall conan -y")
        