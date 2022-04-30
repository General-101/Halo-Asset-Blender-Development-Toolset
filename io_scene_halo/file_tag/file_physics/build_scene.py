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
from mathutils import Vector, Matrix

def build_scene(context, PHYSICS, fix_rotations, report, mesh_processing, global_functions):
    collection = context.collection

    active_object = context.view_layer.objects.active
    armature = None
    if active_object and active_object.type == 'ARMATURE':
        armature = active_object

    if armature:
        for mass_point in PHYSICS.mass_points:
            parent_idx = mass_point.model_node
            object_name_prefix = '#%s' % mass_point.name
            marker_name_override = ""
            if context.scene.objects.get('#%s' % mass_point.name):
                marker_name_override = mass_point.name

            mesh = bpy.data.meshes.new(object_name_prefix)
            object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
            collection.objects.link(object_mesh)

            object_mesh.marker.name_override = marker_name_override

            bm = bmesh.new()
            bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
            bm.to_mesh(mesh)
            bm.free()

            mesh_processing.select_object(context, object_mesh)
            mesh_processing.select_object(context, armature)
            if not parent_idx == -1:
                bpy.ops.object.mode_set(mode='EDIT')
                armature.data.edit_bones.active = armature.data.edit_bones[parent_idx]
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.parent_set(type='BONE', keep_transform=True)

            else:
                bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)

            matrix_translate = Matrix.Translation(mass_point.position)
            matrix_rotation = Matrix.Identity(3)

            a = mass_point.up[1] * mass_point.forward[2] - mass_point.forward[1] * mass_point.up[2]
            b = mass_point.up[2] * mass_point.forward[0] - mass_point.forward[2] * mass_point.up[0]
            c = mass_point.up[0] * mass_point.forward[1] - mass_point.forward[0] * mass_point.up[1]

            matrix_rotation[0] = mass_point.forward
            matrix_rotation[1] = mass_point.up
            matrix_rotation[2] = Vector((a, b, c))

            matrix_rotation = matrix_rotation.to_quaternion().inverted().to_matrix().to_4x4()

            marker_radius = 1
            marker_radius = mass_point.radius

            scale_x = Matrix.Scale(marker_radius, 4, (1, 0, 0))
            scale_y = Matrix.Scale(marker_radius, 4, (0, 1, 0))
            scale_z = Matrix.Scale(marker_radius, 4, (0, 0, 1))
            scale = scale_x @ scale_y @ scale_z

            transform_matrix = matrix_translate @ matrix_rotation @ scale

            object_mesh.matrix_world = transform_matrix
            object_mesh.data.ass_jms.Object_Type = 'SPHERE'
            object_mesh.marker.marker_mask_type = '1'
            object_mesh.select_set(False)
            armature.select_set(False)

    else:
        report({'ERROR'}, "No valid armature is active. Import will now be aborted")
