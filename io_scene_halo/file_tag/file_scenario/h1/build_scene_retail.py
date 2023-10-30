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

from enum import Flag, auto
from math import degrees, radians
from mathutils import Vector, Quaternion, Euler
from ..h1.mesh_helper.build_mesh_retail import get_object
from io_scene_halo.file_tag.file_structure_bsp import build_scene as build_scene_level

def generate_skies(context, level_root, tag_block, tag_format, report):
    asset_collection = bpy.data.collections.get("Skies")
    if asset_collection == None:
        asset_collection = bpy.data.collections.new("Skies")
        context.scene.collection.children.link(asset_collection)

    for element_idx, element in enumerate(tag_block):
        ASSET = element.parse_tag(tag_format, report, "halo1", "retail")
        if not ASSET == None:
            for light_idx, light in enumerate(ASSET.lights):
                tag_name = os.path.basename(element.name)

                name = "%s_light_%s" % (tag_name, light_idx)
                light_data = bpy.data.lights.new(name, "SUN")
                ob = bpy.data.objects.new(name, light_data)

                ob.data.color = (light.color[0], light.color[1], light.color[2])
                ob.data.energy = light.power
                ob.parent = level_root

                rotation = Euler((radians(0.0), radians(90.0), radians(0.0)), 'XYZ')
                pitch = Euler((radians(0.0), -radians(light.direction[1]), radians(0.0)), 'XYZ')
                yaw = Euler((radians(0.0), radians(0.0), radians(light.direction[0])), 'XYZ')
                rotation.rotate(pitch)
                rotation.rotate(yaw)

                ob.rotation_euler = rotation

                asset_collection.objects.link(ob)

def generate_comments(context, level_root, comment_tag_block):
    comment_collection = bpy.data.collections.get("Comments")
    if comment_collection == None:
        comment_collection = bpy.data.collections.new("Comments")
        context.scene.collection.children.link(comment_collection)

    for comment_idx, comment_element in enumerate(comment_tag_block):
        font = bpy.data.curves.new(type="FONT", name="comment")
        font_ob = bpy.data.objects.new("comment_%s" % comment_idx, font)
        font_ob.data.body = comment_element.text

        font_ob.parent = level_root
        font_ob.location = comment_element.position * 100
        comment_collection.objects.link(font_ob)

def generate_object_elements(level_root, collection_name, palette, tag_block, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen):
    objects_list = []
    asset_collection = bpy.data.collections.get(collection_name)
    if asset_collection == None:
        asset_collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(asset_collection)

    for palette_idx, palette_element in enumerate(palette):
        ob = None
        object_name = "temp_%s_%s" % (os.path.basename(palette_element.name), palette_idx)
        ASSET = palette_element.parse_tag(tag_format, report, "halo1", "retail")
        if not ASSET == None:
            if collection_name == "Scenery":
                MODEL = ASSET.scenery_body.model.parse_tag(tag_format, report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, mesh_processing, random_color_gen, tag_format, report)
            elif collection_name == "Biped":
                MODEL = ASSET.biped_body.model.parse_tag(tag_format, report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, mesh_processing, random_color_gen, tag_format, report)
            elif collection_name == "Vehicle":
                MODEL = ASSET.vehicle_body.model.parse_tag(tag_format, report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, mesh_processing, random_color_gen, tag_format, report)
            elif collection_name == "Equipment":
                MODEL = ASSET.equipment_body.model.parse_tag(tag_format, report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, mesh_processing, random_color_gen, tag_format, report)
            elif collection_name == "Weapons":
                MODEL = ASSET.weapon_body.model.parse_tag(tag_format, report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, mesh_processing, random_color_gen, tag_format, report)
            elif collection_name == "Machines":
                MODEL = ASSET.machine_body.model.parse_tag(tag_format, report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, mesh_processing, random_color_gen, tag_format, report)
            elif collection_name == "Controls":
                MODEL = ASSET.control_body.model.parse_tag(tag_format, report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, mesh_processing, random_color_gen, tag_format, report)
            elif collection_name == "Light Fixtures":
                MODEL = ASSET.light_fixture.model.parse_tag(tag_format, report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, mesh_processing, random_color_gen, tag_format, report)
            elif collection_name == "Sound Scenery":
                MODEL = ASSET.sound_scenery_body.model.parse_tag(tag_format, report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, mesh_processing, random_color_gen, tag_format, report)

        objects_list.append(ob)

    for element_idx, element in enumerate(tag_block):
        pallete_item = palette[element.type_index]
        tag_name = os.path.basename(pallete_item.name)

        name = "%s_%s" % (tag_name, element_idx)

        ob = objects_list[element.type_index]
        if not ob == None:
            root = bpy.data.objects.new(name, ob.data)
            asset_collection.objects.link(root)

        else:
            root = bpy.data.objects.new(name, None)
            root.empty_display_type = 'ARROWS'
            asset_collection.objects.link(root)
        
        root.parent = level_root
        root.ass_jms.tag_path = pallete_item.name
        root.location = element.position * 100

        if collection_name == "Biped":
            root.lock_location[0] = True
            root.lock_location[1] = True

        rotation = Euler((radians(0.0), radians(0.0), radians(0.0)), 'XYZ')
        roll = Euler((radians(element.rotation[2]), radians(0.0), radians(0.0)), 'XYZ')
        pitch = Euler((radians(0.0), -radians(element.rotation[1]), radians(0.0)), 'XYZ')
        yaw = Euler((radians(0.0), radians(0.0), radians(element.rotation[0])), 'XYZ')
        rotation.rotate(yaw)
        rotation.rotate(pitch)
        rotation.rotate(roll)

        root.rotation_euler = rotation

    for ob in objects_list:
        if not ob == None:
            bpy.data.objects.remove(ob, do_unlink=True)

def generate_netgame_equipment_elements(level_root, tag_block, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen):
    asset_collection = bpy.data.collections.get("Netgame Equipment")
    if asset_collection == None:
        asset_collection = bpy.data.collections.new("Netgame Equipment")
        context.scene.collection.children.link(asset_collection)

    for element_idx, element in enumerate(tag_block):
        ob = None
        object_name = "%s_%s" % (os.path.basename(element.item_collection.name), element_idx)
        ASSET = element.item_collection.parse_tag(tag_format, report, "halo1", "retail")
        if not ASSET == None:
            if len(ASSET.item_permutations) > 0:
                item_perutation_element = ASSET.item_permutations[0]
                ITEM = item_perutation_element.item.parse_tag(tag_format, report, "halo1", "retail")
                if item_perutation_element.item.tag_group == "eqip":
                    MODEL = ITEM.equipment_body.model.parse_tag(tag_format, report, "halo1", "retail")
                    if not MODEL == None:
                        ob = get_object(asset_collection, MODEL, game_version, object_name, mesh_processing, random_color_gen, tag_format, report)
                elif item_perutation_element.item.tag_group == "weap":
                    MODEL = ITEM.weapon_body.model.parse_tag(tag_format, report, "halo1", "retail")
                    if not MODEL == None:
                        ob = get_object(asset_collection, MODEL, game_version, object_name, mesh_processing, random_color_gen, tag_format, report)

        if ob == None:
            ob = bpy.data.objects.new(object_name, None)
            ob.empty_display_type = 'ARROWS'
            asset_collection.objects.link(ob)
        
        ob.parent = level_root
        ob.ass_jms.tag_path = element.item_collection.name
        ob.location = element.position * 100
        ob.rotation_euler = (radians(0.0), radians(0.0), radians(element.facing))

def generate_empties(context, level_root, collection_name, tag_block):
    asset_collection = bpy.data.collections.get(collection_name)
    if asset_collection == None:
        asset_collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(asset_collection)

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

    for element_idx, element in enumerate(tag_block):
        ob = bpy.data.objects.new(element.name, None)

        ob.empty_display_type = 'ARROWS'
        ob.parent = level_root
        ob.location = element.position * 100

        rotation = Euler((radians(0.0), radians(0.0), radians(0.0)), 'XYZ')
        pitch = Euler((radians(0.0), -radians(element.facing[1]), radians(0.0)), 'XYZ')
        yaw = Euler((radians(0.0), radians(0.0), radians(element.facing[0])), 'XYZ')
        rotation.rotate(yaw)
        rotation.rotate(pitch)

        ob.rotation_euler = rotation

        asset_collection.objects.link(ob)

def generate_camera_points(context, level_root, tag_block):
    asset_collection = bpy.data.collections.get("Cutscene Cameras")
    if asset_collection == None:
        asset_collection = bpy.data.collections.new("Cutscene Cameras")
        context.scene.collection.children.link(asset_collection)

    for element_idx, element in enumerate(tag_block):
        camera_data = bpy.data.cameras.new(name='Camera')
        ob = bpy.data.objects.new(element.name, camera_data)

        ob.parent = level_root
        ob.location = element.position * 100

        rotation = Euler((radians(0.0), radians(0.0), radians(0.0)), 'XYZ')
        roll = Euler((radians(element.orientation[2]), radians(0.0), radians(0.0)), 'XYZ')
        pitch = Euler((radians(0.0), -radians(element.orientation[1]), radians(0.0)), 'XYZ')
        yaw = Euler((radians(0.0), radians(0.0), radians(element.orientation[0])), 'XYZ')
        rotation.rotate(yaw)
        rotation.rotate(pitch)
        rotation.rotate(roll)
        
        ob.data.lens_unit = 'FOV'
        ob.data.angle = radians(element.field_of_view)

        ob.rotation_euler = rotation
        ob.rotation_euler.rotate_axis("X", radians(90.0))
        ob.rotation_euler.rotate_axis("Y", radians(-90.0))

        asset_collection.objects.link(ob)

def generate_scenario_scene(context, H1_ASSET, game_version, game_title, file_version, fix_rotations, empty_markers, report, mesh_processing, global_functions, tag_format):
    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors
    levels_collection = bpy.data.collections.get("BSPs")
    if levels_collection == None:
        levels_collection = bpy.data.collections.new("BSPs")
        context.scene.collection.children.link(levels_collection)

    for bsp_idx, bsp in enumerate(H1_ASSET.structure_bsps):
        ASSET = bsp.parse_tag(tag_format, report, "halo1", "retail")
        if not ASSET == None:
            level_collection = bpy.data.collections.get("%s_%s" % (os.path.basename(bsp.name), bsp_idx))
            if level_collection == None:
                level_collection = bpy.data.collections.new("%s_%s" % (os.path.basename(bsp.name), bsp_idx))
                levels_collection.children.link(level_collection)

            build_scene_level.build_scene(context, ASSET, game_version, game_title, file_version, fix_rotations, empty_markers, report, mesh_processing, global_functions, tag_format, level_collection)

    level_root = bpy.data.objects.get("frame_root")
    if level_root == None:
        level_mesh = bpy.data.meshes.new("frame_root")
        level_root = bpy.data.objects.new("frame_root", level_mesh)
        context.collection.objects.link(level_root)

    if len(H1_ASSET.skies) > 0:
        generate_skies(context, level_root, H1_ASSET.skies, tag_format, report)
    if len(H1_ASSET.comments) > 0:
        generate_comments(context, level_root, H1_ASSET.comments)
    if len(H1_ASSET.scenery) > 0:
        generate_object_elements(level_root, "Scenery", H1_ASSET.scenery_palette, H1_ASSET.scenery, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen)
    if len(H1_ASSET.bipeds) > 0:
        generate_object_elements(level_root, "Biped", H1_ASSET.biped_palette, H1_ASSET.bipeds, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen)
    if len(H1_ASSET.vehicles) > 0:
        generate_object_elements(level_root, "Vehicle", H1_ASSET.vehicle_palette, H1_ASSET.vehicles, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen)
    if len(H1_ASSET.equipment) > 0:
        generate_object_elements(level_root, "Equipment", H1_ASSET.equipment_palette, H1_ASSET.equipment, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen)
    if len(H1_ASSET.weapons) > 0:
        generate_object_elements(level_root, "Weapons", H1_ASSET.weapon_palette, H1_ASSET.weapons, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen)
    if len(H1_ASSET.device_machines) > 0:
        generate_object_elements(level_root, "Machines", H1_ASSET.device_machine_palette, H1_ASSET.device_machines, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen)
    if len(H1_ASSET.device_controls) > 0:
        generate_object_elements(level_root, "Controls", H1_ASSET.device_control_palette, H1_ASSET.device_controls, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen)
    if len(H1_ASSET.device_light_fixtures) > 0:
        generate_object_elements(level_root, "Light Fixtures", H1_ASSET.device_light_fixtures_palette, H1_ASSET.device_light_fixtures, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen)
    if len(H1_ASSET.sound_scenery) > 0:
        generate_object_elements(level_root, "Sound Scenery", H1_ASSET.sound_scenery_palette, H1_ASSET.sound_scenery, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen)
    if len(H1_ASSET.player_starting_locations) > 0:
        generate_empties(context, level_root, "Player Starting Locations", H1_ASSET.player_starting_locations)
    if len(H1_ASSET.netgame_flags) > 0:
        generate_empties(context, level_root, "Netgame Flags", H1_ASSET.netgame_flags)
    if len(H1_ASSET.netgame_equipment) > 0:
        generate_netgame_equipment_elements(level_root, H1_ASSET.netgame_equipment, context, game_version, file_version, fix_rotations, report, mesh_processing, tag_format, random_color_gen)
    if len(H1_ASSET.cutscene_flags) > 0:
        generate_camera_flags(context, level_root, "Cutscene Flags", H1_ASSET.cutscene_flags)
    if len(H1_ASSET.cutscene_camera_points) > 0:
        generate_camera_points(context, level_root, H1_ASSET.cutscene_camera_points)
