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
import bmesh

from math import radians
from mathutils import Matrix, Vector
from ..h1.file_model_collision_geometry.build_mesh import build_collision as build_retail_h1_collision
from ..h2.file_collision_model.build_mesh import build_collision as build_retail_h2_collision
from ...file_tag.tag_interface import tag_interface, tag_common

def build_pathfinding_spheres(context, armature, COLLISION, fix_rotations, empty_markers):
    collision_root = COLLISION["Data"]

    collection = context.collection
    for pathfinding_sphere_idx, pathfinding_sphere in enumerate(collision_root["pathfinding spheres"]):
        parent_idx = pathfinding_sphere["node"]
        object_name = '#pathfinding_sphere_%s' % pathfinding_sphere_idx

        if empty_markers:
            object_mesh = bpy.data.objects.new(object_name, None)
            object_mesh.color = (1, 1, 1, 0)

        else:
            mesh = bpy.data.meshes.new(object_name)
            object_mesh = bpy.data.objects.new(object_name, mesh)
            object_mesh.color = (1, 1, 1, 0)

        collection.objects.link(object_mesh)

        if not empty_markers:
            bm = bmesh.new()
            bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
            bm.to_mesh(mesh)
            bm.free()

        matrix_translate = Matrix.Translation(Vector(pathfinding_sphere["center"]))

        marker_radius = pathfinding_sphere["radius"]

        scale_x = Matrix.Scale(marker_radius, 4, (1, 0, 0))
        scale_y = Matrix.Scale(marker_radius, 4, (0, 1, 0))
        scale_z = Matrix.Scale(marker_radius, 4, (0, 0, 1))
        scale = scale_x @ scale_y @ scale_z

        transform_matrix = matrix_translate @ scale

        if not parent_idx == -1 :
            bone_name = collision_root["nodes"][parent_idx]["name"]

            object_mesh.parent = armature
            object_mesh.parent_type = "BONE"
            object_mesh.parent_bone = bone_name

            pose_bone = armature.pose.bones[bone_name]
            if fix_rotations:
                transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix

            else:
                transform_matrix = pose_bone.matrix @ transform_matrix

        else:
            object_mesh.parent = armature

        object_mesh.matrix_world = transform_matrix
        if not empty_markers:
            object_mesh.data.ass_jms.Object_Type = 'SPHERE'

        object_mesh.ass_jms.marker_mask_type = '1'
        object_mesh.select_set(False)
        armature.select_set(False)

def build_scene(context, tag_ref, asset_cache, game_title, fix_rotations, empty_markers, report):
    if game_title == "halo1":
        tag_groups = tag_common.h1_tag_groups
    elif game_title == "halo2":
        tag_groups = tag_common.h2_tag_groups
    else:
        print("%s is not supported." % game_title)

    collision_data = tag_interface.get_disk_asset(tag_ref["path"], tag_groups.get(tag_ref["group name"]))["Data"]

    active_object = context.view_layer.objects.active
    armature = None
    if active_object and active_object.type == 'ARMATURE':
        armature = active_object

    if not armature == None:
        if game_title == "halo1":
            build_retail_h1_collision(context, armature, collision_data, fix_rotations)
            build_pathfinding_spheres(context, armature, collision_data, fix_rotations, empty_markers)

        elif game_title == "halo2":
            build_retail_h2_collision(context, armature, collision_data, fix_rotations)
            build_pathfinding_spheres(context, armature, collision_data, fix_rotations, empty_markers)

        else:
            report({'ERROR'}, "Game title not supported. Import will now be aborted")

    else:
        report({'ERROR'}, "No valid armature is active. Import will now be aborted")
