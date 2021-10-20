# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2020 Dave Barnes and Steven Garcia
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
import socket

from decimal import *
from math import degrees
from getpass import getuser
from ..global_functions import mesh_processing
from ..global_functions import global_functions

def get_material_strings(material, version):
    material_strings = []
    bm_flags = "BM_FLAGS "
    bm_lmres = "BM_LMRES "
    bm_lighting_basic = "BM_LIGHTING_BASIC "
    bm_lighting_atten = "BM_LIGHTING_ATTEN "
    bm_lighting_frus = "BM_LIGHTING_FRUS "

    bm_flags += str(int(material.ass_jms.two_sided))
    bm_flags += str(int(material.ass_jms.transparent_1_sided))
    bm_flags += str(int(material.ass_jms.transparent_2_sided))
    bm_flags += str(int(material.ass_jms.render_only))
    bm_flags += str(int(material.ass_jms.collision_only))
    bm_flags += str(int(material.ass_jms.sphere_collision_only))
    bm_flags += str(int(material.ass_jms.fog_plane))
    bm_flags += str(int(material.ass_jms.ladder))
    bm_flags += str(int(material.ass_jms.breakable))
    bm_flags += str(int(material.ass_jms.ai_deafening))
    bm_flags += str(int(material.ass_jms.no_shadow))
    bm_flags += str(int(material.ass_jms.shadow_only))
    bm_flags += str(int(material.ass_jms.lightmap_only))
    bm_flags += str(int(material.ass_jms.precise))
    bm_flags += str(int(material.ass_jms.conveyor))
    bm_flags += str(int(material.ass_jms.portal_1_way))
    bm_flags += str(int(material.ass_jms.portal_door))
    bm_flags += str(int(material.ass_jms.portal_vis_blocker))
    bm_flags += str(int(material.ass_jms.ignored_by_lightmaps))
    bm_flags += str(int(material.ass_jms.blocks_sound))
    bm_flags += str(int(material.ass_jms.decal_offset))
    bm_flags += str(int(material.ass_jms.slip_surface))

    bm_lmres += '%0.10f ' % material.ass_jms.lightmap_res
    bm_lmres += '%s ' % int(material.ass_jms.photon_fidelity)
    bm_lmres += '%0.10f ' % material.ass_jms.two_sided_transparent_tint[0]
    bm_lmres += '%0.10f ' % material.ass_jms.two_sided_transparent_tint[1]
    bm_lmres += '%0.10f ' % material.ass_jms.two_sided_transparent_tint[2]
    if version >= 5:
        bm_lmres += '%s ' % int(material.ass_jms.override_lightmap_transparency)
        bm_lmres += '%0.10f ' % material.ass_jms.additive_transparency[0]
        bm_lmres += '%0.10f ' % material.ass_jms.additive_transparency[1]
        bm_lmres += '%0.10f ' % material.ass_jms.additive_transparency[2]
        bm_lmres += '%s ' % int(material.ass_jms.use_shader_gel)
        bm_lmres += '%s' % int(material.ass_jms.ignore_default_res_scale)

    bm_lighting_basic += '%0.10f ' % material.ass_jms.power
    bm_lighting_basic += '%0.10f ' % material.ass_jms.color[0]
    bm_lighting_basic += '%0.10f ' % material.ass_jms.color[1]
    bm_lighting_basic += '%0.10f ' % material.ass_jms.color[2]
    bm_lighting_basic += '%0.10f ' % material.ass_jms.quality
    bm_lighting_basic += '%s ' % int(material.ass_jms.power_per_unit_area)
    if version >= 5:
        bm_lighting_basic += '%0.10f' % material.ass_jms.emissive_focus

    bm_lighting_atten += '%s ' % int(material.ass_jms.attenuation_enabled)
    bm_lighting_atten += '%0.10f ' % material.ass_jms.falloff_distance
    bm_lighting_atten += '%0.10f' % material.ass_jms.cutoff_distance

    bm_lighting_frus += '%0.10f ' % material.ass_jms.frustum_blend
    bm_lighting_frus += '%0.10f ' % material.ass_jms.frustum_falloff
    bm_lighting_frus += '%0.10f' % material.ass_jms.frustum_cutoff

    if material.ass_jms.is_bm:
        material_strings.append(bm_flags)
        material_strings.append(bm_lmres)
        if material.ass_jms.power > 0:
            material_strings.append(bm_lighting_basic)
            material_strings.append(bm_lighting_atten)
            material_strings.append(bm_lighting_frus)

    return material_strings

class ASSScene(global_functions.HaloAsset):
    class Transform:
        def __init__(self,
                     rotation=(0.0, 0.0, 0.0, 1.0),
                     vector=(0.0, 0.0, 0.0),
                     scale=(1.0, 1.0, 1.0)
                     ):

            self.rotation = rotation
            self.vector = vector
            self.scale = scale

    class Material:
        def __init__(self, name, lod=None, permutation=None, region=None, group="", lightmap=[]):
            self.name = name
            self.lod = lod
            self.permutation = permutation
            self.region = region
            self.group = group
            self.lightmap = lightmap

    class Object:
        def __init__(self,
                     geo_class,
                     xref_filepath,
                     xref_objectname,
                     material_index=-1,
                     radius=0.0,
                     extents=None,
                     height=0.0,
                     verts=None,
                     triangles=None,
                     node_index_list=None,
                     light_properties=None
                     ):

            self.geo_class = geo_class
            self.xref_filepath = xref_filepath
            self.xref_objectname = xref_objectname
            self.material_index = material_index
            self.radius = radius
            self.extents = extents
            self.height = height
            self.verts = verts
            self.triangles = triangles
            self.node_index_list = node_index_list
            self.light_properties = light_properties

    class Light:
        def __init__(self,
                     light_type,
                     light_color=None,
                     intensity=0.0,
                     hotspot_size=0.0,
                     hotspot_falloff_size=0.0,
                     uses_near_attenuation=0,
                     near_attenuation_start=0.0,
                     near_attenuation_end=0.0,
                     uses_far_attenuation=0,
                     far_attenuation_start=0,
                     far_attenuation_end=0.0,
                     light_shape=0,
                     light_aspect_ratio=0.0
                     ):

            self.light_type = light_type
            self.light_color = light_color
            self.intensity = intensity
            self.hotspot_size = hotspot_size
            self.hotspot_falloff_size = hotspot_falloff_size
            self.uses_near_attenuation = uses_near_attenuation
            self.near_attenuation_start = near_attenuation_start
            self.near_attenuation_end = near_attenuation_end
            self.uses_far_attenuation = uses_far_attenuation
            self.far_attenuation_start = far_attenuation_start
            self.far_attenuation_end = far_attenuation_end
            self.light_shape = light_shape
            self.light_aspect_ratio = light_aspect_ratio

    class Vertex:
        def __init__(self, node_influence_count=0, node_set=None, region=-1, translation=None, normal=None, color=None, uv_set=None):
            self.node_influence_count = node_influence_count
            self.node_set = node_set
            self.region = region
            self.translation = translation
            self.normal = normal
            self.color = color
            self.uv_set = uv_set

    class Triangle:
        def __init__(self, region=-1, material_index=-1, v0=-1, v1=-1, v2=-1):
            self.region = region
            self.material_index = material_index
            self.v0 = v0
            self.v1 = v1
            self.v2 = v2

    class Instance:
        def __init__(self, name, object_index=-1, unique_id=-1, parent_id=-1, inheritance_flag=0, local_transform=None, pivot_transform=None):
            self.name = name
            self.object_index = object_index
            self.unique_id = unique_id
            self.parent_id = parent_id
            self.inheritance_flag = inheritance_flag
            self.local_transform = local_transform
            self.pivot_transform = pivot_transform

    def __init__(self, context, version, game_version, apply_modifiers, triangulate_faces, edge_split, use_edge_angle, use_edge_sharp, split_angle, clean_normalize_weights, hidden_geo, custom_scale):
        global_functions.unhide_all_collections()

        default_region = mesh_processing.get_default_region_permutation_name(game_version)
        default_permutation = mesh_processing.get_default_region_permutation_name(game_version)

        limit_value = 0.001

        region_list = []
        permutation_list = []

        object_list = list(bpy.context.scene.objects)

        edge_split = global_functions.EdgeSplit(edge_split, use_edge_angle, split_angle, use_edge_sharp)

        self.materials = []
        self.objects = []
        self.instances = []
        material_list = []
        armature = None
        geometry_list = []
        linked_object_list = []
        linked_instance_list = []
        instance_list = [None]
        object_properties = []
        object_count = 0

        for obj in object_list:
            if obj.type== 'MESH':
                if clean_normalize_weights:
                    mesh_processing.vertex_group_clean_normalize(context, obj, limit_value)

                if apply_modifiers:
                    mesh_processing.add_modifier(context, obj, triangulate_faces, edge_split, None)

        depsgraph = context.evaluated_depsgraph_get()
        for obj in object_list:
            object_properties.append([obj.hide_get(), obj.hide_viewport])
            if hidden_geo:
                mesh_processing.unhide_object(obj)

        for obj in object_list:
            if obj.type == 'ARMATURE':
                if mesh_processing.set_ignore(obj) == False or hidden_geo:
                    for bone in obj.data.bones:
                        instance_list.append(bone)
                        if not bone.name in linked_object_list:
                            linked_object_list.append(bone.name)

                        geometry_list.append((bone, bone, 'BONE', obj))
                        object_count += 1

            elif obj.type == 'LIGHT' and version >= 3:
                if mesh_processing.set_ignore(obj) == False or hidden_geo:
                    instance_list.append(obj)
                    if not obj.name in linked_object_list:
                        linked_object_list.append(obj.name)
                        object_count += 1

                    if obj.data.type == 'SPOT':
                        geometry_list.append((obj, obj, 'SPOT_LGT'))

                    elif obj.data.type == 'AREA':
                        geometry_list.append((obj, obj, 'DIRECT_LGT'))

                    elif obj.data.type == 'POINT':
                        geometry_list.append((obj, obj,'OMNI_LGT'))

                    elif obj.data.type == 'SUN':
                        geometry_list.append((obj, obj, 'AMBIENT_LGT'))

                    else:
                        print("Bad light")

            elif obj.type== 'MESH' and len(obj.data.polygons) > 0:
                if mesh_processing.set_ignore(obj) == False or hidden_geo:
                    instance_list.append(obj)
                    if not obj.data.name in linked_object_list:
                        linked_object_list.append(obj.data.name)
                        object_count += 1

                    if obj.data.ass_jms.Object_Type == 'SPHERE':
                        evaluted_mesh = obj.to_mesh(preserve_all_data_layers=True)
                        geometry_list.append((evaluted_mesh, obj, 'SPHERE'))

                    elif obj.data.ass_jms.Object_Type == 'BOX':
                        evaluted_mesh = obj.to_mesh(preserve_all_data_layers=True)
                        geometry_list.append((evaluted_mesh, obj, 'BOX'))

                    elif obj.data.ass_jms.Object_Type == 'CAPSULES':
                        evaluted_mesh = obj.to_mesh(preserve_all_data_layers=True)
                        geometry_list.append((evaluted_mesh, obj, 'PILL'))

                    elif obj.data.ass_jms.Object_Type == 'CONVEX SHAPES':
                        if apply_modifiers:
                            obj_for_convert = obj.evaluated_get(depsgraph)
                            evaluted_mesh = obj_for_convert.to_mesh(preserve_all_data_layers=True, depsgraph=depsgraph)
                            geometry_list.append((evaluted_mesh, obj, 'MESH'))

                        else:
                            evaluted_mesh = obj.to_mesh(preserve_all_data_layers=True)
                            geometry_list.append((evaluted_mesh, obj, 'MESH'))

                    else:
                        print("Bad object")

            else:
                if mesh_processing.set_ignore(obj) == False or hidden_geo:
                    obj_data = None
                    obj_mesh_data = None

                    if obj:
                        obj_data = obj

                    if obj.data:
                        obj_mesh_data = obj.data

                    geometry_list.append((obj_mesh_data, obj_data, 'EMPTY'))
                    instance_list.append(obj_data)

        self.instances.append(ASSScene.Instance(name='Scene Root', local_transform=ASSScene.Transform(), pivot_transform=ASSScene.Transform()))
        for idx, geometry in enumerate(geometry_list):
            verts = []
            triangles = []
            node_index_list = []

            region_index = -1
            lod = None
            region = default_region
            permutation = default_permutation
            face_set = (None, None, default_permutation, default_region)

            evaluted_mesh = geometry[0]
            original_geo = geometry[1]
            geo_class = geometry[2]

            evaluted_mesh_name = None
            if evaluted_mesh:
                evaluted_mesh_name = evaluted_mesh.name

            else:
                evaluted_mesh_name = original_geo.name

            object_index = -1
            if not geo_class == 'EMPTY':
                object_index = linked_object_list.index(evaluted_mesh_name)

            material_index = -1
            radius = 2
            extents = [1.0, 1.0, 1.0]
            height = 1
            light_properties = None
            parent_id = 0
            inheritance_flag = 0
            xref_path = ""
            xref_name = ""

            is_bone = False
            parent = None
            if geo_class == 'BONE':
                is_bone = True
                armature = geometry[3]

            else:
                if original_geo.parent:
                    parent = original_geo.parent
                    if original_geo.parent.type == 'ARMATURE':
                        armature = parent
                        if original_geo.parent_type == 'BONE':
                            parent = original_geo.parent.data.bones[original_geo.parent_bone]

                        else:
                            parent = original_geo.parent.data.bones[0]

            if not parent == None:
                parent_id = instance_list.index(parent)

            geo_matrix = global_functions.get_matrix(original_geo, original_geo, True, armature, instance_list, is_bone, version, 'ASS', 0)
            geo_dimensions = global_functions.get_dimensions(geo_matrix, original_geo, None, None, version, None, False, is_bone, armature, 'ASS')
            rotation = (geo_dimensions.quat_i_a, geo_dimensions.quat_j_a, geo_dimensions.quat_k_a, geo_dimensions.quat_w_a)
            translation = (geo_dimensions.pos_x_a, geo_dimensions.pos_y_a, geo_dimensions.pos_z_a)
            if geo_class == 'BONE':
                scale = armature.pose.bones[original_geo.name].scale

            else:
                scale = original_geo.scale

            local_transform = ASSScene.Transform(rotation, translation, scale)
            self.instances.append(ASSScene.Instance(original_geo.name, object_index, idx, parent_id, inheritance_flag, local_transform, pivot_transform=ASSScene.Transform()))
            if not evaluted_mesh_name in linked_instance_list and not object_index == -1:
                linked_instance_list.append(evaluted_mesh_name)
                if geo_class == 'SPOT_LGT' or geo_class == 'DIRECT_LGT' or geo_class == 'OMNI_LGT' or geo_class == 'AMBIENT_LGT':
                    light_type = geo_class
                    color_rgb = (original_geo.data.color[0], original_geo.data.color[1], original_geo.data.color[2])
                    intensity = original_geo.data.energy
                    hotspot_size = -1.0
                    hotspot_falloff_size = -1.0
                    uses_near_attenuation = 0
                    near_attenuation_start = 0.0
                    near_attenuation_end = 0.0
                    uses_far_attenuation = 0
                    far_attenuation_start = 0.0
                    far_attenuation_end = 0.0
                    light_shape = 0
                    light_aspect_ratio = 0.0
                    if geo_class == 'SPOT_LGT':
                        hotspot_size = degrees(original_geo.data.spot_size)
                        hotspot_falloff_size = original_geo.data.spot_blend * degrees(original_geo.data.spot_size)

                    elif geo_class == 'DIRECT_LGT':
                        light_shape_type = 0
                        if original_geo.data.shape == "RECTANGLE" or original_geo.data.shape == "SQUARE":
                            light_shape_type = 1
                        light_shape = light_shape_type
                        light_aspect_ratio = original_geo.data.size

                    elif geo_class == 'SPOT_LGT' or geo_class == 'DIRECT_LGT':
                        uses_near_attenuation = int(original_geo.data.use_custom_distance)
                        near_attenuation_start = original_geo.data.cutoff_distance
                        near_attenuation_end = original_geo.data.cutoff_distance
                        uses_far_attenuation = int(original_geo.data.use_custom_distance)
                        far_attenuation_start = original_geo.data.cutoff_distance
                        far_attenuation_end = original_geo.data.cutoff_distance

                    light_properties = ASSScene.Light(light_type, color_rgb, intensity, hotspot_size, hotspot_falloff_size, uses_near_attenuation, near_attenuation_start, near_attenuation_end, uses_far_attenuation, far_attenuation_start, far_attenuation_end, light_shape, light_aspect_ratio)

                elif geo_class == 'SPHERE':
                    xref_path = bpy.path.abspath(original_geo.data.ass_jms.XREF_path)
                    if xref_path != "":
                        xref_name = original_geo.name

                    if original_geo.face_maps.active:
                        face_set = original_geo.face_maps[0].name.split()
                        slot_index, lod, permutation, region = global_functions.material_definition_parser(False, face_set, default_region, default_permutation)

                        if not permutation in permutation_list:
                            permutation_list.append(permutation)

                        if not region in region_list:
                            region_list.append(region)

                    radius = geo_dimensions.radius_a
                    face = original_geo.data.polygons[0]
                    material = global_functions.get_material(game_version, original_geo, face, evaluted_mesh, lod, region, permutation)
                    if not material == -1:
                        material_list = global_functions.gather_materials(game_version, material, material_list, 'ASS')
                        material_index = material_list.index(material)

                elif geo_class == 'BOX':
                    xref_path = bpy.path.abspath(original_geo.data.ass_jms.XREF_path)
                    if xref_path != "":
                        xref_name = original_geo.name

                    if original_geo.face_maps.active:
                        face_set = original_geo.face_maps[0].name.split()
                        slot_index, lod, permutation, region = global_functions.material_definition_parser(False, face_set, default_region, default_permutation)

                        if not permutation in permutation_list:
                            permutation_list.append(permutation)

                        if not region in region_list:
                            region_list.append(region)

                    face = original_geo.data.polygons[0]
                    extents = [geo_dimensions.dimension_x_a, geo_dimensions.dimension_y_a, geo_dimensions.dimension_z_a]
                    material = global_functions.get_material(game_version, original_geo, face, evaluted_mesh, lod, region, permutation)
                    if not material == -1:
                        material_list = global_functions.gather_materials(game_version, material, material_list, 'ASS')
                        material_index = material_list.index(material)

                elif geo_class == 'PILL':
                    xref_path = bpy.path.abspath(original_geo.data.ass_jms.XREF_path)
                    if xref_path != "":
                        xref_name = original_geo.name

                    if original_geo.face_maps.active:
                        face_set = original_geo.face_maps[0].name.split()
                        slot_index, lod, permutation, region = global_functions.material_definition_parser(False, face_set, default_region, default_permutation)

                        if not permutation in permutation_list:
                            permutation_list.append(permutation)

                        if not region in region_list:
                            region_list.append(region)

                    face = original_geo.data.polygons[0]
                    height = (geo_dimensions.pill_z_a)
                    radius = (geo_dimensions.radius_a)
                    material = global_functions.get_material(game_version, original_geo, face, evaluted_mesh, lod, region, permutation)
                    if not material == -1:
                        material_list = global_functions.gather_materials(game_version, material, material_list, 'ASS')
                        material_index = material_list.index(material)

                elif geo_class == 'MESH':
                    xref_path = bpy.path.abspath(original_geo.data.ass_jms.XREF_path)
                    if xref_path != "":
                        xref_name = original_geo.name

                    vertex_groups = original_geo.vertex_groups.keys()
                    original_geo_matrix = global_functions.get_matrix(original_geo, original_geo, False, armature, instance_list, False, version, "ASS", 0)
                    for idx, face in enumerate(evaluted_mesh.polygons):
                        if evaluted_mesh.face_maps.active and len(original_geo.face_maps) > 0:
                            face_map_idx = evaluted_mesh.face_maps.active.data[idx].value
                            if not face_map_idx == -1:  
                                face_set = mesh_processing.process_mesh_export_face_set(default_permutation, default_region, game_version, original_geo, face_map_idx)
                                if not region in region_list:
                                    region_list.append(region)

                                region_index = region_list.index(region)
                                if not game_version == 'haloce':
                                    if not permutation in permutation_list:
                                        permutation_list.append(permutation)

                        permutation = face_set[2]
                        region = face_set[3]

                        material = global_functions.get_material(game_version, original_geo, face, evaluted_mesh, lod, region, permutation)
                        material_index = -1
                        if not material == -1:
                            material_list = global_functions.gather_materials(game_version, material, material_list, "ASS")
                            material_index = material_list.index(material)

                        v0 = (idx * 3)
                        v1 = (idx * 3) + 1
                        v2 = (idx * 3) + 2

                        triangles.append(ASSScene.Triangle(region_index, material_index, v0, v1, v2))
                        for loop_index in face.loop_indices:
                            vert = evaluted_mesh.vertices[evaluted_mesh.loops[loop_index].vertex_index]

                            region = region_index
                            scaled_translation, normal = mesh_processing.process_mesh_export_vert(vert, "ASS", original_geo_matrix, version, armature)
                            uv_set = mesh_processing.process_mesh_export_uv(evaluted_mesh, "ASS", loop_index, version)
                            color = mesh_processing.process_mesh_export_color(evaluted_mesh, loop_index)
                            node_influence_count, node_set, node_index_list = mesh_processing.process_mesh_export_weights(vert, armature, original_geo, vertex_groups, instance_list, "ASS")

                            verts.append(ASSScene.Vertex(node_influence_count, node_set, region, scaled_translation, normal, color, uv_set))

                    original_geo.to_mesh_clear()
                    
                else:
                    print("Bad object")

                self.objects.append(ASSScene.Object(geo_class, xref_path, xref_name, material_index, radius, extents, height, verts, triangles, node_index_list, light_properties))

        for material in material_list:
            material_data = material[0]
            material_lightmap = get_material_strings(material_data, version)
            lod = mesh_processing.get_lod(material[1], game_version)

            if len(material[2]) != 0:
                region = material[2].replace(' ', '_').replace('\t', '_')

            if len(material[3]) != 0:
                permutation = material[3].replace(' ', '_').replace('\t', '_')

            self.materials.append(ASSScene.Material(material_data.name, lod, permutation, region, material_data.ass_jms.material_effect, material_lightmap))

        for idx, obj in enumerate(object_list):
            property_value = object_properties[idx]
            obj.hide_set(property_value[0])
            obj.hide_viewport = property_value[1]

def write_file(context,
               filepath,
               report,
               ass_version,
               ass_version_h2,
               ass_version_h3,
               hidden_geo,
               folder_structure,
               apply_modifiers,
               triangulate_faces,
               edge_split,
               use_edge_angle,
               use_edge_sharp,
               split_angle,
               clean_normalize_weights,
               scale_enum,
               scale_float,
               console,
               game_version,
               encoding
               ):

    custom_scale = global_functions.set_scale(scale_enum, scale_float)
    version = global_functions.get_version(ass_version, None, ass_version_h2, ass_version_h3, game_version, console)

    ass_scene = ASSScene(context, version, game_version, apply_modifiers, triangulate_faces, edge_split, use_edge_angle, use_edge_sharp, split_angle, clean_normalize_weights, hidden_geo, custom_scale)

    filename = os.path.basename(filepath)
    root_directory = global_functions.get_directory(game_version, "render", folder_structure, "0", False, filepath)

    file = open(root_directory + os.sep + filename, 'w', encoding=encoding)

    file.write(
        ';### HEADER ###' +
        '\n%s' % (version) +
        '\n"BLENDER"' +
        '\n"%s.%s"' % (bpy.app.version[0], bpy.app.version[1]) +
        '\n"%s"' % (getuser()) +
        '\n"%s"\n' % (socket.gethostname().upper())
    )

    file.write(
        '\n;### MATERIALS ###' +
        '\n%s\n' % (len(ass_scene.materials))
    )

    for idx, material in enumerate(ass_scene.materials):
        file.write(
            '\n;MATERIAL %s' % (idx) +
            '\n"%s"' % (material.name)
        )
        if version >= 8: #3
            file.write(
                '\n"%s %s"\n' % (material.permutation, material.region)
            )

        else:
            file.write(

                '\n"%s"\n' % (material.group)
            )

        if version >= 4:
            file.write(
                '%s\n' % (len(material.lightmap))
            )
            for string in material.lightmap:
                file.write(
                    '"%s"\n' % (string)
                )

    file.write(
        '\n;### OBJECTS ###' +
        '\n%s\n' % (len(ass_scene.objects))
    )

    for idx, geometry in enumerate(ass_scene.objects):
        if geometry.geo_class == 'SPOT_LGT' or geometry.geo_class == 'DIRECT_LGT' or geometry.geo_class == 'OMNI_LGT' or geometry.geo_class == 'AMBIENT_LGT':
            file.write(
                '\n;OBJECT %s' % (idx) +
                '\n"%s"' % ('GENERIC_LIGHT') +
                '\n"%s"' % (geometry.xref_filepath) +
                '\n"%s"' % (geometry.xref_objectname) +
                '\n"%s"' % (geometry.geo_class) +
                '\n%0.10f\t%0.10f\t%0.10f' % (geometry.light_properties.light_color[0], geometry.light_properties.light_color[1], geometry.light_properties.light_color[2]) +
                '\n%0.10f' % (geometry.light_properties.intensity) +
                '\n%0.10f' % (geometry.light_properties.hotspot_size) +
                '\n%0.10f' % (geometry.light_properties.hotspot_falloff_size) +
                '\n%s' % (geometry.light_properties.uses_near_attenuation) +
                '\n%0.10f' % (geometry.light_properties.near_attenuation_start) +
                '\n%0.10f' % (geometry.light_properties.near_attenuation_end) +
                '\n%s' % (geometry.light_properties.uses_far_attenuation) +
                '\n%0.10f' % (geometry.light_properties.far_attenuation_start) +
                '\n%0.10f' % (geometry.light_properties.far_attenuation_end) +
                '\n%s' % (geometry.light_properties.light_shape) +
                '\n%0.10f' % (geometry.light_properties.light_aspect_ratio) +
                '\n'
            )

        elif geometry.geo_class == 'BONE':
            file.write(
                '\n;OBJECT %s' % (idx) +
                '\n"%s"' % ('SPHERE') +
                '\n"%s"' % (geometry.xref_filepath) +
                '\n"%s"' % (geometry.xref_objectname) +
                '\n%s' % (geometry.material_index) +
                '\n%0.10f' % (geometry.radius) +
                '\n'
            )

        elif geometry.geo_class == 'SPHERE':
            file.write(
                '\n;OBJECT %s' % (idx) +
                '\n"%s"' % (geometry.geo_class) +
                '\n"%s"' % (geometry.xref_filepath) +
                '\n"%s"' % (geometry.xref_objectname) +
                '\n%s' % (geometry.material_index) +
                '\n%0.10f' % (geometry.radius) +
                '\n'
            )

        elif geometry.geo_class == 'BOX':
            file.write(
                '\n;OBJECT %s' % (idx) +
                '\n"%s"' % (geometry.geo_class) +
                '\n"%s"' % (geometry.xref_filepath) +
                '\n"%s"' % (geometry.xref_objectname) +
                '\n%s' % (geometry.material_index) +
                '\n%0.10f\t%0.10f\t%0.10f' % ((geometry.extents[0] / 2), (geometry.extents[1] / 2), (geometry.extents[2] / 2)) +
                '\n'
            )

        elif geometry.geo_class == 'PILL':
            file.write(
                '\n;OBJECT %s' % (idx) +
                '\n"%s"' % (geometry.geo_class) +
                '\n"%s"' % (geometry.xref_filepath) +
                '\n"%s"' % (geometry.xref_objectname) +
                '\n%s' % (geometry.material_index) +
                '\n%0.10f' % (geometry.height) +
                '\n%0.10f' % (geometry.radius) +
                '\n'
            )

        elif geometry.geo_class == 'MESH':
            file.write(
                '\n;OBJECT %s' % (idx) +
                '\n"%s"' % (geometry.geo_class) +
                '\n"%s"' % (geometry.xref_filepath) +
                '\n"%s"' % (geometry.xref_objectname) +
                '\n%s' % (len(geometry.verts))
            )

            for vert in geometry.verts:
                file.write(
                    '\n%0.10f\t%0.10f\t%0.10f' % (vert.translation[0], vert.translation[1], vert.translation[2]) +
                    '\n%0.10f\t%0.10f\t%0.10f' % (vert.normal[0], vert.normal[1], vert.normal[2])
                )

                if version >= 6:
                    file.write('\n%0.10f\t%0.10f\t%0.10f' % (vert.color[0], vert.color[1], vert.color[2]))
                file.write('\n%s' % (len(vert.node_set)))

                for node in vert.node_set:
                    node_index = node[0]
                    node_weight = node[1]
                    if version >= 3:
                        file.write(
                            '\n%s\t%0.10f' % (node_index, node_weight)
                        )

                    else:
                        file.write(
                            '\n%s' % (node_index) +
                            '\n%0.10f' % (node_weight)
                        )

                file.write('\n%s' % (len(vert.uv_set)))
                for uv in vert.uv_set:
                    tex_u = uv[0]
                    tex_v = uv[1]
                    tex_w = 0
                    if version >= 5:
                        file.write('\n%0.10f\t%0.10f\t%0.10f\n' % (tex_u, tex_v, tex_w))

                    else:
                        file.write('\n%0.10f\t%0.10f' % (tex_u, tex_v))

            file.write('\n%s' % (len(geometry.triangles)))
            for triangle in geometry.triangles:
                if version >= 3:
                    file.write(
                        '\n%s' % (triangle.material_index) +
                        '\t\t%s\t%s\t%s' % (triangle.v0, triangle.v1, triangle.v2)
                    )

                else:
                    file.write(
                        '\n%s' % (triangle.material_index) +
                        '\n%s\n%s\n%s' % (triangle.v0, triangle.v1, triangle.v2)
                    )

            file.write('\n')

        else:
            print("Bad object")

    file.write(
        '\n;### INSTANCES ###' +
        '\n%s\n' % (len(ass_scene.instances))
    )

    for idx, instance in enumerate(ass_scene.instances):
        node_index_list = []
        if not instance.object_index == -1:
            instance_object = ass_scene.objects[instance.object_index]
            if not instance_object.node_index_list == None:
                node_index_list = instance_object.node_index_list

        file.write(
            '\n;INSTANCE %s' % (idx) +
            '\n%s' % (instance.object_index) +
            '\n\"%s\"' % (instance.name) +
            '\n%s' % (instance.unique_id) +
            '\n%s' % (instance.parent_id) +
            '\n%s' % (instance.inheritance_flag) +
            '\n%0.10f\t%0.10f\t%0.10f\t%0.10f' % (instance.local_transform.rotation[0], instance.local_transform.rotation[1], instance.local_transform.rotation[2], instance.local_transform.rotation[3]) +
            '\n%0.10f\t%0.10f\t%0.10f' % (instance.local_transform.vector[0], instance.local_transform.vector[1], instance.local_transform.vector[2])
            )

        if version <= 1:
            file.write(
                '\n%0.10f\t%0.10f\t%0.10f\n' % (instance.local_transform.scale[0], instance.local_transform.scale[1], instance.local_transform.scale[2])
                )

        else:
            file.write(
                '\n%0.10f' % (instance.local_transform.scale[0])
                )

        file.write(
            '\n%0.10f\t%0.10f\t%0.10f\t%0.10f' % (instance.pivot_transform.rotation[0], instance.pivot_transform.rotation[1], instance.pivot_transform.rotation[2], instance.pivot_transform.rotation[3]) +
            '\n%0.10f\t%0.10f\t%0.10f' % (instance.pivot_transform.vector[0], instance.pivot_transform.vector[1], instance.pivot_transform.vector[2])
            )

        if version <= 1:
            file.write(
                '\n%0.10f\t%0.10f\t%0.10f\n' % (instance.pivot_transform.scale[0], instance.pivot_transform.scale[1], instance.pivot_transform.scale[2])
                )

        else:
            file.write(
                '\n%0.10f\n' % (instance.pivot_transform.scale[0])
                )

        for node_index in node_index_list:
            file.write('%s\n' % node_index)

    file.close()
    report({'INFO'}, "Export completed successfully")
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.export_scene.ass()
