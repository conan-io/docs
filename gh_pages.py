
import os
import shutil


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


tmp_dir = os.getenv("CONANDOCS_TMP_DIR", "/tmp/docs")
excluded_files = (".git", "CNAME", "index.html")

if __name__ == "__main__":

    call("make html")
    call("make linkcheck")
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)

    copytree("_build/html/", tmp_dir)
    call("git checkout gh-pages")
    for entry in os.listdir("."):
        if entry in excluded_files:
            continue
        if os.path.isdir(entry):
            shutil.rmtree(entry)
        else:
            os.unlink(entry)

    if os.path.exists("en"):
        shutil.rmtree("en")

    os.mkdir("en")
    os.mkdir("en/latest")
    
    copytree(tmp_dir, ".")
    call("git add -A .")
    call("git commit -m 'deploying web'", ignore_error=True)
    call("git push origin gh-pages", ignore_error=True)
    call("git checkout master")
    print("PUSHED!")
