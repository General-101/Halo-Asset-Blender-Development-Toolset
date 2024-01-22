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

from math import radians
from mathutils import Matrix
from ..h1.file_model.build_mesh import get_geometry_layout as get_retail_h1_geometry_layout
from ..h2.file_render_model.build_mesh import get_geometry_layout as get_retail_h2_geometry_layout
from ...global_functions import mesh_processing, global_functions

def generate_jms_skeleton(MODEL, game_version, game_title, file_version, armature, fix_rotations):
    first_frame = MODEL.transforms[0]

    bpy.ops.object.mode_set(mode = 'EDIT')
    for idx, asset_node in enumerate(MODEL.nodes):
        current_bone = armature.data.edit_bones.new(asset_node.name)
        current_bone.tail[2] = mesh_processing.get_bone_distance(None, MODEL, idx, "JMS")
        parent_idx = asset_node.parent

        if not parent_idx == -1 and not parent_idx == None:
            parent = MODEL.nodes[parent_idx].name
            current_bone.parent = armature.data.edit_bones[parent]

        if game_title == "halo1":
            matrix_translate = Matrix.Translation(first_frame[idx].translation)
            matrix_rotation = first_frame[idx].rotation.to_matrix().to_4x4()
            transform_matrix = matrix_translate @ matrix_rotation
        elif game_title == "halo2":
            #loc = (first_frame[idx].inverse_position)
            #rot = Matrix((first_frame[idx].inverse_forward,first_frame[idx].inverse_left,first_frame[idx].inverse_up))
            #scale = (first_frame[idx].inverse_scale,first_frame[idx].inverse_scale,first_frame[idx].inverse_scale)
            #transform_matrix = Matrix.LocRotScale(loc, rot, scale).inverted()
            matrix_translate = Matrix.Translation(first_frame[idx].translation)
            matrix_rotation = first_frame[idx].rotation.inverted().to_matrix().to_4x4()
            transform_matrix = matrix_translate @ matrix_rotation

        if fix_rotations:
            if current_bone.parent:
                transform_matrix = (current_bone.parent.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix

            current_bone.matrix = transform_matrix @ Matrix.Rotation(radians(-90.0), 4, 'Z')

        else:
            if current_bone.parent:
                transform_matrix = current_bone.parent.matrix @ transform_matrix

            current_bone.matrix = transform_matrix

    bpy.ops.object.mode_set(mode = 'OBJECT')

def build_scene(context, MODEL, game_version, game_title, file_version, fix_rotations, empty_markers, report):
    collection = context.collection
    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors

    armdata = bpy.data.armatures.new('Armature')
    armature = bpy.data.objects.new('Armature', armdata)
    collection.objects.link(armature)

    mesh_processing.select_object(context, armature)

    generate_jms_skeleton(MODEL, game_version, game_title, file_version, armature, fix_rotations)

    if game_title == "halo1":
        is_triangle_list = False
        get_retail_h1_geometry_layout(context, collection, MODEL, armature, game_version, game_title, file_version, fix_rotations, is_triangle_list, report)
        for region in MODEL.regions:
            for permutation in region.permutations:
                for local_marker in permutation.local_markers:
                    mesh_processing.generate_marker(context, collection, game_version, game_title, file_version, None, MODEL, region.name, "", armature, local_marker, fix_rotations, empty_markers, False)

    else:
        get_retail_h2_geometry_layout(context, collection, MODEL, armature, report)
        for marker_group in MODEL.marker_groups:
            for marker in marker_group.markers:
                mesh_processing.generate_marker(context, collection, game_version, game_title, file_version, None, MODEL, "", marker_group.name, armature, marker, fix_rotations, empty_markers, False)
