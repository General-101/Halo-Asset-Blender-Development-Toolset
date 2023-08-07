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

import bpy

from .format import JMIAsset
from .build_asset import build_asset
from ..global_functions import global_functions

def write_file(
    context,
    filepath,
    report,

    jmi_version,
    apply_modifiers,
    triangulate_faces,
    loop_normals,
    folder_type,
    edge_split,
    clean_normalize_weights,
    scale_value,
    hidden_geo,
    nonrender_geo,
    export_render,
    export_collision,
    export_physics,

    write_textures,
    game_version,
    fix_rotations,
    use_maya_sorting,
):

    filename = global_functions.get_filename(None, None, None, None, None, True, filepath)
    root_directory = global_functions.get_directory(context, None, None, None, folder_type, None, filepath)

    JMS_args = JMIAsset.JMSArgs()

    JMS_args.jmi_version = jmi_version
    JMS_args.folder_type = folder_type
    JMS_args.hidden_geo = hidden_geo
    JMS_args.nonrender_geo = nonrender_geo

    JMS_args.export_render = export_render
    JMS_args.export_collision = export_collision
    JMS_args.export_physics = export_physics

    JMS_args.fix_rotations = fix_rotations
    JMS_args.use_maya_sorting = use_maya_sorting
    JMS_args.apply_modifiers = apply_modifiers
    JMS_args.triangulate_faces = triangulate_faces
    JMS_args.loop_normals = loop_normals
    JMS_args.edge_split = edge_split
    JMS_args.clean_normalize_weights = clean_normalize_weights
    JMS_args.scale_value = scale_value

    build_asset(
        context,
        JMS_args,
        jmi_version,
        game_version,
        write_textures,
        root_directory,
        filename,
        report,
    )

    report({'INFO'}, "Export completed successfully")
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.export_scene.jmi()
