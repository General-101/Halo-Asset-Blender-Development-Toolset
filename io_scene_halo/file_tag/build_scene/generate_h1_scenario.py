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


from math import radians
from mathutils import Euler, Matrix
from . import build_bsp as build_scene_level
from ...global_functions import global_functions
from ..h1.file_scenario.mesh_helper.build_mesh import get_object
from ..h1.file_scenario.format import DataTypesEnum, ObjectFlags, UnitFlags, VehicleFlags

def generate_skies(context, level_root, tag_block, report):
    asset_collection = bpy.data.collections.get("Skies")
    if asset_collection == None:
        asset_collection = bpy.data.collections.new("Skies")
        context.scene.collection.children.link(asset_collection)

    for element_idx, element in enumerate(tag_block):
        ASSET = element.parse_tag(report, "halo1", "retail")
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

    comment_layer_collection = context.view_layer.layer_collection.children[comment_collection.name]
    context.view_layer.active_layer_collection = comment_layer_collection
    context.view_layer.active_layer_collection.hide_viewport = True
    comment_collection.hide_render = True

    for comment_idx, comment_element in enumerate(comment_tag_block):
        font = bpy.data.curves.new(type="FONT", name="comment")
        font_ob = bpy.data.objects.new("comment_%s" % comment_idx, font)
        font_ob.data.body = comment_element.text

        font_ob.parent = level_root
        font_ob.location = comment_element.position * 100
        comment_collection.objects.link(font_ob)

def set_object_data(ob, tag_path, element):
    element_flags = ObjectFlags(element.placement_flags)

    ob.tag_view.tag_path = tag_path
    ob.tag_view.automatically = ObjectFlags.automatically in element_flags
    ob.tag_view.on_easy = ObjectFlags.on_easy in element_flags
    ob.tag_view.on_normal = ObjectFlags.on_normal in element_flags
    ob.tag_view.on_hard = ObjectFlags.on_hard in element_flags
    ob.tag_view.use_player_appearance = ObjectFlags.use_player_appearance in element_flags
    ob.tag_view.desired_permutation = element.desired_permutation
    ob.tag_view.appearance_player_index = element.appearance_player_index

def set_unit_data(ob, element):
    element_flags = UnitFlags(element.flags)

    ob.tag_view.unit_vitality = element.body_vitality
    ob.tag_view.unit_dead = UnitFlags.dead in element_flags

def set_vehicle_data(ob, element):
    element_flags = VehicleFlags(element.multiplayer_spawn_flags)

    ob.tag_view.multiplayer_team_index = element.multiplayer_team_index
    ob.tag_view.slayer_default = VehicleFlags.slayer_default in element_flags
    ob.tag_view.ctf_default = VehicleFlags.ctf_default in element_flags
    ob.tag_view.king_default = VehicleFlags.king_default in element_flags
    ob.tag_view.oddball_default = VehicleFlags.oddball_default in element_flags
    ob.tag_view.slayer_allowed = VehicleFlags.slayer_allowed in element_flags
    ob.tag_view.ctf_allowed = VehicleFlags.ctf_allowed in element_flags
    ob.tag_view.king_allowed = VehicleFlags.king_allowed in element_flags
    ob.tag_view.oddball_allowed = VehicleFlags.oddball_allowed in element_flags

def get_data_type(collection_name, root, tag_path, element):
        if collection_name == "BSPs":
            root.tag_view.data_type_enum = str(DataTypesEnum.clusters.value)
            root.tag_view.lightmap_index = -1

        elif collection_name == "Scenery":
            root.tag_view.data_type_enum = str(DataTypesEnum.scenery.value)
            set_object_data(root, tag_path, element)

        elif collection_name == "Biped":
            root.lock_rotation[0] = True
            root.lock_rotation[1] = True

            root.tag_view.data_type_enum = str(DataTypesEnum.bipeds.value)
            set_object_data(root, tag_path, element)
            set_unit_data(root, element)

        elif collection_name == "Vehicle":
            root.tag_view.data_type_enum = str(DataTypesEnum.vehicles.value)
            set_object_data(root, tag_path, element)
            set_unit_data(root, element)
            set_vehicle_data(root, element)

        elif collection_name == "Equipment":
            root.tag_view.data_type_enum = str(DataTypesEnum.equipment.value)
            set_object_data(root, tag_path, element)

        elif collection_name == "Weapons":
            root.tag_view.data_type_enum = str(DataTypesEnum.weapons.value)
            set_object_data(root, tag_path, element)

        elif collection_name == "Machines":
            root.tag_view.data_type_enum = str(DataTypesEnum.machines.value)
            set_object_data(root, tag_path, element)

        elif collection_name == "Controls":
            root.tag_view.data_type_enum = str(DataTypesEnum.controls.value)
            set_object_data(root, tag_path, element)

        elif collection_name == "Light Fixtures":
            root.tag_view.data_type_enum = str(DataTypesEnum.light_fixtures.value)
            set_object_data(root, tag_path, element)

        elif collection_name == "Sound Scenery":
            root.tag_view.data_type_enum = str(DataTypesEnum.sound_scenery.value)
            set_object_data(root, tag_path, element)

        elif collection_name == "Player Starting Locations":
            root.tag_view.data_type_enum = str(DataTypesEnum.player_starting_locations.value)

        elif collection_name == "Netgame Flags":
            root.tag_view.data_type_enum = str(DataTypesEnum.netgame_flags.value)

        elif collection_name == "Netgame Equipment":
            root.tag_view.data_type_enum = str(DataTypesEnum.netgame_equipment.value)

def generate_object_elements(level_root, collection_name, palette, tag_block, context, game_version, file_version, fix_rotations, report, random_color_gen):
    objects_list = []
    asset_collection = bpy.data.collections.get(collection_name)
    if asset_collection == None:
        asset_collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(asset_collection)

    if collection_name == "Scenery":
        asset_collection.hide_render = False
    elif collection_name == "Biped":
        asset_collection.hide_render = True
    elif collection_name == "Vehicle":
        asset_collection.hide_render = True
    elif collection_name == "Equipment":
        asset_collection.hide_render = True
    elif collection_name == "Weapons":
        asset_collection.hide_render = True
    elif collection_name == "Machines":
        asset_collection.hide_render = True
    elif collection_name == "Controls":
        asset_collection.hide_render = True
    elif collection_name == "Light Fixtures":
        asset_collection.hide_render = True
    elif collection_name == "Sound Scenery":
        asset_collection.hide_render = True

    for palette_idx, palette_element in enumerate(palette):
        ob = None
        object_name = "temp_%s_%s" % (os.path.basename(palette_element.name), palette_idx)
        ASSET = palette_element.parse_tag(report, "halo1", "retail")
        if not ASSET == None:
            if collection_name == "Scenery":
                MODEL = ASSET.scenery_body.model.parse_tag(report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, random_color_gen, report)
            elif collection_name == "Biped":
                MODEL = ASSET.biped_body.model.parse_tag(report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, random_color_gen, report)
            elif collection_name == "Vehicle":
                MODEL = ASSET.vehicle_body.model.parse_tag(report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, random_color_gen, report)
            elif collection_name == "Equipment":
                MODEL = ASSET.equipment_body.model.parse_tag(report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, random_color_gen, report)
            elif collection_name == "Weapons":
                MODEL = ASSET.model.parse_tag(report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, random_color_gen, report)
            elif collection_name == "Machines":
                MODEL = ASSET.machine_body.model.parse_tag(report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, random_color_gen, report)
            elif collection_name == "Controls":
                MODEL = ASSET.control_body.model.parse_tag(report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, random_color_gen, report)
            elif collection_name == "Light Fixtures":
                MODEL = ASSET.light_fixture.model.parse_tag(report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, random_color_gen, report)
            elif collection_name == "Sound Scenery":
                MODEL = ASSET.sound_scenery_body.model.parse_tag(report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, random_color_gen, report)

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
        root.location = element.position * 100

        get_data_type(collection_name, root, pallete_item.name, element)

        rotation = Euler((radians(0.0), radians(0.0), radians(0.0)), 'XYZ')
        roll = Euler((radians(element.rotation[2]), radians(0.0), radians(0.0)), 'XYZ')
        pitch = Euler((radians(0.0), -radians(element.rotation[1]), radians(0.0)), 'XYZ')
        yaw = Euler((radians(0.0), radians(0.0), radians(element.rotation[0])), 'XYZ')
        rotation.rotate(yaw)
        rotation.rotate(pitch)
        rotation.rotate(roll)

        root.rotation_euler = rotation

        if collection_name == "Scenery" and ObjectFlags.automatically in ObjectFlags(element.placement_flags):
            root.hide_set(True)
            root.hide_render = True

    for ob in objects_list:
        if not ob == None:
            bpy.data.objects.remove(ob, do_unlink=True)

def generate_netgame_equipment_elements(level_root, tag_block, context, game_version, file_version, fix_rotations, report, random_color_gen):
    asset_collection = bpy.data.collections.get("Netgame Equipment")
    if asset_collection == None:
        asset_collection = bpy.data.collections.new("Netgame Equipment")
        context.scene.collection.children.link(asset_collection)

    asset_collection.hide_render = True
    for element_idx, element in enumerate(tag_block):
        ob = None
        object_name = "%s_%s" % (os.path.basename(element.item_collection.name), element_idx)
        ASSET = element.item_collection.parse_tag(report, "halo1", "retail")
        if not ASSET == None:
            if len(ASSET.item_permutations) > 0:
                item_perutation_element = ASSET.item_permutations[0]
                ITEM = item_perutation_element.item.parse_tag(report, "halo1", "retail")
                if item_perutation_element.item.tag_group == "eqip":
                    MODEL = ITEM.equipment_body.model.parse_tag(report, "halo1", "retail")
                    if not MODEL == None:
                        ob = get_object(asset_collection, MODEL, game_version, object_name, random_color_gen, report)
                elif item_perutation_element.item.tag_group == "weap":
                    MODEL = ITEM.model.parse_tag(report, "halo1", "retail")
                    if not MODEL == None:
                        ob = get_object(asset_collection, MODEL, game_version, object_name, random_color_gen, report)

        if ob == None:
            ob = bpy.data.objects.new(object_name, None)
            ob.empty_display_type = 'ARROWS'
            asset_collection.objects.link(ob)

        get_data_type("Netgame Equipment", ob, element.item_collection.name, element)

        ob.parent = level_root
        ob.location = element.position * 100
        ob.rotation_euler = (radians(0.0), radians(0.0), radians(element.facing))

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

def generate_trigger_volumes(context, level_root, collection_name, tag_block):
    asset_collection = bpy.data.collections.get(collection_name)
    if asset_collection == None:
        asset_collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(asset_collection)

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

def generate_scenario_scene(context, H1_ASSET, game_version, game_title, file_version, fix_rotations, empty_markers, report):
    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors
    levels_collection = bpy.data.collections.get("BSPs")
    if levels_collection == None:
        levels_collection = bpy.data.collections.new("BSPs")
        context.scene.collection.children.link(levels_collection)

    for bsp_idx, bsp in enumerate(H1_ASSET.structure_bsps):
        ASSET = bsp.parse_tag(report, "halo1", "retail")
        if not ASSET == None:
            level_collection = bpy.data.collections.get("%s_%s" % (os.path.basename(bsp.name), bsp_idx))
            if level_collection == None:
                level_collection = bpy.data.collections.new("%s_%s" % (os.path.basename(bsp.name), bsp_idx))
                clusters_collection = bpy.data.collections.new("%s_clusters" % (os.path.basename(bsp.name)))
                levels_collection.children.link(level_collection)
                level_collection.children.link(clusters_collection)

            build_scene_level.build_scene(context, ASSET, game_version, game_title, file_version, fix_rotations, empty_markers, report, level_collection, clusters_collection)

    level_root = bpy.data.objects.get("frame_root")
    if level_root == None:
        level_mesh = bpy.data.meshes.new("frame_root")
        level_root = bpy.data.objects.new("frame_root", level_mesh)
        context.collection.objects.link(level_root)

    if len(H1_ASSET.skies) > 0:
        generate_skies(context, level_root, H1_ASSET.skies, report)
    if len(H1_ASSET.comments) > 0:
        generate_comments(context, level_root, H1_ASSET.comments)
    if len(H1_ASSET.scenery) > 0:
        generate_object_elements(level_root, "Scenery", H1_ASSET.scenery_palette, H1_ASSET.scenery, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H1_ASSET.bipeds) > 0:
        generate_object_elements(level_root, "Biped", H1_ASSET.biped_palette, H1_ASSET.bipeds, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H1_ASSET.vehicles) > 0:
        generate_object_elements(level_root, "Vehicle", H1_ASSET.vehicle_palette, H1_ASSET.vehicles, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H1_ASSET.equipment) > 0:
        generate_object_elements(level_root, "Equipment", H1_ASSET.equipment_palette, H1_ASSET.equipment, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H1_ASSET.weapons) > 0:
        generate_object_elements(level_root, "Weapons", H1_ASSET.weapon_palette, H1_ASSET.weapons, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H1_ASSET.device_machines) > 0:
        generate_object_elements(level_root, "Machines", H1_ASSET.device_machine_palette, H1_ASSET.device_machines, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H1_ASSET.device_controls) > 0:
        generate_object_elements(level_root, "Controls", H1_ASSET.device_control_palette, H1_ASSET.device_controls, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H1_ASSET.device_light_fixtures) > 0:
        generate_object_elements(level_root, "Light Fixtures", H1_ASSET.device_light_fixtures_palette, H1_ASSET.device_light_fixtures, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H1_ASSET.sound_scenery) > 0:
        generate_object_elements(level_root, "Sound Scenery", H1_ASSET.sound_scenery_palette, H1_ASSET.sound_scenery, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H1_ASSET.player_starting_locations) > 0:
        generate_empties(context, level_root, "Player Starting Locations", H1_ASSET.player_starting_locations)
    if len(H1_ASSET.netgame_flags) > 0:
        generate_empties(context, level_root, "Netgame Flags", H1_ASSET.netgame_flags)
    if len(H1_ASSET.netgame_equipment) > 0:
        generate_netgame_equipment_elements(level_root, H1_ASSET.netgame_equipment, context, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H1_ASSET.trigger_volumes) > 0:
        generate_trigger_volumes(context, level_root, "Trigger Volumes", H1_ASSET.trigger_volumes)
    if len(H1_ASSET.cutscene_flags) > 0:
        generate_camera_flags(context, level_root, "Cutscene Flags", H1_ASSET.cutscene_flags)
    if len(H1_ASSET.cutscene_camera_points) > 0:
        generate_camera_points(context, level_root, H1_ASSET.cutscene_camera_points)
