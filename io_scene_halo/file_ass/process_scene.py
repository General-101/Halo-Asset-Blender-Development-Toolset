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

from math import degrees
from .format import ASSAsset
from ..global_functions import mesh_processing, global_functions

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
    if version >= 4:
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
    if version >= 4:
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

def scale_is_uniform(obj):
    is_uniform = True
    scale_x = obj.scale[0]
    scale_y = obj.scale[1]
    scale_z = obj.scale[2]
    if scale_y > (scale_x + 0.0000900000) or scale_y < (scale_x - 0.0000900000):
        is_uniform = False

    if scale_z > (scale_x + 0.0000900000) or scale_z < (scale_x - 0.0000900000):
        is_uniform = False

    return is_uniform

def process_scene(context, version, game_version, hidden_geo, apply_modifiers, triangulate_faces, edge_split, clean_normalize_weights, custom_scale, report):
    ASS = ASSAsset()

    global_functions.unhide_all_collections(context)

    default_region = mesh_processing.get_default_region_permutation_name(game_version)
    default_permutation = mesh_processing.get_default_region_permutation_name(game_version)

    limit_value = 0.001

    region_list = []
    permutation_list = []

    object_list = list(context.scene.objects)

    ASS.materials = []
    ASS.objects = []
    ASS.instances = []
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
        if not scale_is_uniform(obj):
            report({'WARNING'}, "Object %s has non uniform scale. Object will not look correct ingame. Apply transforms and export again." % (obj.name))

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

    ASS.instances.append(ASS.Instance(name='Scene Root', local_transform=ASS.Transform(), pivot_transform=ASS.Transform()))
    for idx, geometry in enumerate(geometry_list):
        verts = []
        triangles = []
        node_index_list = []

        region_index = -1
        lod = None
        region = default_region
        permutation = default_permutation
        face_set = (None, default_permutation, default_region)

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

        geo_matrix = global_functions.get_matrix(original_geo, original_geo, True, armature, instance_list, is_bone, version, 'ASS', False, custom_scale, False)
        geo_dimensions = global_functions.get_dimensions(geo_matrix, original_geo, version, is_bone, 'ASS', custom_scale)
        rotation = (geo_dimensions.quaternion[0], geo_dimensions.quaternion[1], geo_dimensions.quaternion[2], geo_dimensions.quaternion[3])
        translation = (geo_dimensions.position[0], geo_dimensions.position[1], geo_dimensions.position[2])
        scale = geo_dimensions.scale

        local_transform = ASS.Transform(rotation, translation, scale)
        ASS.instances.append(ASS.Instance(original_geo.name, object_index, idx, parent_id, inheritance_flag, local_transform, pivot_transform=ASS.Transform()))
        if not evaluted_mesh_name in linked_instance_list and not object_index == -1:
            linked_instance_list.append(evaluted_mesh_name)
            object_matrix = global_functions.get_matrix(original_geo, original_geo, False, armature, instance_list, is_bone, version, 'ASS', False, custom_scale, False)
            object_dimensions = global_functions.get_dimensions(object_matrix, original_geo, version, is_bone, 'ASS', custom_scale)
            if geo_class == 'SPOT_LGT' or geo_class == 'DIRECT_LGT' or geo_class == 'OMNI_LGT' or geo_class == 'AMBIENT_LGT':
                light_properties = ASS.Light()
                light_properties.light_type = geo_class
                light_properties.light_color = (original_geo.data.color[0], original_geo.data.color[1], original_geo.data.color[2])
                light_properties.intensity = original_geo.data.energy

                if geo_class == 'SPOT_LGT' or geo_class == 'DIRECT_LGT':
                    light_properties.hotspot_size = degrees(original_geo.data.halo_light.spot_size)
                    light_properties.hotspot_falloff_size = original_geo.data.halo_light.spot_blend * degrees(original_geo.data.halo_light.spot_size)

                    light_properties.light_shape = int(original_geo.data.halo_light.light_cone_shape)
                    light_properties.light_aspect_ratio = original_geo.data.halo_light.aspect_ratio

                    light_properties.uses_near_attenuation = int(original_geo.data.halo_light.use_near_atten)
                    light_properties.near_attenuation_start = original_geo.data.halo_light.near_atten_start
                    light_properties.near_attenuation_end = original_geo.data.halo_light.near_atten_end
                    light_properties.uses_far_attenuation = int(original_geo.data.halo_light.use_far_atten)
                    light_properties.far_attenuation_start = original_geo.data.halo_light.far_atten_start
                    light_properties.far_attenuation_end = original_geo.data.halo_light.far_atten_end

            elif geo_class == 'SPHERE':
                xref_path = bpy.path.abspath(original_geo.data.ass_jms.XREF_path)
                if xref_path != "":
                    xref_name = original_geo.name

                if original_geo.face_maps.active:
                    face_set = original_geo.face_maps[0].name.split()
                    lod, permutation, region = global_functions.material_definition_parser(False, face_set, default_region, default_permutation)

                    if not permutation in permutation_list:
                        permutation_list.append(permutation)

                    if not region in region_list:
                        region_list.append(region)

                radius = object_dimensions.object_radius
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
                    lod, permutation, region = global_functions.material_definition_parser(False, face_set, default_region, default_permutation)

                    if not permutation in permutation_list:
                        permutation_list.append(permutation)

                    if not region in region_list:
                        region_list.append(region)

                face = original_geo.data.polygons[0]
                extents = [object_dimensions.dimension[0], object_dimensions.dimension[1], object_dimensions.dimension[2]]
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
                    lod, permutation, region = global_functions.material_definition_parser(False, face_set, default_region, default_permutation)

                    if not permutation in permutation_list:
                        permutation_list.append(permutation)

                    if not region in region_list:
                        region_list.append(region)

                face = original_geo.data.polygons[0]
                height = object_dimensions.pill_height
                radius = object_dimensions.object_radius
                material = global_functions.get_material(game_version, original_geo, face, evaluted_mesh, lod, region, permutation)
                if not material == -1:
                    material_list = global_functions.gather_materials(game_version, material, material_list, 'ASS')
                    material_index = material_list.index(material)

            elif geo_class == 'MESH':
                xref_path = bpy.path.abspath(original_geo.data.ass_jms.XREF_path)
                if xref_path != "":
                    xref_name = original_geo.name

                vertex_groups = original_geo.vertex_groups.keys()
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

                    permutation = face_set[1]
                    region = face_set[2]

                    material = global_functions.get_material(game_version, original_geo, face, evaluted_mesh, lod, region, permutation)
                    material_index = -1
                    if not material == -1:
                        material_list = global_functions.gather_materials(game_version, material, material_list, "ASS")
                        material_index = material_list.index(material)

                    v0 = (idx * 3)
                    v1 = (idx * 3) + 1
                    v2 = (idx * 3) + 2

                    triangles.append(ASS.Triangle(region_index, material_index, v0, v1, v2))
                    for loop_index in face.loop_indices:
                        vert = evaluted_mesh.vertices[evaluted_mesh.loops[loop_index].vertex_index]

                        region = region_index
                        scaled_translation, normal = mesh_processing.process_mesh_export_vert(vert, "ASS", object_matrix, custom_scale)
                        uv_set = mesh_processing.process_mesh_export_uv(evaluted_mesh, "ASS", loop_index, version)
                        color = mesh_processing.process_mesh_export_color(evaluted_mesh, loop_index)
                        node_influence_count, node_set, node_index_list = mesh_processing.process_mesh_export_weights(vert, armature, original_geo, vertex_groups, instance_list, "ASS")

                        verts.append(ASS.Vertex(node_influence_count, node_set, region, scaled_translation, normal, color, uv_set))

                original_geo.to_mesh_clear()

            else:
                print("Bad object")

            ASS.objects.append(ASS.Object(geo_class, xref_path, xref_name, material_index, radius, extents, height, verts, triangles, node_index_list, light_properties))

    for material in material_list:
        material_data = material[0]

        texture_path = ""

        slot_index = bpy.data.materials.find(material_data.name)
        lod = mesh_processing.get_lod(material[1], game_version)
        region = material[2]
        permutation = material[3]

        material_name = mesh_processing.append_material_symbols(material_data, game_version, True)
        material_lightmap = get_material_strings(material_data, version)

        if region:
            region = region.replace(' ', '_').replace('\t', '_')

        if permutation:
            permutation = permutation.replace(' ', '_').replace('\t', '_')

        ASS.materials.append(ASS.Material(material_name, material_name, texture_path, slot_index, lod, permutation, region, material_data.ass_jms.material_effect, material_lightmap))

    for idx, obj in enumerate(object_list):
        property_value = object_properties[idx]
        obj.hide_set(property_value[0])
        obj.hide_viewport = property_value[1]

    return ASS
