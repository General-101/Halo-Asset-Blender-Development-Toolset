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

import shutil
import json
import os
from os import path
from os.path import exists as file_exists
from .format_json import NWOJSON
from .nwo_utils import (
    run_tool,
    write_error_report,
    rename_file,
    dot_partition,
    clean_files,
    print_box,
)

########################################################################################################################################################################################################################
def export_gr2(report, asset_path, asset_name, tag_type, selected_objects, bsp, perm, model_armature, skeleton_bones, animation, regions_dict={}, global_materials_dict={}, filepath="", sidecar_type='', keep_fbx=True, keep_json=True, **kwargs):
    """Exports a gr2 file"""
    new_fbx_name = get_path(asset_name, tag_type, perm, asset_path, bsp, animation)
    print(filepath)
    rename_file(filepath, new_fbx_name)

    if file_exists(new_fbx_name):

        json_path = new_fbx_name.replace('.fbx', '.json')
        build_json(json_path, model_armature, skeleton_bones, selected_objects, asset_name, sidecar_type, regions_dict, global_materials_dict)

        if file_exists(json_path): 
            gr2_path = new_fbx_name.replace('.fbx', '.gr2')
            build_gr2(new_fbx_name, json_path, gr2_path, asset_path)
        else:
            print(f'Failed to export {json_path}. Please check your asset errors folder')
            write_error_report(asset_path, f'Failed to export {json_path} with fbx-to-gr2', new_fbx_name, json_path)

        if file_exists(gr2_path):
            move_assets(new_fbx_name, json_path, gr2_path, asset_path, keep_fbx, keep_json, tag_type)
        else:
            print(f'Failed to export {gr2_path}. Please check your asset errors folder')
            write_error_report(asset_path, f'Failed to export {gr2_path} with fbx-to-gr2', new_fbx_name, json_path)

    else:
        print(f'WARNING: Failed to export {new_fbx_name}')
        write_error_report(asset_path, f'Failed to export FBX file: {new_fbx_name}')

    return {'FINISHED'}

def build_json(json_path, model_armature, skeleton_bones, selected_objects, asset_name, sidecar_type, regions_dict, global_materials_dict):
    """Builds a json file by passing the currently selected objects to the NWOJSON class, and then writing the resulting dictionary to a .json file"""
    json_props = NWOJSON(selected_objects, sidecar_type, model_armature, None, asset_name, skeleton_bones, regions_dict, global_materials_dict)
    with open(json_path, 'w') as j:
        json.dump(json_props.json_dict, j, indent=4)


def build_gr2(filepath, json_path, gr2_path, asset_path):
    """Builds a json file by running a fbx and json file through Tool using fbx-to-gr2"""
    try:           
        run_tool('fbx-to-gr2', filepath, json_path, gr2_path)
    except:
        print(f'Failed to build {gr2_path}. Please check your asset errors folder')
        write_error_report(asset_path, f'Assert when running Tool with fbx-to-gr2 on {filepath}', filepath, json_path)


def get_path(asset_name, tag_type, perm='', asset_path='', bsp='', animation=''):
    """Gets an appropriate new path for the exported fbx file"""
    if bsp == '':
        if tag_type == 'animations':
            name = path.join(asset_path, dot_partition(animation))

        elif tag_type in ('render', 'collision', 'physics', 'markers', 'skeleton'):
            if perm == 'default' or tag_type in ('markers', 'skeleton'):
                name = f'{path.join(asset_path, asset_name)}_{tag_type}'
            else:
                name = f'{path.join(asset_path, asset_name)}_{perm}_{tag_type}'

        else:
            name = path.join(asset_path, asset_name)

    else:
        if tag_type == 'design':
            if perm == 'default':
                name = f'{path.join(asset_path, asset_name)}_design_{bsp}'
            else:
                name = f'{path.join(asset_path, asset_name)}_design_{bsp}_{perm}'
        else:
            if perm == 'default':
                name = f'{path.join(asset_path, asset_name)}_{bsp}'
            else:
                name = f'{path.join(asset_path, asset_name)}_{bsp}_{perm}'

    # return the name with the fbx extension
    return f'{name}.fbx'


def move_assets(file_name, json_path, gr2_path, asset_path, keep_fbx, keep_json, tag_type):
    if tag_type == 'animations':
        if not file_exists(path.join(asset_path, 'animations')) and (keep_fbx or keep_json):
            os.makedirs(path.join(asset_path, 'animations'))
        if not file_exists(path.join(asset_path, 'export', 'animations')):
            os.makedirs(path.join(asset_path, 'export', 'animations'))
        if keep_fbx:
            shutil.copy(file_name, path.join(asset_path, 'animations'))
        if keep_json:
            shutil.copy(json_path, path.join(asset_path, 'animations'))
        shutil.copy(gr2_path, path.join(asset_path, 'export', 'animations'))
    else: 
        if not file_exists(path.join(asset_path, 'models')) and (keep_fbx or keep_json):
            os.makedirs(path.join(asset_path, 'models'))
        if not file_exists(path.join(asset_path, 'export', 'models')):
            os.makedirs(path.join(asset_path, 'export', 'models'))
        if keep_fbx:
            shutil.copy(file_name, path.join(asset_path, 'models'))
        if keep_json:
            shutil.copy(json_path, path.join(asset_path, 'models'))
        shutil.copy(gr2_path, path.join(asset_path, 'export', 'models'))

    clean_files(file_name, json_path, gr2_path)

