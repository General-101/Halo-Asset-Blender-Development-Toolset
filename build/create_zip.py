"""
Helper script to create a zip file that can just be extracted to the blender addon folder

SPDX-License-Identifier: MIT
"""

from zipfile import ZipFile, ZIP_DEFLATED
import io
import os
import subprocess
from pathlib import Path

# grab the version from git
git_version = subprocess.check_output(["git", "describe", "--always"]).strip().decode()
print(f"version: {git_version}")

# create the output directory
Path("output").mkdir(exist_ok=True)

# create zip name from git hash/version
zip_name = "halo-asset-blender-toolset-v@" + git_version + ".zip"

print(f"zip name: {zip_name}")

def write_file(zip: ZipFile, path_fs, path_zip = None):
    if path_zip is None:
        path_zip = path_fs
    zip.write(path_fs, os.path.join("io_scene_halo", path_zip))

# Add files to zip
zip: ZipFile = ZipFile(os.path.join("output", zip_name), mode='w', compression=ZIP_DEFLATED, compresslevel=9)
write_file(zip, "LICENSE")
write_file(zip, "README.md")
for dir, subdirs, files in os.walk("io_scene_halo"):
    for file in files:
        fs_path = os.path.join(dir, file)
        zip.write(fs_path)

zip.printdir()
zip.close()
print("done!")
