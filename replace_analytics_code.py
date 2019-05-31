import os

branches = ["release/1.10.0", "release/1.10.1",
            "release/1.10.2",
            "release/1.11.0",
            "release/1.11.1",
            "release/1.11.2",
            "release/1.12.0",
            "release/1.12.1",
            "release/1.12.1",
            "release/1.12.3",
            "release/1.13.0",
            "release/1.13.1",
            "release/1.13.2",
            "release/1.13.3",
            "release/1.14.0",
            "release/1.14.1",
            "release/1.14.2",
            "release/1.14.3",
            "release/1.14.4",
            "release/1.14.5",
            "release/1.15.0",
            "release/1.15.5",
            "release/1.3.3",
            "release/1.4.5",
            "release/1.5.2",
            "release/1.6.1",
            "release/1.7.4",
            "release/1.8.5",
            "release/1.9.4"]


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

