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

import os
import bpy
import bmesh

from math import radians
from mathutils import Vector, Matrix
from .h2.format import SurfaceFlags
from ..global_functions import mesh_processing, global_functions

def build_scene(context, LEVEL, fix_rotations, report):
    collection = context.collection

    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors

    level_mesh = bpy.data.meshes.new("frame_root")
    level_root = bpy.data.objects.new("frame_root", level_mesh)
    collection.objects.link(level_root)
    mesh_processing.select_object(context, level_root)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.ops.object.mode_set(mode='OBJECT')

    for bsp_idx, bsp in enumerate(LEVEL.collision_bsps):
        collision_name = "level_collision_%s" % bsp_idx
        collision_bm = bmesh.new()

        collision_mesh = bpy.data.meshes.new(collision_name)
        collision_object = bpy.data.objects.new(collision_name, collision_mesh)
        collection.objects.link(collision_object)
        for surface_idx, surface in enumerate(bsp.surfaces):
            edge_index = surface.first_edge
            surface_edges = []
            vert_indices = []
            while edge_index not in surface_edges:
                surface_edges.append(edge_index)
                edge = bsp.edges[edge_index]
                if edge.left_surface == surface_idx:
                    vert_indices.append(collision_bm.verts.new(bsp.vertices[edge.start_vertex].translation))
                    edge_index = edge.forward_edge

                else:
                    vert_indices.append(collision_bm.verts.new(bsp.vertices[edge.end_vertex].translation))
                    edge_index = edge.reverse_edge

            if not SurfaceFlags.Invalid in SurfaceFlags(surface.flags):
                collision_bm.faces.new(vert_indices)

        collision_bm.faces.ensure_lookup_table()
        for surface_idx, surface in enumerate(bsp.surfaces):
            if not SurfaceFlags.Invalid in SurfaceFlags(surface.flags):
                ngon_material_index = surface.material
                if not ngon_material_index == -1:
                    mat = LEVEL.collision_materials[ngon_material_index]

                if not ngon_material_index == -1:
                    if LEVEL.header.tag_group == "sbsp":
                        shader = mat.shader_tag_ref
                    else:
                        shader = mat.new_shader

                    material_name = os.path.basename(shader.name)

                else:
                    material_name = "+sky"

                material_list = []
                mat = bpy.data.materials.get(material_name)
                if mat is None:
                    mat = bpy.data.materials.new(name=material_name)

                for slot in collision_object.material_slots:
                    material_list.append(slot.material)

                if not mat in material_list:
                    material_list.append(mat)
                    collision_object.data.materials.append(mat)

                mat.diffuse_color = random_color_gen.next()
                material_index = material_list.index(mat)
                collision_bm.faces[surface_idx].material_index = material_index

        collision_bm.to_mesh(collision_mesh)
        collision_bm.free()

        mesh_processing.select_object(context, collision_object)
        mesh_processing.select_object(context, level_root)
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
        collision_object.select_set(False)
        level_root.select_set(False)

    surfaces = LEVEL.surfaces
    for lightmap_idx, lightmap in enumerate(LEVEL.lightmaps):
        face_counter = 0
        vert_normal_list = []
        if len(lightmap.materials) > 0:
            render_name = "level_%s" % lightmap_idx
            render_bm = bmesh.new()

            render_mesh = bpy.data.meshes.new(render_name)
            render_object = bpy.data.objects.new(render_name, render_mesh)
            collection.objects.link(render_object)
            for material in lightmap.materials:
                triangles = []
                start_index = material.surfaces

                for idx in range(material.surface_count):
                    surface_idx = start_index + idx
                    triangles.append([surfaces[surface_idx].v2, surfaces[surface_idx].v1, surfaces[surface_idx].v0])

                for triangle in triangles:
                    vertex_v0 = material.uncompressed_render_vertices[triangle[0]]
                    vertex_v1 = material.uncompressed_render_vertices[triangle[1]]
                    vertex_v2 = material.uncompressed_render_vertices[triangle[2]]
                    vert_normal_list.append(vertex_v0.normal)
                    vert_normal_list.append(vertex_v1.normal)
                    vert_normal_list.append(vertex_v2.normal)
                    p1 = vertex_v0.translation
                    p2 = vertex_v1.translation
                    p3 = vertex_v2.translation
                    v1 = render_bm.verts.new((p1[0], p1[1], p1[2]))
                    v2 = render_bm.verts.new((p2[0], p2[1], p2[2]))
                    v3 = render_bm.verts.new((p3[0], p3[1], p3[2]))
                    render_bm.faces.new((v1, v2, v3))

                render_bm.verts.ensure_lookup_table()
                render_bm.faces.ensure_lookup_table()

                for triangle in triangles:
                    material_list = []
                    if material.shader_tag_ref.name_length > 1:
                        permutation_index = ""
                        if not material.shader_permutation == 0:
                            permutation_index = "%s" % material.shader_permutation

                        material_name = "%s%s" % (os.path.basename(material.shader_tag_ref.name), permutation_index)

                    else:
                        material_name = "unassigned_material"

                    mat = bpy.data.materials.get(material_name)
                    if mat is None:
                        mat = bpy.data.materials.new(name=material_name)

                    for slot in render_object.material_slots:
                        material_list.append(slot.material)

                    if not mat in material_list:
                        material_list.append(mat)
                        render_object.data.materials.append(mat)

                    mat.diffuse_color = random_color_gen.next()
                    material_index = material_list.index(mat)
                    render_bm.faces[face_counter].material_index = material_index

                    vertex_v0 = material.uncompressed_render_vertices[triangle[0]]
                    vertex_v1 = material.uncompressed_render_vertices[triangle[1]]
                    vertex_v2 = material.uncompressed_render_vertices[triangle[2]]

                    vert_list = [vertex_v0, vertex_v1, vertex_v2]
                    for vert_idx, vert in enumerate(vert_list):
                        vertex_index = (3 * face_counter) + vert_idx
                        render_bm.verts[vertex_index].normal = vert.normal

                        uv_name = 'UVMap_0'
                        layer_uv = render_bm.loops.layers.uv.get(uv_name)
                        if layer_uv is None:
                            layer_uv = render_bm.loops.layers.uv.new(uv_name)

                        loop = render_bm.faces[face_counter].loops[vert_idx]
                        loop[layer_uv].uv = (vert.UV[0], 1 - vert.UV[1])

                    face_counter += 1

            render_bm.to_mesh(render_mesh)
            render_bm.free()

            render_object.data.normals_split_custom_set(vert_normal_list)
            render_object.data.use_auto_smooth = True

            mesh_processing.select_object(context, render_object)
            mesh_processing.select_object(context, level_root)
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
            render_object.select_set(False)
            level_root.select_set(False)
