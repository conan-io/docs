import os
import subprocess
from contextlib import contextmanager


latest_v2_folder = "2"
latest_v1_folder = "1"
latest_v1_branch = "master"

conan_versions = {
    # the first of the dictionary
    # must be always the latest version
    "2.0": "release/2.0",
    latest_v1_folder: latest_v1_branch,
    "en/1.60": "release/1.60.2",
    "en/1.59": "release/1.59.0",
    "en/1.58": "release/1.58.0",
    "en/1.57": "release/1.57.0",
    "en/1.56": "release/1.56.0",
    "en/1.55": "release/1.55.0",
    "en/1.54": "release/1.54.0",
    "en/1.53": "release/1.53.0",
    "en/1.52": "release/1.52.0",
    "en/1.51": "release/1.51.3",
    "en/1.50": "release/1.50.2",
    "en/1.49": "release/1.49.0",
    "en/1.48": "release/1.48.2",
    "en/1.47": "release/1.47.0",
    "en/1.46": "release/1.46.2",
    "en/1.45": "release/1.45.0",
    "en/1.44": "release/1.44.1",
    "en/1.43": "release/1.43.4",
    "en/1.42": "release/1.42.2",
    "en/1.41": "release/1.41.0",
    "en/1.40": "release/1.40.4",
    "en/1.39": "release/1.39.0",
    "en/1.38": "release/1.38.0",
    "en/1.37": "release/1.37.2",
    "en/1.36": "release/1.36.0",
    "en/1.35": "release/1.35.2",
    "en/1.34": "release/1.34.1",
    "en/1.33": "release/1.33.1",
    "en/1.32": "release/1.32.1",
    "en/1.31": "release/1.31.4",
    "en/1.30": "release/1.30.2",
    "en/1.29": "release/1.29.2",
    "en/1.28": "release/1.28.2",
    "en/1.27": "release/1.27.1",
    "en/1.26": "release/1.26.1",
    "en/1.25": "release/1.25.2",
    "en/1.24": "release/1.24.1",
    "en/1.23": "release/1.23.0",
    "en/1.22": "release/1.22.3",
    "en/1.21": "release/1.21.3",
    "en/1.20": "release/1.20.5",
    "en/1.19": "release/1.19.3",
    "en/1.18": "release/1.18.5",
    "en/1.17": "release/1.17.2",
    "en/1.16": "release/1.16.1",
    "en/1.15": "release/1.15.2",
    "en/1.14": "release/1.14.5",
    "en/1.13": "release/1.13.3",
    "en/1.12": "release/1.12.3",
    "en/1.11": "release/1.11.2",
    "en/1.10": "release/1.10.2",
    "en/1.9": "release/1.9.4",
    "en/1.8": "release/1.8.4",
    "en/1.7": "release/1.7.4",
    "en/1.6": "release/1.6.1",
    "en/1.5": "release/1.5.2",
    "en/1.4": "release/1.4.5",
    "en/1.3": "release/1.3.3",
}

latest_v2_branch = list(conan_versions.values())[0]
latest_v2_version = list(conan_versions.keys())[0]


def run(cmd, capture=False):
    stdout = subprocess.PIPE if capture else None
    stderr = subprocess.PIPE if capture else None
    process = subprocess.Popen(
        cmd, stdout=stdout, stderr=stderr, shell=True)
    out, err = process.communicate()
    out = out.decode("utf-8") if capture else ""
    err = err.decode("utf-8") if capture else ""
    ret = process.returncode
    output = err + out
    if ret != 0:
        raise Exception("Failed cmd: {}\n{}".format(cmd, output))
    return output


@contextmanager
def chdir(dir_path):
    current = os.getcwd()
    os.makedirs(dir_path, exist_ok=True)
    os.chdir(dir_path)
    try:
        yield
    finally:
        os.chdir(current)
