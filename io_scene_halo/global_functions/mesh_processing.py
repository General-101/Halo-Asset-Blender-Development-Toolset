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
import bpy
import bmesh
import struct

from math import radians
from mathutils import Vector, Matrix
from ..global_functions import global_functions, mesh_processing

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
            permutation_element = region_element[marker_obj.permutation_index]
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

            if not material_name in object_data.materials.keys():
                object_data.materials.append(mat)

            mat.diffuse_color = random_color_gen.next()
            material_index = object_data.materials.keys().index(material_name)
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

def process_mesh_export_color(layer_color, loop_index, vertex_index):
    color = (0.0, 0.0, 0.0)
    if not layer_color == None:
        if layer_color.domain == "POINT":
            color = layer_color.data[vertex_index].color
        else:
            color = layer_color.data[loop_index].color

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
