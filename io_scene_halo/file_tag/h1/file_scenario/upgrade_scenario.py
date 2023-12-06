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

import bpy
import random

from math import radians
from ....global_functions import tag_format
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
        SALT_SIZE
        )

DEBUG_PARSER = True
DEBUG_HEADER = True
DEBUG_BODY = True

UNIQUE_ID = random.randint(0, 100000)

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

def convert_netgame_flag_type(type_index, usage_id):
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
        if not usage_id > 7:
            if usage_id == 0:
                flag_type = NetGameEnum.king_of_the_hill_0.value

            elif usage_id == 1:
                flag_type = NetGameEnum.king_of_the_hill_1.value

            elif usage_id == 2:
                flag_type = NetGameEnum.king_of_the_hill_2.value

            elif usage_id == 3:
                flag_type = NetGameEnum.king_of_the_hill_3.value

            elif usage_id == 4:
                flag_type = NetGameEnum.king_of_the_hill_4.value

            elif usage_id == 5:
                flag_type = NetGameEnum.king_of_the_hill_5.value

            elif usage_id == 6:
                flag_type = NetGameEnum.king_of_the_hill_6.value

            elif usage_id == 7:
                flag_type = NetGameEnum.king_of_the_hill_7.value

        else:
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

        elif "turret" in collection_name: # We are assuming all turrets are Covenant cause that's all there is in vanilla
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

def get_scenery(scenery_tag_block, TAG, SCENARIO):
    SCENARIO.scenery = []
    for scenery_element in scenery_tag_block:
        scenery = SCENARIO.Scenery()

        scenery.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        scenery.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        scenery.sper_header = TAG.TagBlockHeader("sper", 0, 1, 24)
        scenery.sct3_header = TAG.TagBlockHeader("sct3", 0, 1, 20)

        scenery.palette_index = scenery_element.type_index
        scenery.name_index = scenery_element.name_index
        scenery.placement_flags = convert_object_flags(scenery_element.placement_flags)
        scenery.position = scenery_element.position
        scenery.rotation = tag_format.vector_as_radians(scenery_element.rotation)
        scenery.scale = 0
        scenery.transform_flags = 0
        scenery.manual_bsp_flags = 0
        scenery.unique_id = get_id()
        scenery.origin_bsp_index = -1
        scenery.object_type = 6
        scenery.source = 1
        scenery.bsp_policy = 0
        scenery.editor_folder_index = -1

        scenery.variant_name = ""
        scenery.variant_name_length = len(scenery.variant_name)
        scenery.active_change_colors = 0
        scenery.primary_color_BGRA = (0, 0, 0, 1)
        scenery.secondary_color_BGRA = (0, 0, 0, 1)
        scenery.tertiary_color_BGRA = (0, 0, 0, 1)
        scenery.quaternary_color_BGRA = (0, 0, 0, 1)
        scenery.pathfinding_policy = 0
        scenery.lightmap_policy = 0
        scenery.pathfinding_references = TAG.TagBlock(0, 0, 0, 0)
        scenery.valid_multiplayer_games = 0

        SCENARIO.scenery.append(scenery)

    SCENARIO.scenery_header = TAG.TagBlockHeader("tbfd", 4, len(SCENARIO.scenery), 96)

def get_unit(unit_tag_block, TAG, SCENARIO, is_biped):
    unit_list = []
    for unit_element in unit_tag_block:
        unit = SCENARIO.Unit()

        unit.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        unit.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        unit.sper_header = TAG.TagBlockHeader("sper", 0, 1, 24)
        unit.sunt_header = TAG.TagBlockHeader("sunt", 0, 1, 8)

        unit.palette_index = unit_element.type_index
        unit.name_index = unit_element.name_index
        unit.placement_flags = convert_object_flags(unit_element.placement_flags)
        unit.position = unit_element.position
        unit.rotation = tag_format.vector_as_radians(unit_element.rotation)
        unit.scale = 0
        unit.transform_flags = 0
        unit.manual_bsp_flags = 0
        unit.unique_id = get_id()
        unit.origin_bsp_index = -1
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
        unit.primary_color_BGRA = (0, 0, 0, 1)
        unit.secondary_color_BGRA = (0, 0, 0, 1)
        unit.tertiary_color_BGRA = (0, 0, 0, 1)
        unit.quaternary_color_BGRA = (0, 0, 0, 1)
        unit.body_vitality = unit_element.body_vitality
        unit.flags = unit_element.flags

        unit_list.append(unit)

    return TAG.TagBlockHeader("tbfd", 2, len(unit_list), 84), unit_list

def get_equipment(equipment_tag_block, TAG, SCENARIO):
    SCENARIO.equipment = []
    for equipment_element in equipment_tag_block:
        equipment = SCENARIO.Equipment()

        equipment.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        equipment.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        equipment.seqt_header = TAG.TagBlockHeader("seqt", 0, 1, 4)

        equipment.palette_index = equipment_element.type_index
        equipment.name_index = equipment_element.name_index
        equipment.placement_flags = convert_object_flags(equipment_element.placement_flags)
        equipment.position = equipment_element.position
        equipment.rotation = tag_format.vector_as_radians(equipment_element.rotation)
        equipment.scale = 0
        equipment.transform_flags = 0
        equipment.manual_bsp_flags = 0
        equipment.unique_id = get_id()
        equipment.origin_bsp_index = -1
        equipment.object_type = 3
        equipment.source = 1
        equipment.bsp_policy = 0
        equipment.editor_folder_index = -1

        equipment.flags = equipment_element.misc_flags

        SCENARIO.equipment.append(equipment)

    SCENARIO.equipment_header = TAG.TagBlockHeader("tbfd", 2, len(SCENARIO.equipment), 56)

def get_weapon(weapons_tag_block, TAG, SCENARIO):
    SCENARIO.weapons = []
    for weapon_element in weapons_tag_block:
        weapon = SCENARIO.Weapon()

        weapon.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        weapon.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        weapon.sper_header = TAG.TagBlockHeader("sper", 0, 1, 24)
        weapon.swpt_header = TAG.TagBlockHeader("swpt", 0, 1, 8)

        weapon.palette_index = weapon_element.type_index
        weapon.name_index = weapon_element.name_index
        weapon.placement_flags = convert_object_flags(weapon_element.placement_flags)
        weapon.position = weapon_element.position
        weapon.rotation = tag_format.vector_as_radians(weapon_element.rotation)
        weapon.scale = 0
        weapon.transform_flags = 0
        weapon.manual_bsp_flags = 0
        weapon.unique_id = get_id()
        weapon.origin_bsp_index = -1
        weapon.object_type = 2
        weapon.source = 1
        weapon.bsp_policy = 0
        weapon.editor_folder_index = -1

        weapon.variant_name = ""
        weapon.variant_name_length = len(weapon.variant_name)
        weapon.active_change_colors = 0
        weapon.primary_color_BGRA = (0, 0, 0, 1)
        weapon.secondary_color_BGRA = (0, 0, 0, 1)
        weapon.tertiary_color_BGRA = (0, 0, 0, 1)
        weapon.quaternary_color_BGRA = (0, 0, 0, 1)
        weapon.rounds_left = weapon_element.rounds_left
        weapon.rounds_loaded = weapon_element.rounds_loaded
        weapon.flags = weapon_element.flags

        SCENARIO.weapons.append(weapon)

    SCENARIO.weapon_header = TAG.TagBlockHeader("tbfd", 2, len(SCENARIO.weapons), 84)

def get_device_groups(device_groups_tag_block, TAG, SCENARIO):
    SCENARIO.device_groups = []
    for device_group_element in device_groups_tag_block:
        device_group = SCENARIO.DeviceGroup()
        device_group.name = device_group_element.name
        device_group.initial_value = device_group_element.initial_value
        device_group.flags = device_group_element.flags

        SCENARIO.device_groups.append(device_group)

    SCENARIO.device_group_header = TAG.TagBlockHeader("tbfd", 0, len(SCENARIO.device_groups), 40)

def get_device_machines(machine_tag_block, TAG, SCENARIO):
    SCENARIO.device_machines = []
    for machine_element in machine_tag_block:
        device_machine = SCENARIO.DeviceMachine()

        device_machine.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        device_machine.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        device_machine.sdvt_header = TAG.TagBlockHeader("sdvt", 0, 1, 8)
        device_machine.smht_header = TAG.TagBlockHeader("smht", 0, 1, 16)

        device_machine.palette_index = machine_element.type_index
        device_machine.name_index = machine_element.name_index
        device_machine.placement_flags = convert_object_flags(machine_element.placement_flags)
        device_machine.position = machine_element.position
        device_machine.rotation = tag_format.vector_as_radians(machine_element.rotation)
        device_machine.scale = 0
        device_machine.transform_flags = 0
        device_machine.manual_bsp_flags = 0
        device_machine.unique_id = get_id()
        device_machine.origin_bsp_index = -1
        device_machine.object_type = 7
        device_machine.source = 1
        device_machine.bsp_policy = 0
        device_machine.editor_folder_index = -1

        device_machine.power_group_index = machine_element.power_group_index
        device_machine.position_group_index = machine_element.position_group_index
        device_machine.flags_0 = machine_element.flags_0
        device_machine.flags_1 = machine_element.flags_1
        device_machine.pathfinding_references = TAG.TagBlock(0, 0, 0, 0)

        SCENARIO.device_machines.append(device_machine)

    SCENARIO.device_machine_header = TAG.TagBlockHeader("tbfd", 3, len(SCENARIO.device_machines), 76)

def get_device_controls(controls_tag_block, TAG, SCENARIO):
    SCENARIO.device_controls = []
    for control_element in controls_tag_block:
        device_control = SCENARIO.DeviceControl()

        device_control.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        device_control.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        device_control.sdvt_header = TAG.TagBlockHeader("sdvt", 0, 1, 8)
        device_control.sctt_header = TAG.TagBlockHeader("sctt", 0, 1, 8)

        device_control.palette_index = control_element.type_index
        device_control.name_index = control_element.name_index
        device_control.placement_flags = convert_object_flags(control_element.placement_flags)
        device_control.position = control_element.position
        device_control.rotation = tag_format.vector_as_radians(control_element.rotation)
        device_control.scale = 0
        device_control.transform_flags = 0
        device_control.manual_bsp_flags = 0
        device_control.unique_id = get_id()
        device_control.origin_bsp_index = -1
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


def get_light_fixtures(light_fixtures_tag_block, TAG, SCENARIO):
    SCENARIO.light_fixtures = []
    for light_fixture_element in light_fixtures_tag_block:
        light_fixture = SCENARIO.LightFixture()

        light_fixture.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        light_fixture.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        light_fixture.sdvt_header = TAG.TagBlockHeader("sdvt", 0, 1, 8)
        light_fixture.slft_header = TAG.TagBlockHeader("slft", 0, 1, 24)

        light_fixture.palette_index = light_fixture_element.type_index
        light_fixture.name_index = light_fixture_element.name_index
        light_fixture.placement_flags = convert_object_flags(light_fixture_element.placement_flags)
        light_fixture.position = light_fixture_element.position
        light_fixture.rotation = tag_format.vector_as_radians(light_fixture_element.rotation)
        light_fixture.scale = 0
        light_fixture.transform_flags = 0
        light_fixture.manual_bsp_flags = 0
        light_fixture.unique_id = get_id()
        light_fixture.origin_bsp_index = -1
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

        SCENARIO.light_fixtures.append(light_fixture)

    SCENARIO.light_fixture_header = TAG.TagBlockHeader("tbfd", 2, len(SCENARIO.light_fixtures), 84)

def get_sound_scenery(sound_scenery_tag_block, TAG, SCENARIO):
    SCENARIO.sound_scenery = []
    for sound_scenery_element in sound_scenery_tag_block:
        sound_scenery = SCENARIO.SoundScenery()

        sound_scenery.sobj_header = TAG.TagBlockHeader("sobj", 1, 1, 48)
        sound_scenery.obj0_header = TAG.TagBlockHeader("obj#", 0, 1, 8)
        sound_scenery._sc__header = TAG.TagBlockHeader("#sc#", 0, 1, 28)

        sound_scenery.palette_index = sound_scenery_element.type_index
        sound_scenery.name_index = sound_scenery_element.name_index
        sound_scenery.placement_flags = convert_object_flags(sound_scenery_element.placement_flags)
        sound_scenery.position = sound_scenery_element.position
        sound_scenery.rotation = tag_format.vector_as_radians(sound_scenery_element.rotation)
        sound_scenery.scale = 0
        sound_scenery.transform_flags = 0
        sound_scenery.manual_bsp_flags = 0
        sound_scenery.unique_id = get_id()
        sound_scenery.origin_bsp_index = -1
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
    SCENARIO.player_starting_profiles = []
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

    SCENARIO.player_starting_profile_header = TAG.TagBlockHeader("tbfd", 0, len(SCENARIO.player_starting_profiles), 84)

def get_player_starting_locations(player_starting_locations_tag_block, TAG, SCENARIO):
    SCENARIO.player_starting_locations = []
    for player_starting_location_element in player_starting_locations_tag_block:
        if not player_starting_location_element.team_index > 1: # CE only has two teams so ignore everything above 1
            player_starting_location = SCENARIO.PlayerStartingLocation()

            player_starting_location.position = player_starting_location_element.position
            player_starting_location.facing = radians(player_starting_location_element.facing)
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
    SCENARIO.trigger_volumes = []
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
    SCENARIO.recorded_animations = []
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
    SCENARIO.netgame_flags = []
    for netgame_flag_element in netgame_flags_tag_block:
        flag_type, team_designator, identifer, flags, is_valid, needs_return = convert_netgame_flag_type(netgame_flag_element.type, netgame_flag_element.usage_id)

        if is_valid:
            netgame_flag = SCENARIO.NetGameFlag()

            netgame_flag.position = netgame_flag_element.position
            netgame_flag.facing = radians(netgame_flag_element.facing)
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
            netgame_flag.facing = radians(netgame_flag_element.facing)
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
    SCENARIO.netgame_equipment = []
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
        netgame_equipment.orientation = (0.0, 0.0, radians(netgame_equipment_element.facing))

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
            netgame_equipment.orientation = tag_format.vector_as_radians(vehicle_element.rotation)

            item_collection_tag_group = "vehc"
            item_collection_tag_path = vehicle_palette_tag_block[vehicle_element.type_index].name
            netgame_equipment.item_vehicle_collection = TAG.TagRef(item_collection_tag_group, item_collection_tag_path, len(item_collection_tag_path), upgrade_patches=TAG.upgrade_patches)

            SCENARIO.netgame_equipment.append(netgame_equipment)

    SCENARIO.netgame_equipment_header = TAG.TagBlockHeader("tbfd", 0, len(SCENARIO.netgame_equipment), 152)

def get_starting_equipment(starting_equipment_tag_block, TAG, SCENARIO):
    SCENARIO.starting_equipment = []
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
    SCENARIO.decals = []
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

    SCENARIO.zones = []
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
                firing_position.normal_y = 0.0
                firing_position.normal_p = radians(90)

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
    for weapon in SCENARIO.weapon_palette:
        weapon_tag_path = weapon.name
        character_tag_paths.append(weapon_tag_path)

    for actor in actors_palette_tag_block:
        actor_tag = actor.parse_tag(report, "halo1", "retail")
        if not actor_tag == None:
            actor_weapon_tag = actor_tag.actor_variant_body.weapon
            actor_weapon_name = actor_weapon_tag.name
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

    character_weapon_palette_header, character_weapons = get_palette(TAG, weapon_tags, 48)

    SCENARIO.weapon_palette = SCENARIO.weapon_palette + character_weapons
    SCENARIO.weapon_palette_header = TAG.TagBlockHeader("tbfd", 0, len(SCENARIO.weapon_palette), 48)

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
        for squad_element in encounter_element.squads:
            starting_location_count = squad_element.starting_locations_tag_block.count

            actor_weapon = actor_weapon_paths[squad_element.actor_type]

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
            if not actor_weapon == None:
                squad.initial_weapon_index = character_tag_paths.index(actor_weapon)

            squad.initial_secondary_weapon_index = -1
            squad.grenade_type = 0
            squad.initial_order_index = -1
            squad.vehicle_variant = ""
            squad.starting_locations_tag_block = TAG.TagBlock(starting_location_count, 0, 0, 0)
            squad.placement_script = ""
            squad.starting_locations = []

            if len(encounter_element.firing_positions) > 0:
                encounter_index += 1

            if starting_location_count > 0:
                squad.starting_locations_header = TAG.TagBlockHeader("tbfd", 6, starting_location_count, 100)
                for starting_location_idx, starting_location_element in enumerate(squad_element.starting_locations):
                    starting_location = SCENARIO.StartingLocation()

                    starting_location_name = "starting_locations_%s" % starting_location_idx
                    starting_location.name = starting_location_name
                    starting_location.name_length = len(starting_location.name)
                    starting_location.position = starting_location_element.position
                    starting_location.reference_frame = -1
                    starting_location.facing_y = radians(starting_location_element.facing)
                    starting_location.facing_p = 0

                    starting_location.flags = 0
                    starting_location.character_type_index = -1
                    starting_location.initial_weapon_index = -1
                    starting_location.initial_secondary_weapon_index = -1
                    starting_location.vehicle_type_index = -1
                    starting_location.seat_type = 0
                    starting_location.grenade_type = 0
                    starting_location.swarm_count = 0
                    starting_location.actor_variant = ""
                    starting_location.vehicle_variant = ""
                    starting_location.initial_movement_distance = 0
                    starting_location.emitter_vehicle_index = -1
                    starting_location.initial_movement_mode = 0
                    starting_location.placement_script = ""

                    squad.starting_locations.append(starting_location)

            SCENARIO.squads.append(squad)

    SCENARIO.squads_header = TAG.TagBlockHeader("tbfd", 2, len(SCENARIO.squads), 120)

    SCENARIO.character_palette_header, SCENARIO.character_palette = get_palette(TAG, actors_palette_tag_block, 16, "char")

def generate_point_sets(H1_ASSET, TAG, SCENARIO, report):
    SCENARIO.scripting_data = []

    for script_data_idx in range(1):
        scripting_data = SCENARIO.ScriptingData()

        scripting_data.point_sets = []
        object_list = [bpy.data.objects["dropship01"]]
        for obj in object_list:
            point_set = SCENARIO.PointSet()

            point_set.name = obj.name
            point_set.bsp_index = 0
            point_set.manual_reference_frame = 0
            point_set.flags = 0
            point_set.points = []
            for vertex_idx, vertex in enumerate(obj.data.vertices):
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
        cutscene_flags = SCENARIO.CutsceneFlags()

        cutscene_flags.name = cutscene_flag_element.name
        cutscene_flags.position = cutscene_flag_element.position
        cutscene_flags.facing_y = radians(cutscene_flag_element.facing[0])
        cutscene_flags.facing_p = radians(cutscene_flag_element.facing[1])

        SCENARIO.cutscene_flags.append(cutscene_flags)

    SCENARIO.cutscene_flags_header = TAG.TagBlockHeader("tbfd", 0, len(SCENARIO.cutscene_flags), 56)

def get_cutscene_camera_points(cutscene_camera_points_tag_block, TAG, SCENARIO):
    SCENARIO.cutscene_camera_points = []
    for cutscene_camera_point_element in cutscene_camera_points_tag_block:
        cutscene_camera_point = SCENARIO.CutsceneCameraPoints()

        cutscene_camera_point.flags = 0
        cutscene_camera_point.camera_type = 0
        cutscene_camera_point.name = cutscene_camera_point_element.name
        cutscene_camera_point.position = cutscene_camera_point_element.position
        cutscene_camera_point.orientation = tag_format.vector_as_radians(cutscene_camera_point_element.orientation)

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
    SCENARIO.structure_bsp = []
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

        SCENARIO.structure_bsp.append(structure_bsp)

    SCENARIO.structure_bsp_header = TAG.TagBlockHeader("tbfd", 1, len(SCENARIO.structure_bsp), 84)

def get_palette(TAG, palette_tag_block, size, tag_group=None):
    palette_list = []
    tag_group_name = tag_group
    for palette_element in palette_tag_block:
        if tag_group == None:
            tag_group_name = palette_element.tag_group

        tag_group = tag_group_name
        tag_path = palette_element.name

        palette_list.append(TAG.TagRef(tag_group, tag_path, len(tag_path), upgrade_patches=TAG.upgrade_patches))

    return TAG.TagBlockHeader("tbfd", 0, len(palette_list), size), palette_list

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
    SCENARIO.comments = []
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
    SCENARIO.light_fixtures = []
    SCENARIO.light_fixtures_palette = []
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
    SCENARIO.decals = []
    SCENARIO.decal_palette = []
    SCENARIO.style_palette = []
    SCENARIO.squad_groups = []
    SCENARIO.squads = []
    SCENARIO.zones = []
    SCENARIO.character_palette = []
    SCENARIO.scripting_data = []
    SCENARIO.cutscene_flags = []
    SCENARIO.cutscene_camera_points = []
    SCENARIO.orders = []
    SCENARIO.triggers = []
    SCENARIO.background_sound_palette = []
    SCENARIO.sound_environment_palette = []
    SCENARIO.crates = []
    SCENARIO.crates_palette = []

    SCENARIO.skies_header, SCENARIO.skies = get_palette(TAG, H1_ASSET.skies, 16)

    SCENARIO.child_scenario_header, SCENARIO.child_scenarios = get_palette(TAG, H1_ASSET.child_scenarios, 32)

    get_comments(H1_ASSET.comments, TAG, SCENARIO)

    get_object_names(H1_ASSET.object_names, TAG, SCENARIO)

    get_scenery(H1_ASSET.scenery, TAG, SCENARIO)
    SCENARIO.scenery_palette_header, SCENARIO.scenery_palette = get_palette(TAG, H1_ASSET.scenery_palette, 48)

    SCENARIO.bipeds_header, SCENARIO.bipeds = get_unit(H1_ASSET.bipeds, TAG, SCENARIO, True)
    SCENARIO.biped_palette_header, SCENARIO.biped_palette = get_palette(TAG, H1_ASSET.biped_palette, 48)

    if not H1ScenarioTypeEnum(H1_ASSET.scenario_body.scenario_type) == H1ScenarioTypeEnum.multiplayer:
        SCENARIO.vehicles_header, SCENARIO.vehicles = get_unit(H1_ASSET.vehicles, TAG, SCENARIO, False)
        SCENARIO.vehicle_palette_header, SCENARIO.vehicle_palette = get_palette(TAG, H1_ASSET.vehicle_palette, 48)

    get_equipment(H1_ASSET.equipment, TAG, SCENARIO)
    SCENARIO.equipment_palette_header, SCENARIO.equipment_palette = get_palette(TAG, H1_ASSET.equipment_palette, 48)

    get_weapon(H1_ASSET.weapons, TAG, SCENARIO)
    SCENARIO.weapon_palette_header, SCENARIO.weapon_palette = get_palette(TAG, H1_ASSET.weapon_palette, 48)

    get_device_groups(H1_ASSET.device_groups, TAG, SCENARIO)

    get_device_machines(H1_ASSET.device_machines, TAG, SCENARIO)
    SCENARIO.device_machine_palette_header, SCENARIO.device_machine_palette = get_palette(TAG, H1_ASSET.device_machine_palette, 48)

    get_device_controls(H1_ASSET.device_controls, TAG, SCENARIO)
    SCENARIO.device_control_palette_header, SCENARIO.device_control_palette = get_palette(TAG, H1_ASSET.device_control_palette, 48)

    get_light_fixtures(H1_ASSET.device_light_fixtures, TAG, SCENARIO)
    SCENARIO.light_fixture_palette_header, SCENARIO.light_fixtures_palette = get_palette(TAG, H1_ASSET.device_light_fixtures_palette, 48)

    get_sound_scenery(H1_ASSET.sound_scenery, TAG, SCENARIO)
    SCENARIO.sound_scenery_palette_header, SCENARIO.sound_scenery_palette = get_palette(TAG, H1_ASSET.sound_scenery_palette, 48)

    get_player_starting_profiles(H1_ASSET.player_starting_profiles, TAG, SCENARIO)

    get_player_starting_locations(H1_ASSET.player_starting_locations, TAG, SCENARIO)

    get_trigger_volumes(H1_ASSET.trigger_volumes, TAG, SCENARIO)

    get_recorded_animations(H1_ASSET.recorded_animations, TAG, SCENARIO)

    get_netgame_flags(H1_ASSET.netgame_flags, TAG, SCENARIO)

    get_netgame_equipment(H1_ASSET.netgame_equipment, H1_ASSET.vehicles, H1_ASSET.vehicle_palette, H1_ASSET.scenario_body.scenario_type, TAG, SCENARIO)

    get_starting_equipment(H1_ASSET.starting_equipment, TAG, SCENARIO)

    get_decals(H1_ASSET.decals, TAG, SCENARIO)
    SCENARIO.decal_palette_header, SCENARIO.decal_palette = get_palette(TAG, H1_ASSET.decal_palette, 16)

    generate_h2_squads(H1_ASSET, TAG, SCENARIO, report)

    if False:
        generate_point_sets(H1_ASSET, TAG, SCENARIO, report)

    get_cutscene_flags(H1_ASSET.cutscene_flags, TAG, SCENARIO)

    get_cutscene_camera_points(H1_ASSET.cutscene_camera_points, TAG, SCENARIO)

    get_cutscene_titles(H1_ASSET.cutscene_titles, TAG, SCENARIO)

    get_structure_bsp(H1_ASSET.structure_bsps, TAG, SCENARIO)

    SCENARIO.scenario_body_header = TAG.TagBlockHeader("tbfd", 2, 1, 1476)
    SCENARIO.scenario_body = SCENARIO.ScenarioBody()
    SCENARIO.scenario_body.unused_tag_ref = TAG.TagRef("sbsp")
    SCENARIO.scenario_body.skies_tag_block = TAG.TagBlock(len(SCENARIO.skies), 0, 0, 0)
    SCENARIO.scenario_body.scenario_type = H1_ASSET.scenario_body.scenario_type
    SCENARIO.scenario_body.scenario_flags = convert_scenario_flags(H1_ASSET.scenario_body.scenario_flags)
    SCENARIO.scenario_body.child_scenarios_tag_block = TAG.TagBlock(len(SCENARIO.child_scenarios), 0, 0, 0)
    SCENARIO.scenario_body.local_north = radians(H1_ASSET.scenario_body.local_north) # Value in radians
    SCENARIO.scenario_body.predicted_resources_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.functions_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.editor_scenario_data = TAG.RawData(0, 0, 0, 0, 0)
    SCENARIO.scenario_body.comments_tag_block = TAG.TagBlock(len(SCENARIO.comments), 0, 0, 0)
    SCENARIO.scenario_body.environment_objects_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.object_names_tag_block = TAG.TagBlock(len(SCENARIO.object_names), 0, 0, 0)
    SCENARIO.scenario_body.scenery_tag_block = TAG.TagBlock(len(SCENARIO.scenery), 0, 0, 0)
    SCENARIO.scenario_body.scenery_palette_tag_block = TAG.TagBlock(len(SCENARIO.scenery_palette), 0, 0, 0)
    SCENARIO.scenario_body.bipeds_tag_block = TAG.TagBlock(len(SCENARIO.bipeds), 0, 0, 0)
    SCENARIO.scenario_body.biped_palette_tag_block = TAG.TagBlock(len(SCENARIO.biped_palette), 0, 0, 0)
    SCENARIO.scenario_body.vehicles_tag_block = TAG.TagBlock(len(SCENARIO.vehicles), 0, 0, 0)
    SCENARIO.scenario_body.vehicle_palette_tag_block = TAG.TagBlock(len(SCENARIO.vehicle_palette), 0, 0, 0)
    SCENARIO.scenario_body.equipment_tag_block = TAG.TagBlock(len(SCENARIO.equipment), 0, 0, 0)
    SCENARIO.scenario_body.equipment_palette_tag_block = TAG.TagBlock(len(SCENARIO.equipment_palette), 0, 0, 0)
    SCENARIO.scenario_body.weapons_tag_block = TAG.TagBlock(len(SCENARIO.weapons), 0, 0, 0)
    SCENARIO.scenario_body.weapon_palette_tag_block = TAG.TagBlock(len(SCENARIO.weapon_palette), 0, 0, 0)
    SCENARIO.scenario_body.device_groups_tag_block = TAG.TagBlock(len(SCENARIO.device_groups), 0, 0, 0)
    SCENARIO.scenario_body.machines_tag_block = TAG.TagBlock(len(SCENARIO.device_machines), 0, 0, 0)
    SCENARIO.scenario_body.machine_palette_tag_block = TAG.TagBlock(len(SCENARIO.device_machine_palette), 0, 0, 0)
    SCENARIO.scenario_body.controls_tag_block = TAG.TagBlock(len(SCENARIO.device_controls), 0, 0, 0)
    SCENARIO.scenario_body.control_palette_tag_block = TAG.TagBlock(len(SCENARIO.device_control_palette), 0, 0, 0)
    SCENARIO.scenario_body.light_fixtures_tag_block = TAG.TagBlock(len(SCENARIO.light_fixtures), 0, 0, 0)
    SCENARIO.scenario_body.light_fixtures_palette_tag_block = TAG.TagBlock(len(SCENARIO.light_fixtures_palette), 0, 0, 0)
    SCENARIO.scenario_body.sound_scenery_tag_block = TAG.TagBlock(len(SCENARIO.sound_scenery), 0, 0, 0)
    SCENARIO.scenario_body.sound_scenery_palette_tag_block = TAG.TagBlock(len(SCENARIO.sound_scenery_palette), 0, 0, 0)
    SCENARIO.scenario_body.light_volumes_tag_block = TAG.TagBlock(len(SCENARIO.light_volumes), 0, 0, 0)
    SCENARIO.scenario_body.light_volume_palette_tag_block = TAG.TagBlock(len(SCENARIO.light_volume_palette), 0, 0, 0)
    SCENARIO.scenario_body.player_starting_profile_tag_block = TAG.TagBlock(len(SCENARIO.player_starting_profiles), 0, 0, 0)
    SCENARIO.scenario_body.player_starting_locations_tag_block = TAG.TagBlock(len(SCENARIO.player_starting_locations), 0, 0, 0)
    SCENARIO.scenario_body.trigger_volumes_tag_block = TAG.TagBlock(len(SCENARIO.trigger_volumes), 0, 0, 0)
    SCENARIO.scenario_body.recorded_animations_tag_block = TAG.TagBlock(len(SCENARIO.recorded_animations), 0, 0, 0)
    SCENARIO.scenario_body.netgame_flags_tag_block = TAG.TagBlock(len(SCENARIO.netgame_flags), 0, 0, 0)
    SCENARIO.scenario_body.netgame_equipment_tag_block = TAG.TagBlock(len(SCENARIO.netgame_equipment), 0, 0, 0)
    SCENARIO.scenario_body.starting_equipment_tag_block = TAG.TagBlock(len(SCENARIO.starting_equipment), 0, 0, 0)
    SCENARIO.scenario_body.bsp_switch_trigger_volumes_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.decals_tag_block = TAG.TagBlock(len(SCENARIO.decals), 0, 0, 0)
    SCENARIO.scenario_body.decal_palette_tag_block = TAG.TagBlock(len(SCENARIO.decal_palette), 0, 0, 0)
    SCENARIO.scenario_body.detail_object_collection_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.style_palette_tag_block = TAG.TagBlock(len(SCENARIO.style_palette), 0, 0, 0)
    SCENARIO.scenario_body.squad_groups_tag_block = TAG.TagBlock(len(SCENARIO.squad_groups), 0, 0, 0)
    SCENARIO.scenario_body.squads_tag_block = TAG.TagBlock(len(SCENARIO.squads), 0, 0, 0)
    SCENARIO.scenario_body.zones_tag_block = TAG.TagBlock(len(SCENARIO.zones), 0, 0, 0)
    SCENARIO.scenario_body.mission_scenes_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.character_palette_tag_block = TAG.TagBlock(len(SCENARIO.character_palette), 0, 0, 0)
    SCENARIO.scenario_body.ai_pathfinding_data_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.ai_animation_references_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.ai_script_references_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.ai_recording_references_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.ai_conversations_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.script_syntax_data_tag_data = TAG.RawData(0, 0, 0, 0, 0)
    SCENARIO.scenario_body.script_string_data_tag_data = TAG.RawData(0, 0, 0, 0, 0)
    SCENARIO.scenario_body.scripts_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.globals_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.references_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.source_files_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.scripting_data_tag_block = TAG.TagBlock(len(SCENARIO.scripting_data), 0, 0, 0)
    SCENARIO.scenario_body.cutscene_flags_tag_block = TAG.TagBlock(len(SCENARIO.cutscene_flags), 0, 0, 0)
    SCENARIO.scenario_body.cutscene_camera_points_tag_block = TAG.TagBlock(len(SCENARIO.cutscene_camera_points), 0, 0, 0)
    SCENARIO.scenario_body.cutscene_titles_tag_block = TAG.TagBlock(len(SCENARIO.cutscene_titles), 0, 0, 0)
    SCENARIO.scenario_body.custom_object_names_tag_ref = TAG.TagRef("unic")
    SCENARIO.scenario_body.chapter_title_text_tag_ref = TAG.TagRef("unic")
    SCENARIO.scenario_body.hud_messages_tag_ref = TAG.TagRef("hmt ")
    SCENARIO.scenario_body.structure_bsps_tag_block = TAG.TagBlock(len(SCENARIO.structure_bsp), 0, 0, 0)
    SCENARIO.scenario_body.scenario_resources_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.old_structure_physics_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.hs_unit_seats_tag_block =TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.scenario_kill_triggers_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.hs_syntax_datums_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.orders_tag_block = TAG.TagBlock(len(SCENARIO.orders), 0, 0, 0)
    SCENARIO.scenario_body.triggers_tag_block = TAG.TagBlock(len(SCENARIO.triggers), 0, 0, 0)
    SCENARIO.scenario_body.background_sound_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.sound_environment_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.weather_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.unused_0_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.unused_1_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.unused_2_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.unused_3_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.scavenger_hunt_objects_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.scenario_cluster_data_tag_block = TAG.TagBlock(0, 0, 0, 0)

    SCENARIO.scenario_body.salt_array = []
    for salt_idx in range(SALT_SIZE):
        SCENARIO.scenario_body.salt_array.append(0)

    SCENARIO.scenario_body.spawn_data_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.sound_effect_collection_tag_ref = TAG.TagRef("sfx+")
    SCENARIO.scenario_body.crates_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.crate_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.global_lighting_tag_ref = TAG.TagRef("gldf")
    SCENARIO.scenario_body.atmospheric_fog_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.planar_fog_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.flocks_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.subtitles_tag_ref = TAG.TagRef("unic")
    SCENARIO.scenario_body.decorators_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.creatures_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.creature_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.decorator_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.bsp_transition_volumes_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.structure_bsp_lighting_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.editor_folders_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.level_data_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.game_engine_strings_tag_ref = TAG.TagRef("unic")
    SCENARIO.scenario_body.mission_dialogue_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.objectives_tag_ref = TAG.TagRef("unic")
    SCENARIO.scenario_body.interpolators_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.shared_references_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.screen_effect_references_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.simulation_definition_table_tag_block = TAG.TagBlock(0, 0, 0, 0)

    return SCENARIO
