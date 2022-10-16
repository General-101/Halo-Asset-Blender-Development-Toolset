# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Crisp
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
import os
from subprocess import Popen
from ...gr2_utils import (
    GetEKPath,
    GetToolPath,
    GetTagsPath,
    GetDataPath,
)

def LaunchFoundation():
    os.chdir(GetEKPath())
    os.startfile('Foundation.exe')
    Popen('bin\\tools\\bonobo\\TagWatcher.exe')

    return {'FINISHED'}

def LaunchData():
    os.chdir(GetEKPath())
    os.startfile('data')

    return {'FINISHED'}

def LaunchTags():
    os.chdir(GetEKPath())
    os.startfile('tags')

    return {'FINISHED'}

def LaunchSource(sidecar_path):
    os.chdir(GetEKPath())
    source_folder = sidecar_path.replace(GetEKPath(), '')
    source_folder = source_folder.rpartition('\\')[0]
    source_folder = source_folder.strip('\\')
    os.startfile(source_folder)

    return {'FINISHED'}
