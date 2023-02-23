import argparse
import json
import os
import subprocess
import shutil
from contextlib import contextmanager


def run(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    out = out.decode("utf-8")
    err = err.decode("utf-8")
    ret = process.returncode

    output = err + out
    print("Running: {}".format(cmd))
    print("----- OUTPUT -------")
    print(output)
    print("----END OUTPUT------")
    if ret != 0:
        raise Exception("Failed cmd: {}\n{}".format(cmd, output))
    return output

parser = argparse.ArgumentParser()

parser.add_argument("--version", help="version you want to generate")
parser.add_argument("--sources-folder", help="sources for the different documentation branches")
parser.add_argument('--with-pdf', default=False, action='store_true')

args = parser.parse_args()

version = args.version
with_pdf = args.with_pdf

print(version, with_pdf)