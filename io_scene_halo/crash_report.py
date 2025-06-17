# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2023 Steven Garcia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ##### END MIT LICENSE BLOCK #####


import io
import os
import bpy
import time
import zipfile
import pdb, traceback, sys

URL = "https://github.com/General-101/Halo-Asset-Blender-Development-Toolset/issues/new"
EMAIL = "halo-asset-toolset@protonmail.com"

class CrashReport:
    def __init__(self):
        self.zip_buffer = io.BytesIO()
        self.zfile = zipfile.ZipFile(self.zip_buffer, "w", zipfile.ZIP_DEFLATED)

        self.add_file("readme.txt",
        f"""Crash report for Halo-Asset-Blender-Development-Toolset
Please create an issue at {URL} or email {EMAIL}""")

    def add_file(self, name, contents):
        self.zfile.writestr(name, contents)
    def dump(self):
        """Returns the path the file was dumped to"""
        self.zfile.close()
        crash_dir = os.path.join(os.path.expanduser("~"), "Blender Halo Toolset", "Crash Reports")
        try:
            os.makedirs(crash_dir)
        except OSError:
            pass
        file_name = os.path.join(crash_dir, "%s_crash.zip" % int(time.time()))
        with open(file_name, 'wb') as f:
            f.write(self.zip_buffer.getvalue())
        return file_name

def report_crash():
    info = sys.exc_info()
    traceback.print_exception(info[0], info[1], info[2])
    if bpy.context.preferences.addons["io_scene_halo"].preferences.enable_debugging_pm:
        pdb.post_mortem(info[2])
    if bpy.context.preferences.addons["io_scene_halo"].preferences.enable_crash_report:
        report = CrashReport()
        report.add_file("crash/traceback.txt", traceback.format_exc())
        try:
            for i, (frame, _) in enumerate(traceback.walk_tb(info[2])):
                if i > 2:
                    report.add_file(f"crash/frames/locals_{i}.txt", str(frame.f_locals))
        except:
            pass

        dump_path = report.dump()
        print(f"Dumped crash report to {dump_path}")
