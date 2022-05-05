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
from mathutils import Matrix
from .process_file import process_file
from ..global_functions import mesh_processing, global_functions

def set_ass_material_properties(ass_mat, mat):
    material_effect = ass_mat.material_effect
    material_strings = ass_mat.material_strings
    mat.ass_jms.material_effect = material_effect
    if len(material_strings) > 0:
        mat.ass_jms.is_bm = True

    for string in material_strings:
        if string.startswith("BM_FLAGS"):
            string_bitfield = string.split()[1] #Split the string and retrieve the bitfield.
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
            mat.ass_jms.slip_surface = int(string_bitfield[21])

        elif string.startswith("BM_LMRES"):
            lmres_string_args = string.split()
            mat.ass_jms.lightmap_res = float(lmres_string_args[1])
            mat.ass_jms.photon_fidelity = int(lmres_string_args[2])
            mat.ass_jms.two_sided_transparent_tint = (float(lmres_string_args[3]), float(lmres_string_args[4]), float(lmres_string_args[5]))
            if len(lmres_string_args) > 6:
                mat.ass_jms.override_lightmap_transparency = int(lmres_string_args[6])
                mat.ass_jms.additive_transparency = (float(lmres_string_args[7]), float(lmres_string_args[8]), float(lmres_string_args[9]))
                mat.ass_jms.use_shader_gel = int(lmres_string_args[10])
                if len(lmres_string_args) > 11:
                    mat.ass_jms.ignore_default_res_scale = int(lmres_string_args[11])

        elif string.startswith("BM_LIGHTING_BASIC"):
            lighting_basic_args = string.split()
            mat.ass_jms.power = float(lighting_basic_args[1])
            mat.ass_jms.color = (float(lighting_basic_args[2]), float(lighting_basic_args[3]), float(lighting_basic_args[4]))
            mat.ass_jms.quality = float(lighting_basic_args[5])
            mat.ass_jms.power_per_unit_area = int(lighting_basic_args[6])
            if len(lmres_string_args) > 7:
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

def build_scene(context, filepath, report):
    ASS = process_file(filepath)

    collection = context.collection
    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors
    mesh_vertex_groups = []

    mesh_processing.deselect_objects(context)

    for idx, ass_mat in enumerate(ASS.materials):
        material_name = ass_mat.name

        mat = bpy.data.materials.get(material_name)
        if mat is None:
            mat = bpy.data.materials.new(name=material_name)

        set_ass_material_properties(ass_mat, mat)
        mat.ass_jms.name_override = ass_mat.asset_name
        mat.diffuse_color = random_color_gen.next()

    object_list = []
    mesh_list = []
    object_index_list = []
    for idx, instance in enumerate(ASS.instances):
        object_index = instance.object_index
        unique_id = instance.unique_id

        pivot_transform = instance.pivot_transform

        pivot_scale = (pivot_transform.scale, pivot_transform.scale, pivot_transform.scale)
        if ASS.version == 1:
            pivot_scale = pivot_transform.scale

        pivot_transform = Matrix.LocRotScale(pivot_transform.translation, pivot_transform.rotation, pivot_scale)

        geo_class = 'EMPTY'
        object_radius = 2
        object_height = 1
        object_extents = [1.0, 1.0, 1.0]

        if not unique_id == -1:
            if not object_index in object_index_list:
                if not object_index == -1:
                    object_index_list.append(object_index)
                    object_element = ASS.objects[object_index]
                    geo_class = object_element.geo_class
                    object_radius = object_element.radius
                    object_height = object_element.height
                    object_extents = object_element.extents
                    object_material_index = object_element.material_index

                    light_type = "POINT"
                    if geo_class == 'GENERIC_LIGHT':
                        if object_element.light_properties.light_type == 'SPOT_LGT':
                            light_type = "SPOT"

                        elif object_element.light_properties.light_type == 'DIRECT_LGT':
                            light_type = "AREA"

                        elif object_element.light_properties.light_type == 'OMNI_LGT':
                            light_type = "POINT"

                        elif object_element.light_properties.light_type == 'AMBIENT_LGT':
                            light_type = "SUN"

                    if geo_class == 'GENERIC_LIGHT':
                        object_data = bpy.data.lights.new(instance.name, light_type)
                    else:
                        object_data = bpy.data.meshes.new("%s" % idx)

                    object_mesh = bpy.data.objects.new(instance.name, object_data)
                    collection.objects.link(object_mesh)

                    if not geo_class == 'GENERIC_LIGHT':
                        object_mesh.data.ass_jms.XREF_path = object_element.xref_filepath

                    if geo_class == 'GENERIC_LIGHT':
                        object_mesh.data.color = (object_element.light_properties.light_color)
                        object_mesh.data.energy = (object_element.light_properties.intensity)
                        if object_element.light_properties.light_type == 'SPOT_LGT' or object_element.light_properties.light_type == 'DIRECT_LGT':
                            if object_element.light_properties.light_type == 'DIRECT_LGT':
                                light_shape_type = "DISK"
                                if not object_element.light_properties.light_shape == 0:
                                    light_shape_type = "RECTANGLE"

                                object_mesh.data.shape = light_shape_type

                            else:
                                object_mesh.data.spot_size = radians(object_element.light_properties.hotspot_size)
                                object_mesh.data.spot_blend = object_element.light_properties.hotspot_falloff_size / object_element.light_properties.hotspot_size

                            object_mesh.data.halo_light.spot_size = radians(object_element.light_properties.hotspot_size)
                            object_mesh.data.halo_light.spot_blend = object_element.light_properties.hotspot_falloff_size / object_element.light_properties.hotspot_size

                            object_mesh.data.halo_light.light_cone_shape = str(object_element.light_properties.light_shape)
                            object_mesh.data.halo_light.light_aspect_ratio = object_element.light_properties.light_aspect_ratio

                            object_mesh.data.halo_light.use_near_atten = bool(object_element.light_properties.uses_near_attenuation)
                            object_mesh.data.halo_light.near_atten_start = object_element.light_properties.near_attenuation_start
                            object_mesh.data.halo_light.near_atten_end = object_element.light_properties.near_attenuation_end
                            object_mesh.data.halo_light.use_far_atten = bool(object_element.light_properties.uses_far_attenuation)
                            object_mesh.data.halo_light.far_atten_start = object_element.light_properties.far_attenuation_start
                            object_mesh.data.halo_light.far_atten_end = object_element.light_properties.far_attenuation_end

                    elif geo_class == 'PILL':
                        set_primitive_material(object_material_index, ASS, object_data)

                        bm = bmesh.new()
                        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=12, radius1=1, radius2=1, depth=2)
                        bm.transform(Matrix.Translation((0, 0, 1)))
                        
                        bmesh.ops.transform(bm, matrix=pivot_transform, verts=bm.verts)
                        
                        bm.to_mesh(object_data)
                        bm.free()

                        object_mesh.data.ass_jms.Object_Type = 'CAPSULES'
                        object_dimension = object_radius * 2
                        object_mesh.dimensions = (object_dimension, object_dimension, (object_dimension + object_height))

                        mesh_processing.select_object(context, object_mesh)
                        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                        mesh_processing.deselect_objects(context)

                    elif geo_class == 'SPHERE':
                        set_primitive_material(object_material_index, ASS, object_data)

                        bm = bmesh.new()
                        bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=1)
                        
                        bmesh.ops.transform(bm, matrix=pivot_transform, verts=bm.verts)
                        
                        bm.to_mesh(object_data)
                        bm.free()

                        object_mesh.data.ass_jms.Object_Type = 'SPHERE'
                        object_dimension = object_radius * 2
                        object_mesh.dimensions = (object_dimension, object_dimension, object_dimension)

                        mesh_processing.select_object(context, object_mesh)
                        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                        mesh_processing.deselect_objects(context)

                    elif geo_class == 'BOX':
                        set_primitive_material(object_material_index, ASS, object_data)

                        bm = bmesh.new()
                        bmesh.ops.create_cube(bm, size=1.0)
                        
                        bmesh.ops.transform(bm, matrix=pivot_transform, verts=bm.verts)
                        
                        bm.to_mesh(object_data)
                        bm.free()

                        object_mesh.data.ass_jms.Object_Type = 'BOX'
                        object_mesh.dimensions = ((object_extents[0] * 2), (object_extents[1] * 2), (object_extents[2] * 2))

                        mesh_processing.select_object(context, object_mesh)
                        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                        mesh_processing.deselect_objects(context)

                    elif geo_class == 'MESH':
                        bm, vert_normal_list = mesh_processing.process_mesh_import_data('halo3', ASS, object_element, object_mesh, random_color_gen, 'ASS', 0, None, None, None, False)

                        bmesh.ops.transform(bm, matrix=pivot_transform, verts=bm.verts)

                        bm.to_mesh(object_data)
                        bm.free()
                        object_mesh.data.normals_split_custom_set(vert_normal_list)
                        object_mesh.data.use_auto_smooth = True

                        for vertex_groups in mesh_vertex_groups:
                            for group in vertex_groups:
                                if not group in object_mesh.vertex_groups:
                                    object_mesh.vertex_groups.new(name = group)

                    mesh_list.append(object_data)

                else:
                    object_mesh = bpy.data.objects.new(instance.name, None)
                    collection.objects.link(object_mesh)

            else:
                object_mesh = bpy.data.objects.new(instance.name, mesh_list[object_index])
                collection.objects.link(object_mesh)

            object_list.append(object_mesh)

        else:
            if not None in object_list:
                object_list.append(None)

    for idx, instance in enumerate(ASS.instances):
        object_index = instance.object_index
        unique_id = instance.unique_id

        geo_class = 'EMPTY'

        local_transform = instance.local_transform

        local_scale = (local_transform.scale, local_transform.scale, local_transform.scale)
        if ASS.version == 1:
            local_scale = local_transform.scale

        if not unique_id == -1:
            object_list[idx].location = local_transform.translation
            object_list[idx].rotation_euler = local_transform.rotation.to_euler()
            object_list[idx].scale = local_scale

            parent_index = instance.parent_id
            if not parent_index == -1:
                parent_instance = ASS.instances[parent_index]
                parent_unique_id = parent_instance.unique_id
                parent_parent_id = parent_instance.parent_id
                if parent_unique_id >= -1 and parent_parent_id >= -1:
                    object_list[idx].parent = object_list[parent_index]

    report({'INFO'}, "Import completed successfully")
    return {'FINISHED'}
