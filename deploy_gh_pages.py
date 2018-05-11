import os
import shutil
import tempfile

from conf import versions_dict


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


def build_and_copy(branch, folder_name):
    call("git checkout %s" % branch)
    call("git pull origin %s" % branch)

    call("make html")
    call("make linkcheck")
    tmp_dir = tempfile.mkdtemp()

    copytree("_build/html/", tmp_dir)
    shutil.rmtree("_build")

    # Go to deploy branch, copy new files and commit
    call("git checkout gh-pages")
    if not os.path.exists("en"):
        os.mkdir("en")

    version_folder = "en/%s" % folder_name
    if os.path.exists(version_folder):
        shutil.rmtree(version_folder)

    os.mkdir(version_folder)
    copytree(tmp_dir, version_folder)
    call("git add -A .")
    call("git commit --message 'committed version %s'" % folder_name, ignore_error=True)


def deploy():
    if not os.getenv("GITHUB_API_KEY"):
        print("Deploy skipped, missing GITHUB_API_KEY. Is this a PR?")
        return

    call('git remote add origin-pages '
         'https://%s@github.com/conan-io/docs.git > /dev/null 2>&1' % os.getenv("GITHUB_API_KEY"))
    call('git push origin-pages gh-pages')


if __name__ == "__main__":
    config_git()
    clean_gh_pages()

    for branch, folder_name in versions_dict.items():
        build_and_copy(branch, folder_name)

    deploy()
