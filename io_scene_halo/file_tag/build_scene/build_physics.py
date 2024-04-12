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
import bmesh

import numpy as np
from mathutils import Matrix

def build_scene(context, PHYSICS, game_version, game_title, file_version, fix_rotations, empty_markers, report):
    collection = context.collection

    active_object = context.view_layer.objects.active
    armature = None
    if active_object and active_object.type == 'ARMATURE':
        armature = active_object

    if armature:
        for mass_point_idx, mass_point in enumerate(PHYSICS.mass_points):
            if game_title == "halo2" and mass_point.powered_mass_point < 0:
                continue

            parent_idx = mass_point.model_node
            object_name_prefix = '#%s' % mass_point.name

            marker_name_override = ""
            if context.scene.objects.get('#%s' % mass_point.name):
                marker_name_override = mass_point.name

            if empty_markers:
                object_mesh = bpy.data.objects.new(object_name_prefix, None)

            else:
                mesh = bpy.data.meshes.new(object_name_prefix)
                object_mesh = bpy.data.objects.new(object_name_prefix, mesh)

            collection.objects.link(object_mesh)

            object_mesh.ass_jms.name_override = marker_name_override

            if not empty_markers:
                bm = bmesh.new()
                bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
                bm.to_mesh(mesh)
                bm.free()

            node_count = len(armature.data.bones)
            if not parent_idx == -1 and not parent_idx >= node_count:
                bone_name = armature.data.bones[parent_idx].name

                object_mesh.parent = armature
                object_mesh.parent_type = "BONE"
                object_mesh.parent_bone = bone_name

            else:
                object_mesh.parent = armature

            matrix_translate = Matrix.Translation(mass_point.position)
            matrix_rotation = Matrix.Identity(3)

            marker_radius = mass_point.radius

            scale = Matrix.Scale(marker_radius, 4)

            right = np.cross(mass_point.up, mass_point.forward)
            matrix_rotation = Matrix((mass_point.forward, right, mass_point.up))
            matrix_rotation = matrix_rotation.to_4x4().inverted(Matrix.Identity(4))
            transform_matrix = matrix_translate @ matrix_rotation @ scale

            object_mesh.matrix_world = transform_matrix
            if not empty_markers:
                object_mesh.data.ass_jms.Object_Type = 'SPHERE'
            if game_title == "halo2":
                object_mesh.ass_jms.marker_mask_type = '0'
            else:
                object_mesh.ass_jms.marker_mask_type = '2'

    else:
        report({'ERROR'}, "No valid armature is active. Import will now be aborted")
