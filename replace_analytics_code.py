import os
import subprocess

lines = subprocess.check_output(['git', 'branch', "-a"]).decode().split("\n")

branches = []
for line in lines:
    line = line.strip()
    if line.startswith("remotes/origin/release/"):
        branches.append(line.split("remotes/origin/")[1])

old_code = "UA-68594724-3"
old_code_2 = "GTM-53TFLK7"
new_code = "GTM-WK44ZFM"

if __name__ == "__main__":

    for br in branches:
        os.system("git checkout {}".format(br))
        command = "find ./ -type f | grep -v .git | xargs sed -i 's/{}/{}/g'\\;".format(old_code, new_code)
        print(command)
        os.system(command)
        os.system("find ./ -type f | grep -v .git | xargs sed -i 's/{}/{}/g'\\;".format(old_code_2, new_code))
        os.system("git add .")
        os.system("git commit -m \"Replaced old GA code\"")
        os.system("git push origin {}".format(br))
