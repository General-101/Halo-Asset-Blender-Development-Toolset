# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2021 Steven Garcia
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

from os import path
from .format import JMAAsset
from .build_scene import build_scene
from ..file_jms.format import JMSAsset
from ..global_functions import mesh_processing, global_functions
from .process_file_retail import process_file_retail
from ..file_jms.process_file_retail import process_file_retail as jms_process_file_retail

def load_file(context, filepath, game_version, fix_parents, fix_rotations, jms_path_a, jms_path_b, report):
    extension = global_functions.get_true_extension(filepath, None, True)
    retail_version_list = (16390,16391,16392,16393,16394,16395)

    JMA = JMAAsset(filepath)
    JMS_A = None
    JMS_B = None

    jms_version_detect = "auto"
    if path.exists(bpy.path.abspath(jms_path_a)):
        default_region = mesh_processing.get_default_region_permutation_name(game_version)
        default_permutation = mesh_processing.get_default_region_permutation_name(game_version)

        retail_JMS_version_list = (8197, 8198, 8199, 8200, 8201, 8202, 8203, 8204, 8205, 8206, 8207, 8208, 8209, 8210, 8211, 8212, 8213)

        JMS_A = JMSAsset(bpy.path.abspath(jms_path_a))
        JMS_A = jms_process_file_retail(JMS_A, game_version, "JMS", retail_JMS_version_list, default_region, default_permutation)

    if path.exists(bpy.path.abspath(jms_path_a)) and path.exists(bpy.path.abspath(jms_path_b)):
        JMS_B = JMSAsset(bpy.path.abspath(jms_path_b))
        JMS_B = jms_process_file_retail(JMS_B, game_version, "JMS", retail_JMS_version_list, default_region, default_permutation)

    first_line = JMA.get_first_line()
    version_check = int(first_line)

    if version_check in retail_version_list:
        process_file_retail(JMA, extension, game_version, retail_version_list, report)
        build_scene(context, JMA, JMS_A, JMS_B, filepath, game_version, fix_parents, fix_rotations, report)

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.import_scene.jma()
