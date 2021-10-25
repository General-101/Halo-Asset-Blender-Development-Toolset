"""
Helper script to create a zip file that can just be extracted to the blender addon folder

SPDX-License-Identifier: MIT
"""

from zipfile import ZipFile, ZIP_DEFLATED
import io
import os
import subprocess
from pathlib import Path

def build_resources_zip() -> io.BytesIO:
    search_path = os.path.join("io_scene_halo", "resources")
    print(f"Building resources zip (searching in {search_path})!")

    data = io.BytesIO()
    zip: ZipFile = ZipFile(data, mode='w', compression=ZIP_DEFLATED, compresslevel=9)

    for dir, _, files in os.walk(search_path):
        relative_dir = os.path.relpath(dir, search_path)
        print(f"Adding files in {dir} (mapped to {relative_dir} in zip)")
        for file in files:
            fs_path = os.path.join(dir, file)
            zip.write(fs_path, os.path.join(relative_dir, file))

    zip.close()
    zip.printdir()
    data.flush()
    print("Done building resources")
    return data

def build_release_zip():

    resources = build_resources_zip()

    # grab the version from git
    git_version = subprocess.check_output(["git", "describe", "--always"]).strip().decode()
    print(f"git version: {git_version}")

    # grab version from arguments if any
    CI_version = os.getenv('GITHUB_RUN_NUMBER')
    version_minor = 0
    if CI_version is None:
        print("Local build")
        version_string = "v@" + git_version
    else:
        print(f"CI build {CI_version}")
        version_string = f"v{CI_version}@{git_version}"
        version_minor = int(CI_version)
    print(f"version: {version_string}")

    # create the output directory
    Path("output").mkdir(exist_ok=True)

    # create zip name from git hash/version
    zip_name = f"halo-asset-blender-toolset-{version_string}.zip"

    print(f"zip name: {zip_name}")

    def write_file(zip: ZipFile, path_fs, path_zip = None):
        if path_zip is None:
            path_zip = path_fs
        zip.write(path_fs, os.path.join("io_scene_halo", path_zip))

    # Add files to zip
    zip: ZipFile = ZipFile(os.path.join("output", zip_name), mode='w', compression=ZIP_DEFLATED, compresslevel=9)
    write_file(zip, "LICENSE")
    write_file(zip, "README.md")
    for dir, _, files in os.walk("io_scene_halo"):
        if dir.startswith(os.path.join("io_scene_halo", "resources")):
            continue
        for file in files:
            if file.endswith(".pyc") or (dir == 'io_scene_halo' and file == '__init__.py'):
                continue
            fs_path = os.path.join(dir, file)
            zip.write(fs_path)
    init_file = Path('io_scene_halo/__init__.py').read_text()
    # I hate this code but blender requires it
    init_file = init_file.replace("(117, 343, 65521)", f'(2, {version_minor}, 0)')
    init_file = init_file.replace('BUILD_VERSION_STR', version_string)
    zip.writestr('io_scene_halo/__init__.py', init_file)
    zip.writestr('io_scene_halo/resources.zip', resources.getbuffer())
    zip.printdir()
    zip.close()

build_release_zip()
print("done!")
