# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2021 Steven Garcia
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
from ..file_tag.file_model.process_file_mod2_retail import ModelFlags
from ..global_functions import global_functions, mesh_processing

class Triangle:
    def __init__(self, material_index=0, normal=Vector(), v0=0, v1=0, v2=0):
        self.material_index = material_index
        self.normal = normal
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2

class Vertex:
    def __init__(self, translation=Vector(), normal=Vector(), UV=(0.0, 0.0), node_index=0):
        self.translation = translation
        self.normal = normal
        self.UV = UV
        self.node_index = node_index

def count_steps(name, start, val):
    real_pos = start
    steps = 0
    while real_pos < len(name) and real_pos > 0 and name[real_pos] != " ":
        real_pos += val
        steps += val

    return steps

def gather_symbols(used_symbols_list, processed_symbol_name, game_version):
    symbol_name = "".join(processed_symbol_name)
    symbol_list = ("%", "#", "!", "*", "$", "^", "-", "&", "@", ".")
    if game_version == "halo2":
        symbol_list = ("%", "#", "?", "!", "@", "*", "$", "^", "-", "&", "=", ".", ";", ")", ">", "<", "|", "~", "(", "{", "}", "[")

    elif game_version == "halo3mcc":
        symbol_list = ("%", "#", "?", "!", "@", "*", "$", "^", "-", "&", "=", ".", ";", ")", ">", "<", "|", "~", "(", "{", "}", "[", "'", "0", "]")

    for idx, char in enumerate(symbol_name): # loop through the characters in the name
        if char in symbol_list: # Check if the character exists in the symbols list
            symbol_name = symbol_name[:idx] + " " + symbol_name[idx + 1:]
            if not char in used_symbols_list: # Check if it's already been appended
                used_symbols_list += char

        else:
            if not char == " ": # If it isn't a whitespace then break cause we've hit the material name
                break

    return (used_symbols_list, symbol_name)

def gather_parameters(name):
    processed_name = name
    processed_parameters = []
    for lm_idx, char in enumerate(name): # loop through the characters in the name
        parameter = ""
        if char == ":":
            value_length = count_steps(name, lm_idx, 1)
            parameter_length = count_steps(name, lm_idx, -1) * -1
            if parameter_length == 3:
                for num in range(parameter_length + value_length):
                    parameter += processed_name[lm_idx - parameter_length + num]
                    index = lm_idx - parameter_length + num
                    processed_name = processed_name[:index] + " " + processed_name[index + 1:]

                processed_parameters.append(parameter)

    return (processed_name, processed_parameters)

def append_material_symbols(material, game_version, is_ass):
    material_name = material.name
    if not global_functions.string_empty_check(material.ass_jms.name_override):
        material_name = material.ass_jms.name_override

    processed_symbol_name = material_name
    if material.ass_jms.is_bm:
        processed_lightmap_properties = gather_parameters(material_name)
        processed_lightmap_name = processed_lightmap_properties[0]
        processed_parameters = processed_lightmap_properties[1]

        symbol_properties = gather_symbols("", processed_lightmap_name, game_version)
        symbol_properties = gather_symbols(symbol_properties[0], reversed(symbol_properties[1]), game_version)
        used_symbol_list = symbol_properties[0]
        processed_symbol_name = "".join(reversed(symbol_properties[1])).strip()
        if game_version == 'haloce':
            if material.ass_jms.two_sided or "%" in used_symbol_list:
                processed_symbol_name += "%"
            if material.ass_jms.transparent_1_sided or "#" in used_symbol_list:
                processed_symbol_name += "#"
            if material.ass_jms.render_only or "!" in used_symbol_list:
                processed_symbol_name += "!"
            if material.ass_jms.sphere_collision_only or "*" in used_symbol_list:
                processed_symbol_name += "*"
            if material.ass_jms.fog_plane or "$" in used_symbol_list:
                processed_symbol_name += "$"
            if material.ass_jms.ladder or "^" in used_symbol_list:
                processed_symbol_name += "^"
            if material.ass_jms.breakable or "-" in used_symbol_list:
                processed_symbol_name += "-"
            if material.ass_jms.ai_deafening or "&" in used_symbol_list:
                processed_symbol_name += "&"
            if material.ass_jms.collision_only or "@" in used_symbol_list:
                processed_symbol_name += "@"
            if material.ass_jms.portal_exact or "." in used_symbol_list:
                processed_symbol_name += "."

        elif game_version == 'halo2':
            if material.ass_jms.two_sided or "%" in used_symbol_list:
                processed_symbol_name += "%"
            if material.ass_jms.transparent_1_sided or "#" in used_symbol_list:
                processed_symbol_name += "#"
            if material.ass_jms.transparent_2_sided or "?" in used_symbol_list:
                processed_symbol_name += "?"
            if material.ass_jms.render_only or "!" in used_symbol_list:
                processed_symbol_name += "!"
            if material.ass_jms.collision_only or "@" in used_symbol_list:
                processed_symbol_name += "@"
            if material.ass_jms.sphere_collision_only or "*" in used_symbol_list:
                processed_symbol_name += "*"
            if material.ass_jms.fog_plane or "$" in used_symbol_list:
                processed_symbol_name += "$"
            if material.ass_jms.ladder or "^" in used_symbol_list:
                processed_symbol_name += "^"
            if material.ass_jms.breakable or "-" in used_symbol_list:
                processed_symbol_name += "-"
            if material.ass_jms.ai_deafening or "&" in used_symbol_list:
                processed_symbol_name += "&"
            if material.ass_jms.no_shadow or "=" in used_symbol_list:
                processed_symbol_name += "="
            if material.ass_jms.shadow_only or "." in used_symbol_list:
                processed_symbol_name += "."
            if material.ass_jms.lightmap_only or ";" in used_symbol_list:
                processed_symbol_name += ";"
            if material.ass_jms.precise or ")" in used_symbol_list:
                processed_symbol_name += ")"
            if material.ass_jms.conveyor or ">" in used_symbol_list:
                processed_symbol_name += ">"
            if material.ass_jms.portal_1_way or "<" in used_symbol_list:
                processed_symbol_name += "<"
            if material.ass_jms.portal_door or "|" in used_symbol_list:
                processed_symbol_name += "|"
            if material.ass_jms.portal_vis_blocker or "~" in used_symbol_list:
                processed_symbol_name += "~"
            if material.ass_jms.dislike_photons or "(" in used_symbol_list:
                processed_symbol_name += "("
            if material.ass_jms.ignored_by_lightmaps or "{" in used_symbol_list:
                processed_symbol_name += "{"
            if material.ass_jms.blocks_sound or "}" in used_symbol_list:
                processed_symbol_name += "}"
            if material.ass_jms.decal_offset or "[" in used_symbol_list:
                processed_symbol_name += "["
            if material.ass_jms.lightmap_resolution_scale > 0.0:
                processed_symbol_name += " lm:%s" % material.ass_jms.lightmap_resolution_scale
            if material.ass_jms.lightmap_power_scale > 0.0:
                processed_symbol_name += " lp:%s" % material.ass_jms.lightmap_power_scale
            if material.ass_jms.lightmap_half_life > 0.0:
                processed_symbol_name += " hl:%s" % material.ass_jms.lightmap_half_life
            if material.ass_jms.lightmap_diffuse_scale > 0.0:
                processed_symbol_name += " ds:%s" % material.ass_jms.lightmap_diffuse_scale

            for parameter in processed_parameters:
                split_parameter = parameter.split(':', 1)
                if split_parameter[0].strip() == "lm" and not "lm" in processed_symbol_name:
                    processed_symbol_name += " lm:%s" % split_parameter[1]

                elif split_parameter[0].strip() == "lp" and not "lp" in processed_symbol_name:
                    processed_symbol_name += " lp:%s" % split_parameter[1]

                elif split_parameter[0].strip() == "hl" and not "hl" in processed_symbol_name:
                    processed_symbol_name += " hl:%s" % split_parameter[1]

                elif split_parameter[0].strip() == "ds" and not "ds" in processed_symbol_name:
                    processed_symbol_name += " ds:%s" % split_parameter[1]

        elif game_version == 'halo3mcc':
            if not is_ass:
                if material.ass_jms.two_sided or "%" in used_symbol_list:
                    processed_symbol_name += "%"
                if material.ass_jms.transparent_1_sided or "#" in used_symbol_list:
                    processed_symbol_name += "#"
                if material.ass_jms.transparent_2_sided or "?" in used_symbol_list:
                    processed_symbol_name += "?"
                if material.ass_jms.render_only or "!" in used_symbol_list:
                    processed_symbol_name += "!"
                if material.ass_jms.collision_only or "@" in used_symbol_list:
                    processed_symbol_name += "@"
                if material.ass_jms.sphere_collision_only or "*" in used_symbol_list:
                    processed_symbol_name += "*"
                if material.ass_jms.fog_plane or "$" in used_symbol_list:
                    processed_symbol_name += "$"
                if material.ass_jms.ladder or "^" in used_symbol_list:
                    processed_symbol_name += "^"
                if material.ass_jms.breakable or "-" in used_symbol_list:
                    processed_symbol_name += "-"
                if material.ass_jms.ai_deafening or "&" in used_symbol_list:
                    processed_symbol_name += "&"
                if material.ass_jms.no_shadow or "=" in used_symbol_list:
                    processed_symbol_name += "="
                if material.ass_jms.shadow_only or "." in used_symbol_list:
                    processed_symbol_name += "."
                if material.ass_jms.lightmap_only or ";" in used_symbol_list:
                    processed_symbol_name += ";"
                if material.ass_jms.precise or ")" in used_symbol_list:
                    processed_symbol_name += ")"
                if material.ass_jms.conveyor or ">" in used_symbol_list:
                    processed_symbol_name += ">"
                if material.ass_jms.portal_1_way or "<" in used_symbol_list:
                    processed_symbol_name += "<"
                if material.ass_jms.portal_door or "|" in used_symbol_list:
                    processed_symbol_name += "|"
                if material.ass_jms.portal_vis_blocker or "~" in used_symbol_list:
                    processed_symbol_name += "~"
                if material.ass_jms.dislike_photons or "(" in used_symbol_list:
                    processed_symbol_name += "("
                if material.ass_jms.ignored_by_lightmaps or "{" in used_symbol_list:
                    processed_symbol_name += "{"
                if material.ass_jms.blocks_sound or "}" in used_symbol_list:
                    processed_symbol_name += "}"
                if material.ass_jms.decal_offset or "[" in used_symbol_list:
                    processed_symbol_name += "["

            if material.ass_jms.water_surface or "'" in used_symbol_list:
                processed_symbol_name += "'"
            if material.ass_jms.group_transparents_by_plane or "]" in used_symbol_list:
                processed_symbol_name += "]"

            if not is_ass:
                if not material.ass_jms.lightmap_res == 1.0:
                    processed_symbol_name += " lm:%s" % material.ass_jms.lightmap_res
                if material.ass_jms.power > 0.0:
                    processed_symbol_name += " lp:%s" % material.ass_jms.power
                if material.ass_jms.emissive_focus > 0.0:
                    processed_symbol_name += " hl:%s" % material.ass_jms.emissive_focus
                if not material.ass_jms.quality == 1.0:
                    processed_symbol_name += " ds:%s" % material.ass_jms.quality
                if not material.ass_jms.photon_fidelity == 1:
                    processed_symbol_name += " pf:%s" % material.ass_jms.photon_fidelity
                if not material.ass_jms.two_sided_transparent_tint[0] == 0.0 and not material.ass_jms.two_sided_transparent_tint[1] == 0.0 and not material.ass_jms.two_sided_transparent_tint[2] == 0.0:
                    processed_symbol_name += " lt:%s" % 0.0
                if material.ass_jms.override_lightmap_transparency > 0:
                    processed_symbol_name += " to:%s" % int(material.ass_jms.override_lightmap_transparency)
                if not material.ass_jms.additive_transparency[0] == 0.0 and not material.ass_jms.additive_transparency[1] == 0.0 and not material.ass_jms.additive_transparency[2] == 0.0:
                    processed_symbol_name += " at:%s" % 0.0
                if material.ass_jms.ignore_default_res_scale > 0.0:
                    processed_symbol_name += " ro:%s" % int(material.ass_jms.ignore_default_res_scale)

                for parameter in processed_parameters:
                    split_parameter = parameter.split(':', 1)
                    if split_parameter[0].strip() == "lm" and not "lm" in processed_symbol_name:
                        processed_symbol_name += " lm:%s" % split_parameter[1]

                    elif split_parameter[0].strip() == "lp" and not "lp" in processed_symbol_name:
                        processed_symbol_name += " lp:%s" % split_parameter[1]

                    elif split_parameter[0].strip() == "hl" and not "hl" in processed_symbol_name:
                        processed_symbol_name += " hl:%s" % split_parameter[1]

                    elif split_parameter[0].strip() == "ds" and not "ds" in processed_symbol_name:
                        processed_symbol_name += " ds:%s" % split_parameter[1]

                    elif split_parameter[0].strip() == "pf" and not "pf" in processed_symbol_name:
                        processed_symbol_name += " pf:%s" % split_parameter[1]

                    elif split_parameter[0].strip() == "lt" and not "lt" in processed_symbol_name:
                        processed_symbol_name += " lt:%s" % split_parameter[1]

                    elif split_parameter[0].strip() == "to" and not "to" in processed_symbol_name:
                        processed_symbol_name += " to:%s" % split_parameter[1]

                    elif split_parameter[0].strip() == "at" and not "at" in processed_symbol_name:
                        processed_symbol_name += " at:%s" % split_parameter[1]

                    elif split_parameter[0].strip() == "ro" and not "ro" in processed_symbol_name:
                        processed_symbol_name += " ro:%s" % split_parameter[1]

    return processed_symbol_name

def deselect_objects(context):
    active_obj = context.view_layer.objects.active
    if not active_obj == None:
        if not active_obj.hide_get() and not active_obj.hide_viewport:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')

        context.view_layer.objects.active = None

def select_object(context, obj):
    obj.select_set(True)
    context.view_layer.objects.active = obj

def vertex_group_clean_normalize(context, obj, limit_value):
    if len(obj.vertex_groups) > 0:
        select_object(context, obj)
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.object.vertex_group_clean(group_select_mode='ALL', limit=limit_value)
        bpy.ops.object.vertex_group_limit_total(group_select_mode='ALL', limit=4)
        bpy.ops.object.vertex_group_normalize_all(group_select_mode='ALL')
        bpy.ops.object.mode_set(mode = 'OBJECT')

        context.view_layer.update()

def gather_modifers(obj):
    modifier_list = []
    for modifier in obj.modifiers:
        modifier.show_render = True
        modifier.show_viewport = True
        modifier.show_in_editmode = True
        modifier_list.append(modifier.type)

    return modifier_list

def add_modifier(context, obj, triangulate_faces, edge_split_class, armature):
    modifier_list = gather_modifers(obj)
    if triangulate_faces:
        if not 'TRIANGULATE' in modifier_list:
            triangulate = obj.modifiers.new("Triangulate", type='TRIANGULATE')
            triangulate.keep_custom_normals = True

    if edge_split_class and edge_split_class.is_enabled:
        if not 'EDGE_SPLIT' in modifier_list:
            edge_split = obj.modifiers.new("EdgeSplit", type='EDGE_SPLIT')
            edge_split.use_edge_angle = edge_split_class.use_edge_angle
            edge_split.split_angle = edge_split_class.split_angle
            edge_split.use_edge_sharp = edge_split_class.use_edge_sharp

        else:
            modifier_idx = modifier_list.index('EDGE_SPLIT')
            obj.modifiers[modifier_idx].use_edge_angle = edge_split_class.use_edge_angle
            obj.modifiers[modifier_idx].split_angle = edge_split_class.split_angle
            obj.modifiers[modifier_idx].use_edge_sharp = edge_split_class.use_edge_sharp

    if armature:
        if not 'ARMATURE' in modifier_list:
            armature_modifier = obj.modifiers.new("Armature", type='ARMATURE')
            armature_modifier.object = armature

        else:
            modifier_idx = modifier_list.index('ARMATURE')
            obj.modifiers[modifier_idx].object = armature

    context.view_layer.update()

def get_color_version_check(file_type):
    version = 8211
    if file_type == 'ASS':
        version = 6

    return version

class TriangleStrips:
    def __init__(self, strips):
        self.strips = strips
        self.index = 0
        self.count = len(strips)

    def next(self):
        self.index += 1
        return self.strips[self.index - 1]

    def next_array(self, count):
        start = self.index
        self.index += count
        return self.strips[start:(start+count)]

    def reached_end(self) -> bool:
        return self.index >= self.count

def generate_markers_layout_new(context, collection, marker, parent_name, armature, fix_rotations):
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
    mesh_processing.select_object(context, armature)

    bpy.ops.object.mode_set(mode='EDIT')
    armature.data.edit_bones.active = armature.data.edit_bones[parent_name]
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.parent_set(type='BONE', keep_transform=True)

    matrix_translate = Matrix.Translation(marker.translation)
    matrix_rotation = marker.rotation.to_matrix().to_4x4()

    transform_matrix = matrix_translate @ matrix_rotation
    pose_bone = armature.pose.bones[parent_name]
    if fix_rotations:
        transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix

    else:
        transform_matrix = pose_bone.matrix @ transform_matrix

    object_mesh.matrix_world = transform_matrix
    object_mesh.data.ass_jms.Object_Type = 'SPHERE'
    object_mesh.dimensions = (2, 2, 2)
    object_mesh.select_set(False)
    armature.select_set(False)

def build_mesh_layout_new(import_file, geometry, object_mesh, region_name, is_triangle_list, bm):
    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors

    vert_normal_list = []
    active_region_permutations = []
    vertex_groups = []

    current_region_permutation = region_name

    if not current_region_permutation in active_region_permutations:
        active_region_permutations.append(current_region_permutation)
        object_mesh.face_maps.new(name=current_region_permutation)

    uses_local_nodes = False
    if import_file.header.tag_group == "mod2":
        uses_local_nodes = ModelFlags.Parts_Have_Local_Nodes in ModelFlags(import_file.mod2_body.flags)

    face_counter = 0
    vertex_counter = 0
    shader_count = len(import_file.shaders)
    for part_idx, part in enumerate(geometry.parts):
        triangle_indices = []
        triangles = []

        if is_triangle_list:
            for triangle in part.triangles:
                triangles.append([triangle.v2, triangle.v1, triangle.v0]) # Reversed order to fix facing normals

        else:
            for triangle in part.triangles:
                if not triangle.v0 == -1:
                    triangle_indices.append(triangle.v0)
                if not triangle.v1 == -1:
                    triangle_indices.append(triangle.v1)
                if not triangle.v2 == -1:
                    triangle_indices.append(triangle.v2)

            index_count = len(triangle_indices)
            for idx in range(index_count - 2):
                triangles.append([triangle_indices[idx], triangle_indices[idx + 1], triangle_indices[idx + 2]])

            # Fix face normals on even triangle indices
            for even_triangle_idx in range(0, len(triangles), 2):
                triangles[even_triangle_idx].reverse()

            # clean up any triangles that reference the same vertex multiple times
            for reversed_triangle in reversed(triangles):
                if (reversed_triangle[0] == reversed_triangle[1]) or (reversed_triangle[1] == reversed_triangle[2]) or (reversed_triangle[0] == reversed_triangle[2]):
                    del triangles[triangles.index(reversed_triangle)]

        for triangle in triangles:
            vertex_v0 = part.uncompressed_vertices[triangle[0]]
            vertex_v1 = part.uncompressed_vertices[triangle[1]]
            vertex_v2 = part.uncompressed_vertices[triangle[2]]
            vert_normal_list.append(vertex_v0.normal)
            vert_normal_list.append(vertex_v1.normal)
            vert_normal_list.append(vertex_v2.normal)
            p1 = vertex_v0.translation
            p2 = vertex_v1.translation
            p3 = vertex_v2.translation
            v1 = bm.verts.new((p1[0], p1[1], p1[2]))
            v2 = bm.verts.new((p2[0], p2[1], p2[2]))
            v3 = bm.verts.new((p3[0], p3[1], p3[2]))
            bm.faces.new((v1, v2, v3))

            vert_list = [vertex_v0, vertex_v1, vertex_v2]
            for vert in vert_list:
                node_0_index = vert.node_0_index
                node_1_index = vert.node_1_index
                if uses_local_nodes:
                    if not node_0_index == -1:
                        node_0_index = part.local_nodes[node_0_index]

                    if not node_1_index == -1:
                        node_1_index = part.local_nodes[node_1_index]

                if not node_0_index == -1 and not node_0_index in vertex_groups:
                    vertex_groups.append(node_0_index)
                    object_mesh.vertex_groups.new(name = import_file.nodes[node_0_index].name)

                if not node_1_index == -1 and not node_1_index in vertex_groups:
                    vertex_groups.append(node_1_index)
                    object_mesh.vertex_groups.new(name = import_file.nodes[node_1_index].name)

        bm.verts.ensure_lookup_table()
        bm.faces.ensure_lookup_table()
        vertex_groups_names = object_mesh.vertex_groups.keys()
        for triangle in triangles:
            triangle_material_index = part.shader_index
            if not triangle_material_index == -1 and triangle_material_index < shader_count:
                mat = import_file.shaders[triangle_material_index]

            current_region_permutation = region_name

            if not current_region_permutation in active_region_permutations:
                active_region_permutations.append(current_region_permutation)
                object_mesh.face_maps.new(name=current_region_permutation)

            if not triangle_material_index == -1:
                material_list = []
                if triangle_material_index < shader_count:
                    permutation_index = ""
                    if not mat.permutation_index == 0:
                        permutation_index = "%s" % mat.permutation_index

                    material_name = "%s%s" % (os.path.basename(mat.tag_ref.name), permutation_index)

                else:
                    material_name = "invalid_material_%s" % triangle_material_index

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
                bm.faces[face_counter].material_index = material_index

            fm = bm.faces.layers.face_map.verify()
            face_idx = bm.faces[face_counter]
            face_idx[fm] = active_region_permutations.index(current_region_permutation)

            vertex_v0 = part.uncompressed_vertices[triangle[0]]
            vertex_v1 = part.uncompressed_vertices[triangle[1]]
            vertex_v2 = part.uncompressed_vertices[triangle[2]]

            vert_list = [vertex_v0, vertex_v1, vertex_v2]
            for vert_idx, vert in enumerate(vert_list):
                vertex_index = (3 * face_counter) + vert_idx
                bm.verts[vertex_index].normal = vert.normal

                uv_name = 'UVMap_0'
                layer_uv = bm.loops.layers.uv.get(uv_name)
                if layer_uv is None:
                    layer_uv = bm.loops.layers.uv.new(uv_name)

                loop = bm.faces[face_counter].loops[vert_idx]
                loop[layer_uv].uv = (vert.UV[0], 1 - vert.UV[1])

                layer_deform = bm.verts.layers.deform.verify()

                node_0_index = vert.node_0_index
                node_1_index = vert.node_1_index
                if uses_local_nodes:
                    if not node_0_index == -1:
                        node_0_index = part.local_nodes[node_0_index]

                    if not node_1_index == -1:
                        node_1_index = part.local_nodes[node_1_index]

                node_0_weight = vert.node_0_weight
                node_1_weight = vert.node_1_weight
                if not node_0_index == -1:
                    group_name = import_file.nodes[node_0_index].name
                    group_index = vertex_groups_names.index(group_name)
                    vert_idx = bm.verts[vertex_index]
                    vert_idx[layer_deform][group_index] = node_0_weight

                if not node_1_index == -1:
                    group_name = import_file.nodes[node_1_index].name
                    group_index = vertex_groups_names.index(group_name)
                    vert_idx = bm.verts[vertex_index]
                    vert_idx[layer_deform][group_index] = node_1_weight

            face_counter += 1

    return bm, vert_normal_list

def build_object(context, collection, geometry, armature, LOD, region_name, permutation_name, import_file, fix_rotations):
    if region_name == "__unnamed":
        region_name = "unnamed"

    if permutation_name == "__base":
        permutation_name = "base"

    object_name = '%s %s %s' % (region_name, permutation_name, LOD)

    bm = bmesh.new()

    mesh = bpy.data.meshes.new(object_name)
    object_mesh = bpy.data.objects.new(object_name, mesh)
    collection.objects.link(object_mesh)

    bm, vert_normal_list = build_mesh_layout_new(import_file, geometry, object_mesh, region_name, False, bm)

    bm.to_mesh(mesh)
    bm.free()
    object_mesh.data.normals_split_custom_set(vert_normal_list)
    object_mesh.data.use_auto_smooth = True

    object_mesh.parent = armature
    add_modifier(context, object_mesh, False, None, armature)

    object_mesh.select_set(False)
    armature.select_set(False)

def get_geometry_layout_new(context, collection, import_file, armature, fix_rotations):
    for region in import_file.regions:
        for permutation in region.permutations:
            superlow_geometry_index = permutation.superlow_geometry_block
            low_geometry_index = permutation.low_geometry_block
            medium_geometry_index = permutation.medium_geometry_block
            high_geometry_index = permutation.high_geometry_block
            superhigh_geometry_index = permutation.superhigh_geometry_block

            geometry_count = len(import_file.geometries)
            if not superhigh_geometry_index == -1 and superhigh_geometry_index < geometry_count and not import_file.geometries[superhigh_geometry_index].visited:
                import_file.geometries[superhigh_geometry_index].visited = True
                superhigh_geometry = import_file.geometries[superhigh_geometry_index]
                build_object(context, collection, superhigh_geometry, armature, 'superhigh', region.name, permutation.name, import_file, fix_rotations)

            if not high_geometry_index == -1 and high_geometry_index < geometry_count and not import_file.geometries[high_geometry_index].visited:
                import_file.geometries[high_geometry_index].visited = True
                high_geometry = import_file.geometries[high_geometry_index]
                build_object(context, collection, high_geometry, armature, 'high', region.name, permutation.name, import_file, fix_rotations)

            if not medium_geometry_index == -1 and medium_geometry_index < geometry_count and not import_file.geometries[medium_geometry_index].visited:
                import_file.geometries[medium_geometry_index].visited = True
                medium_geometry = import_file.geometries[medium_geometry_index]
                build_object(context, collection, medium_geometry, armature, 'medium', region.name, permutation.name, import_file, fix_rotations)

            if not low_geometry_index == -1 and low_geometry_index < geometry_count and not import_file.geometries[low_geometry_index].visited:
                import_file.geometries[low_geometry_index].visited = True
                low_geometry = import_file.geometries[low_geometry_index]
                build_object(context, collection, low_geometry, armature, 'low', region.name, permutation.name, import_file, fix_rotations)

            if not superlow_geometry_index == -1 and superlow_geometry_index < geometry_count and not import_file.geometries[superlow_geometry_index].visited:
                import_file.geometries[superlow_geometry_index].visited = True
                superlow_geometry = import_file.geometries[superlow_geometry_index]
                build_object(context, collection, superlow_geometry, armature, 'superlow', region.name, permutation.name, import_file, fix_rotations)

def process_mesh_import_data(game_version, import_file, object_element, object_mesh, random_color_gen, file_type, node_idx, context, collection, armature, fix_rotations):
    if file_type == "TAG":
        get_geometry_layout_new(context, collection, import_file, armature, fix_rotations)

    else:
        vert_normal_list = []
        vertex_groups = []
        active_region_permutations = []
        bm = bmesh.new()
        if file_type == 'JMS':
            object_data = import_file
            object_triangles = object_data.triangles
            object_vertices = object_data.vertices

        elif file_type == 'ASS':
            object_data = object_element
            object_triangles = object_data.triangles
            object_vertices = object_data.vertices

        for idx, triangle in enumerate(object_triangles):
            triangle_material_index = triangle.material_index
            mat = None
            if not triangle_material_index == -1:
                mat = import_file.materials[triangle_material_index]

            if game_version == 'haloce':
                if import_file.version >= 8198:
                    region = triangle.region

                    current_region_permutation = import_file.regions[region].name

                else:
                    region = import_file.vertices[triangle.v0].region
                    current_region_permutation = import_file.regions[region].name

            elif game_version == 'halo2' or game_version == 'halo3':
                current_region_permutation = global_functions.material_definition_helper(triangle_material_index, mat)

            if not current_region_permutation in active_region_permutations:
                active_region_permutations.append(current_region_permutation)
                object_mesh.face_maps.new(name=current_region_permutation)

            p1 = object_vertices[triangle.v0].translation
            p2 = object_vertices[triangle.v1].translation
            p3 = object_vertices[triangle.v2].translation
            v1 = bm.verts.new((p1[0], p1[1], p1[2]))
            v2 = bm.verts.new((p2[0], p2[1], p2[2]))
            v3 = bm.verts.new((p3[0], p3[1], p3[2]))

            bm.faces.new((v1, v2, v3))
            vert_list = [triangle.v0, triangle.v1, triangle.v2]
            for vert in vert_list:
                vert_normals = []
                file_vert = object_vertices[vert]
                for normal in file_vert.normal:
                    vert_normals.append(normal)

                vert_normal_list.append(vert_normals)
                for node_values in file_vert.node_set:
                    node_index = node_values[0]
                    if not node_index == -1 and not node_index in vertex_groups:
                        vertex_groups.append(node_index)
                        object_mesh.vertex_groups.new(name = import_file.nodes[node_index].name)

        bm.verts.ensure_lookup_table()
        bm.faces.ensure_lookup_table()
        if file_type == 'JMS':
            vertex_groups_names = object_mesh.vertex_groups.keys()

        for idx, triangle in enumerate(object_triangles):
            triangle_material_index = triangle.material_index
            if not triangle_material_index == -1:
                mat = import_file.materials[triangle_material_index]

            if game_version == 'haloce':
                if import_file.version >= 8198:
                    region = triangle.region

                    current_region_permutation = import_file.regions[region].name

                else:
                    region = import_file.vertices[triangle.v0].region
                    current_region_permutation = import_file.regions[region].name

            elif game_version == 'halo2' or game_version == 'halo3':
                current_region_permutation = global_functions.material_definition_helper(triangle_material_index, mat)

            if not current_region_permutation in active_region_permutations:
                active_region_permutations.append(current_region_permutation)
                object_mesh.face_maps.new(name=current_region_permutation)

            if not triangle_material_index == -1:
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
                bm.faces[idx].material_index = material_index

            fm = bm.faces.layers.face_map.verify()
            face_idx = bm.faces[idx]
            face_idx[fm] = active_region_permutations.index(current_region_permutation)

            vert_list = [triangle.v0, triangle.v1, triangle.v2]
            for vert_idx, vert in enumerate(vert_list):
                vertex_index = (3 * idx) + vert_idx
                file_vert = object_vertices[vert]
                bm.verts[vertex_index].normal = file_vert.normal
                if not file_vert.color == None and game_version == 'halo3' and import_file.version >= get_color_version_check(file_type):
                    color_r = file_vert.color[0]
                    color_g = file_vert.color[1]
                    color_b = file_vert.color[2]
                    color_a = 1
                    if color_r < -1000 and color_g < -1000 and color_b < -1000:
                        color_r = 0.0
                        color_g = 0.01
                        color_b = 0.0

                    layer_color = bm.loops.layers.color.get("color")
                    if layer_color is None:
                        layer_color = bm.loops.layers.color.new("color")

                    loop = bm.faces[idx].loops[vert_idx]
                    loop[layer_color] = (color_r, color_g, color_b, color_a)

                for uv_idx, uv in enumerate(file_vert.uv_set):
                    uv_name = 'UVMap_%s' % uv_idx
                    layer_uv = bm.loops.layers.uv.get(uv_name)
                    if layer_uv is None:
                        layer_uv = bm.loops.layers.uv.new(uv_name)

                    loop = bm.faces[idx].loops[vert_idx]
                    loop[layer_uv].uv = (uv[0], uv[1])

                for node_values in file_vert.node_set:
                    layer_deform = bm.verts.layers.deform.verify()

                    node_index = node_values[0]
                    node_weight = node_values[1]
                    if not node_index == -1:
                        group_name = import_file.nodes[node_index].name
                        group_index = vertex_groups_names.index(group_name)
                        vert_idx = bm.verts[vertex_index]
                        vert_idx[layer_deform][group_index] = node_weight

        return bm, vert_normal_list

def process_mesh_export_weights(vert, armature, original_geo, vertex_groups, joined_list, file_type):
    node_index_list = []
    if len(vert.groups) != 0 and len(vert.groups) <= len(vertex_groups):
        object_vert_group_list = []
        vertex_vert_group_list = []
        for group_index in range(len(vert.groups)):
            vert_group = vert.groups[group_index].group
            if not vert_group >= len(vertex_groups):
                object_vertex_group = vertex_groups[vert_group]
                if armature:
                    if object_vertex_group in armature.data.bones:
                        vertex_vert_group_list.append(group_index)
                        if armature.data.bones[object_vertex_group] in joined_list:
                            object_vert_group_list.append(vert_group)

                else:
                    if object_vertex_group in bpy.data.objects:
                        vertex_vert_group_list.append(group_index)
                        if bpy.data.objects[object_vertex_group] in joined_list:
                            object_vert_group_list.append(vert_group)

        value = len(object_vert_group_list)
        if value > 4:
            value = 4

        node_influence_count = int(value)
        node_set = []
        if len(object_vert_group_list) != 0:
            for idx, group_index in enumerate(object_vert_group_list):
                vert_index = int(vertex_vert_group_list[idx])
                vert_group = vert.groups[vert_index].group
                object_vertex_group = vertex_groups[vert_group]
                if armature:
                    node_obj = armature.data.bones[object_vertex_group]

                else:
                    node_obj = bpy.data.objects[object_vertex_group]

                node_index = int(joined_list.index(node_obj))
                if not node_index in node_index_list:
                    node_index_list.append(node_index)

                node_weight = float(vert.groups[vert_index].weight)
                node_set.append([node_index, node_weight])

        else:
            node_set = []
            node_influence_count = int(0)
            if file_type == 'JMS':
                parent_index = global_functions.get_parent(armature, original_geo, joined_list, 0)
                node_influence_count = int(1)
                node_index = int(parent_index[0])
                node_weight = float(1.0000000000)
                node_set.append([node_index, node_weight])

    else:
        node_set = []
        node_influence_count = int(0)
        if file_type == 'JMS':
            parent_index = global_functions.get_parent(armature, original_geo, joined_list, 0)
            node_influence_count = int(1)
            node_index = int(parent_index[0])
            node_weight = float(1.0000000000)
            node_set.append([node_index, node_weight])

    return node_influence_count, node_set, node_index_list

def process_mesh_export_color(evaluated_geo, loop_index):
    color = (0.0, 0.0, 0.0)
    if evaluated_geo.vertex_colors:
        color = evaluated_geo.vertex_colors.active.data[loop_index].color
        if color[0] == 0.0 and "{:.2f}".format(color[1]) == "0.01" and color[2] == 0.0:
            color = (-65536.0000000000, -65536.0000000000, -65536.0000000000, 1.0)

    return color

def process_mesh_export_uv(evaluated_geo, file_type, loop_index, version):
    uv_set = []
    for uv_index in range(len(evaluated_geo.uv_layers)):
        evaluated_geo.uv_layers.active = evaluated_geo.uv_layers[uv_index]
        uv = evaluated_geo.uv_layers.active.data[evaluated_geo.loops[loop_index].index].uv
        uv_set.append(uv)

    if file_type == 'JMS':
        if not uv_set and version <= 8204:
            uv_set = [(0.0, 0.0)]

    return uv_set

def process_mesh_export_vert(vert, loop, file_type, original_geo_matrix, custom_scale):
    if file_type == 'JMS':
        translation = vert.co
        negative_matrix = original_geo_matrix.determinant() < 0.0
        if negative_matrix and file_type == 'JMS':
            invert_translation_x = vert.co[0] * -1
            invert_translation_y = vert.co[1] * -1
            invert_translation_z = vert.co[2] * -1
            translation = Vector((invert_translation_x, invert_translation_y, invert_translation_z))

        final_translation = original_geo_matrix @ translation

        if loop:
            final_normal = (original_geo_matrix @ (translation + loop.normal) - final_translation).normalized()

        else:
            final_normal = (original_geo_matrix @ (translation + vert.normal) - final_translation).normalized()

        if negative_matrix and original_geo_matrix.determinant() < 0.0 and file_type == 'JMS':
            invert_normal_x = final_normal[0] * -1
            invert_normal_y = final_normal[1] * -1
            invert_normal_z = final_normal[2] * -1

            final_normal = Vector((invert_normal_x, invert_normal_y, invert_normal_z))

    else:
        final_translation = custom_scale * vert.co
        if loop:
            final_normal = (loop.normal).normalized()

        else:
            final_normal = (vert.normal).normalized()


    return final_translation, final_normal

def process_mesh_export_face_set(default_permutation, default_region, game_version, original_geo, face_map_idx):
    if game_version == 'haloce':
        if not face_map_idx == -1:
            region = original_geo.face_maps[face_map_idx].name
            face_set = (None, None, region)

    else:
        if not face_map_idx == -1:
            face_set = original_geo.face_maps[face_map_idx].name.split()

        lod, permutation, region = global_functions.material_definition_parser(False, face_set, default_region, default_permutation)
        face_set = (lod, permutation, region)

    return face_set

def get_default_region_permutation_name(game_version):
    default_name = None
    if game_version == 'haloce':
        default_name = 'unnamed'

    else:
        default_name = 'Default'

    return default_name

def get_lod(lod_setting, game_version):
    LOD_name = None
    if game_version == 'haloce':
        if lod_setting == '1':
            LOD_name = 'superlow'

        elif lod_setting == '2':
            LOD_name = 'low'

        elif lod_setting == '3':
            LOD_name = 'medium'

        elif lod_setting == '4':
            LOD_name = 'high'

        elif lod_setting == '5':
            LOD_name = 'superhigh'

    else:
        LOD_name = lod_setting

    return LOD_name

def get_child_nodes(import_file_main, parent_idx, file_type):
    file_version = import_file_main.version
    first_frame = import_file_main.transforms[0]
    child_list = []
    for child_idx, node in enumerate(import_file_main.nodes):
        if node.parent == parent_idx:
            child_distance = (Vector((0, 0, 0)) - first_frame[child_idx].translation).length
            if file_version >= global_functions.get_version_matrix_check(file_type):
                child_distance = (first_frame[parent_idx].translation - first_frame[child_idx].translation).length

            child_list.append(child_distance)

    return child_list

def get_bone_distance(import_file_main, current_idx, file_type):
    bone_distance = 0
    file_version = import_file_main.version
    first_frame = import_file_main.transforms[0]
    child_list = get_child_nodes(import_file_main, current_idx, file_type)
    import_file_main_nodes = import_file_main.nodes

    if len(child_list) == 0 and import_file_main_nodes[current_idx].parent and not import_file_main_nodes[current_idx].parent == -1:
        bone_distance = (Vector((0, 0, 0)) - first_frame[current_idx].translation).length
        if file_version >= global_functions.get_version_matrix_check(file_type):
            bone_distance = (first_frame[import_file_main_nodes[current_idx].parent].translation - first_frame[current_idx].translation).length

    elif len(child_list) == 1:
        bone_distance = child_list[0]

    elif len(child_list) > 1:
        bone_distance = sum(child_list) / len(child_list)

    if bone_distance < 1.0:
        bone_distance = 1

    return bone_distance
