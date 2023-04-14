# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Generalkidd & Crisp
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

import bpy
from subprocess import Popen
import os

from ..utils.nwo_utils import (
    get_ek_path,
    get_tool_path,
)

def import_bitmap(report, filePath='', bitmap_type=""):
    full_path = filePath.rpartition('\\')[0]
    asset_path = CleanAssetPath(full_path)

    if not bitmap_type == "2dtexture":
        try:
            toolCommand = '"{}" bitmaps-with-type "{}" {}'.format(get_tool_path(), asset_path, bitmap_type)
            os.chdir(get_ek_path())
            p = Popen(toolCommand)
            p.wait()
            report({'INFO'},"Import process complete")

        except:
            report({'WARNING'},"Import Failed!")
    else:
        try:
            toolCommand = '"{}" bitmaps "{}" {}'.format(get_tool_path(), asset_path)
            os.chdir(get_ek_path())
            p = Popen(toolCommand)
            p.wait()
            report({'INFO'},"Import process complete")

        except:
            report({'WARNING'},"Import Failed!")

def CleanAssetPath(path):
    path = path.replace('"','')
    path = path.strip('\\')
    path = path.replace(get_ek_path() + '\\data\\','')

    return path

def save(operator, context, report,
        filepath="",
        bitmap_type="",
        **kwargs
        ):

        import_bitmap(report, filepath, bitmap_type)

        return {'FINISHED'}