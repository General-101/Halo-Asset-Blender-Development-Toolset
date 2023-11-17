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

import io
import os
import bpy
import bmesh
import struct

from .. import config
from math import radians
from mathutils import Vector, Matrix
from ..global_functions import global_functions, mesh_processing
from ..file_tag.file_shader_environment.format_retail import EnvironmentTypeEnum, EnvironmentFlags, DiffuseFlags, ReflectionFlags
from ..file_tag.file_shader_model.format_retail import ModelFlags, DetailFumctionEnum, DetailMaskEnum, FunctionEnum
from ..file_tag.file_bitmap.h1.format_retail import FormatEnum

class Surface:
    def __init__(self, material_index=0, surface_normal=Vector(), vertices=None):
        self.material_index = material_index
        self.surface_normal = surface_normal
        self.vertices = vertices

class Vertex:
    def __init__(self, vertex_index=0, normal_index=0, UV=(0.0, 0.0), node_0_index=0, node_1_index=-1, weight=1.0):
        self.vertex_index = vertex_index
        self.normal_index = normal_index
        self.UV = UV
        self.node_0_index = node_0_index
        self.node_1_index = node_1_index
        self.weight = weight

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

    elif game_version == "halo3":
        symbol_list = ("%", "#", "?", "!", "@", "*", "$", "^", "-", "&", "=", ".", ";", ")", ">", "<", "|", "~", "(", "{", "}", "[", "'", "]")

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

                processed_parameters.append(parameter.lower())

    return (processed_name, processed_parameters)

def append_material_symbols(material, game_version, is_ass):
    material_name = material.name
    if material.ass_jms.is_bm and not global_functions.string_empty_check(material.ass_jms.name_override):
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
        if game_version == "halo1":
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

        elif game_version == "halo2":
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
                if split_parameter[0].strip() == "lm" and not "lm" in processed_parameters:
                    processed_symbol_name += " lm:%s" % split_parameter[1]

                elif split_parameter[0].strip() == "lp" and not "lp" in processed_parameters:
                    processed_symbol_name += " lp:%s" % split_parameter[1]

                elif split_parameter[0].strip() == "hl" and not "hl" in processed_parameters:
                    processed_symbol_name += " hl:%s" % split_parameter[1]

                elif split_parameter[0].strip() == "ds" and not "ds" in processed_parameters:
                    processed_symbol_name += " ds:%s" % split_parameter[1]

        elif game_version == "halo3":
            if "%" in used_symbol_list:
                processed_symbol_name += "%"
            if "#" in used_symbol_list:
                processed_symbol_name += "#"
            if "?" in used_symbol_list:
                processed_symbol_name += "?"
            if "!" in used_symbol_list:
                processed_symbol_name += "!"
            if "@" in used_symbol_list:
                processed_symbol_name += "@"
            if "*" in used_symbol_list:
                processed_symbol_name += "*"
            if "$" in used_symbol_list:
                processed_symbol_name += "$"
            if "^" in used_symbol_list:
                processed_symbol_name += "^"
            if "-" in used_symbol_list:
                processed_symbol_name += "-"
            if "&" in used_symbol_list:
                processed_symbol_name += "&"
            if "=" in used_symbol_list:
                processed_symbol_name += "="
            if "." in used_symbol_list:
                processed_symbol_name += "."
            if ";" in used_symbol_list:
                processed_symbol_name += ";"
            if ")" in used_symbol_list:
                processed_symbol_name += ")"
            if ">" in used_symbol_list:
                processed_symbol_name += ">"
            if "<" in used_symbol_list:
                processed_symbol_name += "<"
            if "|" in used_symbol_list:
                processed_symbol_name += "|"
            if "~" in used_symbol_list:
                processed_symbol_name += "~"
            if "(" in used_symbol_list:
                processed_symbol_name += "("
            if "{" in used_symbol_list:
                processed_symbol_name += "{"
            if "}" in used_symbol_list:
                processed_symbol_name += "}"
            if "[" in used_symbol_list:
                processed_symbol_name += "["
            if "'" in used_symbol_list:
                processed_symbol_name += "'"
            if "]" in used_symbol_list:
                processed_symbol_name += "]"

            for parameter in processed_parameters:
                split_parameter = parameter.split(':', 1)
                if split_parameter[0].strip() == "lm" and not "lm" in processed_parameters:
                    processed_symbol_name += " lm:%s" % split_parameter[1]

                elif split_parameter[0].strip() == "lp" and not "lp" in processed_parameters:
                    processed_symbol_name += " lp:%s" % split_parameter[1]

                elif split_parameter[0].strip() == "hl" and not "hl" in processed_parameters:
                    processed_symbol_name += " hl:%s" % split_parameter[1]

                elif split_parameter[0].strip() == "ds" and not "ds" in processed_parameters:
                    processed_symbol_name += " ds:%s" % split_parameter[1]

                elif split_parameter[0].strip() == "pf" and not "pf" in processed_parameters:
                    processed_symbol_name += " pf:%s" % split_parameter[1]

                elif split_parameter[0].strip() == "lt" and not "lt" in processed_parameters:
                    processed_symbol_name += " lt:%s" % split_parameter[1]

                elif split_parameter[0].strip() == "to" and not "to" in processed_parameters:
                    processed_symbol_name += " to:%s" % split_parameter[1]

                elif split_parameter[0].strip() == "at" and not "at" in processed_parameters:
                    processed_symbol_name += " at:%s" % split_parameter[1]

                elif split_parameter[0].strip() == "ro" and not "ro" in processed_parameters:
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

def generate_marker(context, collection, game_version, game_title, file_version, filepath, ASSET, region_element_name, marker_group, armature, marker_obj, fix_rotations, empty_markers, is_intermediate):
    parent_idx = -1
    if is_intermediate:
        parent_idx = marker_obj.parent
        marker_region_index = marker_obj.region
        radius = marker_obj.radius

    else:
        parent_idx = marker_obj.node_index

    marker_name = ""
    if game_title == 'halo1':
        marker_name = marker_obj.name
    else:
        marker_name = marker_group
        if not marker_obj.region_index == -1:
            region_element = ASSET.regions[marker_obj.region_index]
            permutation_element = region_element.permutations[marker_obj.permutation_index]
            marker_name = "(%s %s)%s" % (permutation_element.name, region_element.name, marker_group)

    object_name_prefix = '#%s' % marker_name
    marker_name_override = ""
    if context.scene.objects.get('#%s' % marker_name):
        marker_name_override = marker_name

    if empty_markers:
        object_mesh = bpy.data.objects.new(object_name_prefix, None)

    else:
        mesh = bpy.data.meshes.new(object_name_prefix)
        object_mesh = bpy.data.objects.new(object_name_prefix, mesh)

    collection.objects.link(object_mesh)

    if filepath:
        if game_title == "halo1":
            if 'physics' in filepath or 'collision' in filepath:
                object_mesh.ass_jms.marker_mask_type = '1'

        else:
            if 'collision' in filepath:
                object_mesh.ass_jms.marker_mask_type = '1'

            elif 'physics' in filepath:
                object_mesh.ass_jms.marker_mask_type = '2'

    object_mesh.ass_jms.name_override = marker_name_override

    if not empty_markers:
        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
        bm.to_mesh(mesh)
        bm.free()

    if game_title == "halo1":
        region_name = None
        if is_intermediate:
            if not marker_region_index == -1:
                region_name = ASSET.regions[marker_region_index].name

        region_name = region_element_name
        if region_name == "__unnamed":
            region_name = "unnamed"

        if not region_name == None:
            if empty_markers:
                object_mesh.ass_jms.marker_region = region_name

            else:
                object_mesh.region_add(region_name)

    if not parent_idx == -1:
        bone_name = ASSET.nodes[parent_idx].name

        object_mesh.parent = armature
        object_mesh.parent_type = "BONE"
        object_mesh.parent_bone = bone_name

    else:
        object_mesh.parent = armature

    matrix_translate = Matrix.Translation(marker_obj.translation)
    matrix_rotation = marker_obj.rotation.to_matrix().to_4x4()

    transform_matrix = matrix_translate @ matrix_rotation
    if not parent_idx == -1:
        pose_bone = armature.pose.bones[ASSET.nodes[parent_idx].name]

        if fix_rotations:
            transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix

        else:
            transform_matrix = pose_bone.matrix @ transform_matrix

    object_mesh.matrix_world = transform_matrix
    if empty_markers:
        object_mesh.empty_display_type = 'ARROWS'

    else:
        object_mesh.data.ass_jms.Object_Type = 'SPHERE'

    if is_intermediate:
        object_scale = radius
        object_mesh.scale = (object_scale, object_scale, object_scale)

    object_mesh.select_set(False)
    armature.select_set(False)

def optimize_geo(object_vertices, object_triangles):
    # From MEK
    verts = object_vertices
    vert_ct = len(verts)
    # this will map the verts to prune to the vert they are identical to
    dup_vert_map = {}
    similar_vert_map = {}

    for vertex_idx, vertex in enumerate(object_vertices):
        similar_vert_map.setdefault((tuple(vertex.translation)), []).append(vertex_idx)

    # loop over all verts and figure out which ones to replace with others
    for similar_vert_indices in similar_vert_map.values():
        for i in range(len(similar_vert_indices) - 1):
            orig_idx = similar_vert_indices[i]
            if orig_idx in dup_vert_map:
                continue

            vert_a = object_vertices[orig_idx]
            for j in similar_vert_indices[i + 1: ]:
                if j in dup_vert_map:
                    continue

                vert_b = object_vertices[j]
                a_node_influence_count = len(vert_a.node_set)
                b_node_influence_count = len(vert_b.node_set)
                a_uv_count = len(vert_a.uv_set)
                b_uv_count = len(vert_b.uv_set)
                if vert_a.normal != vert_b.normal:
                    continue

                elif vert_a.color != vert_b.color:
                    continue

                matching_node_set = True
                if a_node_influence_count == b_node_influence_count:
                    for node_index in range(a_node_influence_count):
                        if vert_a.node_set[node_index] != vert_b.node_set[node_index]:
                            matching_node_set = False

                else:
                    matching_node_set = False

                if not matching_node_set:
                    continue

                matching_uv_set = True
                if a_uv_count == b_uv_count:
                    for uv_index in range(a_uv_count):
                        if vert_a.uv_set[uv_index] != vert_b.uv_set[uv_index]:
                            matching_uv_set = False

                else:
                    matching_uv_set = False

                if not matching_uv_set:
                    continue

                dup_vert_map[j] = orig_idx

    if not dup_vert_map:
        new_verts = object_vertices
        # nothing to optimize away
        return new_verts, object_triangles

    # remap any duplicate triangle vert indices to the original
    get_mapped_vert = dup_vert_map.get
    for tri in object_triangles:
        tri.v0 = get_mapped_vert(tri.v0, tri.v0)
        tri.v1 = get_mapped_vert(tri.v1, tri.v1)
        tri.v2 = get_mapped_vert(tri.v2, tri.v2)

    # copy the verts list so we can modify it without side-effects
    new_vert_ct = vert_ct - len(dup_vert_map)
    new_verts = object_vertices[: new_vert_ct]

    shift_map = {}
    copy_idx = vert_ct - 1
    # loop over all duplicate vert indices and move any vertices
    # on the high end of the vert list down to fill in the empty
    # spaces left by the duplicate verts we're removing.
    for dup_i in sorted(dup_vert_map):
        while copy_idx in dup_vert_map:
            # keep looping until we get to a vert we can move
            # from its high index to overwrite the low index dup
            copy_idx -= 1

        if copy_idx <= dup_i or dup_i >= new_vert_ct:
            # cant copy any lower. all upper index verts are duplicates
            break

        # move the vert from its high index to the low index dup
        new_verts[dup_i] = verts[copy_idx]
        shift_map[copy_idx] = dup_i
        copy_idx -= 1

    # remap any triangle vert indices
    get_mapped_vert = shift_map.get
    for tri in object_triangles:
        tri.v0 = get_mapped_vert(tri.v0, tri.v0)
        tri.v1 = get_mapped_vert(tri.v1, tri.v1)
        tri.v2 = get_mapped_vert(tri.v2, tri.v2)

    return new_verts, object_triangles

def generate_mesh_object_retail(asset, object_vertices, object_triangles, object_name, collection, game_title, random_color_gen, armature, context):
    vertex_groups = []
    active_region_permutations = []

    object_vertices, object_triangles = optimize_geo(object_vertices, object_triangles)
    verts = [vertex.translation for vertex in object_vertices]
    tris = [(triangles.v0, triangles.v1, triangles.v2) for triangles in object_triangles]

    mesh = bpy.data.meshes.new(object_name)
    mesh.from_pydata(verts, [], tris)
    object_mesh = bpy.data.objects.new(object_name, mesh)
    for tri_idx, poly in enumerate(mesh.polygons):
        tri = object_triangles[tri_idx]
        v0_index = tri.v0
        vert = object_vertices[v0_index]

        if poly.normal.dot(vert.normal) < 0:
            poly.flip()

        poly.use_smooth = True

    region_attribute = mesh.get_custom_attribute()
    for vertex_idx, vertex in enumerate(object_vertices):
        for node_values in vertex.node_set:
            node_index = node_values[0]
            node_weight = node_values[1]
            if not node_index == -1 and not node_index in vertex_groups:
                vertex_groups.append(node_index)
                object_mesh.vertex_groups.new(name = asset.nodes[node_index].name)

            if not node_index == -1:
                group_name = asset.nodes[node_index].name
                group_index = object_mesh.vertex_groups.keys().index(group_name)

                object_mesh.vertex_groups[group_index].add([vertex_idx], node_weight, 'ADD')

        if not vertex.color == None and game_title == "halo3" and asset.version >= get_color_version_check("JMS"):
            color_r = vertex.color[0]
            color_g = vertex.color[1]
            color_b = vertex.color[2]
            color_a = 1
            if color_r < -1000 and color_g < -1000 and color_b < -1000:
                color_r = 0.0
                color_g = 0.01
                color_b = 0.0

            layer_color = mesh.color_attributes.get("color")
            if layer_color is None:
                layer_color = mesh.color_attributes.new("color", "FLOAT_COLOR", "POINT")

            layer_color.data[vertex_idx].color = [color_r, color_g, color_b, color_a]

    for triangle_idx, triangle in enumerate(object_triangles):
        triangle_material_index = triangle.material_index
        mat = None
        if not triangle_material_index == -1:
            mat = asset.materials[triangle_material_index]

        if game_title == "halo1":
            if asset.version >= 8198:
                region = triangle.region
                current_region_permutation = asset.regions[region].name

            else:
                region = asset.vertices[triangle.v0].region
                current_region_permutation = asset.regions[region].name

        elif game_title == "halo2" or game_title == "halo3":
            current_region_permutation = global_functions.material_definition_helper(triangle_material_index, mat)

        if not current_region_permutation in active_region_permutations:
            active_region_permutations.append(current_region_permutation)
            object_mesh.region_add(current_region_permutation)

        if not triangle_material_index == -1:
            material_name = mat.name
            mat = bpy.data.materials.get(material_name)
            if mat is None:
                mat = bpy.data.materials.new(name=material_name)

            if not material_name in object_mesh.data.materials.keys():
                object_mesh.data.materials.append(mat)

            mat.diffuse_color = random_color_gen.next()
            material_index = object_mesh.data.materials.keys().index(material_name)
            object_mesh.data.polygons[triangle_idx].material_index = material_index

        region_index = active_region_permutations.index(current_region_permutation)
        region_attribute.data[triangle_idx].value = region_index + 1

        vertex_list = [object_vertices[triangle.v0], object_vertices[triangle.v1], object_vertices[triangle.v2]]
        for vertex_idx, vertex in enumerate(vertex_list):
            loop_index = (3 * triangle_idx) + vertex_idx
            for uv_idx, uv in enumerate(vertex.uv_set):
                uv_name = 'UVMap_%s' % uv_idx
                layer_uv = mesh.uv_layers.get(uv_name)
                if layer_uv is None:
                    layer_uv = mesh.uv_layers.new(name=uv_name)

                layer_uv.data[loop_index].uv = (uv[0], uv[1])

    collection.objects.link(object_mesh)

    if not armature == None:
        object_mesh.parent = armature
        mesh_processing.add_modifier(context, object_mesh, False, None, armature)

    return object_mesh

def generate_mesh_retail(context, asset, object_vertices, object_triangles, object_data, game_title, random_color_gen):
    object_vertices, object_triangles = optimize_geo(object_vertices, object_triangles)
    verts = [vertex.translation for vertex in object_vertices]
    tris = [(triangles.v0, triangles.v1, triangles.v2) for triangles in object_triangles]

    vertex_weights_sets = []
    region_list = []

    object_data.from_pydata(verts, [], tris)
    for poly in object_data.polygons:
        poly.use_smooth = True

    region_attribute = object_data.get_custom_attribute()
    for vertex_idx, vertex in enumerate(object_vertices):
        node_set = []
        for node_values in vertex.node_set:
            node_index = node_values[0]
            node_weight = node_values[1]
            if not node_index == -1:
                node_set.append((node_index, node_weight))

        vertex_weights_sets.append(node_set)

    for triangle_idx, triangle in enumerate(object_triangles):
        triangle_material_index = triangle.material_index
        mat = None
        if not triangle_material_index == -1:
            mat = asset.materials[triangle_material_index]

        if game_title == "halo1":
            if asset.version >= 8198:
                region = triangle.region
                current_region_permutation = asset.regions[region].name

            else:
                region = asset.vertices[triangle.v0].region
                current_region_permutation = asset.regions[region].name

        elif game_title == "halo2" or game_title == "halo3":
            current_region_permutation = global_functions.material_definition_helper(triangle_material_index, mat)

        if not current_region_permutation in region_list:
            region_list.append(current_region_permutation)

        if not triangle_material_index == -1:
            material_name = mat.name
            mat = bpy.data.materials.get(material_name)
            if mat is None:
                mat = bpy.data.materials.new(name=material_name)

            if not mat in object_data.materials.values():
                object_data.materials.append(mat)

            mat.diffuse_color = random_color_gen.next()
            material_index = object_data.materials.values().index(mat)
            object_data.polygons[triangle_idx].material_index = material_index

        region_index = region_list.index(current_region_permutation)
        region_attribute.data[triangle_idx].value = region_index + 1

        vertex_list = [object_vertices[triangle.v0], object_vertices[triangle.v1], object_vertices[triangle.v2]]
        for vertex_idx, vertex in enumerate(vertex_list):
            loop_index = (3 * triangle_idx) + vertex_idx
            for uv_idx, uv in enumerate(vertex.uv_set):
                uv_name = 'UVMap_%s' % uv_idx
                layer_uv = object_data.uv_layers.get(uv_name)
                if layer_uv is None:
                    layer_uv = object_data.uv_layers.new(name=uv_name)

                layer_uv.data[loop_index].uv = (uv[0], uv[1])

            if not vertex.color == None and game_title == "halo3" and asset.version >= get_color_version_check("JMS"):
                color_r = vertex.color[0]
                color_g = vertex.color[1]
                color_b = vertex.color[2]
                color_a = 1
                if color_r < -1000 and color_g < -1000 and color_b < -1000:
                    color_r = 0.0
                    color_g = 0.01
                    color_b = 0.0

                layer_color = object_data.color_attributes.get("color")
                if layer_color is None:
                    layer_color = object_data.color_attributes.new("color", "BYTE_COLOR", "CORNER")

                layer_color.data[loop_index].color = (color_r, color_g, color_b, color_a)

    return vertex_weights_sets, region_list

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

def process_mesh_export_color(evaluted_mesh, loop_index, vertex_index):
    color = (0.0, 0.0, 0.0)
    if not evaluted_mesh.attributes.active_color == None:
        if evaluted_mesh.attributes.active_color.domain == "POINT":
            color = evaluted_mesh.attributes.active_color.data[vertex_index].color
        else:
            color = evaluted_mesh.attributes.active_color.data[loop_index].color

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

def process_mesh_export_vert(vert, point, file_type, original_geo_matrix, custom_scale):
    if file_type == 'JMS':
        translation = vert.co
        negative_matrix = original_geo_matrix.determinant() < 0.0
        if negative_matrix and file_type == 'JMS':
            invert_translation_x = vert.co[0] * -1
            invert_translation_y = vert.co[1] * -1
            invert_translation_z = vert.co[2] * -1
            translation = Vector((invert_translation_x, invert_translation_y, invert_translation_z))

        final_translation = original_geo_matrix @ translation
        final_normal = (original_geo_matrix @ (translation + point.normal) - final_translation).normalized()

        if negative_matrix and original_geo_matrix.determinant() < 0.0 and file_type == 'JMS':
            invert_normal_x = final_normal[0] * -1
            invert_normal_y = final_normal[1] * -1
            invert_normal_z = final_normal[2] * -1

            final_normal = Vector((invert_normal_x, invert_normal_y, invert_normal_z))

    else:
        final_translation = custom_scale * vert.co
        final_normal = (point.normal).normalized()

    return final_translation, final_normal

def process_mesh_export_face_set(default_permutation, default_region, game_version, original_geo, region_idx):
    if game_version == "halo1":
        if not region_idx == -1:
            region = original_geo.region_list[region_idx].name
            face_set = (None, None, region)

    else:
        if not region_idx == -1:
            face_set = original_geo.region_list[region_idx].name.split()

        lod, permutation, region = global_functions.material_definition_parser(False, face_set, default_region, default_permutation)
        face_set = (lod, permutation, region)

    return face_set

def get_default_region_permutation_name(game_version):
    default_name = None
    if game_version == "halo1":
        default_name = 'unnamed'

    else:
        default_name = 'Default'

    return default_name

def get_lod(lod_setting, game_version):
    LOD_name = None
    if game_version == "halo1":
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

def get_child_nodes(import_file_prerelease, import_file_main, parent_idx, file_type):
    file_version = import_file_main.version
    first_frame = import_file_main.transforms[0]

    child_list = []
    for child_idx, node in enumerate(import_file_main.nodes):
        if node.parent == parent_idx:
            child_distance = (Vector((0, 0, 0)) - first_frame[child_idx].translation).length
            if file_version >= global_functions.get_version_matrix_check(file_type, None):
                child_distance = (first_frame[parent_idx].translation - first_frame[child_idx].translation).length

            child_list.append(child_distance)

    return child_list

def get_bone_distance(import_file_prerelease, import_file_main, current_idx, file_type):
    bone_distance = 0
    file_version = import_file_main.version
    first_frame = import_file_main.transforms[0]

    child_list = get_child_nodes(import_file_prerelease, import_file_main, current_idx, file_type)
    import_file_main_nodes = import_file_main.nodes

    if len(child_list) == 0 and import_file_main_nodes[current_idx].parent and not import_file_main_nodes[current_idx].parent == -1:
        bone_distance = (Vector((0, 0, 0)) - first_frame[current_idx].translation).length
        if file_version >= global_functions.get_version_matrix_check(file_type, None):
            bone_distance = (first_frame[import_file_main_nodes[current_idx].parent].translation - first_frame[current_idx].translation).length

    elif len(child_list) == 1:
        bone_distance = child_list[0]

    elif len(child_list) > 1:
        bone_distance = sum(child_list) / len(child_list)

    if bone_distance < 1.0:
        bone_distance = 1

    return bone_distance

def get_output_material_node(mat):
    output_material_node = None
    if not mat == None and mat.use_nodes and not mat.node_tree == None:
        for node in mat.node_tree.nodes:
            if node.type == "OUTPUT_MATERIAL" and node.is_active_output:
                output_material_node = node
                break

    if output_material_node is None:
        output_material_node = mat.node_tree.nodes.new("ShaderNodeOutputMaterial")
        output_material_node.location = (0.0, 0.0)

    return output_material_node

def get_linked_node(node, input_name, search_type):
    linked_node = None
    node_input = node.inputs[input_name]
    if node_input.is_linked:
        for node_link in node_input.links:
            if node_link.from_node.type == search_type:
                linked_node = node_link.from_node
                break

    return linked_node

def connect_inputs(tree, output_node, output_name, input_node, input_name):
    tree.links.new(output_node.outputs[output_name], input_node.inputs[input_name])

def generate_image_node(mat, texture, is_env=False):
    if is_env:
        image_node = mat.node_tree.nodes.new("ShaderNodeTexEnvironment")
    else:
        image_node = mat.node_tree.nodes.new("ShaderNodeTexImage")

    if not texture == None:
        image = bpy.data.images.load(texture, check_existing=True)
        image_node.image = image
    
    else:
        image = bpy.data.images.get("White")
        if not image:
            image = bpy.data.images.new("White", 2, 2)
            image.generated_color = (1, 1, 1, 1)

        image_node.image = image

    return image_node

def generate_biased_multiply_node(tree):
    biased_multiply_logic_group = bpy.data.node_groups.get("Biased Multiply")
    if not biased_multiply_logic_group:
        biased_multiply_logic_group = bpy.data.node_groups.new(type="ShaderNodeTree", name="Biased Multiply")

        base_color_socket = biased_multiply_logic_group.inputs.new("NodeSocketColor", "Color")
        detail_color_socket = biased_multiply_logic_group.inputs.new("NodeSocketColor", "Detail")
        reflection_mask_socket = biased_multiply_logic_group.inputs.new("NodeSocketColor", "Mask")
        input_node = biased_multiply_logic_group.nodes.new("NodeGroupInput")
        input_node.location = Vector((-1100, 0))

        base_color_socket.default_value = (0.5, 0.5, 0.5, 1)
        detail_color_socket.default_value = (0.0, 0.0, 0.0, 1)
        reflection_mask_socket.default_value = (0.0, 0.0, 0.0, 1)

        color_socket = biased_multiply_logic_group.outputs.new("NodeSocketColor", "Color")
        output_node = biased_multiply_logic_group.nodes.new("NodeGroupOutput")
        output_node.location = Vector((0.0, 0.0))

        color_socket.default_value = (0, 0, 0, 0)

        mix_node = biased_multiply_logic_group.nodes.new("ShaderNodeMix")
        mix_node.data_type = 'RGBA'
        mix_node.blend_type = "MULTIPLY"
        mix_node.clamp_result = True
        mix_node.location = Vector((-850, -175))
        mix_node.inputs[0].default_value = 1

        connect_inputs(biased_multiply_logic_group, input_node, "Detail", mix_node, 6)
        connect_inputs(biased_multiply_logic_group, input_node, "Mask", mix_node, 7)

        base_seperate_node = biased_multiply_logic_group.nodes.new("ShaderNodeSeparateColor")
        base_seperate_node.location = Vector((-850, 175))
        connect_inputs(biased_multiply_logic_group, input_node, "Color", base_seperate_node, "Color")

        detail_seperate_node = biased_multiply_logic_group.nodes.new("ShaderNodeSeparateColor")
        detail_seperate_node.location = Vector((-600, -175))
        connect_inputs(biased_multiply_logic_group, mix_node, 2, detail_seperate_node, "Color")

        x_node = biased_multiply_logic_group.nodes.new("ShaderNodeValue")
        x_node.location = Vector((-850, 325))
        x_node.outputs[0].default_value = 2

        multiply_node_a_0 = biased_multiply_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_a_0.operation = 'MULTIPLY'
        multiply_node_a_0.use_clamp = True
        multiply_node_a_0.location = Vector((-600, 525))
        connect_inputs(biased_multiply_logic_group, base_seperate_node, "Red", multiply_node_a_0, 0)
        connect_inputs(biased_multiply_logic_group, x_node, "Value", multiply_node_a_0, 1)

        multiply_node_a_1 = biased_multiply_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_a_1.operation = 'MULTIPLY'
        multiply_node_a_1.use_clamp = True
        multiply_node_a_1.location = Vector((-600, 350))
        connect_inputs(biased_multiply_logic_group, base_seperate_node, "Green", multiply_node_a_1, 0)
        connect_inputs(biased_multiply_logic_group, x_node, "Value", multiply_node_a_1, 1)

        multiply_node_a_2 = biased_multiply_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_a_2.operation = 'MULTIPLY'
        multiply_node_a_2.use_clamp = True
        multiply_node_a_2.location = Vector((-600, 175))
        connect_inputs(biased_multiply_logic_group, base_seperate_node, "Blue", multiply_node_a_2, 0)
        connect_inputs(biased_multiply_logic_group, x_node, "Value", multiply_node_a_2, 1)

        multiply_node_b_0 = biased_multiply_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_b_0.operation = 'MULTIPLY'
        multiply_node_b_0.use_clamp = True
        multiply_node_b_0.location = Vector((-350, 175))
        connect_inputs(biased_multiply_logic_group, multiply_node_a_0, "Value", multiply_node_b_0, 0)
        connect_inputs(biased_multiply_logic_group, detail_seperate_node, "Red", multiply_node_b_0, 1)

        multiply_node_b_1 = biased_multiply_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_b_1.operation = 'MULTIPLY'
        multiply_node_b_1.use_clamp = True
        multiply_node_b_1.location = Vector((-350, 0))
        connect_inputs(biased_multiply_logic_group, multiply_node_a_1, "Value", multiply_node_b_1, 0)
        connect_inputs(biased_multiply_logic_group, detail_seperate_node, "Green", multiply_node_b_1, 1)

        multiply_node_b_2 = biased_multiply_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_b_2.operation = 'MULTIPLY'
        multiply_node_b_2.use_clamp = True
        multiply_node_b_2.location = Vector((-350, -175))
        connect_inputs(biased_multiply_logic_group, multiply_node_a_2, "Value", multiply_node_b_2, 0)
        connect_inputs(biased_multiply_logic_group, detail_seperate_node, "Blue", multiply_node_b_2, 1)

        combine_rgb_node = biased_multiply_logic_group.nodes.new("ShaderNodeCombineColor")
        combine_rgb_node.location = Vector((-175, 0))
        connect_inputs(biased_multiply_logic_group, multiply_node_b_0, "Value", combine_rgb_node, "Red")
        connect_inputs(biased_multiply_logic_group, multiply_node_b_1, "Value", combine_rgb_node, "Green")
        connect_inputs(biased_multiply_logic_group, multiply_node_b_2, "Value", combine_rgb_node, "Blue")
        connect_inputs(biased_multiply_logic_group, combine_rgb_node, "Color", output_node, "Color")

    biased_multiply_node = tree.nodes.new('ShaderNodeGroup')
    biased_multiply_node.node_tree = biased_multiply_logic_group

    return biased_multiply_node

def generate_multiply_node(tree):
    multiply_logic_group = bpy.data.node_groups.get("Multiply")
    if not multiply_logic_group:
        multiply_logic_group = bpy.data.node_groups.new(type="ShaderNodeTree", name="Multiply")

        base_color_socket = multiply_logic_group.inputs.new("NodeSocketColor", "Color")
        detail_color_socket = multiply_logic_group.inputs.new("NodeSocketColor", "Detail")
        reflection_mask_socket = multiply_logic_group.inputs.new("NodeSocketColor", "Mask")
        input_node = multiply_logic_group.nodes.new("NodeGroupInput")
        input_node.location = Vector((-350, 0))

        base_color_socket.default_value = (1, 1, 1, 1)
        detail_color_socket.default_value = (1, 1, 1, 1)
        reflection_mask_socket.default_value = (1, 1, 1, 1)

        color_socket = multiply_logic_group.outputs.new("NodeSocketColor", "Color")
        output_node = multiply_logic_group.nodes.new("NodeGroupOutput")
        output_node.location = Vector((0, 0))

        color_socket.default_value = (0, 0, 0, 0)

        mix_node_0 = multiply_logic_group.nodes.new("ShaderNodeMix")
        mix_node_0.data_type = 'RGBA'
        mix_node_0.blend_type = "MULTIPLY"
        mix_node_0.clamp_result = True
        mix_node_0.location = Vector((-175, 0))
        mix_node_0.inputs[0].default_value = 1
        connect_inputs(multiply_logic_group, input_node, "Color", mix_node_0, 6)
        connect_inputs(multiply_logic_group, input_node, "Detail", mix_node_0, 7)
        connect_inputs(multiply_logic_group, input_node, "Mask", mix_node_0, 0)
        connect_inputs(multiply_logic_group, mix_node_0, 2, output_node, "Color")

    multiply_node = tree.nodes.new('ShaderNodeGroup')
    multiply_node.node_tree = multiply_logic_group

    return multiply_node

def generate_biased_add_node(tree):
    biased_add_logic_group = bpy.data.node_groups.get("Biased Add")
    if not biased_add_logic_group:
        biased_add_logic_group = bpy.data.node_groups.new(type="ShaderNodeTree", name="Biased Add")

        base_color_socket = biased_add_logic_group.inputs.new("NodeSocketColor", "Color")
        detail_color_socket = biased_add_logic_group.inputs.new("NodeSocketColor", "Detail")
        reflection_mask_socket = biased_add_logic_group.inputs.new("NodeSocketColor", "Mask")
        input_node = biased_add_logic_group.nodes.new("NodeGroupInput")
        input_node.location = Vector((-1100, 0))

        base_color_socket.default_value = (0.5, 0.5, 0.5, 1)
        detail_color_socket.default_value = (0.0, 0.0, 0.0, 1)
        reflection_mask_socket.default_value = (0.0, 0.0, 0.0, 1)

        color_socket = biased_add_logic_group.outputs.new("NodeSocketColor", "Color")
        output_node = biased_add_logic_group.nodes.new("NodeGroupOutput")
        output_node.location = Vector((0.0, 0.0))

        color_socket.default_value = (0, 0, 0, 0)

        mix_node = biased_add_logic_group.nodes.new("ShaderNodeMix")
        mix_node.data_type = 'RGBA'
        mix_node.blend_type = "MULTIPLY"
        mix_node.clamp_result = True
        mix_node.location = Vector((-850, -175))
        mix_node.inputs[0].default_value = 1

        connect_inputs(biased_add_logic_group, input_node, "Detail", mix_node, 6)
        connect_inputs(biased_add_logic_group, input_node, "Mask", mix_node, 7)

        base_seperate_node = biased_add_logic_group.nodes.new("ShaderNodeSeparateColor")
        base_seperate_node.location = Vector((-850, 175))
        connect_inputs(biased_add_logic_group, input_node, "Color", base_seperate_node, "Color")

        detail_seperate_node = biased_add_logic_group.nodes.new("ShaderNodeSeparateColor")
        detail_seperate_node.location = Vector((-600, -175))
        connect_inputs(biased_add_logic_group, mix_node, 2, detail_seperate_node, "Color")

        x_node = biased_add_logic_group.nodes.new("ShaderNodeValue")
        x_node.location = Vector((-850, 325))
        x_node.outputs[0].default_value = 2

        multiply_node_a_0 = biased_add_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_a_0.operation = 'MULTIPLY'
        multiply_node_a_0.use_clamp = True
        multiply_node_b_0.location = Vector((-600, 525))
        connect_inputs(biased_add_logic_group, base_seperate_node, "Red", multiply_node_a_0, 0)
        connect_inputs(biased_add_logic_group, x_node, "Value", multiply_node_a_0, 1)

        multiply_node_a_1 = biased_add_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_a_1.operation = 'MULTIPLY'
        multiply_node_a_1.use_clamp = True
        multiply_node_b_1.location = Vector((-600, 350))
        connect_inputs(biased_add_logic_group, base_seperate_node, "Green", multiply_node_a_1, 0)
        connect_inputs(biased_add_logic_group, x_node, "Value", multiply_node_a_1, 1)

        multiply_node_a_2 = biased_add_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_a_2.operation = 'MULTIPLY'
        multiply_node_a_2.use_clamp = True
        multiply_node_a_2.location = Vector((-600, 175))
        connect_inputs(biased_add_logic_group, base_seperate_node, "Blue", multiply_node_a_2, 0)
        connect_inputs(biased_add_logic_group, x_node, "Value", multiply_node_a_2, 1)

        multiply_node_b_0 = biased_add_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_b_0.operation = 'ADD'
        multiply_node_b_0.use_clamp = True
        multiply_node_b_0.location = Vector((-350, 175))
        connect_inputs(biased_add_logic_group, multiply_node_a_0, "Value", multiply_node_b_0, 0)
        connect_inputs(biased_add_logic_group, detail_seperate_node, "Red", multiply_node_b_0, 1)

        multiply_node_b_1 = biased_add_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_b_1.operation = 'ADD'
        multiply_node_b_1.use_clamp = True
        multiply_node_b_1.location = Vector((-350, 0))
        connect_inputs(biased_add_logic_group, multiply_node_a_1, "Value", multiply_node_b_1, 0)
        connect_inputs(biased_add_logic_group, detail_seperate_node, "Green", multiply_node_b_1, 1)

        multiply_node_b_2 = biased_add_logic_group.nodes.new("ShaderNodeMath")
        multiply_node_b_2.operation = 'ADD'
        multiply_node_b_2.use_clamp = True
        multiply_node_b_2.location = Vector((-350, -175))
        connect_inputs(biased_add_logic_group, multiply_node_a_2, "Value", multiply_node_b_2, 0)
        connect_inputs(biased_add_logic_group, detail_seperate_node, "Blue", multiply_node_b_2, 1)

        combine_rgb_node = biased_add_logic_group.nodes.new("ShaderNodeCombineColor")
        combine_rgb_node.location = Vector((-175, 0))
        connect_inputs(biased_add_logic_group, multiply_node_b_0, "Value", combine_rgb_node, "Red")
        connect_inputs(biased_add_logic_group, multiply_node_b_1, "Value", combine_rgb_node, "Green")
        connect_inputs(biased_add_logic_group, multiply_node_b_2, "Value", combine_rgb_node, "Blue")
        connect_inputs(biased_add_logic_group, combine_rgb_node, "Color", output_node, "Color")

    biased_add_node = tree.nodes.new('ShaderNodeGroup')
    biased_add_node.node_tree = biased_add_logic_group

    return biased_add_node

def generate_multipurpose_logic_node(tree):
    multipurpose_logic_group = bpy.data.node_groups.get("Multipurpose Logic")
    if not multipurpose_logic_group:
        multipurpose_logic_group = bpy.data.node_groups.new(type="ShaderNodeTree", name="Multipurpose Logic")

        xbox_socket = multipurpose_logic_group.inputs.new("NodeSocketFloat", "Xbox")
        multipurpose_logic_group.inputs.new("NodeSocketVector", "RGB")
        multipurpose_logic_group.inputs.new("NodeSocketFloat", "A")
        input_node = multipurpose_logic_group.nodes.new("NodeGroupInput")
        input_node.location = Vector((-1250.0, 0))

        xbox_socket.default_value = 0.5
        xbox_socket.min_value = -10000.0
        xbox_socket.max_value = 10000.0

        multipurpose_logic_group.outputs.new("NodeSocketFloat", "Reflective Mask")
        multipurpose_logic_group.outputs.new("NodeSocketFloat", "Self Illumination")
        multipurpose_logic_group.outputs.new("NodeSocketFloat", "Change Color")
        multipurpose_logic_group.outputs.new("NodeSocketFloat", "Auxiliary")
        output_node = multipurpose_logic_group.nodes.new("NodeGroupOutput")
        output_node.location = Vector((0, 0))

        seperate_node = multipurpose_logic_group.nodes.new("ShaderNodeSeparateColor")
        seperate_node.location = Vector((-1000.0, 0))
        connect_inputs(multipurpose_logic_group, input_node, "RGB", seperate_node, "Color")

        greater_than_node = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        greater_than_node.operation = 'GREATER_THAN'
        greater_than_node.use_clamp = True
        greater_than_node.inputs[1].default_value = 0
        greater_than_node.location = Vector((-650.0, 300.0))
        connect_inputs(multipurpose_logic_group, input_node, "Xbox", greater_than_node, "Value")

        multiply_greater_node_0 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        multiply_greater_node_0.operation = 'MULTIPLY'
        multiply_greater_node_0.use_clamp = True
        multiply_greater_node_0.location = Vector((-425.0, 825.0))
        connect_inputs(multipurpose_logic_group, greater_than_node, "Value", multiply_greater_node_0, 0)
        connect_inputs(multipurpose_logic_group, seperate_node, "Red", multiply_greater_node_0, 1)

        multiply_greater_node_1 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        multiply_greater_node_1.operation = 'MULTIPLY'
        multiply_greater_node_1.use_clamp = True
        multiply_greater_node_1.location = Vector((-425.0, 650.0))
        connect_inputs(multipurpose_logic_group, greater_than_node, "Value", multiply_greater_node_1, 0)
        connect_inputs(multipurpose_logic_group, seperate_node, "Green", multiply_greater_node_1, 1)

        multiply_greater_node_2 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        multiply_greater_node_2.operation = 'MULTIPLY'
        multiply_greater_node_2.use_clamp = True
        multiply_greater_node_2.location = Vector((-425.0, 475.0))
        connect_inputs(multipurpose_logic_group, greater_than_node, "Value", multiply_greater_node_2, 0)
        connect_inputs(multipurpose_logic_group, seperate_node, "Blue", multiply_greater_node_2, 1)

        multiply_greater_node_3 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        multiply_greater_node_3.operation = 'MULTIPLY'
        multiply_greater_node_3.use_clamp = True
        multiply_greater_node_3.location = Vector((-425.0, 300.0))
        connect_inputs(multipurpose_logic_group, greater_than_node, "Value", multiply_greater_node_3, 0)
        connect_inputs(multipurpose_logic_group, input_node, "A", multiply_greater_node_3, 1)

        less_than_node = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        less_than_node.operation = 'LESS_THAN'
        less_than_node.use_clamp = True
        less_than_node.inputs[1].default_value = 1
        less_than_node.location = Vector((-650.0, -225.0))
        connect_inputs(multipurpose_logic_group, input_node, "Xbox", less_than_node, "Value")

        multiply_less_node_0 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        multiply_less_node_0.operation = 'MULTIPLY'
        multiply_less_node_0.use_clamp = True
        multiply_less_node_0.location = Vector((-425.0, -225))
        connect_inputs(multipurpose_logic_group, less_than_node, "Value", multiply_less_node_0, 0)
        connect_inputs(multipurpose_logic_group, input_node, "A", multiply_less_node_0, 1)

        multiply_less_node_1 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        multiply_less_node_1.operation = 'MULTIPLY'
        multiply_less_node_1.use_clamp = True
        multiply_less_node_1.location = Vector((-425.0, -400))
        connect_inputs(multipurpose_logic_group, less_than_node, "Value", multiply_less_node_1, 0)
        connect_inputs(multipurpose_logic_group, seperate_node, "Green", multiply_less_node_1, 1)

        multiply_less_node_2 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        multiply_less_node_2.operation = 'MULTIPLY'
        multiply_less_node_2.use_clamp = True
        multiply_less_node_2.location = Vector((-425.0, -575))
        connect_inputs(multipurpose_logic_group, less_than_node, "Value", multiply_less_node_2, 0)
        connect_inputs(multipurpose_logic_group, seperate_node, "Red", multiply_less_node_2, 1)

        multiply_less_node_3 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        multiply_less_node_3.operation = 'MULTIPLY'
        multiply_less_node_3.use_clamp = True
        multiply_less_node_3.location = Vector((-425.0, -750))
        connect_inputs(multipurpose_logic_group, less_than_node, "Value", multiply_less_node_3, 0)
        connect_inputs(multipurpose_logic_group, seperate_node, "Blue", multiply_less_node_3, 1)

        add_node_0 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        add_node_0.operation = 'ADD'
        add_node_0.use_clamp = True
        add_node_0.location = Vector((-200, 300))
        connect_inputs(multipurpose_logic_group, multiply_greater_node_0, "Value", add_node_0, 0)
        connect_inputs(multipurpose_logic_group, multiply_less_node_0, "Value", add_node_0, 1)

        add_node_1 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        add_node_1.operation = 'ADD'
        add_node_1.use_clamp = True
        add_node_1.location = Vector((-200, 125))
        connect_inputs(multipurpose_logic_group, multiply_greater_node_1, "Value", add_node_1, 0)
        connect_inputs(multipurpose_logic_group, multiply_less_node_1, "Value", add_node_1, 1)

        add_node_2 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        add_node_2.operation = 'ADD'
        add_node_2.use_clamp = True
        add_node_2.location = Vector((-200, -50))
        connect_inputs(multipurpose_logic_group, multiply_greater_node_2, "Value", add_node_2, 0)
        connect_inputs(multipurpose_logic_group, multiply_less_node_2, "Value", add_node_2, 1)

        add_node_3 = multipurpose_logic_group.nodes.new("ShaderNodeMath")
        add_node_3.operation = 'ADD'
        add_node_3.use_clamp = True
        add_node_3.location = Vector((-200, -225))
        connect_inputs(multipurpose_logic_group, multiply_greater_node_3, "Value", add_node_3, 0)
        connect_inputs(multipurpose_logic_group, multiply_less_node_3, "Value", add_node_3, 1)

        connect_inputs(multipurpose_logic_group, add_node_0, "Value", output_node, "Reflective Mask")
        connect_inputs(multipurpose_logic_group, add_node_1, "Value", output_node, "Self Illumination")
        connect_inputs(multipurpose_logic_group, add_node_2, "Value", output_node, "Change Color")
        connect_inputs(multipurpose_logic_group, add_node_3, "Value", output_node, "Auxiliary")

    mutipurpose_logic_node = tree.nodes.new('ShaderNodeGroup')
    mutipurpose_logic_node.node_tree = multipurpose_logic_group

    return mutipurpose_logic_node

def generate_reflection_tint_logic_node(tree):
    reflection_tint_logic_group = bpy.data.node_groups.get("Reflection Tint Logic")
    if not reflection_tint_logic_group:
        reflection_tint_logic_group = bpy.data.node_groups.new(type="ShaderNodeTree", name="Reflection Tint Logic")

        perpendicular_tint_socket = reflection_tint_logic_group.inputs.new("NodeSocketVector", "Perpendicular Tint")
        reflection_tint_logic_group.inputs.new("NodeSocketFloat", "Perpendicular Brightness")
        parallel_tint_socket = reflection_tint_logic_group.inputs.new("NodeSocketVector", "Parallel Tint")
        reflection_tint_logic_group.inputs.new("NodeSocketFloat", "Parallel Brightness")
        input_node = reflection_tint_logic_group.nodes.new("NodeGroupInput")
        input_node.location = Vector((-700, -200))

        perpendicular_tint_socket.min_value = -10000.0
        perpendicular_tint_socket.max_value = 10000.0

        parallel_tint_socket.min_value = -10000.0
        parallel_tint_socket.max_value = 10000.0

        reflection_tint_socket = reflection_tint_logic_group.outputs.new("NodeSocketColor", "Color")
        reflection_tint_socket.default_value = (0, 0, 0, 0)

        output_node = reflection_tint_logic_group.nodes.new("NodeGroupOutput")
        output_node.location = Vector((0.0, 0.0))

        perpendicular_vect_math_node = reflection_tint_logic_group.nodes.new("ShaderNodeVectorMath")
        perpendicular_vect_math_node.operation = 'MULTIPLY'
        perpendicular_vect_math_node.location = Vector((-525, -125))
        connect_inputs(reflection_tint_logic_group, input_node, "Perpendicular Tint", perpendicular_vect_math_node, 0)
        connect_inputs(reflection_tint_logic_group, input_node, "Perpendicular Brightness", perpendicular_vect_math_node, 1)

        parallel_vect_math_node = reflection_tint_logic_group.nodes.new("ShaderNodeVectorMath")
        parallel_vect_math_node.operation = 'MULTIPLY'
        parallel_vect_math_node.location = Vector((-525, -275))
        connect_inputs(reflection_tint_logic_group, input_node, "Parallel Tint", parallel_vect_math_node, 0)
        connect_inputs(reflection_tint_logic_group, input_node, "Parallel Brightness", parallel_vect_math_node, 1)

        perpendicular_gamma_node = reflection_tint_logic_group.nodes.new('ShaderNodeGamma')
        perpendicular_gamma_node.inputs[1].default_value = 2.2
        perpendicular_gamma_node.location = Vector((-350, -125))
        connect_inputs(reflection_tint_logic_group, perpendicular_vect_math_node, "Vector", perpendicular_gamma_node, "Color")

        parallel_gamma_node = reflection_tint_logic_group.nodes.new('ShaderNodeGamma')
        parallel_gamma_node.inputs[1].default_value = 2.2
        parallel_gamma_node.location = Vector((-350, -275))
        connect_inputs(reflection_tint_logic_group, parallel_vect_math_node, "Vector", parallel_gamma_node, "Color")

        camera_data_node = reflection_tint_logic_group.nodes.new('ShaderNodeCameraData')
        dot_product_node = reflection_tint_logic_group.nodes.new('ShaderNodeVectorMath')
        dot_product_node.operation = 'DOT_PRODUCT'
        camera_data_node.location = Vector((-875, 125))
        dot_product_node.location = Vector((-700, 50))
        connect_inputs(reflection_tint_logic_group, camera_data_node, "View Vector", dot_product_node, 0)

        new_geometry_node = reflection_tint_logic_group.nodes.new('ShaderNodeNewGeometry')
        vector_transform_node = reflection_tint_logic_group.nodes.new('ShaderNodeVectorTransform')
        vector_transform_node.convert_to = 'CAMERA'
        new_geometry_node.location = Vector((-1050, 75))
        vector_transform_node.location = Vector((-875, 0))
        connect_inputs(reflection_tint_logic_group, new_geometry_node, "Normal", vector_transform_node, "Vector")
        connect_inputs(reflection_tint_logic_group, vector_transform_node, "Vector", dot_product_node, 1)

        absolute_node = reflection_tint_logic_group.nodes.new('ShaderNodeMath')
        absolute_node.operation = 'ABSOLUTE'
        absolute_node.use_clamp = True
        absolute_node.location = Vector((-525, 50))
        connect_inputs(reflection_tint_logic_group, dot_product_node, "Value", absolute_node, "Value")

        camera_gamma_node = reflection_tint_logic_group.nodes.new('ShaderNodeGamma')
        camera_gamma_node.inputs[1].default_value = 2.2
        camera_gamma_node.location = Vector((-350, 50))
        connect_inputs(reflection_tint_logic_group, absolute_node, "Value", camera_gamma_node, "Color")

        mix_node = reflection_tint_logic_group.nodes.new("ShaderNodeMix")
        mix_node.data_type = 'RGBA'
        mix_node.blend_type = "MIX"
        mix_node.clamp_result = True
        mix_node.location = Vector((-175, 0))
        connect_inputs(reflection_tint_logic_group, camera_gamma_node, "Color", mix_node, 0)
        connect_inputs(reflection_tint_logic_group, parallel_gamma_node, "Color", mix_node, 6)
        connect_inputs(reflection_tint_logic_group, perpendicular_gamma_node, "Color", mix_node, 7)
        connect_inputs(reflection_tint_logic_group, mix_node, 2, output_node, "Color")

    reflection_tint_node = tree.nodes.new('ShaderNodeGroup')
    reflection_tint_node.node_tree = reflection_tint_logic_group

    return reflection_tint_node

def generate_detail_logic_node(tree, shader):
    detail_logic_group = bpy.data.node_groups.get("Detail Logic")
    if not detail_logic_group:
        detail_logic_group = bpy.data.node_groups.new(type="ShaderNodeTree", name="Detail Logic")

        detail_after_reflection_socket = detail_logic_group.inputs.new("NodeSocketFloat", "Detail After Reflection")
        reflection_color_socket = detail_logic_group.inputs.new("NodeSocketColor", "Reflection Color")
        detail_socket = detail_logic_group.inputs.new("NodeSocketColor", "Detail")
        mask_socket = detail_logic_group.inputs.new("NodeSocketColor", "Mask")
        base_color_socket = detail_logic_group.inputs.new("NodeSocketColor", "Base Color")
        reflection_only_socket = detail_logic_group.inputs.new("NodeSocketColor", "Reflection Only")
        reflection_mask_socket = detail_logic_group.inputs.new("NodeSocketColor", "Reflection Mask")
        input_node = detail_logic_group.nodes.new("NodeGroupInput")
        input_node.location = Vector((-1500.0, 0.0))

        detail_after_reflection_socket.default_value = 0.5
        detail_after_reflection_socket.min_value = -10000.0
        detail_after_reflection_socket.max_value = 10000.0

        detail_after_reflection_socket.default_value = 0.5
        reflection_color_socket.default_value = (0.5, 0.5, 0.5, 1)
        detail_socket.default_value = (0.5, 0.5, 0.5, 1)
        mask_socket.default_value = (0.5, 0.5, 0.5, 1)
        base_color_socket.default_value = (0.5, 0.5, 0.5, 1)
        reflection_only_socket.default_value = (0.0, 0.0, 0.0, 1)
        reflection_mask_socket.default_value = (0.0, 0.0, 0.0, 1)

        color_socket = detail_logic_group.outputs.new("NodeSocketColor", "Color")
        color_socket.default_value = (0, 0, 0, 0)
        output_node = detail_logic_group.nodes.new("NodeGroupOutput")
        output_node.location = Vector((0, 0))

        detail_before_function_node = None
        if shader.shader_body.detail_function == DetailFumctionEnum.double_biased_multiply.value:
            detail_before_function_node = generate_biased_multiply_node(detail_logic_group)
        elif shader.shader_body.detail_function == DetailFumctionEnum.multiply.value:
            detail_before_function_node = generate_multiply_node(detail_logic_group)
        elif shader.shader_body.detail_function == DetailFumctionEnum.double_biased_add.value:
            detail_before_function_node = generate_biased_add_node(detail_logic_group)

        detail_before_function_node.location = Vector((-1250.0, -400.0))
        connect_inputs(detail_logic_group, input_node, "Detail", detail_before_function_node, "Detail")
        connect_inputs(detail_logic_group, input_node, "Mask", detail_before_function_node, "Mask")
        connect_inputs(detail_logic_group, input_node, "Base Color", detail_before_function_node, "Color")

        reflection_before_mix_node = detail_logic_group.nodes.new("ShaderNodeMix")
        reflection_before_mix_node.data_type = 'RGBA'
        reflection_before_mix_node.blend_type = "ADD"
        reflection_before_mix_node.clamp_result = True
        reflection_before_mix_node.location = Vector((-1050.0, -150.0))
        connect_inputs(detail_logic_group, input_node, "Reflection Mask", reflection_before_mix_node, 0)
        connect_inputs(detail_logic_group, detail_before_function_node, "Color", reflection_before_mix_node, 6)
        connect_inputs(detail_logic_group, input_node, "Reflection Only", reflection_before_mix_node, 7)

        before_less_than_node = detail_logic_group.nodes.new("ShaderNodeMath")
        before_less_than_node.operation = 'LESS_THAN'
        before_less_than_node.use_clamp = True
        before_less_than_node.inputs[1].default_value = 1
        before_less_than_node.location = Vector((-850.0, -225.0))
        connect_inputs(detail_logic_group, input_node, "Detail After Reflection", before_less_than_node, "Value")

        detail_seperate_before_node = detail_logic_group.nodes.new("ShaderNodeSeparateColor")
        detail_seperate_before_node.location = Vector((-850.0, -400.0))
        connect_inputs(detail_logic_group, reflection_before_mix_node, 2, detail_seperate_before_node, "Color")

        detail_multiply_node_before_0 = detail_logic_group.nodes.new("ShaderNodeMath")
        detail_multiply_node_before_0.operation = 'MULTIPLY'
        detail_multiply_node_before_0.use_clamp = True
        detail_multiply_node_before_0.location = Vector((-600.0, -175.0))
        connect_inputs(detail_logic_group, before_less_than_node, "Value", detail_multiply_node_before_0, 0)
        connect_inputs(detail_logic_group, detail_seperate_before_node, "Red", detail_multiply_node_before_0, 1)

        detail_multiply_node_before_1 = detail_logic_group.nodes.new("ShaderNodeMath")
        detail_multiply_node_before_1.operation = 'MULTIPLY'
        detail_multiply_node_before_1.use_clamp = True
        detail_multiply_node_before_1.location = Vector((-600.0, -350.0))
        connect_inputs(detail_logic_group, before_less_than_node, "Value", detail_multiply_node_before_1, 0)
        connect_inputs(detail_logic_group, detail_seperate_before_node, "Green", detail_multiply_node_before_1, 1)

        detail_multiply_node_before_2 = detail_logic_group.nodes.new("ShaderNodeMath")
        detail_multiply_node_before_2.operation = 'MULTIPLY'
        detail_multiply_node_before_2.use_clamp = True
        detail_multiply_node_before_2.location = Vector((-600.0, -525.0))
        connect_inputs(detail_logic_group, before_less_than_node, "Value", detail_multiply_node_before_2, 0)
        connect_inputs(detail_logic_group, detail_seperate_before_node, "Blue", detail_multiply_node_before_2, 1)

        detail_after_function_node = None
        if shader.shader_body.detail_function == DetailFumctionEnum.double_biased_multiply.value:
            detail_after_function_node = generate_biased_multiply_node(detail_logic_group)
        elif shader.shader_body.detail_function == DetailFumctionEnum.multiply.value:
            detail_after_function_node = generate_multiply_node(detail_logic_group)
        elif shader.shader_body.detail_function == DetailFumctionEnum.double_biased_add.value:
            detail_after_function_node = generate_biased_add_node(detail_logic_group)

        detail_after_function_node.location = Vector((-1025, 225))
        connect_inputs(detail_logic_group, input_node, "Detail", detail_after_function_node, "Detail")
        connect_inputs(detail_logic_group, input_node, "Mask", detail_after_function_node, "Mask")
        connect_inputs(detail_logic_group, input_node, "Reflection Color", detail_after_function_node, "Color")

        after_greater_than_node = detail_logic_group.nodes.new("ShaderNodeMath")
        after_greater_than_node.operation = 'GREATER_THAN'
        after_greater_than_node.use_clamp = True
        after_greater_than_node.inputs[1].default_value = 0
        after_greater_than_node.location = Vector((-850, 400))
        connect_inputs(detail_logic_group, input_node, "Detail After Reflection", after_greater_than_node, "Value")

        detail_seperate_after_node = detail_logic_group.nodes.new("ShaderNodeSeparateColor")
        detail_seperate_after_node.location = Vector((-850, 225))
        connect_inputs(detail_logic_group, detail_after_function_node, "Color", detail_seperate_after_node, "Color")

        detail_multiply_node_after_0 = detail_logic_group.nodes.new("ShaderNodeMath")
        detail_multiply_node_after_0.operation = 'MULTIPLY'
        detail_multiply_node_after_0.use_clamp = True
        detail_multiply_node_after_0.location = Vector((-600, 525))
        connect_inputs(detail_logic_group, after_greater_than_node, "Value", detail_multiply_node_after_0, 0)
        connect_inputs(detail_logic_group, detail_seperate_after_node, "Red", detail_multiply_node_after_0, 1)

        detail_multiply_node_after_1 = detail_logic_group.nodes.new("ShaderNodeMath")
        detail_multiply_node_after_1.operation = 'MULTIPLY'
        detail_multiply_node_after_1.use_clamp = True
        detail_multiply_node_after_1.location = Vector((-600, 350))
        connect_inputs(detail_logic_group, after_greater_than_node, "Value", detail_multiply_node_after_1, 0)
        connect_inputs(detail_logic_group, detail_seperate_after_node, "Green", detail_multiply_node_after_1, 1)

        detail_multiply_node_after_2 = detail_logic_group.nodes.new("ShaderNodeMath")
        detail_multiply_node_after_2.operation = 'MULTIPLY'
        detail_multiply_node_after_2.use_clamp = True
        detail_multiply_node_after_2.location = Vector((-600, 175))
        connect_inputs(detail_logic_group, after_greater_than_node, "Value", detail_multiply_node_after_2, 0)
        connect_inputs(detail_logic_group, detail_seperate_after_node, "Blue", detail_multiply_node_after_2, 1)

        detail_add_node_0 = detail_logic_group.nodes.new("ShaderNodeMath")
        detail_add_node_0.operation = 'ADD'
        detail_add_node_0.use_clamp = True
        detail_add_node_0.location = Vector((-350, 175))
        connect_inputs(detail_logic_group, detail_multiply_node_after_0, "Value", detail_add_node_0, 0)
        connect_inputs(detail_logic_group, detail_multiply_node_before_0, "Value", detail_add_node_0, 1)

        detail_add_node_1 = detail_logic_group.nodes.new("ShaderNodeMath")
        detail_add_node_1.operation = 'ADD'
        detail_add_node_1.use_clamp = True
        detail_add_node_1.location = Vector((-350, 0))
        connect_inputs(detail_logic_group, detail_multiply_node_after_1, "Value", detail_add_node_1, 0)
        connect_inputs(detail_logic_group, detail_multiply_node_before_1, "Value", detail_add_node_1, 1)

        detail_add_node_2 = detail_logic_group.nodes.new("ShaderNodeMath")
        detail_add_node_2.operation = 'ADD'
        detail_add_node_2.use_clamp = True
        detail_add_node_2.location = Vector((-350, -175))
        connect_inputs(detail_logic_group, detail_multiply_node_after_2, "Value", detail_add_node_2, 0)
        connect_inputs(detail_logic_group, detail_multiply_node_before_2, "Value", detail_add_node_2, 1)

        combine_rgb_node = detail_logic_group.nodes.new("ShaderNodeCombineColor")
        combine_rgb_node.location = Vector((-175, 0))
        connect_inputs(detail_logic_group, detail_add_node_0, "Value", combine_rgb_node, "Red")
        connect_inputs(detail_logic_group, detail_add_node_1, "Value", combine_rgb_node, "Green")
        connect_inputs(detail_logic_group, detail_add_node_2, "Value", combine_rgb_node, "Blue")
        connect_inputs(detail_logic_group, combine_rgb_node, "Color", output_node, "Color")

    detail_logic_node = tree.nodes.new('ShaderNodeGroup')
    detail_logic_node.node_tree = detail_logic_group

    return detail_logic_node

def generate_shader_model(mat, shader, tag_format, report):
    mat.use_nodes = True

    texture_root = config.HALO_1_DATA_PATH
    base_map = None
    multipurpose_map = None
    detail_map = None
    reflection_map = None
    texture_extensions = ("tif", "tiff")

    base_bitmap = shader.shader_body.base_map.parse_tag(tag_format, report, "halo1", "retail")
    if shader.shader_body.base_map.name_length > 0:
        for extension in texture_extensions:
            texture_path = os.path.join(texture_root, "%s.%s" % (shader.shader_body.base_map.name, extension))
            if os.path.isfile(texture_path):
                base_map = texture_path
                break

    if shader.shader_body.multipurpose_map.name_length > 0:
        for extension in texture_extensions:
            texture_path = os.path.join(texture_root, "%s.%s" % (shader.shader_body.multipurpose_map.name, extension))
            if os.path.isfile(texture_path):
                multipurpose_map = texture_path
                break

    if shader.shader_body.detail_map.name_length > 0:
        for extension in texture_extensions:
            texture_path = os.path.join(texture_root, "%s.%s" % (shader.shader_body.detail_map.name, extension))
            if os.path.isfile(texture_path):
                detail_map = texture_path
                break

    if shader.shader_body.reflection_cube_map.name_length > 0:
        for extension in texture_extensions:
            texture_path = os.path.join(texture_root, "%s.%s" % (shader.shader_body.reflection_cube_map.name, extension))
            if os.path.isfile(texture_path):
                reflection_map = texture_path
                break

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    bdsf_principled.inputs[7].default_value = 0
    bdsf_principled.inputs[9].default_value = 1

    base_node = generate_image_node(mat, base_map)
    if not base_node.image == None:
        base_node.image.alpha_mode = 'CHANNEL_PACKED'

    base_node.location = Vector((-1600, 500))
    shader_model_flags = ModelFlags(shader.shader_body.model_flags)
    if base_bitmap:
        ignore_alpha_bitmap = base_bitmap.bitmap_body.format is FormatEnum.compressed_with_color_key_transparency.value
        ignore_alpha_shader = ModelFlags.not_alpha_tested in shader_model_flags
        if ignore_alpha_shader or ignore_alpha_bitmap:
            base_node.image.alpha_mode = 'NONE'
        else:
            connect_inputs(mat.node_tree, base_node, "Alpha", bdsf_principled, "Alpha")
            mat.shadow_method = 'CLIP'
            mat.blend_method = 'CLIP'

    mat.use_backface_culling = False
    if not ModelFlags.two_sided in shader_model_flags:
        mat.use_backface_culling = True

    multipurpose_node = generate_image_node(mat, multipurpose_map)
    multipurpose_node.location = Vector((-1600, 200))
    if not multipurpose_node.image == None:
        multipurpose_node.image.alpha_mode = 'CHANNEL_PACKED'
        multipurpose_node.image.colorspace_settings.name = 'Non-Color'

    multipurpose_node.interpolation = 'Cubic'

    detail_node = generate_image_node(mat, detail_map)
    if not detail_node.image == None:
        detail_node.image.alpha_mode = 'CHANNEL_PACKED'

    detail_node.location = Vector((-1600, -100))

    reflection_node = generate_image_node(mat, reflection_map, True)
    reflection_node.location = Vector((-1600.0, 750.0))
    texture_coordinate_node = mat.node_tree.nodes.new("ShaderNodeTexCoord")
    texture_coordinate_node.location = Vector((-1775.0, 750.0))
    connect_inputs(mat.node_tree, texture_coordinate_node, "Reflection", reflection_node, "Vector")
    
    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-1775, 250))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", base_node, "Vector")
    connect_inputs(mat.node_tree, vect_math_node, "Vector", multipurpose_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-1950, 275))
    combine_xyz_node.location = Vector((-1950, 150))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    map_u_scale = shader.shader_body.map_u_scale
    if shader.shader_body.map_u_scale == 0.0:
        map_u_scale = 1.0

    map_v_scale = shader.shader_body.map_v_scale
    if shader.shader_body.map_v_scale == 0.0:
        map_v_scale = 1.0

    combine_xyz_node.inputs[0].default_value = map_u_scale
    combine_xyz_node.inputs[1].default_value = map_v_scale
    combine_xyz_node.inputs[2].default_value = 1

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-1775, -200))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", detail_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-1950, -175))
    combine_xyz_node.location = Vector((-1950, -300))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)
    detail_map_scale = shader.shader_body.detail_map_scale
    if shader.shader_body.detail_map_scale == 0.0:
        detail_map_scale = 1.0

    combine_xyz_node.inputs[0].default_value = detail_map_scale
    combine_xyz_node.inputs[1].default_value = detail_map_scale + shader.shader_body.detail_map_v_scale
    combine_xyz_node.inputs[2].default_value = 1

    mutipurpose_logic_node = generate_multipurpose_logic_node(mat.node_tree)
    mutipurpose_logic_node.location = Vector((-1125, -240.0))
    is_xbox = 0
    if ModelFlags.multipurpose_map_uses_og_xbox_channel_order in ModelFlags(shader.shader_body.model_flags):
        is_xbox = 1

    mutipurpose_logic_node.inputs[0].default_value = is_xbox
    connect_inputs(mat.node_tree, multipurpose_node, "Color", mutipurpose_logic_node, "RGB")
    connect_inputs(mat.node_tree, multipurpose_node, "Alpha", mutipurpose_logic_node, "A")
    connect_inputs(mat.node_tree, mutipurpose_logic_node, "Self Illumination", bdsf_principled, "Emission Strength")

    reflection_tint_node = generate_reflection_tint_logic_node(mat.node_tree)
    reflection_tint_node.location = Vector((-1125, -475.0))

    perpendicular_tint_node = mat.node_tree.nodes.new('ShaderNodeRGB')
    perpendicular_tint_node.outputs[0].default_value = shader.shader_body.perpendicular_tint_color
    perpendicular_tint_node.location = Vector((-1300, -525.0))
    connect_inputs(mat.node_tree, perpendicular_tint_node, "Color", reflection_tint_node, "Perpendicular Tint")
    reflection_tint_node.inputs["Perpendicular Brightness"].default_value = shader.shader_body.perpendicular_brightness

    parallel_tint_node = mat.node_tree.nodes.new('ShaderNodeRGB')
    parallel_tint_node.outputs[0].default_value = shader.shader_body.parallel_tint_color
    parallel_tint_node.location = Vector((-1300, -725.0))
    connect_inputs(mat.node_tree, parallel_tint_node, "Color", reflection_tint_node, "Parallel Tint")
    reflection_tint_node.inputs["Parallel Brightness"].default_value = shader.shader_body.parallel_brightness

    reflection_mix_node = mat.node_tree.nodes.new("ShaderNodeMix")
    reflection_mix_node.data_type = 'RGBA'
    reflection_mix_node.blend_type = "MULTIPLY"
    reflection_mix_node.clamp_result = True
    reflection_mix_node.inputs[0].default_value = 1
    reflection_mix_node.location = Vector((-950, -240.0))
    connect_inputs(mat.node_tree, reflection_tint_node, "Color", reflection_mix_node, 6)
    connect_inputs(mat.node_tree, reflection_node, "Color", reflection_mix_node, 7)

    multipurpose_mix_node = mat.node_tree.nodes.new("ShaderNodeMix")
    multipurpose_mix_node.data_type = 'RGBA'
    multipurpose_mix_node.blend_type = "MULTIPLY"
    multipurpose_mix_node.clamp_result = True
    multipurpose_mix_node.inputs[0].default_value = 1
    multipurpose_mix_node.location = Vector((-775.0, -240.0))
    connect_inputs(mat.node_tree, mutipurpose_logic_node, "Reflective Mask", multipurpose_mix_node, 6)
    connect_inputs(mat.node_tree, reflection_mix_node, 2, multipurpose_mix_node, 7)

    diffuse_mix_node = mat.node_tree.nodes.new("ShaderNodeMix")
    diffuse_mix_node.data_type = 'RGBA'
    diffuse_mix_node.blend_type = "ADD"
    diffuse_mix_node.clamp_result = True
    diffuse_mix_node.inputs[0].default_value = 1
    diffuse_mix_node.location = Vector((-600.0, -240.0))
    connect_inputs(mat.node_tree, base_node, "Color", diffuse_mix_node, 6)
    connect_inputs(mat.node_tree, multipurpose_mix_node, 2, diffuse_mix_node, 7)

    detail_logic_node = generate_detail_logic_node(mat.node_tree, shader)
    detail_logic_node.location = Vector((-425.0, 0.0))
    detail_logic_node.inputs[3].default_value = (1, 1, 1, 1)
    detail_after_reflections = 0
    if ModelFlags.detail_after_reflections in ModelFlags(shader.shader_body.model_flags):
        connect_inputs(mat.node_tree, mutipurpose_logic_node, "Reflective Mask", detail_logic_node, "Mask")
        detail_after_reflections = 1

    detail_logic_node.inputs[0].default_value = detail_after_reflections
    connect_inputs(mat.node_tree, diffuse_mix_node, 2, detail_logic_node, "Reflection Color")
    connect_inputs(mat.node_tree, detail_node, "Color", detail_logic_node, "Detail")
    connect_inputs(mat.node_tree, base_node, "Color", detail_logic_node, "Base Color")
    connect_inputs(mat.node_tree, reflection_mix_node, 2, detail_logic_node, "Reflection Only")
    connect_inputs(mat.node_tree, mutipurpose_logic_node, "Reflective Mask", detail_logic_node, "Reflection Mask")
    connect_inputs(mat.node_tree, detail_logic_node, "Color", bdsf_principled, "Base Color")

    animation_color_lower_bound_node = mat.node_tree.nodes.new('ShaderNodeRGB')
    animation_color_lower_bound_node.outputs[0].default_value = shader.shader_body.self_illumination_animation_color_lower_bound
    animation_color_lower_bound_node.location = Vector((-775, -550))

    animation_color_upper_bound_node = mat.node_tree.nodes.new('ShaderNodeRGB')
    animation_color_upper_bound_node.outputs[0].default_value = shader.shader_body.self_illumination_animation_color_upper_bound
    animation_color_upper_bound_node.location = Vector((-775, -750))

    animation_color_lower_bound_gamma_node = mat.node_tree.nodes.new('ShaderNodeGamma')
    animation_color_lower_bound_gamma_node.inputs[1].default_value = 2.2
    animation_color_lower_bound_gamma_node.location = Vector((-600, -600))
    connect_inputs(mat.node_tree, animation_color_lower_bound_node, "Color", animation_color_lower_bound_gamma_node, "Color")

    animation_color_upper_bound_gamma_node = mat.node_tree.nodes.new('ShaderNodeGamma')
    animation_color_upper_bound_gamma_node.inputs[1].default_value = 2.2
    animation_color_upper_bound_gamma_node.location = Vector((-600, -750))
    connect_inputs(mat.node_tree, animation_color_upper_bound_node, "Color", animation_color_upper_bound_gamma_node, "Color")

    mix_factor = 1
    if shader.shader_body.self_illumination_animation_function == FunctionEnum.one.value:
        mix_factor = 0

    animation_color_mix_node = mat.node_tree.nodes.new("ShaderNodeMix")
    animation_color_mix_node.data_type = 'RGBA'
    animation_color_mix_node.blend_type = "MULTIPLY"
    animation_color_mix_node.clamp_result = True
    animation_color_mix_node.inputs[0].default_value = mix_factor
    animation_color_mix_node.location = Vector((-425, -600))
    connect_inputs(mat.node_tree, animation_color_lower_bound_gamma_node, "Color", animation_color_mix_node, 6)
    connect_inputs(mat.node_tree, animation_color_upper_bound_gamma_node, "Color", animation_color_mix_node, 7)
    connect_inputs(mat.node_tree, animation_color_mix_node, 2, bdsf_principled, "Emission")

def generate_shader_environment(mat, shader, permutation_index, tag_format, report):
    mat.use_nodes = True

    texture_root = config.HALO_1_DATA_PATH
    base_map = None
    primary_detail_map = None
    secondary_detail_map = None
    micro_detail_map = None
    bump_map = None
    self_illumination_map = None
    reflection_cube_map = None
    texture_extensions = ("tif", "tiff")

    base_bitmap = shader.shader_body.base_map.parse_tag(tag_format, report, "halo1", "retail")
    primary_detail_bitmap = shader.shader_body.primary_detail_map.parse_tag(tag_format, report, "halo1", "retail")
    secondary_detail_bitmap = shader.shader_body.secondary_detail_map.parse_tag(tag_format, report, "halo1", "retail")
    micro_detail_bitmap = shader.shader_body.micro_detail_map.parse_tag(tag_format, report, "halo1", "retail")
    bump_bitmap = shader.shader_body.bump_map.parse_tag(tag_format, report, "halo1", "retail")
    if shader.shader_body.base_map.name_length > 0:
        for extension in texture_extensions:
            texture_path = os.path.join(texture_root, "%s.%s" % (shader.shader_body.base_map.name, extension))
            if os.path.isfile(texture_path):
                base_map = texture_path
                break

    if shader.shader_body.primary_detail_map.name_length > 0:
        for extension in texture_extensions:
            texture_path = os.path.join(texture_root, "%s.%s" % (shader.shader_body.primary_detail_map.name, extension))
            if os.path.isfile(texture_path):
                primary_detail_map = texture_path
                break

    if shader.shader_body.secondary_detail_map.name_length > 0:
        for extension in texture_extensions:
            texture_path = os.path.join(texture_root, "%s.%s" % (shader.shader_body.secondary_detail_map.name, extension))
            if os.path.isfile(texture_path):
                secondary_detail_map = texture_path
                break

    if shader.shader_body.micro_detail_map.name_length > 0:
        for extension in texture_extensions:
            texture_path = os.path.join(texture_root, "%s.%s" % (shader.shader_body.micro_detail_map.name, extension))
            if os.path.isfile(texture_path):
                micro_detail_map = texture_path
                break

    if shader.shader_body.bump_map.name_length > 0:
        for extension in texture_extensions:
            texture_path = os.path.join(texture_root, "%s.%s" % (shader.shader_body.bump_map.name, extension))
            if os.path.isfile(texture_path):
                bump_map = texture_path
                break

    if shader.shader_body.map.name_length > 0:
        for extension in texture_extensions:
            texture_path = os.path.join(texture_root, "%s.%s" % (shader.shader_body.map.name, extension))
            if os.path.isfile(texture_path):
                self_illumination_map = texture_path
                break

    if shader.shader_body.reflection_cube_map.name_length > 0:
        for extension in texture_extensions:
            texture_path = os.path.join(texture_root, "%s.%s" % (shader.shader_body.reflection_cube_map.name, extension))
            if os.path.isfile(texture_path):
                reflection_cube_map = texture_path
                break

    rescale_detail = DiffuseFlags.rescale_detail_maps in DiffuseFlags(shader.shader_body.diffuse_flags)
    rescale_bump_maps = DiffuseFlags.rescale_bump_maps in DiffuseFlags(shader.shader_body.diffuse_flags)

    base_bitmap_count = 0
    primary_detail_bitmap_count = 0
    secondary_detail_bitmap_count = 0
    micro_detail_bitmap_count = 0
    bump_bitmap_count = 0
    if base_bitmap:
        base_bitmap_count = len(base_bitmap.bitmaps)
    if primary_detail_bitmap:
        primary_detail_bitmap_count = len(primary_detail_bitmap.bitmaps)
    if secondary_detail_bitmap:
        secondary_detail_bitmap_count = len(secondary_detail_bitmap.bitmaps)
    if micro_detail_bitmap:
        micro_detail_bitmap_count = len(micro_detail_bitmap.bitmaps)
    if bump_bitmap:
        bump_bitmap_count = len(bump_bitmap.bitmaps)

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    bdsf_principled.inputs[7].default_value = 0.0
    bdsf_principled.inputs[9].default_value = 1

    base_node = generate_image_node(mat, base_map)
    base_node.name = "Base Map"
    base_node.location = Vector((-2100, 475))
    if not base_node.image == None:
        base_node.image.alpha_mode = 'CHANNEL_PACKED'

    primary_detail_node = generate_image_node(mat, primary_detail_map)
    if not primary_detail_node.image == None:
        primary_detail_node.image.alpha_mode = 'CHANNEL_PACKED'

    primary_detail_node.name = "Primary Detail Map"
    primary_detail_node.location = Vector((-2100, 1350))

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-2275, 1250))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", primary_detail_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-2450, 1325))
    combine_xyz_node.location = Vector((-2450, 1175))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.shader_body.primary_detail_map_scale
    if shader.shader_body.primary_detail_map_scale == 0.0:
        scale = 1.0

    primary_detail_rescale_i = scale
    primary_detail_rescale_j = scale
    if base_bitmap_count > 0 and primary_detail_bitmap_count > 0 and rescale_detail:
        if base_bitmap_count > permutation_index:
            base_element = base_bitmap.bitmaps[permutation_index]
        else:
            base_element = base_bitmap.bitmaps[0]

        if primary_detail_bitmap_count > permutation_index:
            primary_detail_element = primary_detail_bitmap.bitmaps[permutation_index]
        else:
            primary_detail_element = primary_detail_bitmap.bitmaps[0]

        primary_detail_rescale_i *= base_element.width / primary_detail_element.width
        primary_detail_rescale_j *= base_element.height / primary_detail_element.height

    combine_xyz_node.inputs[0].default_value = primary_detail_rescale_i
    combine_xyz_node.inputs[1].default_value = primary_detail_rescale_j
    combine_xyz_node.inputs[2].default_value = 1

    secondary_detail_node = generate_image_node(mat, secondary_detail_map)
    if not secondary_detail_node.image == None:
        secondary_detail_node.image.alpha_mode = 'CHANNEL_PACKED'

    secondary_detail_node.name = "Secondary Detail Map"
    secondary_detail_node.location = Vector((-2100, 1050))

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-2275, 975))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", secondary_detail_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-2450, 1025))
    combine_xyz_node.location = Vector((-2450, 875))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.shader_body.secondary_detail_map_scale
    if shader.shader_body.secondary_detail_map_scale == 0.0:
        scale = 1.0

    secondary_detail_rescale_i = scale
    secondary_detail_rescale_j = scale
    if base_bitmap_count > 0 and secondary_detail_bitmap_count > 0 and rescale_detail:
        if base_bitmap_count > permutation_index:
            base_element = base_bitmap.bitmaps[permutation_index]
        else:
            base_element = base_bitmap.bitmaps[0]
        if secondary_detail_bitmap_count > permutation_index:
            secondary_detail_element = secondary_detail_bitmap.bitmaps[permutation_index]
        else:
            secondary_detail_element = secondary_detail_bitmap.bitmaps[0]

        secondary_detail_rescale_i *= base_element.width / secondary_detail_element.width
        secondary_detail_rescale_j *= base_element.height / secondary_detail_element.height

    combine_xyz_node.inputs[0].default_value = secondary_detail_rescale_i
    combine_xyz_node.inputs[1].default_value = secondary_detail_rescale_j
    combine_xyz_node.inputs[2].default_value = 1

    micro_detail_node = generate_image_node(mat, micro_detail_map)
    if not micro_detail_node.image == None:
        micro_detail_node.image.alpha_mode = 'CHANNEL_PACKED'

    micro_detail_node.name = "Micro Detail Map"
    micro_detail_node.location = Vector((-2100, 775))

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-2275, 675))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", micro_detail_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-2450, 725))
    combine_xyz_node.location = Vector((-2450, 575))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.shader_body.micro_detail_map_scale
    if shader.shader_body.micro_detail_map_scale == 0.0:
        scale = 1.0

    micro_detail_rescale_i = scale
    micro_detail_rescale_j = scale
    if base_bitmap_count > 0 and micro_detail_bitmap_count > 0 and rescale_detail:
        if base_bitmap_count > permutation_index:
            base_element = base_bitmap.bitmaps[permutation_index]
        else:
            base_element = base_bitmap.bitmaps[0]
        if micro_detail_bitmap_count > permutation_index:
            micro_detail_element = micro_detail_bitmap.bitmaps[permutation_index]
        else:
            micro_detail_element = micro_detail_bitmap.bitmaps[0]

        micro_detail_rescale_i *= base_element.width / micro_detail_element.width
        micro_detail_rescale_j *= base_element.height / micro_detail_element.height

    combine_xyz_node.inputs[0].default_value = micro_detail_rescale_i
    combine_xyz_node.inputs[1].default_value = micro_detail_rescale_j
    combine_xyz_node.inputs[2].default_value = 1

    bump_node = generate_image_node(mat, bump_map)
    if not bump_node.image == None:
        bump_node.image.colorspace_settings.name = 'Non-Color'

    bump_node.name = "Bump Map"
    bump_node.location = Vector((-700, -600))

    alpha_shader = EnvironmentFlags.alpha_tested in EnvironmentFlags(shader.shader_body.environment_flags)
    if alpha_shader:
        mat.shadow_method = 'CLIP'
        mat.blend_method = 'CLIP'

    mat.use_backface_culling = True

    connect_inputs(mat.node_tree, bump_node, "Alpha", bdsf_principled, "Alpha")

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-875, -800))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", bump_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    height_node = mat.node_tree.nodes.new("ShaderNodeBump")
    uv_map_node.location = Vector((-1075, -800))
    combine_xyz_node.location = Vector((-1075, -925))
    height_node.location = Vector((-425, -600))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)
    connect_inputs(mat.node_tree, bump_node, "Color", height_node, "Height")
    connect_inputs(mat.node_tree, height_node, "Normal", bdsf_principled, "Normal")

    if bump_bitmap:
        height_node.inputs[0].default_value = bump_bitmap.bitmap_body.bump_height

    scale = shader.shader_body.bump_map_scale
    if shader.shader_body.bump_map_scale == 0.0:
        scale = 1.0

    bump_rescale_i = scale
    bump_rescale_j = scale
    if base_bitmap_count > 0 and bump_bitmap_count > 0 and rescale_bump_maps:
        if base_bitmap_count > permutation_index:
            base_element = base_bitmap.bitmaps[permutation_index]
        else:
            base_element = base_bitmap.bitmaps[0]
        if bump_bitmap_count > permutation_index:
            bump_element = bump_bitmap.bitmaps[permutation_index]
        else:
            bump_element = bump_bitmap.bitmaps[0]

        bump_rescale_i *= base_element.width / bump_element.width
        bump_rescale_j *= base_element.height / bump_element.height

    combine_xyz_node.inputs[0].default_value = bump_rescale_i
    combine_xyz_node.inputs[1].default_value = bump_rescale_j
    combine_xyz_node.inputs[2].default_value = 1

    self_illumination_node = generate_image_node(mat, self_illumination_map)
    self_illumination_node.name = "Self Illumination Map"
    self_illumination_node.location = Vector((-2100.0, 1625.0))

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-2275, 1550))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", self_illumination_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-2450, 1625))
    combine_xyz_node.location = Vector((-2450, 1475))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.shader_body.map_scale
    if shader.shader_body.map_scale == 0.0:
        scale = 1.0

    combine_xyz_node.inputs[0].default_value = scale
    combine_xyz_node.inputs[1].default_value = scale
    combine_xyz_node.inputs[2].default_value = 1

    reflection_node = generate_image_node(mat, reflection_cube_map, True)
    reflection_node.name = "Reflection Map"
    reflection_node.location = Vector((-2100.0, 175.0))
    texture_coordinate_node = mat.node_tree.nodes.new("ShaderNodeTexCoord")
    texture_coordinate_node.location = Vector((-2275.0, 175.0))
    connect_inputs(mat.node_tree, texture_coordinate_node, "Reflection", reflection_node, "Vector")

    reflection_tint_node = generate_reflection_tint_logic_node(mat.node_tree)
    reflection_tint_node.location = Vector((-2000, -75.0))

    perpendicular_tint_node = mat.node_tree.nodes.new('ShaderNodeRGB')
    perpendicular_tint_node.outputs[0].default_value = shader.shader_body.perpendicular_color
    perpendicular_tint_node.location = Vector((-2175, -75.0))
    connect_inputs(mat.node_tree, perpendicular_tint_node, "Color", reflection_tint_node, "Perpendicular Tint")
    reflection_tint_node.inputs["Perpendicular Brightness"].default_value = shader.shader_body.perpendicular_brightness

    parallel_tint_node = mat.node_tree.nodes.new('ShaderNodeRGB')
    parallel_tint_node.outputs[0].default_value = shader.shader_body.parallel_color
    parallel_tint_node.location = Vector((-2175, -275.0))
    connect_inputs(mat.node_tree, parallel_tint_node, "Color", reflection_tint_node, "Parallel Tint")
    reflection_tint_node.inputs["Parallel Brightness"].default_value = shader.shader_body.parallel_brightness

    reflection_mix_node = mat.node_tree.nodes.new("ShaderNodeMix")
    reflection_mix_node.data_type = 'RGBA'
    reflection_mix_node.blend_type = "MULTIPLY"
    reflection_mix_node.clamp_result = True
    reflection_mix_node.inputs[0].default_value = 1
    reflection_mix_node.location = Vector((-1825, -75.0))
    connect_inputs(mat.node_tree, reflection_tint_node, "Color", reflection_mix_node, 6)
    connect_inputs(mat.node_tree, reflection_node, "Color", reflection_mix_node, 7)

    base_mix_node = mat.node_tree.nodes.new("ShaderNodeMix")
    base_mix_node.data_type = 'RGBA'
    base_mix_node.blend_type = "MULTIPLY"
    base_mix_node.clamp_result = True
    base_mix_node.inputs[0].default_value = 1
    base_mix_node.location = Vector((-1650.0, -75.0))
    connect_inputs(mat.node_tree, base_node, "Alpha", base_mix_node, 6)
    connect_inputs(mat.node_tree, reflection_mix_node, 2, base_mix_node, 7)

    if shader.shader_body.environment_type == EnvironmentTypeEnum.normal.value:
        blend_mix_node = mat.node_tree.nodes.new("ShaderNodeMix")
        blend_mix_node.data_type = 'RGBA'
        blend_mix_node.blend_type = "ADD"
        blend_mix_node.clamp_result = True
        blend_mix_node.inputs[0].default_value = 1
        blend_mix_node.location = Vector((-1475.0, -75.0))
        connect_inputs(mat.node_tree, base_mix_node, 2, blend_mix_node, 6)
        connect_inputs(mat.node_tree, base_node, "Color", blend_mix_node, 7)

        blend_biased_multiply_node = generate_biased_multiply_node(mat.node_tree)
        blend_biased_multiply_node.location = Vector((-1300, -75))
        connect_inputs(mat.node_tree, blend_mix_node, 2, blend_biased_multiply_node, "Color")
        connect_inputs(mat.node_tree, micro_detail_node, "Color", blend_biased_multiply_node, "Detail")
        blend_biased_multiply_node.inputs[2].default_value = (1, 1, 1, 1)

        blend_multiply_a_node = generate_multiply_node(mat.node_tree)
        blend_multiply_a_node.location = Vector((-1125, -75))
        connect_inputs(mat.node_tree, blend_biased_multiply_node, "Color", blend_multiply_a_node, "Color")
        connect_inputs(mat.node_tree, secondary_detail_node, "Color", blend_multiply_a_node, "Detail")
        blend_multiply_a_node.inputs[2].default_value = (1, 1, 1, 1)

        blend_multiply_b_node = generate_multiply_node(mat.node_tree)
        blend_multiply_b_node.location = Vector((-950, -75))
        connect_inputs(mat.node_tree, blend_multiply_a_node, "Color", blend_multiply_b_node, "Color")
        connect_inputs(mat.node_tree, primary_detail_node, "Color", blend_multiply_b_node, "Detail")
        connect_inputs(mat.node_tree, blend_multiply_b_node, "Color", bdsf_principled, "Base Color")
        blend_multiply_b_node.inputs[2].default_value = (1, 1, 1, 1)

    elif shader.shader_body.environment_type == EnvironmentTypeEnum.blended.value:
        blend_mix_node = mat.node_tree.nodes.new("ShaderNodeMix")
        blend_mix_node.data_type = 'RGBA'
        blend_mix_node.blend_type = "ADD"
        blend_mix_node.clamp_result = True
        blend_mix_node.inputs[0].default_value = 1
        blend_mix_node.location = Vector((-775.0, -240.0))
        connect_inputs(mat.node_tree, base_mix_node, 2, blend_mix_node, 6)
        connect_inputs(mat.node_tree, base_node, "Color", blend_mix_node, 7)

        blend_detail_mix_node = mat.node_tree.nodes.new("ShaderNodeMix")
        blend_detail_mix_node.data_type = 'RGBA'
        blend_detail_mix_node.blend_type = "MIX"
        blend_detail_mix_node.clamp_result = True
        blend_detail_mix_node.inputs[0].default_value = 1
        blend_detail_mix_node.location = Vector((-775.0, -240.0))
        connect_inputs(mat.node_tree, base_node, "Alpha", blend_detail_mix_node, 0)
        connect_inputs(mat.node_tree, secondary_detail_node, "Color", blend_detail_mix_node, 6)
        connect_inputs(mat.node_tree, primary_detail_node, "Color", blend_detail_mix_node, 7)

        blend_biased_multiply_node = generate_biased_multiply_node(mat.node_tree)
        blend_biased_multiply_node.inputs[2].default_value = (1, 1, 1, 1)
        connect_inputs(mat.node_tree, blend_mix_node, 2, blend_biased_multiply_node, "Color")
        connect_inputs(mat.node_tree, blend_detail_mix_node, 2, blend_biased_multiply_node, "Detail")
        connect_inputs(mat.node_tree, blend_biased_multiply_node, "Color", bdsf_principled, "Base Color")

    elif shader.shader_body.blended_base_specular == EnvironmentTypeEnum.blended_base_specular.value:
        blend_mix_node = mat.node_tree.nodes.new("ShaderNodeMix")
        blend_mix_node.data_type = 'RGBA'
        blend_mix_node.blend_type = "ADD"
        blend_mix_node.clamp_result = True
        blend_mix_node.inputs[0].default_value = 1
        blend_mix_node.location = Vector((-775.0, -240.0))
        connect_inputs(mat.node_tree, base_mix_node, 2, blend_mix_node, 6)
        connect_inputs(mat.node_tree, base_node, "Color", blend_mix_node, 7)

        blend_detail_mix_node = mat.node_tree.nodes.new("ShaderNodeMix")
        blend_detail_mix_node.data_type = 'RGBA'
        blend_detail_mix_node.blend_type = "MIX"
        blend_detail_mix_node.clamp_result = True
        blend_detail_mix_node.inputs[0].default_value = 1
        blend_detail_mix_node.location = Vector((-775.0, -240.0))
        connect_inputs(mat.node_tree, base_node, "Alpha", blend_detail_mix_node, 0)
        connect_inputs(mat.node_tree, secondary_detail_node, "Color", blend_detail_mix_node, 6)
        connect_inputs(mat.node_tree, primary_detail_node, "Color", blend_detail_mix_node, 7)

        blend_biased_multiply_node = generate_biased_multiply_node(mat.node_tree)
        blend_biased_multiply_node.inputs[2].default_value = (1, 1, 1, 1)
        connect_inputs(mat.node_tree, blend_mix_node, 2, blend_biased_multiply_node, "Color")
        connect_inputs(mat.node_tree, blend_detail_mix_node, 2, blend_biased_multiply_node, "Detail")
        connect_inputs(mat.node_tree, blend_biased_multiply_node, "Color", bdsf_principled, "Base Color")

    is_mirror_node = mat.node_tree.nodes.new("ShaderNodeValue")
    is_mirror_node.location = Vector((-950, -475))
    is_mirror_node.outputs[0].default_value = ReflectionFlags.dynamic_mirror in ReflectionFlags(shader.shader_body.reflection_flags)

    greater_than_node = mat.node_tree.nodes.new("ShaderNodeMath")
    greater_than_node.operation = 'GREATER_THAN'
    greater_than_node.use_clamp = True
    greater_than_node.inputs[1].default_value = 0
    greater_than_node.location = Vector((-775, -225))
    connect_inputs(mat.node_tree, is_mirror_node, "Value", greater_than_node, "Value")

    less_than_node = mat.node_tree.nodes.new("ShaderNodeMath")
    less_than_node.operation = 'LESS_THAN'
    less_than_node.use_clamp = True
    less_than_node.inputs[1].default_value = 1
    less_than_node.location = Vector((-600, -400))
    connect_inputs(mat.node_tree, is_mirror_node, "Value", less_than_node, "Value")

    subtract_node = mat.node_tree.nodes.new("ShaderNodeMath")
    subtract_node.operation = 'SUBTRACT'
    subtract_node.use_clamp = True
    subtract_node.inputs[0].default_value = 1
    subtract_node.location = Vector((-600, -225))
    connect_inputs(mat.node_tree, greater_than_node, "Value", subtract_node, 1)

    add_node = mat.node_tree.nodes.new("ShaderNodeMath")
    add_node.operation = 'ADD'
    add_node.use_clamp = True
    add_node.inputs[1].default_value = 1
    add_node.location = Vector((-425, -400))
    connect_inputs(mat.node_tree, less_than_node, "Value", add_node, 0)
    connect_inputs(mat.node_tree, subtract_node, "Value", add_node, 1)
    connect_inputs(mat.node_tree, greater_than_node, "Value", bdsf_principled, "Metallic")
    connect_inputs(mat.node_tree, add_node, "Value", bdsf_principled, "Roughness")

def generate_shader_transparent_meter(mat, shader, tag_format, report):
    mat.use_nodes = True

    texture_root = config.HALO_1_DATA_PATH
    meter_map = None
    texture_extensions = ("tif", "tiff")

    if shader.shader_body.meter_map.name_length > 0:
        for extension in texture_extensions:
            texture_path = os.path.join(texture_root, "%s.%s" % (shader.shader_body.meter_map.name, extension))
            if os.path.isfile(texture_path):
                meter_map = texture_path
                break

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))

    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    mat.node_tree.nodes.remove(bdsf_principled)

    shader_mix_node = mat.node_tree.nodes.new("ShaderNodeMixShader")
    shader_mix_node.location = Vector((-175, 0))
    connect_inputs(mat.node_tree, shader_mix_node, "Shader", output_material_node, "Surface")

    invert_node = mat.node_tree.nodes.new("ShaderNodeInvert")
    emission_node = mat.node_tree.nodes.new("ShaderNodeEmission")
    bsdf_transparent_node = mat.node_tree.nodes.new("ShaderNodeBsdfTransparent")
    invert_node.location = Vector((-350, 125))
    emission_node.location = Vector((-350, 0))
    bsdf_transparent_node.location = Vector((-350, -125))
    invert_node.inputs[0].default_value = 1
    connect_inputs(mat.node_tree, invert_node, "Color", shader_mix_node, 0)
    connect_inputs(mat.node_tree, emission_node, "Emission", shader_mix_node, 1)
    connect_inputs(mat.node_tree, bsdf_transparent_node, "BSDF", shader_mix_node, 2)

    gamma_node = mat.node_tree.nodes.new("ShaderNodeGamma")
    gamma_node.location = Vector((-525, -125))
    gamma_node.inputs[1].default_value = 2.2

    meter_node = generate_image_node(mat, meter_map)
    meter_node.image.alpha_mode = 'CHANNEL_PACKED'
    meter_node.location = Vector((-650, 175))
    connect_inputs(mat.node_tree, gamma_node, "Color", emission_node, "Color")
    connect_inputs(mat.node_tree, meter_node, "Alpha", emission_node, "Strength")
    connect_inputs(mat.node_tree, meter_node, "Alpha", invert_node, "Color")

    rgb_node = mat.node_tree.nodes.new("ShaderNodeRGB")
    rgb_node.location = Vector((-725, -125))
    rgb_node.outputs[0].default_value = shader.shader_body.background_color
    connect_inputs(mat.node_tree, rgb_node, "Color", gamma_node, "Color")

    mat.blend_method = 'BLEND'

def generate_shader_transparent_glass(mat, shader, tag_format, report):
    mat.use_nodes = True

    texture_root = config.HALO_1_DATA_PATH
    background_tint_map = None
    reflection_map = None
    bump_map = None
    diffuse_map = None
    diffuse_detail_map = None
    specular_map = None
    specular_detail_map = None
    texture_extensions = ("tif", "tiff")

    diffuse_bitmap = shader.shader_body.diffuse_map.parse_tag(tag_format, report, "halo1", "retail")
    bump_bitmap = shader.shader_body.bump_map.parse_tag(tag_format, report, "halo1", "retail")
    if shader.shader_body.background_tint_map.name_length > 0:
        for extension in texture_extensions:
            texture_path = os.path.join(texture_root, "%s.%s" % (shader.shader_body.background_tint_map.name, extension))
            if os.path.isfile(texture_path):
                background_tint_map = texture_path
                break

    if shader.shader_body.reflection_map.name_length > 0:
        for extension in texture_extensions:
            texture_path = os.path.join(texture_root, "%s.%s" % (shader.shader_body.reflection_map.name, extension))
            if os.path.isfile(texture_path):
                reflection_map = texture_path
                break

    if shader.shader_body.bump_map.name_length > 0:
        for extension in texture_extensions:
            texture_path = os.path.join(texture_root, "%s.%s" % (shader.shader_body.bump_map.name, extension))
            if os.path.isfile(texture_path):
                bump_map = texture_path
                break

    if shader.shader_body.diffuse_map.name_length > 0:
        for extension in texture_extensions:
            texture_path = os.path.join(texture_root, "%s.%s" % (shader.shader_body.diffuse_map.name, extension))
            if os.path.isfile(texture_path):
                diffuse_map = texture_path
                break

    if shader.shader_body.diffuse_detail_map.name_length > 0:
        for extension in texture_extensions:
            texture_path = os.path.join(texture_root, "%s.%s" % (shader.shader_body.diffuse_detail_map.name, extension))
            if os.path.isfile(texture_path):
                diffuse_detail_map = texture_path
                break

    if shader.shader_body.specular_map.name_length > 0:
        for extension in texture_extensions:
            texture_path = os.path.join(texture_root, "%s.%s" % (shader.shader_body.specular_map.name, extension))
            if os.path.isfile(texture_path):
                specular_map = texture_path
                break

    if shader.shader_body.specular_detail_map.name_length > 0:
        for extension in texture_extensions:
            texture_path = os.path.join(texture_root, "%s.%s" % (shader.shader_body.specular_detail_map.name, extension))
            if os.path.isfile(texture_path):
                specular_detail_map = texture_path
                break

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    background_tint_node = generate_image_node(mat, background_tint_map)
    reflection_node = generate_image_node(mat, reflection_map)
    bump_node = generate_image_node(mat, bump_map)

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-875, -800))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", bump_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    height_node = mat.node_tree.nodes.new("ShaderNodeBump")
    uv_map_node.location = Vector((-1075, -800))
    combine_xyz_node.location = Vector((-1075, -925))
    height_node.location = Vector((-425, -600))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)
    connect_inputs(mat.node_tree, bump_node, "Color", height_node, "Height")
    connect_inputs(mat.node_tree, height_node, "Normal", bdsf_principled, "Normal")

    if bump_bitmap:
        height_node.inputs[0].default_value = bump_bitmap.bitmap_body.bump_height

    scale = shader.shader_body.bump_map_scale
    if shader.shader_body.bump_map_scale == 0.0:
        scale = 1.0

    combine_xyz_node.inputs[0].default_value = scale
    combine_xyz_node.inputs[1].default_value = scale
    combine_xyz_node.inputs[2].default_value = 1

    diffuse_node = generate_image_node(mat, diffuse_map)

    connect_inputs(mat.node_tree, diffuse_node, "Color", bdsf_principled, "Base Color")

    if diffuse_bitmap:
        ignore_alpha_bitmap = diffuse_bitmap.bitmap_body.format is FormatEnum.compressed_with_color_key_transparency.value
        if ignore_alpha_bitmap:
            diffuse_node.image.alpha_mode = 'NONE'
        else:
            connect_inputs(mat.node_tree, diffuse_node, "Alpha", bdsf_principled, "Alpha")
            mat.shadow_method = 'CLIP'
            mat.blend_method = 'BLEND'

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-2275, 1250))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", diffuse_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-2450, 1325))
    combine_xyz_node.location = Vector((-2450, 1175))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.shader_body.diffuse_map_scale
    if shader.shader_body.diffuse_map_scale == 0.0:
        scale = 1.0

    combine_xyz_node.inputs[0].default_value = scale
    combine_xyz_node.inputs[1].default_value = scale
    combine_xyz_node.inputs[2].default_value = 1

    diffuse_detail_node = generate_image_node(mat, diffuse_detail_map)

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-2275, 1250))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", diffuse_detail_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-2450, 1325))
    combine_xyz_node.location = Vector((-2450, 1175))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.shader_body.diffuse_detail_map_scale
    if shader.shader_body.diffuse_detail_map_scale == 0.0:
        scale = 1.0

    combine_xyz_node.inputs[0].default_value = scale
    combine_xyz_node.inputs[1].default_value = scale
    combine_xyz_node.inputs[2].default_value = 1

    specular_node = generate_image_node(mat, specular_map)

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-2275, 1250))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", specular_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-2450, 1325))
    combine_xyz_node.location = Vector((-2450, 1175))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.shader_body.specular_map_scale
    if shader.shader_body.specular_map_scale == 0.0:
        scale = 1.0

    combine_xyz_node.inputs[0].default_value = scale
    combine_xyz_node.inputs[1].default_value = scale
    combine_xyz_node.inputs[2].default_value = 1

    specular_detail_node = generate_image_node(mat, specular_detail_map)

    vect_math_node = mat.node_tree.nodes.new("ShaderNodeVectorMath")
    vect_math_node.operation = 'MULTIPLY'
    vect_math_node.location = Vector((-2275, 1250))

    connect_inputs(mat.node_tree, vect_math_node, "Vector", specular_detail_node, "Vector")

    uv_map_node = mat.node_tree.nodes.new("ShaderNodeUVMap")
    combine_xyz_node = mat.node_tree.nodes.new("ShaderNodeCombineXYZ")
    uv_map_node.location = Vector((-2450, 1325))
    combine_xyz_node.location = Vector((-2450, 1175))
    connect_inputs(mat.node_tree, uv_map_node, "UV", vect_math_node, 0)
    connect_inputs(mat.node_tree, combine_xyz_node, "Vector", vect_math_node, 1)

    scale = shader.shader_body.specular_detail_map_scale
    if shader.shader_body.specular_detail_map_scale == 0.0:
        scale = 1.0

    combine_xyz_node.inputs[0].default_value = scale
    combine_xyz_node.inputs[1].default_value = scale
    combine_xyz_node.inputs[2].default_value = 1

def generate_shader(mat, tag_ref, shader_permutation_index, tag_format, report):
    shader = tag_ref.parse_tag(tag_format, report, "halo1", "retail")
    if not shader == None:
        if shader.header.tag_group == "soso":
            generate_shader_model(mat, shader, tag_format, report)
        elif shader.header.tag_group == "senv":
            generate_shader_environment(mat, shader, shader_permutation_index, tag_format, report)
        elif shader.header.tag_group == "smet":
            generate_shader_transparent_meter(mat, shader, tag_format, report)
        elif shader.header.tag_group == "sgla":
            generate_shader_transparent_glass(mat, shader, tag_format, report)
