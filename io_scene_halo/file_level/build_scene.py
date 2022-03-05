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
from mathutils import Vector, Matrix, Euler
from .h1.format import ClusterPortalFlags, SurfaceFlags as H1SurfaceFlags
from .h2.format import SurfaceFlags as H2SurfaceFlags
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

    is_h1 = True
    if LEVEL.header.tag_group == "psbs":
        is_h1 = False

    for bsp_idx, bsp in enumerate(LEVEL.collision_bsps):
        collision_name = "level_collision"
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

            is_invalid = False
            if not is_h1 and H2SurfaceFlags.Invalid in H2SurfaceFlags(surface.flags):
                is_invalid = True

            if not is_invalid:
                collision_bm.faces.new(vert_indices)
                

        collision_bm.faces.ensure_lookup_table()
        for surface_idx, surface in enumerate(bsp.surfaces):
            is_invalid = False
            if not is_h1 and H2SurfaceFlags.Invalid in H2SurfaceFlags(surface.flags):
                is_invalid = True

            if game_version == "retail" and not is_invalid:
                ngon_material_index = surface.material
                if not ngon_material_index == -1:
                    mat = LEVEL.collision_materials[ngon_material_index]

                if not ngon_material_index == -1:
                    if LEVEL.header.tag_group == "sbsp":
                        shader = mat.shader_tag_ref
                    else:
                        shader = mat.new_shader

                    material_name = os.path.basename(shader.name)
                    if is_h1:
                        if H1SurfaceFlags.Two_Sided in H1SurfaceFlags(surface.flags):
                            material_name += "%"

                        if H1SurfaceFlags.Invisible in H1SurfaceFlags(surface.flags):
                            material_name += "*"

                        if H1SurfaceFlags.Climbable in H1SurfaceFlags(surface.flags):
                            material_name += "^"

                        if H1SurfaceFlags.Breakable in H1SurfaceFlags(surface.flags):
                            material_name += "-"

                    else:
                        if H2SurfaceFlags.Two_Sided in H2SurfaceFlags(surface.flags):
                            material_name += "%"
                            
                        if H2SurfaceFlags.Invisible in H2SurfaceFlags(surface.flags):
                            material_name += "*"

                        if H2SurfaceFlags.Climbable in H2SurfaceFlags(surface.flags):
                            material_name += "^"

                        if H2SurfaceFlags.Breakable in H2SurfaceFlags(surface.flags):
                            material_name += "-"

                        if H2SurfaceFlags.Conveyor in H2SurfaceFlags(surface.flags):
                            material_name += ">"

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

    if is_h1 and len(LEVEL.lightmaps) > 0:
        surfaces = LEVEL.surfaces
        render_name = "level_render"
        render_bm = bmesh.new()

        render_mesh = bpy.data.meshes.new(render_name)
        render_object = bpy.data.objects.new(render_name, render_mesh)
        collection.objects.link(render_object)
        face_counter = 0
        vert_normal_list = []
        for lightmap_idx, lightmap in enumerate(LEVEL.lightmaps):
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

    if is_h1 and len(LEVEL.cluster_portals) > 0:
        portal_bm = bmesh.new()
        portal_mesh = bpy.data.meshes.new("level_portals")
        portal_object = bpy.data.objects.new("level_portals", portal_mesh)
        collection.objects.link(portal_object)
        for cluster in LEVEL.clusters:
            for portal in cluster.portals:
                vert_indices = []
                cluster_portal = LEVEL.cluster_portals[portal]
                for vertex in cluster_portal.vertices:
                    vert_indices.append(portal_bm.verts.new(vertex.translation))
                
                portal_bm.faces.new(vert_indices)

            portal_bm.verts.ensure_lookup_table()
            portal_bm.faces.ensure_lookup_table()

            for portal_idx, portal in enumerate(cluster.portals):
                cluster_portal = LEVEL.cluster_portals[portal]
                material_list = []

                material_name = "+portal"
                if ClusterPortalFlags.AI_Cant_Hear_Through_This in ClusterPortalFlags(cluster_portal.flags):
                    material_name = "+portal&"

                mat = bpy.data.materials.get(material_name)
                if mat is None:
                    mat = bpy.data.materials.new(name=material_name)

                for slot in portal_object.material_slots:
                    material_list.append(slot.material)

                if not mat in material_list:
                    material_list.append(mat)
                    portal_object.data.materials.append(mat)

                mat.diffuse_color = random_color_gen.next()
                material_index = material_list.index(mat)
                portal_bm.faces[portal_idx].material_index = material_index

        portal_bm.to_mesh(portal_mesh)
        portal_bm.free()

        mesh_processing.select_object(context, portal_object)
        mesh_processing.select_object(context, level_root)
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
        portal_object.select_set(False)
        level_root.select_set(False)

    if is_h1:
        for marker in LEVEL.markers:
            object_name_prefix = '#%s' % marker.name
            marker_name_override = ""
            if context.scene.objects.get('#%s' % marker.name):
                marker_name_override = marker.name

            mesh = bpy.data.meshes.new(object_name_prefix)
            object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
            collection.objects.link(object_mesh)

            object_mesh.marker.name_override = marker_name_override

            bm = bmesh.new()
            bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
            bm.to_mesh(mesh)
            bm.free()

            mesh_processing.select_object(context, object_mesh)
            mesh_processing.select_object(context, level_root)
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)

            matrix_translate = Matrix.Translation(marker.translation)
            matrix_rotation = marker.rotation.to_matrix().to_4x4()

            transform_matrix = matrix_translate @ matrix_rotation
            if fix_rotations:
                transform_matrix = Matrix.Rotation(radians(90.0), 4, 'Z') @ transform_matrix

            object_mesh.matrix_world = transform_matrix
            object_mesh.data.ass_jms.Object_Type = 'SPHERE'
            object_mesh.dimensions = (2, 2, 2)
            object_mesh.select_set(False)
            level_root.select_set(False)

    if is_h1 and False: # MEK does this for some reason but lens flare markers are generated by settings in the shader. Enable if you need them for some reason.
        for lens_flare_marker in LEVEL.lens_flare_markers:
            lens_flare = LEVEL.lens_flares[lens_flare_marker.lens_flare_index]
            lens_flare_name = os.path.basename(lens_flare.name)
            object_name_prefix = '#%s' % lens_flare_name
            marker_name_override = ""
            if context.scene.objects.get('#%s' % lens_flare_name):
                marker_name_override = lens_flare_name

            mesh = bpy.data.meshes.new(object_name_prefix)
            object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
            collection.objects.link(object_mesh)

            object_mesh.marker.name_override = marker_name_override

            bm = bmesh.new()
            bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
            bm.to_mesh(mesh)
            bm.free()

            mesh_processing.select_object(context, object_mesh)
            mesh_processing.select_object(context, level_root)
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)

            matrix_translate = Matrix.Translation(lens_flare_marker.position)
            lens_flare_euler = Euler((lens_flare_marker.direction_i_compenent / 128, lens_flare_marker.direction_j_compenent / 128, lens_flare_marker.direction_k_compenent / 128))
            matrix_rotation = lens_flare_euler.to_matrix().to_4x4()

            transform_matrix = matrix_translate @ matrix_rotation
            if fix_rotations:
                transform_matrix = Matrix.Rotation(radians(90.0), 4, 'Z') @ transform_matrix

            object_mesh.matrix_world = transform_matrix
            object_mesh.data.ass_jms.Object_Type = 'SPHERE'
            object_mesh.dimensions = (2, 2, 2)
            object_mesh.select_set(False)
            level_root.select_set(False)

    if is_h1 and len(LEVEL.fog_planes) > 0:
        fog_planes_bm = bmesh.new()
        fog_planes_mesh = bpy.data.meshes.new("level_fog_planes")
        fog_planes_object = bpy.data.objects.new("level_fog_planes", fog_planes_mesh)
        collection.objects.link(fog_planes_object)
        for fog_plane in LEVEL.fog_planes:
            vert_indices = []
            for vertex in fog_plane.vertices:
                vert_indices.append(fog_planes_bm.verts.new(vertex.translation))
            
            fog_planes_bm.faces.new(vert_indices)

        fog_planes_bm.verts.ensure_lookup_table()
        fog_planes_bm.faces.ensure_lookup_table()

        material_list = []

        material_name = "+unused$"
        mat = bpy.data.materials.get(material_name)
        if mat is None:
            mat = bpy.data.materials.new(name=material_name)

        for slot in fog_planes_object.material_slots:
            material_list.append(slot.material)

        if not mat in material_list:
            material_list.append(mat)
            fog_planes_object.data.materials.append(mat)

        mat.diffuse_color = random_color_gen.next()

        fog_planes_bm.to_mesh(fog_planes_mesh)
        fog_planes_bm.free()

        mesh_processing.select_object(context, fog_planes_object)
        mesh_processing.select_object(context, level_root)
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
        fog_planes_object.select_set(False)
        level_root.select_set(False)
