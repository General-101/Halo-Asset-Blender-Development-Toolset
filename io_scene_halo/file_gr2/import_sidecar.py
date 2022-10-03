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

from ..gr2_utils import (
    GetEKPath,
    GetToolPath,
)

def import_sidecar(report, filePath='', import_to_game=False, import_check=False, import_force=False, import_verbose=False, import_draft=False,import_seam_debug=False,import_skip_instances=False,import_decompose_instances=False,import_surpress_errors=False, run_tagwatcher=False, import_in_background=False):
    full_path = filePath.rpartition('\\')[0]
    print('full path = ' + filePath)
    asset_path = CleanAssetPath(full_path)
    asset_name = asset_path.rpartition('\\')[2]

    try:

        toolCommand = '"{}" import "{}" {}'.format(GetToolPath(), asset_path + '\\' + asset_name + '.sidecar.xml', GetImportFlags(import_check, import_force, import_verbose, import_draft, import_seam_debug, import_skip_instances, import_decompose_instances, import_surpress_errors))
        print('\nRunning Tool command... %r' % toolCommand)
        os.chdir(GetEKPath())
        p = Popen(toolCommand)
        if not import_in_background:
            p.wait()

    except:
        report({'WARNING'},"Import Failed!")

    if run_tagwatcher:
        tagwatcher = GetEKPath() + '\\bin\\tools\\bonobo\\TagWatcher.exe'
        Popen(tagwatcher)

    report({'INFO'},"Import process complete")

def CleanAssetPath(path):
    path = path.replace('"','')
    path = path.strip('\\')
    path = path.replace(GetEKPath() + '\\data\\','')

    return path

def GetImportFlags(flag_import_check, flag_import_force, flag_import_verbose, flag_import_draft, flag_import_seam_debug, flag_import_skip_instances, flag_import_decompose_instances, flag_import_surpress_errors):
    flags = []
    if flag_import_check:
        flags.append('check')
    if flag_import_force:
        flags.append('force')
    if flag_import_verbose:
        flags.append('verbose')
    if flag_import_draft:
        flags.append('draft')
    if flag_import_seam_debug:
        flags.append('seam_debug')
    if flag_import_skip_instances:
        flags.append('skip_instances')
    if flag_import_decompose_instances:
        flags.append('decompose_instances')
    if flag_import_surpress_errors:
        flags.append('surpress_errors_to_vrml')
    
    return ' '.join(flags)


def save(operator, context, report,
        filepath="",
        import_to_game=False,
        import_check=False,
        import_force=False,
        import_verbose=False,
        import_draft=False,
        import_seam_debug=False,
        import_skip_instances=False,
        import_decompose_instances=False,
        import_surpress_errors=False,
        run_tagwatcher=False,
        import_in_background=False,
        **kwargs
        ):
        if import_to_game:
            import_sidecar(report, filepath, import_to_game, import_check, import_force, import_verbose, import_draft,import_seam_debug,import_skip_instances,import_decompose_instances,import_surpress_errors, run_tagwatcher, import_in_background)

        return {'FINISHED'}