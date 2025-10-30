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
import struct
import random

from ....global_functions.parse_tags import parse_tag
from ....global_functions import tag_format, global_functions
from ....file_tag.h2.file_scenario.process_file import process_file as process_h2_scenario
from .format import (
        ScenarioTypeEnum as H1ScenarioTypeEnum,
        ScenarioFlags as H1ScenarioFlags,
        ResourceTypeEnum as H1ResourceTypeEnum,
        FunctionFlags as H1FunctionFlags,
        FunctionEnum as H1FunctionEnum,
        MapEnum as H1MapEnum,
        BoundsModeEnum as H1BoundsModeEnum,
        ObjectFlags as H1ObjectFlags,
        UnitFlags as H1UnitFlags,
        VehicleFlags as H1VehicleFlags,
        ItemFlags as H1ItemFlags,
        DeviceGroupFlags as H1DeviceGroupFlags,
        DeviceFlags as H1DeviceFlags,
        MachineFlags as H1MachineFlags,
        ControlFlags as H1ControlFlags,
        GametypeEnum as H1GametypeEnum,
        NetGameEnum as H1NetGameEnum,
        NetGameEquipment as H1NetGameEquipment,
        StartingEquipment as H1StartingEquipment,
        EncounterFlags as H1EncounterFlags,
        TeamEnum as H1TeamEnum,
        SearchBehaviorEnum as H1SearchBehaviorEnum,
        GroupEnum as H1GroupEnum,
        PlatoonFlags as H1PlatoonFlags,
        PlatoonStrengthEnum as H1PlatoonStrengthEnum,
        StateEnum as H1StateEnum,
        SquadFlags as H1SquadFlags,
        LeaderEnum as H1LeaderEnum,
        GroupFlags as H1GroupFlags,
        MajorUpgradeEnum as H1MajorUpgradeEnum
        )

from ...h2.file_scenario.format import (
        ScenarioAsset,
        ScenarioTypeEnum,
        ScenarioFlags,
        ResourceTypeEnum,
        FunctionFlags,
        FunctionEnum,
        MapEnum,
        BoundsModeEnum,
        ObjectFlags,
        TeamDesignatorEnum,
        GametypeEnum,
        NetGameEnum,
        NetGameFlags,
        RespawnTimerStartsEnum,
        ClassificationEnum,
        StartingEquipment,
        PathfindingPolicyEnum,
        LightmappingPolicyEnum,
        SALT_SIZE
        )

DEBUG_PARSER = True
DEBUG_HEADER = True
DEBUG_BODY = True

UNIQUE_ID = random.randint(0, 100000)

def tag_block_header(TAG, header_group, version, count, size):
    TAGBLOCKHEADER = TAG.TagBlockHeader()
    TAGBLOCKHEADER.name = header_group
    TAGBLOCKHEADER.version = version
    TAGBLOCKHEADER.count = count
    TAGBLOCKHEADER.size = size

    return TAGBLOCKHEADER

def get_id():
    global UNIQUE_ID
    UNIQUE_ID += 1

    return UNIQUE_ID

def convert_scenario_flags(scenario_flags):
    flags = 0
    active_h1_flags = [flag.name for flag in H1ScenarioFlags if flag in H1ScenarioFlags(scenario_flags)]
    if "cortana_hack" in active_h1_flags:
        flags += ScenarioFlags.cortana_hack.value

    return flags

def convert_object_flags(object_flags):
    flags = 0
    active_h1_flags = [flag.name for flag in H1ObjectFlags if flag in H1ObjectFlags(object_flags)]
    if "automatically" in active_h1_flags:
        flags += ObjectFlags.not_automatically.value

    return flags

def convert_game_type_setting(game_type_index):
    h2_gametype_index = 0
    h1_gametype = H1GametypeEnum(game_type_index)
    if h1_gametype == H1GametypeEnum.none:
        h2_gametype_index = GametypeEnum.none.value
    elif h1_gametype == H1GametypeEnum.ctf:
        h2_gametype_index = GametypeEnum.ctf.value
    elif h1_gametype == H1GametypeEnum.slayer:
        h2_gametype_index = GametypeEnum.slayer.value
    elif h1_gametype == H1GametypeEnum.oddball:
        h2_gametype_index = GametypeEnum.oddball.value
    elif h1_gametype == H1GametypeEnum.king_of_the_hill:
        h2_gametype_index = GametypeEnum.king_of_the_hill.value
    elif h1_gametype == H1GametypeEnum.race:
        h2_gametype_index = GametypeEnum.race.value
    elif h1_gametype == H1GametypeEnum.terminator:
        h2_gametype_index = GametypeEnum.ignored1.value
    elif h1_gametype == H1GametypeEnum.stub:
        h2_gametype_index = GametypeEnum.stub.value
    elif h1_gametype == H1GametypeEnum.ignored1:
        h2_gametype_index = GametypeEnum.ignored1.value
    elif h1_gametype == H1GametypeEnum.ignored2:
        h2_gametype_index = GametypeEnum.ignored1.value
    elif h1_gametype == H1GametypeEnum.ignored3:
        h2_gametype_index = GametypeEnum.ignored1.value
    elif h1_gametype == H1GametypeEnum.ignored4:
        h2_gametype_index = GametypeEnum.ignored1.value
    elif h1_gametype == H1GametypeEnum.all_games:
        h2_gametype_index = GametypeEnum.all_games.value
    elif h1_gametype == H1GametypeEnum.all_except_ctf:
        h2_gametype_index = GametypeEnum.all_except_ctf.value
    elif h1_gametype == H1GametypeEnum.all_except_race_and_ctf:
        h2_gametype_index = GametypeEnum.all_except_race_and_ctf.value

    return h2_gametype_index

def convert_netgame_flag_type(type_index, usage_id, hill_identifiers):
    is_valid = True
    needs_return = False
    flag_type = 0
    team_designator = TeamDesignatorEnum.neutral.value
    identifer = 0
    flags = 0

    if H1NetGameEnum(type_index) == H1NetGameEnum.ctf_flag:
        flag_type = NetGameEnum.ctf_flag_spawn.value
        flags = NetGameFlags.multi_flag_bomb.value + NetGameFlags.single_flag_bomb.value
        if not usage_id > 1:
            team_designator = usage_id
            needs_return = True

        else:
            is_valid = False

    elif H1NetGameEnum(type_index) == H1NetGameEnum.unused1:
        flag_type = NetGameEnum.unused.value

    elif H1NetGameEnum(type_index) == H1NetGameEnum.oddball_ball_spawn:
        flag_type = NetGameEnum.oddball_spawn.value

    elif H1NetGameEnum(type_index) == H1NetGameEnum.race_track:
        flag_type = NetGameEnum.race_checkpoint.value

    elif H1NetGameEnum(type_index) == H1NetGameEnum.race_vehicle:
        flag_type = NetGameEnum.unused.value

    elif H1NetGameEnum(type_index) == H1NetGameEnum.unused5:
        flag_type = NetGameEnum.unused.value

    elif H1NetGameEnum(type_index) == H1NetGameEnum.teleport_from:
        flag_type = NetGameEnum.teleporter_src.value
        identifer = usage_id

    elif H1NetGameEnum(type_index) == H1NetGameEnum.teleport_to:
        flag_type = NetGameEnum.teleporter_dest.value
        identifer = usage_id

    elif H1NetGameEnum(type_index) == H1NetGameEnum.hill_flag:
        if not len(hill_identifiers) > 8 or usage_id in hill_identifiers:
            if not usage_id in hill_identifiers:
                hill_identifiers.append(usage_id)
            hill_index = hill_identifiers.index(usage_id)
            if hill_index == 0:
                flag_type = NetGameEnum.king_of_the_hill_0.value

            elif hill_index == 1:
                flag_type = NetGameEnum.king_of_the_hill_1.value

            elif hill_index == 2:
                flag_type = NetGameEnum.king_of_the_hill_2.value

            elif hill_index == 3:
                flag_type = NetGameEnum.king_of_the_hill_3.value

            elif hill_index == 4:
                flag_type = NetGameEnum.king_of_the_hill_4.value

            elif hill_index == 5:
                flag_type = NetGameEnum.king_of_the_hill_5.value

            elif hill_index == 6:
                flag_type = NetGameEnum.king_of_the_hill_6.value

            elif hill_index == 7:
                flag_type = NetGameEnum.king_of_the_hill_7.value

        else:
            print("Map has more than 8 hills. Hill %s is now sleeping with the fishes" % usage_id)
            flag_type = NetGameEnum.king_of_the_hill_0.value
            is_valid = False

    return flag_type, team_designator, identifer, flags, is_valid, needs_return

def get_item_stats(collection_name):
    classification = 0
    spawn_time = 0
    respawn_on_empty_time = 15
    respawn_timer_starts = RespawnTimerStartsEnum.on_pick_up.value
    if "grenade" in collection_name:
        classification = ClassificationEnum.grenade.value
        respawn_on_empty_time = 0

    elif "powerups" in collection_name:
        classification = ClassificationEnum.powerup.value
        respawn_on_empty_time = 0
        respawn_timer_starts = RespawnTimerStartsEnum.on_body_depletion.value

    elif "vehicles" in collection_name:
        classification = ClassificationEnum.primary_light_land.value
        spawn_time = 75
        respawn_on_empty_time = 90
        respawn_timer_starts = RespawnTimerStartsEnum.on_body_depletion.value
        if "ghost" in collection_name:
            classification = ClassificationEnum.secondary_light_land.value
            spawn_time = 50
        elif "scorpion" in collection_name:
            classification = ClassificationEnum.primary_heavy_land.value
            spawn_time = 100
            respawn_on_empty_time = 160
        elif "banshee" in collection_name:
            classification = ClassificationEnum.primary_flying.value
            spawn_time = 110
            respawn_on_empty_time = 90

        elif "turret" in collection_name: # We are assuming all turrets are Covenant cause that's all there is in the H1 sandbox
            classification = ClassificationEnum.secondary_turret.value
            spawn_time = 100
            respawn_on_empty_time = 120

    return spawn_time, respawn_on_empty_time, respawn_timer_starts, classification

def get_vehicle_gametypes(vehicle_multiplayer_spawn_flags):
    type0 = GametypeEnum.none.value
    type1 = GametypeEnum.none.value
    type2 = GametypeEnum.none.value
    type3 = GametypeEnum.none.value
    active_h1_flags = H1VehicleFlags(vehicle_multiplayer_spawn_flags)
    if (H1VehicleFlags.ctf_allowed and H1VehicleFlags.king_allowed and H1VehicleFlags.oddball_allowed and H1VehicleFlags.slayer_allowed) in active_h1_flags:
        type0 = GametypeEnum.all_games.value

    return type0, type1, type2, type3

def convert_starting_equipment_flags(starting_equipment_flags):
    flags = 0
    active_h1_flags = [flag.name for flag in H1StartingEquipment if flag in H1StartingEquipment(starting_equipment_flags)]
    if "no_grenades" in active_h1_flags:
        flags += StartingEquipment.no_grenades.value

    if "plasma_grenades_only" in active_h1_flags:
        flags += StartingEquipment.plasma_grenades.value

    return flags

def get_comments(comments_tag_block, TAG, SCENARIO):
    SCENARIO.comments = []
    for comment_idx, comment_element in enumerate(comments_tag_block):
        comment = SCENARIO.Comment()
        comment.position = comment_element.position
        comment.type = 0
        comment.name = "comment %s" % comment_idx
        comment.comment = comment_element.text

        SCENARIO.comments.append(comment)

    SCENARIO.comment_header = TAG.TagBlockHeader("tbfd", 0, len(SCENARIO.comments), 304)

def get_object_names(object_names_tag_block, TAG, SCENARIO):
    SCENARIO.object_names = []
    for object_name_element in object_names_tag_block:
        object_name = SCENARIO.ObjectName()
        object_name.name = object_name_element
        object_name.object_type = -1
        object_name.placement_index = -1

        SCENARIO.object_names.append(object_name)

    SCENARIO.object_name_header = TAG.TagBlockHeader("tbfd", 0, len(SCENARIO.object_names), 36)

def get_scenery(H1_ASSET, TAG, SCENARIO, bsp_bounds_list):
    for scenery_element in H1_ASSET.scenery:
        palette_index = -1
        if scenery_element.type_index >= 0:
            palette_entry = H1_ASSET.scenery_palette[scenery_element.type_index]
            palette_index = find_tag_ref(TAG, SCENARIO.scenery_palette, palette_entry.name, palette_entry.tag_group) 

        scenery = SCENARIO.Scenery()

        scenery.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        scenery.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        scenery.sper_header = TAG.TagBlockHeader("sper", 0, 1, 24)
        scenery.sct3_header = TAG.TagBlockHeader("sct3", 0, 1, 20)

        scenery.palette_index = palette_index
        scenery.name_index = scenery_element.name_index
        scenery.placement_flags = convert_object_flags(scenery_element.placement_flags)
        scenery.position = scenery_element.position
        scenery.rotation = scenery_element.rotation
        scenery.scale = 0
        scenery.transform_flags = 0
        scenery.manual_bsp_flags = 0
        scenery.unique_id = get_id()
        scenery.origin_bsp_index = global_functions.get_origin_bsp(bsp_bounds_list, scenery)
        scenery.object_type = 6
        scenery.source = 1
        scenery.bsp_policy = 0
        scenery.editor_folder_index = -1

        scenery.variant_name = ""
        scenery.variant_name_length = len(scenery.variant_name)
        scenery.active_change_colors = 0
        scenery.primary_color_BGRA = (0, 0, 0, 255)
        scenery.secondary_color_BGRA = (0, 0, 0, 255)
        scenery.tertiary_color_BGRA = (0, 0, 0, 255)
        scenery.quaternary_color_BGRA = (0, 0, 0, 255)
        scenery.pathfinding_policy = PathfindingPolicyEnum.tag_default.value
        scenery.lightmap_policy = LightmappingPolicyEnum.tag_default.value
        scenery.valid_multiplayer_games = 0

        scenery.pathfinding_references = []
        pathfinding_ref_count = len(scenery.pathfinding_references)
        scenery.pathfinding_references_header = TAG.TagBlockHeader("tbfd", 0, pathfinding_ref_count, 4)
        scenery.pathfinding_references_tag_block = TAG.TagBlock(pathfinding_ref_count)

        SCENARIO.scenery.append(scenery)

    SCENARIO.scenery_header = TAG.TagBlockHeader("tbfd", 4, len(SCENARIO.scenery), 96)

def get_unit(H1_ASSET, TAG, SCENARIO, is_biped, bsp_bounds_list):
    h1_unit_tag_block =  H1_ASSET.vehicles
    h1_unit_palette = H1_ASSET.vehicle_palette
    h2_unit_tag_block = SCENARIO.vehicles
    if is_biped:
        h1_unit_tag_block =  H1_ASSET.bipeds
        h1_unit_palette = H1_ASSET.biped_palette
        h2_unit_tag_block = SCENARIO.bipeds

    for unit_element in h1_unit_tag_block:
        palette_index = -1
        if unit_element.type_index >= 0:
            h2_unit_palette =  SCENARIO.vehicle_palette
            if is_biped:
                h2_unit_palette =  SCENARIO.biped_palette

            palette_entry = h1_unit_palette[unit_element.type_index]
            palette_index = find_tag_ref(TAG, h2_unit_palette, palette_entry.name, palette_entry.tag_group) 

        unit = SCENARIO.Unit()

        unit.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        unit.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        unit.sper_header = TAG.TagBlockHeader("sper", 0, 1, 24)
        unit.sunt_header = TAG.TagBlockHeader("sunt", 0, 1, 8)

        unit.palette_index = palette_index
        unit.name_index = unit_element.name_index
        unit.placement_flags = convert_object_flags(unit_element.placement_flags)
        unit.position = unit_element.position
        unit.rotation = unit_element.rotation
        unit.scale = 0
        unit.transform_flags = 0
        unit.manual_bsp_flags = 0
        unit.unique_id = get_id()
        unit.origin_bsp_index = global_functions.get_origin_bsp(bsp_bounds_list, unit)
        if is_biped:
            unit.object_type = 0
        else:
            unit.object_type = 1

        unit.source = 1
        unit.bsp_policy = 0
        unit.editor_folder_index = -1

        unit.variant_name = ""
        unit.variant_name_length = len(unit.variant_name)
        unit.active_change_colors = 0
        unit.primary_color_BGRA = (0, 0, 0, 255)
        unit.secondary_color_BGRA = (0, 0, 0, 255)
        unit.tertiary_color_BGRA = (0, 0, 0, 255)
        unit.quaternary_color_BGRA = (0, 0, 0, 255)
        unit.body_vitality = unit_element.body_vitality
        unit.flags = unit_element.flags

        h2_unit_tag_block.append(unit)

    return TAG.TagBlockHeader("tbfd", 2, len(h2_unit_tag_block), 84)

def get_equipment(H1_ASSET, TAG, SCENARIO, bsp_bounds_list):
    for equipment_element in H1_ASSET.equipment:
        palette_index = -1
        if equipment_element.type_index >= 0:
            palette_entry = H1_ASSET.equipment_palette[equipment_element.type_index]
            palette_index = find_tag_ref(TAG, SCENARIO.equipment_palette, palette_entry.name, palette_entry.tag_group) 

        equipment = SCENARIO.Equipment()

        equipment.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        equipment.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        equipment.seqt_header = TAG.TagBlockHeader("seqt", 0, 1, 4)

        equipment.palette_index = palette_index
        equipment.name_index = equipment_element.name_index
        equipment.placement_flags = convert_object_flags(equipment_element.placement_flags)
        equipment.position = equipment_element.position
        equipment.rotation = equipment_element.rotation
        equipment.scale = 0
        equipment.transform_flags = 0
        equipment.manual_bsp_flags = 0
        equipment.unique_id = get_id()
        equipment.origin_bsp_index = global_functions.get_origin_bsp(bsp_bounds_list, equipment)
        equipment.object_type = 3
        equipment.source = 1
        equipment.bsp_policy = 0
        equipment.editor_folder_index = -1

        equipment.flags = equipment_element.misc_flags

        SCENARIO.equipment.append(equipment)

    SCENARIO.equipment_header = TAG.TagBlockHeader("tbfd", 2, len(SCENARIO.equipment), 56)

def get_weapon(H1_ASSET, TAG, SCENARIO, bsp_bounds_list):
    for weapon_element in H1_ASSET.weapons:
        palette_index = -1
        if weapon_element.type_index >= 0:
            palette_entry = H1_ASSET.weapon_palette[weapon_element.type_index]
            palette_index = find_tag_ref(TAG, SCENARIO.weapon_palette, palette_entry.name, palette_entry.tag_group) 

        weapon = SCENARIO.Weapon()

        weapon.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        weapon.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        weapon.sper_header = TAG.TagBlockHeader("sper", 0, 1, 24)
        weapon.swpt_header = TAG.TagBlockHeader("swpt", 0, 1, 8)

        weapon.palette_index = palette_index
        weapon.name_index = weapon_element.name_index
        weapon.placement_flags = convert_object_flags(weapon_element.placement_flags)
        weapon.position = weapon_element.position
        weapon.rotation = weapon_element.rotation
        weapon.scale = 0
        weapon.transform_flags = 0
        weapon.manual_bsp_flags = 0
        weapon.unique_id = get_id()
        weapon.origin_bsp_index = global_functions.get_origin_bsp(bsp_bounds_list, weapon)
        weapon.object_type = 2
        weapon.source = 1
        weapon.bsp_policy = 0
        weapon.editor_folder_index = -1

        weapon.variant_name = ""
        weapon.variant_name_length = len(weapon.variant_name)
        weapon.active_change_colors = 0
        weapon.primary_color_BGRA = (0, 0, 0, 255)
        weapon.secondary_color_BGRA = (0, 0, 0, 255)
        weapon.tertiary_color_BGRA = (0, 0, 0, 255)
        weapon.quaternary_color_BGRA = (0, 0, 0, 255)
        weapon.rounds_left = weapon_element.rounds_left
        weapon.rounds_loaded = weapon_element.rounds_loaded
        weapon.flags = weapon_element.flags

        SCENARIO.weapons.append(weapon)

    SCENARIO.weapon_header = TAG.TagBlockHeader("tbfd", 2, len(SCENARIO.weapons), 84)

def get_device_groups(device_groups_tag_block, TAG, SCENARIO):
    for device_group_element in device_groups_tag_block:
        device_group = SCENARIO.DeviceGroup()
        device_group.name = device_group_element.name
        device_group.initial_value = device_group_element.initial_value
        device_group.flags = device_group_element.flags

        SCENARIO.device_groups.append(device_group)

    SCENARIO.device_group_header = TAG.TagBlockHeader("tbfd", 0, len(SCENARIO.device_groups), 40)

def get_device_machines(H1_ASSET, TAG, SCENARIO, bsp_bounds_list):
    for machine_element in H1_ASSET.device_machines:
        palette_index = -1
        if machine_element.type_index >= 0:
            palette_entry = H1_ASSET.device_machine_palette[machine_element.type_index]
            palette_index = find_tag_ref(TAG, SCENARIO.device_machine_palette, palette_entry.name, palette_entry.tag_group) 

        device_machine = SCENARIO.DeviceMachine()

        device_machine.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        device_machine.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        device_machine.sdvt_header = TAG.TagBlockHeader("sdvt", 0, 1, 8)
        device_machine.smht_header = TAG.TagBlockHeader("smht", 0, 1, 16)

        device_machine.palette_index = palette_index
        device_machine.name_index = machine_element.name_index
        device_machine.placement_flags = convert_object_flags(machine_element.placement_flags)
        device_machine.position = machine_element.position
        device_machine.rotation = machine_element.rotation
        device_machine.scale = 0
        device_machine.transform_flags = 0
        device_machine.manual_bsp_flags = 0
        device_machine.unique_id = get_id()
        device_machine.origin_bsp_index = global_functions.get_origin_bsp(bsp_bounds_list, device_machine)
        device_machine.object_type = 7
        device_machine.source = 1
        device_machine.bsp_policy = 0
        device_machine.editor_folder_index = -1

        device_machine.power_group_index = machine_element.power_group_index
        device_machine.position_group_index = machine_element.position_group_index
        device_machine.flags_0 = machine_element.flags_0
        device_machine.flags_1 = machine_element.flags_1

        device_machine.pathfinding_references = []
        pathfinding_ref_count = len(device_machine.pathfinding_references)
        device_machine.pathfinding_references_header = TAG.TagBlockHeader("tbfd", 0, pathfinding_ref_count, 4)
        device_machine.pathfinding_references_tag_block = TAG.TagBlock(pathfinding_ref_count)

        SCENARIO.device_machines.append(device_machine)

    SCENARIO.device_machine_header = TAG.TagBlockHeader("tbfd", 3, len(SCENARIO.device_machines), 76)

def get_device_controls(H1_ASSET, TAG, SCENARIO, bsp_bounds_list):
    for control_element in H1_ASSET.device_controls:
        palette_index = -1
        if control_element.type_index >= 0:
            palette_entry = H1_ASSET.device_control_palette[control_element.type_index]
            palette_index = find_tag_ref(TAG, SCENARIO.device_control_palette, palette_entry.name, palette_entry.tag_group) 

        device_control = SCENARIO.DeviceControl()

        device_control.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        device_control.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        device_control.sdvt_header = TAG.TagBlockHeader("sdvt", 0, 1, 8)
        device_control.sctt_header = TAG.TagBlockHeader("sctt", 0, 1, 8)

        device_control.palette_index = palette_index
        device_control.name_index = control_element.name_index
        device_control.placement_flags = convert_object_flags(control_element.placement_flags)
        device_control.position = control_element.position
        device_control.rotation = control_element.rotation
        device_control.scale = 0
        device_control.transform_flags = 0
        device_control.manual_bsp_flags = 0
        device_control.unique_id = get_id()
        device_control.origin_bsp_index = global_functions.get_origin_bsp(bsp_bounds_list, device_control)
        device_control.object_type = 8
        device_control.source = 1
        device_control.bsp_policy = 0
        device_control.editor_folder_index = -1

        device_control.power_group_index = control_element.power_group_index
        device_control.position_group_index = control_element.position_group_index
        device_control.flags_0 = control_element.flags_0
        device_control.flags_1 = control_element.flags_1
        device_control.unk = control_element.unknown

        SCENARIO.device_controls.append(device_control)

    SCENARIO.device_control_header = TAG.TagBlockHeader("tbfd", 2, len(SCENARIO.device_controls), 68)

def get_light_fixtures(H1_ASSET, TAG, SCENARIO, bsp_bounds_list):
    for light_fixture_element in H1_ASSET.device_light_fixtures:
        palette_index = -1
        if light_fixture_element.type_index >= 0:
            palette_entry = H1_ASSET.device_light_fixtures_palette[light_fixture_element.type_index]
            palette_index = find_tag_ref(TAG, SCENARIO.device_light_fixtures_palette, palette_entry.name, palette_entry.tag_group) 

        light_fixture = SCENARIO.LightFixture()

        light_fixture.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        light_fixture.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        light_fixture.sdvt_header = TAG.TagBlockHeader("sdvt", 0, 1, 8)
        light_fixture.slft_header = TAG.TagBlockHeader("slft", 0, 1, 24)

        light_fixture.palette_index = palette_index
        light_fixture.name_index = light_fixture_element.name_index
        light_fixture.placement_flags = convert_object_flags(light_fixture_element.placement_flags)
        light_fixture.position = light_fixture_element.position
        light_fixture.rotation = light_fixture_element.rotation
        light_fixture.scale = 0
        light_fixture.transform_flags = 0
        light_fixture.manual_bsp_flags = 0
        light_fixture.unique_id = get_id()
        light_fixture.origin_bsp_index = global_functions.get_origin_bsp(bsp_bounds_list, light_fixture)
        light_fixture.object_type = 9
        light_fixture.source = 1
        light_fixture.bsp_policy = 0
        light_fixture.editor_folder_index = -1

        light_fixture.power_group_index = light_fixture_element.power_group_index
        light_fixture.position_group_index = light_fixture_element.position_group_index
        light_fixture.flags = light_fixture_element.flags
        light_fixture.color_RGBA = light_fixture_element.color_RGBA
        light_fixture.intensity = light_fixture_element.intensity
        light_fixture.falloff_angle = light_fixture_element.falloff_angle
        light_fixture.cutoff_angle = light_fixture_element.cutoff_angle

        SCENARIO.device_light_fixtures.append(light_fixture)

    SCENARIO.device_light_fixture_header = TAG.TagBlockHeader("tbfd", 2, len(SCENARIO.device_light_fixtures), 84)

def get_sound_scenery(H1_ASSET, TAG, SCENARIO, bsp_bounds_list):
    for sound_scenery_element in H1_ASSET.sound_scenery:
        palette_index = -1
        if sound_scenery_element.type_index >= 0:
            palette_entry = H1_ASSET.sound_scenery_palette[sound_scenery_element.type_index]
            palette_index = find_tag_ref(TAG, SCENARIO.sound_scenery_palette, palette_entry.name, palette_entry.tag_group) 
        
        sound_scenery = SCENARIO.SoundScenery()

        sound_scenery.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        sound_scenery.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        sound_scenery._sc__header = TAG.TagBlockHeader("#sc#", 0, 1, 28)

        sound_scenery.palette_index = palette_index
        sound_scenery.name_index = sound_scenery_element.name_index
        sound_scenery.placement_flags = convert_object_flags(sound_scenery_element.placement_flags)
        sound_scenery.position = sound_scenery_element.position
        sound_scenery.rotation = sound_scenery_element.rotation
        sound_scenery.scale = 0
        sound_scenery.transform_flags = 0
        sound_scenery.manual_bsp_flags = 0
        sound_scenery.unique_id = get_id()
        sound_scenery.origin_bsp_index = global_functions.get_origin_bsp(bsp_bounds_list, sound_scenery)
        sound_scenery.object_type = 10
        sound_scenery.source = 1
        sound_scenery.bsp_policy = 0
        sound_scenery.editor_folder_index = -1

        sound_scenery.volume_type = 0
        sound_scenery.height = 0.0
        sound_scenery.override_distance_bounds = (0.0, 0.0)
        sound_scenery.override_core_angle_bounds = (0.0, 0.0)
        sound_scenery.override_outer_core_gain = 0.0

        SCENARIO.sound_scenery.append(sound_scenery)

    SCENARIO.sound_scenery_header = TAG.TagBlockHeader("tbfd", 2, len(SCENARIO.sound_scenery), 80)

def get_player_starting_profiles(player_starting_profiles_tag_block, TAG, SCENARIO):
    for player_starting_profile_element in player_starting_profiles_tag_block:
        player_starting_profile = SCENARIO.PlayerStartingProfile()

        player_starting_profile.name = player_starting_profile_element.name
        player_starting_profile.starting_health_damage = player_starting_profile_element.starting_health_damage
        player_starting_profile.starting_shield_damage = player_starting_profile_element.starting_shield_damage

        primary_tag_group = player_starting_profile_element.primary_weapon_tag_ref.tag_group
        primary_tag_path = player_starting_profile_element.primary_weapon_tag_ref.name
        player_starting_profile.primary_weapon_tag_ref = TAG.TagRef(primary_tag_group, primary_tag_path, len(primary_tag_path), upgrade_patches=TAG.upgrade_patches)

        player_starting_profile.primary_rounds_loaded = player_starting_profile_element.primary_rounds_loaded
        player_starting_profile.primary_rounds_total = player_starting_profile_element.primary_rounds_total

        secondary_tag_group = player_starting_profile_element.secondary_weapon_tag_ref.tag_group
        secondary_tag_path = player_starting_profile_element.secondary_weapon_tag_ref.name
        player_starting_profile.secondary_weapon_tag_ref = TAG.TagRef(secondary_tag_group, secondary_tag_path, len(secondary_tag_path), upgrade_patches=TAG.upgrade_patches)

        player_starting_profile.secondary_rounds_loaded = player_starting_profile_element.secondary_rounds_loaded
        player_starting_profile.secondary_rounds_total = player_starting_profile_element.secondary_rounds_total
        player_starting_profile.starting_fragmentation_grenades_count = player_starting_profile_element.starting_fragmentation_grenades_count
        player_starting_profile.starting_plasma_grenade_count = player_starting_profile_element.starting_plasma_grenade_count
        player_starting_profile.starting_custom_2_grenade_count = player_starting_profile_element.starting_grenade_type2_count
        player_starting_profile.starting_custom_3_grenade_count = player_starting_profile_element.starting_grenade_type3_count

        SCENARIO.player_starting_profiles.append(player_starting_profile)

    if len(SCENARIO.player_starting_profiles) == 0:
        battle_rifle_path = r"objects\weapons\rifle\battle_rifle\battle_rifle"
        smg_path = r"objects\weapons\rifle\smg\smg"

        player_starting_profile = SCENARIO.PlayerStartingProfile()

        player_starting_profile.name = "player starting profile_0"
        player_starting_profile.starting_health_damage = 0.0
        player_starting_profile.starting_shield_damage = 0.0
        player_starting_profile.primary_weapon_tag_ref = TAG.TagRef("weap", battle_rifle_path, len(battle_rifle_path))
        player_starting_profile.primary_rounds_loaded = 36
        player_starting_profile.primary_rounds_total = 108
        player_starting_profile.secondary_weapon_tag_ref = TAG.TagRef("weap", smg_path, len(smg_path))
        player_starting_profile.secondary_rounds_loaded = 60
        player_starting_profile.secondary_rounds_total = 180
        player_starting_profile.starting_fragmentation_grenades_count = 2
        player_starting_profile.starting_plasma_grenade_count = 0
        player_starting_profile.starting_custom_2_grenade_count = 0
        player_starting_profile.starting_custom_3_grenade_count = 0

        SCENARIO.player_starting_profiles.append(player_starting_profile)

    SCENARIO.player_starting_profile_header = TAG.TagBlockHeader("tbfd", 0, len(SCENARIO.player_starting_profiles), 84)

def get_player_starting_locations(player_starting_locations_tag_block, TAG, SCENARIO):
    for player_starting_location_element in player_starting_locations_tag_block:
        if not player_starting_location_element.team_index > 1: # CE only has two teams so ignore everything above 1
            player_starting_location = SCENARIO.PlayerStartingLocation()

            player_starting_location.position = player_starting_location_element.position
            player_starting_location.facing = player_starting_location_element.facing
            player_starting_location.team_designator = player_starting_location_element.team_index
            player_starting_location.bsp_index = -1
            player_starting_location.type_0 = convert_game_type_setting(player_starting_location_element.type_0)
            player_starting_location.type_1 = convert_game_type_setting(player_starting_location_element.type_1)
            player_starting_location.type_2 = convert_game_type_setting(player_starting_location_element.type_2)
            player_starting_location.type_3 = convert_game_type_setting(player_starting_location_element.type_3)
            player_starting_location.spawn_type_0 = 0
            player_starting_location.spawn_type_1 = 0
            player_starting_location.spawn_type_2 = 0
            player_starting_location.spawn_type_3 = 0
            player_starting_location.unk_0 = ""
            player_starting_location.unk_1 = ""
            player_starting_location.unk_0_length = len(player_starting_location.unk_0)
            player_starting_location.unk_1_length = len(player_starting_location.unk_1)
            player_starting_location.campaign_player_type = 0

            SCENARIO.player_starting_locations.append(player_starting_location)

    SCENARIO.player_starting_location_header = TAG.TagBlockHeader("tbfd", 0, len(SCENARIO.player_starting_locations), 52)

def get_trigger_volumes(trigger_volumes_tag_block, TAG, SCENARIO):
    for trigger_volume_element in trigger_volumes_tag_block:
        trigger_volume = SCENARIO.TriggerVolume()

        trigger_volume.name = trigger_volume_element.name
        trigger_volume.name_length = len(trigger_volume.name)
        trigger_volume.object_name_index = -1
        trigger_volume.node_name = ""
        trigger_volume.node_name_length = len(trigger_volume.node_name)
        trigger_volume.forward = trigger_volume_element.forward
        trigger_volume.up = trigger_volume_element.up
        trigger_volume.position = trigger_volume_element.position
        trigger_volume.extents = trigger_volume_element.extents
        trigger_volume.kill_trigger_volume_index = -1

        SCENARIO.trigger_volumes.append(trigger_volume)

    SCENARIO.trigger_volumes_header = TAG.TagBlockHeader("tbfd", 1, len(SCENARIO.trigger_volumes), 68)

def get_recorded_animations(recorded_animations_tag_block, TAG, SCENARIO):
    for recorded_animation_element in recorded_animations_tag_block:
        recorded_animation = SCENARIO.RecordedAnimation()

        recorded_animation.name = recorded_animation_element.name
        recorded_animation.version = recorded_animation_element.version
        recorded_animation.raw_animation_data = recorded_animation_element.raw_animation_data
        recorded_animation.unit_control_data_version = recorded_animation_element.unit_control_data_version
        recorded_animation.length_of_animation = recorded_animation_element.length_of_animation
        recorded_animation.recorded_animation_event_stream_tag_data = recorded_animation_element.recorded_animation_event_stream_tag_data
        recorded_animation.recorded_animation_event_stream = recorded_animation_element.recorded_animation_event_stream

        SCENARIO.recorded_animations.append(recorded_animation)

    SCENARIO.recorded_animation_header = TAG.TagBlockHeader("tbfd", 0, len(SCENARIO.recorded_animations), 64)

def get_netgame_flags(netgame_flags_tag_block, TAG, SCENARIO):
    hill_identifiers = []
    for netgame_flag_element in netgame_flags_tag_block:
        flag_type, team_designator, identifer, flags, is_valid, needs_return = convert_netgame_flag_type(netgame_flag_element.type, netgame_flag_element.usage_id, hill_identifiers)

        if is_valid:
            netgame_flag = SCENARIO.NetGameFlag()

            netgame_flag.position = netgame_flag_element.position
            netgame_flag.facing = netgame_flag_element.facing
            netgame_flag.type = flag_type
            netgame_flag.team_designator = team_designator
            netgame_flag.identifer = identifer
            netgame_flag.flags = flags
            netgame_flag.spawn_object_name = ""
            netgame_flag.spawn_object_name_length = len(netgame_flag.spawn_object_name)
            netgame_flag.spawn_marker_name = ""
            netgame_flag.spawn_marker_name_length = len(netgame_flag.spawn_marker_name)

            SCENARIO.netgame_flags.append(netgame_flag)

        if needs_return:
            netgame_flag = SCENARIO.NetGameFlag()

            netgame_flag.position = netgame_flag_element.position
            netgame_flag.facing = netgame_flag_element.facing
            netgame_flag.type = NetGameEnum.ctf_flag_return.value
            netgame_flag.team_designator = team_designator
            netgame_flag.identifer = identifer
            netgame_flag.flags = NetGameFlags.multi_flag_bomb.value + NetGameFlags.single_flag_bomb.value + NetGameFlags.neutral_flag_bomb.value
            netgame_flag.spawn_object_name = ""
            netgame_flag.spawn_object_name_length = len(netgame_flag.spawn_object_name)
            netgame_flag.spawn_marker_name = ""
            netgame_flag.spawn_marker_name_length = len(netgame_flag.spawn_marker_name)

            SCENARIO.netgame_flags.append(netgame_flag)

    SCENARIO.netgame_flag_header = TAG.TagBlockHeader("tbfd", 1, len(SCENARIO.netgame_flags), 32)

def get_netgame_equipment(netgame_equipment_tag_block, vehicles_tag_block, vehicle_palette_tag_block, scenario_type, TAG, SCENARIO):
    for netgame_equipment_element in netgame_equipment_tag_block:
        spawn_time, respawn_on_empty_time, respawn_timer_starts, classification = get_item_stats(netgame_equipment_element.item_collection.name)

        netgame_equipment = SCENARIO.NetGameEquipment()

        netgame_equipment.ntor_header = TAG.TagBlockHeader("ntor", 0, 1, 12)

        netgame_equipment.flags = netgame_equipment_element.flags
        netgame_equipment.type_0 = convert_game_type_setting(netgame_equipment_element.type_0)
        netgame_equipment.type_1 = convert_game_type_setting(netgame_equipment_element.type_1)
        netgame_equipment.type_2 = convert_game_type_setting(netgame_equipment_element.type_2)
        netgame_equipment.type_3 = convert_game_type_setting(netgame_equipment_element.type_3)
        netgame_equipment.spawn_time = netgame_equipment_element.spawn_time
        netgame_equipment.respawn_on_empty_time = respawn_on_empty_time
        netgame_equipment.respawn_timer_starts = respawn_timer_starts
        netgame_equipment.classification = classification
        netgame_equipment.position = netgame_equipment_element.position
        netgame_equipment.orientation = (0.0, 0.0, netgame_equipment_element.facing)

        item_collection_tag_group = netgame_equipment_element.item_collection.tag_group
        item_collection_tag_path = netgame_equipment_element.item_collection.name
        netgame_equipment.item_vehicle_collection = TAG.TagRef(item_collection_tag_group, item_collection_tag_path, len(item_collection_tag_path), upgrade_patches=TAG.upgrade_patches)

        SCENARIO.netgame_equipment.append(netgame_equipment)

    if H1ScenarioTypeEnum(scenario_type) == H1ScenarioTypeEnum.multiplayer:
        for vehicle_element in vehicles_tag_block:
            spawn_time, respawn_on_empty_time, respawn_timer_starts, classification = get_item_stats(vehicle_palette_tag_block[vehicle_element.type_index].name)
            type0, type1, type2, type3 = get_vehicle_gametypes(vehicle_element.multiplayer_spawn_flags)

            netgame_equipment = SCENARIO.NetGameEquipment()

            netgame_equipment.ntor_header = TAG.TagBlockHeader("ntor", 0, 1, 12)

            netgame_equipment.flags = 0
            netgame_equipment.type_0 = type0
            netgame_equipment.type_1 = type1
            netgame_equipment.type_2 = type2
            netgame_equipment.type_3 = type3
            netgame_equipment.spawn_time = spawn_time
            netgame_equipment.respawn_on_empty_time = respawn_on_empty_time
            netgame_equipment.respawn_timer_starts = respawn_timer_starts
            netgame_equipment.classification = classification
            netgame_equipment.position = vehicle_element.position
            netgame_equipment.orientation = vehicle_element.rotation

            item_collection_tag_group = "vehc"
            item_collection_tag_path = vehicle_palette_tag_block[vehicle_element.type_index].name
            netgame_equipment.item_vehicle_collection = TAG.TagRef(item_collection_tag_group, item_collection_tag_path, len(item_collection_tag_path), upgrade_patches=TAG.upgrade_patches)

            SCENARIO.netgame_equipment.append(netgame_equipment)

    netgame_count = len(SCENARIO.netgame_equipment)
    if netgame_count > 100:
        leftovers = netgame_count - 100
        SCENARIO.netgame_equipment = SCENARIO.netgame_equipment[:100]
        print(f"Netgame equipment has over 100 items. Delete {leftovers} elements from either the vehicle tag block or the netgame equipment tag block in the Halo 1 Scenario or be forever lost.")
    SCENARIO.netgame_equipment_header = TAG.TagBlockHeader("tbfd", 0, len(SCENARIO.netgame_equipment), 152)

def get_starting_equipment(starting_equipment_tag_block, TAG, SCENARIO):
    for starting_equipment_element in starting_equipment_tag_block:
        starting_equipment = SCENARIO.StartingEquipment()

        starting_equipment.flags = convert_starting_equipment_flags(starting_equipment_element.flags)
        starting_equipment.type_0 = convert_game_type_setting(starting_equipment_element.type_0)
        starting_equipment.type_1 = convert_game_type_setting(starting_equipment_element.type_1)
        starting_equipment.type_2 = convert_game_type_setting(starting_equipment_element.type_2)
        starting_equipment.type_3 = convert_game_type_setting(starting_equipment_element.type_3)
        item_collection_1_tag_group = starting_equipment_element.item_collection_1.tag_group
        item_collection_1_tag_path = starting_equipment_element.item_collection_1.name
        starting_equipment.item_collection_1 = TAG.TagRef(item_collection_1_tag_group, item_collection_1_tag_path, len(item_collection_1_tag_path), upgrade_patches=TAG.upgrade_patches)

        item_collection_2_tag_group = starting_equipment_element.item_collection_2.tag_group
        item_collection_2_tag_path = starting_equipment_element.item_collection_2.name
        starting_equipment.item_collection_2 = TAG.TagRef(item_collection_2_tag_group, item_collection_2_tag_path, len(item_collection_2_tag_path), upgrade_patches=TAG.upgrade_patches)

        item_collection_3_tag_group = starting_equipment_element.item_collection_3.tag_group
        item_collection_3_tag_path = starting_equipment_element.item_collection_3.name
        starting_equipment.item_collection_3 = TAG.TagRef(item_collection_3_tag_group, item_collection_3_tag_path, len(item_collection_3_tag_path), upgrade_patches=TAG.upgrade_patches)

        item_collection_4_tag_group = starting_equipment_element.item_collection_4.tag_group
        item_collection_4_tag_path = starting_equipment_element.item_collection_4.name
        starting_equipment.item_collection_4 = TAG.TagRef(item_collection_4_tag_group, item_collection_4_tag_path, len(item_collection_4_tag_path), upgrade_patches=TAG.upgrade_patches)

        item_collection_5_tag_group = starting_equipment_element.item_collection_5.tag_group
        item_collection_5_tag_path = starting_equipment_element.item_collection_5.name
        starting_equipment.item_collection_5 = TAG.TagRef(item_collection_5_tag_group, item_collection_5_tag_path, len(item_collection_5_tag_path), upgrade_patches=TAG.upgrade_patches)

        item_collection_6_tag_group = starting_equipment_element.item_collection_6.tag_group
        item_collection_6_tag_path = starting_equipment_element.item_collection_6.name
        starting_equipment.item_collection_6 = TAG.TagRef(item_collection_6_tag_group, item_collection_6_tag_path, len(item_collection_6_tag_path), upgrade_patches=TAG.upgrade_patches)

        SCENARIO.starting_equipment.append(starting_equipment)

    SCENARIO.starting_equipment_header = TAG.TagBlockHeader("tbfd", 0, len(SCENARIO.starting_equipment), 204)

def get_decals(decals_tag_block, TAG, SCENARIO):
    for decal_element in decals_tag_block:
        decal = SCENARIO.Decal()

        decal.palette_index = decal_element.palette_index
        decal.yaw = decal_element.yaw
        decal.pitch = decal_element.pitch
        decal.position = decal_element.position

        SCENARIO.decals.append(decal)

    SCENARIO.decals_header = TAG.TagBlockHeader("tbfd", 0, len(SCENARIO.decals), 16)

def get_zone_index(encounter_index, firing_position_count):
    zone_index = -1
    if firing_position_count > 0:
        zone_index = encounter_index

    return zone_index

def generate_h2_squads(H1_ASSET, TAG, SCENARIO, report):
    encounters_tag_block = H1_ASSET.encounters
    actors_palette_tag_block = H1_ASSET.actor_palette

    for encounter_element in encounters_tag_block:
        firing_point_count = len(encounter_element.firing_positions)
        if firing_point_count > 0:
            zone = SCENARIO.Zone()

            active_groups = []

            for firing_position in encounter_element.firing_positions:
                group_name = H1GroupEnum(firing_position.group_index).name
                if not group_name in active_groups:
                    active_groups.append(group_name)

            area_count = len(active_groups)
            zone.name = "zone_%s" % encounter_element.name
            zone.flags = 0
            zone.manual_bsp_index = -1
            zone.firing_positions_tag_block = TAG.TagBlock(firing_point_count)
            zone.areas_tag_block = TAG.TagBlock(area_count)
            zone.firing_positions = []
            zone.areas = []

            zone.firing_positions_header = TAG.TagBlockHeader("tbfd", 3, firing_point_count, 32)
            for firing_position_element in encounter_element.firing_positions:
                firing_position = SCENARIO.FiringPosition()

                firing_position.position = firing_position_element.position
                firing_position.reference_frame = -1
                firing_position.flags = 0
                firing_position.area_index = active_groups.index(H1GroupEnum(firing_position_element.group_index).name)
                firing_position.cluster_index = 0
                firing_position.normal = (0.0, 90)

                zone.firing_positions.append(firing_position)

            if area_count > 0:
                zone.areas_header = TAG.TagBlockHeader("tbfd", 1, area_count, 140)
                for group_element in active_groups:
                    area = SCENARIO.Area()

                    area.name = "area_%s" % group_element
                    area.flags = 0
                    area.runtime_starting_index = 0
                    area.runtime_count = 0
                    area.manual_reference_frame = 0
                    area.flight_hints_tag_block = TAG.TagBlock()

                    zone.areas.append(area)

            SCENARIO.zones.append(zone)

    SCENARIO.zones_header = TAG.TagBlockHeader("tbfd", 1, len(SCENARIO.zones), 64)

    actor_weapon_paths = []
    character_tag_paths = []
    weapon_tags = []
    actor_grenade_settings = []
    for weapon in SCENARIO.weapon_palette:
        weapon_tag_path = weapon.name
        character_tag_paths.append(weapon_tag_path)

    for actor in actors_palette_tag_block:
        actor_tag = parse_tag(actor, report, "halo1", "retail")
        if not actor_tag == None:
            actor_weapon_tag = actor_tag.weapon
            actor_weapon_name = actor_weapon_tag.name
            actor_grenade_settings.append(actor_tag.grenade_type)
            if not actor_weapon_name == "":
                patched_actor_weapon_name = tag_format.get_patched_name(TAG.upgrade_patches, actor_weapon_name)
                actor_weapon_paths.append(patched_actor_weapon_name)
                if not patched_actor_weapon_name in character_tag_paths:
                    character_tag_paths.append(patched_actor_weapon_name)
                    weapon_tags.append(actor_weapon_tag)

            else:
                actor_weapon_paths.append(None)
        else:
            actor_weapon_paths.append(None)

    SCENARIO.weapon_palette_header = get_palette(TAG, SCENARIO.weapon_palette, weapon_tags, 48)

    SCENARIO.squad_groups = []
    for encounter_element in encounters_tag_block:
        squad_group = SCENARIO.SquadGroups()

        squad_group.name = encounter_element.name
        squad_group.parent_index = -1
        squad_group.initial_order_index = -1

        SCENARIO.squad_groups.append(squad_group)

    SCENARIO.squad_groups_header = TAG.TagBlockHeader("tbfd", 0, len(SCENARIO.squad_groups), 36)

    SCENARIO.squads = []
    encounter_index = 0
    for encounter_idx, encounter_element in enumerate(encounters_tag_block):
        for squad_idx, squad_element in enumerate(encounter_element.squads):
            if not len(SCENARIO.squads) >= 335 and squad_element.starting_locations_tag_block.count > 0:
                squad_actor_weapon = None
                grenade_setting = 0
                if squad_element.actor_type >= 0:
                    squad_actor_weapon = actor_weapon_paths[squad_element.actor_type]
                    grenade_setting = actor_grenade_settings[squad_element.actor_type] + 1

                squad = SCENARIO.Squad()

                squad.name = squad_element.name
                squad.flags = 0
                squad.team = encounter_element.team_index
                squad.parent_squad_group_index = encounter_idx
                squad.squad_delay_time = squad_element.squad_delay_time
                squad.normal_difficulty_count = squad_element.normal_diff_count
                squad.insane_difficulty_count = squad_element.insane_diff_count
                squad.major_upgrade = squad_element.major_upgrade
                squad.vehicle_type_index = -1
                squad.character_type_index = squad_element.actor_type
                squad.initial_zone_index = get_zone_index(encounter_index, len(encounter_element.firing_positions))
                squad.initial_weapon_index = -1
                if not squad_actor_weapon == None:
                    squad.initial_weapon_index = character_tag_paths.index(squad_actor_weapon)

                squad.initial_secondary_weapon_index = -1
                squad.grenade_type = grenade_setting
                squad.initial_order_index = -1
                squad.vehicle_variant = ""
                squad.vehicle_variant_length = len(squad.vehicle_variant)
                squad.placement_script = ""

                squad.starting_locations = []
                if squad_element.starting_locations_tag_block.count > 0:
                    for starting_location_idx, starting_location_element in enumerate(squad_element.starting_locations):
                        if not starting_location_idx > 31:
                            starting_location_actor_weapon = None
                            sl_grenade_setting = 0
                            if starting_location_element.actor_type >= 0:
                                starting_location_actor_weapon = actor_weapon_paths[starting_location_element.actor_type]
                                sl_grenade_setting = actor_grenade_settings[starting_location_element.actor_type] + 1

                            starting_location = SCENARIO.StartingLocation()

                            starting_location_name = "starting_locations_%s" % starting_location_idx
                            starting_location.name = starting_location_name
                            starting_location.name_length = len(starting_location.name)
                            starting_location.position = starting_location_element.position
                            starting_location.reference_frame = -1
                            starting_location.facing = (0.0, starting_location_element.facing)

                            starting_location.flags = 0
                            starting_location.character_type_index = starting_location_element.actor_type
                            starting_location.initial_weapon_index = -1
                            if not starting_location_actor_weapon == None:
                                starting_location.initial_weapon_index = character_tag_paths.index(starting_location_actor_weapon)
                            starting_location.initial_secondary_weapon_index = -1
                            starting_location.vehicle_type_index = -1
                            starting_location.seat_type = 0
                            starting_location.grenade_type = sl_grenade_setting
                            starting_location.swarm_count = 0
                            starting_location.actor_variant = ""
                            starting_location.vehicle_variant = ""
                            starting_location.initial_movement_distance = 0
                            starting_location.emitter_vehicle_index = -1
                            starting_location.initial_movement_mode = 0
                            starting_location.placement_script = ""

                            squad.starting_locations.append(starting_location)

                        else:
                            print("Excedded limits on starting locations")

                starting_location_count = len(squad.starting_locations)
                squad.starting_locations_header = TAG.TagBlockHeader("tbfd", 6, starting_location_count, 100)
                squad.starting_locations_tag_block = TAG.TagBlock(starting_location_count)

                SCENARIO.squads.append(squad)

            else:
                print("Excedded limits on squad")

        if len(encounter_element.firing_positions) > 0:
            encounter_index += 1

    SCENARIO.squads_header = TAG.TagBlockHeader("tbfd", 2, len(SCENARIO.squads), 120)
    SCENARIO.character_palette_header = get_palette(TAG, SCENARIO.character_palette, actors_palette_tag_block, 16, "char")

def generate_point_sets(H1_ASSET, TAG, SCENARIO):
    for script_data_idx in range(1):
        scripting_data = SCENARIO.ScriptingData()

        scripting_data.point_sets = []
        for command_list_element in H1_ASSET.command_lists:
            point_set = SCENARIO.PointSet()

            point_set.name = command_list_element.name
            point_set.bsp_index = 0
            point_set.manual_reference_frame = 0
            point_set.flags = 0
            point_set.points = []
            for point_idx, point_element in enumerate(command_list_element.points):
                point = SCENARIO.Point()

                point.name = "p%s" % point_idx
                point.position = point_element
                point.reference_frame = -1
                point.surface_index = 0
                point.facing_direction_y = 0.0
                point.facing_direction_p = 0.0

                point_set.points.append(point)

            point_set.points_tag_block = TAG.TagBlock(len(point_set.points))
            point_set.points_header = TAG.TagBlockHeader("tbfd", 1, len(point_set.points), 60)

            scripting_data.point_sets.append(point_set)

        point_set_collection = bpy.data.collections.get("Point Set")
        if point_set_collection:
            for obj in point_set_collection.objects:
                point_set = SCENARIO.PointSet()

                point_set.name = obj.name
                point_set.bsp_index = 0
                point_set.manual_reference_frame = 0
                point_set.flags = 0
                point_set.points = []
                for vertex_idx, vertex in enumerate(obj.data.vertices):
                    if vertex_idx >= 20:
                        print("Object %s has more than 20 vertices. Limit the amount of vertices to 20 max" % obj.name)
                        break

                    halo_pos = vertex.co * 0.01
                    point = SCENARIO.Point()

                    point.name = "p%s" % vertex_idx
                    point.position = halo_pos
                    point.reference_frame = -1
                    point.surface_index = 0
                    point.facing_direction_y = 0.0
                    point.facing_direction_p = 0.0

                    point_set.points.append(point)

                point_set.points_tag_block = TAG.TagBlock(len(point_set.points))
                point_set.points_header = TAG.TagBlockHeader("tbfd", 1, len(point_set.points), 60)

                scripting_data.point_sets.append(point_set)

        scripting_data.point_sets_tag_block = TAG.TagBlock(len(scripting_data.point_sets))
        scripting_data.point_sets_header = TAG.TagBlockHeader("tbfd", 1, len(scripting_data.point_sets), 52)

        SCENARIO.scripting_data.append(scripting_data)

    SCENARIO.scripting_data_header = TAG.TagBlockHeader("tbfd", 0, len(SCENARIO.scripting_data), 132)

def get_cutscene_flags(cutscene_flags_tag_block, TAG, SCENARIO):
    SCENARIO.cutscene_flags = []
    for cutscene_flag_element in cutscene_flags_tag_block:
        cutscene_flags = SCENARIO.CutsceneFlag()

        cutscene_flags.name = cutscene_flag_element.name
        cutscene_flags.position = cutscene_flag_element.position
        cutscene_flags.facing = cutscene_flag_element.facing

        SCENARIO.cutscene_flags.append(cutscene_flags)

    SCENARIO.cutscene_flags_header = TAG.TagBlockHeader("tbfd", 0, len(SCENARIO.cutscene_flags), 56)

def get_cutscene_camera_points(cutscene_camera_points_tag_block, TAG, SCENARIO):
    SCENARIO.cutscene_camera_points = []
    for cutscene_camera_point_element in cutscene_camera_points_tag_block:
        cutscene_camera_point = SCENARIO.CutsceneCameraPoint()

        cutscene_camera_point.flags = 0
        cutscene_camera_point.camera_type = 0
        cutscene_camera_point.name = cutscene_camera_point_element.name
        cutscene_camera_point.position = cutscene_camera_point_element.position
        cutscene_camera_point.orientation = cutscene_camera_point_element.orientation

        SCENARIO.cutscene_camera_points.append(cutscene_camera_point)

    SCENARIO.cutscene_camera_points_header = TAG.TagBlockHeader("tbfd", 0, len(SCENARIO.cutscene_camera_points), 64)

def get_cutscene_titles(cutscene_titles_tag_block, TAG, SCENARIO):
    SCENARIO.cutscene_titles = []
    for cutscene_titles_element in cutscene_titles_tag_block:
        cutscene_title = SCENARIO.CutsceneTitle()

        cutscene_title.name = cutscene_titles_element.name
        cutscene_title.name_length = len(cutscene_title.name)
        cutscene_title.text_bounds = cutscene_titles_element.text_bounds
        cutscene_title.justification = cutscene_titles_element.justification
        cutscene_title.font = 0
        cutscene_title.text_color = cutscene_titles_element.text_color
        cutscene_title.shadow_color = cutscene_titles_element.shadow_color
        cutscene_title.fade_in_time = cutscene_titles_element.fade_in_time
        cutscene_title.up_time = cutscene_titles_element.up_time
        cutscene_title.fade_out_time = cutscene_titles_element.fade_out_time

        SCENARIO.cutscene_titles.append(cutscene_title)

    SCENARIO.cutscene_titles_header = TAG.TagBlockHeader("tbfd", 0, len(SCENARIO.cutscene_titles), 36)

def get_structure_bsp(structure_bsp_tag_block, TAG, SCENARIO):
    SCENARIO.structure_bsps = []
    for structure_bsp_element in structure_bsp_tag_block:
        structure_bsp = SCENARIO.StructureBSP()

        structure_bsp_tag_group = "sbsp"
        structure_bsp_tag_path = structure_bsp_element.name
        structure_bsp.structure_bsp = TAG.TagRef(structure_bsp_tag_group, structure_bsp_tag_path, len(structure_bsp_tag_path), upgrade_patches=TAG.upgrade_patches)

        structure_lightmap_tag_group = "ltmp"
        structure_lightmap_tag_path = ""
        structure_bsp.structure_lightmap = TAG.TagRef(structure_lightmap_tag_group, structure_lightmap_tag_path, len(structure_lightmap_tag_path), upgrade_patches=TAG.upgrade_patches)
        structure_bsp.unused_radiance_estimated_search_distance = 0.0
        structure_bsp.unused_luminels_per_world_unit = 0.0
        structure_bsp.unused_output_white_reference = 0.0
        structure_bsp.flags = 0
        structure_bsp.default_sky = -1

        SCENARIO.structure_bsps.append(structure_bsp)

    SCENARIO.structure_bsps_header = TAG.TagBlockHeader("tbfd", 1, len(SCENARIO.structure_bsps), 84)

def get_palette(TAG, palette_list, palette_tag_block, size, tag_group=None):
    tag_group_name = tag_group
    for palette_element in palette_tag_block:
        if tag_group == None:
            tag_group_name = palette_element.tag_group

        tag_group = tag_group_name
        tag_path = palette_element.name

        tag_ref = TAG.TagRef(tag_group, tag_path, len(tag_path))

        palette_list.append(tag_ref)

    return TAG.TagBlockHeader("tbfd", 0, len(palette_list), size)

def scan_palette(TAG, palette_tag_block):
    palette_indices = []
    palette_destination_list = []

    for palette_element_idx, palette_element in enumerate(palette_tag_block):
        prepatched_tag_path = '%s,%s' % (palette_element.name, palette_element.tag_group)
        prepatched_tag_group = None
        patched_tag_path = tag_format.get_patched_name(TAG.upgrade_patches, prepatched_tag_path)
        patched_tag_group = None
        if "," in prepatched_tag_path:
            result = prepatched_tag_path.rsplit(",", 1)
            if len(result) == 2 and len(result[1]) <= 4:
                prepatched_tag_path = result[0].lower()
                prepatched_tag_group = "{:<4}".format(result[1].lower())

        if "," in patched_tag_path:
            result = patched_tag_path.rsplit(",", 1)
            if len(result) == 2 and len(result[1]) <= 4:
                patched_tag_path = result[0].lower()
                patched_tag_group = "{:<4}".format(result[1].lower())

        if prepatched_tag_group and patched_tag_group and not prepatched_tag_group == patched_tag_group:
            palette_indices.append(palette_element_idx)
            palette_destination_list.append((prepatched_tag_group, patched_tag_group))

    return palette_indices, palette_destination_list

def mutate_element(block_element, TAG, SCENARIO, source, destination, bsp_bounds_list, H1_SCENARIO):
    if source == "scen":
        scenario_palette = H1_SCENARIO.scenery_palette
    elif source == "bipd":
        scenario_palette = H1_SCENARIO.biped_palette
    elif source == "vehi":
        scenario_palette = H1_SCENARIO.vehicle_palette
    elif source == "eqip":
        scenario_palette = H1_SCENARIO.equipment_palette
    elif source == "weap":
        scenario_palette = H1_SCENARIO.weapon_palette
    elif source == "mach":
        scenario_palette = H1_SCENARIO.device_machine_palette
    elif source == "ctrl":
        scenario_palette = H1_SCENARIO.device_control_palette
    elif source == "lifi":
        scenario_palette = H1_SCENARIO.device_light_fixtures_palette
    elif source == "ssce":
        scenario_palette = H1_SCENARIO.sound_scenery_palette

    if destination == "scen":
        palette_index = -1
        if block_element.type_index >= 0:
            palette_entry = scenario_palette[block_element.type_index]
            palette_index = find_tag_ref(TAG, SCENARIO.scenery_palette, palette_entry.name, source) 

        mutated_element = SCENARIO.Scenery()

        mutated_element.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        mutated_element.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        mutated_element.sper_header = TAG.TagBlockHeader("sper", 0, 1, 24)
        mutated_element.sct3_header = TAG.TagBlockHeader("sct3", 0, 1, 20)

        mutated_element.palette_index = palette_index
        mutated_element.name_index = block_element.name_index
        mutated_element.placement_flags = block_element.placement_flags
        mutated_element.position = block_element.position
        mutated_element.rotation = block_element.rotation
        mutated_element.scale = 0
        mutated_element.transform_flags = 0
        mutated_element.manual_bsp_flags = 0
        mutated_element.unique_id = get_id()
        mutated_element.origin_bsp_index = global_functions.get_origin_bsp(bsp_bounds_list, mutated_element)
        mutated_element.object_type = 6
        mutated_element.source = 1
        mutated_element.bsp_policy = 0
        mutated_element.editor_folder_index = -1

        mutated_element.variant_name = ""
        mutated_element.variant_name_length = len(mutated_element.variant_name)
        mutated_element.active_change_colors = 0
        mutated_element.primary_color_BGRA = (0, 0, 0, 255)
        mutated_element.secondary_color_BGRA = (0, 0, 0, 255)
        mutated_element.tertiary_color_BGRA = (0, 0, 0, 255)
        mutated_element.quaternary_color_BGRA = (0, 0, 0, 255)
        mutated_element.pathfinding_policy = 0
        mutated_element.lightmap_policy = 0
        mutated_element.valid_multiplayer_games = 0

        mutated_element.pathfinding_references = []
        pathfinding_ref_count = len(mutated_element.pathfinding_references)
        mutated_element.pathfinding_references_header = TAG.TagBlockHeader("tbfd", 0, pathfinding_ref_count, 4)
        mutated_element.pathfinding_references_tag_block = TAG.TagBlock(pathfinding_ref_count)

    elif destination == "bipd" or destination == "vehi":
        palette_index = -1
        if block_element.type_index >= 0:
            palette_list =  SCENARIO.vehicle_palette
            if destination == 'bipd':
                palette_list =  SCENARIO.biped_palette

            palette_entry = scenario_palette[block_element.type_index]
            palette_index = find_tag_ref(TAG, palette_list, palette_entry.name, source) 

        mutated_element = SCENARIO.Unit()

        mutated_element.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        mutated_element.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        mutated_element.sper_header = TAG.TagBlockHeader("sper", 0, 1, 24)
        mutated_element.sunt_header = TAG.TagBlockHeader("sunt", 0, 1, 8)

        mutated_element.palette_index = palette_index
        mutated_element.name_index = block_element.name_index
        mutated_element.placement_flags = block_element.placement_flags
        mutated_element.position = block_element.position
        mutated_element.rotation = block_element.rotation
        mutated_element.scale = 0
        mutated_element.transform_flags = 0
        mutated_element.manual_bsp_flags = 0
        mutated_element.unique_id = get_id()
        mutated_element.origin_bsp_index = global_functions.get_origin_bsp(bsp_bounds_list, mutated_element)
        if destination == "bipd":
            mutated_element.object_type = 0
        else:
            mutated_element.object_type = 1

        mutated_element.source = 1
        mutated_element.bsp_policy = 0
        mutated_element.editor_folder_index = -1
        mutated_element.variant_name = ""
        mutated_element.variant_name_length = len(mutated_element.variant_name)
        mutated_element.active_change_colors = 0
        mutated_element.primary_color_BGRA = (0, 0, 0, 255)
        mutated_element.secondary_color_BGRA = (0, 0, 0, 255)
        mutated_element.tertiary_color_BGRA = (0, 0, 0, 255)
        mutated_element.quaternary_color_BGRA = (0, 0, 0, 255)
        mutated_element.body_vitality = 0.0
        mutated_element.flags = 0

    elif destination == "eqip":
        palette_index = -1
        if block_element.type_index >= 0:
            palette_entry = scenario_palette[block_element.type_index]
            palette_index = find_tag_ref(TAG, SCENARIO.equipment_palette, palette_entry.name, source) 

        mutated_element = SCENARIO.Equipment()

        mutated_element.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        mutated_element.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        mutated_element.seqt_header = TAG.TagBlockHeader("seqt", 0, 1, 4)

        mutated_element.palette_index = palette_index
        mutated_element.name_index = block_element.name_index
        mutated_element.placement_flags = block_element.placement_flags
        mutated_element.position = block_element.position
        mutated_element.rotation = block_element.rotation
        mutated_element.scale = 0
        mutated_element.transform_flags = 0
        mutated_element.manual_bsp_flags = 0
        mutated_element.unique_id = get_id()
        mutated_element.origin_bsp_index = global_functions.get_origin_bsp(bsp_bounds_list, mutated_element)
        mutated_element.object_type = 3
        mutated_element.source = 1
        mutated_element.bsp_policy = 0
        mutated_element.editor_folder_index = -1
        mutated_element.flags = 0

    elif destination == "weap":
        palette_index = -1
        if block_element.type_index >= 0:
            palette_entry = scenario_palette[block_element.type_index]
            palette_index = find_tag_ref(TAG, SCENARIO.weapon_palette, palette_entry.name, source) 

        mutated_element = SCENARIO.Weapon()

        mutated_element.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        mutated_element.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        mutated_element.sper_header = TAG.TagBlockHeader("sper", 0, 1, 24)
        mutated_element.swpt_header = TAG.TagBlockHeader("swpt", 0, 1, 8)

        mutated_element.palette_index = palette_index
        mutated_element.name_index = block_element.name_index
        mutated_element.placement_flags = block_element.placement_flags
        mutated_element.position = block_element.position
        mutated_element.rotation = block_element.rotation
        mutated_element.scale = 0
        mutated_element.transform_flags = 0
        mutated_element.manual_bsp_flags = 0
        mutated_element.unique_id = get_id()
        mutated_element.origin_bsp_index = global_functions.get_origin_bsp(bsp_bounds_list, mutated_element)
        mutated_element.object_type = 2
        mutated_element.source = 1
        mutated_element.bsp_policy = 0
        mutated_element.editor_folder_index = -1

        mutated_element.variant_name = ""
        mutated_element.variant_name_length = len(mutated_element.variant_name)
        mutated_element.active_change_colors = 0
        mutated_element.primary_color_BGRA = (0, 0, 0, 255)
        mutated_element.secondary_color_BGRA = (0, 0, 0, 255)
        mutated_element.tertiary_color_BGRA = (0, 0, 0, 255)
        mutated_element.quaternary_color_BGRA = (0, 0, 0, 255)
        mutated_element.rounds_left = 0
        mutated_element.rounds_loaded = 0
        mutated_element.flags = 0

    elif destination == "mach":
        palette_index = -1
        if block_element.type_index >= 0:
            palette_entry = scenario_palette[block_element.type_index]
            palette_index = find_tag_ref(TAG, SCENARIO.device_machine_palette, palette_entry.name, source) 

        mutated_element = SCENARIO.DeviceMachine()

        mutated_element.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        mutated_element.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        mutated_element.sdvt_header = TAG.TagBlockHeader("sdvt", 0, 1, 8)
        mutated_element.smht_header = TAG.TagBlockHeader("smht", 0, 1, 16)

        mutated_element.palette_index = palette_index
        mutated_element.name_index = block_element.name_index
        mutated_element.placement_flags = block_element.placement_flags
        mutated_element.position = block_element.position
        mutated_element.rotation = block_element.rotation
        mutated_element.scale = 0
        mutated_element.transform_flags = 0
        mutated_element.manual_bsp_flags = 0
        mutated_element.unique_id = get_id()
        mutated_element.origin_bsp_index = global_functions.get_origin_bsp(bsp_bounds_list, mutated_element)
        mutated_element.object_type = 7
        mutated_element.source = 1
        mutated_element.bsp_policy = 0
        mutated_element.editor_folder_index = -1

        mutated_element.power_group_index = -1
        mutated_element.position_group_index = -1
        mutated_element.flags_0 = 0
        mutated_element.flags_1 = 0

        mutated_element.pathfinding_references = []
        pathfinding_ref_count = len(mutated_element.pathfinding_references)
        mutated_element.pathfinding_references_header = TAG.TagBlockHeader("tbfd", 0, pathfinding_ref_count, 4)
        mutated_element.pathfinding_references_tag_block = TAG.TagBlock(pathfinding_ref_count)

    elif destination == "ctrl":
        palette_index = -1
        if block_element.type_index >= 0:
            palette_entry = scenario_palette[block_element.type_index]
            palette_index = find_tag_ref(TAG, SCENARIO.device_control_palette, palette_entry.name, source) 

        mutated_element = SCENARIO.DeviceControl()

        mutated_element.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        mutated_element.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        mutated_element.sdvt_header = TAG.TagBlockHeader("sdvt", 0, 1, 8)
        mutated_element.sctt_header = TAG.TagBlockHeader("sctt", 0, 1, 8)

        mutated_element.palette_index = palette_index
        mutated_element.name_index = block_element.name_index
        mutated_element.placement_flags = block_element.placement_flags
        mutated_element.position = block_element.position
        mutated_element.rotation = block_element.rotation
        mutated_element.scale = 0
        mutated_element.transform_flags = 0
        mutated_element.manual_bsp_flags = 0
        mutated_element.unique_id = get_id()
        mutated_element.origin_bsp_index = global_functions.get_origin_bsp(bsp_bounds_list, mutated_element)
        mutated_element.object_type = 8
        mutated_element.source = 1
        mutated_element.bsp_policy = 0
        mutated_element.editor_folder_index = -1
        mutated_element.power_group_index = -1
        mutated_element.position_group_index = -1
        mutated_element.flags_0 = 0
        mutated_element.flags_1 = 0
        mutated_element.unk = 0

    elif destination == "lifi":
        palette_index = -1
        if block_element.type_index >= 0:
            palette_entry = scenario_palette[block_element.type_index]
            palette_index = find_tag_ref(TAG, SCENARIO.device_light_fixtures_palette, palette_entry.name, source) 

        mutated_element = SCENARIO.LightFixture()

        mutated_element.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        mutated_element.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        mutated_element.sdvt_header = TAG.TagBlockHeader("sdvt", 0, 1, 8)
        mutated_element.slft_header = TAG.TagBlockHeader("slft", 0, 1, 24)

        mutated_element.palette_index = palette_index
        mutated_element.name_index = block_element.name_index
        mutated_element.placement_flags = block_element.placement_flags
        mutated_element.position = block_element.position
        mutated_element.rotation = block_element.rotation
        mutated_element.scale = 0
        mutated_element.transform_flags = 0
        mutated_element.manual_bsp_flags = 0
        mutated_element.unique_id = get_id()
        mutated_element.origin_bsp_index = global_functions.get_origin_bsp(bsp_bounds_list, mutated_element)
        mutated_element.object_type = 9
        mutated_element.source = 1
        mutated_element.bsp_policy = 0
        mutated_element.editor_folder_index = -1
        mutated_element.power_group_index = -1
        mutated_element.position_group_index = -1
        mutated_element.flags = 0
        mutated_element.color_RGBA = (0, 0, 0, 255)
        mutated_element.intensity = 0.0
        mutated_element.falloff_angle = 0.0
        mutated_element.cutoff_angle = 0.0

    elif destination == "ssce":
        palette_index = -1
        if block_element.type_index >= 0:
            palette_entry = scenario_palette[block_element.type_index]
            palette_index = find_tag_ref(TAG, SCENARIO.sound_scenery_palette, palette_entry.name, source) 

        mutated_element = SCENARIO.SoundScenery()

        mutated_element.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        mutated_element.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        mutated_element._sc__header = TAG.TagBlockHeader("#sc#", 0, 1, 28)

        mutated_element.palette_index = palette_index
        mutated_element.name_index = block_element.name_index
        mutated_element.placement_flags = block_element.placement_flags
        mutated_element.position = block_element.position
        mutated_element.rotation = block_element.rotation
        mutated_element.scale = 0
        mutated_element.transform_flags = 0
        mutated_element.manual_bsp_flags = 0
        mutated_element.unique_id = get_id()
        mutated_element.origin_bsp_index = global_functions.get_origin_bsp(bsp_bounds_list, mutated_element)
        mutated_element.object_type = 10
        mutated_element.source = 1
        mutated_element.bsp_policy = 0
        mutated_element.editor_folder_index = -1
        mutated_element.volume_type = 0
        mutated_element.height = 0.0
        mutated_element.override_distance_bounds = (0.0, 0.0)
        mutated_element.override_core_angle_bounds = (0.0, 0.0)
        mutated_element.override_outer_core_gain = 0.0

    elif destination == "bloc":
        palette_index = -1
        if block_element.type_index >= 0:
            palette_entry = scenario_palette[block_element.type_index]
            palette_index = find_tag_ref(TAG, SCENARIO.crates_palette, palette_entry.name, source)

        mutated_element = SCENARIO.Crate()

        mutated_element.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        mutated_element.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        mutated_element.sper_header = TAG.TagBlockHeader("sper", 0, 1, 24)

        mutated_element.palette_index = palette_index
        mutated_element.name_index = block_element.name_index
        mutated_element.placement_flags = block_element.placement_flags
        mutated_element.position = block_element.position
        mutated_element.rotation = block_element.rotation
        mutated_element.scale = 0
        mutated_element.transform_flags = 0
        mutated_element.manual_bsp_flags = 0
        mutated_element.unique_id = get_id()
        mutated_element.origin_bsp_index = global_functions.get_origin_bsp(bsp_bounds_list, mutated_element)
        mutated_element.object_type = 11
        mutated_element.source = 1
        mutated_element.bsp_policy = 0
        mutated_element.editor_folder_index = -1
        mutated_element.variant_name = ""
        mutated_element.active_change_colors = 0
        mutated_element.primary_color_BGRA = (0, 0, 0, 255)
        mutated_element.secondary_color_BGRA = (0, 0, 0, 255)
        mutated_element.tertiary_color_BGRA = (0, 0, 0, 255)
        mutated_element.quaternary_color_BGRA = (0, 0, 0, 255)

    return mutated_element

def find_tag_ref(TAG, palette_list, source_tag_path, source_tag_group):
    palette_index = -1
    source_tag_path = '%s,%s' % (source_tag_path, source_tag_group)
    for palette_idx, palette_entry in enumerate(palette_list):
        target_tag_path = '%s,%s' % (palette_entry.name, palette_entry.tag_group)
        if source_tag_path == target_tag_path:
            palette_index = palette_idx
            break

    return palette_index

def mutate_block(H1_SCENARIO, TAG, SCENARIO, palette_indices, palette_destination_list, donor_tag_block, bsp_bounds_list):
    transfered_indices = []

    for block_element_idx, block_element in enumerate(donor_tag_block):
        palette_index = block_element.type_index
        if palette_index in palette_indices:
            index = palette_indices.index(palette_index)
            palette_destination_item = palette_destination_list[index]
            source = palette_destination_item[0]
            destination = palette_destination_item[1]
            transfered_indices.append(block_element_idx)

            if destination == "scen":
                mutated_element = mutate_element(block_element, TAG, SCENARIO, source, destination, bsp_bounds_list, H1_SCENARIO)
                SCENARIO.scenery.append(mutated_element)
            elif destination == "bipd":
                mutated_element = mutate_element(block_element, TAG, SCENARIO, source, destination, bsp_bounds_list, H1_SCENARIO)
                SCENARIO.bipeds.append(mutated_element)
            elif destination == "vehi":
                mutated_element = mutate_element(block_element, TAG, SCENARIO, source, destination, bsp_bounds_list, H1_SCENARIO)
                SCENARIO.vehicles.append(mutated_element)
            elif destination == "eqip":
                mutated_element = mutate_element(block_element, TAG, SCENARIO, source, destination, bsp_bounds_list, H1_SCENARIO)
                SCENARIO.equipment.append(mutated_element)
            elif destination == "weap":
                mutated_element = mutate_element(block_element, TAG, SCENARIO, source, destination, bsp_bounds_list, H1_SCENARIO)
                SCENARIO.weapons.append(mutated_element)
            elif destination == "mach":
                mutated_element = mutate_element(block_element, TAG, SCENARIO, source, destination, bsp_bounds_list, H1_SCENARIO)
                SCENARIO.device_machines.append(mutated_element)
            elif destination == "ctrl":
                mutated_element = mutate_element(block_element, TAG, SCENARIO, source, destination, bsp_bounds_list, H1_SCENARIO)
                SCENARIO.device_controls.append(mutated_element)
            elif destination == "lifi":
                mutated_element = mutate_element(block_element, TAG, SCENARIO, source, destination, bsp_bounds_list, H1_SCENARIO)
                SCENARIO.device_light_fixtures.append(mutated_element)
            elif destination == "ssce":
                mutated_element = mutate_element(block_element, TAG, SCENARIO, source, destination, bsp_bounds_list, H1_SCENARIO)
                SCENARIO.sound_scenery.append(mutated_element)
            elif destination == "ligh":
                mutated_element = mutate_element(block_element, TAG, SCENARIO, source, destination, bsp_bounds_list, H1_SCENARIO)
                SCENARIO.light_volumes.append(mutated_element)
            elif destination == "bloc":
                mutated_element = mutate_element(block_element, TAG, SCENARIO, source, destination, bsp_bounds_list, H1_SCENARIO)
                SCENARIO.crates.append(mutated_element)

    for idx in reversed(transfered_indices):
        del donor_tag_block[idx]

def mutate_palette(H1_SCENARIO, TAG, SCENARIO, palette_indices, palette_destination_list):
    for palette_idx, palette_index in enumerate(palette_indices):
        palette_destination_item = palette_destination_list[palette_idx]
        source = palette_destination_item[0]
        destination = palette_destination_item[1]
        tag_ref = None
        if source == "scen":
            tag_ref = H1_SCENARIO.scenery_palette[palette_index]
        elif source == "bipd":
            tag_ref = H1_SCENARIO.biped_palette[palette_index]
        elif source == "vehi":
            tag_ref = H1_SCENARIO.vehicle_palette[palette_index]
        elif source == "eqip":
            tag_ref = H1_SCENARIO.equipment_palette[palette_index]
        elif source == "weap":
            tag_ref = H1_SCENARIO.weapon_palette[palette_index]
        elif source == "mach":
            tag_ref = H1_SCENARIO.device_machine_palette[palette_index]
        elif source == "ctrl":
            tag_ref = H1_SCENARIO.device_control_palette[palette_index]
        elif source == "lifi":
            tag_ref = H1_SCENARIO.device_light_fixtures_palette[palette_index]
        elif source == "ssce":
            tag_ref = H1_SCENARIO.sound_scenery_palette[palette_index]
        elif source == "ligh":
            tag_ref = H1_SCENARIO.light_volume_palette[palette_index]
        elif source == "bloc":
            tag_ref = H1_SCENARIO.crates_palette[palette_index]

        if destination == "scen":
            tag_name = "%s,%s" % (tag_ref.name, tag_ref.tag_group)
            tag_ref_unique = True
            for palette_element in SCENARIO.scenery_palette:
                palette_tag_name = "%s,%s" % (palette_element.name, palette_element.tag_group)
                if tag_name == palette_tag_name:
                    tag_ref_unique = False

            if tag_ref_unique:
                SCENARIO.scenery_palette.append(tag_ref)

        elif destination == "bipd":
            tag_name = "%s,%s" % (tag_ref.name, tag_ref.tag_group)
            tag_ref_unique = True
            for palette_element in SCENARIO.biped_palette:
                palette_tag_name = "%s,%s" % (palette_element.name, palette_element.tag_group)
                if tag_name == palette_tag_name:
                    tag_ref_unique = False

            if tag_ref_unique:
                SCENARIO.biped_palette.append(tag_ref)

        elif destination == "vehi":
            tag_name = "%s,%s" % (tag_ref.name, tag_ref.tag_group)
            tag_ref_unique = True
            for palette_element in SCENARIO.vehicle_palette:
                palette_tag_name = "%s,%s" % (palette_element.name, palette_element.tag_group)
                if tag_name == palette_tag_name:
                    tag_ref_unique = False

            if tag_ref_unique:
                SCENARIO.vehicle_palette.append(tag_ref)

        elif destination == "eqip":
            tag_name = "%s,%s" % (tag_ref.name, tag_ref.tag_group)
            tag_ref_unique = True
            for palette_element in SCENARIO.equipment_palette:
                palette_tag_name = "%s,%s" % (palette_element.name, palette_element.tag_group)
                if tag_name == palette_tag_name:
                    tag_ref_unique = False

            if tag_ref_unique:
                SCENARIO.equipment_palette.append(tag_ref)

        elif destination == "weap":
            tag_name = "%s,%s" % (tag_ref.name, tag_ref.tag_group)
            tag_ref_unique = True
            for palette_element in SCENARIO.weapon_palette:
                palette_tag_name = "%s,%s" % (palette_element.name, palette_element.tag_group)
                if tag_name == palette_tag_name:
                    tag_ref_unique = False

            if tag_ref_unique:
                SCENARIO.weapon_palette.append(tag_ref)

        elif destination == "mach":
            tag_name = "%s,%s" % (tag_ref.name, tag_ref.tag_group)
            tag_ref_unique = True
            for palette_element in SCENARIO.device_machine_palette:
                palette_tag_name = "%s,%s" % (palette_element.name, palette_element.tag_group)
                if tag_name == palette_tag_name:
                    tag_ref_unique = False

            if tag_ref_unique:
                SCENARIO.device_machine_palette.append(tag_ref)

        elif destination == "ctrl":
            tag_name = "%s,%s" % (tag_ref.name, tag_ref.tag_group)
            tag_ref_unique = True
            for palette_element in SCENARIO.device_control_palette:
                palette_tag_name = "%s,%s" % (palette_element.name, palette_element.tag_group)
                if tag_name == palette_tag_name:
                    tag_ref_unique = False

            if tag_ref_unique:
                SCENARIO.device_control_palette.append(tag_ref)

        elif destination == "lifi":
            tag_name = "%s,%s" % (tag_ref.name, tag_ref.tag_group)
            tag_ref_unique = True
            for palette_element in SCENARIO.device_light_fixture_palette:
                palette_tag_name = "%s,%s" % (palette_element.name, palette_element.tag_group)
                if tag_name == palette_tag_name:
                    tag_ref_unique = False

            if tag_ref_unique:
                SCENARIO.device_light_fixture_palette.append(tag_ref)

        elif destination == "ssce":
            tag_name = "%s,%s" % (tag_ref.name, tag_ref.tag_group)
            tag_ref_unique = True
            for palette_element in SCENARIO.sound_scenery_palette:
                palette_tag_name = "%s,%s" % (palette_element.name, palette_element.tag_group)
                if tag_name == palette_tag_name:
                    tag_ref_unique = False

            if tag_ref_unique:
                SCENARIO.sound_scenery_palette.append(tag_ref)

        elif destination == "ligh":
            tag_name = "%s,%s" % (tag_ref.name, tag_ref.tag_group)
            tag_ref_unique = True
            for palette_element in SCENARIO.light_volume_palette:
                palette_tag_name = "%s,%s" % (palette_element.name, palette_element.tag_group)
                if tag_name == palette_tag_name:
                    tag_ref_unique = False

            if tag_ref_unique:
                SCENARIO.light_volume_palette.append(tag_ref)

        elif destination == "bloc":
            tag_name = "%s,%s" % (tag_ref.name, tag_ref.tag_group)
            tag_ref_unique = True
            for palette_element in SCENARIO.crates_palette:
                palette_tag_name = "%s,%s" % (palette_element.name, palette_element.tag_group)
                if tag_name == palette_tag_name:
                    tag_ref_unique = False

            if tag_ref_unique:
                SCENARIO.crates_palette.append(tag_ref)

def block_mutation(H1_SCENARIO, TAG, SCENARIO, bsp_bounds_list):
    scenery_palette_indices, scenery_palette_destination_list = scan_palette(TAG, H1_SCENARIO.scenery_palette)
    biped_palette_indices, biped_palette_destination_list = scan_palette(TAG, H1_SCENARIO.biped_palette)
    vehicle_palette_indices, vehicle_palette_destination_list = scan_palette(TAG, H1_SCENARIO.vehicle_palette)
    equipment_palette_indices, equipment_palette_destination_list = scan_palette(TAG, H1_SCENARIO.equipment_palette)
    weapon_palette_indices, weapon_palette_destination_list = scan_palette(TAG, H1_SCENARIO.weapon_palette)
    machine_palette_indices, machine_palette_destination_list = scan_palette(TAG, H1_SCENARIO.device_machine_palette)
    sound_scenery_palette_indices, sound_scenery_destination_list = scan_palette(TAG, H1_SCENARIO.sound_scenery_palette)
    if len(scenery_palette_indices) > 0:
        mutate_palette(H1_SCENARIO, TAG, SCENARIO, scenery_palette_indices, scenery_palette_destination_list)
        mutate_block(H1_SCENARIO, TAG, SCENARIO, scenery_palette_indices, scenery_palette_destination_list, H1_SCENARIO.scenery, bsp_bounds_list)

    if len(biped_palette_indices) > 0:
        mutate_palette(H1_SCENARIO, TAG, SCENARIO, biped_palette_indices, biped_palette_destination_list)
        mutate_block(H1_SCENARIO, TAG, SCENARIO, biped_palette_indices, biped_palette_destination_list, H1_SCENARIO.bipeds, bsp_bounds_list)

    if len(vehicle_palette_indices) > 0:
        mutate_palette(H1_SCENARIO, TAG, SCENARIO, vehicle_palette_indices, vehicle_palette_destination_list)
        mutate_block(H1_SCENARIO, TAG, SCENARIO, vehicle_palette_indices, vehicle_palette_destination_list, H1_SCENARIO.vehicles, bsp_bounds_list)

    if len(equipment_palette_indices) > 0:
        mutate_palette(H1_SCENARIO, TAG, SCENARIO, equipment_palette_indices, equipment_palette_destination_list)
        mutate_block(H1_SCENARIO, TAG, SCENARIO, equipment_palette_indices, equipment_palette_destination_list, H1_SCENARIO.equipment, bsp_bounds_list)

    if len(weapon_palette_indices) > 0:
        mutate_palette(H1_SCENARIO, TAG, SCENARIO, weapon_palette_indices, weapon_palette_destination_list)
        mutate_block(H1_SCENARIO, TAG, SCENARIO, weapon_palette_indices, weapon_palette_destination_list, H1_SCENARIO.weapons, bsp_bounds_list)

    if len(machine_palette_indices) > 0:
        mutate_palette(H1_SCENARIO, TAG, SCENARIO, machine_palette_indices, machine_palette_destination_list)
        mutate_block(H1_SCENARIO, TAG, SCENARIO, machine_palette_indices, machine_palette_destination_list, H1_SCENARIO.device_machines, bsp_bounds_list)

    if len(sound_scenery_palette_indices) > 0:
        mutate_palette(H1_SCENARIO, TAG, SCENARIO, sound_scenery_palette_indices, sound_scenery_destination_list)
        mutate_block(H1_SCENARIO, TAG, SCENARIO, sound_scenery_palette_indices, sound_scenery_destination_list, H1_SCENARIO.sound_scenery, bsp_bounds_list)

    SCENARIO.scenery_header = tag_block_header(TAG, "tbfd", 4, len(SCENARIO.scenery), 96)
    SCENARIO.bipeds_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.bipeds), 84)
    SCENARIO.vehicles_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.vehicles), 84)
    SCENARIO.equipment_header = tag_block_header(TAG, "tbfd", 2, len(SCENARIO.equipment), 56)
    SCENARIO.weapon_header = tag_block_header(TAG, "tbfd", 2, len(SCENARIO.weapons), 84)
    SCENARIO.device_machine_header = tag_block_header(TAG, "tbfd", 3, len(SCENARIO.device_machines), 76)
    SCENARIO.device_control_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.device_controls), 48)
    SCENARIO.light_fixture_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.device_light_fixtures), 48)
    SCENARIO.sound_scenery_header = tag_block_header(TAG, "tbfd", 2, len(SCENARIO.sound_scenery), 80)
    SCENARIO.light_volume_header = tag_block_header(TAG, "tbfd", 2, len(SCENARIO.light_volumes), 108)
    SCENARIO.crates_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.crates), 76)
    SCENARIO.scenery_palette_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.scenery_palette), 48)
    SCENARIO.biped_palette_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.biped_palette), 48)
    SCENARIO.vehicle_palette_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.vehicle_palette), 48)
    SCENARIO.equipment_palette_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.equipment_palette), 48)
    SCENARIO.weapon_palette_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.weapon_palette), 48)
    SCENARIO.device_machine_palette_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.device_machine_palette), 48)
    SCENARIO.device_control_palette_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.device_control_palette), 48)
    SCENARIO.device_light_fixture_palette_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.device_light_fixtures_palette), 48)
    SCENARIO.sound_scenery_palette_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.sound_scenery_palette), 48)
    SCENARIO.light_volume_palette_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.light_volume_palette), 48)
    SCENARIO.crates_palette_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.crates_palette), 48)

def merge_by_name(base_tag_block, donor_tag_block, name_type=0):
    base_entries = []
    for base_element in base_tag_block:
        entry_name = ""
        if name_type == 0:
            entry_name = base_element.name
        elif name_type == 1:
            entry_name = base_element.animation_name
        elif name_type == 2:
            entry_name = base_element

        base_entries.append(entry_name)

    for donor_element in donor_tag_block:
        entry_name = ""
        if name_type == 0:
            entry_name = donor_element.name
        elif name_type == 1:
            entry_name = donor_element.animation_name
        elif name_type == 2:
            entry_name = donor_element

        if not entry_name in base_entries:
            base_tag_block.append(donor_element)

def merge_scavenger_hunt_objects(base_scavenger_hunt_objects, donor_scavenger_hunt_objects, base_object_names, donor_object_names):
    base_indices = [base_object.scenario_object_name_index for base_object in base_scavenger_hunt_objects]
    base_names = [object_name for object_name in base_object_names]
    donor_names = [object_name for object_name in donor_object_names]

    for donor_element in donor_scavenger_hunt_objects:
        if donor_element.scenario_object_name_index >= 0:
            donor_name = donor_names[donor_element.scenario_object_name_index]
            base_name_index = base_names.index(donor_name)
            donor_element.scenario_object_name_index = base_name_index

        if not base_name_index in base_indices:
            base_scavenger_hunt_objects.append(donor_element)

def merge_objects(base_objects, donor_object, base_palette, donor_palette, base_object_names=None, donor_object_names=None, base_device_groups=None, donor_device_groups=None):
    base_palette_names = [base_element.name for base_element in base_palette]
    donor_palette_names = [object_element.name for object_element in donor_palette]
    base_names = []
    donor_names = []
    base_device_groups_names = []
    donor_device_groups_names = []
    if not base_object_names == None:
        base_names = [object_name for object_name in base_object_names]
    if not donor_object_names == None:
        donor_names = [object_name for object_name in donor_object_names]
    if not base_device_groups == None:
        base_device_groups_names = [base_device_group.name for base_device_group in base_device_groups]
    if not donor_device_groups == None:
        donor_device_groups_names = [donor_device_group.name for donor_device_group in donor_device_groups]

    for donor_element in donor_palette:
        if not donor_element.name in base_palette_names:
            base_palette.append(donor_element)

    base_palette_names = [base_element.name for base_element in base_palette]
    for donor_element in donor_object:
        if not base_object_names == None:
            donor_type_index = donor_palette_names[donor_element.type_index]
            donor_element.type_index = base_palette_names.index(donor_type_index)
            donor_name_index = donor_names[donor_element.name_index]
            donor_element.name_index = base_names.index(donor_name_index)
            if not base_device_groups == None:
                if donor_element.power_group_index >= 0:
                    power_group_index = donor_device_groups_names[donor_element.power_group_index]
                    donor_element.power_group_index = base_device_groups_names.index(power_group_index)

            if not donor_device_groups == None:
                if donor_element.position_group_index >= 0:
                    position_group_index = donor_device_groups_names[donor_element.position_group_index]
                    donor_element.position_group_index = base_device_groups_names.index(position_group_index)

        else:
            donor_type_index = donor_palette_names[donor_element.palette_index]
            donor_element.palette_index = base_palette_names.index(donor_type_index)

        base_objects.append(donor_element)

def merge_by_location(base_tag_block, donor_tag_block):
    location_checksums = []
    for base_element in base_tag_block:
        x, y, z = base_element.position
        x_int = struct.unpack('<i', struct.pack('<f', x))[0]
        y_int = struct.unpack('<i', struct.pack('<f', y))[0]
        z_int = struct.unpack('<i', struct.pack('<f', z))[0]

        location_checksums.append((x_int + y_int + z_int))

    for donor_element in donor_tag_block:
        x, y, z = donor_element.position
        x_int = struct.unpack('<i', struct.pack('<f', x))[0]
        y_int = struct.unpack('<i', struct.pack('<f', y))[0]
        z_int = struct.unpack('<i', struct.pack('<f', z))[0]
        donor_checksum = (x_int + y_int + z_int)
        if not donor_checksum in location_checksums:
            base_tag_block.append(donor_element)

def merge_elements(base_tag_block, donor_tag_block):
    for donor_element in donor_tag_block:
        base_tag_block.append(donor_element)

def merge_ai_conversations(base_tag_block, donor_tag_block, base_object_names, donor_object_names):
    base_names = [object_name for object_name in base_object_names]
    donor_names = [object_name for object_name in donor_object_names]
    base_entries = [base_element.name for base_element in base_tag_block]
    for donor_element in donor_tag_block:
        if not donor_element.name in base_entries:
            for participant in donor_element.participants:
                if participant.use_this_object >= 0:
                    use_this_object_index = donor_names[participant.use_this_object]
                    participant.use_this_object = base_names.index(use_this_object_index)

                if participant.set_new_name >= 0:
                    set_new_name_index = donor_names[participant.set_new_name]
                    participant.set_new_name = base_names.index(set_new_name_index)

            base_tag_block.append(donor_element)

def merge_encounters(base_encounters, donor_encounters, base_palette, donor_palette):
    base_encounters_names = [base_element.name for base_element in base_encounters]
    base_palette_names = [base_element.name for base_element in base_palette]
    donor_palette_names = [object_element.name for object_element in donor_palette]
    for donor_element in donor_palette:
        if not donor_element.name in base_palette_names:
            base_palette.append(donor_element)

    base_palette_names = [base_element.name for base_element in base_palette]
    for donor_element in donor_encounters:
        if not donor_element.name in base_encounters_names:
            for squad_element in donor_element.squads:
                if squad_element.actor_type >= 0:
                    donor_actor_index = donor_palette_names[squad_element.actor_type]
                    squad_element.actor_type = base_palette_names.index(donor_actor_index)

            base_encounters.append(donor_element)

def merge_child_scenarios(TAG, SCENARIO, report):
    for child_scenario_element in SCENARIO.child_scenarios:
        CHILD = parse_tag(child_scenario_element, report, "halo1", "retail")

        merge_by_name(SCENARIO.skies, CHILD.skies)
        merge_by_name(SCENARIO.object_names, CHILD.object_names, 2)
        merge_by_location(SCENARIO.comments, CHILD.comments)
        merge_scavenger_hunt_objects(SCENARIO.scavenger_hunt_objects, CHILD.scavenger_hunt_objects, SCENARIO.object_names, CHILD.object_names)
        merge_objects(SCENARIO.scenery, CHILD.scenery, SCENARIO.scenery_palette, CHILD.scenery_palette, SCENARIO.object_names, CHILD.object_names)
        merge_objects(SCENARIO.bipeds, CHILD.bipeds, SCENARIO.biped_palette, CHILD.biped_palette, SCENARIO.object_names, CHILD.object_names)
        merge_objects(SCENARIO.vehicles, CHILD.vehicles, SCENARIO.vehicle_palette, CHILD.vehicle_palette, SCENARIO.object_names, CHILD.object_names)
        merge_objects(SCENARIO.equipment, CHILD.equipment, SCENARIO.equipment_palette, CHILD.equipment_palette, SCENARIO.object_names, CHILD.object_names)
        merge_objects(SCENARIO.weapons, CHILD.weapons, SCENARIO.weapon_palette, CHILD.weapon_palette, SCENARIO.object_names, CHILD.object_names)
        merge_by_name(SCENARIO.device_groups, CHILD.device_groups)
        merge_objects(SCENARIO.device_machines, CHILD.device_machines, SCENARIO.device_machine_palette, CHILD.device_machine_palette, SCENARIO.object_names, CHILD.object_names, SCENARIO.device_groups, CHILD.device_groups)
        merge_objects(SCENARIO.device_controls, CHILD.device_controls, SCENARIO.device_control_palette, CHILD.device_control_palette, SCENARIO.object_names, CHILD.object_names, SCENARIO.device_groups, CHILD.device_groups)
        merge_objects(SCENARIO.device_light_fixtures, CHILD.device_light_fixtures, SCENARIO.device_light_fixtures_palette, CHILD.device_light_fixtures_palette, SCENARIO.object_names, CHILD.object_names, SCENARIO.device_groups, CHILD.device_groups)
        merge_objects(SCENARIO.sound_scenery, CHILD.sound_scenery, SCENARIO.sound_scenery_palette, CHILD.sound_scenery_palette, SCENARIO.object_names, CHILD.object_names)
        merge_by_name(SCENARIO.player_starting_profiles, CHILD.player_starting_profiles)
        #merge_by_location(SCENARIO.player_starting_locations, CHILD.player_starting_locations)
        merge_by_name(SCENARIO.trigger_volumes, CHILD.trigger_volumes)
        merge_by_name(SCENARIO.recorded_animations, CHILD.recorded_animations)
        merge_by_location(SCENARIO.netgame_flags, CHILD.netgame_flags)
        merge_by_location(SCENARIO.netgame_equipment, CHILD.netgame_equipment)
        merge_elements(SCENARIO.starting_equipment, CHILD.starting_equipment)
        merge_elements(SCENARIO.bsp_switch_trigger_volumes, CHILD.bsp_switch_trigger_volumes)
        merge_objects(SCENARIO.decals, CHILD.decals, SCENARIO.decal_palette, CHILD.decal_palette)
        merge_by_name(SCENARIO.detail_object_collection_palette, CHILD.detail_object_collection_palette)
        merge_encounters(SCENARIO.encounters, CHILD.encounters, SCENARIO.actor_palette, CHILD.actor_palette)
        merge_by_name(SCENARIO.command_lists, CHILD.command_lists)
        merge_by_name(SCENARIO.ai_animation_references, CHILD.ai_animation_references, 1)
        merge_by_name(SCENARIO.ai_script_references, CHILD.ai_script_references, 2)
        merge_ai_conversations(SCENARIO.ai_conversations, CHILD.ai_conversations, SCENARIO.object_names, CHILD.object_names)
        merge_by_name(SCENARIO.source_files, CHILD.source_files)
        merge_by_name(SCENARIO.cutscene_flags, CHILD.cutscene_flags)
        merge_by_name(SCENARIO.cutscene_camera_points, CHILD.cutscene_camera_points)
        merge_by_name(SCENARIO.cutscene_titles, CHILD.cutscene_titles)
        merge_by_name(SCENARIO.structure_bsps, CHILD.structure_bsps)

def upgrade_h2_scenario(H1_ASSET, patch_txt_path, report):
    TAG = tag_format.TagAsset()
    SCENARIO = ScenarioAsset()
    TAG.upgrade_patches = tag_format.get_patch_set(patch_txt_path)

    SCENARIO.header = TAG.Header()
    SCENARIO.header.unk1 = 0
    SCENARIO.header.flags = 0
    SCENARIO.header.type = 0
    SCENARIO.header.name = ""
    SCENARIO.header.tag_group = "scnr"
    SCENARIO.header.checksum = 0
    SCENARIO.header.data_offset = 64
    SCENARIO.header.data_length = 0
    SCENARIO.header.unk2 = 0
    SCENARIO.header.version = 2
    SCENARIO.header.destination = 0
    SCENARIO.header.plugin_handle = -1
    SCENARIO.header.engine_tag = "BLM!"

    SCENARIO.skies = []
    SCENARIO.child_scenarios = []
    SCENARIO.predicted_resources = []
    SCENARIO.functions = []
    SCENARIO.editor_scenario_data = TAG.RawData()
    SCENARIO.editor_scenario_data.data = bytes()
    SCENARIO.comments = []
    SCENARIO.environment_objects = []
    SCENARIO.object_names = []
    SCENARIO.scenery = []
    SCENARIO.scenery_palette = []
    SCENARIO.bipeds = []
    SCENARIO.biped_palette = []
    SCENARIO.vehicles = []
    SCENARIO.vehicle_palette = []
    SCENARIO.equipment = []
    SCENARIO.equipment_palette = []
    SCENARIO.weapons = []
    SCENARIO.weapon_palette = []
    SCENARIO.device_groups = []
    SCENARIO.device_machines = []
    SCENARIO.device_machine_palette = []
    SCENARIO.device_controls = []
    SCENARIO.device_control_palette = []
    SCENARIO.device_light_fixtures = []
    SCENARIO.device_light_fixtures_palette = []
    SCENARIO.sound_scenery = []
    SCENARIO.sound_scenery_palette = []
    SCENARIO.light_volumes = []
    SCENARIO.light_volume_palette = []
    SCENARIO.player_starting_profiles = []
    SCENARIO.player_starting_locations = []
    SCENARIO.trigger_volumes = []
    SCENARIO.recorded_animations = []
    SCENARIO.netgame_flags = []
    SCENARIO.netgame_equipment = []
    SCENARIO.starting_equipment = []
    SCENARIO.bsp_switch_trigger_volumes = []
    SCENARIO.decals = []
    SCENARIO.decal_palette = []
    SCENARIO.detail_object_collection_palette = []
    SCENARIO.style_palette = []
    SCENARIO.squad_groups = []
    SCENARIO.squads = []
    SCENARIO.zones = []
    SCENARIO.mission_scenes = []
    SCENARIO.character_palette = []
    SCENARIO.ai_pathfinding_data = []
    SCENARIO.ai_animation_references = []
    SCENARIO.ai_script_references = []
    SCENARIO.ai_recording_references = []
    SCENARIO.ai_conversations = []
    SCENARIO.script_syntax_data = bytes()
    SCENARIO.script_string_data = bytes()
    SCENARIO.scripts = []
    SCENARIO.script_globals = []
    SCENARIO.references = []
    SCENARIO.source_files = []
    SCENARIO.scripting_data = []
    SCENARIO.cutscene_flags = []
    SCENARIO.cutscene_camera_points = []
    SCENARIO.cutscene_titles = []
    SCENARIO.structure_bsps = []
    SCENARIO.scenario_resources = []
    SCENARIO.old_structure_physics = []
    SCENARIO.hs_unit_seats = []
    SCENARIO.scenario_kill_triggers = []
    SCENARIO.hs_syntax_datums = []
    SCENARIO.orders = []
    SCENARIO.triggers = []
    SCENARIO.background_sound_palette = []
    SCENARIO.sound_environment_palette = []
    SCENARIO.weather_palette = []
    SCENARIO.unused_0 = []
    SCENARIO.unused_1 = []
    SCENARIO.unused_2 = []
    SCENARIO.unused_3 = []
    SCENARIO.scavenger_hunt_objects = []
    SCENARIO.scenario_cluster_data = []
    SCENARIO.spawn_data = []
    SCENARIO.crates = []
    SCENARIO.crates_palette = []
    SCENARIO.atmospheric_fog_palette = []
    SCENARIO.planar_fog_palette = []
    SCENARIO.flocks = []
    SCENARIO.decorators = []
    SCENARIO.creatures = []
    SCENARIO.creatures_palette = []
    SCENARIO.decorator_palette = []
    SCENARIO.bsp_transition_volumes = []
    SCENARIO.structure_bsp_lighting = []
    SCENARIO.editor_folders = []
    SCENARIO.level_data = []
    SCENARIO.mission_dialogue = []
    SCENARIO.interpolators = []
    SCENARIO.shared_references = []
    SCENARIO.screen_effect_references = []
    SCENARIO.simulation_definition_table = []

    bsp_bounds_list = []

    h2_scenario_path = os.path.join(bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_tag_path, "%s.scenario" % H1_ASSET.header.local_path)
    if os.path.isfile(h2_scenario_path):
        input_stream = open(h2_scenario_path, "rb")
        SCNR_ASSET = process_h2_scenario(input_stream, print)
        input_stream.close()

        global_functions.build_bounds_list(SCNR_ASSET, bsp_bounds_list)

    merge_child_scenarios(TAG, H1_ASSET, report)

    block_mutation(H1_ASSET, TAG, SCENARIO, bsp_bounds_list)

    SCENARIO.skies_header = get_palette(TAG, SCENARIO.skies, H1_ASSET.skies, 16)

    SCENARIO.child_scenario_header = get_palette(TAG, SCENARIO.child_scenarios, H1_ASSET.child_scenarios, 32)

    get_comments(H1_ASSET.comments, TAG, SCENARIO)

    get_object_names(H1_ASSET.object_names, TAG, SCENARIO)

    get_scenery(H1_ASSET, TAG, SCENARIO, bsp_bounds_list)
    SCENARIO.scenery_palette_header = get_palette(TAG, SCENARIO.scenery_palette, H1_ASSET.scenery_palette, 48)

    SCENARIO.bipeds_header = get_unit(H1_ASSET, TAG, SCENARIO, True, bsp_bounds_list)
    SCENARIO.biped_palette_header = get_palette(TAG, SCENARIO.biped_palette, H1_ASSET.biped_palette, 48)

    if not H1ScenarioTypeEnum(H1_ASSET.scenario_type) == H1ScenarioTypeEnum.multiplayer:
        SCENARIO.vehicles_header = get_unit(H1_ASSET, TAG, SCENARIO, False, bsp_bounds_list)
        SCENARIO.vehicle_palette_header = get_palette(TAG, SCENARIO.vehicle_palette, H1_ASSET.vehicle_palette, 48)

    get_equipment(H1_ASSET, TAG, SCENARIO, bsp_bounds_list)
    SCENARIO.equipment_palette_header = get_palette(TAG, SCENARIO.equipment_palette, H1_ASSET.equipment_palette, 48)

    get_weapon(H1_ASSET, TAG, SCENARIO, bsp_bounds_list)
    SCENARIO.weapon_palette_header = get_palette(TAG, SCENARIO.weapon_palette, H1_ASSET.weapon_palette, 48)

    get_device_groups(H1_ASSET.device_groups, TAG, SCENARIO)

    get_device_machines(H1_ASSET, TAG, SCENARIO, bsp_bounds_list)
    SCENARIO.device_machine_palette_header = get_palette(TAG, SCENARIO.device_machine_palette, H1_ASSET.device_machine_palette, 48)

    get_device_controls(H1_ASSET, TAG, SCENARIO, bsp_bounds_list)
    SCENARIO.device_control_palette_header = get_palette(TAG, SCENARIO.device_control_palette, H1_ASSET.device_control_palette, 48)

    get_light_fixtures(H1_ASSET, TAG, SCENARIO, bsp_bounds_list)
    SCENARIO.device_light_fixture_palette_header = get_palette(TAG, SCENARIO.device_light_fixtures_palette, H1_ASSET.device_light_fixtures_palette, 48)

    get_sound_scenery(H1_ASSET, TAG, SCENARIO, bsp_bounds_list)
    SCENARIO.sound_scenery_palette_header = get_palette(TAG, SCENARIO.sound_scenery_palette, H1_ASSET.sound_scenery_palette, 48)

    get_player_starting_profiles(H1_ASSET.player_starting_profiles, TAG, SCENARIO)

    get_player_starting_locations(H1_ASSET.player_starting_locations, TAG, SCENARIO)

    get_trigger_volumes(H1_ASSET.trigger_volumes, TAG, SCENARIO)

    get_recorded_animations(H1_ASSET.recorded_animations, TAG, SCENARIO)

    get_netgame_flags(H1_ASSET.netgame_flags, TAG, SCENARIO)

    get_netgame_equipment(H1_ASSET.netgame_equipment, H1_ASSET.vehicles, H1_ASSET.vehicle_palette, H1_ASSET.scenario_type, TAG, SCENARIO)

    get_starting_equipment(H1_ASSET.starting_equipment, TAG, SCENARIO)

    get_decals(H1_ASSET.decals, TAG, SCENARIO)
    SCENARIO.decal_palette_header = get_palette(TAG, SCENARIO.decal_palette, H1_ASSET.decal_palette, 16)

    generate_h2_squads(H1_ASSET, TAG, SCENARIO, report)

    generate_point_sets(H1_ASSET, TAG, SCENARIO)

    get_cutscene_flags(H1_ASSET.cutscene_flags, TAG, SCENARIO)

    get_cutscene_camera_points(H1_ASSET.cutscene_camera_points, TAG, SCENARIO)

    get_cutscene_titles(H1_ASSET.cutscene_titles, TAG, SCENARIO)

    get_structure_bsp(H1_ASSET.structure_bsps, TAG, SCENARIO)

    for sky_element in SCENARIO.skies:
        sky_element.get_patched_tag_ref(TAG.upgrade_patches)
        sky_element.tag_group = "sky "

    for scenery_palette in SCENARIO.scenery_palette:
        scenery_palette.get_patched_tag_ref(TAG.upgrade_patches)
        scenery_palette.tag_group = "scen"

    for biped_palette in SCENARIO.biped_palette:
        biped_palette.get_patched_tag_ref(TAG.upgrade_patches)
        biped_palette.tag_group = "bipd"

    for vehicle_palette in SCENARIO.vehicle_palette:
        vehicle_palette.get_patched_tag_ref(TAG.upgrade_patches)
        vehicle_palette.tag_group = "vehi"

    for equipment_palette in SCENARIO.equipment_palette:
        equipment_palette.get_patched_tag_ref(TAG.upgrade_patches)
        equipment_palette.tag_group = "eqip"

    for weapon_palette in SCENARIO.weapon_palette:
        weapon_palette.get_patched_tag_ref(TAG.upgrade_patches)
        weapon_palette.tag_group = "weap"

    for device_machine_palette in SCENARIO.device_machine_palette:
        device_machine_palette.get_patched_tag_ref(TAG.upgrade_patches)
        device_machine_palette.tag_group = "mach"

    for device_control_palette in SCENARIO.device_control_palette:
        device_control_palette.get_patched_tag_ref(TAG.upgrade_patches)
        device_control_palette.tag_group = "ctrl"

    for device_light_fixtures_palette in SCENARIO.device_light_fixtures_palette:
        device_light_fixtures_palette.get_patched_tag_ref(TAG.upgrade_patches)
        device_light_fixtures_palette.tag_group = "lifi"

    for sound_scenery_palette in SCENARIO.sound_scenery_palette:
        sound_scenery_palette.get_patched_tag_ref(TAG.upgrade_patches)
        sound_scenery_palette.tag_group = "ssce"

    for decal_palette in SCENARIO.decal_palette:
        decal_palette.get_patched_tag_ref(TAG.upgrade_patches)
        decal_palette.tag_group = "deca"

    for detail_object_collection_palette in SCENARIO.detail_object_collection_palette:
        detail_object_collection_palette.get_patched_tag_ref(TAG.upgrade_patches)
        detail_object_collection_palette.tag_group = "dobc"

    for character_palette in SCENARIO.character_palette:
        character_palette.get_patched_tag_ref(TAG.upgrade_patches)
        character_palette.tag_group = "char"

    for crates_palette in SCENARIO.crates_palette:
        crates_palette.get_patched_tag_ref(TAG.upgrade_patches)
        crates_palette.tag_group = "bloc"

    SCENARIO.body_header = TAG.TagBlockHeader("tbfd", 2, 1, 1476)
    SCENARIO.unused_tag_ref = TAG.TagRef("sbsp")
    SCENARIO.skies_tag_block = TAG.TagBlock(len(SCENARIO.skies))
    SCENARIO.scenario_type = H1_ASSET.scenario_type
    SCENARIO.scenario_flags = convert_scenario_flags(H1_ASSET.scenario_flags)
    SCENARIO.child_scenarios_tag_block = TAG.TagBlock(len(SCENARIO.child_scenarios))
    SCENARIO.local_north = H1_ASSET.local_north
    SCENARIO.predicted_resources_tag_block = TAG.TagBlock(len(SCENARIO.predicted_resources))
    SCENARIO.functions_tag_block = TAG.TagBlock(len(SCENARIO.functions))
    SCENARIO.comments_tag_block = TAG.TagBlock(len(SCENARIO.comments))
    SCENARIO.environment_objects_tag_block = TAG.TagBlock(len(SCENARIO.environment_objects))
    SCENARIO.object_names_tag_block = TAG.TagBlock(len(SCENARIO.object_names))
    SCENARIO.scenery_tag_block = TAG.TagBlock(len(SCENARIO.scenery))
    SCENARIO.scenery_palette_tag_block = TAG.TagBlock(len(SCENARIO.scenery_palette))
    SCENARIO.bipeds_tag_block = TAG.TagBlock(len(SCENARIO.bipeds))
    SCENARIO.biped_palette_tag_block = TAG.TagBlock(len(SCENARIO.biped_palette))
    SCENARIO.vehicles_tag_block = TAG.TagBlock(len(SCENARIO.vehicles))
    SCENARIO.vehicle_palette_tag_block = TAG.TagBlock(len(SCENARIO.vehicle_palette))
    SCENARIO.equipment_tag_block = TAG.TagBlock(len(SCENARIO.equipment))
    SCENARIO.equipment_palette_tag_block = TAG.TagBlock(len(SCENARIO.equipment_palette))
    SCENARIO.weapons_tag_block = TAG.TagBlock(len(SCENARIO.weapons))
    SCENARIO.weapon_palette_tag_block = TAG.TagBlock(len(SCENARIO.weapon_palette))
    SCENARIO.device_groups_tag_block = TAG.TagBlock(len(SCENARIO.device_groups))
    SCENARIO.machines_tag_block = TAG.TagBlock(len(SCENARIO.device_machines))
    SCENARIO.machine_palette_tag_block = TAG.TagBlock(len(SCENARIO.device_machine_palette))
    SCENARIO.controls_tag_block = TAG.TagBlock(len(SCENARIO.device_controls))
    SCENARIO.control_palette_tag_block = TAG.TagBlock(len(SCENARIO.device_control_palette))
    SCENARIO.light_fixtures_tag_block = TAG.TagBlock(len(SCENARIO.device_light_fixtures))
    SCENARIO.light_fixtures_palette_tag_block = TAG.TagBlock(len(SCENARIO.device_light_fixtures_palette))
    SCENARIO.sound_scenery_tag_block = TAG.TagBlock(len(SCENARIO.sound_scenery))
    SCENARIO.sound_scenery_palette_tag_block = TAG.TagBlock(len(SCENARIO.sound_scenery_palette))
    SCENARIO.light_volumes_tag_block = TAG.TagBlock(len(SCENARIO.light_volumes))
    SCENARIO.light_volume_palette_tag_block = TAG.TagBlock(len(SCENARIO.light_volume_palette))
    SCENARIO.player_starting_profile_tag_block = TAG.TagBlock(len(SCENARIO.player_starting_profiles))
    SCENARIO.player_starting_locations_tag_block = TAG.TagBlock(len(SCENARIO.player_starting_locations))
    SCENARIO.trigger_volumes_tag_block = TAG.TagBlock(len(SCENARIO.trigger_volumes))
    SCENARIO.recorded_animations_tag_block = TAG.TagBlock(len(SCENARIO.recorded_animations))
    SCENARIO.netgame_flags_tag_block = TAG.TagBlock(len(SCENARIO.netgame_flags))
    SCENARIO.netgame_equipment_tag_block = TAG.TagBlock(len(SCENARIO.netgame_equipment))
    SCENARIO.starting_equipment_tag_block = TAG.TagBlock(len(SCENARIO.starting_equipment))
    SCENARIO.bsp_switch_trigger_volumes_tag_block = TAG.TagBlock(len(SCENARIO.bsp_switch_trigger_volumes))
    SCENARIO.decals_tag_block = TAG.TagBlock(len(SCENARIO.decals))
    SCENARIO.decal_palette_tag_block = TAG.TagBlock(len(SCENARIO.decal_palette))
    SCENARIO.detail_object_collection_palette_tag_block = TAG.TagBlock(len(SCENARIO.detail_object_collection_palette))
    SCENARIO.style_palette_tag_block = TAG.TagBlock(len(SCENARIO.style_palette))
    SCENARIO.squad_groups_tag_block = TAG.TagBlock(len(SCENARIO.squad_groups))
    SCENARIO.squads_tag_block = TAG.TagBlock(len(SCENARIO.squads))
    SCENARIO.zones_tag_block = TAG.TagBlock(len(SCENARIO.zones))
    SCENARIO.mission_scenes_tag_block = TAG.TagBlock(len(SCENARIO.mission_scenes))
    SCENARIO.character_palette_tag_block = TAG.TagBlock(len(SCENARIO.character_palette))
    SCENARIO.ai_pathfinding_data_tag_block = TAG.TagBlock(len(SCENARIO.ai_pathfinding_data))
    SCENARIO.ai_animation_references_tag_block = TAG.TagBlock(len(SCENARIO.ai_animation_references))
    SCENARIO.ai_script_references_tag_block = TAG.TagBlock(len(SCENARIO.ai_script_references))
    SCENARIO.ai_recording_references_tag_block = TAG.TagBlock(len(SCENARIO.ai_recording_references))
    SCENARIO.ai_conversations_tag_block = TAG.TagBlock(len(SCENARIO.ai_conversations))
    SCENARIO.script_syntax_data_tag_data = TAG.RawData()
    SCENARIO.script_string_data_tag_data = TAG.RawData()
    SCENARIO.scripts_tag_block = TAG.TagBlock(len(SCENARIO.scripts))
    SCENARIO.globals_tag_block = TAG.TagBlock(len(SCENARIO.script_globals))
    SCENARIO.references_tag_block = TAG.TagBlock(len(SCENARIO.references))
    SCENARIO.source_files_tag_block = TAG.TagBlock(len(SCENARIO.source_files))
    SCENARIO.scripting_data_tag_block = TAG.TagBlock(len(SCENARIO.scripting_data))
    SCENARIO.cutscene_flags_tag_block = TAG.TagBlock(len(SCENARIO.cutscene_flags))
    SCENARIO.cutscene_camera_points_tag_block = TAG.TagBlock(len(SCENARIO.cutscene_camera_points))
    SCENARIO.cutscene_titles_tag_block = TAG.TagBlock(len(SCENARIO.cutscene_titles))
    SCENARIO.custom_object_names_tag_ref = TAG.TagRef("unic")
    SCENARIO.chapter_title_text_tag_ref = TAG.TagRef("unic")
    SCENARIO.hud_messages_tag_ref = TAG.TagRef("hmt ")
    SCENARIO.structure_bsps_tag_block = TAG.TagBlock(len(SCENARIO.structure_bsps))
    SCENARIO.scenario_resources_tag_block = TAG.TagBlock(len(SCENARIO.scenario_resources))
    SCENARIO.old_structure_physics_tag_block = TAG.TagBlock(len(SCENARIO.old_structure_physics))
    SCENARIO.hs_unit_seats_tag_block =TAG.TagBlock(len(SCENARIO.hs_unit_seats))
    SCENARIO.scenario_kill_triggers_tag_block = TAG.TagBlock(len(SCENARIO.scenario_kill_triggers))
    SCENARIO.hs_syntax_datums_tag_block = TAG.TagBlock(len(SCENARIO.hs_syntax_datums))
    SCENARIO.orders_tag_block = TAG.TagBlock(len(SCENARIO.orders))
    SCENARIO.triggers_tag_block = TAG.TagBlock(len(SCENARIO.triggers))
    SCENARIO.background_sound_palette_tag_block = TAG.TagBlock(len(SCENARIO.background_sound_palette))
    SCENARIO.sound_environment_palette_tag_block = TAG.TagBlock(len(SCENARIO.sound_environment_palette))
    SCENARIO.weather_palette_tag_block = TAG.TagBlock(len(SCENARIO.weather_palette))
    SCENARIO.unused_0_tag_block = TAG.TagBlock(len(SCENARIO.unused_0))
    SCENARIO.unused_1_tag_block = TAG.TagBlock(len(SCENARIO.unused_1))
    SCENARIO.unused_2_tag_block = TAG.TagBlock(len(SCENARIO.unused_2))
    SCENARIO.unused_3_tag_block = TAG.TagBlock(len(SCENARIO.unused_3))
    SCENARIO.scavenger_hunt_objects_tag_block = TAG.TagBlock(len(SCENARIO.scavenger_hunt_objects))
    SCENARIO.scenario_cluster_data_tag_block = TAG.TagBlock(len(SCENARIO.scenario_cluster_data))

    SCENARIO.salt_array = []
    for salt_idx in range(SALT_SIZE):
        SCENARIO.salt_array.append(0)

    SCENARIO.spawn_data_tag_block = TAG.TagBlock(len(SCENARIO.spawn_data))
    SCENARIO.sound_effect_collection_tag_ref = TAG.TagRef("sfx+")
    SCENARIO.crates_tag_block = TAG.TagBlock(len(SCENARIO.crates))
    SCENARIO.crate_palette_tag_block = TAG.TagBlock(len(SCENARIO.crates_palette))
    SCENARIO.global_lighting_tag_ref = TAG.TagRef("gldf")
    SCENARIO.atmospheric_fog_palette_tag_block = TAG.TagBlock(len(SCENARIO.atmospheric_fog_palette))
    SCENARIO.planar_fog_palette_tag_block = TAG.TagBlock(len(SCENARIO.planar_fog_palette))
    SCENARIO.flocks_tag_block = TAG.TagBlock(len(SCENARIO.flocks))
    SCENARIO.subtitles_tag_ref = TAG.TagRef("unic")
    SCENARIO.decorators_tag_block = TAG.TagBlock(len(SCENARIO.decorators))
    SCENARIO.creatures_tag_block = TAG.TagBlock(len(SCENARIO.creatures))
    SCENARIO.creature_palette_tag_block = TAG.TagBlock(len(SCENARIO.creatures_palette))
    SCENARIO.decorator_palette_tag_block = TAG.TagBlock(len(SCENARIO.decorator_palette))
    SCENARIO.bsp_transition_volumes_tag_block = TAG.TagBlock(len(SCENARIO.bsp_transition_volumes))
    SCENARIO.structure_bsp_lighting_tag_block = TAG.TagBlock(len(SCENARIO.structure_bsp_lighting))
    SCENARIO.editor_folders_tag_block = TAG.TagBlock(len(SCENARIO.editor_folders))
    SCENARIO.level_data_tag_block = TAG.TagBlock(len(SCENARIO.level_data))
    SCENARIO.game_engine_strings_tag_ref = TAG.TagRef("unic")
    SCENARIO.mission_dialogue_tag_block = TAG.TagBlock(len(SCENARIO.mission_dialogue))
    SCENARIO.objectives_tag_ref = TAG.TagRef("unic")
    SCENARIO.interpolators_tag_block = TAG.TagBlock(len(SCENARIO.interpolators))
    SCENARIO.shared_references_tag_block = TAG.TagBlock(len(SCENARIO.shared_references))
    SCENARIO.screen_effect_references_tag_block = TAG.TagBlock(len(SCENARIO.screen_effect_references))
    SCENARIO.simulation_definition_table_tag_block = TAG.TagBlock(len(SCENARIO.simulation_definition_table))

    for sky_element in SCENARIO.skies:
        sky_element.get_patched_tag_ref(TAG.upgrade_patches)
        sky_element.tag_group = "sky "

    for scenery_palette in SCENARIO.scenery_palette:
        scenery_palette.get_patched_tag_ref(TAG.upgrade_patches)
        scenery_palette.tag_group = "scen"

    for biped_palette in SCENARIO.biped_palette:
        biped_palette.get_patched_tag_ref(TAG.upgrade_patches)
        biped_palette.tag_group = "bipd"

    for vehicle_palette in SCENARIO.vehicle_palette:
        vehicle_palette.get_patched_tag_ref(TAG.upgrade_patches)
        vehicle_palette.tag_group = "vehi"

    for equipment_palette in SCENARIO.equipment_palette:
        equipment_palette.get_patched_tag_ref(TAG.upgrade_patches)
        equipment_palette.tag_group = "eqip"

    for weapon_palette in SCENARIO.weapon_palette:
        weapon_palette.get_patched_tag_ref(TAG.upgrade_patches)
        weapon_palette.tag_group = "weap"

    for device_machine_palette in SCENARIO.device_machine_palette:
        device_machine_palette.get_patched_tag_ref(TAG.upgrade_patches)
        device_machine_palette.tag_group = "mach"

    for device_control_palette in SCENARIO.device_control_palette:
        device_control_palette.get_patched_tag_ref(TAG.upgrade_patches)
        device_control_palette.tag_group = "ctrl"

    for device_light_fixtures_palette in SCENARIO.device_light_fixtures_palette:
        device_light_fixtures_palette.get_patched_tag_ref(TAG.upgrade_patches)
        device_light_fixtures_palette.tag_group = "lifi"

    for sound_scenery_palette in SCENARIO.sound_scenery_palette:
        sound_scenery_palette.get_patched_tag_ref(TAG.upgrade_patches)
        sound_scenery_palette.tag_group = "ssce"

    for decal_palette in SCENARIO.decal_palette:
        decal_palette.get_patched_tag_ref(TAG.upgrade_patches)
        decal_palette.tag_group = "deca"

    for detail_object_collection_palette in SCENARIO.detail_object_collection_palette:
        detail_object_collection_palette.get_patched_tag_ref(TAG.upgrade_patches)
        detail_object_collection_palette.tag_group = "dobc"

    for character_palette in SCENARIO.character_palette:
        character_palette.get_patched_tag_ref(TAG.upgrade_patches)
        character_palette.tag_group = "char"

    for crates_palette in SCENARIO.crates_palette:
        crates_palette.get_patched_tag_ref(TAG.upgrade_patches)
        crates_palette.tag_group = "bloc"

    return SCENARIO
