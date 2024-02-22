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

from math import radians
from mathutils import Matrix
from .process_file import process_file
from ..global_functions import mesh_processing, global_functions

def set_ass_material_properties(ass_mat, mat):
    material_strings = ass_mat.material_strings
    if len(material_strings) > 0:
        mat.ass_jms.is_bm = True

    for string in material_strings:
        if string.startswith("BM_FLAGS"):
            string_bitfield = string.split()[1] #Split the string and retrieve the bitfield.
            settings_count = len(string_bitfield)
            mat.ass_jms.two_sided = int(string_bitfield[0])
            mat.ass_jms.transparent_1_sided = int(string_bitfield[1])
            mat.ass_jms.transparent_2_sided = int(string_bitfield[2])
            mat.ass_jms.render_only = int(string_bitfield[3])
            mat.ass_jms.collision_only = int(string_bitfield[4])
            mat.ass_jms.sphere_collision_only = int(string_bitfield[5])
            mat.ass_jms.fog_plane = int(string_bitfield[6])
            mat.ass_jms.ladder = int(string_bitfield[7])
            mat.ass_jms.breakable = int(string_bitfield[8])
            mat.ass_jms.ai_deafening = int(string_bitfield[9])
            mat.ass_jms.no_shadow = int(string_bitfield[10])
            mat.ass_jms.shadow_only = int(string_bitfield[11])
            mat.ass_jms.lightmap_only = int(string_bitfield[12])
            mat.ass_jms.precise = int(string_bitfield[13])
            mat.ass_jms.conveyor = int(string_bitfield[14])
            mat.ass_jms.portal_1_way = int(string_bitfield[15])
            mat.ass_jms.portal_door = int(string_bitfield[16])
            mat.ass_jms.portal_vis_blocker = int(string_bitfield[17])
            mat.ass_jms.ignored_by_lightmaps = int(string_bitfield[18])
            mat.ass_jms.blocks_sound = int(string_bitfield[19])
            mat.ass_jms.decal_offset = int(string_bitfield[20])
            if settings_count >= 22:
                mat.ass_jms.slip_surface = int(string_bitfield[21])

        elif string.startswith("BM_LMRES"):
            lmres_string_args = string.split()
            lmres_count = len(lmres_string_args) - 1
            mat.ass_jms.lightmap_res = float(lmres_string_args[1])
            mat.ass_jms.photon_fidelity = int(lmres_string_args[2])
            if lmres_count >= 3:
                transparent_color = float(lmres_string_args[3])
                mat.ass_jms.two_sided_transparent_tint = (transparent_color, transparent_color, transparent_color)
            else:
                mat.ass_jms.two_sided_transparent_tint = (float(lmres_string_args[3]), float(lmres_string_args[4]), float(lmres_string_args[5]))
            if lmres_count >= 6:
                mat.ass_jms.override_lightmap_transparency = int(lmres_string_args[6])
                mat.ass_jms.additive_transparency = (float(lmres_string_args[7]), float(lmres_string_args[8]), float(lmres_string_args[9]))
                mat.ass_jms.use_shader_gel = int(lmres_string_args[10])
            if lmres_count >= 11:
                mat.ass_jms.ignore_default_res_scale = int(lmres_string_args[11])

        elif string.startswith("BM_LIGHTING_BASIC"):
            lighting_basic_args = string.split()
            lighting_count = len(lighting_basic_args) - 1
            mat.ass_jms.power = float(lighting_basic_args[1])
            mat.ass_jms.color = (float(lighting_basic_args[2]), float(lighting_basic_args[3]), float(lighting_basic_args[4]))
            mat.ass_jms.quality = float(lighting_basic_args[5])
            if lighting_count >= 6:
                mat.ass_jms.power_per_unit_area = int(lighting_basic_args[6])
            if lighting_count >= 7:
                mat.ass_jms.emissive_focus = float(lighting_basic_args[7])

        elif string.startswith("BM_LIGHTING_ATTEN"):
            lighting_attenuation_args = string.split()
            mat.ass_jms.attenuation_enabled = int(lighting_attenuation_args[1])
            mat.ass_jms.falloff_distance = float(lighting_attenuation_args[2])
            mat.ass_jms.cutoff_distance = float(lighting_attenuation_args[3])

        elif string.startswith("BM_LIGHTING_FRUS"):
            lighting_frus_args = string.split()
            mat.ass_jms.frustum_blend = float(lighting_frus_args[1])
            mat.ass_jms.frustum_falloff = float(lighting_frus_args[2])
            mat.ass_jms.frustum_cutoff = float(lighting_frus_args[3])

def set_primitive_material(object_material_index, ASS, mesh):
    if not object_material_index == -1:
        mat = ASS.materials[object_material_index]
        if mesh.materials:
            mesh.materials[0] = bpy.data.materials[mat.name]

def sort_by_parent(instances):
    instance_count = len(instances)
    iteration_count = 0
    instance_list = instances
    ordered_list = []
    unordered_map = []
    layer_index_list = [-1]
    while not len(ordered_list) == instance_count and not iteration_count == instance_count:
        layer_list = []
        layer_instance_list = []
        for instance_idx, instance in enumerate(instance_list):
            if instance.parent_id in layer_index_list:
                layer_list.append(instance_idx)
                unordered_map.append(instance_idx)
                layer_instance_list.append(instance)

        iteration_count += 1
        ordered_list = ordered_list + layer_instance_list
        layer_index_list = layer_list

    return ordered_list, unordered_map

def build_scene(context, filepath, report):
    ASS = process_file(filepath)

    collection = context.collection
    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors

    object_list = []
    object_settings_list = []
    for idx, ass_mat in enumerate(ASS.materials):
        material_name = ass_mat.name

        mat = bpy.data.materials.get(material_name)
        if mat is None:
            mat = bpy.data.materials.new(name=material_name)

        set_ass_material_properties(ass_mat, mat)
        mat.ass_jms.name_override = ass_mat.asset_name
        if len(mat.ass_jms.name_override) > 0:
            mat.ass_jms.is_bm = True

        mat.diffuse_color = random_color_gen.next()

    for ass_object in ASS.objects:
        mesh_name = "object_%s" % idx

        geo_class = ass_object.geo_class
        object_radius = ass_object.radius
        object_height = ass_object.height
        object_extents = ass_object.extents
        object_material_index = ass_object.material_index

        light_type = "POINT"
        if geo_class == 'GENERIC_LIGHT':
            if ass_object.light_properties.light_type == 'SPOT_LGT':
                light_type = "SPOT"

            elif ass_object.light_properties.light_type == 'DIRECT_LGT':
                light_type = "AREA"

            elif ass_object.light_properties.light_type == 'OMNI_LGT':
                light_type = "POINT"

            elif ass_object.light_properties.light_type == 'AMBIENT_LGT':
                light_type = "SUN"

        if geo_class == 'GENERIC_LIGHT':
            object_data = bpy.data.lights.new(mesh_name, light_type)
        else:
            object_data = bpy.data.meshes.new(mesh_name)
            object_data.ass_jms.XREF_path = ass_object.xref_filepath
            object_data.ass_jms.XREF_name = ass_object.xref_objectname

        object_settings = None
        if geo_class == 'GENERIC_LIGHT':
            object_data.color = (ass_object.light_properties.light_color)
            object_data.energy = (ass_object.light_properties.intensity)
            if ass_object.light_properties.light_type == 'SPOT_LGT' or ass_object.light_properties.light_type == 'DIRECT_LGT':
                if ass_object.light_properties.light_type == 'DIRECT_LGT':
                    light_shape_type = "DISK"
                    if not ass_object.light_properties.light_shape == 0:
                        light_shape_type = "RECTANGLE"

                    object_data.shape = light_shape_type

                else:
                    object_data.spot_size = radians(ass_object.light_properties.hotspot_size)
                    if not ass_object.light_properties.hotspot_size == 0.0:
                        object_data.spot_blend = ass_object.light_properties.hotspot_falloff_size / ass_object.light_properties.hotspot_size

                object_data.halo_light.spot_size = radians(ass_object.light_properties.hotspot_size)
                if not ass_object.light_properties.hotspot_size == 0.0:
                    object_data.halo_light.spot_blend = ass_object.light_properties.hotspot_falloff_size / ass_object.light_properties.hotspot_size

                object_data.halo_light.light_cone_shape = str(ass_object.light_properties.light_shape)
                object_data.halo_light.light_aspect_ratio = ass_object.light_properties.light_aspect_ratio

                object_data.halo_light.use_near_atten = bool(ass_object.light_properties.uses_near_attenuation)
                object_data.halo_light.near_atten_start = ass_object.light_properties.near_attenuation_start
                object_data.halo_light.near_atten_end = ass_object.light_properties.near_attenuation_end
                object_data.halo_light.use_far_atten = bool(ass_object.light_properties.uses_far_attenuation)
                object_data.halo_light.far_atten_start = ass_object.light_properties.far_attenuation_start
                object_data.halo_light.far_atten_end = ass_object.light_properties.far_attenuation_end

        elif geo_class == 'PILL':
            set_primitive_material(object_material_index, ASS, object_data)

            bm = bmesh.new()
            bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=12, radius1=1, radius2=1, depth=2)
            bm.transform(Matrix.Translation((0, 0, 1)))

            object_data.ass_jms.Object_Type = 'CAPSULES'
            object_dimension = object_radius * 2
            bmesh.ops.scale(bm, vec=(object_dimension, object_dimension, (object_dimension + object_height)), verts=bm.verts)

            bm.to_mesh(object_data)
            bm.free()

        elif geo_class == 'SPHERE':
            set_primitive_material(object_material_index, ASS, object_data)

            bm = bmesh.new()
            bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)

            object_data.ass_jms.Object_Type = 'SPHERE'
            object_dimension = object_radius * 2
            bmesh.ops.scale(bm, vec=(object_dimension, object_dimension, object_dimension), verts=bm.verts)

            bm.to_mesh(object_data)
            bm.free()

        elif geo_class == 'BOX':
            set_primitive_material(object_material_index, ASS, object_data)

            bm = bmesh.new()
            bmesh.ops.create_cube(bm, size=1.0)

            object_data.ass_jms.Object_Type = 'BOX'
            bmesh.ops.scale(bm, vec=((object_extents[0] * 2), (object_extents[1] * 2), (object_extents[2] * 2)), verts=bm.verts)

            bm.to_mesh(object_data)
            bm.free()

        elif geo_class == 'MESH':
            vertex_weights_sets, regions = mesh_processing.generate_mesh_retail(context, ASS, ass_object.vertices, ass_object.triangles, object_data, "halo3", random_color_gen)
            object_settings = (vertex_weights_sets, regions)

        object_settings_list.append(object_settings)
        object_list.append(object_data)

    instances = []
    global_transforms = []
    visited_objects = [False for object in object_list]
    for idx, instance_element in enumerate(ASS.instances):
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

        if not unique_id == -1:
            pivot_transform = instance_element.pivot_transform
            pivot_scale = (pivot_transform.scale, pivot_transform.scale, pivot_transform.scale)
            if ASS.version == 1:
                pivot_scale = pivot_transform.scale

            pivot_matrix = Matrix.LocRotScale(pivot_transform.translation, pivot_transform.rotation, pivot_scale)

            mesh = None
            object_setings = None
            xref = False
            if not object_index == -1:
                mesh = object_list[object_index]
                object_setings = object_settings_list[object_index]
                if hasattr(mesh, 'ass_jms') and not len(mesh.ass_jms.XREF_path) == 0:
                    xref = True

            instance_name_override = ""
            if context.scene.objects.get(instance_element.name):
                instance_name_override = instance_element.name

            instance = bpy.data.objects.new(instance_element.name, mesh)
            collection.objects.link(instance)
            instances.append(instance)

            instance.ass_jms.name_override = instance_name_override
            instance.ass_jms.unique_id = str(instance_element.unique_id)

            if not object_setings == None:
                vertex_weights_sets = object_setings[0]
                regions = object_setings[1]

                for bone_goup in instance_element.bone_groups:
                    instance.vertex_groups.new(name = ASS.instances[bone_goup].name)

                for vertex_weights_set_idx, vertex_weights_set in enumerate(vertex_weights_sets):
                    for node_set in vertex_weights_set:
                        group_index = node_set[0]
                        node_weight = node_set[1]
                        instance.vertex_groups[group_index].add([vertex_weights_set_idx], node_weight, 'ADD')

                for region in regions:
                    if not global_functions.string_empty_check(region):
                        instance.region_add(region)

            if xref and instance.type == 'MESH' and not visited_objects[object_index]:
                visited_objects[object_index] = True
                bm = bmesh.new()
                bm.from_mesh(instance.data)
                bmesh.ops.transform(bm, matrix=pivot_matrix, space=Matrix.Identity(4), verts=bm.verts)
                bm.to_mesh(instance.data)
                bm.free()

        else:
            instances.append(None)

    for idx, instance_element in enumerate(ASS.instances):
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

            instance = instances[idx]

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

            instance.parent = parent_object
            instance.matrix_world = full_transform

    report({'INFO'}, "Import completed successfully")
    return {'FINISHED'}
