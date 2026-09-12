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

import os
import bpy
import bmesh
import numpy as np

from io import TextIOWrapper
from math import radians
from mathutils import Vector, Matrix, Quaternion, Euler
from ..file_tag.tag_interface.tag_definitions import h1, h2
from ..file_tag.tag_interface import tag_interface, tag_common
from ..global_functions import mesh_processing, global_functions, shader_processing
from .format import JMSAsset

class Node:
    def __init__(self, name="", children=None, child=-1, sibling=-1, parent=-1, rotation=Quaternion(), translation=Vector()):
        self.name = name
        self.children = children
        self.child = child
        self.sibling = sibling
        self.parent = parent
        self.rotation = rotation
        self.translation = translation
        self.visited = False

def skip_checksum_8197(JMS):
    JMS.next()

def get_child_nodes(jms_version, node_data, node_idx):
    child_list = []
    current_node = node_data[node_idx]
    for child_idx, node in enumerate(node_data):
        child_node = node_data[child_idx]
        if node.parent == node_idx:
            child_distance = (Vector((0, 0, 0)) - child_node.translation).length
            if jms_version >= global_functions.get_version_matrix_check("JMS"):
                child_distance = (current_node.translation - child_node.translation).length

            child_list.append(child_distance)

    return child_list

def get_bone_distance(jms_version, node_data, node_idx):
    bone_distance = 0

    child_list = get_child_nodes(jms_version, node_data, node_idx)
    current_node = node_data[node_idx]
    if len(child_list) == 0 and current_node.parent and not current_node.parent == -1:
        bone_distance = (Vector((0, 0, 0)) - current_node.translation).length
        if jms_version >= global_functions.get_version_matrix_check("JMS"):
            bone_distance = (node_data[current_node.parent].translation - current_node.translation).length

    elif len(child_list) == 1:
        bone_distance = child_list[0]

    elif len(child_list) > 1:
        bone_distance = sum(child_list) / len(child_list)

    if bone_distance < 1.0:
        bone_distance = 1

    return bone_distance

def process_node_tree_h1_era(node_data):
    node_count = len(node_data)
    for node_idx in range(node_count):
        node = node_data[node_idx]
        if node.child == -1:
            continue # no child nodes, nothing to update

        if node.child >= node_count or node.child == node_idx:
            raise global_functions.ParseError("Malformed node graph (bad child index)")

        child_node = node_data[node.child]
        while child_node != None:
            child_node.parent = node_idx
            if child_node.visited:
                raise global_functions.ParseError("Malformed node graph (circular reference)")

            child_node.visited = True
            if child_node.sibling >= node_count:
                raise global_functions.ParseError("Malformed node graph (sibling index out of range)")

            if child_node.sibling != -1:
                child_node = node_data[child_node.sibling]

            else:
                child_node = None

def process_node_tree_h2_era(node_data):
    node_count = len(node_data)
    for node_idx in range(node_count):
        node = node_data[node_idx]
        if node.parent == -1:
            continue # this is a root node, nothing to update

        if node.parent >= node_count or node.parent == node_idx:
            raise global_functions.ParseError("Malformed node graph (bad parent index)")

        parent_node = node_data[node.parent]
        if parent_node.child:
            node.sibling = parent_node.child

        else:
            node.sibling = -1

        if node.sibling >= node_count:
            raise global_functions.ParseError("Malformed node graph (sibling index out of range)")

        parent_node.child = node_idx

def read_nodes_8197(JMS, armature, node_names, jms_version, fix_rotations, valid_armature):
    bpy.ops.object.mode_set(mode = 'EDIT')
    node_count = int(JMS.next())
    node_data = []
    for node_idx in range(node_count):
        node_element = Node()
        node_element.name = JMS.next()
        node_element.child = int(JMS.next())
        node_element.sibling = int(JMS.next())
        node_element.rotation = JMS.next_quaternion()
        node_element.translation = JMS.next_vector()
        node_data.append(node_element)

    process_node_tree_h1_era(node_data)
    if not valid_armature:
        for node_element in node_data:
            current_bone = armature.data.edit_bones.new(node_element.name)
            current_bone.tail[2] = get_bone_distance(jms_version, node_data, node_idx)
            current_bone.parent = armature.data.edit_bones[node_element.parent]

            matrix_translate = Matrix.Translation(node_element.translation)
            matrix_rotation = node_element.rotation.to_matrix().to_4x4()

            transform_matrix = matrix_translate @ matrix_rotation
            if fix_rotations:
                if jms_version < 8205 and current_bone.parent:
                    transform_matrix = (current_bone.parent.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix

                current_bone.matrix = transform_matrix @ Matrix.Rotation(radians(-90.0), 4, 'Z')

            else:
                if jms_version < 8205 and current_bone.parent:
                    transform_matrix = current_bone.parent.matrix @ transform_matrix

                current_bone.matrix = transform_matrix

            node_names.append(current_bone.name)
    else:
        node_name_set = set()
        for node_idx, node_element in enumerate(node_data):
            node_name = node_element.name
            if node_element.name not in node_name_set:
                current_name = node_name
            else:
                i = 1
                while f"{node_name}.{i:03d}" in node_name_set:
                    i += 1

                current_name = f"{node_name}.{i:03d}"

            node_name_set.add(current_name)
            node_names.append(current_name)

    bpy.ops.object.mode_set(mode = 'OBJECT')

def read_nodes_8205(JMS, armature, node_names, jms_version, fix_rotations, valid_armature):
    bpy.ops.object.mode_set(mode = 'EDIT')
    node_count = int(JMS.next())
    node_data = []
    for node_idx in range(node_count):
        node_element = Node()
        node_element.name = JMS.next()
        node_element.parent = int(JMS.next())
        node_element.rotation = JMS.next_quaternion()
        node_element.translation = JMS.next_vector()
        node_data.append(node_element)

    process_node_tree_h2_era(node_data)
    if not valid_armature:
        for node_idx, node_element in enumerate(node_data):
            current_bone = armature.data.edit_bones.new(node_element.name)
            current_bone.tail[2] = get_bone_distance(jms_version, node_data, node_idx)
            current_bone.parent = armature.data.edit_bones[node_element.parent]

            matrix_translate = Matrix.Translation(node_element.translation)
            matrix_rotation = node_element.rotation.to_matrix().to_4x4()

            transform_matrix = matrix_translate @ matrix_rotation
            if fix_rotations:
                transform_matrix @= Matrix.Rotation(radians(-90.0), 4, 'Z')

            current_bone.matrix = transform_matrix

            node_names.append(current_bone.name)
    else:
        node_name_set = set()
        for node_idx, node_element in enumerate(node_data):
            node_name = node_element.name
            if node_element.name not in node_name_set:
                current_name = node_name
            else:
                i = 1
                while f"{node_name}.{i:03d}" in node_name_set:
                    i += 1

                current_name = f"{node_name}.{i:03d}"

            node_name_set.add(current_name)
            node_names.append(current_name)

    bpy.ops.object.mode_set(mode = 'OBJECT')

def unpack_material_definition_h1_era(material_definition, default_region, default_permutation, sections, section_map, material_idx):
    return None
    
def unpack_material_definition_h2_era(material_definition, default_region, default_permutation, sections, section_map, material_idx):
    lod, permutation, region = global_functions.material_definition_parser(material_definition.split(), default_region, default_permutation)

    section_name = ""
    if lod != None:
        section_name = lod
    if permutation != None:
        if len(section_name) > 0:
            section_name += " " 

        section_name += permutation

    if region != None:
        if len(section_name) > 0:
            section_name += " " 

        section_name += region

    if section_name in sections:
        map_id = sections.index(section_name)
    else:
        sections.append(section_name) 
        map_id = len(sections) - 1

    section_map[material_idx] = map_id

    return None

def read_materials_8197(JMS, game_title, materials, sections, section_map, triangle_material_map, random_color_gen, filepath, shader_gen_setting, report):
    material_names = []
    shader_tag_refs = []

    default_region = mesh_processing.get_default_region_permutation_name(game_title)
    default_permutation = mesh_processing.get_default_region_permutation_name(game_title)

    unpack_material_definition = unpack_material_definition_h1_era
    if game_title != "halo1":
        unpack_material_definition = unpack_material_definition_h2_era

    material_count = int(JMS.next())
    for material_idx in range(material_count):
        shader_tag_ref = None

        material_name = JMS.next()
        material_definition = JMS.next()
        unpack_material_definition(material_definition, default_region, default_permutation, sections, section_map, material_idx)

        if material_name in material_names:
            map_id = material_names.index(material_name)
        else:
            material_names.append(material_name)
            material = bpy.data.materials.new(name=material_name)
            material.diffuse_color = random_color_gen.next()
            materials.append(material)
            map_id = len(materials) - 1

            if not shader_gen_setting == 0:
                if game_title == "halo1":
                    shader_tag_ref = shader_processing.find_h1_shader_tag(filepath, material_name)

                elif game_title == "halo2":
                    shader_tag_ref = shader_processing.find_h2_shader_tag(filepath, material_name)

                elif game_title == "halo3":
                    shader_tag_ref = shader_processing.find_h3_shader_tag(filepath, material_name)

            shader_tag_refs.append(shader_tag_ref)

        triangle_material_map[material_idx] = map_id

    if not shader_gen_setting == 0:
        asset_cache = {}
        if not game_title == "halo3":
            tag_groups = None
            engine_tag = None
            merged_defs = None
            if game_title == "halo1":
                output_dir = os.path.join(os.path.dirname(tag_common.h1_defs_directory), "h1_merged_output")
                tag_groups = tag_common.h1_tag_groups
                engine_tag = tag_common.EngineTag.H1Latest.value
                merged_defs = h1.generate_defs(tag_common.h1_defs_directory, output_dir)
                tag_directory = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_tag_path
                
            elif game_title == "halo2":
                output_dir = os.path.join(os.path.dirname(tag_common.h1_defs_directory), "h2_merged_output")
                tag_groups = tag_common.h2_tag_groups
                engine_tag = tag_common.EngineTag.H2Latest.value
                merged_defs = h2.generate_defs(tag_common.h2_defs_directory, output_dir)
                tag_directory = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_tag_path
            else:
                print("%s is not supported." % game_title)

            for shader_tag_ref in shader_tag_refs:
                if shader_tag_ref is not None:
                    tag_interface.generate_tag_dictionary(game_title, shader_tag_ref, tag_directory, tag_groups, engine_tag, merged_defs, asset_cache)

        for shader_idx, shader_tag_ref in enumerate(shader_tag_refs):
            asset_material_name = material_names[shader_idx]
            material_element = materials[shader_idx]
            shader_group = ""
            shader_name = ""
            if shader_tag_ref is not None:
                shader_group = shader_tag_ref["group name"]
                shader_name = shader_tag_ref["path"]

            permutation = 0
            if game_title == "halo1":
                material_name, permutation = mesh_processing.get_shader_permutation(asset_material_name)

            if not game_title == "halo3":
                SHAD_ASSET = asset_cache.get(shader_group, {}).get(shader_name) 
                if SHAD_ASSET:
                    material_name = material_element.name
                    cached_material = SHAD_ASSET["blender_assets"].get(material_name)
                    if cached_material is None:
                        SHAD_ASSET["blender_assets"][material_name] = material_element
                        if game_title == "halo1":
                            shader_processing.generate_h1_shader(shader_gen_setting, material_element, shader_tag_ref, permutation, asset_cache, report)

                        elif game_title == "halo2":
                            shader_processing.generate_h2_shader(shader_gen_setting, material_element, shader_tag_ref, asset_cache, report)

            else:
                if shader_tag_ref is not None:
                    shader_processing.generate_h3_shader(shader_gen_setting, material_element, shader_tag_ref, asset_cache, report)

def read_materials_8202(JMS, game_title, materials, sections, section_map, triangle_material_map, random_color_gen, filepath, shader_gen_setting, report):
    material_names = []
    shader_tag_refs = []

    default_region = mesh_processing.get_default_region_permutation_name(game_title)
    default_permutation = mesh_processing.get_default_region_permutation_name(game_title)

    unpack_material_definition = unpack_material_definition_h1_era
    if game_title != "halo1":
        unpack_material_definition = unpack_material_definition_h2_era

    material_count = int(JMS.next())
    for material_idx in range(material_count):
        shader_tag_ref = None

        material_name = JMS.next()
        texture_definition = JMS.next()
        material_definition = JMS.next()
        unpack_material_definition(material_definition, default_region, default_permutation, sections, section_map, material_idx)

        if material_name in material_names:
            map_id = material_names.index(material_name)
        else:
            material_names.append(material_name)
            material = bpy.data.materials.new(name=material_name)
            material.diffuse_color = random_color_gen.next()
            materials.append(material)
            map_id = len(materials) - 1

            if not shader_gen_setting == 0:
                if game_title == "halo1":
                    shader_tag_ref = shader_processing.find_h1_shader_tag(filepath, material_name)

                elif game_title == "halo2":
                    shader_tag_ref = shader_processing.find_h2_shader_tag(filepath, material_name)

                elif game_title == "halo3":
                    shader_tag_ref = shader_processing.find_h3_shader_tag(filepath, material_name)

            shader_tag_refs.append(shader_tag_ref)

        triangle_material_map[material_idx] = map_id

    if not shader_gen_setting == 0:
        asset_cache = {}
        if not game_title == "halo3":
            tag_groups = None
            engine_tag = None
            merged_defs = None
            if game_title == "halo1":
                output_dir = os.path.join(os.path.dirname(tag_common.h1_defs_directory), "h1_merged_output")
                tag_groups = tag_common.h1_tag_groups
                engine_tag = tag_common.EngineTag.H1Latest.value
                merged_defs = h1.generate_defs(tag_common.h1_defs_directory, output_dir)
                tag_directory = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_tag_path
                
            elif game_title == "halo2":
                output_dir = os.path.join(os.path.dirname(tag_common.h1_defs_directory), "h2_merged_output")
                tag_groups = tag_common.h2_tag_groups
                engine_tag = tag_common.EngineTag.H2Latest.value
                merged_defs = h2.generate_defs(tag_common.h2_defs_directory, output_dir)
                tag_directory = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_tag_path
            else:
                print("%s is not supported." % game_title)

            for shader_tag_ref in shader_tag_refs:
                if shader_tag_ref is not None:
                    tag_interface.generate_tag_dictionary(game_title, shader_tag_ref, tag_directory, tag_groups, engine_tag, merged_defs, asset_cache)

        for shader_idx, shader_tag_ref in enumerate(shader_tag_refs):
            asset_material_name = material_names[shader_idx]
            material_element = materials[shader_idx]
            shader_group = ""
            shader_name = ""
            if shader_tag_ref is not None:
                shader_group = shader_tag_ref["group name"]
                shader_name = shader_tag_ref["path"]

            permutation = 0
            if game_title == "halo1":
                material_name, permutation = mesh_processing.get_shader_permutation(asset_material_name)

            if not game_title == "halo3":
                SHAD_ASSET = asset_cache.get(shader_group, {}).get(shader_name) 
                if SHAD_ASSET:
                    material_name = material_element.name
                    cached_material = SHAD_ASSET["blender_assets"].get(material_name)
                    if cached_material is None:
                        SHAD_ASSET["blender_assets"][material_name] = material_element
                        if game_title == "halo1":
                            shader_processing.generate_h1_shader(shader_gen_setting, material_element, shader_tag_ref, permutation, asset_cache, report)

                        elif game_title == "halo2":
                            shader_processing.generate_h2_shader(shader_gen_setting, material_element, shader_tag_ref, asset_cache, report)

            else:
                if shader_tag_ref is not None:
                    shader_processing.generate_h3_shader(shader_gen_setting, material_element, shader_tag_ref, asset_cache, report)

def read_markers_8197(JMS, context, game_title, armature, node_names, fix_rotations):
    marker_count = int(JMS.next())
    marker_data = []
    for marker_idx in range(marker_count):
        marker_name = JMS.next()
        marker_parent = int(JMS.next())
        marker_rotation = JMS.next_quaternion()
        marker_translation = JMS.next_vector()

        build_markers(armature, context, node_names, game_title, fix_rotations, marker_data, marker_name, marker_parent, marker_rotation, marker_translation)

    return marker_data

def read_markers_8198(JMS, context, game_title, armature, node_names, fix_rotations):
    marker_count = int(JMS.next())
    marker_data = []
    for marker_idx in range(marker_count):
        marker_name = JMS.next()
        marker_region = int(JMS.next())
        marker_parent = int(JMS.next())
        marker_rotation = JMS.next_quaternion()
        marker_translation = JMS.next_vector()

        build_markers(armature, context, node_names, game_title, fix_rotations, marker_data, marker_name, marker_parent, marker_rotation, marker_translation, marker_region=marker_region)

    return marker_data

def read_markers_8200(JMS, context, game_title, armature, node_names, fix_rotations):
    marker_count = int(JMS.next())
    marker_data = []
    for marker_idx in range(marker_count):
        marker_name = JMS.next()
        marker_region = int(JMS.next())
        marker_parent = int(JMS.next())
        marker_rotation = JMS.next_quaternion()
        marker_translation = JMS.next_vector()
        marker_radius = float(JMS.next())

        build_markers(armature, context, node_names, game_title, fix_rotations, marker_data, marker_name, marker_parent, marker_rotation, marker_translation, marker_radius, marker_region)

    return marker_data

def read_markers_8206(JMS, context, game_title, armature, node_names, fix_rotations):
    marker_count = int(JMS.next())
    marker_data = []
    for marker_idx in range(marker_count):
        marker_name = JMS.next()
        marker_parent = int(JMS.next())
        marker_rotation = JMS.next_quaternion()
        marker_translation = JMS.next_vector()
        marker_radius = float(JMS.next())

        build_markers(armature, context, node_names, game_title, fix_rotations, marker_data, marker_name, marker_parent, marker_rotation, marker_translation, marker_radius)

    return marker_data

def build_markers(armature, context, node_names, game_title, fix_rotations, marker_data, name, parent_idx, rotation, translation, radius=1.0, region_idx=-1):
    object_name_prefix = '#%s' % name

    object_mesh = bpy.data.objects.new(object_name_prefix, None)
    object_mesh.color = (1, 1, 1, 0)

    context.collection.objects.link(object_mesh)

    bone_name = ""
    if not parent_idx == -1:
        bone_name = node_names[parent_idx]

        object_mesh.parent = armature
        object_mesh.parent_type = "BONE"
        object_mesh.parent_bone = bone_name

    else:
        object_mesh.parent = armature

    matrix_translate = Matrix.Translation(translation)
    if game_title == 'halo1':
        matrix_rotation = rotation.inverted().to_matrix().to_4x4()
    else:
        matrix_rotation = rotation.to_matrix().to_4x4()

    transform_matrix = matrix_translate @ matrix_rotation
    if not parent_idx == -1:
        pose_bone = armature.pose.bones[bone_name]

        if fix_rotations:
            transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ transform_matrix

        else:
            transform_matrix = pose_bone.matrix @ transform_matrix

    object_mesh.matrix_world = transform_matrix
    object_mesh.empty_display_type = 'ARROWS'

    object_mesh.scale = (radius, radius, radius)

    marker_data.append((object_mesh, region_idx))

def read_xref_instances_8201(JMS, xref_instances):
    xref_instance_count = int(JMS.next())
    for xref_idx in range(xref_instance_count):
        xref_path = JMS.next()

        xref_instances.append((xref_path, "xref_%s" % xref_idx))

def read_xref_instances_8208(JMS, xref_instances):
    xref_instance_count = int(JMS.next())
    for xref_idx in range(xref_instance_count):
        xref_path = JMS.next()
        xref_name = JMS.next()

        xref_instances.append((xref_path, xref_name))

def read_xref_markers_8201(JMS, context, armature, jms_version, xref_instances):
    build_xrefs = build_xrefs_2001
    if jms_version >= 8205:
        build_xrefs = build_xrefs_8205

    xref_markers_count = int(JMS.next())
    for xref_marker_idx in range(xref_markers_count):
        name = JMS.next()
        path_index = int(JMS.next())
        rotation = JMS.next_quaternion()
        translation = JMS.next_vector()

        build_xrefs(context, armature, name, path_index, rotation, translation, xref_instances)

def read_xref_markers_8203(JMS, context, armature, jms_version, xref_instances):
    build_xrefs = build_xrefs_2001
    if jms_version >= 8205:
        build_xrefs = build_xrefs_8205

    xref_markers_count = int(JMS.next())
    for xref_marker_idx in range(xref_markers_count):
        name = JMS.next()
        unique_identifier = int(JMS.next())
        path_index = int(JMS.next())
        rotation = JMS.next_quaternion()
        translation = JMS.next_vector()

        build_xrefs(context, armature, name, path_index, rotation, translation, xref_instances, unique_identifier)

def build_xrefs_2001(context, armature, name, path_index, rotation, translation, xref_instances, unique_identifier=-1):
    mesh = bpy.data.meshes.new(name)
    object_mesh = bpy.data.objects.new(name, mesh)
    object_mesh.color = (1, 1, 1, 0)
    context.collection.objects.link(object_mesh)

    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.to_mesh(mesh)
    bm.free()

    object_mesh.data.ass_jms.Object_Type = 'BOX'
    object_mesh.parent = armature

    matrix_translate = Matrix.Translation(translation)
    matrix_rotation = rotation.to_matrix().to_4x4()

    transform_matrix = matrix_translate @ matrix_rotation

    object_mesh.matrix_world = transform_matrix

def build_xrefs_8205(context, armature, name, path_index, rotation, translation, xref_instances, unique_identifier=-1):
    mesh = bpy.data.meshes.new(name)
    object_mesh = bpy.data.objects.new(name, mesh)
    object_mesh.color = (1, 1, 1, 0)
    context.collection.objects.link(object_mesh)

    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.to_mesh(mesh)
    bm.free()

    object_mesh.data.ass_jms.Object_Type = 'BOX'
    path, name = xref_instances[path_index]
    object_mesh.data.ass_jms.XREF_path = path
    object_mesh.data.ass_jms.XREF_name = name

    object_mesh.parent = armature

    matrix_translate = Matrix.Translation(translation)
    matrix_rotation = rotation.to_matrix().to_4x4()

    transform_matrix = matrix_translate @ matrix_rotation

    object_mesh.matrix_world = transform_matrix

def read_regions_8197(JMS, sections, section_map):
    region_count = int(JMS.next())
    for region_idx in range(region_count):
        region_name = JMS.next()
        if region_name == "__unnamed":
            region_name = "unnamed"

        if region_name in sections:
            map_id = sections.index(region_name)
        else:
            sections.append(region_name) 
            map_id = len(sections) - 1

        section_map[region_idx] = map_id

def read_vertices_8197(JMS):
    vertex_count = int(JMS.next())

    vertices = np.empty((vertex_count, 3), dtype=np.float32)
    vertex_normals = np.empty((vertex_count, 3), dtype=np.float32)
    vertex_region_ids = np.empty(vertex_count, dtype=np.int32)
    vertex_skinning_data = []
    vertex_uv_data = None
    
    for vertex_idx in range(vertex_count):
        vertex_region_ids[vertex_idx] = int(JMS.next())
        vertex_node_0_index = int(JMS.next())
        vertices[vertex_idx] = JMS.next_vector()
        vertex_normals[vertex_idx] = JMS.next_vector()
        vertex_node_1_index = int(JMS.next())
        vertex_node_1_weight = float(JMS.next())

        skinning_set = []
        skinning_set.append((vertex_node_0_index, 1 - vertex_node_1_weight))
        skinning_set.append((vertex_node_1_index, vertex_node_1_weight))

        vertex_skinning_data.append(tuple(skinning_set))
        
        if vertex_uv_data is None:
            vertex_uv_data = [np.empty((vertex_count, 2), dtype=np.float32) for uv_set_idx in range(1)]

        vertex_uv_data[0][vertex_idx, 0] = float(JMS.next())
        vertex_uv_data[0][vertex_idx, 1] = float(JMS.next())

    return vertices, vertex_normals, vertex_region_ids, vertex_skinning_data, vertex_uv_data

def read_vertices_8198(JMS):
    vertex_count = int(JMS.next())

    vertices = np.empty((vertex_count, 3), dtype=np.float32)
    vertex_normals = np.empty((vertex_count, 3), dtype=np.float32)
    vertex_skinning_data = []
    vertex_uv_data = None

    for vertex_idx in range(vertex_count):
        vertex_node_0_index = int(JMS.next())
        vertices[vertex_idx] = JMS.next_vector()
        vertex_normals[vertex_idx] = JMS.next_vector()
        vertex_node_1_index = int(JMS.next())
        vertex_node_1_weight = float(JMS.next())

        skinning_set = []
        skinning_set.append((vertex_node_0_index, 1 - vertex_node_1_weight))
        skinning_set.append((vertex_node_1_index, vertex_node_1_weight))

        vertex_skinning_data.append(tuple(skinning_set))

        if vertex_uv_data is None:
            vertex_uv_data = [np.empty((vertex_count, 2), dtype=np.float32) for uv_set_idx in range(1)]

        vertex_uv_data[0][vertex_idx, 0] = float(JMS.next())
        vertex_uv_data[0][vertex_idx, 1] = float(JMS.next())

    return vertices, vertex_normals, vertex_skinning_data, vertex_uv_data

def read_vertices_8199(JMS):
    vertex_count = int(JMS.next())

    vertices = np.empty((vertex_count, 3), dtype=np.float32)
    vertex_normals = np.empty((vertex_count, 3), dtype=np.float32)
    vertex_skinning_data = []
    vertex_uv_data = None

    for vertex_idx in range(vertex_count):
        vertex_node_0_index = int(JMS.next())
        vertices[vertex_idx] = JMS.next_vector()
        vertex_normals[vertex_idx] = JMS.next_vector()
        vertex_node_1_index = int(JMS.next())
        vertex_node_1_weight = float(JMS.next())

        skinning_set = []
        skinning_set.append((vertex_node_0_index, 1 - vertex_node_1_weight))
        skinning_set.append((vertex_node_1_index, vertex_node_1_weight))

        vertex_skinning_data.append(tuple(skinning_set))
        
        if vertex_uv_data is None:
            vertex_uv_data = [np.empty((vertex_count, 2), dtype=np.float32) for uv_set_idx in range(1)]

        vertex_uv_data[0][vertex_idx, 0] = float(JMS.next())
        vertex_uv_data[0][vertex_idx, 1] = float(JMS.next())

        vertex_flags = int(JMS.next()) #Unused int or boolean value. Don't know which but definitely not a float

    return vertices, vertex_normals, vertex_skinning_data, vertex_uv_data

def read_vertices_8202(JMS):
    vertex_count = int(JMS.next())

    vertices = np.empty((vertex_count, 3), dtype=np.float32)
    vertex_normals = np.empty((vertex_count, 3), dtype=np.float32)
    vertex_skinning_data = []
    vertex_uv_data = None

    for vertex_idx in range(vertex_count):
        vertex_node_0_index = int(JMS.next())
        vertices[vertex_idx] = JMS.next_vector()
        vertex_normals[vertex_idx] = JMS.next_vector()
        vertex_node_1_index = int(JMS.next())
        vertex_node_1_weight = float(JMS.next())

        skinning_set = []
        skinning_set.append((vertex_node_0_index, 1 - vertex_node_1_weight))
        skinning_set.append((vertex_node_1_index, vertex_node_1_weight))

        vertex_skinning_data.append(tuple(skinning_set))

        if vertex_uv_data is None:
            vertex_uv_data = [np.empty((vertex_count, 2), dtype=np.float32) for uv_set_idx in range(4)]

        vertex_uv_data[0][vertex_idx, 0] = float(JMS.next())
        vertex_uv_data[0][vertex_idx, 1] = float(JMS.next())
        vertex_uv_data[1][vertex_idx, 0] = float(JMS.next())
        vertex_uv_data[1][vertex_idx, 1] = float(JMS.next())
        vertex_uv_data[2][vertex_idx, 0] = float(JMS.next())
        vertex_uv_data[2][vertex_idx, 1] = float(JMS.next())
        vertex_uv_data[3][vertex_idx, 0] = float(JMS.next())
        vertex_uv_data[3][vertex_idx, 1] = float(JMS.next())

        vertex_flags = int(JMS.next()) #Unused int or boolean value. Don't know which but definitely not a float

    return vertices, vertex_normals, vertex_skinning_data, vertex_uv_data

def read_vertices_8204(JMS):
    vertex_count = int(JMS.next())

    vertices = np.empty((vertex_count, 3), dtype=np.float32)
    vertex_normals = np.empty((vertex_count, 3), dtype=np.float32)
    vertex_skinning_data = []
    vertex_uv_data = None

    for vertex_idx in range(vertex_count):
        vertex_node_0_index = int(JMS.next())
        vertex_node_0_weight = float(JMS.next())

        vertices[vertex_idx] = JMS.next_vector()
        vertex_normals[vertex_idx] = JMS.next_vector()

        vertex_node_1_index = int(JMS.next())
        vertex_node_1_weight = float(JMS.next())
        vertex_node_2_index = int(JMS.next())
        vertex_node_2_weight = float(JMS.next())
        vertex_node_3_index = int(JMS.next())
        vertex_node_3_weight = float(JMS.next())

        skinning_set = []
        skinning_set.append((vertex_node_0_index, vertex_node_0_weight))
        skinning_set.append((vertex_node_1_index, vertex_node_1_weight))
        skinning_set.append((vertex_node_2_index, vertex_node_2_weight))
        skinning_set.append((vertex_node_3_index, vertex_node_3_weight))

        vertex_skinning_data.append(tuple(skinning_set))

        if vertex_uv_data is None:
            vertex_uv_data = [np.empty((vertex_count, 2), dtype=np.float32) for uv_set_idx in range(4)]

        vertex_uv_data[0][vertex_idx, 0] = float(JMS.next())
        vertex_uv_data[0][vertex_idx, 1] = float(JMS.next())
        vertex_uv_data[1][vertex_idx, 0] = float(JMS.next())
        vertex_uv_data[1][vertex_idx, 1] = float(JMS.next())
        vertex_uv_data[2][vertex_idx, 0] = float(JMS.next())
        vertex_uv_data[2][vertex_idx, 1] = float(JMS.next())
        vertex_uv_data[3][vertex_idx, 0] = float(JMS.next())
        vertex_uv_data[3][vertex_idx, 1] = float(JMS.next())

        vertex_flags = int(JMS.next()) #Unused int or boolean value. Don't know which but definitely not a float

    return vertices, vertex_normals, vertex_skinning_data, vertex_uv_data

def read_vertices_8205(JMS):
    vertex_count = int(JMS.next())

    vertices = np.empty((vertex_count, 3), dtype=np.float32)
    vertex_normals = np.empty((vertex_count, 3), dtype=np.float32)
    vertex_skinning_data = []
    vertex_uv_data = None

    for vertex_idx in range(vertex_count):
        vertices[vertex_idx] = JMS.next_vector()
        vertex_normals[vertex_idx] = JMS.next_vector()

        skinning_set = []
        vertex_node_influence_count = int(JMS.next())
        for node_influence_idx in range(vertex_node_influence_count):
            vertex_node_index = int(JMS.next())
            vertex_node_weight = float(JMS.next())

            skinning_set.append((vertex_node_index, vertex_node_weight))

        vertex_skinning_data.append(tuple(skinning_set))

        vertex_uv_count = int(JMS.next())
        if vertex_uv_data is None:
            vertex_uv_data = [np.empty((vertex_count, 2), dtype=np.float32) for uv_set_idx in range(vertex_uv_count)]

        for uv_idx in range(vertex_uv_count):
            vertex_uv_data[uv_idx][vertex_idx, 0] = float(JMS.next())
            vertex_uv_data[uv_idx][vertex_idx, 1] = float(JMS.next())

    return vertices, vertex_normals, vertex_skinning_data, vertex_uv_data

def read_vertices_8211(JMS):
    vertex_count = int(JMS.next())

    vertices = np.empty((vertex_count, 3), dtype=np.float32)
    vertex_normals = np.empty((vertex_count, 3), dtype=np.float32)
    vertex_skinning_data = []
    vertex_uv_data = None
    vertex_colors = np.empty((vertex_count, 3), dtype=np.float32)

    for vertex_idx in range(vertex_count):
        vertices[vertex_idx] = JMS.next_vector()
        vertex_normals[vertex_idx] = JMS.next_vector()

        skinning_set = []
        vertex_node_influence_count = int(JMS.next())
        for node_influence_idx in range(vertex_node_influence_count):
            vertex_node_index = int(JMS.next())
            vertex_node_weight = float(JMS.next())

            skinning_set.append((vertex_node_index, vertex_node_weight))

        vertex_skinning_data.append(tuple(skinning_set))

        vertex_uv_count = int(JMS.next())
        if vertex_uv_data is None:
            vertex_uv_data = [np.empty((vertex_count, 2), dtype=np.float32) for uv_set_idx in range(vertex_uv_count)]

        for uv_idx in range(vertex_uv_count):
            vertex_uv_data[uv_idx][vertex_idx, 0] = float(JMS.next())
            vertex_uv_data[uv_idx][vertex_idx, 1] = float(JMS.next())

        vertex_colors[vertex_idx] = JMS.next_vector()

    return vertices, vertex_normals, vertex_skinning_data, vertex_uv_data, vertex_colors

def get_region_h1_era(triangle_idx, v0_idx, triangle_region_ids, vertex_region_ids, triangle_region, mat_id, section_map):
    region_idx = 0
    if vertex_region_ids != None:
        triangle_region = vertex_region_ids[v0_idx]

    map_id = section_map.get(triangle_region)
    if map_id != None:
        region_idx = map_id

    triangle_region_ids[triangle_idx] = region_idx

def get_region_h2_era(triangle_idx, v0_idx, triangle_region_ids, vertex_region_ids, triangle_region, mat_id, section_map):
    region_idx = 0
    map_id = section_map.get(mat_id)
    if map_id != None:
        region_idx = map_id

    triangle_region_ids[triangle_idx] = region_idx

def read_triangles_8197(JMS, game_title, vertex_region_ids, section_map):
    triangle_count = int(JMS.next())
    get_region = get_region_h1_era
    if game_title != "halo1":
        get_region = get_region_h2_era

    triangles = np.empty((triangle_count, 3), dtype=np.int32)
    triangle_material_ids = np.empty(triangle_count, dtype=np.int32)
    triangle_region_ids = np.empty(triangle_count, dtype=np.int32)

    for triangle_idx in range(triangle_count):
        mat_idx = int(JMS.next())
        v0_idx = int(JMS.next())

        triangle_material_ids[triangle_idx] = mat_idx

        triangles[triangle_idx, 0] = v0_idx
        triangles[triangle_idx, 1] = int(JMS.next())
        triangles[triangle_idx, 2] = int(JMS.next())
        get_region(triangle_idx, v0_idx, triangle_region_ids, vertex_region_ids, None, mat_idx, section_map)

    return triangles, triangle_material_ids, triangle_region_ids

def read_triangles_8198(JMS, game_title, section_map):
    triangle_count = int(JMS.next())
    get_region = get_region_h1_era
    if game_title != "halo1":
        get_region = get_region_h2_era

    triangles = np.empty((triangle_count, 3), dtype=np.int32)
    triangle_material_ids = np.empty(triangle_count, dtype=np.int32)
    triangle_region_ids = np.empty(triangle_count, dtype=np.int32)

    for triangle_idx in range(triangle_count):
        triangle_region = int(JMS.next())
        mat_idx = int(JMS.next())
        v0_idx = int(JMS.next())
        v1_idx = int(JMS.next())
        v2_idx = int(JMS.next())

        triangle_region_ids[triangle_idx] = triangle_region
        triangle_material_ids[triangle_idx] = mat_idx

        triangles[triangle_idx, 0] = v0_idx
        triangles[triangle_idx, 1] = v1_idx
        triangles[triangle_idx, 2] = v2_idx

        get_region(triangle_idx, v0_idx, triangle_region_ids, None, triangle_region, mat_idx, section_map)

    return triangles, triangle_material_ids, triangle_region_ids

def read_spheres_8206(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map):
    sphere_count = int(JMS.next())
    for sphere_idx in range(sphere_count):
        name = JMS.next()
        parent_index = int(JMS.next())

        rotation = JMS.next_quaternion()
        translation = JMS.next_vector()
        radius = float(JMS.next())

        build_sphere(armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map, name, parent_index, rotation, 
                     translation, radius)

def read_spheres_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map):
    sphere_count = int(JMS.next())
    for sphere_idx in range(sphere_count):
        name = JMS.next()
        parent_index = int(JMS.next())
        material_index = int(JMS.next())

        rotation = JMS.next_quaternion()
        translation = JMS.next_vector()
        radius = float(JMS.next())

        build_sphere(armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map, name, parent_index, rotation, 
                     translation, radius, material_index)

def build_sphere(armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map, name, parent_index, rotation, 
                 translation, radius, material_index=-1):
    object_name_prefix = '$%s' % name
    mesh = bpy.data.meshes.new(object_name_prefix)
    object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
    object_mesh.color = (1, 1, 1, 0)
    context.collection.objects.link(object_mesh)

    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
    bm.to_mesh(mesh)
    bm.free()

    matrix_translate = Matrix.Translation(translation)
    matrix_rotation = rotation.to_matrix().to_4x4()

    transform_matrix = matrix_translate @ matrix_rotation

    if not parent_index == -1 :
        bone_name = node_names[parent_index]

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
    primitive_shapes.append((object_mesh, parent_index))
    if not material_index == -1:
        mat = materials[triangle_material_map[material_index]]
        object_mesh.data.materials.append(mat)
        current_region_permutation = sections[section_map[material_index]]
        object_mesh.data.region_add(current_region_permutation)

    object_mesh.data.ass_jms.Object_Type = 'SPHERE'
    object_scale = radius
    object_mesh.scale = (object_scale, object_scale, object_scale)
    object_mesh.select_set(False)
    armature.select_set(False)

def read_boxes_8206(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map):
    boxes_count = int(JMS.next())
    for box_idx in range(boxes_count):
        name = JMS.next()
        parent_index = int(JMS.next())

        rotation = JMS.next_quaternion()
        translation = JMS.next_vector()
        width = float(JMS.next())
        length = float(JMS.next())
        height = float(JMS.next())

        build_box(armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map, name, parent_index, rotation, 
                  translation, width, length, height)

def read_boxes_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map):
    boxes_count = int(JMS.next())
    for box_idx in range(boxes_count):
        name = JMS.next()
        parent_index = int(JMS.next())
        material_index = int(JMS.next())

        rotation = JMS.next_quaternion()
        translation = JMS.next_vector()
        width = float(JMS.next())
        length = float(JMS.next())
        height = float(JMS.next())

        build_box(armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map, name, parent_index, rotation, 
                  translation, width, length, height, material_index)

def build_box(armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map, name, parent_index, rotation, 
              translation, width, length, height, material_index=-1):
    object_name_prefix = '$%s' % name
    mesh = bpy.data.meshes.new(object_name_prefix)
    object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
    object_mesh.color = (1, 1, 1, 0)
    context.collection.objects.link(object_mesh)

    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.to_mesh(mesh)
    bm.free()

    matrix_translate = Matrix.Translation(translation)
    matrix_rotation = rotation.to_matrix().to_4x4()

    transform_matrix = matrix_translate @ matrix_rotation

    if not parent_index == -1 :
        bone_name = node_names[parent_index]

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
    primitive_shapes.append((object_mesh, parent_index))
    if not material_index == -1:
        mat = materials[triangle_material_map[material_index]]
        object_mesh.data.materials.append(mat)
        current_region_permutation = sections[section_map[material_index]]
        object_mesh.data.region_add(current_region_permutation)

    object_mesh.data.ass_jms.Object_Type = 'BOX'
    object_mesh.scale = (width, length, height)
    object_mesh.select_set(False)
    armature.select_set(False)

def read_capsules_8206(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map):
    capsules_count = int(JMS.next())
    for capsule_idx in range(capsules_count):
        name = JMS.next()
        parent_index = int(JMS.next())

        rotation = JMS.next_quaternion()
        translation = JMS.next_vector()
        height = float(JMS.next())
        radius = float(JMS.next())

        build_capsule(armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map, name, parent_index, rotation, 
                      translation, height, radius)

def read_capsules_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map):
    capsules_count = int(JMS.next())
    for capsule_idx in range(capsules_count):
        name = JMS.next()
        parent_index = int(JMS.next())
        material_index = int(JMS.next())

        rotation = JMS.next_quaternion()
        translation = JMS.next_vector()
        height = float(JMS.next())
        radius = float(JMS.next())

        build_capsule(armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map, name, parent_index, rotation, 
                      translation, height, radius, material_index)

def build_capsule(armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map, name, parent_index, rotation, translation, 
              height, radius, material_index=-1):
    object_name_prefix = '$%s' % name
    mesh = bpy.data.meshes.new(object_name_prefix)
    object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
    object_mesh.color = (1, 1, 1, 0)
    context.collection.objects.link(object_mesh)

    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=12, radius1=1, radius2=1, depth=2)
    bm.transform(Matrix.Translation((0, 0, 1)))
    bm.to_mesh(mesh)
    bm.free()

    matrix_translate = Matrix.Translation(translation)
    matrix_rotation = rotation.to_matrix().to_4x4()

    transform_matrix = matrix_translate @ matrix_rotation

    if not parent_index == -1 :
        bone_name = node_names[parent_index]

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
    primitive_shapes.append((object_mesh, parent_index))
    if not material_index == -1:
        mat = materials[triangle_material_map[material_index]]
        object_mesh.data.materials.append(mat)
        current_region_permutation = sections[section_map[material_index]]
        object_mesh.data.region_add(current_region_permutation)

    object_mesh.data.ass_jms.Object_Type = 'CAPSULES'
    object_scale = radius
    object_mesh.scale = (object_scale, object_scale, (object_scale + (height / 2)))
    object_mesh.select_set(False)
    armature.select_set(False)

def read_convex_shapes_8206(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map):
    convex_shape_count = int(JMS.next())
    for convex_shape_idx in range(convex_shape_count):
        name = JMS.next()
        parent_index = int(JMS.next())

        rotation = JMS.next_quaternion()
        translation = JMS.next_vector()
        vertex_count = int(JMS.next())

        bm = bmesh.new()
        for vertex_idx in range(vertex_count):
            bm.verts.new(JMS.next_vector())
    
        bm.free()

        build_convex_shape(armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map, name, parent_index, 
                           rotation, translation, bm)

def read_convex_shapes_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map):
    convex_shape_count = int(JMS.next())
    for convex_shape_idx in range(convex_shape_count):
        name = JMS.next()
        parent_index = int(JMS.next())
        material_index = int(JMS.next())

        rotation = JMS.next_quaternion()
        translation = JMS.next_vector()
        vertex_count = int(JMS.next())

        bm = bmesh.new()
        for vertex_idx in range(vertex_count):
            bm.verts.new(JMS.next_vector())
    
        bm.free()

        build_convex_shape(armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map, name, parent_index, 
                           rotation, translation, bm, material_index)

def build_convex_shape(armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map, name, parent_index, rotation, 
                       translation, bm, material_index=-1):
    object_name_prefix = '$%s' % name
    mesh = bpy.data.meshes.new(object_name_prefix)
    object_mesh = bpy.data.objects.new(object_name_prefix, mesh)
    object_mesh.color = (1, 1, 1, 0)
    context.collection.objects.link(object_mesh)

    bm.to_mesh(mesh)

    matrix_translate = Matrix.Translation(translation)
    matrix_rotation = rotation.to_matrix().to_4x4()

    transform_matrix = matrix_translate @ matrix_rotation
    
    if not parent_index == -1 :
        bone_name = node_names[parent_index]

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
    primitive_shapes.append((object_mesh, parent_index))
    if not material_index == -1:
        mat = materials[triangle_material_map[material_index]]
        object_mesh.data.materials.append(mat)
        current_region_permutation = sections[section_map[material_index]]
        object_mesh.data.region_add(current_region_permutation)

    mesh_processing.select_object(context, object_mesh)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.convex_hull(delete_unused=True, use_existing_faces=True, join_triangles=True)
    bpy.ops.object.mode_set(mode='OBJECT')
    object_mesh.data.ass_jms.Object_Type = 'CONVEX SHAPES'
    mesh_processing.deselect_objects(context)

def read_ragdolls_8206(JMS, armature, context, fix_rotations, primitive_shapes):
    ragdoll_count  = int(JMS.next())
    for ragdoll_idx in range(ragdoll_count):
        name = JMS.next()
        attached_index = int(JMS.next())
        referenced_index = int(JMS.next())
        attached_rotation = JMS.next_quaternion()
        attached_translation = JMS.next_vector()
        referenced_rotation = JMS.next_quaternion()
        referenced_translation = JMS.next_vector()
        min_twist = float(JMS.next())
        max_twist = float(JMS.next())
        min_cone = float(JMS.next())
        max_cone = float(JMS.next())
        min_plane = float(JMS.next())
        max_plane = float(JMS.next())

        build_ragdoll(armature, context, fix_rotations, primitive_shapes, name, attached_index, referenced_index, attached_rotation, attached_translation, referenced_rotation, 
                      referenced_translation, min_twist, max_twist, min_cone, max_cone, min_plane, max_plane)

def read_ragdolls_8213(JMS, armature, context, fix_rotations, primitive_shapes):
    ragdoll_count  = int(JMS.next())
    for ragdoll_idx in range(ragdoll_count):
        name = JMS.next()
        attached_index = int(JMS.next())
        referenced_index = int(JMS.next())
        attached_rotation = JMS.next_quaternion()
        attached_translation = JMS.next_vector()
        referenced_rotation = JMS.next_quaternion()
        referenced_translation = JMS.next_vector()
        min_twist = float(JMS.next())
        max_twist = float(JMS.next())
        min_cone = float(JMS.next())
        max_cone = float(JMS.next())
        min_plane = float(JMS.next())
        max_plane = float(JMS.next())
        friction_limit = float(JMS.next())

        build_ragdoll(armature, context, fix_rotations, primitive_shapes, name, attached_index, referenced_index, attached_rotation, attached_translation, referenced_rotation, 
                      referenced_translation, min_twist, max_twist, min_cone, max_cone, min_plane, max_plane, friction_limit)

def build_ragdoll(armature, context, fix_rotations, primitive_shapes, name, attached_index, referenced_index, attached_rotation, attached_translation, referenced_rotation, 
                  referenced_translation, min_twist, max_twist, min_cone, max_cone, min_plane, max_plane, friction_limit=0.0):
    ragdoll_attached_object = None
    ragdoll_referenced_object = None
    if not attached_index == -1:
        for shape in primitive_shapes:
            shape_object = shape[0]
            shape_parent_index = shape[1]
            if shape_parent_index == attached_index:
                ragdoll_attached_object = shape_object
                if not not shape_object.rigid_body:
                    mesh_processing.select_object(context, shape_object)
                    bpy.ops.rigidbody.object_add()
                    mesh_processing.deselect_objects(context)

                break

    if not referenced_index == -1:
        for shape in primitive_shapes:
            shape_object = shape[0]
            shape_parent_index = shape[1]
            if shape_parent_index == referenced_index:
                ragdoll_referenced_object = shape_object
                if not shape_object.rigid_body:
                    mesh_processing.select_object(context, shape_object)
                    bpy.ops.rigidbody.object_add()
                    mesh_processing.deselect_objects(context)

                break

    object_name_prefix = '$%s' % name

    object_empty = bpy.data.objects.new(object_name_prefix, None)
    object_empty.color = (1, 1, 1, 0)
    context.collection.objects.link(object_empty)

    object_empty.empty_display_size = 2
    object_empty.empty_display_type = 'ARROWS'

    mesh_processing.select_object(context, object_empty)

    bpy.ops.rigidbody.constraint_add()

    object_empty.jms.jms_friction_limit = friction_limit

    object_empty.rigid_body_constraint.type = 'GENERIC'
    object_empty.rigid_body_constraint.use_limit_ang_x = True
    object_empty.rigid_body_constraint.use_limit_ang_y = True
    object_empty.rigid_body_constraint.use_limit_ang_z = True

    object_empty.rigid_body_constraint.use_limit_lin_x = True
    object_empty.rigid_body_constraint.use_limit_lin_y = True
    object_empty.rigid_body_constraint.use_limit_lin_z = True

    object_empty.rigid_body_constraint.limit_ang_x_lower = radians(min_twist)
    object_empty.rigid_body_constraint.limit_ang_x_upper = radians(max_twist)
    object_empty.rigid_body_constraint.limit_ang_y_lower = radians(min_cone)
    object_empty.rigid_body_constraint.limit_ang_y_upper = radians(max_cone)
    object_empty.rigid_body_constraint.limit_ang_z_lower = radians(min_plane)
    object_empty.rigid_body_constraint.limit_ang_z_upper = radians(max_plane)

    object_empty.rigid_body_constraint.limit_lin_x_lower = 0
    object_empty.rigid_body_constraint.limit_lin_x_upper = 0
    object_empty.rigid_body_constraint.limit_lin_y_lower = 0
    object_empty.rigid_body_constraint.limit_lin_y_upper = 0
    object_empty.rigid_body_constraint.limit_lin_z_lower = 0
    object_empty.rigid_body_constraint.limit_lin_z_upper = 0

    object_empty.rigid_body_constraint.object1 = ragdoll_attached_object
    object_empty.rigid_body_constraint.object2 = ragdoll_referenced_object

    object_empty.parent = armature
    transform_matrix = Euler((0, 0, 0)).to_matrix().to_4x4()

    ragdoll_origin_index = None
    ragdoll_origin_is_attached = False
    if not attached_index == -1:
        ragdoll_origin_is_attached = True
        ragdoll_origin_index = attached_index

    elif not referenced_index == -1 and ragdoll_origin_index == None:
        ragdoll_origin_index = referenced_index

    if not ragdoll_origin_index == None:
        pose_bone = armature.pose.bones[ragdoll_origin_index]
        ragdoll_rotation = attached_rotation
        ragdoll_translation = attached_translation
        if not ragdoll_origin_is_attached:
            ragdoll_rotation = referenced_rotation
            ragdoll_translation = referenced_translation

        hinge_local_translate = Matrix.Translation(ragdoll_translation)
        hinge_local_rotation = ragdoll_rotation.to_matrix().to_4x4()
        hinge_local_matrix = hinge_local_translate @ hinge_local_rotation

        if fix_rotations:
            transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ hinge_local_matrix

        else:
            transform_matrix = pose_bone.matrix @ hinge_local_matrix

    object_empty.matrix_world = transform_matrix
    object_empty.select_set(False)

def read_hinges_8206(JMS, armature, context, fix_rotations, primitive_shapes):
    hinge_count  = int(JMS.next())
    for hinge_idx in range(hinge_count):
        name = JMS.next()
        body_a_index = int(JMS.next())
        body_b_index = int(JMS.next())
        body_a_rotation = JMS.next_quaternion()
        body_a_translation = JMS.next_vector()
        body_b_rotation = JMS.next_quaternion()
        body_b_translation = JMS.next_vector()
        is_limited = int(JMS.next())
        friction_limit = float(JMS.next())
        min_angle = float(JMS.next())
        max_angle = float(JMS.next())

        hinge_body_a_object = None
        hinge_body_b_object = None
        if not body_a_index == -1:
            for shape in primitive_shapes:
                shape_object = shape[0]
                shape_parent_index = shape[1]
                if shape_parent_index == body_a_index:
                    hinge_body_a_object = shape_object
                    if not shape_object.rigid_body:
                        mesh_processing.select_object(context, shape_object)
                        bpy.ops.rigidbody.object_add()
                        mesh_processing.deselect_objects(context)

                    break

        if not body_b_index == -1:
            for shape in primitive_shapes:
                shape_object = shape[0]
                shape_parent_index = shape[1]
                if shape_parent_index == body_b_index:
                    hinge_body_b_object = shape_object
                    if not shape_object.rigid_body:
                        mesh_processing.select_object(context, shape_object)
                        bpy.ops.rigidbody.object_add()
                        mesh_processing.deselect_objects(context)

                    break

        object_name_prefix = '$%s' % name

        object_empty = bpy.data.objects.new(object_name_prefix, None)
        object_empty.color = (1, 1, 1, 0)
        context.collection.objects.link(object_empty)

        object_empty.empty_display_size = 2
        object_empty.empty_display_type = 'ARROWS'

        mesh_processing.select_object(context, object_empty)

        bpy.ops.rigidbody.constraint_add()

        object_empty.jms.jms_friction_limit = friction_limit

        object_empty.rigid_body_constraint.type = 'HINGE'
        object_empty.rigid_body_constraint.use_limit_ang_z = bool(is_limited)

        object_empty.rigid_body_constraint.limit_ang_z_lower = radians(min_angle)
        object_empty.rigid_body_constraint.limit_ang_z_upper = radians(max_angle)

        object_empty.rigid_body_constraint.object1 = hinge_body_a_object
        object_empty.rigid_body_constraint.object2 = hinge_body_b_object

        object_empty.parent = armature
        transform_matrix = Euler((0, 0, 0)).to_matrix().to_4x4()

        hinge_origin_index = None
        hinge_origin_is_attached = False
        if not body_a_index == -1:
            hinge_origin_is_attached = True
            hinge_origin_index = body_a_index

        elif not body_b_index == -1 and hinge_origin_index == None:
            hinge_origin_index = body_b_index

        if not hinge_origin_index == None:
            pose_bone = armature.pose.bones[hinge_origin_index]
            hinge_rotation = body_a_rotation
            hinge_translation = body_a_translation
            if not hinge_origin_is_attached:
                hinge_rotation = body_b_rotation
                hinge_translation = body_b_translation

            hinge_local_translate = Matrix.Translation(hinge_translation)
            hinge_local_rotation = hinge_rotation.to_matrix().to_4x4()
            hinge_local_matrix = hinge_local_translate @ hinge_local_rotation

            if fix_rotations:
                transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ hinge_local_matrix

            else:
                transform_matrix = pose_bone.matrix @ hinge_local_matrix

        object_empty.matrix_world = transform_matrix
        object_empty.select_set(False)

def read_car_wheels_8210(JMS, armature, context, fix_rotations, primitive_shapes):
    car_wheel_count  = int(JMS.next())
    for car_wheel_idx in range(car_wheel_count):
        name = JMS.next()
        chassis_index = int(JMS.next())
        wheel_index = int(JMS.next())
        wheel_rotation = JMS.next_quaternion()
        wheel_translation = JMS.next_vector()
        suspension_rotation = JMS.next_quaternion()
        suspension_translation = JMS.next_vector()
        suspension_min_limit = float(JMS.next())
        suspension_max_limit = float(JMS.next())
        friction_limit = float(JMS.next())
        velocity = float(JMS.next())
        gain = float(JMS.next())

        car_wheel_chassis_object = None
        car_wheel_wheel_object = None
        if not chassis_index == -1:
            for shape in primitive_shapes:
                shape_object = shape[0]
                shape_parent_index = shape[1]
                if shape_parent_index == chassis_index:
                    car_wheel_chassis_object = shape_object
                    if not shape_object.rigid_body:
                        mesh_processing.select_object(context, shape_object)
                        bpy.ops.rigidbody.object_add()
                        mesh_processing.deselect_objects(context)
                        shape_object.rigid_body.linear_damping = friction_limit

                    break

        if not wheel_index == -1:
            for shape in primitive_shapes:
                shape_object = shape[0]
                shape_parent_index = shape[1]
                if shape_parent_index == wheel_index:
                    car_wheel_wheel_object = shape_object
                    if not shape_object.rigid_body:
                        mesh_processing.select_object(context, shape_object)
                        bpy.ops.rigidbody.object_add()
                        mesh_processing.deselect_objects(context)
                        shape_object.rigid_body.linear_damping = friction_limit

                    break

        object_name_prefix = '$%s' % name

        object_empty = bpy.data.objects.new(object_name_prefix, None)
        object_empty.color = (1, 1, 1, 0)
        context.collection.objects.link(object_empty)

        object_empty.empty_display_size = 2
        object_empty.empty_display_type = 'ARROWS'

        mesh_processing.select_object(context, object_empty)
        object_empty.parent = armature
        transform_matrix = Euler((0, 0, 0)).to_matrix().to_4x4()

        car_wheel_origin_index = None
        car_wheel_origin_is_attached = False
        if not chassis_index == -1:
            car_wheel_origin_is_attached = True
            car_wheel_origin_index = chassis_index

        elif not chassis_index == -1 and car_wheel_origin_index == None:
            car_wheel_origin_index = chassis_index

        if not car_wheel_origin_index == None:
            pose_bone = armature.pose.bones[car_wheel_origin_index]
            car_wheel_rotation = wheel_rotation
            car_wheel_translation = wheel_translation
            if not car_wheel_origin_is_attached:
                car_wheel_rotation = suspension_rotation
                car_wheel_translation = suspension_translation

            car_wheel_local_translate = Matrix.Translation(car_wheel_translation)
            car_wheel_local_rotation = car_wheel_rotation.to_matrix().to_4x4()
            car_wheel_local_matrix = car_wheel_local_translate @ car_wheel_local_rotation

            if fix_rotations:
                transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ car_wheel_local_matrix

            else:
                transform_matrix = pose_bone.matrix @ car_wheel_local_matrix

        object_empty.matrix_world = transform_matrix
        object_empty.select_set(False)

def read_point_to_points_8210(JMS, armature, context, fix_rotations, primitive_shapes):
    point_to_point_count = int(JMS.next())
    for point_to_point_idx in range(point_to_point_count):
        name = JMS.next()
        body_a_index = int(JMS.next())
        body_b_index = int(JMS.next())
        body_a_rotation = JMS.next_quaternion()
        body_a_translation = JMS.next_vector()
        body_b_rotation = JMS.next_quaternion()
        body_b_translation = JMS.next_vector()
        constraint_type = int(JMS.next())
        x_min_limit = float(JMS.next())
        x_max_limit = float(JMS.next())
        y_min_limit = float(JMS.next())
        y_max_limit = float(JMS.next())
        z_min_limit = float(JMS.next())
        z_max_limit = float(JMS.next())
        spring_length = float(JMS.next())

        point_to_point_body_a_object = None
        point_to_point_body_b_object = None
        if not body_a_index == -1:
            for shape in primitive_shapes:
                shape_object = shape[0]
                shape_parent_index = shape[1]
                if shape_parent_index == body_a_index:
                    point_to_point_body_a_object = shape_object
                    if not shape_object.rigid_body:
                        mesh_processing.select_object(context, shape_object)
                        bpy.ops.rigidbody.object_add()
                        mesh_processing.deselect_objects(context)

                    break

        if not body_b_index == -1:
            for shape in primitive_shapes:
                shape_object = shape[0]
                shape_parent_index = shape[1]
                if shape_parent_index == body_b_index:
                    point_to_point_body_b_object = shape_object
                    if not shape_object.rigid_body:
                        mesh_processing.select_object(context, shape_object)
                        bpy.ops.rigidbody.object_add()
                        mesh_processing.deselect_objects(context)

                    break

        object_name_prefix = '$%s' % name

        object_empty = bpy.data.objects.new(object_name_prefix, None)
        object_empty.color = (1, 1, 1, 0)
        context.collection.objects.link(object_empty)

        object_empty.empty_display_size = 2
        object_empty.empty_display_type = 'ARROWS'

        mesh_processing.select_object(context, object_empty)

        bpy.ops.rigidbody.constraint_add()

        object_empty.rigid_body_constraint.type = 'GENERIC_SPRING'

        object_empty.rigid_body_constraint.object1 = point_to_point_body_a_object
        object_empty.rigid_body_constraint.object2 = point_to_point_body_b_object

        object_empty.jms.jms_spring_type = str(constraint_type)

        object_empty.rigid_body_constraint.use_limit_ang_x = True
        object_empty.rigid_body_constraint.limit_ang_x_lower = radians(x_min_limit)
        object_empty.rigid_body_constraint.limit_ang_x_upper = radians(x_max_limit)

        object_empty.rigid_body_constraint.use_limit_ang_y = True
        object_empty.rigid_body_constraint.limit_ang_y_lower = radians(y_min_limit)
        object_empty.rigid_body_constraint.limit_ang_y_upper = radians(y_max_limit)

        object_empty.rigid_body_constraint.use_limit_ang_z = True
        object_empty.rigid_body_constraint.limit_ang_z_lower = radians(z_min_limit)
        object_empty.rigid_body_constraint.limit_ang_z_upper = radians(z_max_limit)

        object_empty.rigid_body_constraint.use_limit_lin_z = True
        object_empty.rigid_body_constraint.limit_lin_z_upper = spring_length

        object_empty.parent = armature
        transform_matrix = Euler((0, 0, 0)).to_matrix().to_4x4()

        point_to_point_origin_index = None
        point_to_point_origin_is_attached = False
        if not body_a_index == -1:
            point_to_point_origin_is_attached = True
            point_to_point_origin_index = body_a_index

        elif not body_b_index == -1 and point_to_point_origin_index == None:
            point_to_point_origin_index = body_b_index

        if not point_to_point_origin_index == None:
            pose_bone = armature.pose.bones[point_to_point_origin_index]
            point_to_point_rotation = body_a_rotation
            point_to_point_translation = body_a_translation
            if not point_to_point_origin_is_attached:
                point_to_point_rotation = body_b_rotation
                point_to_point_translation = body_b_translation

            point_to_point_local_translate = Matrix.Translation(point_to_point_translation)
            point_to_point_local_rotation = point_to_point_rotation.to_matrix().to_4x4()
            point_to_point_local_matrix = point_to_point_local_translate @ point_to_point_local_rotation

            if fix_rotations:
                transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ point_to_point_local_matrix

            else:
                transform_matrix = pose_bone.matrix @ point_to_point_local_matrix

        object_empty.matrix_world = transform_matrix
        object_empty.select_set(False)

def read_prismatics_8210(JMS, armature, context, fix_rotations, primitive_shapes):
    prismatic_count = int(JMS.next())
    for prismatic_idx in range(prismatic_count):
        name = JMS.next()
        body_a_index = int(JMS.next())
        body_b_index = int(JMS.next())
        body_a_rotation = JMS.next_quaternion()
        body_a_translation = JMS.next_vector()
        body_b_rotation = JMS.next_quaternion()
        body_b_translation = JMS.next_vector()
        is_limited = int(JMS.next())
        friction_limit = float(JMS.next())
        min_limit = float(JMS.next())
        max_limit = float(JMS.next())

        prismatic_body_a_object = None
        prismatic_body_b_object = None
        if not body_a_index == -1:
            for shape in primitive_shapes:
                shape_object = shape[0]
                shape_parent_index = shape[1]
                if shape_parent_index == body_a_index:
                    prismatic_body_a_object = shape_object
                    if not shape_object.rigid_body:
                        mesh_processing.select_object(context, shape_object)
                        bpy.ops.rigidbody.object_add()
                        mesh_processing.deselect_objects(context)

                    break

        if not body_b_index == -1:
            for shape in primitive_shapes:
                shape_object = shape[0]
                shape_parent_index = shape[1]
                if shape_parent_index == body_b_index:
                    prismatic_body_b_object = shape_object
                    if not shape_object.rigid_body:
                        mesh_processing.select_object(context, shape_object)
                        bpy.ops.rigidbody.object_add()
                        mesh_processing.deselect_objects(context)

                    break

        object_name_prefix = '$%s' % name

        object_empty = bpy.data.objects.new(object_name_prefix, None)
        object_empty.color = (1, 1, 1, 0)
        context.collection.objects.link(object_empty)

        object_empty.empty_display_size = 2
        object_empty.empty_display_type = 'ARROWS'

        mesh_processing.select_object(context, object_empty)

        bpy.ops.rigidbody.constraint_add()

        object_empty.rigid_body_constraint.type = 'SLIDER'

        object_empty.rigid_body_constraint.object1 = prismatic_body_a_object
        object_empty.rigid_body_constraint.object2 = prismatic_body_b_object

        object_empty.jms.jms_friction_limit = friction_limit

        object_empty.rigid_body_constraint.use_limit_lin_x = bool(is_limited)
        object_empty.rigid_body_constraint.limit_lin_x_lower = radians(min_limit)
        object_empty.rigid_body_constraint.limit_lin_x_upper = radians(max_limit)

        object_empty.parent = armature
        transform_matrix = Euler((0, 0, 0)).to_matrix().to_4x4()

        prismatic_origin_index = None
        prismatic_origin_is_attached = False
        if not body_a_index == -1:
            prismatic_origin_is_attached = True
            prismatic_origin_index = body_a_index

        elif not body_b_index == -1 and prismatic_origin_index == None:
            prismatic_origin_index = body_b_index

        if not prismatic_origin_index == None:
            pose_bone = armature.pose.bones[prismatic_origin_index]
            prismatic_rotation = body_a_rotation
            prismatic_translation = body_a_translation
            if not prismatic_origin_is_attached:
                prismatic_rotation = body_b_rotation
                prismatic_translation = body_b_translation

            prismatic_local_translate = Matrix.Translation(prismatic_translation)
            prismatic_local_rotation = prismatic_rotation.to_matrix().to_4x4()
            prismatic_local_matrix = prismatic_local_translate @ prismatic_local_rotation

            if fix_rotations:
                transform_matrix = (pose_bone.matrix @ Matrix.Rotation(radians(90.0), 4, 'Z')) @ prismatic_local_matrix

            else:
                transform_matrix = pose_bone.matrix @ prismatic_local_matrix

        object_empty.matrix_world = transform_matrix
        object_empty.select_set(False)

def read_bounding_spheres_8209(JMS, armature, context):
    bounding_sphere_count = int(JMS.next())
    for bounding_sphere_idx in range(bounding_sphere_count):
        translation = JMS.next_vector()
        radius = float(JMS.next())

        name = 'bounding_sphere_%s' % bounding_sphere_idx
  
        mesh = bpy.data.meshes.new(name)
        object_mesh = bpy.data.objects.new(name, mesh)
        object_mesh.color = (1, 1, 1, 0)
        context.collection.objects.link(object_mesh)

        bm = bmesh.new()
        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
        bm.to_mesh(mesh)
        bm.free()

        object_mesh.parent = armature

        matrix_translate = Matrix.Translation(translation)

        transform_matrix = matrix_translate
        object_mesh.matrix_world = transform_matrix

        object_mesh.data.ass_jms.Object_Type = 'SPHERE'
        object_mesh.data.ass_jms.bounding_radius = True
        object_mesh.scale = (radius, radius, radius)

def read_skylights_8212(JMS, armature, context):
    skylight_count = int(JMS.next())
    for skylight_idx in range(skylight_count):
        direction = JMS.next_vector()
        radiant_intensity = JMS.next_vector()
        solid_angle = float(JMS.next())

        name = 'skylight_%s' % skylight_idx
        down_vector = Vector((0, 0, -1))

        light_data = bpy.data.lights.new(name, "SUN")
        object_mesh = bpy.data.objects.new(name, light_data)
        object_mesh.color = (1, 1, 1, 0)
        context.collection.objects.link(object_mesh)
        object_mesh.rotation_euler = down_vector.rotation_difference(direction).to_euler()
        object_mesh.data.color = (radiant_intensity)
        object_mesh.data.energy = (solid_angle)

        object_mesh.parent = armature

        object_mesh.select_set(False)
        armature.select_set(False)

def load_file(context, filepath, game_title, reuse_armature, fix_parents, fix_rotations, empty_markers, shader_gen_setting, report):
    object_name = bpy.path.basename(filepath).rsplit('.', 1)[0]
    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors

    valid_armature = False
    if context.object and context.object.type == "ARMATURE" and reuse_armature:
        valid_armature = True
        armature = context.object

    else:
        mesh_processing.deselect_objects(context)
        armdata = bpy.data.armatures.new('Armature')
        armature = bpy.data.objects.new('Armature', armdata)
        armature.color = (1, 1, 1, 0)
        context.collection.objects.link(armature)
        mesh_processing.select_object(context, armature)

    JMS = JMSAsset(filepath)
    jms_version = int(JMS.next())
    JMS.version = jms_version
    JMS.are_quaternions_inverted = jms_version < 8205
    if game_title == 'auto':
        game_title = global_functions.get_game_title(jms_version, 'JMS')

    node_names = []
    materials = []
    sections = []
    primitive_shapes = []
    xref_instances = []
    marker_data = None
    vertex_region_ids = None
    vertex_colors = None
    triangle_material_map = {}
    section_map = {}
    if jms_version == 8197:
        skip_checksum_8197(JMS)
        read_nodes_8197(JMS, armature, node_names, jms_version, fix_rotations, valid_armature)
        read_materials_8197(JMS, game_title, materials, sections, section_map, triangle_material_map, random_color_gen, filepath, shader_gen_setting, report)
        read_markers_8197(JMS, context, game_title, armature, node_names, fix_rotations)
        read_regions_8197(JMS, sections, section_map)
        vertices, vertex_normals, vertex_region_ids, vertex_skinning_data, vertex_uv_data = read_vertices_8197(JMS)
        triangles, triangle_material_ids, triangle_region_ids = read_triangles_8197(JMS, game_title, vertex_region_ids, section_map)
    elif jms_version == 8198:
        skip_checksum_8197(JMS)
        read_nodes_8197(JMS, armature, node_names, jms_version, fix_rotations, valid_armature)
        read_materials_8197(JMS, game_title, materials, sections, section_map, triangle_material_map, random_color_gen, filepath, shader_gen_setting, report)
        marker_data = read_markers_8198(JMS, context, game_title, armature, node_names, fix_rotations)
        read_regions_8197(JMS, sections, section_map)
        vertices, vertex_normals, vertex_skinning_data, vertex_uv_data = read_vertices_8198(JMS)
        triangles, triangle_material_ids, triangle_region_ids = read_triangles_8198(JMS, game_title, section_map)
    elif jms_version == 8199:
        skip_checksum_8197(JMS)
        read_nodes_8197(JMS, armature, node_names, jms_version, fix_rotations, valid_armature)
        read_materials_8197(JMS, game_title, materials, sections, section_map, triangle_material_map, random_color_gen, filepath, shader_gen_setting, report)
        marker_data = read_markers_8198(JMS, context, game_title, armature, node_names, fix_rotations)
        read_regions_8197(JMS, sections, section_map)
        vertices, vertex_normals, vertex_skinning_data, vertex_uv_data = read_vertices_8199(JMS)
        triangles, triangle_material_ids, triangle_region_ids = read_triangles_8198(JMS, game_title, section_map)
    elif jms_version == 8200:
        skip_checksum_8197(JMS)
        read_nodes_8197(JMS, armature, node_names, jms_version, fix_rotations, valid_armature)
        read_materials_8197(JMS, game_title, materials, sections, section_map, triangle_material_map, random_color_gen, filepath, shader_gen_setting, report)
        marker_data = read_markers_8200(JMS, context, game_title, armature, node_names, fix_rotations)
        read_regions_8197(JMS, sections, section_map)
        vertices, vertex_normals, vertex_skinning_data, vertex_uv_data = read_vertices_8199(JMS)
        triangles, triangle_material_ids, triangle_region_ids = read_triangles_8198(JMS, game_title, section_map)
    elif jms_version == 8201:
        skip_checksum_8197(JMS)
        read_nodes_8197(JMS, armature, node_names, jms_version, fix_rotations, valid_armature)
        read_materials_8197(JMS, game_title, materials, sections, section_map, triangle_material_map, random_color_gen, filepath, shader_gen_setting, report)
        marker_data = read_markers_8200(JMS, context, game_title, armature, node_names, fix_rotations)
        read_xref_instances_8201(JMS, xref_instances)
        read_xref_markers_8201(JMS, context, armature, jms_version, xref_instances)
        read_regions_8197(JMS, sections, section_map)
        vertices, vertex_normals, vertex_skinning_data, vertex_uv_data = read_vertices_8199(JMS)
        triangles, triangle_material_ids, triangle_region_ids = read_triangles_8198(JMS, game_title, section_map)
    elif jms_version == 8202:
        skip_checksum_8197(JMS)
        read_nodes_8197(JMS, armature, node_names, jms_version, fix_rotations, valid_armature)
        read_materials_8202(JMS, game_title, materials, sections, section_map, triangle_material_map, random_color_gen, filepath, shader_gen_setting, report)
        marker_data = read_markers_8200(JMS, context, game_title, armature, node_names, fix_rotations)
        read_xref_instances_8201(JMS, xref_instances)
        read_xref_markers_8201(JMS, context, armature, jms_version, xref_instances)
        read_regions_8197(JMS, sections, section_map)
        vertices, vertex_normals, vertex_skinning_data, vertex_uv_data = read_vertices_8202(JMS)
        triangles, triangle_material_ids, triangle_region_ids = read_triangles_8198(JMS, game_title, section_map)
    elif jms_version == 8203:
        skip_checksum_8197(JMS)
        read_nodes_8197(JMS, armature, node_names, jms_version, fix_rotations, valid_armature)
        read_materials_8202(JMS, game_title, materials, sections, section_map, triangle_material_map, random_color_gen, filepath, shader_gen_setting, report)
        marker_data = read_markers_8200(JMS, context, game_title, armature, node_names, fix_rotations)
        read_xref_instances_8201(JMS, xref_instances)
        read_xref_markers_8203(JMS, context, armature, jms_version, xref_instances)
        read_regions_8197(JMS, sections, section_map)
        vertices, vertex_normals, vertex_skinning_data, vertex_uv_data = read_vertices_8202(JMS)
        triangles, triangle_material_ids, triangle_region_ids = read_triangles_8198(JMS, game_title, section_map)
    elif jms_version == 8204:
        skip_checksum_8197(JMS)
        read_nodes_8197(JMS, armature, node_names, jms_version, fix_rotations, valid_armature)
        read_materials_8202(JMS, game_title, materials, sections, section_map, triangle_material_map, random_color_gen, filepath, shader_gen_setting, report)
        marker_data = read_markers_8200(JMS, context, game_title, armature, node_names, fix_rotations)
        read_xref_instances_8201(JMS, xref_instances)
        read_xref_markers_8203(JMS, context, armature, jms_version, xref_instances)
        read_regions_8197(JMS, sections, section_map)
        vertices, vertex_normals, vertex_skinning_data, vertex_uv_data = read_vertices_8204(JMS)
        triangles, triangle_material_ids, triangle_region_ids = read_triangles_8198(JMS, game_title, section_map)
    elif jms_version == 8205:
        read_nodes_8205(JMS, armature, node_names, jms_version, fix_rotations, valid_armature)
        read_materials_8197(JMS, game_title, materials, sections, section_map, triangle_material_map, random_color_gen, filepath, shader_gen_setting, report)
        marker_data = read_markers_8200(JMS, context, game_title, armature, node_names, fix_rotations)
        read_xref_instances_8201(JMS, xref_instances)
        read_xref_markers_8203(JMS, context, armature, jms_version, xref_instances)
        vertices, vertex_normals, vertex_skinning_data, vertex_uv_data = read_vertices_8205(JMS)
        triangles, triangle_material_ids, triangle_region_ids = read_triangles_8197(JMS, game_title, vertex_region_ids, section_map)
    elif jms_version == 8206:
        read_nodes_8205(JMS, armature, node_names, jms_version, fix_rotations, valid_armature)
        read_materials_8197(JMS, game_title, materials, sections, section_map, triangle_material_map, random_color_gen, filepath, shader_gen_setting, report)
        read_markers_8206(JMS, context, game_title, armature, node_names, fix_rotations)
        read_xref_instances_8201(JMS, xref_instances)
        read_xref_markers_8203(JMS, context, armature, jms_version, xref_instances)
        vertices, vertex_normals, vertex_skinning_data, vertex_uv_data = read_vertices_8205(JMS)
        triangles, triangle_material_ids, triangle_region_ids = read_triangles_8197(JMS, game_title, vertex_region_ids, section_map)
        read_spheres_8206(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_boxes_8206(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_capsules_8206(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_convex_shapes_8206(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_ragdolls_8206(JMS, armature, context, fix_rotations, primitive_shapes)
        read_hinges_8206(JMS, armature, context, fix_rotations, primitive_shapes)
    elif jms_version == 8207:
        read_nodes_8205(JMS, armature, node_names, jms_version, fix_rotations, valid_armature)
        read_materials_8197(JMS, game_title, materials, sections, section_map, triangle_material_map, random_color_gen, filepath, shader_gen_setting, report)
        read_markers_8206(JMS, context, game_title, armature, node_names, fix_rotations)
        read_xref_instances_8201(JMS, xref_instances)
        read_xref_markers_8203(JMS, context, armature, jms_version, xref_instances)
        vertices, vertex_normals, vertex_skinning_data, vertex_uv_data = read_vertices_8205(JMS)
        triangles, triangle_material_ids, triangle_region_ids = read_triangles_8197(JMS, game_title, vertex_region_ids, section_map)
        read_spheres_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_boxes_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_capsules_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_convex_shapes_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_ragdolls_8206(JMS, armature, context, fix_rotations, primitive_shapes)
        read_hinges_8206(JMS, armature, context, fix_rotations, primitive_shapes)
    elif jms_version == 8208:
        read_nodes_8205(JMS, armature, node_names, jms_version, fix_rotations, valid_armature)
        read_materials_8197(JMS, game_title, materials, sections, section_map, triangle_material_map, random_color_gen, filepath, shader_gen_setting, report)
        read_markers_8206(JMS, context, game_title, armature, node_names, fix_rotations)
        read_xref_instances_8208(JMS, xref_instances)
        read_xref_markers_8203(JMS, context, armature, jms_version, xref_instances)
        read_vertices_8205(JMS, vertices, vertex_normals, vertex_skinning_data, vertex_uv_data)
        triangles, triangle_material_ids, triangle_region_ids = read_triangles_8197(JMS, game_title, vertex_region_ids, section_map)
        read_spheres_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_boxes_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_capsules_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_convex_shapes_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_ragdolls_8206(JMS, armature, context, fix_rotations, primitive_shapes)
        read_hinges_8206(JMS, armature, context, fix_rotations, primitive_shapes)
    elif jms_version == 8209:
        read_nodes_8205(JMS, armature, node_names, jms_version, fix_rotations, valid_armature)
        read_materials_8197(JMS, game_title, materials, sections, section_map, triangle_material_map, random_color_gen, filepath, shader_gen_setting, report)
        read_markers_8206(JMS, context, game_title, armature, node_names, fix_rotations)
        read_xref_instances_8208(JMS, xref_instances)
        read_xref_markers_8203(JMS, context, armature, jms_version, xref_instances)
        vertices, vertex_normals, vertex_skinning_data, vertex_uv_data = read_vertices_8205(JMS)
        triangles, triangle_material_ids, triangle_region_ids = read_triangles_8197(JMS, game_title, vertex_region_ids, section_map)
        read_spheres_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_boxes_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_capsules_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_convex_shapes_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_ragdolls_8206(JMS, armature, context, fix_rotations, primitive_shapes)
        read_hinges_8206(JMS, armature, context, fix_rotations, primitive_shapes)
        read_bounding_spheres_8209(JMS, armature, context)
    elif jms_version == 8210:
        read_nodes_8205(JMS, armature, node_names, jms_version, fix_rotations, valid_armature)
        read_materials_8197(JMS, game_title, materials, sections, section_map, triangle_material_map, random_color_gen, filepath, shader_gen_setting, report)
        read_markers_8206(JMS, context, game_title, armature, node_names, fix_rotations)
        read_xref_instances_8208(JMS, xref_instances)
        read_xref_markers_8203(JMS, context, armature, jms_version, xref_instances)
        vertices, vertex_normals, vertex_skinning_data, vertex_uv_data = read_vertices_8205(JMS)
        triangles, triangle_material_ids, triangle_region_ids = read_triangles_8197(JMS, game_title, vertex_region_ids, section_map)
        read_spheres_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_boxes_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_capsules_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_convex_shapes_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_ragdolls_8206(JMS, armature, context, fix_rotations, primitive_shapes)
        read_hinges_8206(JMS, armature, context, fix_rotations, primitive_shapes)
        read_car_wheels_8210(JMS, armature, context, fix_rotations, primitive_shapes)
        read_point_to_points_8210(JMS, armature, context, fix_rotations, primitive_shapes)
        read_prismatics_8210(JMS, armature, context, fix_rotations, primitive_shapes)
        read_bounding_spheres_8209(JMS, armature, context)
    elif jms_version == 8211:
        read_nodes_8205(JMS, armature, node_names, jms_version, fix_rotations, valid_armature)
        read_materials_8197(JMS, game_title, materials, sections, section_map, triangle_material_map, random_color_gen, filepath, shader_gen_setting, report)
        read_markers_8206(JMS, context, game_title, armature, node_names, fix_rotations)
        read_xref_instances_8208(JMS, xref_instances)
        read_xref_markers_8203(JMS, context, armature, jms_version, xref_instances)
        vertices, vertex_normals, vertex_skinning_data, vertex_uv_data, vertex_colors = read_vertices_8211(JMS)
        triangles, triangle_material_ids, triangle_region_ids = read_triangles_8197(JMS, game_title, vertex_region_ids, section_map)
        read_spheres_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_boxes_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_capsules_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_convex_shapes_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_ragdolls_8206(JMS, armature, context, fix_rotations, primitive_shapes)
        read_hinges_8206(JMS, armature, context, fix_rotations, primitive_shapes)
        read_car_wheels_8210(JMS, armature, context, fix_rotations, primitive_shapes)
        read_point_to_points_8210(JMS, armature, context, fix_rotations, primitive_shapes)
        read_prismatics_8210(JMS, armature, context, fix_rotations, primitive_shapes)
        read_bounding_spheres_8209(JMS, armature, context)
    elif jms_version == 8212:
        read_nodes_8205(JMS, armature, node_names, jms_version, fix_rotations, valid_armature)
        read_materials_8197(JMS, game_title, materials, sections, section_map, triangle_material_map, random_color_gen, filepath, shader_gen_setting, report)
        read_markers_8206(JMS, context, game_title, armature, node_names, fix_rotations)
        read_xref_instances_8208(JMS, xref_instances)
        read_xref_markers_8203(JMS, context, armature, jms_version, xref_instances)
        vertices, vertex_normals, vertex_skinning_data, vertex_uv_data, vertex_colors = read_vertices_8211(JMS)
        triangles, triangle_material_ids, triangle_region_ids = read_triangles_8197(JMS, game_title, vertex_region_ids, section_map)
        read_spheres_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_boxes_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_capsules_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_convex_shapes_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_ragdolls_8206(JMS, armature, context, fix_rotations, primitive_shapes)
        read_hinges_8206(JMS, armature, context, fix_rotations, primitive_shapes)
        read_car_wheels_8210(JMS, armature, context, fix_rotations, primitive_shapes)
        read_point_to_points_8210(JMS, armature, context, fix_rotations, primitive_shapes)
        read_prismatics_8210(JMS, armature, context, fix_rotations, primitive_shapes)
        read_bounding_spheres_8209(JMS, armature, context)
        read_skylights_8212(JMS, armature, context)
    elif jms_version == 8213:
        read_nodes_8205(JMS, armature, node_names, jms_version, fix_rotations, valid_armature)
        read_materials_8197(JMS, game_title, materials, sections, section_map, triangle_material_map, random_color_gen, filepath, shader_gen_setting, report)
        read_markers_8206(JMS, context, game_title, armature, node_names, fix_rotations)
        read_xref_instances_8208(JMS, xref_instances)
        read_xref_markers_8203(JMS, context, armature, jms_version, xref_instances)
        vertices, vertex_normals, vertex_skinning_data, vertex_uv_data, vertex_colors = read_vertices_8211(JMS)
        triangles, triangle_material_ids, triangle_region_ids = read_triangles_8197(JMS, game_title, vertex_region_ids, section_map)
        read_spheres_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_boxes_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_capsules_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_convex_shapes_8207(JMS, armature, context, node_names, fix_rotations, primitive_shapes, materials, triangle_material_map, sections, section_map)
        read_ragdolls_8213(JMS, armature, context, fix_rotations, primitive_shapes)
        read_hinges_8206(JMS, armature, context, fix_rotations, primitive_shapes)
        read_car_wheels_8210(JMS, armature, context, fix_rotations, primitive_shapes)
        read_point_to_points_8210(JMS, armature, context, fix_rotations, primitive_shapes)
        read_prismatics_8210(JMS, armature, context, fix_rotations, primitive_shapes)
        read_bounding_spheres_8209(JMS, armature, context)
        read_skylights_8212(JMS, armature, context)

    object_name = bpy.path.basename(filepath).rsplit('.', 1)[0]
    if game_title == "halo1":
        if 'physics' in filepath or 'collision' in filepath:
            object_name = '@%s' % object_name

    else:
        if 'collision' in filepath:
            object_name = '@%s' % object_name

    if marker_data is not None:
        for marker_element in marker_data:
            marker_ob, region_idx = marker_element
            if region_idx >= 0:
                marker_ob.ass_jms.marker_region = sections[section_map[region_idx]]

    for section_idx, section in enumerate(sections):
        triangle_mask = triangle_region_ids == section_idx
        selected_triangles = triangles[triangle_mask]
        if len(selected_triangles) == 0:
            continue

        used_vertex_indices = np.unique(selected_triangles.ravel())
        selected_vertices = vertices[used_vertex_indices]
        remap = np.full(len(vertices), -1, dtype=np.int32)
        remap[used_vertex_indices] = np.arange(len(used_vertex_indices), dtype=np.int32)
        remapped_triangles = remap[selected_triangles]

        mesh = bpy.data.meshes.new(section)

        mesh.vertices.add(len(selected_vertices))
        mesh.loops.add(len(remapped_triangles) * 3)
        mesh.polygons.add(len(remapped_triangles))

        mesh.vertices.foreach_set("co", selected_vertices.ravel())
        mesh.loops.foreach_set("vertex_index", remapped_triangles.ravel())
        mesh.polygons.foreach_set("loop_start", np.arange(0, len(remapped_triangles) * 3, 3, dtype=np.int32))
        mesh.polygons.foreach_set("loop_total", np.full(len(remapped_triangles), 3, dtype=np.int32))
        mesh.update()

        object_mesh = bpy.data.objects.new(section, mesh)
        bpy.context.collection.objects.link(object_mesh)

        selected_normals = vertex_normals[used_vertex_indices]
        mesh.normals_split_custom_set_from_vertices(selected_normals)

        mesh.region_add(section)
        region_attribute = mesh.get_custom_attribute()
        region_attribute.data.foreach_set("value", np.ones(len(selected_triangles), dtype=np.int32))

        uv_layer_sets = []
        uv_count = len(vertex_uv_data)
        for uv_idx in range(uv_count):
            uv_name = "UVMap_Render"
            if uv_count > 1:
                uv_name += "_%s" % uv_idx

            layer_uv = mesh.uv_layers.new(name=uv_name)
            uv_layer_sets.append(layer_uv)
            selected_uvs = vertex_uv_data[uv_idx][used_vertex_indices]
            loop_uvs = selected_uvs[remapped_triangles]
            layer_uv.data.foreach_set("uv", loop_uvs.reshape(-1).ravel())

        if vertex_colors is not None:
            color_attribute = mesh.color_attributes.new(name="Color", type='FLOAT_COLOR', domain='CORNER')

            selected_colors = vertex_colors[used_vertex_indices]
            loop_colors = selected_colors[remapped_triangles]

            loop_colors = np.concatenate((loop_colors, np.ones((len(loop_colors), 1), dtype=loop_colors.dtype)), axis=1)
            color_attribute.data.foreach_set("color", loop_colors.reshape(-1).ravel())

        selected_material_ids = triangle_material_ids[triangle_mask]
        valid_materials = selected_material_ids >= 0
        selected_material_indices = np.full(len(selected_material_ids), -1, dtype=np.int32)
        selected_material_indices[valid_materials] = np.fromiter((triangle_material_map[material_id] for material_id in selected_material_ids[valid_materials]), dtype=np.int32, count=np.count_nonzero(valid_materials))
        used_material_indices = np.unique(selected_material_indices[valid_materials])
        material_map = np.full(len(materials), -1, dtype=np.int32)
        for local_index, material_index in enumerate(used_material_indices):
            mesh.materials.append(materials[material_index])
            material_map[material_index] = local_index

        material_indices = np.zeros(len(selected_material_indices), dtype=np.int32)
        material_indices[valid_materials] = material_map[selected_material_indices[valid_materials]]
        mesh.polygons.foreach_set("material_index", material_indices)

        vertex_groups = {}
        for local_vertex_idx, original_vertex_idx in enumerate(used_vertex_indices):
            vertex_skinning_set = vertex_skinning_data[original_vertex_idx]
            for node_index, node_weight in vertex_skinning_set:
                if node_index == -1:
                    node_index = 0

                if node_index == -1:
                    continue

                if node_index not in vertex_groups:

                    group = object_mesh.vertex_groups.new(
                        name=node_names[node_index]
                    )

                    vertex_groups[node_index] = group

                else:
                    group = vertex_groups[node_index]

                group.add([local_vertex_idx], node_weight, 'ADD')

        object_mesh.parent = armature
        mesh_processing.add_modifier(context, object_mesh, False, None, None, armature)

    report({'INFO'}, "Import completed successfully")
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.import_scene.jms()
