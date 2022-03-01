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

from .format import JMIAsset
from .build_asset import build_asset
from ..global_functions import global_functions

def write_file(context, filepath, report, jmi_version, jmi_version_ce, jmi_version_h2, jmi_version_h3, apply_modifiers, triangulate_faces, folder_type, edge_split, use_edge_angle, use_edge_sharp, split_angle, clean_normalize_weights, scale_enum, scale_float, console, hidden_geo, export_render, export_collision, export_physics, game_version, fix_rotations):
    version = global_functions.get_version(jmi_version, jmi_version_ce, jmi_version_h2, jmi_version_h3, game_version, console)

    filename = global_functions.get_filename(None, None, None, None, None, True, filepath)
    root_directory = global_functions.get_directory(context, None, None, None, folder_type, None, filepath)

    JMS_args = JMIAsset.JMSArgs()
    JMS_args.jmi_version = jmi_version
    JMS_args.jmi_version_ce = jmi_version_ce
    JMS_args.jmi_version_h2 = jmi_version_h2
    JMS_args.jmi_version_h3 = jmi_version_h3
    JMS_args.folder_type = folder_type
    JMS_args.hidden_geo = hidden_geo
    JMS_args.export_render = export_render
    JMS_args.export_collision = export_collision
    JMS_args.export_physics = export_physics
    JMS_args.fix_rotations = fix_rotations
    JMS_args.apply_modifiers = apply_modifiers
    JMS_args.triangulate_faces = triangulate_faces
    JMS_args.edge_split = edge_split
    JMS_args.use_edge_angle = use_edge_angle
    JMS_args.use_edge_sharp = use_edge_sharp
    JMS_args.split_angle = split_angle
    JMS_args.clean_normalize_weights = clean_normalize_weights
    JMS_args.scale_enum = scale_enum
    JMS_args.scale_float = scale_float
    JMS_args.console = console

    build_asset(context, JMS_args, version, game_version, root_directory, filename, report)

    report({'INFO'}, "Export completed successfully")
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.export_scene.jmi()
