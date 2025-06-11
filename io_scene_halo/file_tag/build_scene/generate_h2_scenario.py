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

from mathutils import Euler, Matrix
from math import radians, degrees, cos, sin, asin, atan2
from . import build_bsp as build_scene_level
from ...global_functions import global_functions
from ...global_functions.parse_tags import parse_tag
from ..h2.file_scenario.format import ObjectFlags, ClassificationEnum, LightFlags, LightmapTypeEnum, LightmappingPolicyEnum as SCNRLightmappingPolicyEnum
from . import build_lightmap as build_scene_lightmap
from ..h2.file_scenario.mesh_helper.build_mesh import get_object
from ...file_tag.h2.file_light.format import ShapeTypeEnum, DefaultLightmapSettingEnum
from ...file_tag.h2.file_scenery.format import LightmappingPolicyEnum

def get_rotation_euler(yaw=0, pitch=0, roll=0):
    yaw = -radians(yaw)
    pitch = radians(pitch)
    roll = -radians(roll)

    z = Matrix([[cos(yaw), -sin(yaw), 0],
                [sin(yaw), cos(yaw), 0],
                [0, 0, 1]])

    y = Matrix([[cos(pitch), 0, sin(pitch)],
                [0, 1, 0],
                [-sin(pitch), 0, cos(pitch)]])

    x = Matrix([[1, 0, 0],
                [0, cos(roll), -sin(roll)],
                [0, sin(roll), cos(roll)]])

    rot_matrix = z @ y @ x
    return rot_matrix.inverted().to_euler()

def get_decal_rotation_euler(yaw=0, pitch=0):
    max_value = 127
    forward = [0, 0, (yaw / max_value)]
    up = [0, (pitch / max_value), 0]

    right = np.cross(up, forward)
    rot_matrix = Matrix((forward, right, up))
    
    return Matrix(rot_matrix).inverted_safe(rot_matrix).to_euler()

def generate_skies(context, level_root, tag_block, report):
    asset_collection = bpy.data.collections.get("Skies")
    if asset_collection == None:
        asset_collection = bpy.data.collections.new("Skies")
        context.scene.collection.children.link(asset_collection)

    for element_idx, element in enumerate(tag_block):
        ASSET = parse_tag(element, report, "halo2", "retail")
        if not ASSET == None:
            for light_idx, light in enumerate(ASSET.lights):
                radiosity_color = (1.0, 1.0, 1.0)
                radiosity_power = 1.0
                if len(light.radiosity) > 0:
                    radiosity = light.radiosity[0]
                    radiosity_color = radiosity.color
                    radiosity_power = radiosity.power

                tag_name = os.path.basename(element.name)

                name = "%s_light_%s" % (tag_name, light_idx)
                light_data = bpy.data.lights.new(name, "SUN")
                ob = bpy.data.objects.new(name, light_data)

                ob.data.color = (radiosity_color[0], radiosity_color[1], radiosity_color[2])
                ob.data.energy = radiosity_power * 10
                ob.parent = level_root

                ob.rotation_euler = get_rotation_euler(*light.direction)

                asset_collection.objects.link(ob)

def generate_comments(context, level_root, comment_tag_block):
    comment_collection = bpy.data.collections.get("Comments")
    if comment_collection == None:
        comment_collection = bpy.data.collections.new("Comments")
        context.scene.collection.children.link(comment_collection)

    comment_layer_collection = context.view_layer.layer_collection.children[comment_collection.name]
    context.view_layer.active_layer_collection = comment_layer_collection
    context.view_layer.active_layer_collection.hide_viewport = True
    comment_collection.hide_render = True

    for comment_idx, comment_element in enumerate(comment_tag_block):
        font = bpy.data.curves.new(type="FONT", name="%s_%s" % (comment_element.name, comment_idx))
        font_ob = bpy.data.objects.new("%s_%s" % (comment_element.name, comment_idx), font)
        font_ob.data.body = comment_element.comment

        font_ob.parent = level_root
        font_ob.location = comment_element.position * 100
        comment_collection.objects.link(font_ob)

def get_data_type(collection_name, root, tag_path, element):
        if collection_name == "BSPs":
            root.tag_mesh.lightmap_index = -1

        #elif collection_name == "Scenery":
            #set_object_data(root, tag_path, element)

        elif collection_name == "Biped":
            root.lock_rotation[0] = True
            root.lock_rotation[1] = True

            #set_object_data(root, tag_path, element)
            #set_unit_data(root, element)

        #elif collection_name == "Vehicle":
            #set_object_data(root, tag_path, element)
            #set_unit_data(root, element)
            #set_vehicle_data(root, element)

        #elif collection_name == "Equipment":
            #set_object_data(root, tag_path, element)

        #elif collection_name == "Weapons":
            #set_object_data(root, tag_path, element)

        #elif collection_name == "Machines":
            #set_object_data(root, tag_path, element)

        #elif collection_name == "Controls":
            #set_object_data(root, tag_path, element)

        #elif collection_name == "Light Fixtures":
            #set_object_data(root, tag_path, element)

        #elif collection_name == "Sound Scenery":
            #set_object_data(root, tag_path, element)

        #elif collection_name == "Player Starting Locations":

        #elif collection_name == "Netgame Flags":

        #elif collection_name == "Netgame Equipment":

def generate_object_elements(level_root, collection_name, palette, tag_block, context, game_version, file_version, fix_rotations, report, random_color_gen):
    objects_list = []
    asset_collection = bpy.data.collections.get(collection_name)
    if asset_collection == None:
        asset_collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(asset_collection)

    asset_collection.hide_render = True
    if collection_name == "Scenery" or collection_name == "Lights" :
        asset_collection.hide_render = False

    object_tags = []
    for palette_idx, palette_element in enumerate(palette):
        ob = None
        object_name = "temp_%s_%s" % (os.path.basename(palette_element.name), palette_idx)
        ASSET = parse_tag(palette_element, report, "halo2", "retail")
        if not ASSET == None:
            if collection_name == "Scenery":
                MODEL = parse_tag(ASSET.model, report, "halo2", "retail")
                if not MODEL == None:
                    RENDER = parse_tag(MODEL.render_model, report, "halo2", "retail")
                    if not RENDER == None:
                        ob = get_object(asset_collection, RENDER, game_version, object_name, random_color_gen, report)
            elif collection_name == "Biped":
                MODEL = parse_tag(ASSET.model, report, "halo2", "retail")
                if not MODEL == None:
                    RENDER = parse_tag(MODEL.render_model, report, "halo2", "retail")
                    if not RENDER == None:
                        ob = get_object(asset_collection, RENDER, game_version, object_name, random_color_gen, report)
            elif collection_name == "Vehicle":
                MODEL = parse_tag(ASSET.model, report, "halo2", "retail")
                if not MODEL == None:
                    RENDER = parse_tag(MODEL.render_model, report, "halo2", "retail")
                    if not RENDER == None:
                        ob = get_object(asset_collection, RENDER, game_version, object_name, random_color_gen, report)
            elif collection_name == "Equipment":
                MODEL = parse_tag(ASSET.model, report, "halo2", "retail")
                if not MODEL == None:
                    RENDER = parse_tag(MODEL.render_model, report, "halo2", "retail")
                    if not RENDER == None:
                        ob = get_object(asset_collection, RENDER, game_version, object_name, random_color_gen, report)
            elif collection_name == "Weapons":
                MODEL = parse_tag(ASSET.model, report, "halo2", "retail")
                if not MODEL == None:
                    RENDER = parse_tag(MODEL.render_model, report, "halo2", "retail")
                    if not RENDER == None:
                        ob = get_object(asset_collection, RENDER, game_version, object_name, random_color_gen, report)
            elif collection_name == "Machines":
                MODEL = parse_tag(ASSET.model, report, "halo2", "retail")
                if not MODEL == None:
                    RENDER = parse_tag(MODEL.render_model, report, "halo2", "retail")
                    if not RENDER == None:
                        ob = get_object(asset_collection, RENDER, game_version, object_name, random_color_gen, report)
            elif collection_name == "Controls":
                MODEL = parse_tag(ASSET.model, report, "halo2", "retail")
                if not MODEL == None:
                    RENDER = parse_tag(MODEL.render_model, report, "halo2", "retail")
                    if not RENDER == None:
                        ob = get_object(asset_collection, RENDER, game_version, object_name, random_color_gen, report)
            elif collection_name == "Light Fixtures":
                MODEL = parse_tag(ASSET.model, report, "halo2", "retail")
                if not MODEL == None:
                    RENDER = parse_tag(MODEL.render_model, report, "halo2", "retail")
                    if not RENDER == None:
                        ob = get_object(asset_collection, RENDER, game_version, object_name, random_color_gen, report)
            elif collection_name == "Sound Scenery":
                MODEL = parse_tag(ASSET.model, report, "halo2", "retail")
                if not MODEL == None:
                    RENDER = parse_tag(MODEL.render_model, report, "halo2", "retail")
                    if not RENDER == None:
                        ob = get_object(asset_collection, RENDER, game_version, object_name, random_color_gen, report)
            elif collection_name == "Crates":
                MODEL = parse_tag(ASSET.model, report, "halo2", "retail")
                if not MODEL == None:
                    RENDER = parse_tag(MODEL.render_model, report, "halo2", "retail")
                    if not RENDER == None:
                        ob = get_object(asset_collection, RENDER, game_version, object_name, random_color_gen, report)

        object_tags.append(ASSET)
        objects_list.append(ob)

    for element_idx, element in enumerate(tag_block):
        pallete_item = palette[element.palette_index]
        tag_name = os.path.basename(pallete_item.name)

        name = "%s_%s" % (tag_name, element_idx)

        ob = objects_list[element.palette_index]
        if not ob == None:
            root = bpy.data.objects.new(name, ob.data)
            asset_collection.objects.link(root)

        else:
            root = bpy.data.objects.new(name, None)
            root.empty_display_type = 'ARROWS'
            asset_collection.objects.link(root)

        root.parent = level_root
        root.location = element.position * 100
        ob_scale = element.scale
        if ob_scale > 0.0:
            root.scale = (ob_scale, ob_scale, ob_scale)

        get_data_type(collection_name, root, pallete_item.name, element)

        root.rotation_euler = get_rotation_euler(*element.rotation)

        if collection_name == "Scenery":
            pallete_tag = object_tags[element.palette_index]
            hidden_in_render = False
            if ObjectFlags.not_automatically in ObjectFlags(element.placement_flags):
                hidden_in_render = True

            lightmap_policy = SCNRLightmappingPolicyEnum(element.lightmap_policy)
            if lightmap_policy == SCNRLightmappingPolicyEnum.tag_default:
                if not pallete_tag == None:
                    scenery_policy = LightmappingPolicyEnum(pallete_tag.lightmapping_policy)
                    if scenery_policy == LightmappingPolicyEnum.dynamic:
                        hidden_in_render = True
            else:
                if lightmap_policy == SCNRLightmappingPolicyEnum.dynamic:
                    hidden_in_render = True
        
            root.hide_set(hidden_in_render)
            root.hide_render = hidden_in_render

    for ob in objects_list:
        if not ob == None:
            bpy.data.objects.remove(ob, do_unlink=True)

def generate_light_volumes_elements(level_root, collection_name, palette, tag_block, context, game_version, file_version, fix_rotations, report, random_color_gen):
    asset_collection = bpy.data.collections.get(collection_name)
    if asset_collection == None:
        asset_collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(asset_collection)

    asset_collection.hide_render = False

    light_tags = []
    for palette_idx, palette_element in enumerate(palette):
        ASSET = parse_tag(palette_element, report, "halo2", "retail")
        light_tags.append(ASSET)

    for element in tag_block:
        pallete_item = palette[element.palette_index]
        light_tag = light_tags[element.palette_index]
        if light_tag and pallete_item: 
            scnr_light_flags = LightFlags(element.flags_1)
            emission_setting = LightmapTypeEnum(element.lightmap_type)

            light_name = "%s_%s" % (os.path.basename(pallete_item.name), element.palette_index)
            
            light_shape_type = ShapeTypeEnum(light_tag.shape_type)
            if LightFlags.custom_geometry in scnr_light_flags:
                light_shape_type = ShapeTypeEnum(element.shape_type)

            generate_light = False
            if LightmapTypeEnum.use_light_tag_settings == emission_setting:
                emission_setting = DefaultLightmapSettingEnum(light_tag.default_lightmap_setting)
                if not emission_setting == DefaultLightmapSettingEnum.dynamic_only:
                    generate_light = True
            else:
                if emission_setting == LightmapTypeEnum.lightmaps_only or emission_setting == LightmapTypeEnum.dynamic_with_lightmaps :
                    generate_light = True

            if generate_light:
                if light_shape_type == ShapeTypeEnum.sphere:
                    light_type = "POINT"
                elif light_shape_type == ShapeTypeEnum.orthogonal:
                    light_type = "AREA"
                else:
                    light_type = "SPOT"

                light_data_element = bpy.data.lights.new(light_name, light_type)
                if light_shape_type == ShapeTypeEnum.orthogonal:
                    light_data_element.shape = 'SQUARE'

                R, G, B, A = light_tag.diffuse_upper_bound
                light_data_element.color = (R, G, B)

                tag_light_size_min = light_tag.size_modifier[0]
                if tag_light_size_min == 0.0:
                    tag_light_size_min= 1.0
                tag_light_size_max = light_tag.size_modifier[1]
                if tag_light_size_max == 0.0:
                    tag_light_size_max= 1.0
                scnr_light_scale = element.lightmap_light_scale
                if scnr_light_scale == 0.0:
                    scnr_light_scale = 1.0

                light_size = max(tag_light_size_min, tag_light_size_max)
                light_size *= scnr_light_scale

                light_data_element.energy = (100 * light_size) * 1000

                root = bpy.data.objects.new(light_name, light_data_element)
                asset_collection.objects.link(root)

                root.parent = level_root
                root.location = element.position * 100
                ob_scale = element.scale
                if ob_scale > 0.0:
                    root.scale = (ob_scale, ob_scale, ob_scale)

                root.rotation_euler = get_rotation_euler(*element.rotation)

def generate_netgame_equipment_elements(level_root, tag_block, context, game_version, file_version, fix_rotations, report, random_color_gen):
    asset_collection = bpy.data.collections.get("Netgame Equipment")
    if asset_collection == None:
        asset_collection = bpy.data.collections.new("Netgame Equipment")
        context.scene.collection.children.link(asset_collection)

    asset_collection.hide_render = True
    for element_idx, element in enumerate(tag_block):
        ob = None
        if element.item_vehicle_collection.name == "":
            object_name = "%s_%s" % (ClassificationEnum(element.classification).name, element_idx)
        else:
            object_name = "%s_%s" % (os.path.basename(element.item_vehicle_collection.name), element_idx)

        COLLECTION = parse_tag(element.item_vehicle_collection, report, "halo2", "retail")
        if not COLLECTION == None:
            if len(COLLECTION.permutations) > 0:
                perutation_element = COLLECTION.permutations[0]
                if element.item_vehicle_collection.tag_group == "itmc":
                    perutation_element = COLLECTION.permutations[0]
                    ITEM = parse_tag(perutation_element.item, report, "halo2", "retail")
                    if not ITEM == None:
                        if perutation_element.item.tag_group == "eqip":
                            MODEL = parse_tag(ITEM.model, report, "halo2", "retail")
                            if not MODEL == None:
                                RENDER = parse_tag(MODEL.render_model, report, "halo2", "retail")
                                if not RENDER == None:
                                    ob = get_object(asset_collection, RENDER, game_version, object_name, random_color_gen, report)
                        elif perutation_element.item.tag_group == "weap":
                            MODEL = parse_tag(ITEM.model, report, "halo2", "retail")
                            if not MODEL == None:
                                RENDER = parse_tag(MODEL.render_model, report, "halo2", "retail")
                                if not RENDER == None:
                                    ob = get_object(asset_collection, RENDER, game_version, object_name, random_color_gen, report)

                elif element.item_vehicle_collection.tag_group == "vehc":
                    VEHICLE = parse_tag(perutation_element.item, report, "halo2", "retail")
                    if not VEHICLE == None:
                        MODEL = parse_tag(VEHICLE.model, report, "halo2", "retail")
                        if not MODEL == None:
                            RENDER = parse_tag(MODEL.render_model, report, "halo2", "retail")
                            if not RENDER == None:
                                ob = get_object(asset_collection, RENDER, game_version, object_name, random_color_gen, report)

        if ob == None:
            ob = bpy.data.objects.new(object_name, None)
            ob.empty_display_type = 'ARROWS'
            asset_collection.objects.link(ob)

        get_data_type("Netgame Equipment", ob, element.item_vehicle_collection.name, element)

        ob.parent = level_root
        ob.location = element.position * 100

        ob.rotation_euler = get_rotation_euler(*element.orientation)

def generate_empties(context, level_root, collection_name, tag_block):
    asset_collection = bpy.data.collections.get(collection_name)
    if asset_collection == None:
        asset_collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(asset_collection)

    asset_collection.hide_render = True
    for element_idx, element in enumerate(tag_block):
        ob = bpy.data.objects.new("%s_%s" % (collection_name, element_idx), None)

        ob.empty_display_type = 'ARROWS'
        ob.parent = level_root
        ob.location = element.position * 100
        ob.rotation_euler = (radians(0.0), radians(0.0), radians(element.facing))

        asset_collection.objects.link(ob)

def generate_camera_flags(context, level_root, collection_name, tag_block):
    asset_collection = bpy.data.collections.get(collection_name)
    if asset_collection == None:
        asset_collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(asset_collection)

    asset_collection.hide_render = True
    for element_idx, element in enumerate(tag_block):
        ob = bpy.data.objects.new(element.name, None)

        ob.empty_display_type = 'ARROWS'
        ob.parent = level_root
        ob.location = element.position * 100
        ob.rotation_euler = get_rotation_euler(*element.facing)

        asset_collection.objects.link(ob)

def generate_camera_points(context, level_root, tag_block):
    asset_collection = bpy.data.collections.get("Cutscene Cameras")
    if asset_collection == None:
        asset_collection = bpy.data.collections.new("Cutscene Cameras")
        context.scene.collection.children.link(asset_collection)

    asset_collection.hide_render = True
    for element_idx, element in enumerate(tag_block):
        camera_data = bpy.data.cameras.new(name='Camera')
        ob = bpy.data.objects.new(element.name, camera_data)

        ob.parent = level_root
        ob.location = element.position * 100

        ob.rotation_euler = get_rotation_euler(*element.orientation)
        ob.rotation_euler.rotate_axis("X", radians(90.0))
        ob.rotation_euler.rotate_axis("Y", radians(-90.0))

        asset_collection.objects.link(ob)

def generate_trigger_volumes(context, level_root, collection_name, tag_block):
    asset_collection = bpy.data.collections.get(collection_name)
    if asset_collection == None:
        asset_collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(asset_collection)

    volume_layer_collection = context.view_layer.layer_collection.children[asset_collection.name]
    context.view_layer.active_layer_collection = volume_layer_collection
    context.view_layer.active_layer_collection.hide_viewport = True
    asset_collection.hide_render = True

    for element_idx, element in enumerate(tag_block):
        mesh = bpy.data.meshes.new("part_%s" % element.name)
        ob = bpy.data.objects.new(element.name, mesh)

        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=2.0)
        bm.transform(Matrix.Translation((1, 1, 1)))
        bm.to_mesh(mesh)
        bm.free()

        ob.parent = level_root
        right = np.cross(element.up, element.forward)
        matrix_rotation = Matrix((element.forward, right, element.up))

        ob.matrix_world = matrix_rotation.to_4x4()
        ob.location = element.position * 100
        ob.dimensions = element.extents * 100

        asset_collection.objects.link(ob)

def generate_decals(level_root, collection_name, palette, tag_block, context, game_version, file_version, fix_rotations, report, random_color_gen):
    asset_collection = bpy.data.collections.get(collection_name)
    if asset_collection == None:
        asset_collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(asset_collection)

    volume_layer_collection = context.view_layer.layer_collection.children[asset_collection.name]
    context.view_layer.active_layer_collection = volume_layer_collection
    context.view_layer.active_layer_collection.hide_viewport = True
    asset_collection.hide_render = True

    for element_idx, element in enumerate(tag_block):  
        mesh = bpy.data.meshes.new("part_%s" % element_idx)
        ob = bpy.data.objects.new("decal_%s" % element_idx, mesh)
        asset_collection.objects.link(ob)

        bm = bmesh.new()
        vertex1 = bm.verts.new( (-1.0, -1.0, 0.0) )
        vertex2 = bm.verts.new( (1.0, -1.0, 0.0) )
        vertex3 = bm.verts.new( (-1.0, 1.0, 0.0) )
        vertex4 = bm.verts.new( (1.0, 1.0, 0.0) )

        bm.verts.index_update()
        bm.faces.new( (vertex2, vertex4, vertex3, vertex1) )
        bm.to_mesh(mesh)
        bm.free()

        ob.location = element.position * 100
        ob.rotation_euler = get_decal_rotation_euler(element.yaw, element.pitch)

def scenario_get_resources(H2_ASSET, report):
    ai_resource = None
    bipeds_resource = None
    cinematics_resource = None
    cluster_data_resource = None
    comments_resource = None
    creature_resource = None
    decals_resource = None
    decorators_resource = None
    devices_resource = None
    equipment_resource = None
    lights_resource = None
    scenery_resource = None
    sound_scenery_resource = None
    structure_lighting_resource = None
    trigger_volumes_resource = None
    vehicles_resource = None
    weapons_resource = None
    for scenario_reference in H2_ASSET.scenario_resources:
        for reference in scenario_reference.references:
            if reference.tag_group == "ai**":
                ai_resource = reference
            elif reference.tag_group == "*ipd":
                bipeds_resource = reference
            elif reference.tag_group == "cin*":
                cinematics_resource = reference
            elif reference.tag_group == "clu*":
                cluster_data_resource = reference
            elif reference.tag_group == "/**/":
                comments_resource = reference
            elif reference.tag_group == "*rea":
                creature_resource = reference
            elif reference.tag_group == "dec*":
                decals_resource = reference
            elif reference.tag_group == "dc*s":
                decorators_resource = reference
            elif reference.tag_group == "dgr*":
                devices_resource = reference
            elif reference.tag_group == "*qip":
                equipment_resource = reference
            elif reference.tag_group == "*igh":
                lights_resource = reference
            elif reference.tag_group == "*cen":
                scenery_resource = reference
            elif reference.tag_group == "*sce":
                sound_scenery_resource = reference
            elif reference.tag_group == "sslt":
                structure_lighting_resource = reference
            elif reference.tag_group == "trg*":
                trigger_volumes_resource = reference
            elif reference.tag_group == "*ehi":
                vehicles_resource = reference
            elif reference.tag_group == "*eap":
                weapons_resource = reference
        for reference in scenario_reference.ai_resources:
            if reference.tag_group == "ai**":
                ai_resource = reference
            elif reference.tag_group == "*ipd":
                bipeds_resource = reference
            elif reference.tag_group == "cin*":
                cinematics_resource = reference
            elif reference.tag_group == "clu*":
                cluster_data_resource = reference
            elif reference.tag_group == "/**/":
                comments_resource = reference
            elif reference.tag_group == "*rea":
                creature_resource = reference
            elif reference.tag_group == "dec*":
                decals_resource = reference
            elif reference.tag_group == "dc*s":
                decorators_resource = reference
            elif reference.tag_group == "dgr*":
                devices_resource = reference
            elif reference.tag_group == "*qip":
                equipment_resource = reference
            elif reference.tag_group == "*igh":
                lights_resource = reference
            elif reference.tag_group == "*cen":
                scenery_resource = reference
            elif reference.tag_group == "*sce":
                sound_scenery_resource = reference
            elif reference.tag_group == "sslt":
                structure_lighting_resource = reference
            elif reference.tag_group == "trg*":
                trigger_volumes_resource = reference
            elif reference.tag_group == "*ehi":
                vehicles_resource = reference
            elif reference.tag_group == "*eap":
                weapons_resource = reference

    if ai_resource:
        RESOURCE_ASSET = parse_tag(ai_resource, report, "halo2", "retail")
        if not RESOURCE_ASSET == None:
            H2_ASSET.style_palette = RESOURCE_ASSET.style_palette
            H2_ASSET.squad_groups = RESOURCE_ASSET.squad_groups
            H2_ASSET.squads = RESOURCE_ASSET.squads
            H2_ASSET.zones = RESOURCE_ASSET.zones
            H2_ASSET.character_palette = RESOURCE_ASSET.character_palette
            H2_ASSET.ai_animation_references = RESOURCE_ASSET.ai_animation_references
            H2_ASSET.ai_script_references = RESOURCE_ASSET.ai_script_references
            H2_ASSET.ai_recording_references = RESOURCE_ASSET.ai_recording_references
            H2_ASSET.ai_conversations = RESOURCE_ASSET.ai_conversations
            H2_ASSET.scripting_data = RESOURCE_ASSET.scripting_data
            H2_ASSET.orders = RESOURCE_ASSET.orders
            H2_ASSET.triggers = RESOURCE_ASSET.triggers
            H2_ASSET.structure_bsps = RESOURCE_ASSET.structure_bsps
            H2_ASSET.weapon_palette = RESOURCE_ASSET.weapon_palette
            H2_ASSET.vehicle_palette = RESOURCE_ASSET.vehicle_palette
            H2_ASSET.vehicles = RESOURCE_ASSET.vehicles
            H2_ASSET.mission_scenes = RESOURCE_ASSET.mission_scenes
            H2_ASSET.flocks = RESOURCE_ASSET.flocks
            H2_ASSET.trigger_volumes = RESOURCE_ASSET.trigger_volumes

    if bipeds_resource:
        RESOURCE_ASSET = parse_tag(bipeds_resource, report, "halo2", "retail")
        if not RESOURCE_ASSET == None:
            H2_ASSET.object_names = RESOURCE_ASSET.object_names
            H2_ASSET.structure_bsps = RESOURCE_ASSET.structure_bsps
            H2_ASSET.biped_palette = RESOURCE_ASSET.biped_palette
            H2_ASSET.bipeds = RESOURCE_ASSET.bipeds
            H2_ASSET.editor_folders = RESOURCE_ASSET.editor_folders

    if cinematics_resource:
        RESOURCE_ASSET = parse_tag(cinematics_resource, report, "halo2", "retail")
        if not RESOURCE_ASSET == None:
            H2_ASSET.cutscene_flags = RESOURCE_ASSET.cutscene_flags
            H2_ASSET.cutscene_camera_points = RESOURCE_ASSET.cutscene_camera_points
            H2_ASSET.recorded_animations = RESOURCE_ASSET.recorded_animations

    if cluster_data_resource:
        RESOURCE_ASSET = parse_tag(cluster_data_resource, report, "halo2", "retail")
        if not RESOURCE_ASSET == None:
            H2_ASSET.scenario_cluster_data = RESOURCE_ASSET.scenario_cluster_data
            H2_ASSET.background_sound_palette = RESOURCE_ASSET.background_sound_palette
            H2_ASSET.sound_environment_palette = RESOURCE_ASSET.sound_environment_palette
            H2_ASSET.weather_palette = RESOURCE_ASSET.weather_palette
            H2_ASSET.atmospheric_fog_palette = RESOURCE_ASSET.atmospheric_fog_palette

    if comments_resource:
        RESOURCE_ASSET = parse_tag(comments_resource, report, "halo2", "retail")
        if not RESOURCE_ASSET == None:
            H2_ASSET.comments = RESOURCE_ASSET.comments

    if creature_resource:
        RESOURCE_ASSET = parse_tag(creature_resource, report, "halo2", "retail")
        if not RESOURCE_ASSET == None:
            H2_ASSET.object_names = RESOURCE_ASSET.object_names
            H2_ASSET.structure_bsps = RESOURCE_ASSET.structure_bsps
            H2_ASSET.creatures_palette = RESOURCE_ASSET.creatures_palette
            H2_ASSET.creatures = RESOURCE_ASSET.creatures
            H2_ASSET.editor_folders = RESOURCE_ASSET.editor_folders

    if decals_resource:
        RESOURCE_ASSET = parse_tag(decals_resource, report, "halo2", "retail")
        if not RESOURCE_ASSET == None:
            H2_ASSET.decal_palette = RESOURCE_ASSET.decal_palette
            H2_ASSET.decals = RESOURCE_ASSET.decals

    if decorators_resource:
        RESOURCE_ASSET = parse_tag(decorators_resource, report, "halo2", "retail")
        if not RESOURCE_ASSET == None:
            H2_ASSET.decorators = RESOURCE_ASSET.decorators
            H2_ASSET.decorator_palette = RESOURCE_ASSET.decorator_palette

    if devices_resource:
        RESOURCE_ASSET = parse_tag(devices_resource, report, "halo2", "retail")
        if not RESOURCE_ASSET == None:
            H2_ASSET.object_names = RESOURCE_ASSET.object_names
            H2_ASSET.structure_bsps = RESOURCE_ASSET.structure_bsps
            H2_ASSET.device_groups = RESOURCE_ASSET.device_groups
            H2_ASSET.device_machines = RESOURCE_ASSET.device_machines
            H2_ASSET.device_machine_palette = RESOURCE_ASSET.device_machine_palette
            H2_ASSET.device_controls = RESOURCE_ASSET.device_controls
            H2_ASSET.device_control_palette = RESOURCE_ASSET.device_control_palette
            H2_ASSET.device_light_fixtures = RESOURCE_ASSET.device_light_fixtures
            H2_ASSET.device_light_fixtures_palette = RESOURCE_ASSET.device_light_fixtures_palette
            H2_ASSET.editor_folders = RESOURCE_ASSET.editor_folders

    if equipment_resource:
        RESOURCE_ASSET = parse_tag(equipment_resource, report, "halo2", "retail")
        if not RESOURCE_ASSET == None:
            H2_ASSET.object_names = RESOURCE_ASSET.object_names
            H2_ASSET.structure_bsps = RESOURCE_ASSET.structure_bsps
            H2_ASSET.equipment_palette = RESOURCE_ASSET.equipment_palette
            H2_ASSET.equipment = RESOURCE_ASSET.equipment
            H2_ASSET.editor_folders = RESOURCE_ASSET.editor_folders

    if lights_resource:
        RESOURCE_ASSET = parse_tag(lights_resource, report, "halo2", "retail")
        if not RESOURCE_ASSET == None:
            H2_ASSET.object_names = RESOURCE_ASSET.object_names
            H2_ASSET.structure_bsps = RESOURCE_ASSET.structure_bsps
            H2_ASSET.light_volume_palette = RESOURCE_ASSET.light_volume_palette
            H2_ASSET.light_volumes = RESOURCE_ASSET.light_volumes
            H2_ASSET.editor_folders = RESOURCE_ASSET.editor_folders

    if scenery_resource:
        RESOURCE_ASSET = parse_tag(lights_resource, report, "halo2", "retail")
        if not RESOURCE_ASSET == None:
            H2_ASSET.object_names = RESOURCE_ASSET.object_names
            H2_ASSET.structure_bsps = RESOURCE_ASSET.structure_bsps
            H2_ASSET.scenery_palette = RESOURCE_ASSET.scenery_palette
            H2_ASSET.scenery = RESOURCE_ASSET.scenery
            H2_ASSET.crates_palette = RESOURCE_ASSET.crates_palette
            H2_ASSET.crates = RESOURCE_ASSET.crates
            H2_ASSET.editor_folders = RESOURCE_ASSET.editor_folders

    if sound_scenery_resource:
        RESOURCE_ASSET = parse_tag(sound_scenery_resource, report, "halo2", "retail")
        if not RESOURCE_ASSET == None:
            H2_ASSET.object_names = RESOURCE_ASSET.object_names
            H2_ASSET.structure_bsps = RESOURCE_ASSET.structure_bsps
            H2_ASSET.sound_scenery_palette = RESOURCE_ASSET.sound_scenery_palette
            H2_ASSET.sound_scenery = RESOURCE_ASSET.sound_scenery
            H2_ASSET.editor_folders = RESOURCE_ASSET.editor_folders

    if structure_lighting_resource:
        RESOURCE_ASSET = parse_tag(structure_lighting_resource, report, "halo2", "retail")
        if not RESOURCE_ASSET == None:
            H2_ASSET.structure_bsp_lighting = RESOURCE_ASSET.structure_bsp_lighting

    if trigger_volumes_resource:
        RESOURCE_ASSET = parse_tag(trigger_volumes_resource, report, "halo2", "retail")
        if not RESOURCE_ASSET == None:
            H2_ASSET.trigger_volumes = RESOURCE_ASSET.trigger_volumes
            H2_ASSET.object_names = RESOURCE_ASSET.object_names

    if vehicles_resource:
        RESOURCE_ASSET = parse_tag(vehicles_resource, report, "halo2", "retail")
        if not RESOURCE_ASSET == None:
            H2_ASSET.object_names = RESOURCE_ASSET.object_names
            H2_ASSET.structure_bsps = RESOURCE_ASSET.structure_bsps
            H2_ASSET.vehicle_palette = RESOURCE_ASSET.vehicle_palette
            H2_ASSET.vehicles = RESOURCE_ASSET.vehicles
            H2_ASSET.editor_folders = RESOURCE_ASSET.editor_folders

    if weapons_resource:
        RESOURCE_ASSET = parse_tag(weapons_resource, report, "halo2", "retail")
        if not RESOURCE_ASSET == None:
            H2_ASSET.object_names = RESOURCE_ASSET.object_names
            H2_ASSET.structure_bsps = RESOURCE_ASSET.structure_bsps
            H2_ASSET.weapon_palette = RESOURCE_ASSET.weapon_palette
            H2_ASSET.weapons = RESOURCE_ASSET.weapons
            H2_ASSET.editor_folders = RESOURCE_ASSET.editor_folders

def generate_scenario_scene(context, H2_ASSET, game_version, game_title, file_version, fix_rotations, empty_markers, report):
    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors
    levels_collection = bpy.data.collections.get("BSPs")
    if levels_collection == None:
        levels_collection = bpy.data.collections.new("BSPs")
        context.scene.collection.children.link(levels_collection)

    for bsp_idx, bsp_element in enumerate(H2_ASSET.structure_bsps):
        bsp = bsp_element.structure_bsp
        lightmap = bsp_element.structure_lightmap
        SBSP_ASSET = parse_tag(bsp, report, "halo2", "retail")
        LTMP_ASSET = parse_tag(lightmap, report, "halo2", "retail")

        bsp_name = os.path.basename(bsp.name)
        collection_name = "%s_%s" % (bsp_name, bsp_idx)
        level_collection = bpy.data.collections.get(collection_name)
        if level_collection == None:
            level_collection = bpy.data.collections.new(collection_name)
            levels_collection.children.link(level_collection)
            
        if not SBSP_ASSET == None:
            cluster_name = "%s_clusters" % bsp_name
            clusters_collection = bpy.data.collections.get(cluster_name)
            if clusters_collection == None:
                clusters_collection = bpy.data.collections.new(cluster_name)
                level_collection.children.link(clusters_collection)

            clusters_collection.hide_viewport = True
            clusters_collection.hide_render = True

            build_scene_level.build_scene(context, SBSP_ASSET, game_version, game_title, file_version, fix_rotations, empty_markers, report, level_collection, clusters_collection)

        if not LTMP_ASSET == None:
            lightmap_name = "%s_lightmaps" % bsp_name
            lightmap_collection = bpy.data.collections.get(lightmap_name)
            if lightmap_collection == None:
                lightmap_collection = bpy.data.collections.new(lightmap_name)
                level_collection.children.link(lightmap_collection)

            build_scene_lightmap.build_scene(context, LTMP_ASSET, game_version, game_title, file_version, fix_rotations, empty_markers, report, level_collection, lightmap_collection, SBSP_ASSET)

    level_root = bpy.data.objects.get("frame_root")
    if level_root == None:
        level_mesh = bpy.data.meshes.new("frame_root")
        level_root = bpy.data.objects.new("frame_root", level_mesh)
        context.collection.objects.link(level_root)

    scenario_get_resources(H2_ASSET, report)
    if len(H2_ASSET.skies) > 0:
        generate_skies(context, level_root, H2_ASSET.skies, report)
    if len(H2_ASSET.comments) > 0:
        generate_comments(context, level_root, H2_ASSET.comments)
    if len(H2_ASSET.scenery) > 0:
        generate_object_elements(level_root, "Scenery", H2_ASSET.scenery_palette, H2_ASSET.scenery, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H2_ASSET.bipeds) > 0:
        generate_object_elements(level_root, "Biped", H2_ASSET.biped_palette, H2_ASSET.bipeds, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H2_ASSET.vehicles) > 0:
        generate_object_elements(level_root, "Vehicle", H2_ASSET.vehicle_palette, H2_ASSET.vehicles, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H2_ASSET.equipment) > 0:
        generate_object_elements(level_root, "Equipment", H2_ASSET.equipment_palette, H2_ASSET.equipment, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H2_ASSET.weapons) > 0:
        generate_object_elements(level_root, "Weapons", H2_ASSET.weapon_palette, H2_ASSET.weapons, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H2_ASSET.device_machines) > 0:
        generate_object_elements(level_root, "Machines", H2_ASSET.device_machine_palette, H2_ASSET.device_machines, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H2_ASSET.device_controls) > 0:
        generate_object_elements(level_root, "Controls", H2_ASSET.device_control_palette, H2_ASSET.device_controls, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H2_ASSET.device_light_fixtures) > 0:
        generate_object_elements(level_root, "Light Fixtures", H2_ASSET.device_light_fixtures_palette, H2_ASSET.device_light_fixtures, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H2_ASSET.sound_scenery) > 0:
        generate_object_elements(level_root, "Sound Scenery", H2_ASSET.sound_scenery_palette, H2_ASSET.sound_scenery, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H2_ASSET.crates) > 0:
        generate_object_elements(level_root, "Crates", H2_ASSET.crates_palette, H2_ASSET.crates, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H2_ASSET.creatures) > 0:
        generate_object_elements(level_root, "Creatures", H2_ASSET.creatures_palette, H2_ASSET.creatures, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H2_ASSET.light_volumes) > 0:
        generate_light_volumes_elements(level_root, "Lights", H2_ASSET.light_volume_palette, H2_ASSET.light_volumes, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H2_ASSET.player_starting_locations) > 0:
        generate_empties(context, level_root, "Player Starting Locations", H2_ASSET.player_starting_locations)
    if len(H2_ASSET.netgame_flags) > 0:
        generate_empties(context, level_root, "Netgame Flags", H2_ASSET.netgame_flags)
    if len(H2_ASSET.netgame_equipment) > 0:
        generate_netgame_equipment_elements(level_root, H2_ASSET.netgame_equipment, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H2_ASSET.trigger_volumes) > 0:
        generate_trigger_volumes(context, level_root, "Trigger Volumes", H2_ASSET.trigger_volumes)
    if len(H2_ASSET.cutscene_flags) > 0:
        generate_camera_flags(context, level_root, "Cutscene Flags", H2_ASSET.cutscene_flags)
    if len(H2_ASSET.cutscene_camera_points) > 0:
        generate_camera_points(context, level_root, H2_ASSET.cutscene_camera_points)
    if len(H2_ASSET.decals) > 0:
        generate_decals(level_root, "Decals", H2_ASSET.decal_palette, H2_ASSET.decals, context, game_version, file_version, fix_rotations, report, random_color_gen)
