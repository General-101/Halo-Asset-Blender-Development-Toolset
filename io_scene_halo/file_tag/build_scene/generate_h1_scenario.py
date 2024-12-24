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

from mathutils import Euler, Matrix, Vector
from math import radians, degrees, cos, sin, asin, atan2
from . import build_bsp as build_scene_level
from ...global_functions import global_functions
from ...global_functions.parse_tags import parse_tag
from ..h1.file_scenario.mesh_helper.build_mesh import get_object
from ..h1.file_scenario.format import (ScenarioFlags, 
                                       ObjectFlags, 
                                       UnitFlags, 
                                       VehicleFlags, 
                                       ItemFlags, 
                                       DeviceFlags, 
                                       MachineFlags, 
                                       ControlFlags, 
                                       NetGameEquipment,
                                       EncounterFlags,
                                       SquadFlags,
                                       StartingLocationFlags,
                                       PlatoonFlags,
                                       GroupFlags,
                                       CommandListFlags)
from ...global_ui.tag_fields.object_names import object_name_add
from ...global_functions.tag_format import h1_tag_groups, h1_tag_groups_dic, h1_tag_extensions_dic

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
    if not global_functions.string_empty_check(tag_ref.name):
        tag_display = "%s.%s" % (tag_ref.name, h1_tag_groups_dic.get(tag_ref.tag_group))

    return tag_display

def get_group_string(behavior_flags):
    group_string = ""
    group_flags = GroupFlags(behavior_flags)
    for group_flag in GroupFlags:
        if group_flag in group_flags:
            group_string += group_flag.name.upper()

    return group_string

def get_referenced_collection(collection_name, parent_collection, hide_render=False):
    asset_collection = bpy.data.collections.get(collection_name)
    if asset_collection == None:
        asset_collection = bpy.data.collections.new(collection_name)
        parent_collection.children.link(asset_collection)
        if not parent_collection.name == "Scene Collection":
            asset_collection.tag_collection.parent = parent_collection

    asset_collection.hide_render = hide_render

    return asset_collection

def get_block_collection(block_index, block_indices, tag_block, key, has_name=True):
    unique_name = None
    if block_index >= 0 and len(tag_block) > block_index:
        if has_name:
            platoon_name = tag_block[block_index].name
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

            ob.empty_display_type = 'ARROWS'
            ob.parent = level_root
            ob.location = tag_block[point_index] * 100

            point_collection.objects.link(ob)

    return ob

def set_scenario_data(context, SCENARIO):
    context.scene.tag_scenario.dont_use = get_tag_display(SCENARIO.dont_use_tag_ref)
    context.scene.tag_scenario.wont_use = get_tag_display(SCENARIO.wont_use_tag_ref)
    context.scene.tag_scenario.cant_use = get_tag_display(SCENARIO.cant_use_tag_ref)
    context.scene.tag_scenario.scenario_type_enum = str(SCENARIO.scenario_type)

    scenario_flags = ScenarioFlags(SCENARIO.scenario_flags)
    context.scene.tag_scenario.cortana_hack = ScenarioFlags.cortana_hack in scenario_flags
    context.scene.tag_scenario.use_demo_ui = ScenarioFlags.use_demo_ui in scenario_flags
    context.scene.tag_scenario.color_correction = ScenarioFlags.color_correction_ntsc_srgb in scenario_flags
    context.scene.tag_scenario.disable_tag_patches = ScenarioFlags.do_not_apply_bungie_campaign_patches in scenario_flags

    context.scene.tag_scenario.local_north = radians(SCENARIO.local_north)
    context.scene.tag_scenario.custom_object_names = get_tag_display(SCENARIO.custom_object_names_tag_ref)
    context.scene.tag_scenario.ingame_help_text = get_tag_display(SCENARIO.chapter_title_text_tag_ref)
    context.scene.tag_scenario.hud_messages = get_tag_display(SCENARIO.hud_messages_tag_ref)

def set_object_data(ob, tag_path, element, object_name_tag_block):
    element_flags = ObjectFlags(element.placement_flags)

    object_name = ""
    if element.name_index >= 0:
        object_name = object_name_tag_block[element.name_index]
        
    ob.tag_object.tag_path = tag_path
    ob.tag_object.object_name = object_name
    ob.tag_object.automatically = ObjectFlags.automatically in element_flags
    ob.tag_object.on_easy = ObjectFlags.on_easy in element_flags
    ob.tag_object.on_normal = ObjectFlags.on_normal in element_flags
    ob.tag_object.on_hard = ObjectFlags.on_hard in element_flags
    ob.tag_object.use_player_appearance = ObjectFlags.use_player_appearance in element_flags
    ob.tag_object.desired_permutation = element.desired_permutation
    ob.tag_object.appearance_player_index = element.appearance_player_index

def set_unit_data(ob, element):
    element_flags = UnitFlags(element.flags)

    ob.tag_unit.unit_vitality = element.body_vitality
    ob.tag_unit.unit_dead = UnitFlags.dead in element_flags

def set_vehicle_data(ob, element):
    element_flags = VehicleFlags(element.multiplayer_spawn_flags)

    ob.tag_unit.multiplayer_team_index = element.multiplayer_team_index
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

def get_data_type(ob, ob_parent, element, H1_ASSET, tag_path="", block_indices=(), level_root=None):
        ob_parent_name = ob_parent.name.lower().replace(" ", "_")

        if ob_parent_name.startswith("bsps"):
            ob.tag_mesh.lightmap_index = -1

        elif ob_parent_name.startswith("scenery"):
            set_object_data(ob, tag_path, element, H1_ASSET.object_names)

        elif ob_parent_name.startswith("biped"):
            ob.lock_rotation[0] = True
            ob.lock_rotation[1] = True

            set_object_data(ob, tag_path, element, H1_ASSET.object_names)
            set_unit_data(ob, element)

        elif ob_parent_name.startswith("vehicle"):
            set_object_data(ob, tag_path, element, H1_ASSET.object_names)
            set_unit_data(ob, element)
            set_vehicle_data(ob, element)

        elif ob_parent_name.startswith("equipment"):
            set_object_data(ob, tag_path, element, H1_ASSET.object_names)
            set_item_data(ob, element.misc_flags)

        elif ob_parent_name.startswith("weapons"):
            set_object_data(ob, tag_path, element, H1_ASSET.object_names)
            ob.tag_weapon.rounds_left = element.rounds_left
            ob.tag_weapon.rounds_loaded = element.rounds_loaded
            set_item_data(ob, element.flags)

        elif ob_parent_name.startswith("machines"):
            set_object_data(ob, tag_path, element, H1_ASSET.object_names)
            ob.tag_device.power_group = element.power_group_index
            ob.tag_device.position_group = element.position_group_index
            set_device_data(ob, element.flags_0)
            set_machine_data(ob, element.flags_1)

        elif ob_parent_name.startswith("controls"):
            set_object_data(ob, tag_path, element, H1_ASSET.object_names)
            ob.tag_device.power_group = element.power_group_index
            ob.tag_device.position_group = element.position_group_index
            set_device_data(ob, element.flags_0)
            set_control_data(ob, element.flags_1)
            ob.tag_control.control_value = element.unknown

        elif ob_parent_name.startswith("light_fixtures"):
            set_object_data(ob, tag_path, element, H1_ASSET.object_names)
            ob.tag_device.power_group = element.power_group_index
            ob.tag_device.position_group = element.position_group_index
            set_device_data(ob, element.flags)
            ob.tag_light_fixture.color = element.color_RGBA[0:3]
            ob.tag_light_fixture.intensity = element.intensity
            ob.tag_light_fixture.falloff_angle = element.falloff_angle
            ob.tag_light_fixture.cutoff_angle = element.cutoff_angle

        elif ob_parent_name.startswith("sound_scenery"):
            set_object_data(ob, tag_path, element, H1_ASSET.object_names)

        elif ob_parent_name.startswith("player_starting_locations"):
            ob.tag_player_starting_location.team_index = element.team_index
            ob.tag_player_starting_location.bsp_index = element.bsp_index
            ob.tag_player_starting_location.type_0 = str(element.type_0)
            ob.tag_player_starting_location.type_1 = str(element.type_1)
            ob.tag_player_starting_location.type_2 = str(element.type_2)
            ob.tag_player_starting_location.type_3 = str(element.type_3)

        elif ob_parent_name.startswith("netgame_flags"):
            ob.tag_netgame_flag.netgame_type = str(element.type)
            ob.tag_netgame_flag.usage_id = element.usage_id
            ob.tag_netgame_flag.weapon_group = tag_path

        elif ob_parent_name.startswith("netgame_equipment"):
            element_flags = NetGameEquipment(element.flags)

            ob.tag_netgame_equipment.levitate = NetGameEquipment.levitate in element_flags
            ob.tag_netgame_equipment.type_0 = str(element.type_0)
            ob.tag_netgame_equipment.type_1 = str(element.type_1)
            ob.tag_netgame_equipment.type_2 = str(element.type_2)
            ob.tag_netgame_equipment.type_3 = str(element.type_3)
            ob.tag_netgame_equipment.team_index = element.team_index
            ob.tag_netgame_equipment.spawn_time = element.spawn_time
            ob.tag_netgame_equipment.item_collection = tag_path

        elif ob_parent_name.startswith("decal"):
            ob.tag_decal.decal_type = tag_path
            ob.tag_decal.yaw = element.yaw
            ob.tag_decal.pitch = element.pitch

        elif ob_parent_name.startswith("encounter"):
            encounter_flags = EncounterFlags(element.flags)

            ob.tag_collection.parent = ob_parent

            ob.tag_encounter.name = element.name
            ob.tag_encounter.not_initially_created = EncounterFlags.not_initially_created in encounter_flags
            ob.tag_encounter.respawn_enabled = EncounterFlags.respawn_enabled in encounter_flags
            ob.tag_encounter.initially_blind = EncounterFlags.initially_blind in encounter_flags
            ob.tag_encounter.initially_deaf = EncounterFlags.initially_deaf in encounter_flags
            ob.tag_encounter.initially_braindead = EncounterFlags.initially_braindead in encounter_flags
            ob.tag_encounter.firing_positions = EncounterFlags._3d_firing_positions in encounter_flags
            ob.tag_encounter.manual_bsp_index_specified = EncounterFlags.manual_bsp_index_specified in encounter_flags
            ob.tag_encounter.team_index = str(element.team_index)
            ob.tag_encounter.search_behavior = str(element.search_behavior)
            ob.tag_encounter.manual_bsp_index = element.manual_bsp_index
            ob.tag_encounter.respawn_delay_min = element.respawn_delay[0]
            ob.tag_encounter.respawn_delay_max = element.respawn_delay[1]

        elif ob_parent_name.startswith("squads"):
            tag_path = ""
            if element.actor_type >= 0 and len(H1_ASSET.actor_palette) > element.actor_type:
                tag_ref = H1_ASSET.actor_palette[element.actor_type]
                tag_path = get_tag_display(tag_ref)

            platoon_unique_name = get_block_collection(element.platoon, block_indices, H1_ASSET.encounters[block_indices[0]].platoons, "%s_e%sp%s")
            squad_unique_name = get_block_collection(element.maneuver_to_squad, block_indices, H1_ASSET.encounters[block_indices[0]].squads, "%s_e%ss%s")

            encounter_flags = SquadFlags(element.flags)

            ob.tag_squad.name = element.name
            ob.tag_squad.actor_type = tag_path
            if not platoon_unique_name == None:
                ob.tag_squad.platoon = get_referenced_collection(platoon_unique_name, bpy.data.collections.get("Platoons_e%s" % block_indices[0]))
            ob.tag_squad.initial_state = str(element.initial_state)
            ob.tag_squad.return_state = str(element.return_state)
            ob.tag_squad.unused = SquadFlags.unused in encounter_flags
            ob.tag_squad.never_search = SquadFlags.never_search in encounter_flags
            ob.tag_squad.start_timer_immediately = SquadFlags.start_timer_immediately in encounter_flags
            ob.tag_squad.no_timer_delay_forever = SquadFlags.no_timer_delay_forever in encounter_flags
            ob.tag_squad.magic_sight_after_timer = SquadFlags.magic_sight_after_timer in encounter_flags
            ob.tag_squad.automatic_migration = SquadFlags.automatic_migration in encounter_flags
            ob.tag_squad.unique_leader_type = str(element.unique_leader_type)
            if not squad_unique_name == None:
                ob.tag_squad.maneuver_to_squad = get_referenced_collection(squad_unique_name, ob_parent)
            ob.tag_squad.squad_delay_time = element.squad_delay_time
            ob.tag_squad.attacking_groups = get_group_string(element.attacking)
            ob.tag_squad.attacking_search_groups = get_group_string(element.attacking_search)
            ob.tag_squad.attacking_guard_groups = get_group_string(element.attacking_guard)
            ob.tag_squad.defending_groups = get_group_string(element.defending)
            ob.tag_squad.defending_search_groups = get_group_string(element.defending_search)
            ob.tag_squad.defending_guard_groups = get_group_string(element.defending_guard)
            ob.tag_squad.pursuing_groups = get_group_string(element.pursuing)
            ob.tag_squad.normal_diff_count = element.normal_diff_count
            ob.tag_squad.insane_diff_count = element.insane_diff_count
            ob.tag_squad.major_upgrade = str(element.major_upgrade)
            ob.tag_squad.respawn_min_actors = element.respawn_min_actors
            ob.tag_squad.respawn_max_actors = element.respawn_max_actors
            ob.tag_squad.respawn_total = element.respawn_total
            ob.tag_squad.respawn_delay_min = element.respawn_delay[0]
            ob.tag_squad.respawn_delay_max = element.respawn_delay[1]

        elif ob_parent_name.startswith("move_positions"):
            ob.tag_move_position.weight = element.weight
            ob.tag_move_position.time = element.time
            ob.tag_move_position.animation = element.animation
            ob.tag_move_position.sequence_id = element.sequence_id
            ob.tag_move_position.surface_index = element.surface_index

        elif ob_parent_name.startswith("starting_location"):
            command_list_collection = None
            if element.command_list >= 0 and len(H1_ASSET.command_lists) > element.command_list:
                command_list_block_collection = bpy.data.collections.get("Command Lists")

                command_list_name = H1_ASSET.command_lists[element.command_list].name

                command_list_name = "%s_cl%s" % (command_list_name, element.command_list)
                command_list_collection = get_referenced_collection(command_list_name, command_list_block_collection, True)

            tag_path = ""
            if element.actor_type >= 0 and len(H1_ASSET.actor_palette) > element.actor_type:
                tag_ref = H1_ASSET.actor_palette[element.actor_type]
                tag_path = get_tag_display(tag_ref)

            starting_location_flags = StartingLocationFlags(element.flags)

            ob.tag_starting_location.sequence_id = element.sequence_id
            ob.tag_starting_location.flags = StartingLocationFlags.required in starting_location_flags
            ob.tag_starting_location.return_state = str(element.return_state)
            ob.tag_starting_location.initial_state = str(element.initial_state)
            ob.tag_starting_location.actor_type = tag_path

            if not command_list_collection == None:
                ob.tag_starting_location.command_list = command_list_collection

        elif ob_parent_name.startswith("platoons"):
            platoon_unique_name_a = get_block_collection(element.happens_to_a, block_indices, H1_ASSET.encounters[block_indices[0]].platoons, "%s_e%sp%s")
            platoon_unique_name_b = get_block_collection(element.happens_to_b, block_indices, H1_ASSET.encounters[block_indices[0]].platoons, "%s_e%sp%s")

            platoon_flags = PlatoonFlags(element.flags)

            ob.tag_platoon.name = element.name
            ob.tag_platoon.flee_when_maneuvering = PlatoonFlags.flee_when_maneuvering in platoon_flags
            ob.tag_platoon.say_advancing_when_maneuver = PlatoonFlags.say_advancing_when_maneuver in platoon_flags
            ob.tag_platoon.start_in_defending_state = PlatoonFlags.start_in_defending_state in platoon_flags
            ob.tag_platoon.change_attacking_defending_state = str(element.change_attacking_defending_state)
            if not platoon_unique_name_a == None:
                ob.tag_platoon.happens_to_a = get_referenced_collection(platoon_unique_name_a, ob_parent)
            ob.tag_platoon.maneuver_when = str(element.maneuver_when)
            if not platoon_unique_name_b == None:
                ob.tag_platoon.happens_to_b = get_referenced_collection(platoon_unique_name_b, ob_parent)

        elif ob_parent_name.startswith("firing_points"):
            ob.tag_firing_position.group_index = str(element.group_index)

        elif ob_parent_name.startswith("command_lists"):
            command_list_flags = CommandListFlags(element.flags)

            ob.tag_command_list.name = element.name
            ob.tag_command_list.allow_initiative = CommandListFlags.allow_initiative in command_list_flags
            ob.tag_command_list.allow_targeting = CommandListFlags.allow_targeting in command_list_flags
            ob.tag_command_list.disable_looking = CommandListFlags.disable_looking in command_list_flags
            ob.tag_command_list.disable_communication = CommandListFlags.disable_communication in command_list_flags
            ob.tag_command_list.disable_falling_damage = CommandListFlags.disable_falling_damage in command_list_flags
            ob.tag_command_list.manual_bsp_index_flag = CommandListFlags.manual_bsp_index in command_list_flags
            ob.tag_command_list.manual_bsp_index = element.manual_bsp_index

        elif ob_parent_name.startswith("commands"):
            command_unique_name = get_block_collection(element.command, block_indices, H1_ASSET.command_lists[block_indices[0]].commands, "command_cl%sc%s", False)
            command_point_1 = get_point(block_indices, element.point_1, H1_ASSET.command_lists[block_indices[0]].points, level_root)
            command_point_2 = get_point(block_indices, element.point_2, H1_ASSET.command_lists[block_indices[0]].points, level_root)

            object_name = ""
            if element.object_name >= 0:
                object_name = H1_ASSET.object_names[element.object_name]

            ob.tag_command.atom_type = str(element.atom_type)
            ob.tag_command.atom_modifier = element.atom_modifier
            ob.tag_command.parameter_1 = element.parameter1
            ob.tag_command.parameter_2 = element.parameter2
            if not command_point_1 == None:
                ob.tag_command.point_1 = command_point_1
            if not command_point_2 == None:
                ob.tag_command.point_2 = command_point_2
            ob.tag_command.animation_index = element.animation
            ob.tag_command.script_index = element.script
            ob.tag_command.recording_index = element.recording
            if not command_unique_name == None:
                ob.tag_command.command_index = get_referenced_collection(command_unique_name, ob_parent)
            ob.tag_command.object_name = object_name

        elif ob_parent_name.startswith("cutscene_flags"):
            ob.tag_cutscene_flag.name = element.name

        elif ob_parent_name.startswith("cutscene_cameras"):
            ob.tag_cutscene_camera.name = element.name

def generate_skies(context, level_root, H1_ASSET, report):
    asset_collection = get_referenced_collection("Skies", context.scene.collection, False)
    for element_idx, element in enumerate(H1_ASSET.skies):
        ASSET = parse_tag(element, report, "halo1", "retail")
        tag_name = os.path.basename(element.name)
        sky_collection = get_referenced_collection("%s_%s" % (tag_name, element_idx), asset_collection, False)
        if not ASSET == None:
            for light_idx, light in enumerate(ASSET.lights):


                name = "%s_light_%s" % (tag_name, light_idx)
                light_data = bpy.data.lights.new(name, "SUN")
                ob = bpy.data.objects.new(name, light_data)

                ob.data.color = (light.color[0], light.color[1], light.color[2])
                ob.data.energy = light.power
                ob.parent = level_root

                ob.rotation_euler = get_rotation_euler(*light.direction)

                sky_collection.objects.link(ob)

        sky_collection.tag_sky.sky_path = get_tag_display(element)

def generate_comments(context, level_root, H1_ASSET):
    comment_collection = bpy.data.collections.get("Comments")
    if comment_collection == None:
        comment_collection = bpy.data.collections.new("Comments")
        context.scene.collection.children.link(comment_collection)

    comment_layer_collection = context.view_layer.layer_collection.children[comment_collection.name]
    context.view_layer.active_layer_collection = comment_layer_collection
    context.view_layer.active_layer_collection.hide_viewport = True
    comment_collection.hide_render = True

    for comment_idx, comment_element in enumerate(H1_ASSET.comments):
        font = bpy.data.curves.new(type="FONT", name="comment")
        font_ob = bpy.data.objects.new("comment_%s" % comment_idx, font)
        font_ob.data.body = comment_element.text

        font_ob.parent = level_root
        font_ob.location = comment_element.position * 100
        comment_collection.objects.link(font_ob)

def generate_object_elements(context, level_root, collection_name, H1_ASSET, game_version, file_version, fix_rotations, report, random_color_gen):
    objects_list = []
    asset_collection = bpy.data.collections.get(collection_name)
    if asset_collection == None:
        asset_collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(asset_collection)

    tag_block = None
    tag_palette = None
    if collection_name == "Scenery":
        asset_collection.hide_render = False
        tag_block = H1_ASSET.scenery
        tag_palette = H1_ASSET.scenery_palette
    elif collection_name == "Bipeds":
        asset_collection.hide_render = True
        tag_block = H1_ASSET.bipeds
        tag_palette = H1_ASSET.biped_palette
    elif collection_name == "Vehicles":
        asset_collection.hide_render = True
        tag_block = H1_ASSET.vehicles
        tag_palette = H1_ASSET.vehicle_palette
    elif collection_name == "Equipment":
        asset_collection.hide_render = True
        tag_block = H1_ASSET.equipment
        tag_palette = H1_ASSET.equipment_palette
    elif collection_name == "Weapons":
        asset_collection.hide_render = True
        tag_block = H1_ASSET.weapons
        tag_palette = H1_ASSET.weapon_palette
    elif collection_name == "Machines":
        asset_collection.hide_render = True
        tag_block = H1_ASSET.device_machines
        tag_palette = H1_ASSET.device_machine_palette
    elif collection_name == "Controls":
        asset_collection.hide_render = True
        tag_block = H1_ASSET.device_controls
        tag_palette = H1_ASSET.device_control_palette
    elif collection_name == "Light Fixtures":
        asset_collection.hide_render = True
        tag_block = H1_ASSET.device_light_fixtures
        tag_palette = H1_ASSET.device_light_fixtures_palette
    elif collection_name == "Sound Scenery":
        asset_collection.hide_render = True
        tag_block = H1_ASSET.sound_scenery
        tag_palette = H1_ASSET.sound_scenery_palette

    for palette_idx, palette_element in enumerate(tag_palette):
        ob = None
        object_name = "temp_%s_%s" % (os.path.basename(palette_element.name), palette_idx)
        ASSET = parse_tag(palette_element, report, "halo1", "retail")
        if not ASSET == None:
            if collection_name == "Scenery":
                MODEL = parse_tag(ASSET.model, report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, random_color_gen, report)
            elif collection_name == "Bipeds":
                MODEL = parse_tag(ASSET.model, report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, random_color_gen, report)
            elif collection_name == "Vehicles":
                MODEL = parse_tag(ASSET.model, report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, random_color_gen, report)
            elif collection_name == "Equipment":
                MODEL = parse_tag(ASSET.model, report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, random_color_gen, report)
            elif collection_name == "Weapons":
                MODEL = parse_tag(ASSET.model, report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, random_color_gen, report)
            elif collection_name == "Machines":
                MODEL = parse_tag(ASSET.model, report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, random_color_gen, report)
            elif collection_name == "Controls":
                MODEL = parse_tag(ASSET.model, report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, random_color_gen, report)
            elif collection_name == "Light Fixtures":
                MODEL = parse_tag(ASSET.model, report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, random_color_gen, report)
            elif collection_name == "Sound Scenery":
                MODEL = parse_tag(ASSET.model, report, "halo1", "retail")
                if not MODEL == None:
                    ob = get_object(asset_collection, MODEL, game_version, object_name, random_color_gen, report)

        objects_list.append(ob)

    for element_idx, element in enumerate(tag_block):
        tag_path = ""
        ob = None
        if element.type_index >= 0:
            pallete_item = tag_palette[element.type_index]
            ob = objects_list[element.type_index]
            tag_path_no_ext = pallete_item.name
            tag_path = "%s.%s" % (pallete_item.name, h1_tag_groups_dic.get(pallete_item.tag_group))

        tag_name = "NONE"
        if not global_functions.string_empty_check(tag_path_no_ext):
            tag_name = os.path.basename(tag_path_no_ext)

        name = "%s_%s" % (tag_name, element_idx)
        if not ob == None:
            root = bpy.data.objects.new(name, ob.data)
            asset_collection.objects.link(root)

        else:
            root = bpy.data.objects.new(name, None)
            root.empty_display_type = 'ARROWS'
            asset_collection.objects.link(root)

        root.parent = level_root
        root.location = element.position * 100

        get_data_type(root, asset_collection, element, H1_ASSET, tag_path)

        root.rotation_euler = get_rotation_euler(*element.rotation)

        if collection_name == "Scenery" and ObjectFlags.automatically in ObjectFlags(element.placement_flags):
            root.hide_set(True)
            root.hide_render = True

    for ob in objects_list:
        if not ob == None:
            bpy.data.objects.remove(ob, do_unlink=True)

def generate_netgame_equipment_elements(context, level_root, H1_ASSET, game_version, file_version, fix_rotations, report, random_color_gen):
    asset_collection = bpy.data.collections.get("Netgame Equipment")
    if asset_collection == None:
        asset_collection = bpy.data.collections.new("Netgame Equipment")
        context.scene.collection.children.link(asset_collection)

    asset_collection.hide_render = True
    for element_idx, element in enumerate(H1_ASSET.netgame_equipment):
        ob = None
        tag_path_no_ext = element.item_collection.name
        tag_path = "%s.%s" % (element.item_collection.name, h1_tag_groups_dic.get(element.item_collection.tag_group))

        tag_name = "NONE"
        if not global_functions.string_empty_check(tag_path_no_ext):
            tag_name = os.path.basename(tag_path_no_ext)

        object_name = "%s_%s" % (tag_name, element_idx)
        ASSET = parse_tag(element.item_collection, report, "halo1", "retail")
        if not ASSET == None:
            if len(ASSET.item_permutations) > 0:
                item_perutation_element = ASSET.item_permutations[0]
                ITEM = parse_tag(item_perutation_element.item, report, "halo1", "retail")
                if item_perutation_element.item.tag_group == "eqip":
                    MODEL = parse_tag(ITEM.model, report, "halo1", "retail")
                    if not MODEL == None:
                        ob = get_object(asset_collection, MODEL, game_version, object_name, random_color_gen, report)
                elif item_perutation_element.item.tag_group == "weap":
                    MODEL = parse_tag(ITEM.model, report, "halo1", "retail")
                    if not MODEL == None:
                        ob = get_object(asset_collection, MODEL, game_version, object_name, random_color_gen, report)

        if ob == None:
            ob = bpy.data.objects.new(object_name, None)
            ob.empty_display_type = 'ARROWS'
            asset_collection.objects.link(ob)

        get_data_type(ob, asset_collection, element, H1_ASSET, tag_path)

        ob.parent = level_root
        ob.location = element.position * 100
        ob.rotation_euler = (radians(0.0), radians(0.0), radians(element.facing))

def generate_encounters(context, level_root, H1_ASSET):
    collection_name = "Encounters"

    asset_collection = get_referenced_collection(collection_name, context.scene.collection, True)
    for encounter_idx, encounter in enumerate(H1_ASSET.encounters):
        block_indices = (encounter_idx)
        encounter_coll_name = "%s_e%s" % (encounter.name, encounter_idx)
        encounter_element_id = "e%s" % (encounter_idx)

        squads_coll_name = "Squads_e%s" % encounter_idx
        platoons_coll_name = "Platoons_e%s" % encounter_idx

        encounter_collection = get_referenced_collection(encounter_coll_name, asset_collection, True)
        get_data_type(encounter_collection, asset_collection, encounter, H1_ASSET, block_indices=block_indices)

        s_e_collection = get_referenced_collection(squads_coll_name, encounter_collection, True)
        p_e_collection = get_referenced_collection(platoons_coll_name, encounter_collection, True)
        for squad_idx, squad in  enumerate(encounter.squads):
            block_indices = (encounter_idx, squad_idx)

            squad_coll_name = "%s_e%ss%s" % (squad.name, encounter_idx, squad_idx)
            squad_element_id = "e%ss%s" % (encounter_idx, squad_idx)

            squad_collection = get_referenced_collection(squad_coll_name, s_e_collection, True)
            get_data_type(squad_collection, s_e_collection, squad, H1_ASSET, block_indices=block_indices)

            generate_encounter_obs(context, level_root, "Move Positions", squad_collection, squad_element_id, H1_ASSET, block_indices)
            generate_encounter_obs(context, level_root, "Starting Locations", squad_collection, squad_element_id, H1_ASSET, block_indices)

        for platoon_idx, platoon in enumerate(encounter.platoons):
            platoon_coll_name = "%s_e%sp%s" % (platoon.name, encounter_idx, platoon_idx)
            platoon_collection = get_referenced_collection(platoon_coll_name, p_e_collection, True)
            get_data_type(platoon_collection, p_e_collection, platoon, H1_ASSET, block_indices=block_indices)

        generate_encounter_obs(context, level_root, "Firing Points", encounter_collection, encounter_element_id, H1_ASSET, block_indices)
        generate_encounter_obs(context, level_root, "Player Starting Locations", encounter_collection, encounter_element_id, H1_ASSET, block_indices)

def generate_encounter_obs(context, level_root, collection_name, parent_collection, element_id, H1_ASSET, block_indices=()):
    unique_collection_name = "%s_%s" % (collection_name, element_id)

    asset_collection = get_referenced_collection(unique_collection_name, parent_collection, True)

    tag_block = None
    tag_palette = None
    if collection_name == "Move Positions":
        asset_collection.hide_render = False
        tag_block = H1_ASSET.encounters[block_indices[0]].squads[block_indices[1]].move_positions
    elif collection_name == "Starting Locations":
        tag_block = H1_ASSET.encounters[block_indices[0]].squads[block_indices[1]].starting_locations
        tag_palette = H1_ASSET.actor_palette 
    elif collection_name == "Firing Points":
        tag_block = H1_ASSET.encounters[block_indices[0]].firing_positions
    elif collection_name == "Player Starting Locations":
        tag_block = H1_ASSET.encounters[block_indices[0]].player_starting_locations

    for element_idx, element in enumerate(tag_block):
        tag_name = unique_collection_name

        ob = bpy.data.objects.new("%s_%s" % (tag_name, element_idx), None)

        ob.empty_display_type = 'ARROWS'
        ob.parent = level_root
        ob.location = element.position * 100
        if not collection_name == "Firing Points":
            ob.rotation_euler = (radians(0.0), radians(0.0), radians(element.facing))

        get_data_type(ob, asset_collection, element, H1_ASSET)

        asset_collection.objects.link(ob)

def generate_command_lists(context, level_root, H1_ASSET):
    collection_name = "Command Lists"

    asset_collection = get_referenced_collection(collection_name, context.scene.collection, True)
    for command_list_idx, command_list in enumerate(H1_ASSET.command_lists):
        block_indices = (command_list_idx)
        command_list_name = "%s_cl%s" % (command_list.name, command_list_idx)
        commands_coll_name = "Commands_cl%s" % command_list_idx
        points_coll_name = "Points_cl%s" % command_list_idx

        command_list_collection = get_referenced_collection(command_list_name, asset_collection, True)
        get_data_type(command_list_collection, asset_collection, command_list, H1_ASSET, block_indices=block_indices)

        c_cl_collection = get_referenced_collection(commands_coll_name, command_list_collection, True)
        p_cl_collection = get_referenced_collection(points_coll_name, command_list_collection, True)
        for command_idx, command in  enumerate(command_list.commands):
            block_indices = (command_list_idx, command_idx)

            command_coll_name = "%s_cl%sc%s" % ("command", command_list_idx, command_idx)

            command_collection = get_referenced_collection(command_coll_name, c_cl_collection, True)
            get_data_type(command_collection, c_cl_collection, command, H1_ASSET, block_indices=block_indices)

        for point_idx, point in enumerate(command_list.points):
            point_ob = get_point(block_indices, point_idx, H1_ASSET.command_lists[block_indices[0]].points, level_root)

def generate_empties(context, level_root, collection_name, H1_ASSET, parent_collection):
    asset_collection = get_referenced_collection(collection_name, parent_collection, True)

    tag_block = None
    if collection_name == "Player Starting Locations":
        tag_block = H1_ASSET.player_starting_locations
    elif collection_name == "Netgame Flags":
        tag_block = H1_ASSET.netgame_flags

    for element_idx, element in enumerate(tag_block):
        tag_name = collection_name
        tag_path = ""
        if collection_name == "Netgame Flags":
            tag_path_no_ext = element.weapon_group.name
            tag_path = "%s.%s" % (element.weapon_group.name, h1_tag_groups_dic.get(element.weapon_group.tag_group))

            tag_name = collection_name
            if not global_functions.string_empty_check(tag_path_no_ext):
                tag_name = os.path.basename(tag_path_no_ext)

        ob = bpy.data.objects.new("%s_%s" % (tag_name, element_idx), None)

        ob.empty_display_type = 'ARROWS'
        ob.parent = level_root
        ob.location = element.position * 100
        if not collection_name.startswith("Firing Points"):
            ob.rotation_euler = (radians(0.0), radians(0.0), radians(element.facing))

        get_data_type(ob, asset_collection, element, H1_ASSET, tag_path)

        asset_collection.objects.link(ob)

def generate_camera_flags(context, level_root, H1_ASSET):
    collection_name = "Cutscene Flags"
    asset_collection = get_referenced_collection(collection_name, context.scene.collection, True)
    for element_idx, element in enumerate(H1_ASSET.cutscene_flags):
        ob = bpy.data.objects.new(element.name, None)

        ob.empty_display_type = 'ARROWS'
        ob.parent = level_root
        ob.location = element.position * 100

        ob.rotation_euler = get_rotation_euler(*element.facing)

        get_data_type(ob, asset_collection, element, H1_ASSET)

        asset_collection.objects.link(ob)

def generate_camera_points(context, level_root, H1_ASSET):
    collection_name = "Cutscene Cameras"

    asset_collection = get_referenced_collection(collection_name, context.scene.collection, True)
    for element_idx, element in enumerate(H1_ASSET.cutscene_camera_points):
        camera_data = bpy.data.cameras.new(name='Camera')
        ob = bpy.data.objects.new(element.name, camera_data)

        ob.parent = level_root
        ob.location = element.position * 100

        ob.data.lens_unit = 'FOV'
        ob.data.angle = radians(element.field_of_view)

        ob.rotation_euler = get_rotation_euler(*element.orientation)
        ob.rotation_euler.rotate_axis("X", radians(90.0))
        ob.rotation_euler.rotate_axis("Y", radians(-90.0))

        get_data_type(ob, asset_collection, element, H1_ASSET)

        asset_collection.objects.link(ob)

def generate_trigger_volumes(context, level_root, H1_ASSET):
    collection_name = "Trigger Volumes"

    asset_collection = get_referenced_collection(collection_name, context.scene.collection, True)
    for element_idx, element in enumerate(H1_ASSET.trigger_volumes):
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

def generate_decals(context, level_root, H1_ASSET):
    collection_name = "Decals"
    asset_collection = get_referenced_collection(collection_name, context.scene.collection, True)
    for element_idx, element in enumerate(H1_ASSET.decals): 
        tag_name = "decal"
        tag_path = ""
        if element.palette_index >= 0 and len(H1_ASSET.decal_palette) > element.palette_index:
            tag_ref = H1_ASSET.decal_palette[element.palette_index]
            tag_name = os.path.basename(tag_ref.name)
            tag_path_no_ext = tag_ref.name
            tag_path = "%s.%s" % (tag_ref.name, h1_tag_groups_dic.get(tag_ref.tag_group))

        mesh = bpy.data.meshes.new("part_%s" % element_idx)
        ob = bpy.data.objects.new("%s_%s" % (tag_name, element_idx), mesh)
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
        ob.location = element.position * 100
        ob.rotation_euler = get_decal_rotation_euler(element.yaw, element.pitch)

        get_data_type(ob, asset_collection, element, H1_ASSET, tag_path)

def generate_scenario_scene(context, H1_ASSET, game_version, game_title, file_version, fix_rotations, empty_markers, report):
    random_color_gen = global_functions.RandomColorGenerator() # generates a random sequence of colors
    levels_collection = get_referenced_collection("BSPs", context.scene.collection, False)
    for bsp_idx, bsp in enumerate(H1_ASSET.structure_bsps):
        ASSET = parse_tag(bsp, report, "halo1", "retail")
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

    for object_name in H1_ASSET.object_names:
        if not global_functions.string_empty_check(object_name):
            context.scene.object_name_add(object_name)

    tag_references = set()
    if not global_functions.string_empty_check(H1_ASSET.dont_use_tag_ref.name):
        tag_references.add((H1_ASSET.dont_use_tag_ref.name, H1_ASSET.dont_use_tag_ref.tag_group))
    if not global_functions.string_empty_check(H1_ASSET.wont_use_tag_ref.name):
        tag_references.add((H1_ASSET.wont_use_tag_ref.name, H1_ASSET.wont_use_tag_ref.tag_group))
    if not global_functions.string_empty_check(H1_ASSET.cant_use_tag_ref.name):
        tag_references.add((H1_ASSET.cant_use_tag_ref.name, H1_ASSET.cant_use_tag_ref.tag_group))
    for sky_element in H1_ASSET.skies:
        if not global_functions.string_empty_check(sky_element.name):
            tag_references.add((sky_element.name, sky_element.tag_group))
    for scenery_element in H1_ASSET.scenery_palette:
        if not global_functions.string_empty_check(scenery_element.name):
            tag_references.add((scenery_element.name, scenery_element.tag_group))
    for biped_element in H1_ASSET.biped_palette:
        if not global_functions.string_empty_check(biped_element.name):
            tag_references.add((biped_element.name, biped_element.tag_group))
    for vehicle_element in H1_ASSET.vehicle_palette:
        if not global_functions.string_empty_check(vehicle_element.name):
            tag_references.add((vehicle_element.name, vehicle_element.tag_group))
    for equipment_element in H1_ASSET.equipment_palette:
        if not global_functions.string_empty_check(equipment_element.name):
            tag_references.add((equipment_element.name, equipment_element.tag_group))
    for weapon_element in H1_ASSET.weapon_palette:
        if not global_functions.string_empty_check(weapon_element.name):
            tag_references.add((weapon_element.name, weapon_element.tag_group))
    for machine_element in H1_ASSET.device_machine_palette:
        if not global_functions.string_empty_check(machine_element.name):
            tag_references.add((machine_element.name, machine_element.tag_group))
    for control_element in H1_ASSET.device_control_palette:
        if not global_functions.string_empty_check(control_element.name):
            tag_references.add((control_element.name, control_element.tag_group))
    for light_element in H1_ASSET.device_light_fixtures_palette:
        if not global_functions.string_empty_check(light_element.name):
            tag_references.add((light_element.name, light_element.tag_group))
    for sound_element in H1_ASSET.sound_scenery_palette:
        if not global_functions.string_empty_check(sound_element.name):
            tag_references.add((sound_element.name, sound_element.tag_group))
    for flag_element in H1_ASSET.netgame_flags:
        if not global_functions.string_empty_check(flag_element.weapon_group.name):
            tag_references.add((flag_element.weapon_group.name, flag_element.weapon_group.tag_group))
    for netgame_equipment_element in H1_ASSET.netgame_equipment:
        if not global_functions.string_empty_check(netgame_equipment_element.item_collection.name):
            tag_references.add((netgame_equipment_element.item_collection.name, netgame_equipment_element.item_collection.tag_group))
    for decal_palette_element in H1_ASSET.decal_palette:
        if not global_functions.string_empty_check(decal_palette_element.name):
            tag_references.add((decal_palette_element.name, decal_palette_element.tag_group))
    for actor_element in H1_ASSET.actor_palette:
        if not global_functions.string_empty_check(actor_element.name):
            tag_references.add((actor_element.name, actor_element.tag_group))
    if not global_functions.string_empty_check(H1_ASSET.custom_object_names_tag_ref.name):
        tag_references.add((H1_ASSET.custom_object_names_tag_ref.name, H1_ASSET.custom_object_names_tag_ref.tag_group))
    if not global_functions.string_empty_check(H1_ASSET.chapter_title_text_tag_ref.name):
        tag_references.add((H1_ASSET.chapter_title_text_tag_ref.name, H1_ASSET.chapter_title_text_tag_ref.tag_group))
    if not global_functions.string_empty_check(H1_ASSET.hud_messages_tag_ref.name):
        tag_references.add((H1_ASSET.hud_messages_tag_ref.name, H1_ASSET.hud_messages_tag_ref.tag_group))

    for tag_reference in tag_references:
        tag_path, tag_group = tag_reference
        context.scene.tag_add(tag_path=tag_path, tag_group=tag_group)

    set_scenario_data(context, H1_ASSET)

    if len(H1_ASSET.skies) > 0:
        generate_skies(context, level_root, H1_ASSET, report)
    if len(H1_ASSET.comments) > 0:
        generate_comments(context, level_root, H1_ASSET)
    if len(H1_ASSET.scenery) > 0:
        generate_object_elements(context, level_root, "Scenery", H1_ASSET, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H1_ASSET.bipeds) > 0:
        generate_object_elements(context, level_root, "Bipeds", H1_ASSET, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H1_ASSET.vehicles) > 0:
        generate_object_elements(context, level_root, "Vehicles", H1_ASSET, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H1_ASSET.equipment) > 0:
        generate_object_elements(context, level_root, "Equipment", H1_ASSET, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H1_ASSET.weapons) > 0:
        generate_object_elements(context, level_root, "Weapons", H1_ASSET, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H1_ASSET.device_machines) > 0:
        generate_object_elements(context, level_root, "Machines", H1_ASSET, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H1_ASSET.device_controls) > 0:
        generate_object_elements(context, level_root, "Controls", H1_ASSET, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H1_ASSET.device_light_fixtures) > 0:
        generate_object_elements(context, level_root, "Light Fixtures", H1_ASSET, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H1_ASSET.sound_scenery) > 0:
        generate_object_elements(context, level_root, "Sound Scenery", H1_ASSET, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H1_ASSET.player_starting_locations) > 0:
        generate_empties(context, level_root, "Player Starting Locations", H1_ASSET, context.scene.collection)
    if len(H1_ASSET.netgame_flags) > 0:
        generate_empties(context, level_root, "Netgame Flags", H1_ASSET, context.scene.collection)
    if len(H1_ASSET.netgame_equipment) > 0:
        generate_netgame_equipment_elements(context, level_root, H1_ASSET, game_version, file_version, fix_rotations, report, random_color_gen)
    if len(H1_ASSET.trigger_volumes) > 0:
        generate_trigger_volumes(context, level_root, H1_ASSET)
    if len(H1_ASSET.decals) > 0:
        generate_decals(context, level_root, H1_ASSET)
    if len(H1_ASSET.command_lists) > 0:
        generate_command_lists(context, level_root, H1_ASSET)
    if len(H1_ASSET.encounters) > 0:
        generate_encounters(context, level_root, H1_ASSET)
    if len(H1_ASSET.cutscene_flags) > 0:
        generate_camera_flags(context, level_root, H1_ASSET)
    if len(H1_ASSET.cutscene_camera_points) > 0:
        generate_camera_points(context, level_root, H1_ASSET)
