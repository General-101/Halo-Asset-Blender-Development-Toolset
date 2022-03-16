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
from mathutils import Matrix, Vector
from ..global_functions import mesh_processing, global_functions

def build_pathfinding_spheres(context, armature, COLLISION, fix_rotations):
    collection = context.collection
    for pathfinding_sphere_idx, pathfinding_sphere in enumerate(COLLISION.pathfinding_spheres):
        parent_idx = pathfinding_sphere.node
        object_name = '#pathfinding_sphere_%s' % pathfinding_sphere_idx

        mesh = bpy.data.meshes.new(object_name)
        object_mesh = bpy.data.objects.new(object_name, mesh)
        collection.objects.link(object_mesh)

        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
        bm.to_mesh(mesh)
        bm.free()

        matrix_translate = Matrix.Translation(pathfinding_sphere.center)

        marker_radius = pathfinding_sphere.radius

        scale_x = Matrix.Scale(marker_radius, 4, (1, 0, 0))
        scale_y = Matrix.Scale(marker_radius, 4, (0, 1, 0))
        scale_z = Matrix.Scale(marker_radius, 4, (0, 0, 1))
        scale = scale_x @ scale_y @ scale_z

        transform_matrix = matrix_translate @ scale

        mesh_processing.select_object(context, object_mesh)
        mesh_processing.select_object(context, armature)
        if not parent_idx == -1:
            parent_name = COLLISION.nodes[parent_idx].name

            bpy.ops.object.mode_set(mode='EDIT')
            armature.data.edit_bones.active = armature.data.edit_bones[parent_name]
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.parent_set(type='BONE', keep_transform=True)

            pose_bone = armature.pose.bones[parent_name]
            if fix_rotations:
                transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix

            else:
                transform_matrix = pose_bone.matrix @ transform_matrix

        else:
            bpy.ops.object.parent_set(type='ARMATURE', keep_transform=True)

        object_mesh.matrix_world = transform_matrix
        object_mesh.data.ass_jms.Object_Type = 'SPHERE'
        object_mesh.marker.marker_mask_type = '1'
        object_mesh.select_set(False)
        armature.select_set(False)

def build_collision(context, armature, COLLISION):
    collection = context.collection
    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors
    for node_idx, node in enumerate(COLLISION.nodes):
        parent_name = node.name
        for bsp_idx, bsp in enumerate(node.bsps):
            if len(bsp.surfaces) > 0:
                active_region_permutations = []

                region = COLLISION.regions[node.region]
                region_name = region.name
                permutation_name = region.permutations[bsp_idx].name

                if region_name == "__unnamed":
                    region_name = "unnamed"

                if permutation_name == "__base":
                    permutation_name = "base"

                object_name = '@%s %s %s' % (region_name, permutation_name, node.name)
                bm = bmesh.new()

                mesh = bpy.data.meshes.new(object_name)
                object_mesh = bpy.data.objects.new(object_name, mesh)
                collection.objects.link(object_mesh)

                for surface_idx, surface in enumerate(bsp.surfaces):
                    edge_index = surface.first_edge
                    surface_edges = []
                    vert_indices = []
                    while edge_index not in surface_edges:
                        surface_edges.append(edge_index)
                        edge = bsp.edges[edge_index]
                        if edge.left_surface == surface_idx:
                            vert_indices.append(bm.verts.new(bsp.vertices[edge.start_vertex].translation))
                            edge_index = edge.forward_edge

                        else:
                            vert_indices.append(bm.verts.new(bsp.vertices[edge.end_vertex].translation))
                            edge_index = edge.reverse_edge

                    bm.faces.new(vert_indices)

                bm.faces.ensure_lookup_table()
                for surface_idx, surface in enumerate(bsp.surfaces):
                    ngon_material_index = surface.material
                    if not ngon_material_index == -1:
                        mat = COLLISION.materials[ngon_material_index]

                    current_region_permutation = region_name

                    if not current_region_permutation in active_region_permutations:
                        active_region_permutations.append(current_region_permutation)
                        object_mesh.face_maps.new(name=current_region_permutation)

                    if not ngon_material_index == -1:
                        material_list = []

                        material_name = mat.name
                        mat = bpy.data.materials.get(material_name)
                        if mat is None:
                            mat = bpy.data.materials.new(name=material_name)

                        for slot in object_mesh.material_slots:
                            material_list.append(slot.material)

                        if not mat in material_list:
                            material_list.append(mat)
                            object_mesh.data.materials.append(mat)

                        mat.diffuse_color = random_color_gen.next()
                        material_index = material_list.index(mat)
                        bm.faces[surface_idx].material_index = material_index

                    fm = bm.faces.layers.face_map.verify()
                    face_idx = bm.faces[surface_idx]
                    face_idx[fm] = active_region_permutations.index(current_region_permutation)

                bm.to_mesh(mesh)
                bm.free()

                mesh_processing.select_object(context, object_mesh)
                mesh_processing.select_object(context, armature)
                bpy.ops.object.mode_set(mode='EDIT')
                armature.data.edit_bones.active = armature.data.edit_bones[parent_name]
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.parent_set(type='BONE', keep_transform=True)
                object_mesh.matrix_world = armature.pose.bones[parent_name].matrix
                object_mesh.select_set(False)
                armature.select_set(False)

            else:
                active_region_permutations = []

                region = COLLISION.regions[node.region]
                region_name = region.name
                permutation_name = region.permutations[bsp_idx].name

                if region_name == "__unnamed":
                    region_name = "unnamed"

                if permutation_name == "__base":
                    permutation_name = "base"

                object_name = '@%s %s %s' % (region_name, permutation_name, node.name)
                bm = bmesh.new()

                mesh = bpy.data.meshes.new(object_name)
                object_mesh = bpy.data.objects.new(object_name, mesh)
                collection.objects.link(object_mesh)


                vert_indices = [bm.verts.new(Vector((0,0,0))), bm.verts.new(Vector((1,0,1))), bm.verts.new(Vector((1,0,0)))]
                bm.faces.new(vert_indices)
                bm.faces.ensure_lookup_table()

                current_region_permutation = region_name

                if not current_region_permutation in active_region_permutations:
                    active_region_permutations.append(current_region_permutation)
                    object_mesh.face_maps.new(name=current_region_permutation)

                if not ngon_material_index == -1:
                    material_list = []

                    material_name = "+unused"
                    mat = bpy.data.materials.get(material_name)
                    if mat is None:
                        mat = bpy.data.materials.new(name=material_name)

                    for slot in object_mesh.material_slots:
                        material_list.append(slot.material)

                    if not mat in material_list:
                        material_list.append(mat)
                        object_mesh.data.materials.append(mat)

                    mat.diffuse_color = random_color_gen.next()
                    material_index = material_list.index(mat)
                    bm.faces[0].material_index = material_index

                fm = bm.faces.layers.face_map.verify()
                face_idx = bm.faces[0]
                face_idx[fm] = active_region_permutations.index(current_region_permutation)

                bm.to_mesh(mesh)
                bm.free()

                mesh_processing.select_object(context, object_mesh)
                mesh_processing.select_object(context, armature)
                bpy.ops.object.mode_set(mode='EDIT')
                armature.data.edit_bones.active = armature.data.edit_bones[parent_name]
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.parent_set(type='BONE', keep_transform=True)
                object_mesh.matrix_world = armature.pose.bones[parent_name].matrix
                object_mesh.select_set(False)
                armature.select_set(False)

def build_scene(context, COLLISION, fix_rotations, report):
    active_object = context.view_layer.objects.active
    armature = None
    if active_object and active_object.type == 'ARMATURE':
        armature = active_object

    if armature:
        build_collision(context, armature, COLLISION)
        build_pathfinding_spheres(context, armature, COLLISION, fix_rotations)

    else:
        report({'ERROR'}, "No valid armature is active. Import will now be aborted")
