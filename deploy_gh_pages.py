import json
import os
import shutil
import tempfile

# from _elastic.indexer import ElasticManager


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


excluded_files = (".git", "CNAME", "index.html")


def config_git():
    call('git config --global user.email "lasote@gmail.com"')
    call('git config --global user.name "Luis Martinez de Bartolome"')


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

    call("make html")
    call("make json")

    if validate_links:
        call("make spelling")
        call("make linkcheck")
    call("make latexpdf")
    tmp_dir = tempfile.mkdtemp()

    copytree("_build/html/", tmp_dir)
    shutil.copy2("_build/latex/conan.pdf", tmp_dir)

    tmp_dir_json = tempfile.mkdtemp()
    copytree("_build/json/", tmp_dir_json)

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

    return tmp_dir_json


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
    call('git remote add origin-pages '
         'https://%s@github.com/conan-io/docs.git > /dev/null 2>&1' % os.getenv("GITHUB_API_KEY"))
    call('git push origin-pages gh-pages')


if __name__ == "__main__":
    if should_deploy():

        # Copy the _themes to be able to share them between old versions
        themes_dir = tempfile.mkdtemp()
        copytree("_themes", themes_dir)

        host = os.getenv("ELASTIC_SEARCH_HOST")
        region = os.getenv("ELASTIC_SEARCH_REGION")
        #es = ElasticManager(host, region)
        #es.ping()

        # config_git()
        clean_gh_pages()
        versions_dict = {"master": "1.19",
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

        to_index = {}
        for branch, folder_name in versions_dict.items():
            json_folder = build_and_copy(branch, folder_name, versions_dict, themes_dir,
                                         validate_links=branch == "master")
            to_index[folder_name] = json_folder

        # Index
        print("Indexing...")
        print(to_index)

        #try:
        #    es.remove_index()
        #except:
        #    pass
        #es.create_index()
        #for version, folder in to_index.items():
        #    es.index(version, folder)

        deploy()

    else:
        call("make html")
        call("make json")
        call("make spelling")
        call("make linkcheck")
