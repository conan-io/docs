import json
import os
import shutil
import tempfile


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def call(command, ignore_error=False):
    ret = os.system(command)
    if ret != 0 and not ignore_error:
        raise Exception("Command failed: %s" % command)


def clean_gh_pages():
    call('git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*" 1>/dev/null')
    call("git fetch origin -q")
    call("git checkout gh-pages")
    if os.path.exists("en"):
        shutil.rmtree("en")


def build_and_copy(branch, folder_name, versions_available, themes_dir, validate_links=False):

    call("git checkout %s" % branch)
    call("git pull origin %s" % branch)

    with open('versions.json', 'w') as f:
        f.write(json.dumps(versions_available))

    shutil.rmtree("_themes")
    copytree(themes_dir, "_themes")

    call("make html > /dev/null")

    if validate_links:
        call("make spelling > /dev/null")
        call("make linkcheck")
    call("make latexpdf > /dev/null")
    tmp_dir = tempfile.mkdtemp()

    copytree("_build/html/", tmp_dir)
    shutil.copy2("_build/latex/conan.pdf", tmp_dir)

    shutil.rmtree("_build")

    # Go to deploy branch, copy new files and commit
    call("git stash")
    call("git stash drop || true")
    call("git clean -d -f")
    call("git checkout gh-pages")
    if not os.path.exists("en"):
        os.mkdir("en")

    version_folders = ["en/%s" % folder_name]
    if branch == "master":
        version_folders.append("en/latest")

    for version_folder in version_folders:
        if os.path.exists(version_folder):
            shutil.rmtree(version_folder)

        os.mkdir(version_folder)
        copytree(tmp_dir, version_folder)
        call("git add -A .")
        call("git commit --message 'committed version %s'" % folder_name, ignore_error=True)


def should_deploy():
    if not os.getenv("TRAVIS_BRANCH", None) == "master":
        print("Skipping deploy for not master branch")
        return False

    if os.getenv("TRAVIS_PULL_REQUEST", "") != "false":
        print("Deploy skipped, This is a PR in the main repository")
        return False

    if not os.getenv("GITHUB_API_KEY"):
        print("Deploy skipped, missing GITHUB_API_KEY. Is this a PR?")
        return False

    return True


def deploy():
    call('rm -rf .git')
    call('git init .')
    call('git add .')
    call('git checkout -b gh-pages')
    call('git commit -m "Cleared web"')
    call('git remote add origin-pages '
         'https://%s@github.com/conan-io/docs.git > /dev/null 2>&1' % os.getenv("GITHUB_API_KEY"))
    call('git push origin-pages gh-pages --force')


if __name__ == "__main__":
    if should_deploy():

        # Copy the _themes to be able to share them between old versions
        themes_dir = tempfile.mkdtemp()
        copytree("_themes", themes_dir)

        clean_gh_pages()
        versions_dict = {"master": "1.26",
                         "release/1.25.2": "1.25",
                         "release/1.24.1": "1.24",
                         "release/1.23.0": "1.23",
                         "release/1.22.3": "1.22",
                         "release/1.21.3": "1.21",
                         "release/1.20.5": "1.20",
                         "release/1.19.3": "1.19",
                         "release/1.18.5": "1.18",
                         "release/1.17.2": "1.17",
                         "release/1.16.1": "1.16",
                         "release/1.15.2": "1.15",
                         "release/1.14.5": "1.14",
                         "release/1.13.3": "1.13",
                         "release/1.12.3": "1.12",
                         "release/1.11.2": "1.11",
                         "release/1.10.2": "1.10",
                         "release/1.9.4": "1.9",
                         "release/1.8.4": "1.8",
                         "release/1.7.4": "1.7",
                         "release/1.6.1": "1.6",
                         "release/1.5.2": "1.5",
                         "release/1.4.5": "1.4",
                         "release/1.3.3": "1.3"}

        for branch, folder_name in versions_dict.items():
            print("Building {}...".format(branch))
            build_and_copy(branch, folder_name, versions_dict, themes_dir)

        deploy()

    else:
        call("make html > /dev/null")
        call("make spelling")
        call("make linkcheck")
