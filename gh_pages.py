
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


def clean_gh_pages():
    call("git checkout gh-pages")
    call("git pull origin gh-pages")
    if os.path.exists("en"):
        shutil.rmtree("en")


def build_and_copy(branch, folder_name):
    call("git checkout %s" % branch)

    call("make html")
    # call("make linkcheck")
    tmp_dir = tempfile.mkdtemp()
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)

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
    call("git commit -m 'committed version %s'" % folder_name, ignore_error=True)


if __name__ == "__main__":

    clean_gh_pages()

    for branch, folder_name in versions_dict.items():
        build_and_copy(branch, folder_name)

    #call("git push origin gh-pages", ignore_error=True)

    print("PUSH skipped, make sure all is ok and 'git push origin gh-pages'")
