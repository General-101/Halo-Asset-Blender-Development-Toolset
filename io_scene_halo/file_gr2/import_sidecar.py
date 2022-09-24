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

EKPath = bpy.context.preferences.addons['io_scene_halo'].preferences.hrek_path

#clean editing kit path
EKPath = EKPath.replace('"','')
EKPath = EKPath.strip('\\')

#get tool path
toolPath = EKPath + '\\tool_fast.exe'

def import_sidecar(report, fbxPath='', sidecar_path='', import_to_game=False, import_check=False, import_force=False, import_verbose=False, import_draft=False,import_seam_debug=False,import_skip_instances=False,import_decompose_instances=False,import_surpress_errors=False):
    print ('import sidecar tbd')
    if(import_to_game):
        toolCommand = '"{}" import "{}" "{}" "{}"'.format(toolPath, fbxPath, getJSONPath(fbxPath), getGR2Path(fbxPath))
        print('\nRunning Tool command... %r' % toolCommand)
        p = Popen(toolCommand)
        p.wait()
    else:
        return {'FINISHED'}

def getJSONPath(filePath):
    pathList = filePath.split(".")
    jsonPath = ""
    for x in range(len(pathList)-1):
        jsonPath += pathList[x]
    jsonPath += ".json"
    return jsonPath

def getGR2Path(filePath):
    pathList = filePath.split(".")
    gr2Path = ""
    for x in range(len(pathList)-1):
        gr2Path += pathList[x]
        gr2Path += ".gr2"
    return gr2Path

def save(operator, context, report,
        filepath="",
        sidecar_path='',
        import_to_game=False,
        import_check=False,
        import_force=False,
        import_verbose=False,
        import_draft=False,
        import_seam_debug=False,
        import_skip_instances=False,
        import_decompose_instances=False,
        import_surpress_errors=False,
        **kwargs
        ):
        import_sidecar(report, filepath, sidecar_path, import_to_game, import_check, import_force, import_verbose, import_draft,import_seam_debug,import_skip_instances,import_decompose_instances,import_surpress_errors)