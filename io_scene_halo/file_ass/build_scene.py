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
import copy
import bmesh

from math import radians
from mathutils import Matrix
from .process_file import process_file
from ..global_functions import mesh_processing, shader_processing, global_functions
from ..file_tag.tag_interface import tag_interface, tag_common
from ..file_tag.tag_interface.tag_definitions import h1, h2

def find_root_instances(instances):
    root_instances_indices = []
    for instance_idx, instance in enumerate(instances):
        if instance.parent_id == -1:
            root_instances_indices.append(instance_idx)

    return root_instances_indices

def sort_by_parent(ASS):
    parent_index_list = []
    ordered_instances = []
    unordered_map = []

    instance_count = len(ASS.instances)
    loop_index = 0

    parent_nest = find_root_instances(ASS.instances)
    while len(parent_nest) > 0 and not loop_index >= instance_count:
        current_parent_nest = []
        current_parent_indices = set()
        for instance_index in parent_nest:
            instance_parent_id = ASS.instances[instance_index].parent_id
            if not instance_parent_id in parent_index_list:
                parent_index_list.append(instance_parent_id)

            current_parent_indices.add(instance_index)

        for instance_idx, instance in enumerate(ASS.instances):
            if instance.parent_id in current_parent_indices:
                current_parent_nest.append(instance_idx)

        loop_index += 1
        parent_nest = current_parent_nest

    for parent_idx, parent_index in enumerate(parent_index_list):
        for instance_idx, instance in enumerate(ASS.instances):
            if instance.parent_id == parent_index:
                ordered_instances.append(instance)
                unordered_map.append(instance_idx)

    for ordered_instance in ordered_instances:
        if ordered_instance.parent_id >= 0:
            ordered_instance.parent_id = unordered_map.index(ordered_instance.parent_id)

        for bone_group_idx, bone_group in enumerate(ordered_instance.bone_groups):
            if bone_group >= 0:
                ordered_instance.bone_groups[bone_group_idx] = unordered_map.index(bone_group)

    for ob in ASS.objects:
        for node_idx, node_index in enumerate(ob.node_index_list):
            if node_index >= 0:
                ob.node_index_list[node_idx] = unordered_map.index(node_index)

    return ordered_instances

def build_scene(context, filepath, report):
    ASS = process_file(filepath)
    game_title = global_functions.get_game_title(ASS.version, "ASS")

    generate_skeleton = False
    if os.path.basename(os.path.dirname(filepath)) == "render" and game_title == "halo3":
        generate_skeleton = True

    context.scene.halo.game_title = game_title

    collection = context.collection
    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors

    asset_cache = {}

    tag_groups = None
    engine_tag = None
    merged_defs = None
    if game_title == "halo1":
        output_dir = os.path.join(os.path.dirname(tag_common.h1_defs_directory), "h1_merged_output")
        tag_groups = tag_common.h1_tag_groups
        engine_tag = tag_interface.EngineTag.H1Latest.value
        merged_defs = h1.generate_defs(tag_common.h1_defs_directory, output_dir)
        tag_directory = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_tag_path
        
    elif game_title == "halo2":
        output_dir = os.path.join(os.path.dirname(tag_common.h1_defs_directory), "h2_merged_output")
        tag_groups = tag_common.h2_tag_groups
        engine_tag = tag_interface.EngineTag.H2Latest.value
        merged_defs = h2.generate_defs(tag_common.h2_defs_directory, output_dir)
        tag_directory = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_tag_path
    else:
        print("%s is not supported." % game_title)

    object_list = []
    vertex_weights_list = []
    blender_mats = []
    material_count = len(ASS.materials)
    for ass_mat in ASS.materials:
        material_name = ass_mat.name
        blend_mat = bpy.data.materials.new(name=material_name)
        if game_title == "halo1":
            shader_ref = shader_processing.find_h1_shader_tag(ASS.filepath, material_name)
            tag_interface.generate_tag_dictionary(game_title, shader_ref, tag_directory, tag_groups, engine_tag, merged_defs, asset_cache)
            shader_processing.generate_h1_shader(blend_mat, shader_ref, 0, asset_cache, report)
        elif game_title == "halo2":
            shader_ref = shader_processing.find_h2_shader_tag(ASS.filepath, material_name)
            tag_interface.generate_tag_dictionary(game_title, shader_ref, tag_directory, tag_groups, engine_tag, merged_defs, asset_cache)
            shader_processing.generate_h2_shader(blend_mat, shader_ref, 0, asset_cache, report)
        elif game_title == "halo3":
            shader_ref = shader_processing.find_h3_shader_tag(ASS.filepath, material_name)
            shader_processing.generate_h3_shader(blend_mat, shader_ref, asset_cache, report)

        global_functions.set_ass_material_properties(ass_mat, blend_mat)
        blend_mat.ass_jms.name_override = ass_mat.name
        blend_mat.diffuse_color = random_color_gen.next()

        blender_mats.append(blend_mat)

    ordered_instances = sort_by_parent(ASS)
    node_prefix_tuple = ('b ', 'b_', 'bone', 'frame', 'bip01')
    bone_instance_index_list = []
    bone_object_index_list = []
    for instance_idx, instance in enumerate(ordered_instances):
        object_index = instance.object_index
        if generate_skeleton and instance.name.startswith(node_prefix_tuple):
            bone_instance_index_list.append(instance_idx)
            if object_index >= 0 and not object_index in bone_object_index_list:
                bone_object_index_list.append(object_index)

    armature = None
    if len(bone_instance_index_list) > 0:
        armdata = bpy.data.armatures.new('Armature')
        armature = bpy.data.objects.new('Armature', armdata)
        armature.color = (1, 1, 1, 0)
        collection.objects.link(armature)
        for bone_instance in bone_instance_index_list:
            mesh_processing.select_object(context, armature)
            bpy.ops.object.mode_set(mode = 'EDIT')

            child_bone = armature.data.edit_bones.new(ordered_instances[bone_instance].name)
            child_bone.tail[2] = 1

            bpy.ops.object.mode_set(mode = 'OBJECT')

    for ob_idx, ass_object in enumerate(ASS.objects):
        mesh_name = "object_%s" % ob_idx

        geo_class = ass_object.geo_class
        object_radius = ass_object.radius
        object_height = ass_object.height
        object_extents = ass_object.extents
        object_material_index = ass_object.material_index

        vertex_weights_sets = None
        object_data = None
        if not ob_idx in bone_object_index_list:
            if geo_class == 'GENERIC_LIGHT':
                light_type = "POINT"
                if ass_object.light_properties.light_type == 'SPOT_LGT':
                    light_type = "SPOT"

                elif ass_object.light_properties.light_type == 'DIRECT_LGT':
                    light_type = "AREA"

                elif ass_object.light_properties.light_type == 'OMNI_LGT':
                    light_type = "POINT"

                elif ass_object.light_properties.light_type == 'AMBIENT_LGT':
                    light_type = "SUN"

                object_data = bpy.data.lights.new(mesh_name, light_type)
            else:
                object_data = bpy.data.meshes.new(mesh_name)
                object_data.ass_jms.XREF_path = ass_object.xref_filepath
                object_data.ass_jms.XREF_name = ass_object.xref_objectname


            if geo_class == 'GENERIC_LIGHT':
                object_data.color = (ass_object.light_properties.light_color)
                object_data.energy = (ass_object.light_properties.intensity)
                if ass_object.light_properties.light_type == 'SPOT_LGT' or ass_object.light_properties.light_type == 'DIRECT_LGT':
                    HFS = ass_object.light_properties.hotspot_falloff_size
                    HS = ass_object.light_properties.hotspot_size
                    if ass_object.light_properties.light_type == 'DIRECT_LGT':
                        light_shape_type = "DISK"
                        if not ass_object.light_properties.light_shape == 0:
                            light_shape_type = "RECTANGLE"

                        object_data.shape = light_shape_type

                    else:
                        object_data.spot_size = radians(HFS)
                        object_data.spot_blend = (HFS - HS) / HFS

                    object_data.halo_light.spot_size = radians(HFS)
                    object_data.halo_light.spot_blend = (HFS - HS) / HFS

                    object_data.halo_light.light_cone_shape = str(ass_object.light_properties.light_shape)
                    object_data.halo_light.light_aspect_ratio = ass_object.light_properties.light_aspect_ratio

                    object_data.halo_light.use_near_atten = bool(ass_object.light_properties.uses_near_attenuation)
                    object_data.halo_light.near_atten_start = ass_object.light_properties.near_attenuation_start
                    object_data.halo_light.near_atten_end = ass_object.light_properties.near_attenuation_end
                    object_data.halo_light.use_far_atten = bool(ass_object.light_properties.uses_far_attenuation)
                    object_data.halo_light.far_atten_start = ass_object.light_properties.far_attenuation_start
                    object_data.halo_light.far_atten_end = ass_object.light_properties.far_attenuation_end

            elif geo_class == 'PILL':
                bm = bmesh.new()
                bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=12, radius1=1, radius2=1, depth=2)
                bm.transform(Matrix.Translation((0, 0, 1)))

                object_data.ass_jms.Object_Type = 'CAPSULES'
                object_dimension = object_radius * 2
                bmesh.ops.scale(bm, vec=(object_dimension, object_dimension, (object_dimension + object_height)), verts=bm.verts)

                bm.to_mesh(object_data)
                bm.free()

                if 0 <= object_material_index < material_count:
                    object_data.materials.append(blender_mats[object_material_index])

                    current_variant = ASS.materials[object_material_index].variant
                    if not global_functions.string_empty_check(current_variant) and not current_variant in object_data.region_list.keys():
                        object_data.region_add(current_variant)

            elif geo_class == 'SPHERE':
                bm = bmesh.new()
                bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)

                object_data.ass_jms.Object_Type = 'SPHERE'
                object_dimension = object_radius * 2
                bmesh.ops.scale(bm, vec=(object_dimension, object_dimension, object_dimension), verts=bm.verts)

                bm.to_mesh(object_data)
                bm.free()

                if 0 <= object_material_index < material_count:
                    object_data.materials.append(blender_mats[object_material_index])

                    current_variant = ASS.materials[object_material_index].variant
                    if not global_functions.string_empty_check(current_variant) and not current_variant in object_data.region_list.keys():
                        object_data.region_add(current_variant)

            elif geo_class == 'BOX':
                bm = bmesh.new()
                bmesh.ops.create_cube(bm, size=1.0)

                object_data.ass_jms.Object_Type = 'BOX'
                bmesh.ops.scale(bm, vec=((object_extents[0] * 2), (object_extents[1] * 2), (object_extents[2] * 2)), verts=bm.verts)

                bm.to_mesh(object_data)
                bm.free()

                if 0 <= object_material_index < material_count:
                    object_data.materials.append(blender_mats[object_material_index])

                    current_variant = ASS.materials[object_material_index].variant
                    if not global_functions.string_empty_check(current_variant) and not current_variant in object_data.region_list.keys():
                        object_data.region_add(current_variant)

            elif geo_class == 'MESH':
                vertex_weights_sets = mesh_processing.generate_mesh_retail(context, ASS, ass_object.vertices, ass_object.triangles, object_data, game_title, random_color_gen, blender_mats, asset_cache, material_count, report)

        vertex_weights_list.append(vertex_weights_sets)
        object_list.append(object_data)

    instances = []
    global_transforms = []
    visited_objects = [False for object in object_list]

    for instance_idx, instance_element in enumerate(ordered_instances):
        object_index = instance_element.object_index
        unique_id = instance_element.unique_id

        local_transform = instance_element.local_transform
        local_scale = (local_transform.scale, local_transform.scale, local_transform.scale)
        if ASS.version == 1:
            local_scale = local_transform.scale

        global_transform = Matrix.LocRotScale(local_transform.translation, local_transform.rotation, local_scale)
        parent_index = instance_element.parent_id
        if not parent_index == -1:
            parent_matrix = global_transforms[parent_index]
            global_transform = parent_matrix @ global_transform

        global_transforms.append(global_transform)

        if not unique_id == -1 and not instance_idx in bone_instance_index_list:
            pivot_transform = instance_element.pivot_transform
            pivot_scale = (pivot_transform.scale, pivot_transform.scale, pivot_transform.scale)
            if ASS.version == 1:
                pivot_scale = pivot_transform.scale

            pivot_matrix = Matrix.LocRotScale(pivot_transform.translation, pivot_transform.rotation, pivot_scale)

            mesh = None
            vertex_weights_set = None
            xref = False
            if not object_index == -1:
                mesh = object_list[object_index]
                vertex_weights_set = vertex_weights_list[object_index]
                if hasattr(mesh, 'ass_jms') and not len(mesh.ass_jms.XREF_path) == 0:
                    xref = True

            instance_name_override = ""
            if context.scene.objects.get(instance_element.name):
                instance_name_override = instance_element.name

            instance = bpy.data.objects.new(instance_element.name, mesh)
            instance.color = (1, 1, 1, 0)
            collection.objects.link(instance)
            instances.append(instance)

            instance.ass_jms.name_override = instance_name_override
            instance.ass_jms.unique_id = str(instance_element.unique_id)

            if (4, 1, 0) > bpy.app.version and instance.type == 'MESH':
                instance.data.use_auto_smooth = True

            if not vertex_weights_set == None:
                for bone_goup in instance_element.bone_groups:
                    instance.vertex_groups.new(name = ordered_instances[bone_goup].name)

                for vertex_weights_idx, vertex_weights in enumerate(vertex_weights_set):
                    for node_set in vertex_weights:
                        group_index = node_set[0]
                        node_weight = node_set[1]
                        instance.vertex_groups[group_index].add([vertex_weights_idx], node_weight, 'ADD')

            if xref and instance.type == 'MESH' and not visited_objects[object_index]:
                visited_objects[object_index] = True
                bm = bmesh.new()
                bm.from_mesh(instance.data)
                bmesh.ops.transform(bm, matrix=pivot_matrix, space=Matrix.Identity(4), verts=bm.verts)
                bm.to_mesh(instance.data)
                bm.free()

        else:
            instances.append(None)

    for instance_idx, instance_element in enumerate(ordered_instances):
        object_index = instance_element.object_index
        unique_id = instance_element.unique_id

        if not unique_id == -1:
            local_transform = instance_element.local_transform
            pivot_transform = instance_element.pivot_transform
            local_scale = (local_transform.scale, local_transform.scale, local_transform.scale)
            pivot_scale = (pivot_transform.scale, pivot_transform.scale, pivot_transform.scale)
            if ASS.version == 1:
                local_scale = local_transform.scale
                pivot_scale = pivot_transform.scale

            instance = instances[instance_idx]
            if not instance_idx in bone_instance_index_list:
                xref = False
                if not object_index == -1 and instance.type == "MESH" and not len(instance.data.ass_jms.XREF_path) == 0:
                    xref = True

                local_matrix = Matrix.LocRotScale(local_transform.translation, local_transform.rotation, local_scale)
                pivot_matrix = Matrix.LocRotScale(pivot_transform.translation, pivot_transform.rotation, pivot_scale)
                full_transform = local_matrix
                if not xref:
                    full_transform = local_matrix @ pivot_matrix

                parent_object = None
                parent_index = instance_element.parent_id
                if not parent_index == -1:
                    parent_object = instances[parent_index]
                    full_transform = global_transforms[parent_index] @ full_transform

                if len(instance_element.bone_groups) > 0:
                    mesh_processing.add_modifier(context, instance, False, None, armature)

                if parent_index in bone_instance_index_list:
                    instance.parent = armature
                    instance.parent_type = "BONE"
                    instance.parent_bone = ordered_instances[parent_index].name
                else:
                    instance.parent = parent_object

                instance.matrix_world = full_transform
            else:
                local_matrix = Matrix.LocRotScale(local_transform.translation, local_transform.rotation, local_scale)
                pivot_matrix = Matrix.LocRotScale(pivot_transform.translation, pivot_transform.rotation, pivot_scale)
                full_transform = local_matrix @ pivot_matrix

                parent_index = instance_element.parent_id

                mesh_processing.select_object(context, armature)
                bpy.ops.object.mode_set(mode = 'EDIT')

                child_bone = armature.data.edit_bones.get(instance_element.name)
                if parent_index >= 0 and parent_index in bone_instance_index_list:
                    instance_name = ordered_instances[parent_index].name
                    child_bone.parent = armature.data.edit_bones.get(instance_name)
                    full_transform = global_transforms[parent_index] @ full_transform

                child_bone.matrix = full_transform

                bpy.ops.object.mode_set(mode = 'OBJECT')

    report({'INFO'}, "Import completed successfully")
    return {'FINISHED'}
