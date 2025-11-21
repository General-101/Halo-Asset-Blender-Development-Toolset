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
import json

from math import radians
from mathutils import Matrix, Vector
from ..h1.file_model.build_mesh import get_geometry_layout as get_retail_h1_geometry_layout
from ..h2.file_render_model.build_mesh import get_geometry_layout as get_retail_h2_geometry_layout
from ...global_functions import mesh_processing, global_functions
from ...file_tag.tag_interface import tag_interface, tag_common

def generate_tag_skeleton(model_data, game_title, armature, fix_rotations):
    bpy.ops.object.mode_set(mode = 'EDIT')
    for node_idx, node in enumerate(model_data["nodes"]):
        bone_name = node["name"]
        if global_functions.string_empty_check(bone_name):
            bone_name = "bone_%s" % node_idx

        current_bone = armature.data.edit_bones.new(bone_name)
        current_bone.tail[2] = mesh_processing.get_bone_distance_from_tags(model_data["nodes"], node_idx, "JMS", 8200)
        parent_idx = node["parent node"]

        if not parent_idx == -1 and not parent_idx == None:
            parent_name = model_data["nodes"][parent_idx]["name"]
            if global_functions.string_empty_check(parent_name):
                parent_name = "bone_%s" % parent_idx

            current_bone.parent = armature.data.edit_bones[parent_name]

        matrix_translate = Matrix.Translation(Vector(node["default translation"]) * 100)
        if game_title == "halo1":
            matrix_rotation = global_functions.convert_quaternion(node["default rotation"]).inverted().to_matrix().to_4x4()
        elif game_title == "halo2":
            matrix_rotation = global_functions.convert_quaternion(node["default rotation"]).to_matrix().to_4x4()

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

def build_scene(context, tag_ref, asset_cache, game_title, fix_rotations, empty_markers, report):
    if game_title == "halo1":
        tag_groups = tag_common.h1_tag_groups
    elif game_title == "halo2":
        tag_groups = tag_common.h2_tag_groups
    else:
        print("%s is not supported." % game_title)

    model_data = tag_interface.get_disk_asset(tag_ref["path"], tag_groups.get(tag_ref["group name"]))["Data"]

    collection = context.collection
    armdata = bpy.data.armatures.new('Armature')
    armature = bpy.data.objects.new('Armature', armdata)
    armature.color = (1, 1, 1, 0)
    collection.objects.link(armature)

    mesh_processing.select_object(context, armature)

    generate_tag_skeleton(model_data, game_title, armature, fix_rotations)

    if game_title == "halo1":
        is_triangle_list = False
        get_retail_h1_geometry_layout(tag_ref, asset_cache, armature, is_triangle_list, report)
        for region in model_data["regions"]:
            for permutation in region["permutations"]:
                for local_marker in permutation["markers"]:
                    mesh_processing.generate_marker(context, collection, game_title, None, model_data, region["name"], "", armature, local_marker, fix_rotations, empty_markers, False)

    else:
        get_retail_h2_geometry_layout(tag_ref, asset_cache, armature, report)
        for marker_group in model_data["marker groups"]:
            for marker in marker_group["markers"]:
                mesh_processing.generate_marker(context, collection, game_title, None, model_data, "", marker_group["name"], armature, marker, fix_rotations, empty_markers, False)
