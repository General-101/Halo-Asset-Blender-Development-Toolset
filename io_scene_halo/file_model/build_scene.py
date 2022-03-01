# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Steven Garcia
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
import bmesh

from math import radians
from mathutils import Matrix
from ..global_functions import mesh_processing, global_functions

def generate_jms_skeleton(MODEL, armature, fix_rotations):
    first_frame = MODEL.transforms[0]

    bpy.ops.object.mode_set(mode = 'EDIT')
    for idx, asset_node in enumerate(MODEL.nodes):
        current_bone = armature.data.edit_bones.new(asset_node.name)
        current_bone.tail[2] = mesh_processing.get_bone_distance(MODEL, idx, "JMS")
        parent_idx = asset_node.parent

        if not parent_idx == -1 and not parent_idx == None:
            parent = MODEL.nodes[parent_idx].name
            current_bone.parent = armature.data.edit_bones[parent]

        matrix_translate = Matrix.Translation(first_frame[idx].translation)
        matrix_rotation = first_frame[idx].rotation.to_matrix().to_4x4()

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

def generate_markers_layout_new(context, collection, MODEL, armature, fix_rotations):
    for region in MODEL.regions:
        for permutation in region.permutations:
            for local_marker in permutation.local_markers:
                parent_idx = local_marker.node_index
                object_name_prefix = '#%s' % local_marker.name
                marker_name_override = ""
                if context.scene.objects.get('#%s' % local_marker.name):
                    marker_name_override = local_marker.name

                mesh = bpy.data.meshes.new(object_name_prefix)
                object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
                collection.objects.link(object_mesh)

                object_mesh.marker.name_override = marker_name_override

                bm = bmesh.new()
                bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
                bm.to_mesh(mesh)
                bm.free()

                region_name = region.name
                if region_name == "__unnamed":
                    region_name = "unnamed"

                object_mesh.face_maps.new(name=region_name)

                mesh_processing.select_object(context, object_mesh)
                mesh_processing.select_object(context, armature)
                if not parent_idx == -1:
                    bpy.ops.object.mode_set(mode='EDIT')
                    armature.data.edit_bones.active = armature.data.edit_bones[MODEL.nodes[parent_idx].name]
                    bpy.ops.object.mode_set(mode='OBJECT')
                    bpy.ops.object.parent_set(type='BONE', keep_transform=True)

                else:
                    bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)

                matrix_translate = Matrix.Translation(local_marker.translation)
                matrix_rotation = local_marker.rotation.to_matrix().to_4x4()

                transform_matrix = matrix_translate @ matrix_rotation
                if not parent_idx == -1:
                    pose_bone = armature.pose.bones[MODEL.nodes[parent_idx].name]
                    if fix_rotations:
                        transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix

                    else:
                        transform_matrix = pose_bone.matrix @ transform_matrix

                object_mesh.matrix_world = transform_matrix
                object_mesh.data.ass_jms.Object_Type = 'SPHERE'
                object_mesh.dimensions = (2, 2, 2)
                object_mesh.select_set(False)
                armature.select_set(False)

def build_scene(context, MODEL, fix_rotations, report):
    collection = context.collection
    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors

    armdata = bpy.data.armatures.new('Armature')
    armature = bpy.data.objects.new('Armature', armdata)
    collection.objects.link(armature)

    mesh_processing.select_object(context, armature)

    generate_jms_skeleton(MODEL, armature, fix_rotations)

    mesh_processing.process_mesh_import_data("haloce", MODEL, None, None, random_color_gen, 'TAG', 0, context, collection, armature, fix_rotations)

    generate_markers_layout_new(context, collection, MODEL, armature, fix_rotations)

