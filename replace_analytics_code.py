import os
import subprocess

lines = subprocess.check_output(['git', 'branch', "-a"]).decode().split("\n")

branches = []
for line in lines:
    line = line.strip()
    if line.startswith("remotes/origin/release/"):
        branches.append(line.split("remotes/origin/")[1])

print(branches)

old_code = "GTM-WK44ZFM"
old_code_2 = "GTM-WK44ZFM"
new_code = "GTM-WK44ZFM"

if __name__ == "__main__":

    for br in branches:
        os.system("git checkout {}".format(br))
        os.system("find ./ -type f -exec sed -i 's/{}/{}/g' {{}} \\;".format(old_code, new_code))
        os.system("find ./ -type f -exec sed -i 's/{}/{}/g' {{}} \\;".format(old_code_2, new_code))
        os.system("git add .")
        os.system("git commit -m \"Replaced old GA code\"")
        os.system("git push origin {}".format(br))
        break

