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
import base64
import numpy as np

from enum import Flag, Enum, auto
from math import radians, cos, sin
from mathutils import Euler, Matrix, Vector
from . import build_bsp as build_scene_level
from ...global_functions import global_functions
from ..h1.file_model.build_mesh import get_geometry_layout
from ...file_tag.tag_interface.tag_common import h1_tag_groups
from ...file_tag.tag_interface import tag_interface
from ...global_functions.shader_generation.shader_helper import convert_to_blender_color

class ScenarioFlags(Flag):
    cortana_hack = auto()
    use_demo_ui = auto()
    color_correction_ntsc_srgb = auto()
    do_not_apply_bungie_campaign_patches = auto()

class ObjectFlags(Flag):
    automatically = auto()
    on_easy = auto()
    on_normal = auto()
    on_hard = auto()
    use_player_appearance = auto()

class UnitFlags(Flag):
    dead = auto()

class VehicleFlags(Flag):
    slayer_default = auto()
    ctf_default = auto()
    king_default = auto()
    oddball_default = auto()
    unused0 = auto()
    unused1 = auto()
    unused2 = auto()
    unused3 = auto()
    slayer_allowed = auto()
    ctf_allowed = auto()
    king_allowed = auto()
    oddball_allowed = auto()
    unused4 = auto()
    unused5 = auto()
    unused6 = auto()
    unused7 = auto()

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

class ControlFlags(Flag):
    usable_from_both_sides = auto()

class NetGameEquipment(Flag):
    levitate = auto()

class EncounterFlags(Flag):
    not_initially_created = auto()
    respawn_enabled = auto()
    initially_blind = auto()
    initially_deaf = auto()
    initially_braindead = auto()
    _3d_firing_positions = auto()
    manual_bsp_index_specified = auto()

class SquadFlags(Flag):
    unused = auto()
    never_search = auto()
    start_timer_immediately = auto()
    no_timer_delay_forever = auto()
    magic_sight_after_timer = auto()
    automatic_migration = auto()

class StartingLocationFlags(Flag):
    required = auto()

class PlatoonFlags(Flag):
    flee_when_maneuvering = auto()
    say_advancing_when_maneuver = auto()
    start_in_defending_state = auto()

class GroupFlags(Flag):
    a = auto()
    b = auto()
    c = auto()
    d = auto()
    e = auto()
    f = auto()
    g = auto()
    h = auto()
    i = auto()
    j = auto()
    k = auto()
    l = auto()
    m = auto()
    n = auto()
    o = auto()
    p = auto()
    q = auto()
    r = auto()
    s = auto()
    t = auto()
    u = auto()
    v = auto()
    w = auto()
    x = auto()
    y = auto()
    z = auto()

class CommandListFlags(Flag):
    allow_initiative = auto()
    allow_targeting = auto()
    disable_looking = auto()
    disable_communication = auto()
    disable_falling_damage = auto()
    manual_bsp_index = auto()

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

def get_tag_display(tag_ref):
    tag_display = ""
    if not global_functions.string_empty_check(tag_ref["path"]):
        tag_display = "%s.%s" % (tag_ref["path"], h1_tag_groups.get(tag_ref["group name"]))

    return tag_display

def get_group_string(behavior_flags):
    group_string = ""
    group_flags = GroupFlags(behavior_flags)
    for group_flag in GroupFlags:
        if group_flag in group_flags:
            group_string += group_flag.name.upper()

    return group_string

def get_block_collection(block_index, block_indices, tag_block, key, has_name=True):
    unique_name = None
    if block_index >= 0 and len(tag_block) > block_index:
        if has_name:
            platoon_name = tag_block[block_index]["name"]
            unique_name = key % (platoon_name, block_indices[0], block_index)
        else:
            unique_name = key % (block_indices[0], block_index)

    return unique_name

def get_point(block_indices, point_index, tag_block, level_root):
    points_coll_name = "Points_cl%s" % block_indices[0]
    point_unique_name = "point_cl%sp%s" % (block_indices[0], point_index)
    ob = None
    if point_index >= 0 and len(tag_block) > point_index:
        point_collection = bpy.data.collections.get(points_coll_name)
        ob = bpy.data.objects.get(point_unique_name)
        if ob == None:
            ob = bpy.data.objects.new(point_unique_name, None)
            ob.color = (1, 1, 1, 0)

            ob.empty_display_type = 'ARROWS'
            ob.parent = level_root
            ob.location = Vector(tag_block[point_index]["position"]) * 100

            point_collection.objects.link(ob)

    return ob

def set_scenario_data(context, scnr_data):
    context.scene.tag_scenario.dont_use = get_tag_display(scnr_data["dont use"])
    context.scene.tag_scenario.wont_use = get_tag_display(scnr_data["wont use"])
    context.scene.tag_scenario.cant_use = get_tag_display(scnr_data["cant use"])
    context.scene.tag_scenario.scenario_type_enum = str(scnr_data["type"]["value"])

    scenario_flags = ScenarioFlags(scnr_data["flags"])
    context.scene.tag_scenario.cortana_hack = ScenarioFlags.cortana_hack in scenario_flags
    context.scene.tag_scenario.use_demo_ui = ScenarioFlags.use_demo_ui in scenario_flags
    context.scene.tag_scenario.color_correction = ScenarioFlags.color_correction_ntsc_srgb in scenario_flags
    context.scene.tag_scenario.disable_tag_patches = ScenarioFlags.do_not_apply_bungie_campaign_patches in scenario_flags

    context.scene.tag_scenario.local_north = radians(scnr_data["local north"])
    context.scene.tag_scenario.custom_object_names = get_tag_display(scnr_data["custom object names"])
    context.scene.tag_scenario.ingame_help_text = get_tag_display(scnr_data["ingame help text"])
    context.scene.tag_scenario.hud_messages = get_tag_display(scnr_data["hud messages"])

def set_object_data(ob, tag_path, element, object_name_tag_block):
    element_flags = ObjectFlags(element["not placed"])

    object_name = ""
    if element["name"] >= 0:
        object_name = object_name_tag_block[element["name"]]["name"]
        
    ob.tag_object.tag_path = tag_path
    ob.tag_object.object_name = object_name
    ob.tag_object.automatically = ObjectFlags.automatically in element_flags
    ob.tag_object.on_easy = ObjectFlags.on_easy in element_flags
    ob.tag_object.on_normal = ObjectFlags.on_normal in element_flags
    ob.tag_object.on_hard = ObjectFlags.on_hard in element_flags
    ob.tag_object.use_player_appearance = ObjectFlags.use_player_appearance in element_flags
    ob.tag_object.desired_permutation = element["desired permutation"]
    ob.tag_object.appearance_player_index = element["appearance player index"]

def set_unit_data(ob, element):
    element_flags = UnitFlags(element["flags"])

    ob.tag_unit.unit_vitality = element["body vitality"]
    ob.tag_unit.unit_dead = UnitFlags.dead in element_flags

def set_vehicle_data(ob, element):
    element_flags = VehicleFlags(element["multiplayer spawn flags"])

    ob.tag_unit.multiplayer_team_index = element["multiplayer team index"]
    ob.tag_unit.slayer_default = VehicleFlags.slayer_default in element_flags
    ob.tag_unit.ctf_default = VehicleFlags.ctf_default in element_flags
    ob.tag_unit.king_default = VehicleFlags.king_default in element_flags
    ob.tag_unit.oddball_default = VehicleFlags.oddball_default in element_flags
    ob.tag_unit.unused_0 = VehicleFlags.unused0 in element_flags
    ob.tag_unit.unused_1 = VehicleFlags.unused1 in element_flags
    ob.tag_unit.unused_2 = VehicleFlags.unused2 in element_flags
    ob.tag_unit.unused_3 = VehicleFlags.unused3 in element_flags
    ob.tag_unit.slayer_allowed = VehicleFlags.slayer_allowed in element_flags
    ob.tag_unit.ctf_allowed = VehicleFlags.ctf_allowed in element_flags
    ob.tag_unit.king_allowed = VehicleFlags.king_allowed in element_flags
    ob.tag_unit.oddball_allowed = VehicleFlags.oddball_allowed in element_flags
    ob.tag_unit.unused_4 = VehicleFlags.unused4 in element_flags
    ob.tag_unit.unused_5 = VehicleFlags.unused5 in element_flags
    ob.tag_unit.unused_6 = VehicleFlags.unused6 in element_flags
    ob.tag_unit.unused_7 = VehicleFlags.unused7 in element_flags

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

def set_control_data(ob, element_flags):
    control_flags = ControlFlags(element_flags)

    ob.tag_control.usable_from_both_sides = ControlFlags.usable_from_both_sides in control_flags

def get_data_type(ob, ob_parent, element, scnr_data, tag_path="", block_indices=(), level_root=None):
        ob_parent_name = ob_parent.name.lower().replace(" ", "_")

        if ob_parent_name.startswith("bsps"):
            ob.tag_mesh.lightmap_index = -1

        elif ob_parent_name.startswith("scenery"):
            set_object_data(ob, tag_path, element, scnr_data["object names"])

        elif ob_parent_name.startswith("biped"):
            ob.lock_rotation[0] = True
            ob.lock_rotation[1] = True

            set_object_data(ob, tag_path, element, scnr_data["object names"])
            set_unit_data(ob, element)

        elif ob_parent_name.startswith("vehicle"):
            set_object_data(ob, tag_path, element, scnr_data["object names"])
            set_unit_data(ob, element)
            set_vehicle_data(ob, element)

        elif ob_parent_name.startswith("equipment"):
            set_object_data(ob, tag_path, element, scnr_data["object names"])
            set_item_data(ob, element["misc flags"])

        elif ob_parent_name.startswith("weapons"):
            set_object_data(ob, tag_path, element, scnr_data["object names"])
            ob.tag_weapon.rounds_left = element["rounds reserved"]
            ob.tag_weapon.rounds_loaded = element["rounds loaded"]
            set_item_data(ob, element["flags"])

        elif ob_parent_name.startswith("machines"):
            set_object_data(ob, tag_path, element, scnr_data["object names"])
            ob.tag_device.power_group = element["power group"]
            ob.tag_device.position_group = element["position group"]
            set_device_data(ob, element["device flags"])
            set_machine_data(ob, element["machine flags"])

        elif ob_parent_name.startswith("controls"):
            set_object_data(ob, tag_path, element, scnr_data["object names"])
            ob.tag_device.power_group = element["power group"]
            ob.tag_device.position_group = element["position group"]
            set_device_data(ob, element["device flags"])
            set_control_data(ob, element["control flags"])
            ob.tag_control.control_value = element["no name"]

        elif ob_parent_name.startswith("light_fixtures"):
            set_object_data(ob, tag_path, element, scnr_data["object names"])
            ob.tag_device.power_group = element["power group"]
            ob.tag_device.position_group = element["position group"]
            set_device_data(ob, element["device flags"])
            ob.tag_light_fixture.color = convert_to_blender_color(element["color"], False)
            ob.tag_light_fixture.intensity = element["intensity"]
            ob.tag_light_fixture.falloff_angle = element["falloff angle"]
            ob.tag_light_fixture.cutoff_angle = element["cutoff angle"]

        elif ob_parent_name.startswith("sound_scenery"):
            set_object_data(ob, tag_path, element, scnr_data["object names"])

        elif ob_parent_name.startswith("player_starting_locations"):
            ob.tag_player_starting_location.team_index = element["team index"]
            ob.tag_player_starting_location.bsp_index = element["bsp index"]
            ob.tag_player_starting_location.type_0 = element["type 0"]["value"]
            ob.tag_player_starting_location.type_1 = element["type 1"]["value"]
            ob.tag_player_starting_location.type_2 = element["type 2"]["value"]
            ob.tag_player_starting_location.type_3 = element["type 3"]["value"]

        elif ob_parent_name.startswith("netgame_flags"):
            ob.tag_netgame_flag.netgame_type = element["type"]["value"]
            ob.tag_netgame_flag.usage_id = element["usage id"]
            ob.tag_netgame_flag.weapon_group = tag_path

        elif ob_parent_name.startswith("netgame_equipment"):
            element_flags = NetGameEquipment(element["flags"])

            ob.tag_netgame_equipment.levitate = NetGameEquipment.levitate in element_flags
            ob.tag_netgame_equipment.type_0 = element["type 0"]["value"]
            ob.tag_netgame_equipment.type_1 = element["type 1"]["value"]
            ob.tag_netgame_equipment.type_2 = element["type 2"]["value"]
            ob.tag_netgame_equipment.type_3 = element["type 3"]["value"]
            ob.tag_netgame_equipment.team_index = element["team index"]
            ob.tag_netgame_equipment.spawn_time = element["spawn time"]
            ob.tag_netgame_equipment.item_collection = tag_path

        elif ob_parent_name.startswith("decal"):
            ob.tag_decal.decal_type = tag_path
            ob.tag_decal.yaw = element["yaw"]
            ob.tag_decal.pitch = element["pitch"]

        elif ob_parent_name.startswith("encounter"):
            encounter_flags = EncounterFlags(element["flags"])

            ob.tag_collection.parent = ob_parent

            ob.tag_encounter.name = element["name"]
            ob.tag_encounter.not_initially_created = EncounterFlags.not_initially_created in encounter_flags
            ob.tag_encounter.respawn_enabled = EncounterFlags.respawn_enabled in encounter_flags
            ob.tag_encounter.initially_blind = EncounterFlags.initially_blind in encounter_flags
            ob.tag_encounter.initially_deaf = EncounterFlags.initially_deaf in encounter_flags
            ob.tag_encounter.initially_braindead = EncounterFlags.initially_braindead in encounter_flags
            ob.tag_encounter.firing_positions = EncounterFlags._3d_firing_positions in encounter_flags
            ob.tag_encounter.manual_bsp_index_specified = EncounterFlags.manual_bsp_index_specified in encounter_flags
            ob.tag_encounter.team_index = str(element["team index"]["value"])
            ob.tag_encounter.search_behavior = str(element["search behavior"]["value"])
            ob.tag_encounter.manual_bsp_index = element["manual bsp index"]
            rd_min, rd_max = element["respawn delay"].values()
            ob.tag_encounter.respawn_delay_min = rd_min
            ob.tag_encounter.respawn_delay_max = rd_max

        elif ob_parent_name.startswith("squads"):
            tag_path = ""
            if element["actor type"] >= 0 and len(scnr_data["actor palette"]) > element["actor type"]:
                tag_ref = scnr_data["actor palette"][element["actor type"]]
                tag_path = get_tag_display(tag_ref["reference"])

            platoon_unique_name = get_block_collection(element["platoon"], block_indices, scnr_data["encounters"][block_indices[0]]["platoons"], "%s_e%sp%s")
            squad_unique_name = get_block_collection(element["maneuver to squad"], block_indices, scnr_data["encounters"][block_indices[0]]["squads"], "%s_e%ss%s")

            encounter_flags = SquadFlags(element["flags"])

            ob.tag_squad.name = element["name"]
            ob.tag_squad.actor_type = tag_path
            if not platoon_unique_name == None:
                ob.tag_squad.platoon = global_functions.get_referenced_collection(platoon_unique_name, bpy.data.collections.get("Platoons_e%s" % block_indices[0]))
            ob.tag_squad.initial_state = str(element["initial state"]["value"])
            ob.tag_squad.return_state = str(element["return state"]["value"])
            ob.tag_squad.unused = SquadFlags.unused in encounter_flags
            ob.tag_squad.never_search = SquadFlags.never_search in encounter_flags
            ob.tag_squad.start_timer_immediately = SquadFlags.start_timer_immediately in encounter_flags
            ob.tag_squad.no_timer_delay_forever = SquadFlags.no_timer_delay_forever in encounter_flags
            ob.tag_squad.magic_sight_after_timer = SquadFlags.magic_sight_after_timer in encounter_flags
            ob.tag_squad.automatic_migration = SquadFlags.automatic_migration in encounter_flags
            ob.tag_squad.unique_leader_type = str(element["unique leader type"]["value"])
            if not squad_unique_name == None:
                ob.tag_squad.maneuver_to_squad = global_functions.get_referenced_collection(squad_unique_name, ob_parent)
            ob.tag_squad.squad_delay_time = element["squad delay time"]
            ob.tag_squad.attacking_groups = get_group_string(element["attacking"])
            ob.tag_squad.attacking_search_groups = get_group_string(element["attacking search"])
            ob.tag_squad.attacking_guard_groups = get_group_string(element["attacking guard"])
            ob.tag_squad.defending_groups = get_group_string(element["defending"])
            ob.tag_squad.defending_search_groups = get_group_string(element["defending search"])
            ob.tag_squad.defending_guard_groups = get_group_string(element["defending guard"])
            ob.tag_squad.pursuing_groups = get_group_string(element["pursuing"])
            ob.tag_squad.normal_diff_count = element["normal diff count"]
            ob.tag_squad.insane_diff_count = element["insane diff count"]
            ob.tag_squad.major_upgrade = str(element["major upgrade"]["value"])
            ob.tag_squad.respawn_min_actors = element["respawn min actors"]
            ob.tag_squad.respawn_max_actors = element["respawn max actors"]
            ob.tag_squad.respawn_total = element["respawn total"]
            rd_min, rd_max = element["respawn delay"].values()
            ob.tag_squad.respawn_delay_min = rd_min
            ob.tag_squad.respawn_delay_max = rd_max

        elif ob_parent_name.startswith("move_positions"):
            ob.tag_move_position.weight = element["weight"]
            ob.tag_move_position.time = element["time"]
            ob.tag_move_position.animation = element["animation"]
            ob.tag_move_position.sequence_id = element["sequence id"]
            ob.tag_move_position.surface_index = element["surface index"]

        elif ob_parent_name.startswith("starting_location"):
            command_list_collection = None
            if element["command list"] >= 0 and len(scnr_data["command lists"]) > element["command list"]:
                command_list_block_collection = bpy.data.collections.get("Command Lists")

                command_list_name = scnr_data["command lists"][element["command list"]]["name"]

                command_list_name = "%s_cl%s" % (command_list_name, element["command list"])
                command_list_collection = global_functions.get_referenced_collection(command_list_name, command_list_block_collection, True)

            tag_path = ""
            if element["actor type"] >= 0 and len(scnr_data["actor palette"]) > element["actor type"]:
                tag_ref = scnr_data["actor palette"][element["actor type"]]
                tag_path = get_tag_display(tag_ref["reference"])

            starting_location_flags = StartingLocationFlags(element["flags"])

            ob.tag_starting_location.sequence_id = element["sequence id"]
            ob.tag_starting_location.flags = StartingLocationFlags.required in starting_location_flags
            ob.tag_starting_location.return_state = str(element["return state"]["value"])
            ob.tag_starting_location.initial_state = str(element["initial state"]["value"])
            ob.tag_starting_location.actor_type = tag_path

            if not command_list_collection == None:
                ob.tag_starting_location.command_list = command_list_collection

        elif ob_parent_name.startswith("platoons"):
            platoon_unique_name_a = get_block_collection(element["happens to"], block_indices, scnr_data["encounters"][block_indices[0]]["platoons"], "%s_e%sp%s")
            platoon_unique_name_b = get_block_collection(element["happens to 1"], block_indices, scnr_data["encounters"][block_indices[0]]["platoons"], "%s_e%sp%s")

            platoon_flags = PlatoonFlags(element["flags"])

            ob.tag_platoon.name = element["name"]
            ob.tag_platoon.flee_when_maneuvering = PlatoonFlags.flee_when_maneuvering in platoon_flags
            ob.tag_platoon.say_advancing_when_maneuver = PlatoonFlags.say_advancing_when_maneuver in platoon_flags
            ob.tag_platoon.start_in_defending_state = PlatoonFlags.start_in_defending_state in platoon_flags
            ob.tag_platoon.change_attacking_defending_state = str(element["change attacking defending state when"]["value"])
            if not platoon_unique_name_a == None:
                ob.tag_platoon.happens_to_a = global_functions.get_referenced_collection(platoon_unique_name_a, ob_parent)
            ob.tag_platoon.maneuver_when = str(element["maneuver when"]["value"])
            if not platoon_unique_name_b == None:
                ob.tag_platoon.happens_to_b = global_functions.get_referenced_collection(platoon_unique_name_b, ob_parent)

        elif ob_parent_name.startswith("firing_points"):
            ob.tag_firing_position.group_index = str(element["group index"]["value"])

        elif ob_parent_name.startswith("command_lists"):
            command_list_flags = CommandListFlags(element["flags"])

            ob.tag_command_list.name = element["name"]
            ob.tag_command_list.allow_initiative = CommandListFlags.allow_initiative in command_list_flags
            ob.tag_command_list.allow_targeting = CommandListFlags.allow_targeting in command_list_flags
            ob.tag_command_list.disable_looking = CommandListFlags.disable_looking in command_list_flags
            ob.tag_command_list.disable_communication = CommandListFlags.disable_communication in command_list_flags
            ob.tag_command_list.disable_falling_damage = CommandListFlags.disable_falling_damage in command_list_flags
            ob.tag_command_list.manual_bsp_index_flag = CommandListFlags.manual_bsp_index in command_list_flags
            ob.tag_command_list.manual_bsp_index = element["manual bsp index"]

        elif ob_parent_name.startswith("commands"):
            command_unique_name = get_block_collection(element["command"], block_indices, scnr_data["command lists"][block_indices[0]]["commands"], "command_cl%sc%s", False)
            command_point_1 = get_point(block_indices, element["point 1"], scnr_data["command lists"][block_indices[0]]["points"], level_root)
            command_point_2 = get_point(block_indices, element["point 2"], scnr_data["command lists"][block_indices[0]]["points"], level_root)

            object_name = ""
            if element["object name"] >= 0:
                object_name = scnr_data["object names"][element["object name"]]["name"]

            ob.tag_command.atom_type = str(element["atom type"]["value"])
            ob.tag_command.atom_modifier = element["atom modifier"]
            ob.tag_command.parameter_1 = element["parameter1"]
            ob.tag_command.parameter_2 = element["parameter2"]
            if not command_point_1 == None:
                ob.tag_command.point_1 = command_point_1
            if not command_point_2 == None:
                ob.tag_command.point_2 = command_point_2
            ob.tag_command.animation_index = element["animation"]
            ob.tag_command.script_index = element["script"]
            ob.tag_command.recording_index = element["recording"]
            if not command_unique_name == None:
                ob.tag_command.command_index = global_functions.get_referenced_collection(command_unique_name, ob_parent)
            ob.tag_command.object_name = object_name

        elif ob_parent_name.startswith("cutscene_flags"):
            ob.tag_cutscene_flag.name = element["name"]

        elif ob_parent_name.startswith("cutscene_cameras"):
            ob.tag_cutscene_camera.name = element["name"]

def generate_skies(context, level_root, scnr_data, asset_cache):
    asset_collection = global_functions.get_referenced_collection("Skies", context.scene.collection, False)
    for element_idx, element in enumerate(scnr_data["skies"]):
        sky_asset = tag_interface.get_disk_asset(element["sky"]["path"], h1_tag_groups.get(element["sky"]["group name"]))
        sky_data = sky_asset["Data"]
        tag_name = os.path.basename(element["sky"]["path"])
        sky_collection = global_functions.get_referenced_collection("sky_%s_%s" % (tag_name, element_idx), asset_collection, False)
        if not sky_asset == None:
            for light_idx, light in enumerate(sky_data["lights"]):
                name = "%s_light_%s" % (tag_name, light_idx)
                light_data = bpy.data.lights.new(name, "SUN")
                ob = bpy.data.objects.new(name, light_data)
                ob.color = (1, 1, 1, 0)

                ob.data.color = convert_to_blender_color(light["color"], False)
                ob.data.energy = light["power"] * 10
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
        font = bpy.data.curves.new(type="FONT", name="comment")
        font_ob = bpy.data.objects.new("comment_%s" % comment_idx, font)
        font_ob.color = (1, 1, 1, 0)
        font_ob.data.body = base64.b64decode(comment_element["comment"]["encoded"])

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
        hide_collection = True
        tag_block = scnr_data["light fixtures"]
        tag_palette = scnr_data["light fixture palette"]
    elif collection_name == "Sound Scenery":
        hide_collection = True
        tag_block = scnr_data["sound scenery"]
        tag_palette = scnr_data["sound scenery palette"]

    asset_collection = global_functions.get_referenced_collection(collection_name, context.scene.collection, hide_collection)
    for palette_element in tag_palette:
        object_asset = tag_interface.get_disk_asset(palette_element["name"]["path"], h1_tag_groups.get(palette_element["name"]["group name"]))
        if not object_asset == None:
            mesh_collections = ("Scenery", "Bipeds", "Vehicles", "Equipment", "Weapons", "Machines", "Controls", "Light Fixtures", "Sound Scenery")
            if collection_name in mesh_collections:
                if object_asset["Data"]["model"]["group name"] == "mode":
                    object_asset["Data"]["model"]["group name"] = "mod2"

                model_asset = tag_interface.get_disk_asset(object_asset["Data"]["model"]["path"], h1_tag_groups.get(object_asset["Data"]["model"]["group name"]))
                if model_asset is not None and len(object_asset["Data"]["model"]["path"]) > 0:
                    mesh = asset_cache[object_asset["Data"]["model"]["group name"]][object_asset["Data"]["model"]["path"]]["blender_assets"].get("blender_asset")
                    if not mesh:
                        get_geometry_layout(object_asset["Data"]["model"], asset_cache, None, False, report, True)

    palette_count = len(tag_palette)
    for element_idx, element in enumerate(tag_block):
        tag_path = ""
        mesh_data = None
        tag_path_no_ext = ""
        if element["type"] >= 0 and element["type"] < palette_count:
            pallete_item = tag_palette[element["type"]]["name"]
            tag_path_no_ext = pallete_item["path"]
            tag_path = "%s.%s" % (pallete_item["path"], h1_tag_groups.get(pallete_item["group name"]))
            palette_asset = tag_interface.get_disk_asset(pallete_item["path"], h1_tag_groups.get(pallete_item["group name"]))
            if palette_asset is not None and len(palette_asset["Data"]["model"]["path"]) > 0:
                mesh_data = asset_cache[palette_asset["Data"]["model"]["group name"]][palette_asset["Data"]["model"]["path"]]["blender_assets"].get("blender_asset")

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

        if collection_name == "Scenery" and ObjectFlags.automatically in ObjectFlags(element["not placed"]):
            root.hide_set(True)
            root.hide_render = True

def generate_netgame_equipment_elements(context, level_root, scnr_data, asset_cache, fix_rotations, report, random_color_gen):
    asset_collection = global_functions.get_referenced_collection("Netgame Equipment", context.scene.collection, True)
    for element_idx, element in enumerate(scnr_data["netgame equipment"]):
        ob = None
        tag_path = ""
        tag_path_no_ext = element["item collection"]["path"]

        tag_name = "NONE"
        if not global_functions.string_empty_check(tag_path_no_ext):
            tag_name = os.path.basename(tag_path_no_ext)

        object_name = "%s_%s" % (tag_name, element_idx)
        object_asset = tag_interface.get_disk_asset(element["item collection"]["path"], h1_tag_groups.get(element["item collection"]["group name"]))
        model_asset = None
        if not object_asset == None:
            tag_path = "%s.%s" % (element["item collection"]["path"], h1_tag_groups.get(element["item collection"]["group name"]))
            object_data = object_asset["Data"]
            if len(object_data["permutations"]) > 0:
                item_permutation_element = object_data["permutations"][0]
                item_asset = tag_interface.get_disk_asset(item_permutation_element["item"]["path"], h1_tag_groups.get(item_permutation_element["item"]["group name"]))
                if not item_asset == None:
                    item_data = item_asset["Data"]
                    model_asset = tag_interface.get_disk_asset(item_data["model"]["path"], h1_tag_groups.get(item_data["model"]["group name"]))
                    if not model_asset == None:
                        get_geometry_layout(item_data["model"], asset_cache, None, False, report, True)

        if model_asset:
            mesh_data = asset_cache[item_data["model"]["group name"]][item_data["model"]["path"]]["blender_assets"].get("blender_asset")
            ob = bpy.data.objects.new(object_name, mesh_data)
            ob.color = (1, 1, 1, 0)

        else:
            ob = bpy.data.objects.new(object_name, None)
            ob.color = (1, 1, 1, 0)
            ob.empty_display_type = 'ARROWS'

        asset_collection.objects.link(ob)

        get_data_type(ob, asset_collection, element, scnr_data, tag_path)

        ob.parent = level_root
        ob.location = Vector(element["position"]) * 100
        ob.rotation_euler = (radians(0.0), radians(0.0), radians(element["facing"]))

def generate_encounters(context, level_root, scnr_data):
    collection_name = "Encounters"

    asset_collection = global_functions.get_referenced_collection(collection_name, context.scene.collection, True)
    for encounter_idx, encounter in enumerate(scnr_data["encounters"]):
        block_indices = (encounter_idx)
        encounter_coll_name = "%s_e%s" % (encounter["name"], encounter_idx)
        encounter_element_id = "e%s" % (encounter_idx)

        squads_coll_name = "Squads_e%s" % encounter_idx
        platoons_coll_name = "Platoons_e%s" % encounter_idx

        encounter_collection = global_functions.get_referenced_collection(encounter_coll_name, asset_collection, True)
        get_data_type(encounter_collection, asset_collection, encounter, scnr_data, block_indices=block_indices)

        s_e_collection = global_functions.get_referenced_collection(squads_coll_name, encounter_collection, True)
        p_e_collection = global_functions.get_referenced_collection(platoons_coll_name, encounter_collection, True)
        for squad_idx, squad in  enumerate(encounter["squads"]):
            block_indices = (encounter_idx, squad_idx)

            squad_coll_name = "%s_e%ss%s" % (squad["name"], encounter_idx, squad_idx)
            squad_element_id = "e%ss%s" % (encounter_idx, squad_idx)

            squad_collection = global_functions.get_referenced_collection(squad_coll_name, s_e_collection, True)
            get_data_type(squad_collection, s_e_collection, squad, scnr_data, block_indices=block_indices)

            generate_encounter_obs(context, level_root, "Move Positions", squad_collection, squad_element_id, scnr_data, block_indices)
            generate_encounter_obs(context, level_root, "Starting Locations", squad_collection, squad_element_id, scnr_data, block_indices)

        for platoon_idx, platoon in enumerate(encounter["platoons"]):
            platoon_coll_name = "%s_e%sp%s" % (platoon["name"], encounter_idx, platoon_idx)
            platoon_collection = global_functions.get_referenced_collection(platoon_coll_name, p_e_collection, True)
            get_data_type(platoon_collection, p_e_collection, platoon, scnr_data, block_indices=block_indices)

        generate_encounter_obs(context, level_root, "Firing Points", encounter_collection, encounter_element_id, scnr_data, block_indices)
        generate_encounter_obs(context, level_root, "Player Starting Locations", encounter_collection, encounter_element_id, scnr_data, block_indices)

def generate_encounter_obs(context, level_root, collection_name, parent_collection, element_id, scnr_data, block_indices=()):
    unique_collection_name = "%s_%s" % (collection_name, element_id)

    asset_collection = global_functions.get_referenced_collection(unique_collection_name, parent_collection, True)

    tag_block = None
    tag_palette = None
    if collection_name == "Move Positions":
        asset_collection.hide_render = False
        tag_block = scnr_data["encounters"][block_indices[0]]["squads"][block_indices[1]]["move positions"]
    elif collection_name == "Starting Locations":
        tag_block = scnr_data["encounters"][block_indices[0]]["squads"][block_indices[1]]["starting locations"]
        tag_palette = scnr_data["actor palette"] 
    elif collection_name == "Firing Points":
        tag_block = scnr_data["encounters"][block_indices[0]]["firing positions"]
    elif collection_name == "Player Starting Locations":
        tag_block = scnr_data["encounters"][block_indices[0]]["player starting locations"]

    for element_idx, element in enumerate(tag_block):
        tag_name = unique_collection_name

        ob = bpy.data.objects.new("%s_%s" % (tag_name, element_idx), None)
        ob.color = (1, 1, 1, 0)

        ob.empty_display_type = 'ARROWS'
        ob.parent = level_root
        ob.location = Vector(element["position"]) * 100
        if not collection_name == "Firing Points":
            ob.rotation_euler = (radians(0.0), radians(0.0), radians(element["facing"]))

        get_data_type(ob, asset_collection, element, scnr_data)

        asset_collection.objects.link(ob)

def generate_command_lists(context, level_root, scnr_data):
    collection_name = "Command Lists"

    asset_collection = global_functions.get_referenced_collection(collection_name, context.scene.collection, True)
    for command_list_idx, command_list in enumerate(scnr_data["command lists"]):
        block_indices = (command_list_idx)
        command_list_name = "%s_cl%s" % (command_list["name"], command_list_idx)
        commands_coll_name = "Commands_cl%s" % command_list_idx
        points_coll_name = "Points_cl%s" % command_list_idx

        command_list_collection = global_functions.get_referenced_collection(command_list_name, asset_collection, True)
        get_data_type(command_list_collection, asset_collection, command_list, scnr_data, block_indices=block_indices)

        c_cl_collection = global_functions.get_referenced_collection(commands_coll_name, command_list_collection, True)
        p_cl_collection = global_functions.get_referenced_collection(points_coll_name, command_list_collection, True)
        for command_idx, command in  enumerate(command_list["commands"]):
            block_indices = (command_list_idx, command_idx)

            command_coll_name = "%s_cl%sc%s" % ("command", command_list_idx, command_idx)

            command_collection = global_functions.get_referenced_collection(command_coll_name, c_cl_collection, True)
            get_data_type(command_collection, c_cl_collection, command, scnr_data, block_indices=block_indices)

        for point_idx, point in enumerate(command_list["points"]):
            point_ob = get_point(block_indices, point_idx, scnr_data["command lists"][block_indices[0]]["points"], level_root)

def generate_empties(context, level_root, collection_name, scnr_data, parent_collection):
    asset_collection = global_functions.get_referenced_collection(collection_name, parent_collection, True)

    tag_block = None
    if collection_name == "Player Starting Locations":
        tag_block = scnr_data["player starting locations"]
    elif collection_name == "Netgame Flags":
        tag_block = scnr_data["netgame flags"]

    for element_idx, element in enumerate(tag_block):
        tag_name = collection_name
        tag_path = ""
        if collection_name == "Netgame Flags":
            tag_path_no_ext = element["weapon group"]["path"]
            tag_path = "%s.%s" % (element["weapon group"]["path"], h1_tag_groups.get(element["weapon group"]["group name"]))

            tag_name = collection_name
            if not global_functions.string_empty_check(tag_path_no_ext):
                tag_name = os.path.basename(tag_path_no_ext)

        ob = bpy.data.objects.new("%s_%s" % (tag_name, element_idx), None)
        ob.color = (1, 1, 1, 0)

        ob.empty_display_type = 'ARROWS'
        ob.parent = level_root
        ob.location = Vector(element["position"]) * 100
        if not collection_name.startswith("Firing Points"):
            ob.rotation_euler = (radians(0.0), radians(0.0), radians(element["facing"]))

        get_data_type(ob, asset_collection, element, scnr_data, tag_path)

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

        ob.data.lens_unit = 'FOV'
        ob.data.angle = radians(element["field of view"])

        ob.rotation_euler = get_rotation_euler(*element["orientation"])
        ob.rotation_euler.rotate_axis("X", radians(90.0))
        ob.rotation_euler.rotate_axis("Y", radians(-90.0))

        get_data_type(ob, asset_collection, element, scnr_data)

        asset_collection.objects.link(ob)

def generate_trigger_volumes(context, level_root, scnr_data):
    collection_name = "Trigger Volumes"

    asset_collection = global_functions.get_referenced_collection(collection_name, context.scene.collection, True)
    for element_idx, element in enumerate(scnr_data["trigger volumes"]):
        mesh = bpy.data.meshes.new("part_%s" % element["name"])
        ob = bpy.data.objects.new(element["name"], mesh)
        ob.color = (1, 1, 1, 0)

        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=2.0)
        bm.transform(Matrix.Translation((1, 1, 1)))
        bm.to_mesh(mesh)
        bm.free()

        ob.parent = level_root
        forward = Vector(element["rotation vector forward"])
        up = Vector(element["rotation vector up"])
        right = np.cross(up, forward)
        matrix_rotation = Matrix((forward, right, up))

        ob.matrix_world = matrix_rotation.to_4x4()
        ob.location = Vector(element["starting corner"]) * 100
        ob.dimensions = Vector(element["ending corner offset"]) * 100

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
            tag_path = "%s.%s" % (tag_ref["path"], h1_tag_groups.get(tag_ref["group name"]))

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
        ob.rotation_euler = get_decal_rotation_euler(element["yaw"], element["pitch"])

        get_data_type(ob, asset_collection, element, scnr_data, tag_path)

def generate_scenario_scene(context, tag_ref, asset_cache, game_title, fix_rotations, empty_markers, report):
    scnr_asset = tag_interface.get_disk_asset(tag_ref["path"], h1_tag_groups.get(tag_ref["group name"]))
    scnr_data = scnr_asset["Data"]

    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors
    levels_collection = global_functions.get_referenced_collection("BSPs", context.scene.collection, False)
    for bsp_idx, bsp in enumerate(scnr_data["structure bsps"]):
        bsp_tag_ref = bsp["structure bsp"]
        sbps_asset = tag_interface.get_disk_asset(bsp_tag_ref["path"], h1_tag_groups.get(bsp_tag_ref["group name"]))
        if not sbps_asset == None:
            bsp_name = os.path.basename(bsp_tag_ref["path"])
            c_bsp_name = "%s_%s" % (bsp_name, bsp_idx)
            c_cluster_name = "%s_clusters" % (bsp_name)
            level_collection = global_functions.get_referenced_collection(c_bsp_name, levels_collection, False)
            clusters_collection = global_functions.get_referenced_collection(c_cluster_name, level_collection, False)

            build_scene_level.build_scene(context, bsp_tag_ref, asset_cache, game_title, fix_rotations, empty_markers, report, level_collection, clusters_collection)

    level_root = bpy.data.objects.get("frame_root")
    if level_root == None:
        level_mesh = bpy.data.meshes.new("frame_root")
        level_root = bpy.data.objects.new("frame_root", level_mesh)
        level_root.color = (1, 1, 1, 0)
        context.collection.objects.link(level_root)

    for object_name in scnr_data["object names"]:
        if not global_functions.string_empty_check(object_name["name"]):
            context.scene.object_name_add(object_name["name"])

    tag_references = set()
    if not global_functions.string_empty_check(scnr_data["dont use"]["path"]):
        tag_references.add((scnr_data["dont use"]["path"], scnr_data["dont use"]["group name"]))
    if not global_functions.string_empty_check(scnr_data["wont use"]["path"]):
        tag_references.add((scnr_data["wont use"]["path"], scnr_data["wont use"]["group name"]))
    if not global_functions.string_empty_check(scnr_data["cant use"]["path"]):
        tag_references.add((scnr_data["cant use"]["path"], scnr_data["cant use"]["group name"]))
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
    for light_element in scnr_data["light fixture palette"]:
        if not global_functions.string_empty_check(light_element["name"]["path"]):
            tag_references.add((light_element["name"]["path"], light_element["name"]["group name"]))
    for sound_element in scnr_data["sound scenery palette"]:
        if not global_functions.string_empty_check(sound_element["name"]["path"]):
            tag_references.add((sound_element["name"]["path"], sound_element["name"]["group name"]))
    for flag_element in scnr_data["netgame flags"]:
        if not global_functions.string_empty_check(flag_element["weapon group"]["path"]):
            tag_references.add((flag_element["weapon group"]["path"], flag_element["weapon group"]["group name"]))
    for netgame_equipment_element in scnr_data["netgame equipment"]:
        if not global_functions.string_empty_check(netgame_equipment_element["item collection"]["path"]):
            tag_references.add((netgame_equipment_element["item collection"]["path"], netgame_equipment_element["item collection"]["group name"]))
    for decal_palette_element in scnr_data["decal palette"]:
        if not global_functions.string_empty_check(decal_palette_element["reference"]["path"]):
            tag_references.add((decal_palette_element["reference"]["path"], decal_palette_element["reference"]["group name"]))
    for actor_element in scnr_data["actor palette"]:
        if not global_functions.string_empty_check(actor_element["reference"]["path"]):
            tag_references.add((actor_element["reference"]["path"], actor_element["reference"]["group name"]))
    if not global_functions.string_empty_check(scnr_data["custom object names"]["path"]):
        tag_references.add((scnr_data["custom object names"]["path"], scnr_data["custom object names"]["group name"]))
    if not global_functions.string_empty_check(scnr_data["ingame help text"]["path"]):
        tag_references.add((scnr_data["ingame help text"]["path"], scnr_data["ingame help text"]["group name"]))
    if not global_functions.string_empty_check(scnr_data["hud messages"]["path"]):
        tag_references.add((scnr_data["hud messages"]["path"], scnr_data["hud messages"]["group name"]))

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
    if len(scnr_data["player starting locations"]) > 0:
        generate_empties(context, level_root, "Player Starting Locations", scnr_data, context.scene.collection)
    if len(scnr_data["netgame flags"]) > 0:
        generate_empties(context, level_root, "Netgame Flags", scnr_data, context.scene.collection)
    if len(scnr_data["netgame equipment"]) > 0:
        generate_netgame_equipment_elements(context, level_root, scnr_data, asset_cache, fix_rotations, report, random_color_gen)
    if len(scnr_data["trigger volumes"]) > 0:
        generate_trigger_volumes(context, level_root, scnr_data)
    if len(scnr_data["decals"]) > 0:
        generate_decals(context, level_root, scnr_data)
    if len(scnr_data["command lists"]) > 0:
        generate_command_lists(context, level_root, scnr_data)
    if len(scnr_data["encounters"]) > 0:
        generate_encounters(context, level_root, scnr_data)
    if len(scnr_data["cutscene flags"]) > 0:
        generate_camera_flags(context, level_root, scnr_data)
    if len(scnr_data["cutscene camera points"]) > 0:
        generate_camera_points(context, level_root, scnr_data)
