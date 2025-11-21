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

from enum import Flag, Enum, auto
from mathutils import Euler, Matrix, Vector
from . import build_bsp as build_scene_level
from ...global_functions import global_functions
from . import build_lightmap as build_scene_lightmap
from ...file_tag.tag_interface import tag_interface
from math import radians, degrees, cos, sin, asin, atan2
from ...file_tag.tag_interface.tag_common import h2_tag_groups
from ..h2.file_render_model.build_mesh import get_geometry_layout
from ...global_functions.shader_generation.shader_helper import convert_to_blender_color

class ScenarioFlags(Flag):
    cortana_hack = auto()
    always_draw_sky = auto()
    dont_strip_pathfinding = auto()
    symmetric_multiplayer_map = auto()
    quick_loading_cinematic_only_scenario = auto()
    characters_use_previous_mission_weapons = auto()
    lightmaps_smooth_palettes_with_neighbors = auto()
    snap_to_white_at_start = auto()
    do_not_apply_bungie_mp_tag_patches = auto()

class ObjectFlags(Flag):
    not_automatically = auto()
    unused_0 = auto()
    unused_1 = auto()
    unused_2 = auto()
    lock_type_to_env_object = auto()
    lock_transform_to_env_object = auto()
    never_placed = auto()
    lock_name_to_env_object = auto()
    create_at_rest = auto()

class TransformFlags(Flag):
    mirrored = auto()

class ObjectTypeEnum(Enum):
    biped = 0
    vehicle = auto()
    weapon = auto()
    equipment = auto()
    garbage = auto()
    projectile = auto()
    scenery = auto()
    machine = auto()
    control = auto()
    light_fixture = auto()
    sound_scenery = auto()
    crate = auto()
    creature = auto()

class ObjectSourceEnum(Enum):
    structure = 0
    editor = auto()
    dynamic = auto()
    legacy = auto()

class ObjectBSPPolicyEnum(Enum):
    default = 0
    always_placed = auto()
    manual_bsp_placement = auto()

class ObjectColorChangeFlags(Flag):
    primary = auto()
    secondary = auto()
    tertiary = auto()
    quaternary = auto()

class PathfindingPolicyEnum(Enum):
    tag_default = 0
    pathfinding_dynamic = auto()
    pathfinding_cut_out = auto()
    pathfinding_static = auto()
    pathfinding_none = auto()

class LightmappingPolicyEnum(Enum):
    tag_default = 0
    dynamic = auto()
    per_vertex = auto()

class ObjectGametypeFlags(Flag):
    ctf = auto()
    slayer = auto()
    oddball = auto()
    king = auto()
    juggernaut = auto()
    territories = auto()
    assault = auto()
    medic = auto()
    vip = auto()
    infection = auto()
    headhunter = auto()

class UnitFlags(Flag):
    dead = auto()
    closed = auto()
    not_enterable_by_player = auto()

class ItemFlags(Flag):
    initially_at_rest_doesnt_fall = auto()
    obsolete = auto()
    does_accelerate_moves_due_to_explosions = auto()

class DeviceFlags(Flag):
    initially_open = auto()
    initially_off = auto()
    can_change_only_once = auto()
    position_reversed = auto()
    not_usable_from_any_side = auto()

class MachineFlags(Flag):
    does_not_operate_automatically = auto()
    one_sided = auto()
    never_appears_locked = auto()
    opened_by_melee_attack = auto()
    one_sided_for_player = auto()
    does_not_close_automatically = auto()

class ControlFlags(Flag):
    usable_from_both_sides = auto()

class NetGameFlags(Flag):
    multi_flagbomb = auto()
    single_flagbomb = auto()
    neutral_flagbomb = auto()

class NetGameEquipmentFlags(Flag):
    levitate = auto()
    destroy_existing_on_new_spawn = auto()

class ClassificationEnum(Enum):
    weapon = 0
    primary_light_land = auto()
    secondary_light_land = auto()
    primary_heavy_land = auto()
    primary_flying = auto()
    secondary_heavy_land = auto()
    primary_turret = auto()
    secondary_turret = auto()
    grenade = auto()
    powerup = auto()

class LightFlags(Flag):
    custom_geometry = auto()
    unused = auto()
    cinematic_only = auto()

class LightmapTypeEnum(Enum):
    use_light_tag_settings = 0
    dynamic_only = auto()
    dynamic_with_lightmaps = auto()
    lightmaps_only = auto()

class SCNRLightmappingPolicyEnum(Enum):
    tag_default = 0
    dynamic = auto()
    per_vertex = auto()

class ShapeTypeEnum(Enum):
    sphere = 0
    orthogonal = auto()
    projective = auto()
    pyramid = auto()

class DefaultLightmapSettingEnum(Enum):
    dynamic_only = 0
    dynamic_with_lightmaps = auto()
    lightmaps_only = auto()

class LightmappingPolicyEnum(Enum):
    per_vertex = 0
    per_pixel = auto()
    dynamic = auto()

def get_tag_display(tag_ref):
    tag_display = ""
    if not global_functions.string_empty_check(tag_ref["path"]):
        tag_display = "%s.%s" % (tag_ref["path"], h2_tag_groups.get(tag_ref["group name"]))

    return tag_display

def set_scenario_data(context, scnr_data):
    context.scene.tag_scenario.dont_use = get_tag_display(scnr_data["DON'T USE"])
    context.scene.tag_scenario.scenario_type_enum = str(scnr_data["type"]["value"])

    scenario_flags = ScenarioFlags(scnr_data["flags"])
    context.scene.tag_scenario.cortana_hack = ScenarioFlags.cortana_hack in scenario_flags
    context.scene.tag_scenario.always_draw_sky = ScenarioFlags.always_draw_sky in scenario_flags
    context.scene.tag_scenario.dont_strip_pathfinding = ScenarioFlags.dont_strip_pathfinding in scenario_flags
    context.scene.tag_scenario.symmetric_multiplayer_map = ScenarioFlags.symmetric_multiplayer_map in scenario_flags
    context.scene.tag_scenario.quick_loading_cinematic_only_scenario = ScenarioFlags.quick_loading_cinematic_only_scenario in scenario_flags
    context.scene.tag_scenario.characters_use_previous_mission_weapons = ScenarioFlags.characters_use_previous_mission_weapons in scenario_flags
    context.scene.tag_scenario.lightmaps_smooth_palettes_with_neighbors = ScenarioFlags.lightmaps_smooth_palettes_with_neighbors in scenario_flags
    context.scene.tag_scenario.snap_to_white_at_start = ScenarioFlags.snap_to_white_at_start in scenario_flags
    context.scene.tag_scenario.do_not_apply_bungie_campaign_patches = ScenarioFlags.do_not_apply_bungie_mp_tag_patches in scenario_flags

    context.scene.tag_scenario.local_north = radians(scnr_data["local north"])
    context.scene.tag_scenario.custom_object_names = get_tag_display(scnr_data["custom object names"])
    context.scene.tag_scenario.ingame_help_text = get_tag_display(scnr_data["chapter title text"])
    context.scene.tag_scenario.hud_messages = get_tag_display(scnr_data["hud messages"])

def set_object_data(ob, tag_path, element, object_name_tag_block):
    element_object_flags = ObjectFlags(element["placement flags"])
    element_transform_flags = TransformFlags(element["WordFlags"])

    object_name = ""
    if element["name"] >= 0 and element["name"] < len(object_name_tag_block):
        object_name = object_name_tag_block[element["name"]]["name"]
        
    ob.tag_object.tag_path = tag_path
    ob.tag_object.object_name = object_name
    ob.tag_object.automatically = ObjectFlags.not_automatically in element_object_flags
    ob.tag_object.on_easy = ObjectFlags.unused_0 in element_object_flags
    ob.tag_object.on_normal = ObjectFlags.unused_1 in element_object_flags
    ob.tag_object.on_hard = ObjectFlags.unused_2 in element_object_flags
    ob.tag_object.lock_type_to_env_object = ObjectFlags.lock_type_to_env_object in element_object_flags
    ob.tag_object.lock_transform_to_env_object = ObjectFlags.lock_transform_to_env_object in element_object_flags
    ob.tag_object.never_placed = ObjectFlags.never_placed in element_object_flags
    ob.tag_object.lock_name_to_env_object = ObjectFlags.lock_name_to_env_object in element_object_flags
    ob.tag_object.create_at_rest = ObjectFlags.create_at_rest in element_object_flags

    ob.tag_object.mirrored = TransformFlags.mirrored in element_transform_flags
    ob.tag_object.manual_bsp_flags = element["manual bsp flags"]
    ob.tag_object.unique_id = element["unique id"]
    ob.tag_object.origin_bsp_index = element["origin bsp index"]
    ob.tag_object.object_type = str(element["type_1"]["value"])
    ob.tag_object.object_source = str(element["source"]["value"])
    ob.tag_object.bsp_policy = str(element["bsp policy"]["value"])
    ob.tag_object.editor_folder_index = element["ShortBlockIndex"]

def set_permutation_data(ob, element):
    element_color_flags = ObjectColorChangeFlags(element["active change colors"])

    ob.tag_permutation.variant_name = element["variant name"]
    ob.tag_permutation.primary = ObjectColorChangeFlags.primary in element_color_flags
    ob.tag_permutation.secondary = ObjectColorChangeFlags.secondary in element_color_flags
    ob.tag_permutation.tertiary = ObjectColorChangeFlags.tertiary in element_color_flags
    ob.tag_permutation.quaternary = ObjectColorChangeFlags.quaternary in element_color_flags
    ob.tag_permutation.primary_color = convert_to_blender_color(element["primary color"], False)
    ob.tag_permutation.secondary_color = convert_to_blender_color(element["secondary color"], False)
    ob.tag_permutation.tertiary_color = convert_to_blender_color(element["tertiary color"], False)
    ob.tag_permutation.quaternary_color = convert_to_blender_color(element["quaternary color"], False)

def set_scenery_data(ob, element):
    element_game_flags = ObjectGametypeFlags(element["valid multiplayer games"])

    ob.tag_scenery.pathfinding_policy = str(element["Pathfinding policy"]["value"])
    ob.tag_scenery.lightmapping_policy = str(element["Lightmapping policy"]["value"])
    ob.tag_scenery.ctf = ObjectGametypeFlags.ctf in element_game_flags
    ob.tag_scenery.slayer = ObjectGametypeFlags.slayer in element_game_flags
    ob.tag_scenery.oddball = ObjectGametypeFlags.oddball in element_game_flags
    ob.tag_scenery.king = ObjectGametypeFlags.king in element_game_flags
    ob.tag_scenery.juggernaut = ObjectGametypeFlags.juggernaut in element_game_flags
    ob.tag_scenery.territories = ObjectGametypeFlags.territories in element_game_flags
    ob.tag_scenery.assault = ObjectGametypeFlags.assault in element_game_flags
    ob.tag_scenery.medic = ObjectGametypeFlags.medic in element_game_flags
    ob.tag_scenery.vip = ObjectGametypeFlags.vip in element_game_flags
    ob.tag_scenery.infection = ObjectGametypeFlags.infection in element_game_flags
    ob.tag_scenery.headhunter = ObjectGametypeFlags.headhunter in element_game_flags

def set_unit_data(ob, element):
    element_flags = UnitFlags(element["flags"])

    ob.tag_unit.unit_vitality = element["body vitality"]
    ob.tag_unit.unit_dead = UnitFlags.dead in element_flags
    ob.tag_unit.unit_closed = UnitFlags.closed in element_flags
    ob.tag_unit.unit_not_enterable_by_player = UnitFlags.not_enterable_by_player in element_flags

def set_item_data(ob, element_flags):
    item_flags = ItemFlags(element_flags)

    ob.tag_item.initially_at_rest = ItemFlags.initially_at_rest_doesnt_fall in item_flags
    ob.tag_item.obsolete = ItemFlags.obsolete in item_flags
    ob.tag_item.does_accelerate = ItemFlags.does_accelerate_moves_due_to_explosions in item_flags

def set_device_data(ob, element_flags):
    device_flags = DeviceFlags(element_flags)

    ob.tag_device.initially_open = DeviceFlags.initially_open in device_flags
    ob.tag_device.initially_off = DeviceFlags.initially_off in device_flags
    ob.tag_device.can_change_only_once = DeviceFlags.can_change_only_once in device_flags
    ob.tag_device.position_reversed = DeviceFlags.position_reversed in device_flags
    ob.tag_device.not_usable_from_any_side = DeviceFlags.not_usable_from_any_side in device_flags

def set_machine_data(ob, element_flags):
    machine_flags = MachineFlags(element_flags)

    ob.tag_machine.does_not_operate_automatically = MachineFlags.does_not_operate_automatically in machine_flags
    ob.tag_machine.one_sided = MachineFlags.one_sided in machine_flags
    ob.tag_machine.never_appears_locked = MachineFlags.never_appears_locked in machine_flags
    ob.tag_machine.opened_by_melee_attack = MachineFlags.opened_by_melee_attack in machine_flags
    ob.tag_machine.one_sided_for_player = MachineFlags.one_sided_for_player in machine_flags
    ob.tag_machine.does_not_close_automatically = MachineFlags.does_not_close_automatically in machine_flags

def set_control_data(ob, element_flags):
    control_flags = ControlFlags(element_flags)

    ob.tag_control.usable_from_both_sides = ControlFlags.usable_from_both_sides in control_flags

def set_sound_scenery_data(ob, element):
    ob.tag_sound_scenery.volume_type = str(element["volume type"]["value"])
    ob.tag_sound_scenery.height = element["height"]
    ob.tag_sound_scenery.override_distance_bounds_min = element["override distance bounds"]["Min"]
    ob.tag_sound_scenery.override_distance_bounds_max = element["override distance bounds"]["Max"]
    ob.tag_sound_scenery.override_cone_angle_bounds_min = element["override cone angle bounds"]["Min"]
    ob.tag_sound_scenery.override_cone_angle_bounds_max = element["override cone angle bounds"]["Max"]
    ob.tag_sound_scenery.override_outer_cone_gain = element["override outer cone gain"]

def get_data_type(ob, ob_parent, element, scnr_data, tag_path="", block_indices=(), level_root=None):
        ob_parent_name = ob_parent.name.lower().replace(" ", "_")

        if ob_parent_name.startswith("bsps"):
            ob.tag_mesh.lightmap_index = -1

        elif ob_parent_name.startswith("scenery"):
            set_object_data(ob, tag_path, element, scnr_data["object names"])
            set_permutation_data(ob, element)
            set_scenery_data(ob, element)

        elif ob_parent_name.startswith("biped"):
            ob.lock_rotation[0] = True
            ob.lock_rotation[1] = True

            set_object_data(ob, tag_path, element, scnr_data["object names"])
            set_permutation_data(ob, element)
            set_unit_data(ob, element)

        elif ob_parent_name.startswith("vehicle"):
            set_object_data(ob, tag_path, element, scnr_data["object names"])
            set_permutation_data(ob, element)
            set_unit_data(ob, element)

        elif ob_parent_name.startswith("equipment"):
            set_object_data(ob, tag_path, element, scnr_data["object names"])
            set_item_data(ob, element["equipment flags"])

        elif ob_parent_name.startswith("weapons"):
            set_object_data(ob, tag_path, element, scnr_data["object names"])
            set_permutation_data(ob, element)
            ob.tag_weapon.rounds_left = element["rounds left"]
            ob.tag_weapon.rounds_loaded = element["rounds loaded"]
            set_item_data(ob, element["flags"])

        elif ob_parent_name.startswith("machines"):
            set_object_data(ob, tag_path, element, scnr_data["object names"])
            ob.tag_device.power_group = element["power group"]
            ob.tag_device.position_group = element["position group"]
            set_device_data(ob, element["flags"])
            set_machine_data(ob, element["flags_1"])

        elif ob_parent_name.startswith("controls"):
            set_object_data(ob, tag_path, element, scnr_data["object names"])
            ob.tag_device.power_group = element["power group"]
            ob.tag_device.position_group = element["position group"]
            set_device_data(ob, element["flags"])
            set_control_data(ob, element["flags_1"])
            ob.tag_control.control_value = element["DON'T TOUCH THIS"]

        elif ob_parent_name.startswith("light_fixtures"):
            set_object_data(ob, tag_path, element, scnr_data["object names"])
            ob.tag_device.power_group = element["power group"]
            ob.tag_device.position_group = element["position group"]
            set_device_data(ob, element["flags"])
            ob.tag_light_fixture.color = convert_to_blender_color(element["color"], False)
            ob.tag_light_fixture.intensity = element["intensity"]
            ob.tag_light_fixture.falloff_angle = element["falloff angle"]
            ob.tag_light_fixture.cutoff_angle = element["cutoff angle"]

        elif ob_parent_name.startswith("sound_scenery"):
            set_object_data(ob, tag_path, element, scnr_data["object names"])
            set_sound_scenery_data(ob, element)

        elif ob_parent_name.startswith("lights"):
            set_object_data(ob, tag_path, element, scnr_data["object names"])

        elif ob_parent_name.startswith("player_starting_locations"):
            ob.lock_rotation[0] = True
            ob.lock_rotation[1] = True

            ob.tag_player_starting_location.team_designator = str(element["team designator"]["value"])
            ob.tag_player_starting_location.bsp_index = element["bsp index"]
            ob.tag_player_starting_location.type_0 = element["type 0"]["value"]
            ob.tag_player_starting_location.type_1 = element["type 1"]["value"]
            ob.tag_player_starting_location.type_2 = element["type 2"]["value"]
            ob.tag_player_starting_location.type_3 = element["type 3"]["value"]
            ob.tag_player_starting_location.spawn_type_0 = str(element["spawn type 0"]["value"])
            ob.tag_player_starting_location.spawn_type_1 = str(element["spawn type 1"]["value"])
            ob.tag_player_starting_location.spawn_type_2 = str(element["spawn type 2"]["value"])
            ob.tag_player_starting_location.spawn_type_3 = str(element["spawn type 3"]["value"])
            ob.tag_player_starting_location.unused_name_0 = element["unused_names0"]
            ob.tag_player_starting_location.unused_name_1 = element["unused_names1"]
            ob.tag_player_starting_location.campaign_player_type = str(element["campaign player type"]["value"])

        elif ob_parent_name.startswith("netgame_flags"):
            ob.tag_netgame_flag.netgame_type = element["type"]["value"]
            ob.tag_netgame_flag.team_designator = str(element["team designator"]["value"])
            ob.tag_netgame_flag.usage_id = element["identifier"]

            gametype_flags = NetGameFlags(element["flags"])

            ob.tag_netgame_flag.multi_flagbomb = NetGameFlags.multi_flagbomb in gametype_flags
            ob.tag_netgame_flag.single_flagbomb = NetGameFlags.single_flagbomb in gametype_flags
            ob.tag_netgame_flag.neutral_flagbomb = NetGameFlags.neutral_flagbomb in gametype_flags

            ob.tag_netgame_flag.spawn_object_name = element["spawn_object_name"]
            ob.tag_netgame_flag.spawn_marker_name = element["spawn_marker_name"]

        elif ob_parent_name.startswith("netgame_equipment"):
            element_flags = NetGameEquipmentFlags(element["flags"])

            ob.tag_netgame_equipment.levitate = NetGameEquipmentFlags.levitate in element_flags
            ob.tag_netgame_equipment.destroy_existing_on_new_spawn = NetGameEquipmentFlags.destroy_existing_on_new_spawn in element_flags
            ob.tag_netgame_equipment.type_0 = element["type 0"]["value"]
            ob.tag_netgame_equipment.type_1 = element["type 1"]["value"]
            ob.tag_netgame_equipment.type_2 = element["type 2"]["value"]
            ob.tag_netgame_equipment.type_3 = element["type 3"]["value"]
            ob.tag_netgame_equipment.spawn_time = element["spawn time (in seconds, 0 = default)"]
            ob.tag_netgame_equipment.respawn_on_empty_time = element["respawn on empty time"]
            ob.tag_netgame_equipment.respawn_timer_starts = str(element["respawn timer starts"]["value"])
            ob.tag_netgame_equipment.classification = str(element["classification"]["value"])
            ob.tag_netgame_equipment.item_collection = tag_path

        elif ob_parent_name.startswith("decal"):
            ob.tag_decal.decal_type = tag_path
            ob.tag_decal.yaw = element["yaw[-127,127]"]
            ob.tag_decal.pitch = element["pitch[-127,127]"]

        elif ob_parent_name.startswith("cutscene_flags"):
            ob.tag_cutscene_flag.name = element["name"]

        elif ob_parent_name.startswith("cutscene_cameras"):
            ob.tag_cutscene_camera.name = element["name"]

        elif ob_parent_name.startswith("crates"):
            set_object_data(ob, tag_path, element, scnr_data["object names"])
            set_permutation_data(ob, element)

        elif ob_parent_name.startswith("creatures"):
            set_object_data(ob, tag_path, element, scnr_data["object names"])

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
    forward = Vector((0, 0, (yaw / max_value)))
    up = Vector((0, (pitch / max_value), 0))

    right = np.cross(up, forward)
    rot_matrix = Matrix((forward, right, up))

    return Matrix(rot_matrix).inverted_safe().to_euler()

def generate_skies(context, level_root, scnr_data, asset_cache):
    asset_collection = global_functions.get_referenced_collection("Skies", context.scene.collection, False)
    for element_idx, element in enumerate(scnr_data["skies"]):
        sky_asset = tag_interface.get_disk_asset(element["sky"]["path"], h2_tag_groups.get(element["sky"]["group name"]))
        tag_name = os.path.basename(element["sky"]["path"])
        sky_collection = global_functions.get_referenced_collection("sky_%s_%s" % (tag_name, element_idx), asset_collection, False)
        if not sky_asset == None:
            sky_data = sky_asset["Data"]
            for light_idx, light in enumerate(sky_data["lights"]):
                for radiosity in light["radiosity"]:
                    name = "%s_light_%s" % (tag_name, light_idx)
                    light_data = bpy.data.lights.new(name, "SUN")
                    ob = bpy.data.objects.new(name, light_data)
                    ob.color = (1, 1, 1, 0)

                    ob.data.color = convert_to_blender_color(radiosity["color"], False)
                    ob.data.energy = radiosity["power"] * 10
                    ob.parent = level_root

                    yaw, pitch = light["direction"]

                    euler = Euler((0, radians(90), 0), 'XYZ')
                    rot_matrix = euler.to_matrix()

                    rot_z = Matrix.Rotation(radians(yaw), 3, 'Z')
                    rot_y = Matrix.Rotation(radians(-pitch), 3, 'Y')

                    rot_matrix = rot_z @ rot_matrix
                    rot_matrix = rot_matrix @ rot_y 

                    ob.rotation_euler = rot_matrix.to_euler('XYZ')

                    sky_collection.objects.link(ob)

        sky_collection.tag_sky.sky_path = get_tag_display(element["sky"])

def generate_comments(context, level_root, scnr_data, asset_cache):
    asset_collection = global_functions.get_referenced_collection("Comments", context.scene.collection, True)
    for comment_idx, comment_element in enumerate(scnr_data["comments"]):
        font = bpy.data.curves.new(type="FONT", name="%s_%s" % (comment_element["name"], comment_idx))
        font_ob = bpy.data.objects.new("%s_%s" % (comment_element["name"], comment_idx), font)
        font_ob.color = (1, 1, 1, 0)
        font_ob.data.body = comment_element["comment"]

        font_ob.parent = level_root
        font_ob.location = Vector(comment_element["position"]) * 100
        asset_collection.objects.link(font_ob)

def generate_object_elements(context, level_root, collection_name, scnr_data, asset_cache, fix_rotations, report, random_color_gen):
    hide_collection = False
    tag_block = None
    tag_palette = None
    if collection_name == "Scenery":
        hide_collection = False
        tag_block = scnr_data["scenery"]
        tag_palette = scnr_data["scenery palette"]
    elif collection_name == "Bipeds":
        hide_collection = True
        tag_block = scnr_data["bipeds"]
        tag_palette = scnr_data["biped palette"]
    elif collection_name == "Vehicles":
        hide_collection = True
        tag_block = scnr_data["vehicles"]
        tag_palette = scnr_data["vehicle palette"]
    elif collection_name == "Equipment":
        hide_collection = True
        tag_block = scnr_data["equipment"]
        tag_palette = scnr_data["equipment palette"]
    elif collection_name == "Weapons":
        hide_collection = True
        tag_block = scnr_data["weapons"]
        tag_palette = scnr_data["weapon palette"]
    elif collection_name == "Machines":
        hide_collection = True
        tag_block = scnr_data["machines"]
        tag_palette = scnr_data["machine palette"]
    elif collection_name == "Controls":
        hide_collection = True
        tag_block = scnr_data["controls"]
        tag_palette = scnr_data["control palette"]
    elif collection_name == "Light Fixtures":
        hide_collection = False
        tag_block = scnr_data["light fixtures"]
        tag_palette = scnr_data["light fixtures palette"]
    elif collection_name == "Sound Scenery":
        hide_collection = True
        tag_block = scnr_data["sound scenery"]
        tag_palette = scnr_data["sound scenery palette"]
    elif collection_name == "Crates":
        hide_collection = True
        tag_block = scnr_data["crates"]
        tag_palette = scnr_data["crate palette"]
    elif collection_name == "Creatures":
        hide_collection = True
        tag_block = scnr_data["creatures"]
        tag_palette = scnr_data["creature palette"]

    asset_collection = global_functions.get_referenced_collection(collection_name, context.scene.collection, hide_collection)
    palette_count = len(tag_palette)
    for element_idx, element in enumerate(tag_block):
        variant_name = ""
        variant_element = None
        tag_path = ""
        mesh_data = None
        tag_path_no_ext = ""
        if element["type"] >= 0 and element["type"] < palette_count:
            if element.get("variant name") is not None:
                variant_name = element["variant name"]

            pallete_item = tag_palette[element["type"]]["name"]
            tag_path_no_ext = pallete_item["path"]
            tag_path = "%s.%s" % (pallete_item["path"], h2_tag_groups.get(pallete_item["group name"]))
            palette_asset = tag_interface.get_disk_asset(pallete_item["path"], h2_tag_groups.get(pallete_item["group name"]))
            if not palette_asset == None:
                if global_functions.string_empty_check(variant_name):
                    variant_name = palette_asset["Data"]["default model variant"]

                mesh_collections = ("Scenery", "Bipeds", "Vehicles", "Equipment", "Weapons", "Machines", "Controls", "Light Fixtures", "Sound Scenery", "Crates", "Creatures")
                if collection_name in mesh_collections:
                    model_asset = tag_interface.get_disk_asset(palette_asset["Data"]["model"]["path"], h2_tag_groups.get(palette_asset["Data"]["model"]["group name"]))
                    if not model_asset == None:
                        if global_functions.string_empty_check(variant_name):
                            variant_name = "default"

                        model_data = model_asset["Data"]
                        for tag_element in model_data["variants"]:
                            if tag_element["name"] == variant_name:
                                variant_element = tag_element

                        render_model_asset = tag_interface.get_disk_asset(model_data["render model"]["path"], h2_tag_groups.get(model_data["render model"]["group name"]))
                        if render_model_asset is not None:
                            render_tag_ref = asset_cache[model_data["render model"]["group name"]][model_data["render model"]["path"]]
                            mesh_data = render_tag_ref["blender_assets"].get("blender_asset")
                            if variant_element:
                                mesh_data = render_tag_ref["blender_assets"].get(variant_element["name"])

                            if render_model_asset is not None and mesh_data is None:
                                get_geometry_layout(model_asset["Data"]["render model"], asset_cache, None, report, True, variant_element)
                                mesh_data = render_tag_ref["blender_assets"].get("blender_asset")
                                if variant_element:
                                    mesh_data = render_tag_ref["blender_assets"].get(variant_element["name"])

        tag_name = "NONE"
        if not global_functions.string_empty_check(tag_path_no_ext):
            tag_name = os.path.basename(tag_path_no_ext)

        name = "%s_%s" % (tag_name, element_idx)
        if not mesh_data == None:
            root = bpy.data.objects.new(name, mesh_data)
            root.color = (1, 1, 1, 0)
            asset_collection.objects.link(root)

        else:
            root = bpy.data.objects.new(name, None)
            root.color = (1, 1, 1, 0)
            root.empty_display_type = 'ARROWS'
            asset_collection.objects.link(root)

        root.parent = level_root
        root.location = Vector(element["position"]) * 100

        get_data_type(root, asset_collection, element, scnr_data, tag_path)

        root.rotation_euler = get_rotation_euler(*element["rotation"])

        if collection_name == "Scenery":
            element_game_flags = element["valid multiplayer games"]
            palette_asset = tag_interface.get_disk_asset(pallete_item["path"], h2_tag_groups.get(pallete_item["group name"]))
            hidden_in_render = False
            if ObjectFlags.not_automatically in ObjectFlags(element["placement flags"]):
                hidden_in_render = True

            lightmap_policy = SCNRLightmappingPolicyEnum(element["Lightmapping policy"]["value"])
            if lightmap_policy == SCNRLightmappingPolicyEnum.tag_default:
                if not palette_asset == None:
                    scenery_policy = LightmappingPolicyEnum(palette_asset["Data"]["lightmapping policy"]["value"])
                    if scenery_policy == LightmappingPolicyEnum.dynamic:
                        hidden_in_render = True
            else:
                if lightmap_policy == SCNRLightmappingPolicyEnum.dynamic:
                    hidden_in_render = True
        
            if element_game_flags != 0:
                hidden_in_render = True

            root.hide_set(hidden_in_render)
            root.hide_render = hidden_in_render 





def generate_light_volumes_elements(context, level_root, collection_name, scnr_data, asset_cache, fix_rotations, report, random_color_gen):
    asset_collection = global_functions.get_referenced_collection(collection_name, context.scene.collection, False)
    for element_idx, element in enumerate(scnr_data["light volumes"]):
        pallete_item = None
        light_asset = None
        if element["type"] >= 0 and element["type"] < len(scnr_data["light volumes palette"]):
            pallete_item = scnr_data["light volumes palette"][element["type"]]["name"]
            light_asset = tag_interface.get_disk_asset(pallete_item["path"], h2_tag_groups.get(pallete_item["group name"]))

        if light_asset is not None: 
            light_data = light_asset["Data"]
            scnr_light_flags = LightFlags(element["flags_1"])
            emission_setting = LightmapTypeEnum(element["lightmap type"]["value"])

            light_name = "%s_%s" % (os.path.basename(pallete_item["path"]), element_idx)
            
            light_shape_type = ShapeTypeEnum(light_data["type"]["value"])
            if LightFlags.custom_geometry in scnr_light_flags:
                light_shape_type = ShapeTypeEnum(element["type_2"]["value"])

            generate_light = False
            if LightmapTypeEnum.use_light_tag_settings == emission_setting:
                emission_setting = DefaultLightmapSettingEnum(light_data["default lightmap setting"]["value"])
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

                light_data_element.color = convert_to_blender_color(light_data["diffuse upper bound"], False)

                tag_light_size_min = light_data["size modifer"]["Min"]
                if tag_light_size_min == 0.0:
                    tag_light_size_min= 1.0
                tag_light_size_max = light_data["size modifer"]["Max"]
                if tag_light_size_max == 0.0:
                    tag_light_size_max= 1.0
                scnr_light_scale = element["lightmap light scale"]
                if scnr_light_scale == 0.0:
                    scnr_light_scale = 1.0

                light_size = max(tag_light_size_min, tag_light_size_max)
                light_size *= scnr_light_scale

                light_data_element.energy = (100 * light_size) * 1000

                root = bpy.data.objects.new(light_name, light_data_element)
                root.color = (1, 1, 1, 0)
                asset_collection.objects.link(root)

                root.parent = level_root
                root.location = Vector(element["position"]) * 100
                ob_scale = element["scale"]
                if ob_scale > 0.0:
                    root.scale = (ob_scale, ob_scale, ob_scale)

                root.rotation_euler = get_rotation_euler(*element["rotation"])

def generate_netgame_equipment_elements(context, level_root, scnr_data, asset_cache, fix_rotations, report, random_color_gen):
    asset_collection = global_functions.get_referenced_collection("Netgame Equipment", context.scene.collection, True)
    for element_idx, element in enumerate(scnr_data["netgame equipment"]):
        variant_name = ""
        variant_element = None
        tag_path = ""
        mesh_data = None
        tag_path_no_ext = element["item/vehicle collection"]["path"]

        collection_asset = tag_interface.get_disk_asset(element["item/vehicle collection"]["path"], h2_tag_groups.get(element["item/vehicle collection"]["group name"]))
        if not collection_asset == None:
            tag_path = "%s.%s" % (element["item/vehicle collection"]["path"], h2_tag_groups.get(element["item/vehicle collection"]["group name"]))
            collection_data = collection_asset["Data"]
            block_key = "item permutations"
            field_key = "item"
            if element["item/vehicle collection"]["group name"] == "vehc":
                block_key = "vehicle permutations"
                field_key = "vehicle"

            if len(collection_data[block_key]) > 0:
                collection_permutation_element = collection_data[block_key][0]
                equipment_asset = tag_interface.get_disk_asset(collection_permutation_element[field_key]["path"], h2_tag_groups.get(collection_permutation_element[field_key]["group name"]))
                variant_name = collection_permutation_element["variant name"]
                if not equipment_asset == None:
                    model_asset = tag_interface.get_disk_asset(equipment_asset["Data"]["model"]["path"], h2_tag_groups.get(equipment_asset["Data"]["model"]["group name"]))
                    if not model_asset == None:
                        if global_functions.string_empty_check(variant_name):
                            variant_name = "default"

                        model_data = model_asset["Data"]
                        for tag_element in model_data["variants"]:
                            if tag_element["name"] == variant_name:
                                variant_element = tag_element

                        render_tag_ref = asset_cache[model_data["render model"]["group name"]][model_data["render model"]["path"]]
                        render_model_asset = tag_interface.get_disk_asset(model_data["render model"]["path"], h2_tag_groups.get(model_data["render model"]["group name"]))
                        mesh_data = render_tag_ref["blender_assets"].get("blender_asset")
                        if variant_element:
                            mesh_data = render_tag_ref["blender_assets"].get(variant_element["name"])

                        if render_model_asset is not None and mesh_data is None:
                            get_geometry_layout(model_asset["Data"]["render model"], asset_cache, None, report, True, variant_element)
                            mesh_data = render_tag_ref["blender_assets"].get("blender_asset")
                            if variant_element:
                                mesh_data = render_tag_ref["blender_assets"].get(variant_element["name"])

        tag_name = "NONE"
        if not global_functions.string_empty_check(tag_path_no_ext):
            tag_name = os.path.basename(tag_path_no_ext)

        name = "%s_%s" % (tag_name, element_idx)
        if not mesh_data == None:
            root = bpy.data.objects.new(name, mesh_data)
            root.color = (1, 1, 1, 0)
            asset_collection.objects.link(root)

        else:
            root = bpy.data.objects.new(name, None)
            root.color = (1, 1, 1, 0)
            root.empty_display_type = 'ARROWS'
            asset_collection.objects.link(root)

        get_data_type(root, asset_collection, element, scnr_data, tag_path)

        root.parent = level_root
        root.location = Vector(element["position"]) * 100
        root.rotation_euler = get_rotation_euler(*element["orientation"])

def generate_empties(context, level_root, collection_name, scnr_data, parent_collection):
    asset_collection = global_functions.get_referenced_collection(collection_name, parent_collection, True)

    tag_block = None
    if collection_name == "Player Starting Locations":
        tag_block = scnr_data["player starting locations"]
    elif collection_name == "Netgame Flags":
        tag_block = scnr_data["netgame flags"]

    for element_idx, element in enumerate(tag_block):
        ob = bpy.data.objects.new("%s_%s" % (collection_name, element_idx), None)
        ob.color = (1, 1, 1, 0)

        ob.empty_display_type = 'ARROWS'
        ob.parent = level_root
        ob.location = Vector(element["position"]) * 100

        get_data_type(ob, asset_collection, element, scnr_data, collection_name)

        asset_collection.objects.link(ob)

def generate_camera_flags(context, level_root, scnr_data):
    collection_name = "Cutscene Flags"
    asset_collection = global_functions.get_referenced_collection(collection_name, context.scene.collection, True)
    for element_idx, element in enumerate(scnr_data["cutscene flags"]):
        ob = bpy.data.objects.new(element["name"], None)
        ob.color = (1, 1, 1, 0)

        ob.empty_display_type = 'ARROWS'
        ob.parent = level_root
        ob.location = Vector(element["position"]) * 100

        ob.rotation_euler = get_rotation_euler(*element["facing"])

        get_data_type(ob, asset_collection, element, scnr_data)

        asset_collection.objects.link(ob)

def generate_camera_points(context, level_root, scnr_data):
    collection_name = "Cutscene Cameras"

    asset_collection = global_functions.get_referenced_collection(collection_name, context.scene.collection, True)
    for element_idx, element in enumerate(scnr_data["cutscene camera points"]):
        camera_data = bpy.data.cameras.new(name='Camera')
        ob = bpy.data.objects.new(element["name"], camera_data)
        ob.color = (1, 1, 1, 0)

        ob.parent = level_root
        ob.location = Vector(element["position"]) * 100

        ob.rotation_euler = get_rotation_euler(*element["orientation"])
        ob.rotation_euler.rotate_axis("X", radians(90.0))
        ob.rotation_euler.rotate_axis("Y", radians(-90.0))

        get_data_type(ob, asset_collection, element, scnr_data)

        asset_collection.objects.link(ob)

def generate_trigger_volumes(context, level_root, scnr_data):
    collection_name = "Trigger Volumes"

    asset_collection = global_functions.get_referenced_collection(collection_name, context.scene.collection, True)
    for element in scnr_data["trigger volumes"]:
        mesh = bpy.data.meshes.new("part_%s" % element["name"])
        ob = bpy.data.objects.new(element["name"], mesh)
        ob.color = (1, 1, 1, 0)

        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=2.0)
        bm.transform(Matrix.Translation((1, 1, 1)))
        bm.to_mesh(mesh)
        bm.free()

        ob.parent = level_root
        forward_vec = Vector(element["forward"])
        up_vec = Vector(element["up"])
        right_vec = np.cross(up_vec, forward_vec)
        matrix_rotation = Matrix((forward_vec, right_vec, up_vec))

        ob.matrix_world = matrix_rotation.to_4x4()
        ob.location = Vector(element["position"]) * 100
        ob.dimensions = Vector(element["extents"]) * 100

        asset_collection.objects.link(ob)

def generate_decals(context, level_root, scnr_data):
    # This doesn't work. Currently decals have improper rotations
    # I assume the actual rotation comes from the surface normal while the rotation here is just using or the Z axis on the normal or something. - Gen
    collection_name = "Decals"
    asset_collection = global_functions.get_referenced_collection(collection_name, context.scene.collection, True)
    for element_idx, element in enumerate(scnr_data["decals"]):  
        tag_name = "decal"
        tag_path = ""
        if element["decal type"] >= 0 and len(scnr_data["decal palette"]) > element["decal type"]:
            tag_ref = scnr_data["decal palette"][element["decal type"]]["reference"]
            tag_name = os.path.basename(tag_ref["path"])
            tag_path = "%s.%s" % (tag_ref["path"], h2_tag_groups.get(tag_ref["group name"]))

        mesh = bpy.data.meshes.new("part_%s" % element_idx)
        ob = bpy.data.objects.new("%s_%s" % (tag_name, element_idx), mesh)
        ob.color = (1, 1, 1, 0)
        asset_collection.objects.link(ob)

        bm = bmesh.new()
        vertex1 = bm.verts.new( (0, -1.0, 1.0) )
        vertex2 = bm.verts.new( (0, -1.0, -1.0) )
        vertex3 = bm.verts.new( (0, 1.0, 1.0) )
        vertex4 = bm.verts.new( (0, 1.0, -1.0) )

        bm.verts.index_update()
        bm.faces.new( (vertex2, vertex4, vertex3, vertex1) )
        bm.to_mesh(mesh)
        bm.free()

        ob.parent = level_root
        ob.location = Vector(element["position"]) * 100
        ob.rotation_euler = get_decal_rotation_euler(element["yaw[-127,127]"], element["pitch[-127,127]"])

        get_data_type(ob, asset_collection, element, scnr_data, tag_path)

def generate_squad_groups(context, level_root, scnr_data):
    collection_name = "Squad Groups"

    asset_collection = global_functions.get_referenced_collection(collection_name, context.scene.collection, True)
    for squad_group_idx, squad_group in enumerate(scnr_data["squad groups"]):
        squad_coll_name = "%s_%s" % (squad_group["name"], squad_group_idx)
        squad_collection = global_functions.get_referenced_collection(squad_coll_name, asset_collection, True)

    squad_group_count = len(scnr_data["squad groups"])
    for squad_group_idx, squad_group in enumerate(scnr_data["squad groups"]):
        squad_coll_name = "%s_%s" % (squad_group["name"], squad_group_idx)
        squad_collection = global_functions.get_referenced_collection(squad_coll_name, asset_collection, True)

        parent_index = squad_group["parent"]
        if parent_index >= 0 and squad_group_count > parent_index:
            parent_name = scnr_data["squad groups"][parent_index]["name"]
            parent_squad_coll_name = "%s_%s" % (parent_name, parent_index)

            parent_collection = global_functions.get_referenced_collection(parent_squad_coll_name, context.scene.collection, True)
            parent_collection.children.link(squad_collection)
            if not parent_collection.name == "Scene Collection":
                asset_collection.tag_collection.parent = parent_collection

def generate_squads(context, level_root, scnr_data):
    collection_name = "Squads"

    asset_collection = global_functions.get_referenced_collection(collection_name, context.scene.collection, True)
    for squad_idx, squad in enumerate(scnr_data["squads"]):
        squad_coll_name = "%s_%s" % (squad["name"], squad_idx)

        squad_collection = global_functions.get_referenced_collection(squad_coll_name, asset_collection, True)
        #get_data_type(encounter_collection, asset_collection, encounter, scnr_data, block_indices=block_indices)
        for starting_location_idx, starting_location in  enumerate(squad["starting locations"]):
            sl_coll_name = "%s_s%ssl%s" % (starting_location["name"], squad_idx, starting_location_idx)

            #get_data_type(squad_collection, s_e_collection, squad, scnr_data, block_indices=block_indices)

            ob = bpy.data.objects.new(sl_coll_name, None)
            ob.color = (1, 1, 1, 0)

            ob.empty_display_type = 'ARROWS'
            ob.parent = level_root
            ob.location = Vector(starting_location["position"]) * 100

            #get_data_type(ob, asset_collection, element, scnr_data, collection_name)

            squad_collection.objects.link(ob)

def generate_zones(context, level_root, scnr_data):
    collection_name = "Zones"

    asset_collection = global_functions.get_referenced_collection(collection_name, context.scene.collection, True)
    for zone_idx, zone in enumerate(scnr_data["zones"]):
        zone_coll_name = "%s_%s" % (zone["name"], zone_idx)
        firing_position_coll_name = "firing_positions_z%s" % zone_idx
        areas_coll_name = "areas_z%s" % zone_idx

        zone_collection = global_functions.get_referenced_collection(zone_coll_name, asset_collection, True)
        firing_position_collection = global_functions.get_referenced_collection(firing_position_coll_name, zone_collection, True)
        areas_collection = global_functions.get_referenced_collection(areas_coll_name, zone_collection, True)
        #get_data_type(encounter_collection, asset_collection, encounter, scnr_data, block_indices=block_indices)
        for firing_position_idx, firing_position in  enumerate(zone["firing positions"]):
            fp_name = "firing_position_%s_z%s" % (firing_position_idx, zone_idx)

            #get_data_type(squad_collection, s_e_collection, squad, scnr_data, block_indices=block_indices)

            ob = bpy.data.objects.new(fp_name, None)
            ob.color = (1, 1, 1, 0)

            ob.empty_display_type = 'ARROWS'
            ob.parent = level_root
            ob.location = Vector(firing_position["position (local)"]) * 100

            #get_data_type(ob, asset_collection, element, scnr_data, collection_name)

            firing_position_collection.objects.link(ob)

        for area_idx, area in  enumerate(zone["areas"]):
            area_coll_name = "%s_%s_z%s" % (area["name"], area_idx, zone_idx)

            #get_data_type(squad_collection, s_e_collection, squad, scnr_data, block_indices=block_indices)
            area_collection = global_functions.get_referenced_collection(area_coll_name, areas_collection, True)

def generate_orders(context, level_root, scnr_data):
    collection_name = "Orders"

    asset_collection = global_functions.get_referenced_collection(collection_name, context.scene.collection, True)
    for order_idx, order in enumerate(scnr_data["Orders"]):
        order_coll_name = "%s_%s" % (order["name"], order_idx)
        primary_area_set_coll_name = "primary_area_sets_o%s" % order_idx
        secondary_area_set_coll_name = "secondary_area_sets_o%s" % order_idx
        secondary_set_trigger_coll_name = "secondary_set_triggers_o%s" % order_idx
        special_movement_coll_name = "special_movement_o%s" % order_idx
        order_endings_coll_name = "order_endings_o%s" % order_idx

        order_collection = global_functions.get_referenced_collection(order_coll_name, asset_collection, True)
        primary_area_set_collection = global_functions.get_referenced_collection(primary_area_set_coll_name, order_collection, True)
        secondary_area_set_collection = global_functions.get_referenced_collection(secondary_area_set_coll_name, order_collection, True)
        secondary_set_trigger_collection = global_functions.get_referenced_collection(secondary_set_trigger_coll_name, order_collection, True)
        special_movement_collection = global_functions.get_referenced_collection(special_movement_coll_name, order_collection, True)
        order_endings_collection = global_functions.get_referenced_collection(order_endings_coll_name, order_collection, True)
        #get_data_type(encounter_collection, asset_collection, encounter, scnr_data, block_indices=block_indices)
        for primary_area_set_idx, primary_area_set in  enumerate(order["Primary area set"]):
            pas_name = "primary_area_set_%s_o%s" % (primary_area_set_idx, order_idx)
            pas_collection = global_functions.get_referenced_collection(pas_name, primary_area_set_collection, True)

        for secondary_area_set_idx, secondary_area_set in  enumerate(order["Secondary area set"]):
            sas_name = "secondary_area_set_%s_o%s" % (secondary_area_set_idx, order_idx)
            sas_collection = global_functions.get_referenced_collection(sas_name, secondary_area_set_collection, True)

        for secondary_set_trigger_idx, secondary_set_trigger in  enumerate(order["Secondary set trigger"]):
            sst_name = "secondary_set_trigger_%s_o%s" % (secondary_set_trigger_idx, order_idx)
            sst_triggers_name = "triggers_sst%s_o%s" % (secondary_set_trigger_idx, order_idx)

            sst_collection = global_functions.get_referenced_collection(sst_name, secondary_set_trigger_collection, True)
            sst_triggers_collection = global_functions.get_referenced_collection(sst_triggers_name, sst_collection, True)
            for sst_trigger_idx, sst_trigger in  enumerate(secondary_set_trigger["triggers"]):
                sst_trigger_name = "trigger_%s_sst%s_o%s" % (sst_trigger_idx, secondary_set_trigger_idx, order_idx)
                sst_trigger_collection = global_functions.get_referenced_collection(sst_trigger_name, sst_triggers_collection, True)

        for special_movement_idx, special_movement in  enumerate(order["Special movement"]):
            sm_name = "special_movement_%s_o%s" % (special_movement_idx, order_idx)
            sm_collection = global_functions.get_referenced_collection(sm_name, special_movement_collection, True)

        for order_ending_idx, order_ending in  enumerate(order["Order endings"]):
            oe_name = "order_ending_%s_o%s" % (order_ending_idx, order_idx)
            oe_triggers_name = "triggers_oe%s_o%s" % (order_ending_idx, order_idx)

            oet_collection = global_functions.get_referenced_collection(oe_name, order_endings_collection, True)
            oe_triggers_collection = global_functions.get_referenced_collection(oe_triggers_name, oet_collection, True)
            for sst_trigger_idx, sst_trigger in  enumerate(order_ending["triggers"]):
                oe_trigger_name = "trigger_%s_oe%s_o%s" % (sst_trigger_idx, order_ending_idx, order_idx)
                oe_trigger_collection = global_functions.get_referenced_collection(oe_trigger_name, oe_triggers_collection, True)

def get_object_names(object_name_list, resource, field_key="names"):
    if not resource == None:
        for object_name_element in resource["Data"][field_key]:
            object_name = object_name_element["name"]
            if object_name not in object_name_list:
                object_name_list.append(object_name_element["name"])

def get_tag_references(tag_reference_list, tag_palette, field_key="name"):
    for palette_element in tag_palette:
        field_element = palette_element[field_key]
        tag_reference_tuple = (field_element.get("path"), field_element.get("group name"))
        if tag_reference_tuple not in tag_reference_list:
            tag_reference_list.append(tag_reference_tuple)

def get_editor_folder(editor_folder_list, tag_block, field_key_a="name", field_key_b="parent folder"):
    for tag_element in tag_block:
        folder_name = tag_element[field_key_a]
        parent_index = tag_element[field_key_b]
        parent_name = None
        if parent_index >= 0 and parent_index < len(tag_block):
            parent_name = tag_block[field_key_a]

        editor_name = (folder_name, parent_name)
        if editor_name not in editor_folder_list:
            editor_folder_list.append(editor_name)

def get_structure_bsps(structure_bsp_list, tag_block, field_key_a="structure bsp", field_key_b="structure lightmap"):
    for tag_element in tag_block:
        bsp_path = tag_element[field_key_a].get("path", "")
        lightmap_path = tag_element[field_key_b].get("path", "")

        structure_bsp_list.append((bsp_path, lightmap_path))

def scenario_get_resources(scnr_data, asset_cache, report):
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
    for scenario_reference in scnr_data["scenario resources"]:
        for reference_element in scenario_reference["references"]:
            reference = reference_element["reference"]
            if reference["group name"] == "ai**":
                ai_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "*ipd":
                bipeds_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "cin*":
                cinematics_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "clu*":
                cluster_data_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "/**/":
                comments_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "*rea":
                creature_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "dec*":
                decals_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "dc*s":
                decorators_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "dgr*":
                devices_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "*qip":
                equipment_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "*igh":
                lights_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "*cen":
                scenery_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "*sce":
                sound_scenery_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "sslt":
                structure_lighting_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "trg*":
                trigger_volumes_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "*ehi":
                vehicles_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "*eap":
                weapons_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
        for reference_element in scenario_reference["ai resources"]:
            reference = reference_element["reference"]
            if reference["group name"] == "ai**":
                ai_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "*ipd":
                bipeds_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "cin*":
                cinematics_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "clu*":
                cluster_data_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "/**/":
                comments_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "*rea":
                creature_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "dec*":
                decals_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "dc*s":
                decorators_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "dgr*":
                devices_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "*qip":
                equipment_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "*igh":
                lights_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "*cen":
                scenery_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "*sce":
                sound_scenery_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "sslt":
                structure_lighting_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "trg*":
                trigger_volumes_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "*ehi":
                vehicles_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))
            elif reference["group name"] == "*eap":
                weapons_resource = tag_interface.get_disk_asset(reference["path"], h2_tag_groups.get(reference["group name"]))

    object_names = set()
    style_palette_set = set()
    character_palette_set = set()
    weapon_palette_set = set()
    vehicle_palette_set = set()
    biped_palette_set = set()
    creature_palette_set = set()
    decal_palette_set = set()
    decorator_palette_set = set()
    machine_palette_set = set()
    control_palette_set = set()
    light_fixture_palette_set = set()
    equipment_palette_set = set()
    light_palette_set = set()
    scenery_palette_set = set()
    crate_palette_set = set()
    sound_scenery_palette_set = set()
    editor_folder_set = set()
    structure_bsp_set = set()
    get_structure_bsps(structure_bsp_set, scnr_data["structure bsps"])
    if False: # Original resources. Don't believe we'll be needing it since we're generating a fresh set from the combined data in the resources. - Gen
        get_object_names(object_names, scnr_data, "object names")
        get_editor_folder(editor_folder_set, scnr_data["editor folders"])
        get_tag_references(style_palette_set, scnr_data["style pallette"])
        get_tag_references(character_palette_set, scnr_data["character palette"])
        get_tag_references(weapon_palette_set, scnr_data["weapon palette"])
        get_tag_references(vehicle_palette_set, scnr_data["vehicle palette"])
        get_tag_references(biped_palette_set, scnr_data["biped palette"])
        get_tag_references(creature_palette_set, scnr_data["creature palette"])
        get_tag_references(machine_palette_set, scnr_data["machine palette"])
        get_tag_references(control_palette_set, scnr_data["control palette"])
        get_tag_references(light_fixture_palette_set, scnr_data["light fixtures palette"])
        get_tag_references(equipment_palette_set, scnr_data["equipment palette"])
        get_tag_references(light_palette_set, scnr_data["light volumes palette"])
        get_tag_references(scenery_palette_set, scnr_data["scenery palette"])
        get_tag_references(crate_palette_set, scnr_data["crate_palette"])
        get_tag_references(sound_scenery_palette_set, scnr_data["sound scenery palette"])
    if not ai_resource == None:
        ai_resource_data = ai_resource["Data"]
        get_tag_references(weapon_palette_set, ai_resource_data["weapon references"])
        get_tag_references(vehicle_palette_set, ai_resource_data["vehicle references"])
    if not bipeds_resource == None:
        bipeds_resource_data = bipeds_resource["Data"]
        get_object_names(object_names, bipeds_resource)
        get_tag_references(biped_palette_set, bipeds_resource_data["biped palette"])
        get_editor_folder(editor_folder_set, bipeds_resource_data["editor folders"])
    if not creature_resource == None:
        creature_resource_data = creature_resource["Data"]
        get_object_names(object_names, creature_resource)
        get_editor_folder(editor_folder_set, creature_resource_data["editor folders"])
    if not devices_resource == None:
        devices_resource_data = devices_resource["Data"]
        get_object_names(object_names, devices_resource)
        get_tag_references(machine_palette_set, devices_resource_data["machine palette"])
        get_tag_references(control_palette_set, devices_resource_data["control palette"])
        get_tag_references(light_fixture_palette_set, devices_resource_data["light fixture palette"])
    if not equipment_resource == None:
        equipment_resource_data = equipment_resource["Data"]
        get_object_names(object_names, equipment_resource)
        get_tag_references(equipment_palette_set, equipment_resource_data["equipment palette"])
    if not lights_resource == None:
        lights_resource_data = lights_resource["Data"]
        get_object_names(object_names, lights_resource)
        get_tag_references(light_palette_set, lights_resource_data["light palette"])
    if not scenery_resource == None:
        scenery_resource_data = scenery_resource["Data"]
        get_object_names(object_names, scenery_resource)
        get_tag_references(scenery_palette_set, scenery_resource_data["scenery palette"])
        get_tag_references(crate_palette_set, scenery_resource_data["crate palette"])
    if not sound_scenery_resource == None:
        sound_scenery_resource_data = sound_scenery_resource["Data"]
        get_object_names(object_names, sound_scenery_resource)
        get_tag_references(scenery_palette_set, sound_scenery_resource_data["sound_scenery palette"])
    if not trigger_volumes_resource == None:
        get_object_names(object_names, trigger_volumes_resource, "object names")
    if not vehicles_resource == None:
        vehicles_resource_data = vehicles_resource["Data"]
        get_object_names(object_names, vehicles_resource)
        get_tag_references(vehicle_palette_set, vehicles_resource_data["vehicle palette"])
    if not weapons_resource == None:
        weapons_resource_data = weapons_resource["Data"]
        get_object_names(object_names, weapons_resource)
        get_tag_references(weapon_palette_set, weapons_resource_data["weapon palette"])

    if not ai_resource == None:
        # TODO: FIX UP NEEDED
        ai_resource_data = ai_resource["Data"]
        scnr_data["squad groups"] = ai_resource_data["squad groups"]
        scnr_data["Orders"] = ai_resource_data["Orders"]
        scnr_data["zones"] = ai_resource_data["zones"]
        scnr_data["Triggers"] = ai_resource_data["Triggers"]
        scnr_data["mission scenes"] = ai_resource_data["mission dialogue scenes"]
        scnr_data["ai animation references"] = ai_resource_data["ai animation references"]
        scnr_data["ai script references"] = ai_resource_data["ai script references"]
        scnr_data["ai recording references"] = ai_resource_data["ai recording references"]
        scnr_data["ai conversations"] = ai_resource_data["ai conversations"]
        scnr_data["squads"] = ai_resource_data["squads"]
        scnr_data["scripting data"] = ai_resource_data["scripting data"]
        scnr_data["structure bsps"] = ai_resource_data["bsp references"]
        scnr_data["vehicles"] = ai_resource_data["vehicle datum references"]
        scnr_data["flocks"] = ai_resource_data["flocks"]
        scnr_data["trigger volumes"] = ai_resource_data["trigger volume references"]
 
    if not bipeds_resource == None:
        # TODO: FIX UP NEEDED
        bipeds_resource_data = bipeds_resource["Data"]
        scnr_data["structure bsps"] = bipeds_resource_data["structure references"]
        scnr_data["bipeds"] = bipeds_resource_data["bipeds"]
        scnr_data["editor folders"] = bipeds_resource_data["editor folders"]

        scnr_data["style pallette"] = bipeds_resource_data["style pallette"]

    if not cinematics_resource == None:
        cinematics_resource_data = cinematics_resource["Data"]
        scnr_data["cutscene flags"] = cinematics_resource_data["flags"]
        scnr_data["cutscene camera points"] = cinematics_resource_data["camera points"]
        scnr_data["recorded animations"] = cinematics_resource_data["recorded animations"]

    if not cluster_data_resource == None:
        cluster_data_resource_data = cluster_data_resource["Data"]
        scnr_data["scenario cluster data"] = cluster_data_resource_data["cluster data"]
        scnr_data["background sound palette"] = cluster_data_resource_data["background sound palette"]
        scnr_data["sound environment palette"] = cluster_data_resource_data["sound environment palette"]
        scnr_data["weather palette"] = cluster_data_resource_data["weather palette"]
        scnr_data["atmospheric fog palette"] = cluster_data_resource_data["atmospheric fog palette"]

    if not comments_resource == None:
        comments_resource_data = comments_resource["Data"]
        scnr_data["comments"] = comments_resource_data["comments"]

    if not creature_resource == None:
        # TODO: FIX UP NEEDED
        creature_resource_data = creature_resource["Data"]
        scnr_data["structure bsps"] = creature_resource_data["structure references"]
        scnr_data["creature palette"] = creature_resource_data["creature palette"]
        scnr_data["creatures"] = creature_resource_data["creatures"]
        scnr_data["editor folders"] = creature_resource_data["editor folders"]

    if not decals_resource == None:
        decals_resource_data = decals_resource["Data"]
        scnr_data["decals"] = decals_resource_data["decals"]

    if not decorators_resource == None:
        decorators_resource_data = decorators_resource["Data"]
        scnr_data["decorators"] = decorators_resource_data["decorator"]
        scnr_data["decorator palette"] = decorators_resource_data["decorator palette"]

    if not devices_resource == None:
        # TODO: FIX UP NEEDED
        devices_resource_data = devices_resource["Data"]
        scnr_data["structure bsps"] = devices_resource_data["structure references"]
        scnr_data["device groups"] = devices_resource_data["device groups"]
        scnr_data["machines"] = devices_resource_data["machines"]
        scnr_data["controls"] = devices_resource_data["controls"]
        scnr_data["light fixtures"] = devices_resource_data["light fixtures"]
        scnr_data["editor folders"] = devices_resource_data["editor folders"]

    if not equipment_resource == None:
        # TODO: FIX UP NEEDED
        equipment_resource_data = equipment_resource["Data"]
        scnr_data["object names"] = equipment_resource_data["names"]
        scnr_data["structure bsps"] = equipment_resource_data["structure references"]
        scnr_data["equipment"] = equipment_resource_data["equipments"]
        scnr_data["editor folders"] = equipment_resource_data["editor folders"]

    if not lights_resource == None:
        # TODO: FIX UP NEEDED
        lights_resource_data = lights_resource["Data"]
        scnr_data["structure bsps"] = lights_resource_data["structure references"]
        scnr_data["light volumes"] = lights_resource_data["lights"]
        scnr_data["editor folders"] = lights_resource_data["editor folders"]

    if not scenery_resource == None:
        # TODO: FIX UP NEEDED
        scenery_resource_data = scenery_resource["Data"]
        scnr_data["structure bsps"] = scenery_resource_data["structure references"]
        scnr_data["scenery palette"] = scenery_resource_data["scenery palette"]
        scnr_data["scenery"] = scenery_resource_data["scenerys"]
        scnr_data["crate_palette"] = scenery_resource_data["crate palette"]
        scnr_data["crates"] = scenery_resource_data["crates"]
        scnr_data["editor folders"] = scenery_resource_data["editor folders"]

    if not sound_scenery_resource == None:
        # TODO: FIX UP NEEDED
        sound_scenery_resource_data = sound_scenery_resource["Data"]
        scnr_data["structure bsps"] = sound_scenery_resource_data["structure references"]
        scnr_data["sound scenery palette"] = sound_scenery_resource_data["sound_scenery palette"]
        scnr_data["sound scenery"] = sound_scenery_resource_data["sound_scenerys"]
        scnr_data["editor folders"] = sound_scenery_resource_data["editor folders"]

    if not structure_lighting_resource == None:
        structure_lighting_resource_data = structure_lighting_resource["Data"]
        scnr_data["structure bsp lighting"] = structure_lighting_resource_data["structure lighting"]

    if not trigger_volumes_resource == None:
        # TODO: FIX UP NEEDED
        trigger_volumes_resource_data = trigger_volumes_resource["Data"]
        scnr_data["trigger volumes"] = trigger_volumes_resource_data["trigger volumes"]

    if not vehicles_resource == None:
        # TODO: FIX UP NEEDED
        vehicles_resource_data = vehicles_resource["Data"]
        scnr_data["structure bsps"] = vehicles_resource_data["structure references"]
        scnr_data["vehicles"] = vehicles_resource_data["vehicles"]
        scnr_data["editor folders"] = vehicles_resource_data["editor folders"]

    if not weapons_resource == None:
        # TODO: FIX UP NEEDED
        weapons_resource_data = weapons_resource["Data"]
        scnr_data["structure bsps"] = weapons_resource_data["structure references"]
        scnr_data["weapons"] = weapons_resource_data["weapons"]
        scnr_data["editor folders"] = weapons_resource_data["editor folders"]

def generate_scenario_scene(context, tag_ref, asset_cache, game_title, fix_rotations, empty_markers, report):
    scnr_asset = tag_interface.get_disk_asset(tag_ref["path"], h2_tag_groups.get(tag_ref["group name"]))
    scnr_data = scnr_asset["Data"]

    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors
    levels_collection = global_functions.get_referenced_collection("BSPs", context.scene.collection, False)
    for bsp_idx, bsp_element in enumerate(scnr_data["structure bsps"]):
        bsp_tag_ref = bsp_element["structure bsp"]
        lightmap_tag_ref = bsp_element["structure lightmap"]
        sbsp_asset = tag_interface.get_disk_asset(bsp_tag_ref["path"], h2_tag_groups.get(bsp_tag_ref["group name"]))
        ltmp_asset = tag_interface.get_disk_asset(lightmap_tag_ref["path"], h2_tag_groups.get(lightmap_tag_ref["group name"]))
        if not sbsp_asset == None:
            bsp_name = os.path.basename(bsp_tag_ref["path"])
            c_bsp_name = "%s_%s" % (bsp_name, bsp_idx)
            c_cluster_name = "%s_clusters" % bsp_name
            level_collection = global_functions.get_referenced_collection(c_bsp_name, levels_collection, False)
            clusters_collection = global_functions.get_referenced_collection(c_cluster_name, level_collection, True, True)

            build_scene_level.build_scene(context, bsp_tag_ref, asset_cache, game_title, fix_rotations, empty_markers, report, level_collection, clusters_collection)

            if not ltmp_asset == None:
                lightmap_name = "%s_lightmaps" % bsp_name
                lightmap_collection = global_functions.get_referenced_collection(lightmap_name, level_collection, False)

                build_scene_lightmap.build_scene(context, lightmap_tag_ref, asset_cache, game_title, fix_rotations, empty_markers, report, level_collection, lightmap_collection, bsp_tag_ref)

    level_root = bpy.data.objects.get("frame_root")
    if level_root == None:
        level_mesh = bpy.data.meshes.new("frame_root")
        level_root = bpy.data.objects.new("frame_root", level_mesh)
        level_root.color = (1, 1, 1, 0)
        context.collection.objects.link(level_root)

    #scenario_get_resources(scnr_data, asset_cache, report)

    for object_name in scnr_data["object names"]:
        if not global_functions.string_empty_check(object_name["name"]):
            context.scene.object_name_add(object_name["name"])

    tag_references = set()
    if not global_functions.string_empty_check(scnr_data["DON'T USE"]["path"]):
        tag_references.add((scnr_data["DON'T USE"]["path"], scnr_data["DON'T USE"]["group name"]))
    for sky_element in scnr_data["skies"]:
        if not global_functions.string_empty_check(sky_element["sky"]["path"]):
            tag_references.add((sky_element["sky"]["path"], sky_element["sky"]["group name"]))
    for scenery_element in scnr_data["scenery palette"]:
        if not global_functions.string_empty_check(scenery_element["name"]["path"]):
            tag_references.add((scenery_element["name"]["path"], scenery_element["name"]["group name"]))
    for biped_element in scnr_data["biped palette"]:
        if not global_functions.string_empty_check(biped_element["name"]["path"]):
            tag_references.add((biped_element["name"]["path"], biped_element["name"]["group name"]))
    for vehicle_element in scnr_data["vehicle palette"]:
        if not global_functions.string_empty_check(vehicle_element["name"]["path"]):
            tag_references.add((vehicle_element["name"]["path"], vehicle_element["name"]["group name"]))
    for equipment_element in scnr_data["equipment palette"]:
        if not global_functions.string_empty_check(equipment_element["name"]["path"]):
            tag_references.add((equipment_element["name"]["path"], equipment_element["name"]["group name"]))
    for weapon_element in scnr_data["weapon palette"]:
        if not global_functions.string_empty_check(weapon_element["name"]["path"]):
            tag_references.add((weapon_element["name"]["path"], weapon_element["name"]["group name"]))
    for machine_element in scnr_data["machine palette"]:
        if not global_functions.string_empty_check(machine_element["name"]["path"]):
            tag_references.add((machine_element["name"]["path"], machine_element["name"]["group name"]))
    for control_element in scnr_data["control palette"]:
        if not global_functions.string_empty_check(control_element["name"]["path"]):
            tag_references.add((control_element["name"]["path"], control_element["name"]["group name"]))
    for light_element in scnr_data["light fixtures palette"]:
        if not global_functions.string_empty_check(light_element["name"]["path"]):
            tag_references.add((light_element["name"]["path"], light_element["name"]["group name"]))
    for sound_element in scnr_data["sound scenery palette"]:
        if not global_functions.string_empty_check(sound_element["name"]["path"]):
            tag_references.add((sound_element["name"]["path"], sound_element["name"]["group name"]))
    for light_volume_element in scnr_data["light volumes palette"]:
        if not global_functions.string_empty_check(light_volume_element["name"]["path"]):
            tag_references.add((light_volume_element["name"]["path"], light_volume_element["name"]["group name"]))
    for netgame_equipment_element in scnr_data["netgame equipment"]:
        if not global_functions.string_empty_check(netgame_equipment_element["item/vehicle collection"]["path"]):
            tag_references.add((netgame_equipment_element["item/vehicle collection"]["path"], netgame_equipment_element["item/vehicle collection"]["group name"]))
    for decal_palette_element in scnr_data["decal palette"]:
        if not global_functions.string_empty_check(decal_palette_element["reference"]["path"]):
            tag_references.add((decal_palette_element["reference"]["path"], decal_palette_element["reference"]["group name"]))
    for style_element in scnr_data["style pallette"]:
        if not global_functions.string_empty_check(style_element["reference"]["path"]):
            tag_references.add((style_element["reference"]["path"], style_element["reference"]["group name"]))
    for character_element in scnr_data["character palette"]:
        if not global_functions.string_empty_check(character_element["reference"]["path"]):
            tag_references.add((character_element["reference"]["path"], character_element["reference"]["group name"]))
    if not global_functions.string_empty_check(scnr_data["custom object names"]["path"]):
        tag_references.add((scnr_data["custom object names"]["path"], scnr_data["custom object names"]["group name"]))
    if not global_functions.string_empty_check(scnr_data["chapter title text"]["path"]):
        tag_references.add((scnr_data["chapter title text"]["path"], scnr_data["chapter title text"]["group name"]))
    if not global_functions.string_empty_check(scnr_data["hud messages"]["path"]):
        tag_references.add((scnr_data["hud messages"]["path"], scnr_data["hud messages"]["group name"]))
    if not global_functions.string_empty_check(scnr_data["sound effect collection"]["path"]):
        tag_references.add((scnr_data["sound effect collection"]["path"], scnr_data["sound effect collection"]["group name"]))
    if not global_functions.string_empty_check(scnr_data["global lighting"]["path"]):
        tag_references.add((scnr_data["global lighting"]["path"], scnr_data["global lighting"]["group name"]))
    if not global_functions.string_empty_check(scnr_data["subtitles"]["path"]):
        tag_references.add((scnr_data["subtitles"]["path"], scnr_data["subtitles"]["group name"]))
    for crate_element in scnr_data["crate palette"]:
        if not global_functions.string_empty_check(crate_element["name"]["path"]):
            tag_references.add((crate_element["name"]["path"], crate_element["name"]["group name"]))
    for creature_element in scnr_data["creature palette"]:
        if not global_functions.string_empty_check(creature_element["name"]["path"]):
            tag_references.add((creature_element["name"]["path"], creature_element["name"]["group name"]))
    if not global_functions.string_empty_check(scnr_data["game engine strings"]["path"]):
        tag_references.add((scnr_data["game engine strings"]["path"], scnr_data["game engine strings"]["group name"]))
    if not global_functions.string_empty_check(scnr_data["objectives"]["path"]):
        tag_references.add((scnr_data["objectives"]["path"], scnr_data["objectives"]["group name"]))

    for tag_reference in tag_references:
        tag_path, tag_group = tag_reference
        context.scene.tag_add(tag_path=tag_path, tag_group=tag_group)

    set_scenario_data(context, scnr_data)
    if len(scnr_data["skies"]) > 0:
        generate_skies(context, level_root, scnr_data, asset_cache)
    if len(scnr_data["comments"]) > 0:
        generate_comments(context, level_root, scnr_data, asset_cache)
    if len(scnr_data["scenery"]) > 0:
        generate_object_elements(context, level_root, "Scenery", scnr_data, asset_cache, fix_rotations, report, random_color_gen)
    if len(scnr_data["bipeds"]) > 0:
        generate_object_elements(context, level_root, "Bipeds", scnr_data, asset_cache, fix_rotations, report, random_color_gen)
    if len(scnr_data["vehicles"]) > 0:
        generate_object_elements(context, level_root, "Vehicles", scnr_data, asset_cache, fix_rotations, report, random_color_gen)
    if len(scnr_data["equipment"]) > 0:
        generate_object_elements(context, level_root, "Equipment", scnr_data, asset_cache, fix_rotations, report, random_color_gen)
    if len(scnr_data["weapons"]) > 0:
        generate_object_elements(context, level_root, "Weapons", scnr_data, asset_cache, fix_rotations, report, random_color_gen)
    if len(scnr_data["machines"]) > 0:
        generate_object_elements(context, level_root, "Machines", scnr_data, asset_cache, fix_rotations, report, random_color_gen)
    if len(scnr_data["controls"]) > 0:
        generate_object_elements(context, level_root, "Controls", scnr_data, asset_cache, fix_rotations, report, random_color_gen)
    if len(scnr_data["light fixtures"]) > 0:
        generate_object_elements(context, level_root, "Light Fixtures", scnr_data, asset_cache, fix_rotations, report, random_color_gen)
    if len(scnr_data["sound scenery"]) > 0:
        generate_object_elements(context, level_root, "Sound Scenery", scnr_data, asset_cache, fix_rotations, report, random_color_gen)
    if len(scnr_data["light volumes"]) > 0:
        generate_light_volumes_elements(context, level_root, "Lights", scnr_data, asset_cache, fix_rotations, report, random_color_gen)
    if len(scnr_data["player starting locations"]) > 0:
        generate_empties(context, level_root, "Player Starting Locations", scnr_data, context.scene.collection)
    if len(scnr_data["trigger volumes"]) > 0:
        generate_trigger_volumes(context, level_root, scnr_data)
    if len(scnr_data["netgame flags"]) > 0:
        generate_empties(context, level_root, "Netgame Flags", scnr_data, context.scene.collection)
    if len(scnr_data["netgame equipment"]) > 0:
        generate_netgame_equipment_elements(context, level_root, scnr_data, asset_cache, fix_rotations, report, random_color_gen)
    if len(scnr_data["decals"]) > 0:
        generate_decals(context, level_root, scnr_data)
    if len(scnr_data["squad groups"]) > 0:
        generate_squad_groups(context, level_root, scnr_data)
    if len(scnr_data["squads"]) > 0:
        generate_squads(context, level_root, scnr_data)
    if len(scnr_data["zones"]) > 0:
        generate_zones(context, level_root, scnr_data)
    #if len(scnr_data["user-placed hints"]) > 0:
    #if len(scnr_data["point sets"]) > 0:
    if len(scnr_data["cutscene flags"]) > 0:
        generate_camera_flags(context, level_root, scnr_data)
    if len(scnr_data["cutscene camera points"]) > 0:
        generate_camera_points(context, level_root, scnr_data)
    if len(scnr_data["Orders"]) > 0:
        generate_orders(context, level_root, scnr_data)
    #if len(scnr_data["Triggers"]) > 0:
    #if len(scnr_data["spawn data"]) > 0:
    if len(scnr_data["crates"]) > 0:
        generate_object_elements(context, level_root, "Crates", scnr_data, asset_cache, fix_rotations, report, random_color_gen)
    if len(scnr_data["creatures"]) > 0:
        generate_object_elements(context, level_root, "Creatures", scnr_data, asset_cache, fix_rotations, report, random_color_gen)

