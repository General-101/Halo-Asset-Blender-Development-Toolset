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

from xml.dom import minidom
from ....global_functions import tag_format
from .format import (
        ScenarioAsset,
        ScenarioTypeEnum,
        ScenarioFlags,
        ResourceTypeEnum,
        FunctionFlags,
        FunctionEnum,
        MapEnum,
        BoundsModeEnum,
        ObjectFlags,
        UnitFlags,
        VehicleFlags,
        ItemFlags,
        DeviceGroupFlags,
        DeviceFlags,
        MachineFlags,
        ControlFlags,
        GametypeEnum,
        NetGameEnum,
        NetGameEquipment,
        StartingEquipment,
        EncounterFlags,
        TeamEnum,
        SearchBehaviorEnum,
        GroupEnum,
        PlatoonFlags,
        PlatoonStrengthEnum,
        StateEnum,
        SquadFlags,
        LeaderEnum,
        GroupFlags,
        MajorUpgradeEnum,
        CommandListFlags,
        AtomTypeEnum,
        AIConversationFlags,
        ParticipantFlags,
        SelectionTypeEnum,
        ActorTypeEnum,
        LineFlags,
        AddresseeEnum,
        ScriptTypeEnum,
        ReturnTypeEnum,
        StyleEnum,
        JustificationEnum,
        TextFlags
        )

XML_OUTPUT = False

def get_predicted_resource(input_stream, SCENARIO, TAG, node_element):
    predicted_resource = SCENARIO.PredictedResource()
    predicted_resource.tag_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type", ResourceTypeEnum))
    predicted_resource.resource_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "resource index"))
    predicted_resource.tag_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "tag index"))

    return predicted_resource

def get_functions(input_stream, SCENARIO, TAG, node_element):
    function = SCENARIO.Function()
    function.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", FunctionFlags))
    function.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    function.period = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "period"))
    function.scale_period_by = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "scale period by", None, SCENARIO.functions_tag_block.count, "scenario_function_block"))
    function.function_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "function", FunctionEnum))
    function.scale_function_by = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "scale function by", None, SCENARIO.functions_tag_block.count, "scenario_function_block"))
    function.wobble_function_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "function", FunctionEnum))
    function.wobble_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "wobble period"))
    function.wobble_magnitude = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "wobble magnitude"))
    function.square_wave_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "square wave threshold"))
    function.step_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "step count"))
    function.map_to = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "map to", MapEnum))
    function.sawtooth_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "sawtooth count"))
    input_stream.read(2) # Padding?
    function.scale_result_by = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "scale result by", None, SCENARIO.functions_tag_block.count, "scenario_function_block"))
    function.bounds_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "bounds mode", BoundsModeEnum))
    function.bounds = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(node_element, "bounds"))
    input_stream.read(6) # Padding?
    function.turn_off_with = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "turn off with", None, SCENARIO.functions_tag_block.count, "scenario_function_block"))
    input_stream.read(32) # Padding?

    return function

def get_comments(input_stream, SCENARIO, TAG, node_element):
    comment = SCENARIO.Comment()
    comment.position = TAG.read_point_3d(input_stream, TAG,  tag_format.XMLData(node_element, "translation"))
    input_stream.read(16) # Padding?
    comment.data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(node_element, "editor scenario data"))

    return comment

def get_scavenger_hunt_objects(input_stream, SCENARIO, TAG, node_element):
    scanvenger_hunt_object = SCENARIO.ScanvengerHuntObject()
    scanvenger_hunt_object.exported_name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "exported name"))
    scanvenger_hunt_object.scenario_object_name_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "scenario object name index", None, SCENARIO.object_names_tag_block.count, "scenario_object_names_block"))
    input_stream.read(2) # Padding?

    return scanvenger_hunt_object

def get_object_names(input_stream, SCENARIO, TAG, node_element):
    object_name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    input_stream.read(4)

    return object_name

def get_scenery(input_stream, SCENARIO, TAG, node_element):
    scenery = SCENARIO.Object()
    scenery.type_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "type", None, SCENARIO.scenery_palette_tag_block.count, "scenario_scenery_palette_block"))
    scenery.name_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "name", None, SCENARIO.object_names_tag_block.count, "scenario_object_names_block"))
    scenery.placement_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "not placed", ObjectFlags))
    scenery.desired_permutation = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "desired permutation"))
    scenery.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    scenery.rotation = TAG.read_euler_angles(input_stream, TAG, tag_format.XMLData(node_element, "rotation"))
    input_stream.read(4) # Padding?
    scenery.appearance_player_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "appearance player index"))
    input_stream.read(35) # Padding?

    return scenery

def get_bipeds(input_stream, SCENARIO, TAG, node_element):
    unit = SCENARIO.Unit()
    unit.type_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "type", None, SCENARIO.biped_palette_tag_block.count, "scenario_biped_palette_block"))
    unit.name_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "name", None, SCENARIO.object_names_tag_block.count, "scenario_object_names_block"))
    unit.placement_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "not placed", ObjectFlags))
    unit.desired_permutation = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "desired permutation"))
    unit.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    unit.rotation = TAG.read_euler_angles(input_stream, TAG, tag_format.XMLData(node_element, "rotation"))
    input_stream.read(4) # Padding?
    unit.appearance_player_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "appearance player index"))
    input_stream.read(35) # Padding?
    unit.body_vitality = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "body vitality"))
    unit.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", UnitFlags))
    input_stream.read(40) # Padding?

    return unit

def get_vehicles(input_stream, SCENARIO, TAG, node_element):
    unit = SCENARIO.Vehicle()
    unit.type_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "type", None, SCENARIO.vehicle_palette_tag_block.count, "scenario_vehicle_palette_block"))
    unit.name_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "name", None, SCENARIO.object_names_tag_block.count, "scenario_object_names_block"))
    unit.placement_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "not placed", ObjectFlags))
    unit.desired_permutation = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "desired permutation"))
    unit.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    unit.rotation = TAG.read_euler_angles(input_stream, TAG, tag_format.XMLData(node_element, "rotation"))
    input_stream.read(4) # Padding?
    unit.appearance_player_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "appearance player index"))
    input_stream.read(35) # Padding?
    unit.body_vitality = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "body vitality"))
    unit.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", UnitFlags))
    input_stream.read(8) # Padding?
    unit.multiplayer_team_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "multiplayer team index"))
    input_stream.read(1) # Padding?
    unit.multiplayer_spawn_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "multiplayer spawn flags", VehicleFlags))
    input_stream.read(28) # Padding?

    return unit

def get_equipment(input_stream, SCENARIO, TAG, node_element):
    equipment = SCENARIO.Equipment()
    equipment.type_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "type", None, SCENARIO.equipment_palette_tag_block.count, "scenario_equipment_palette_block"))
    equipment.name_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "name", None, SCENARIO.object_names_tag_block.count, "scenario_object_names_block"))
    equipment.placement_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "not placed", ObjectFlags))
    equipment.desired_permutation = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "desired permutation"))
    equipment.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    equipment.rotation = TAG.read_euler_angles(input_stream, TAG, tag_format.XMLData(node_element, "rotation"))
    equipment.misc_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "misc flags", ItemFlags))
    equipment.appearance_player_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "appearance player index"))
    input_stream.read(3) # Padding?

    return equipment

def get_weapons(input_stream, SCENARIO, TAG, node_element):
    weapon = SCENARIO.Weapon()
    weapon.type_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "type", None, SCENARIO.weapon_palette_tag_block.count, "scenario_weapon_palette_block"))
    weapon.name_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "name", None, SCENARIO.object_names_tag_block.count, "scenario_object_names_block"))
    weapon.placement_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "not placed", ObjectFlags))
    weapon.desired_permutation = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "desired permutation"))
    weapon.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    weapon.rotation = TAG.read_euler_angles(input_stream, TAG, tag_format.XMLData(node_element, "rotation"))
    input_stream.read(4) # Padding?
    weapon.appearance_player_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "appearance player index"))
    input_stream.read(35) # Padding?
    weapon.rounds_left = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "rounds left"))
    weapon.rounds_loaded = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "rounds loaded"))
    weapon.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "flags", ItemFlags))
    input_stream.read(14) # Padding?

    return weapon

def get_device_groups(input_stream, SCENARIO, TAG, node_element):
    device_group = SCENARIO.DeviceGroup()
    device_group.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    device_group.initial_value = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "initial value"))
    device_group.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", DeviceGroupFlags))
    input_stream.read(12) # Padding?

    return device_group

def get_machines(input_stream, SCENARIO, TAG, node_element):
    device_machine = SCENARIO.DeviceMachine()
    device_machine.type_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "type", None, SCENARIO.machine_palette_tag_block.count, "scenario_machine_palette_block"))
    device_machine.name_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "name", None, SCENARIO.object_names_tag_block.count, "scenario_object_names_block"))
    device_machine.placement_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "not placed", ObjectFlags))
    device_machine.desired_permutation = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "desired permutation"))
    device_machine.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    device_machine.rotation = TAG.read_euler_angles(input_stream, TAG, tag_format.XMLData(node_element, "rotation"))
    input_stream.read(4) # Padding?
    device_machine.appearance_player_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "appearance player index"))
    input_stream.read(3) # Padding?
    device_machine.power_group_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "power group", None, SCENARIO.device_groups_tag_block.count, "scenario_device_groups_block"))
    device_machine.position_group_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "position group", None, SCENARIO.device_groups_tag_block.count, "scenario_device_groups_block"))
    device_machine.flags_0 = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", DeviceFlags))
    device_machine.flags_1 = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", MachineFlags))
    input_stream.read(12) # Padding?

    return device_machine

def get_controls(input_stream, SCENARIO, TAG, node_element):
    device_control = SCENARIO.DeviceControl()
    device_control.type_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "type", None, SCENARIO.control_palette_tag_block.count, "scenario_control_palette_block"))
    device_control.name_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "name", None, SCENARIO.object_names_tag_block.count, "scenario_object_names_block"))
    device_control.placement_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "not placed", ObjectFlags))
    device_control.desired_permutation = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "desired permutation"))
    device_control.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    device_control.rotation = TAG.read_euler_angles(input_stream, TAG, tag_format.XMLData(node_element, "rotation"))
    input_stream.read(4) # Padding?
    device_control.appearance_player_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "appearance player index"))
    input_stream.read(3) # Padding?
    device_control.power_group_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "power group", None, SCENARIO.device_groups_tag_block.count, "scenario_device_groups_block"))
    device_control.position_group_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "position group", None, SCENARIO.device_groups_tag_block.count, "scenario_device_groups_block"))
    device_control.flags_0 = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", DeviceFlags))
    device_control.flags_1 = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", ControlFlags))
    device_control.unknown = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "unknown"))
    input_stream.read(10)

    return device_control

def get_light_fixtures(input_stream, SCENARIO, TAG, node_element):
    device_light_fixture = SCENARIO.DeviceLightFixture()
    device_light_fixture.type_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "type", None, SCENARIO.light_fixtures_palette_tag_block.count, "scenario_light_fixtures_palette_block"))
    device_light_fixture.name_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "name", None, SCENARIO.object_names_tag_block.count, "scenario_object_names_block"))
    device_light_fixture.placement_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "not placed", ObjectFlags))
    device_light_fixture.desired_permutation = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "desired permutation"))
    device_light_fixture.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    device_light_fixture.rotation = TAG.read_euler_angles(input_stream, TAG, tag_format.XMLData(node_element, "rotation"))
    input_stream.read(4) # Padding?
    device_light_fixture.appearance_player_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "appearance player index"))
    input_stream.read(3) # Padding?
    device_light_fixture.power_group_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "power group", None, SCENARIO.device_groups_tag_block.count, "scenario_device_groups_block"))
    device_light_fixture.position_group_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "position group", None, SCENARIO.device_groups_tag_block.count, "scenario_device_groups_block"))
    device_light_fixture.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", DeviceFlags))
    device_light_fixture.color_RGBA = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(node_element, "color"))
    device_light_fixture.intensity = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "intensity"))
    device_light_fixture.falloff_angle = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "falloff angle"))
    device_light_fixture.cutoff_angle = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "cutoff angle"))
    input_stream.read(16) # Padding?

    return device_light_fixture

def get_sound_scenery(input_stream, SCENARIO, TAG, node_element):
    sound_scenery = SCENARIO.Object()
    sound_scenery.type_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "type", None, SCENARIO.sound_scenery_palette_tag_block.count, "scenario_sound_scenery_palette_block"))
    sound_scenery.name_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "name", None, SCENARIO.object_names_tag_block.count, "scenario_object_names_block"))
    sound_scenery.placement_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "not placed", ObjectFlags))
    sound_scenery.desired_permutation = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "desired permutation"))
    sound_scenery.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    sound_scenery.rotation = TAG.read_euler_angles(input_stream, TAG, tag_format.XMLData(node_element, "rotation"))
    input_stream.read(4) # Padding?
    sound_scenery.appearance_player_index = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "appearance player index"))
    input_stream.read(3) # Padding?

    return sound_scenery

def get_player_starting_profiles(input_stream, SCENARIO, TAG, node_element):
    player_starting_profile = SCENARIO.PlayerStartingProfile()
    player_starting_profile.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    player_starting_profile.starting_health_damage = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "cutoff angle"))
    player_starting_profile.starting_shield_damage = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "cutoff angle"))
    player_starting_profile.primary_weapon_tag_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "primary weapon"))
    player_starting_profile.primary_rounds_loaded = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "primary rounds loaded"))
    player_starting_profile.primary_rounds_total = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "primary rounds total"))
    player_starting_profile.secondary_weapon_tag_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "secondary weapon"))
    player_starting_profile.secondary_rounds_loaded = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "secondary rounds total"))
    player_starting_profile.secondary_rounds_total = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "secondary rounds total"))
    player_starting_profile.starting_fragmentation_grenades_count = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "starting fragmentation grenades count"))
    player_starting_profile.starting_plasma_grenade_count = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "starting plasma grenade count"))
    player_starting_profile.starting_grenade_type2_count = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "starting grenade type2 count"))
    player_starting_profile.starting_grenade_type3_count = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "starting grenade type3 count"))
    input_stream.read(20) # Padding?

    return player_starting_profile

def get_player_starting_locations(input_stream, SCENARIO, TAG, node_element):
    player_starting_location = SCENARIO.PlayerStartingLocation()
    player_starting_location.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    player_starting_location.facing = TAG.read_degree(input_stream, TAG, tag_format.XMLData(node_element, "facing"))
    player_starting_location.team_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "team index"))
    player_starting_location.bsp_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "bsp index", None, SCENARIO.structure_bsps_tag_block.count, "scenario_structure_bsps_block"))
    player_starting_location.type_0 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type 0", GametypeEnum))
    player_starting_location.type_1 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type 1", GametypeEnum))
    player_starting_location.type_2 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type 2", GametypeEnum))
    player_starting_location.type_3 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type 3", GametypeEnum))
    input_stream.read(24) # Padding?

    return player_starting_location

def get_trigger_volumes(input_stream, SCENARIO, TAG, node_element):
    trigger_volume = SCENARIO.TriggerVolume()
    input_stream.read(4) # Padding?
    trigger_volume.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    trigger_volume.parameter = TAG.read_vector(input_stream, TAG, tag_format.XMLData(node_element, "parameter"))
    trigger_volume.forward = TAG.read_vector(input_stream, TAG, tag_format.XMLData(node_element, "forward"))
    trigger_volume.up = TAG.read_vector(input_stream, TAG, tag_format.XMLData(node_element, "up"))
    trigger_volume.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    trigger_volume.extents = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "extents"))

    return trigger_volume

def get_recorded_animations(input_stream, SCENARIO, TAG, node_element):
    recorded_animation = SCENARIO.RecordedAnimation()
    recorded_animation.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    recorded_animation.version = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "version"))
    recorded_animation.raw_animation_data = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "raw animation data"))
    recorded_animation.unit_control_data_version = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "unit control data version"))
    input_stream.read(1) # Padding?
    recorded_animation.length_of_animation = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "length of animation"))
    input_stream.read(6) # Padding?
    recorded_animation.recorded_animation_event_stream_tag_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(node_element, "recorded animation event stream"))

    return recorded_animation

def get_netgame_flags(input_stream, SCENARIO, TAG, node_element):
    netgame_flag = SCENARIO.NetGameFlag()
    netgame_flag.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    netgame_flag.facing = TAG.read_degree(input_stream, TAG, tag_format.XMLData(node_element, "facing"))
    netgame_flag.type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type", NetGameEnum))
    netgame_flag.usage_id = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "usage id"))
    netgame_flag.weapon_group = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "weapon group"))
    input_stream.read(112) # Padding?

    return netgame_flag

def get_netgame_equipment(input_stream, SCENARIO, TAG, node_element):
    netgame_equipment = SCENARIO.NetGameEquipment()
    netgame_equipment.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", NetGameEquipment))
    netgame_equipment.type_0 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type 0", GametypeEnum))
    netgame_equipment.type_1 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type 1", GametypeEnum))
    netgame_equipment.type_2 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type 2", GametypeEnum))
    netgame_equipment.type_3 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type 3", GametypeEnum))
    netgame_equipment.team_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "team index"))
    netgame_equipment.spawn_time = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "spawn time"))
    input_stream.read(48) # Padding?
    netgame_equipment.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    netgame_equipment.facing = TAG.read_degree(input_stream, TAG, tag_format.XMLData(node_element, "facing"))
    netgame_equipment.item_collection = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "item collection"))
    input_stream.read(48) # Padding?

    return netgame_equipment

def get_starting_equipment(input_stream, SCENARIO, TAG, node_element):
    starting_equipment = SCENARIO.StartingEquipment()
    starting_equipment.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", StartingEquipment))
    starting_equipment.type_0 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type 0", GametypeEnum))
    starting_equipment.type_1 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type 1", GametypeEnum))
    starting_equipment.type_2 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type 2", GametypeEnum))
    starting_equipment.type_3 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type 3", GametypeEnum))
    input_stream.read(48) # Padding?
    starting_equipment.item_collection_1 = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "item collection 1"))
    starting_equipment.item_collection_2 = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "item collection 2"))
    starting_equipment.item_collection_3 = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "item collection 3"))
    starting_equipment.item_collection_4 = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "item collection 4"))
    starting_equipment.item_collection_5 = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "item collection 5"))
    starting_equipment.item_collection_6 = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "item collection 6"))
    input_stream.read(48) # Padding?

    return starting_equipment

def get_bsp_switch_trigger_volumes(input_stream, SCENARIO, TAG, node_element):
    bsp_switch_trigger_volume = SCENARIO.BSPSwitchTriggerVolume()
    bsp_switch_trigger_volume.trigger_volume = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "bsp index", None, SCENARIO.trigger_volumes_tag_block.count, "scenario_trigger_volumes_block"))
    bsp_switch_trigger_volume.source = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "bsp index", None, SCENARIO.structure_bsps_tag_block.count, "scenario_structure_bsps_block"))
    bsp_switch_trigger_volume.destination = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "bsp index", None, SCENARIO.structure_bsps_tag_block.count, "scenario_structure_bsps_block"))
    input_stream.read(2)

    return bsp_switch_trigger_volume

def get_decals(input_stream, SCENARIO, TAG, node_element):
    decal = SCENARIO.Decal()
    decal.palette_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "palette index", None, SCENARIO.decal_palette_tag_block.count, "scenario_decal_palette_block"))
    decal.yaw = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "yaw"))
    decal.pitch = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "pitch"))
    decal.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))

    return decal

def get_encounters(input_stream, SCENARIO, TAG, node_element):
    encounter = SCENARIO.Encounter()
    encounter.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    encounter.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", EncounterFlags))
    encounter.team_index = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "team index", TeamEnum))
    input_stream.read(2) # Padding
    encounter.search_behavior = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "search behavior", SearchBehaviorEnum))
    encounter.manual_bsp_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "manual bsp index"))
    encounter.respawn_delay = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(node_element, "respawn delay"))
    input_stream.read(76) # Padding
    encounter.squads_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "squads"))
    encounter.platoons_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "platoons"))
    encounter.firing_positions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "firing positions"))
    encounter.player_starting_locations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "player starting locations"))

    return encounter

def get_squads(input_stream, SCENARIO, TAG, node_element, squad_count, platoon_count):
    squad = SCENARIO.Squad()
    squad.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    squad.actor_type = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "actor type", None, SCENARIO.actor_palette_tag_block.count, "scenario_actor_palette_block"))
    squad.platoon = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "platoon", None, platoon_count, "platoons_block"))
    squad.initial_state = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "initial state", StateEnum))
    squad.return_state = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "return state", StateEnum))
    squad.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", SquadFlags))
    squad.unique_leader_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "unique leader type", LeaderEnum))
    input_stream.read(32) # Padding
    squad.maneuver_to_squad = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "maneuver to squad", None, squad_count, "squads_block"))
    squad.squad_delay_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "squad delay time"))
    squad.attacking = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "attacking", GroupFlags))
    squad.attacking_search = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "attacking search", GroupFlags))
    squad.attacking_guard = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "attacking guard", GroupFlags))
    squad.defending = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "defending", GroupFlags))
    squad.defending_search = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "defending search", GroupFlags))
    squad.defending_guard = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "defending guard", GroupFlags))
    squad.pursuing = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "pursuing", GroupFlags))
    input_stream.read(12) # Padding
    squad.normal_diff_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "normal diff count"))
    squad.insane_diff_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "insane diff count"))
    squad.major_upgrade = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "major upgrade", MajorUpgradeEnum))
    input_stream.read(2) # Padding
    squad.respawn_min_actors = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "respawn min actors"))
    squad.respawn_max_actors = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "respawn max actors"))
    squad.respawn_total = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "respawn total"))
    input_stream.read(2) # Padding
    squad.respawn_delay = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(node_element, "respawn delay"))
    input_stream.read(48) # Padding
    squad.move_positions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "move positions"))
    squad.starting_locations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "starting locations"))
    input_stream.read(12) # Padding

    return squad

def get_move_positions(input_stream, SCENARIO, TAG, node_element):
    move_position = SCENARIO.MovePosition()
    move_position.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    move_position.facing = TAG.read_degree(input_stream, TAG, tag_format.XMLData(node_element, "facing"))
    move_position.weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "weight"))
    move_position.time = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(node_element, "time"))
    move_position.animation = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "animation", None, SCENARIO.ai_recording_references_tag_block.count, "scenario_ai_animation_references_block"))
    move_position.sequence_id = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "sequence id"))
    input_stream.read(45) # Padding
    move_position.surface_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "surface id"))

    return move_position

def get_starting_locations(input_stream, SCENARIO, TAG, node_element):
    starting_location = SCENARIO.StartingLocation()
    starting_location.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    starting_location.facing = TAG.read_degree(input_stream, TAG, tag_format.XMLData(node_element, "facing"))
    input_stream.read(2) # Padding
    starting_location.sequence_id = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "sequence id"))
    starting_location.flags = TAG.read_flag_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "flags", GroupFlags))
    starting_location.return_state = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "return state", LeaderEnum))
    starting_location.initial_state = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "initial state", LeaderEnum))
    starting_location.actor_type = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "actor type", None, SCENARIO.actor_palette_tag_block.count, "scenario_ai_palette_block"))
    starting_location.command_list = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "command list", None, SCENARIO.command_lists_tag_block.count, "scenario_command_list_block"))

    return starting_location

def get_platoons(input_stream, SCENARIO, TAG, node_element, block_count):
    platoon = SCENARIO.Platoon()
    platoon.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    platoon.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", PlatoonFlags))
    input_stream.read(12) # Padding
    platoon.change_attacking_defending_state = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "change attacking/defending state", PlatoonStrengthEnum))
    platoon.happens_to_a = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "happens to", None, block_count, "platoons_block"))
    input_stream.read(8) # Padding
    platoon.maneuver_when = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "maneuver when", PlatoonStrengthEnum))
    platoon.happens_to_b = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "happens to", None, block_count, "platoons_block"))
    input_stream.read(108) # Padding

    return platoon

def get_firing_positions(input_stream, SCENARIO, TAG, node_element):
    firing_position = SCENARIO.FiringPosition()
    firing_position.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    firing_position.group_index = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "group index", GroupEnum))
    input_stream.read(10) # Padding?

    return firing_position

def get_command_list(input_stream, SCENARIO, TAG, node_element):
    command_list = SCENARIO.CommandList()
    command_list.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    command_list.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", CommandListFlags))
    input_stream.read(8) # Padding
    command_list.manual_bsp_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "manual bsp index"))
    input_stream.read(2) # Padding
    command_list.command_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "commands"))
    command_list.points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "points"))
    input_stream.read(24) # Padding

    return command_list

def get_commands(input_stream, SCENARIO, TAG, node_element, point_block_count, command_block_count):
    command = SCENARIO.Command()
    command.atom_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "atom type", AtomTypeEnum))
    command.atom_modifier = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "atom modifier"))
    command.parameter1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "parameter1"))
    command.parameter2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "parameter2"))
    command.point_1 = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "point 1", None, point_block_count, "points_block"))
    command.point_2 = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "point 2", None, point_block_count, "points_block"))
    command.animation = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "animation", None, SCENARIO.ai_animation_references_tag_block.count, "platoons_block"))
    command.script = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "script", None, SCENARIO.ai_script_references_tag_block.count, "platoons_block"))
    command.recording = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "recording", None, SCENARIO.ai_recording_references_tag_block.count, "platoons_block"))
    command.command = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "command", None, command_block_count, "command_block"))
    command.object_name = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "object name", None, SCENARIO.object_names_tag_block.count, "scenario_object_names_block"))
    input_stream.read(6) # Padding?

    return command

def get_point(input_stream, SCENARIO, TAG, node_element):
    points = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    input_stream.read(8) # Padding?

    return points

def get_ai_animation_reference(input_stream, SCENARIO, TAG, node_element):
    ai_animation_reference = SCENARIO.AIAnimationReference()
    ai_animation_reference.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    ai_animation_reference.animation_reference = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "animation graph"))
    input_stream.read(12) # Padding?

    return ai_animation_reference

def get_name(input_stream, SCENARIO, TAG, node_element):
    name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    input_stream.read(8) # Padding?

    return name

def get_ai_conversations(input_stream, SCENARIO, TAG, node_element):
    ai_conversation = SCENARIO.AIConversation()
    ai_conversation.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    ai_conversation.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "flags", AIConversationFlags))
    input_stream.read(2) # Padding
    ai_conversation.trigger_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "trigger distance"))
    ai_conversation.run_to_player_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "run-to-player-dist"))
    input_stream.read(36) # Padding
    ai_conversation.participants_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "participants"))
    ai_conversation.lines_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "lines"))
    input_stream.read(12) # Padding

    return ai_conversation

def get_participants(input_stream, SCENARIO, TAG, node_element):
    participant = SCENARIO.Participant()
    participant.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", ParticipantFlags))
    participant.selection_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "selection type", SelectionTypeEnum))
    participant.actor_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "actor type", ActorTypeEnum))
    participant.use_this_object = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "use this object", None, SCENARIO.object_names_tag_block.count, "scenario_object_names_block"))
    participant.set_new_name = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "set new name", None, SCENARIO.object_names_tag_block.count, "scenario_object_names_block"))
    input_stream.read(24) # Padding?
    participant.encounter_name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "encounter name"))
    input_stream.read(16) # Padding?

    return participant

def get_lines(input_stream, SCENARIO, TAG, node_element, participant_count):
    line = SCENARIO.Line()
    line.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "flags", LineFlags))
    line.participant = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "participant", None, participant_count, "scenario_object_names_block"))
    line.addresses = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "addresses", AddresseeEnum))
    line.addresse_participant = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "addresse participant", None, participant_count, "scenario_object_names_block"))
    input_stream.read(4) # Padding
    line.line_delay_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "trigger distance"))
    input_stream.read(12) # Padding
    line.variant_1 = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "variant 1"))
    line.variant_2 = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "variant 2"))
    line.variant_3 = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "variant 3"))
    line.variant_4 = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "variant 4"))
    line.variant_5 = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "variant 5"))
    line.variant_6 = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "variant 6"))

    return line

def get_scripts(input_stream, SCENARIO, TAG, node_element):
    script = SCENARIO.Script()
    script.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    script.script_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "script type", ScriptTypeEnum))
    script.return_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "return type", ReturnTypeEnum))
    script.root_expression_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "root expression index"))
    input_stream.read(40) # Padding
    script.parameters_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "parameters"))

    return script

def get_parameters(input_stream, SCENARIO, TAG, node_element):
    parameter = SCENARIO.Parameter()
    parameter.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    parameter.return_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "return type", ReturnTypeEnum))
    input_stream.read(2) # Padding

    return parameter

def get_globals(input_stream, SCENARIO, TAG, node_element):
    script_global = SCENARIO.ScriptGlobal()
    script_global.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    script_global.return_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "return type", ReturnTypeEnum))
    input_stream.read(6) # Padding
    script_global.initialization_expression_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "initialization expression index"))
    input_stream.read(48) # Padding

    return script_global

def get_references(input_stream, SCENARIO, TAG, node_element):
    input_stream.read(24) # Padding?
    tag_reference = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "reference"))

    return tag_reference

def get_source_file(input_stream, SCENARIO, TAG, node_element):
    source_file = SCENARIO.SourceFile()
    source_file.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    source_file.source_tag_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(node_element, "source"))

    return source_file

def get_cutscene_flags(input_stream, SCENARIO, TAG, node_element):
    cutscene_flag = SCENARIO.CutsceneFlag()
    input_stream.read(4) # Padding
    cutscene_flag.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    cutscene_flag.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    cutscene_flag.facing = TAG.read_degree_2d(input_stream, TAG, tag_format.XMLData(node_element, "facing"))
    input_stream.read(36) # Padding

    return cutscene_flag

def get_cutscene_camera_points(input_stream, SCENARIO, TAG, node_element):
    cutscene_camera = SCENARIO.CutsceneCameraPoint()
    input_stream.read(4) # Padding
    cutscene_camera.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    input_stream.read(4) # Padding
    cutscene_camera.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    cutscene_camera.orientation = TAG.read_euler_angles(input_stream, TAG, tag_format.XMLData(node_element, "orientation"))
    cutscene_camera.field_of_view = TAG.read_degree(input_stream, TAG, tag_format.XMLData(node_element, "field of view"))
    input_stream.read(36) # Padding

    return cutscene_camera

def get_cutscene_titles(input_stream, SCENARIO, TAG, node_element):
    cutscene_title = SCENARIO.CutsceneTitle()
    input_stream.read(4) # Padding
    cutscene_title.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    input_stream.read(4) # Padding
    cutscene_title.text_bounds = TAG.read_rectangle(input_stream, TAG, tag_format.XMLData(node_element, "text bounds (on screen)"))
    cutscene_title.string_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "string index"))
    cutscene_title.style = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "style", StyleEnum))
    cutscene_title.justification = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "justification", JustificationEnum))
    input_stream.read(4) # Padding
    cutscene_title.text_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "text flags", TextFlags))
    cutscene_title.text_color = TAG.read_argb_byte(input_stream, TAG, tag_format.XMLData(node_element, "text color"))
    cutscene_title.shadow_color = TAG.read_argb_byte(input_stream, TAG, tag_format.XMLData(node_element, "shadow color"))
    cutscene_title.fade_in_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "fade in time [seconds]"))
    cutscene_title.up_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "up time [seconds]"))
    cutscene_title.fade_out_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "fade out time [seconds]"))
    input_stream.read(16) # Padding

    return cutscene_title

def get_structure_bsp(input_stream, SCENARIO, TAG, node_element):
    input_stream.read(16) # Padding?
    tag_reference = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "structure bsp"))

    return tag_reference

def get_palette(input_stream, SCENARIO, TAG, node_element, padding=32):
    tag_reference = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    input_stream.read(padding) # Padding?

    return tag_reference

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    SCENARIO = ScenarioAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    SCENARIO.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    SCENARIO.dont_use_tag_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "dont use"))
    SCENARIO.wont_use_tag_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "wont use"))
    SCENARIO.cant_use_tag_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "cant use"))
    SCENARIO.skies_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "skies"))
    SCENARIO.scenario_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "type", ScenarioTypeEnum))
    SCENARIO.scenario_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ScenarioFlags))
    SCENARIO.child_scenarios_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "child scenarios"))
    SCENARIO.local_north = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "local north"))
    input_stream.read(156) # Padding?
    SCENARIO.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    SCENARIO.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    SCENARIO.editor_scenario_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(tag_node, "editor scenario data"))
    SCENARIO.comments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "comments"))
    SCENARIO.scavenger_hunt_objects_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "scavenger hunt objects"))
    input_stream.read(212) # Padding?
    SCENARIO.object_names_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "object names"))
    SCENARIO.scenery_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "scenery"))
    SCENARIO.scenery_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "scenery palette"))
    SCENARIO.bipeds_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "bipeds"))
    SCENARIO.biped_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "biped palette"))
    SCENARIO.vehicles_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "vehicles"))
    SCENARIO.vehicle_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "vehicle palette"))
    SCENARIO.equipment_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "equipment"))
    SCENARIO.equipment_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "equipment palette"))
    SCENARIO.weapons_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "weapons"))
    SCENARIO.weapon_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "weapon palette"))
    SCENARIO.device_groups_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "device groups"))
    SCENARIO.machines_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "machines"))
    SCENARIO.machine_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "machine palette"))
    SCENARIO.controls_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "controls"))
    SCENARIO.control_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "control palette"))
    SCENARIO.light_fixtures_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "light fixtures"))
    SCENARIO.light_fixtures_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "light fixtures palette"))
    SCENARIO.sound_scenery_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "sound scenery"))
    SCENARIO.sound_scenery_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "sound scenery palette"))
    input_stream.read(84) # Padding?
    SCENARIO.player_starting_profile_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "player starting profile"))
    SCENARIO.player_starting_locations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "player starting locations"))
    SCENARIO.trigger_volumes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "trigger volumes"))
    SCENARIO.recorded_animations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "recorded animations"))
    SCENARIO.netgame_flags_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "netgame flags"))
    SCENARIO.netgame_equipment_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "netgame equipment"))
    SCENARIO.starting_equipment_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "starting equipment"))
    SCENARIO.bsp_switch_trigger_volumes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "bsp switch trigger volumes"))
    SCENARIO.decals_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "decals"))
    SCENARIO.decal_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "decal palette"))
    SCENARIO.detail_object_collection_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "decal object collection palette"))
    input_stream.read(84) # Padding?
    SCENARIO.actor_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "actor palette"))
    SCENARIO.encounters_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "encounters"))
    SCENARIO.command_lists_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "command list"))
    SCENARIO.ai_animation_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai animation references"))
    SCENARIO.ai_script_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai script references"))
    SCENARIO.ai_recording_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai recording references"))
    SCENARIO.ai_conversations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai conversations"))
    SCENARIO.script_syntax_data_tag_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(tag_node, "script syntax data"))
    SCENARIO.script_string_data_tag_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(tag_node, "script string data"))
    SCENARIO.scripts_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "scripts"))
    SCENARIO.globals_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "globals"))
    SCENARIO.references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "references"))
    SCENARIO.source_files_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "source files"))
    input_stream.read(24) # Padding?
    SCENARIO.cutscene_flags_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "cutscene flags"))
    SCENARIO.cutscene_camera_points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "cutscene camera points"))
    SCENARIO.cutscene_titles_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "cutscene titles"))
    input_stream.read(108) # Padding?
    SCENARIO.custom_object_names_tag_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "custom object names"))
    SCENARIO.chapter_title_text_tag_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "chapter title text"))
    SCENARIO.hud_messages_tag_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "hud messages"))
    SCENARIO.structure_bsps_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "structure bsps"))

    dont_use_tag_ref = SCENARIO.dont_use_tag_ref
    wont_use_tag_ref = SCENARIO.wont_use_tag_ref
    cant_use_tag_ref = SCENARIO.cant_use_tag_ref
    dont_use_name_length = dont_use_tag_ref.name_length
    wont_use_name_length = wont_use_tag_ref.name_length
    cant_use_name_length = cant_use_tag_ref.name_length
    if dont_use_name_length > 0:
        dont_use_tag_ref.name = TAG.read_variable_string(input_stream, dont_use_name_length, TAG)

    if wont_use_name_length > 0:
        wont_use_tag_ref.name = TAG.read_variable_string(input_stream, wont_use_name_length, TAG)

    if cant_use_name_length > 0:
        cant_use_tag_ref.name = TAG.read_variable_string(input_stream, cant_use_name_length, TAG)

    if XML_OUTPUT:
        dont_use_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "dont use")
        wont_use_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "wont use")
        cant_use_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "cant use")
        dont_use_tag_ref.append_xml_attributes(dont_use_node)
        wont_use_tag_ref.append_xml_attributes(wont_use_node)
        cant_use_tag_ref.append_xml_attributes(cant_use_node)

    SCENARIO.skies = []
    SCENARIO.child_scenarios = []
    SCENARIO.predicted_resources = []
    SCENARIO.functions = []
    SCENARIO.comments = []
    SCENARIO.scavenger_hunt_objects = []
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
    SCENARIO.detail_object_collection_palette  = []
    SCENARIO.actor_palette = []
    SCENARIO.encounters = []
    SCENARIO.command_lists = []
    SCENARIO.ai_animation_references = []
    SCENARIO.ai_script_references = []
    SCENARIO.ai_recording_references = []
    SCENARIO.ai_conversations = []
    SCENARIO.scripts = []
    SCENARIO.script_globals = []
    SCENARIO.references = []
    SCENARIO.source_files = []
    SCENARIO.cutscene_flags = []
    SCENARIO.cutscene_camera_points = []
    SCENARIO.cutscene_titles = []
    SCENARIO.structure_bsps = []

    sky_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.skies_tag_block.count, tag_node, "name", "skies")
    for sky_idx in range(SCENARIO.skies_tag_block.count):
        sky_element_node = None
        if XML_OUTPUT:
            sky_element_node = TAG.xml_doc.createElement('element')
            sky_element_node.setAttribute('index', str(sky_idx))
            sky_node.appendChild(sky_element_node)

        SCENARIO.skies.append(TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(sky_element_node, "sky")))

    for sky_idx, sky in enumerate(SCENARIO.skies):
        sky_name_length = sky.name_length
        if sky_name_length > 0:
            sky.name = TAG.read_variable_string(input_stream, sky_name_length, TAG)

        if XML_OUTPUT:
            sky_element_node = sky_node.childNodes[sky_idx]
            sky_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, sky_element_node, "name", "sky")
            sky.append_xml_attributes(sky_tag_ref_node)

    child_scenario_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.child_scenarios_tag_block.count, tag_node, "name", "child scenarios")
    for child_scenario_idx in range(SCENARIO.child_scenarios_tag_block.count):
        child_scenario_element_node = None
        if XML_OUTPUT:
            child_scenario_element_node = TAG.xml_doc.createElement('element')
            child_scenario_element_node.setAttribute('index', str(child_scenario_idx))
            child_scenario_node.appendChild(child_scenario_element_node)

        SCENARIO.child_scenarios.append(TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(child_scenario_element_node, "child scenario")))
        input_stream.read(16) # Padding?

    for child_scenario_idx, child_scenario in enumerate(SCENARIO.child_scenarios):
        child_scenario_name_length = child_scenario.name_length
        if child_scenario_name_length > 0:
            child_scenario.name = TAG.read_variable_string(input_stream, child_scenario_name_length, TAG)

        if XML_OUTPUT:
            child_scenario_element_node = child_scenario_node.childNodes[child_scenario_idx]
            child_scenario_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, child_scenario_element_node, "name", "child scenario")
            child_scenario.append_xml_attributes(child_scenario_tag_ref_node)

    predicted_resource_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.predicted_resources_tag_block.count, tag_node, "name", "predicted resources")
    for predicted_resource_idx in range(SCENARIO.predicted_resources_tag_block.count):
        predicted_resource_element_node = None
        if XML_OUTPUT:
            predicted_resource_element_node = TAG.xml_doc.createElement('element')
            predicted_resource_element_node.setAttribute('index', str(predicted_resource_idx))
            predicted_resource_node.appendChild(predicted_resource_element_node)

        SCENARIO.predicted_resources.append(get_predicted_resource(input_stream, SCENARIO, TAG, predicted_resource_element_node))

    function_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.functions_tag_block.count, tag_node, "name", "functions")
    for function_idx in range(SCENARIO.functions_tag_block.count):
        function_element_node = None
        if XML_OUTPUT:
            function_element_node = TAG.xml_doc.createElement('element')
            function_element_node.setAttribute('index', str(function_idx))
            function_node.appendChild(function_element_node)

        SCENARIO.functions.append(get_functions(input_stream, SCENARIO, TAG, function_element_node))

    SCENARIO.editor_scenario_data.data = input_stream.read(SCENARIO.editor_scenario_data.size)

    comment_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.comments_tag_block.count, tag_node, "name", "comments")
    for comment_idx in range(SCENARIO.comments_tag_block.count):
        comment_element_node = None
        if XML_OUTPUT:
            comment_element_node = TAG.xml_doc.createElement('element')
            comment_element_node.setAttribute('index', str(comment_idx))
            comment_node.appendChild(comment_element_node)

        SCENARIO.comments.append(get_comments(input_stream, SCENARIO, TAG, comment_element_node))

    for comment_idx, comment in enumerate(SCENARIO.comments):
        comment.text = TAG.read_variable_string_no_terminator(input_stream, comment.data.size, TAG)
        if XML_OUTPUT:
            child_scenario_element_node = comment_node.childNodes[comment_idx]
            tag_format.append_xml_node(tag_format.XMLData(child_scenario_element_node, "text"), "string", comment.text)

    scavenger_hunt_object_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scavenger_hunt_objects_tag_block.count, tag_node, "name", "scavenger hunt objects")
    for scavenger_hunt_object_idx in range(SCENARIO.scavenger_hunt_objects_tag_block.count):
        scavenger_hunt_object_element_node = None
        if XML_OUTPUT:
            scavenger_hunt_object_element_node = TAG.xml_doc.createElement('element')
            scavenger_hunt_object_element_node.setAttribute('index', str(scavenger_hunt_object_idx))
            scavenger_hunt_object_node.appendChild(scavenger_hunt_object_element_node)

        SCENARIO.scavenger_hunt_objects.append(get_scavenger_hunt_objects(input_stream, SCENARIO, TAG, scavenger_hunt_object_element_node))

    object_name_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.object_names_tag_block.count, tag_node, "name", "object names")
    for object_name_idx in range(SCENARIO.object_names_tag_block.count):
        object_name_element_node = None
        if XML_OUTPUT:
            object_name_element_node = TAG.xml_doc.createElement('element')
            object_name_element_node.setAttribute('index', str(object_name_idx))
            object_name_node.appendChild(object_name_element_node)

        SCENARIO.object_names.append(get_object_names(input_stream, SCENARIO, TAG, object_name_element_node))

    scenery_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenery_tag_block.count, tag_node, "name", "scenery")
    for scenery_idx in range(SCENARIO.scenery_tag_block.count):
        scenery_element_node = None
        if XML_OUTPUT:
            scenery_element_node = TAG.xml_doc.createElement('element')
            scenery_element_node.setAttribute('index', str(scenery_idx))
            scenery_node.appendChild(scenery_element_node)

        SCENARIO.scenery.append(get_scenery(input_stream, SCENARIO, TAG, scenery_element_node))

    scenery_palette_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenery_palette_tag_block.count, tag_node, "name", "scenery palette")
    for scenery_palette_idx in range(SCENARIO.scenery_palette_tag_block.count):
        scenery_palette_element_node = None
        if XML_OUTPUT:
            scenery_palette_element_node = TAG.xml_doc.createElement('element')
            scenery_palette_element_node.setAttribute('index', str(scenery_palette_idx))
            scenery_palette_node.appendChild(scenery_palette_element_node)

        SCENARIO.scenery_palette.append(get_palette(input_stream, SCENARIO, TAG, scenery_palette_element_node))

    for scenery_palette_idx, scenery_palette in enumerate(SCENARIO.scenery_palette):
        scenery_palette_name_length = scenery_palette.name_length
        if scenery_palette_name_length > 0:
            scenery_palette.name = TAG.read_variable_string(input_stream, scenery_palette_name_length, TAG)

        if XML_OUTPUT:
            scenery_palette_element_node = scenery_palette_node.childNodes[scenery_palette_idx]
            scenery_palette_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, scenery_palette_element_node, "name", "name")
            scenery_palette.append_xml_attributes(scenery_palette_tag_ref_node)

    biped_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.bipeds_tag_block.count, tag_node, "name", "bipeds")
    for biped_idx in range(SCENARIO.bipeds_tag_block.count):
        biped_element_node = None
        if XML_OUTPUT:
            biped_element_node = TAG.xml_doc.createElement('element')
            biped_element_node.setAttribute('index', str(biped_idx))
            biped_node.appendChild(biped_element_node)

        SCENARIO.bipeds.append(get_bipeds(input_stream, SCENARIO, TAG, biped_element_node))

    biped_palette_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.biped_palette_tag_block.count, tag_node, "name", "biped palette")
    for biped_palette_idx in range(SCENARIO.biped_palette_tag_block.count):
        biped_palette_element_node = None
        if XML_OUTPUT:
            biped_palette_element_node = TAG.xml_doc.createElement('element')
            biped_palette_element_node.setAttribute('index', str(biped_palette_idx))
            biped_palette_node.appendChild(biped_palette_element_node)

        SCENARIO.biped_palette.append(get_palette(input_stream, SCENARIO, TAG, biped_palette_element_node))

    for biped_palette_idx, biped_palette in enumerate(SCENARIO.biped_palette):
        biped_palette_name_length = biped_palette.name_length
        if biped_palette_name_length > 0:
            biped_palette.name = TAG.read_variable_string(input_stream, biped_palette_name_length, TAG)

        if XML_OUTPUT:
            biped_palette_element_node = biped_palette_node.childNodes[biped_palette_idx]
            biped_palette_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, biped_palette_element_node, "name", "name")
            biped_palette.append_xml_attributes(biped_palette_tag_ref_node)

    vehicle_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.vehicles_tag_block.count, tag_node, "name", "vehicles")
    for vehicle_idx in range(SCENARIO.vehicles_tag_block.count):
        vehicle_element_node = None
        if XML_OUTPUT:
            vehicle_element_node = TAG.xml_doc.createElement('element')
            vehicle_element_node.setAttribute('index', str(vehicle_idx))
            vehicle_node.appendChild(vehicle_element_node)

        SCENARIO.vehicles.append(get_vehicles(input_stream, SCENARIO, TAG, vehicle_element_node))

    vehicle_palette_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.vehicle_palette_tag_block.count, tag_node, "name", "vehicle palette")
    for vehicle_palette_idx in range(SCENARIO.vehicle_palette_tag_block.count):
        vehicle_palette_element_node = None
        if XML_OUTPUT:
            vehicle_palette_element_node = TAG.xml_doc.createElement('element')
            vehicle_palette_element_node.setAttribute('index', str(vehicle_palette_idx))
            vehicle_palette_node.appendChild(vehicle_palette_element_node)

        SCENARIO.vehicle_palette.append(get_palette(input_stream, SCENARIO, TAG, vehicle_palette_element_node))

    for vehicle_palette_idx, vehicle_palette in enumerate(SCENARIO.vehicle_palette):
        vehicle_palette_name_length = vehicle_palette.name_length
        if vehicle_palette_name_length > 0:
            vehicle_palette.name = TAG.read_variable_string(input_stream, vehicle_palette_name_length, TAG)

        if XML_OUTPUT:
            vehicle_palette_element_node = vehicle_palette_node.childNodes[vehicle_palette_idx]
            vehicle_palette_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, vehicle_palette_element_node, "name", "name")
            vehicle_palette.append_xml_attributes(vehicle_palette_tag_ref_node)

    equipment_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.equipment_tag_block.count, tag_node, "name", "equipment")
    for equipment_idx in range(SCENARIO.equipment_tag_block.count):
        equipment_element_node = None
        if XML_OUTPUT:
            equipment_element_node = TAG.xml_doc.createElement('element')
            equipment_element_node.setAttribute('index', str(equipment_idx))
            equipment_node.appendChild(equipment_element_node)

        SCENARIO.equipment.append(get_equipment(input_stream, SCENARIO, TAG, equipment_element_node))

    equipment_palette_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.equipment_palette_tag_block.count, tag_node, "name", "equipment palette")
    for equipment_palette_idx in range(SCENARIO.equipment_palette_tag_block.count):
        equipment_palette_element_node = None
        if XML_OUTPUT:
            equipment_palette_element_node = TAG.xml_doc.createElement('element')
            equipment_palette_element_node.setAttribute('index', str(equipment_palette_idx))
            equipment_palette_node.appendChild(equipment_palette_element_node)

        SCENARIO.equipment_palette.append(get_palette(input_stream, SCENARIO, TAG, equipment_palette_element_node))

    for equipment_palette_idx, equipment_palette in enumerate(SCENARIO.equipment_palette):
        equipment_palette_name_length = equipment_palette.name_length
        if equipment_palette_name_length > 0:
            equipment_palette.name = TAG.read_variable_string(input_stream, equipment_palette_name_length, TAG)

        if XML_OUTPUT:
            equipment_palette_element_node = equipment_palette_node.childNodes[equipment_palette_idx]
            equipment_palette_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, equipment_palette_element_node, "name", "name")
            equipment_palette.append_xml_attributes(equipment_palette_tag_ref_node)

    weapon_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.weapons_tag_block.count, tag_node, "name", "weapons")
    for weapon_idx in range(SCENARIO.weapons_tag_block.count):
        weapon_element_node = None
        if XML_OUTPUT:
            weapon_element_node = TAG.xml_doc.createElement('element')
            weapon_element_node.setAttribute('index', str(weapon_idx))
            weapon_node.appendChild(weapon_element_node)

        SCENARIO.weapons.append(get_weapons(input_stream, SCENARIO, TAG, weapon_element_node))

    weapon_palette_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.weapon_palette_tag_block.count, tag_node, "name", "weapon palette")
    for weapon_palette_idx in range(SCENARIO.weapon_palette_tag_block.count):
        weapon_palette_element_node = None
        if XML_OUTPUT:
            weapon_palette_element_node = TAG.xml_doc.createElement('element')
            weapon_palette_element_node.setAttribute('index', str(weapon_palette_idx))
            weapon_palette_node.appendChild(weapon_palette_element_node)

        SCENARIO.weapon_palette.append(get_palette(input_stream, SCENARIO, TAG, weapon_palette_element_node))

    for weapon_palette_idx, weapon_palette in enumerate(SCENARIO.weapon_palette):
        weapon_palette_name_length = weapon_palette.name_length
        if weapon_palette_name_length > 0:
            weapon_palette.name = TAG.read_variable_string(input_stream, weapon_palette_name_length, TAG)

        if XML_OUTPUT:
            weapon_palette_element_node = weapon_palette_node.childNodes[weapon_palette_idx]
            weapon_palette_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, weapon_palette_element_node, "name", "name")
            weapon_palette.append_xml_attributes(weapon_palette_tag_ref_node)

    device_group_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.device_groups_tag_block.count, tag_node, "name", "device groups")
    for device_group_idx in range(SCENARIO.device_groups_tag_block.count):
        device_group_element_node = None
        if XML_OUTPUT:
            device_group_element_node = TAG.xml_doc.createElement('element')
            device_group_element_node.setAttribute('index', str(device_group_idx))
            device_group_node.appendChild(device_group_element_node)

        SCENARIO.device_groups.append(get_device_groups(input_stream, SCENARIO, TAG, device_group_element_node))

    machine_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.machines_tag_block.count, tag_node, "name", "machines")
    for machine_idx in range(SCENARIO.machines_tag_block.count):
        machine_element_node = None
        if XML_OUTPUT:
            machine_element_node = TAG.xml_doc.createElement('element')
            machine_element_node.setAttribute('index', str(machine_idx))
            machine_node.appendChild(machine_element_node)

        SCENARIO.device_machines.append(get_machines(input_stream, SCENARIO, TAG, machine_element_node))

    machine_palette_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.machine_palette_tag_block.count, tag_node, "name", "machine palette")
    for machine_palette_idx in range(SCENARIO.machine_palette_tag_block.count):
        machine_palette_element_node = None
        if XML_OUTPUT:
            machine_palette_element_node = TAG.xml_doc.createElement('element')
            machine_palette_element_node.setAttribute('index', str(machine_palette_idx))
            machine_palette_node.appendChild(machine_palette_element_node)

        SCENARIO.device_machine_palette.append(get_palette(input_stream, SCENARIO, TAG, machine_palette_element_node))

    for device_machine_palette_idx, device_machine_palette in enumerate(SCENARIO.device_machine_palette):
        device_machine_palette_name_length = device_machine_palette.name_length
        if device_machine_palette_name_length > 0:
            device_machine_palette.name = TAG.read_variable_string(input_stream, device_machine_palette_name_length, TAG)

        if XML_OUTPUT:
            machine_palette_element_node = machine_palette_node.childNodes[device_machine_palette_idx]
            machine_palette_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, machine_palette_element_node, "name", "name")
            device_machine_palette.append_xml_attributes(machine_palette_tag_ref_node)

    control_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.controls_tag_block.count, tag_node, "name", "controls")
    for control_idx in range(SCENARIO.controls_tag_block.count):
        control_element_node = None
        if XML_OUTPUT:
            control_element_node = TAG.xml_doc.createElement('element')
            control_element_node.setAttribute('index', str(control_idx))
            control_node.appendChild(control_element_node)

        SCENARIO.device_controls.append(get_controls(input_stream, SCENARIO, TAG, control_element_node))

    control_palette_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.control_palette_tag_block.count, tag_node, "name", "control palette")
    for control_palette_idx in range(SCENARIO.control_palette_tag_block.count):
        control_palette_element_node = None
        if XML_OUTPUT:
            control_palette_element_node = TAG.xml_doc.createElement('element')
            control_palette_element_node.setAttribute('index', str(control_palette_idx))
            control_palette_node.appendChild(control_palette_element_node)

        SCENARIO.device_control_palette.append(get_palette(input_stream, SCENARIO, TAG, control_palette_element_node))

    for device_control_palette_idx, device_control_palette in enumerate(SCENARIO.device_control_palette):
        device_control_palette_name_length = device_control_palette.name_length
        if device_control_palette_name_length > 0:
            device_control_palette.name = TAG.read_variable_string(input_stream, device_control_palette_name_length, TAG)

        if XML_OUTPUT:
            control_palette_element_node = control_palette_node.childNodes[device_control_palette_idx]
            control_palette_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, control_palette_element_node, "name", "name")
            device_control_palette.append_xml_attributes(control_palette_tag_ref_node)

    light_fixture_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.light_fixtures_tag_block.count, tag_node, "name", "light fixtures")
    for light_fixture_idx in range(SCENARIO.light_fixtures_tag_block.count):
        light_fixture_element_node = None
        if XML_OUTPUT:
            light_fixture_element_node = TAG.xml_doc.createElement('element')
            light_fixture_element_node.setAttribute('index', str(light_fixture_idx))
            light_fixture_node.appendChild(light_fixture_element_node)

        SCENARIO.device_light_fixtures.append(get_light_fixtures(input_stream, SCENARIO, TAG, light_fixture_element_node))

    light_fixture_palette_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.control_palette_tag_block.count, tag_node, "name", "light fixtures palette")
    for light_fixtures_palette_idx in range(SCENARIO.light_fixtures_palette_tag_block.count):
        light_fixture_palette_element_node = None
        if XML_OUTPUT:
            light_fixture_palette_element_node = TAG.xml_doc.createElement('element')
            light_fixture_palette_element_node.setAttribute('index', str(light_fixtures_palette_idx))
            light_fixture_palette_node.appendChild(light_fixture_palette_element_node)

        SCENARIO.device_light_fixtures_palette.append(get_palette(input_stream, SCENARIO, TAG, light_fixture_palette_element_node))

    for device_light_fixtures_palette_idx, device_light_fixtures_palette in enumerate(SCENARIO.device_light_fixtures_palette):
        device_light_fixtures_palette_name_length = device_light_fixtures_palette.name_length
        if device_light_fixtures_palette_name_length > 0:
            device_light_fixtures_palette.name = TAG.read_variable_string(input_stream, device_light_fixtures_palette_name_length, TAG)

        if XML_OUTPUT:
            light_fixture_palette_element_node = light_fixture_palette_node.childNodes[device_light_fixtures_palette_idx]
            light_fixture_palette_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, light_fixture_palette_element_node, "name", "name")
            device_light_fixtures_palette.append_xml_attributes(light_fixture_palette_tag_ref_node)

    sound_scenery_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.sound_scenery_tag_block.count, tag_node, "name", "sound scenery")
    for sound_scenery_idx in range(SCENARIO.sound_scenery_tag_block.count):
        sound_scenery_element_node = None
        if XML_OUTPUT:
            sound_scenery_element_node = TAG.xml_doc.createElement('element')
            sound_scenery_element_node.setAttribute('index', str(sound_scenery_idx))
            sound_scenery_node.appendChild(sound_scenery_element_node)

        SCENARIO.sound_scenery.append(get_sound_scenery(input_stream, SCENARIO, TAG, sound_scenery_element_node))

    sound_scenery_palette_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.sound_scenery_palette_tag_block.count, tag_node, "name", "sound scenery palette")
    for sound_scenery_palette_idx in range(SCENARIO.sound_scenery_palette_tag_block.count):
        sound_scenery_palette_element_node = None
        if XML_OUTPUT:
            sound_scenery_palette_element_node = TAG.xml_doc.createElement('element')
            sound_scenery_palette_element_node.setAttribute('index', str(sound_scenery_palette_idx))
            sound_scenery_palette_node.appendChild(sound_scenery_palette_element_node)

        SCENARIO.sound_scenery_palette.append(get_palette(input_stream, SCENARIO, TAG, sound_scenery_palette_element_node))

    for sound_scenery_palette_idx, sound_scenery_palette in enumerate(SCENARIO.sound_scenery_palette):
        sound_scenery_palette_name_length = sound_scenery_palette.name_length
        if sound_scenery_palette_name_length > 0:
            sound_scenery_palette.name = TAG.read_variable_string(input_stream, sound_scenery_palette_name_length, TAG)

        if XML_OUTPUT:
            sound_scenery_palette_element_node = sound_scenery_palette_node.childNodes[sound_scenery_palette_idx]
            sound_scenery_palette_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, sound_scenery_palette_element_node, "name", "name")
            sound_scenery_palette.append_xml_attributes(sound_scenery_palette_tag_ref_node)

    player_starting_profile_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.player_starting_profile_tag_block.count, tag_node, "name", "player starting profile")
    for player_starting_profile_idx in range(SCENARIO.player_starting_profile_tag_block.count):
        player_starting_profile_element_node = None
        if XML_OUTPUT:
            player_starting_profile_element_node = TAG.xml_doc.createElement('element')
            player_starting_profile_element_node.setAttribute('index', str(player_starting_profile_idx))
            player_starting_profile_node.appendChild(player_starting_profile_element_node)

        SCENARIO.player_starting_profiles.append(get_player_starting_profiles(input_stream, SCENARIO, TAG, player_starting_profile_element_node))

    for player_starting_profile_idx, player_starting_profile in enumerate(SCENARIO.player_starting_profiles):
        primary_weapon = player_starting_profile.primary_weapon_tag_ref
        secondary_weapon = player_starting_profile.secondary_weapon_tag_ref
        primary_weapon_name_length = primary_weapon.name_length
        secondary_weapon_name_length = secondary_weapon.name_length
        if primary_weapon_name_length > 0:
            primary_weapon.name = TAG.read_variable_string(input_stream, primary_weapon_name_length, TAG)

        if secondary_weapon_name_length > 0:
            secondary_weapon.name = TAG.read_variable_string(input_stream, secondary_weapon_name_length, TAG)

        if XML_OUTPUT:
            player_starting_profile_element_node = player_starting_profile_node.childNodes[player_starting_profile_idx]
            primary_weapon_node = tag_format.get_xml_node(XML_OUTPUT, 1, player_starting_profile_element_node, "name", "primary weapon")
            secondary_weapon_node = tag_format.get_xml_node(XML_OUTPUT, 1, player_starting_profile_element_node, "name", "secondary weapon")
            primary_weapon.append_xml_attributes(primary_weapon_node)
            secondary_weapon.append_xml_attributes(secondary_weapon_node)

    player_starting_locations_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.player_starting_locations_tag_block.count, tag_node, "name", "player starting locations")
    for player_starting_location_idx in range(SCENARIO.player_starting_locations_tag_block.count):
        player_starting_location_element_node = None
        if XML_OUTPUT:
            player_starting_location_element_node = TAG.xml_doc.createElement('element')
            player_starting_location_element_node.setAttribute('index', str(player_starting_location_idx))
            player_starting_locations_node.appendChild(player_starting_location_element_node)

        SCENARIO.player_starting_locations.append(get_player_starting_locations(input_stream, SCENARIO, TAG, player_starting_location_element_node))

    trigger_volume_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.trigger_volumes_tag_block.count, tag_node, "name", "trigger volumes")
    for trigger_volume_idx in range(SCENARIO.trigger_volumes_tag_block.count):
        trigger_volume_element_node = None
        if XML_OUTPUT:
            trigger_volume_element_node = TAG.xml_doc.createElement('element')
            trigger_volume_element_node.setAttribute('index', str(trigger_volume_idx))
            trigger_volume_node.appendChild(trigger_volume_element_node)

        SCENARIO.trigger_volumes.append(get_trigger_volumes(input_stream, SCENARIO, TAG, trigger_volume_element_node))

    recorded_animations_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.recorded_animations_tag_block.count, tag_node, "name", "recorded animations")
    for recorded_animation_idx in range(SCENARIO.recorded_animations_tag_block.count):
        recorded_animation_element_node = None
        if XML_OUTPUT:
            recorded_animation_element_node = TAG.xml_doc.createElement('element')
            recorded_animation_element_node.setAttribute('index', str(recorded_animation_idx))
            recorded_animations_node.appendChild(recorded_animation_element_node)

        SCENARIO.recorded_animations.append(get_recorded_animations(input_stream, SCENARIO, TAG, recorded_animation_element_node))

    for recorded_animation in SCENARIO.recorded_animations:
        recorded_animation.recorded_animation_event_stream = input_stream.read(recorded_animation.recorded_animation_event_stream_tag_data.size)

    netgame_flag_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.netgame_flags_tag_block.count, tag_node, "name", "netgame flags")
    for netgame_flag_idx in range(SCENARIO.netgame_flags_tag_block.count):
        netgame_flag_element_node = None
        if XML_OUTPUT:
            netgame_flag_element_node = TAG.xml_doc.createElement('element')
            netgame_flag_element_node.setAttribute('index', str(netgame_flag_idx))
            netgame_flag_node.appendChild(netgame_flag_element_node)

        SCENARIO.netgame_flags.append(get_netgame_flags(input_stream, SCENARIO, TAG, netgame_flag_element_node))

    for netgame_flag_idx, netgame_flag in enumerate(SCENARIO.netgame_flags):
        weapon_group = netgame_flag.weapon_group
        weapon_group_name_length = weapon_group.name_length
        if weapon_group_name_length > 0:
            weapon_group.name = TAG.read_variable_string(input_stream, weapon_group_name_length, TAG)

        if XML_OUTPUT:
            netgame_flag_element_node = netgame_flag_node.childNodes[netgame_flag_idx]
            weapon_group_node = tag_format.get_xml_node(XML_OUTPUT, 1, netgame_flag_element_node, "name", "weapon group")
            weapon_group.append_xml_attributes(weapon_group_node)

    netgame_equipment_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.netgame_equipment_tag_block.count, tag_node, "name", "netgame equipment")
    for netgame_equipment_idx in range(SCENARIO.netgame_equipment_tag_block.count):
        netgame_equipment_element_node = None
        if XML_OUTPUT:
            netgame_equipment_element_node = TAG.xml_doc.createElement('element')
            netgame_equipment_element_node.setAttribute('index', str(netgame_equipment_idx))
            netgame_equipment_node.appendChild(netgame_equipment_element_node)

        SCENARIO.netgame_equipment.append(get_netgame_equipment(input_stream, SCENARIO, TAG, netgame_equipment_element_node))

    for netgame_equipment_idx, netgame_equipment in enumerate(SCENARIO.netgame_equipment):
        item_collection = netgame_equipment.item_collection
        item_collection_name_length = item_collection.name_length
        if item_collection_name_length > 0:
            item_collection.name = TAG.read_variable_string(input_stream, item_collection_name_length, TAG)

        if XML_OUTPUT:
            netgame_equipment_element_node = netgame_equipment_node.childNodes[netgame_equipment_idx]
            item_collection_node = tag_format.get_xml_node(XML_OUTPUT, 1, netgame_equipment_element_node, "name", "item collection")
            item_collection.append_xml_attributes(item_collection_node)

    starting_equipment_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.starting_equipment_tag_block.count, tag_node, "name", "starting equipment")
    for starting_equipment_idx in range(SCENARIO.starting_equipment_tag_block.count):
        starting_equipment_element_node = None
        if XML_OUTPUT:
            starting_equipment_element_node = TAG.xml_doc.createElement('element')
            starting_equipment_element_node.setAttribute('index', str(starting_equipment_idx))
            starting_equipment_node.appendChild(starting_equipment_element_node)

        SCENARIO.starting_equipment.append(get_starting_equipment(input_stream, SCENARIO, TAG, starting_equipment_element_node))

    for starting_equipment_idx, starting_equipment in enumerate(SCENARIO.starting_equipment):
        item_collection_1 = starting_equipment.item_collection_1
        item_collection_2 = starting_equipment.item_collection_2
        item_collection_3 = starting_equipment.item_collection_3
        item_collection_4 = starting_equipment.item_collection_4
        item_collection_5 = starting_equipment.item_collection_5
        item_collection_6 = starting_equipment.item_collection_6
        item_collection_1_name_length = item_collection_1.name_length
        item_collection_2_name_length = item_collection_2.name_length
        item_collection_3_name_length = item_collection_3.name_length
        item_collection_4_name_length = item_collection_4.name_length
        item_collection_5_name_length = item_collection_5.name_length
        item_collection_6_name_length = item_collection_6.name_length
        if item_collection_1_name_length > 0:
            item_collection_1.name = TAG.read_variable_string(input_stream, item_collection_1_name_length, TAG)

        if item_collection_2_name_length > 0:
            item_collection_2.name = TAG.read_variable_string(input_stream, item_collection_2_name_length, TAG)

        if item_collection_3_name_length > 0:
            item_collection_3.name = TAG.read_variable_string(input_stream, item_collection_3_name_length, TAG)

        if item_collection_4_name_length > 0:
            item_collection_4.name = TAG.read_variable_string(input_stream, item_collection_4_name_length, TAG)

        if item_collection_5_name_length > 0:
            item_collection_5.name = TAG.read_variable_string(input_stream, item_collection_5_name_length, TAG)

        if item_collection_6_name_length > 0:
            item_collection_6.name = TAG.read_variable_string(input_stream, item_collection_6_name_length, TAG)

        if XML_OUTPUT:
            starting_equipment_element_node = starting_equipment_node.childNodes[starting_equipment_idx]
            item_collection_1_node = tag_format.get_xml_node(XML_OUTPUT, 1, starting_equipment_element_node, "name", "item collection 1")
            item_collection_2_node = tag_format.get_xml_node(XML_OUTPUT, 1, starting_equipment_element_node, "name", "item collection 2")
            item_collection_3_node = tag_format.get_xml_node(XML_OUTPUT, 1, starting_equipment_element_node, "name", "item collection 3")
            item_collection_4_node = tag_format.get_xml_node(XML_OUTPUT, 1, starting_equipment_element_node, "name", "item collection 4")
            item_collection_5_node = tag_format.get_xml_node(XML_OUTPUT, 1, starting_equipment_element_node, "name", "item collection 5")
            item_collection_6_node = tag_format.get_xml_node(XML_OUTPUT, 1, starting_equipment_element_node, "name", "item collection 6")
            item_collection_1.append_xml_attributes(item_collection_1_node)
            item_collection_2.append_xml_attributes(item_collection_2_node)
            item_collection_3.append_xml_attributes(item_collection_3_node)
            item_collection_4.append_xml_attributes(item_collection_4_node)
            item_collection_5.append_xml_attributes(item_collection_5_node)
            item_collection_6.append_xml_attributes(item_collection_6_node)

    bsp_switch_trigger_volume_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.bsp_switch_trigger_volumes_tag_block.count, tag_node, "name", "bsp switch trigger volumes")
    for bsp_switch_trigger_volume_idx in range(SCENARIO.bsp_switch_trigger_volumes_tag_block.count):
        bsp_switch_trigger_volume_element_node = None
        if XML_OUTPUT:
            bsp_switch_trigger_volume_element_node = TAG.xml_doc.createElement('element')
            bsp_switch_trigger_volume_element_node.setAttribute('index', str(bsp_switch_trigger_volume_idx))
            bsp_switch_trigger_volume_node.appendChild(bsp_switch_trigger_volume_element_node)

        SCENARIO.bsp_switch_trigger_volumes.append(get_bsp_switch_trigger_volumes(input_stream, SCENARIO, TAG, bsp_switch_trigger_volume_element_node))

    decal_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.decals_tag_block.count, tag_node, "name", "decals")
    for decal_idx in range(SCENARIO.decals_tag_block.count):
        decal_element_node = None
        if XML_OUTPUT:
            decal_element_node = TAG.xml_doc.createElement('element')
            decal_element_node.setAttribute('index', str(decal_idx))
            decal_node.appendChild(decal_element_node)

        SCENARIO.decals.append(get_decals(input_stream, SCENARIO, TAG, decal_element_node))

    decal_palette_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.decal_palette_tag_block.count, tag_node, "name", "decal palette")
    for decal_palette_idx in range(SCENARIO.decal_palette_tag_block.count):
        decal_palette_element_node = None
        if XML_OUTPUT:
            decal_palette_element_node = TAG.xml_doc.createElement('element')
            decal_palette_element_node.setAttribute('index', str(decal_palette_idx))
            decal_palette_node.appendChild(decal_palette_element_node)

        SCENARIO.decal_palette.append(get_palette(input_stream, SCENARIO, TAG, decal_palette_element_node, 0))

    for decal_palette_idx, decal_palette in enumerate(SCENARIO.decal_palette):
        decal_palette_name_length = decal_palette.name_length
        if decal_palette_name_length > 0:
            decal_palette.name = TAG.read_variable_string(input_stream, decal_palette_name_length, TAG)

        if XML_OUTPUT:
            decal_palette_element_node = decal_palette_node.childNodes[decal_palette_idx]
            decal_palette_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, decal_palette_element_node, "name", "name")
            decal_palette.append_xml_attributes(decal_palette_tag_ref_node)

    detail_object_collection_palette_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.detail_object_collection_palette_tag_block.count, tag_node, "name", "decal object collection palette")
    for detail_object_collection_palette_idx in range(SCENARIO.detail_object_collection_palette_tag_block.count):
        detail_object_collection_palette_element_node = None
        if XML_OUTPUT:
            detail_object_collection_palette_element_node = TAG.xml_doc.createElement('element')
            detail_object_collection_palette_element_node.setAttribute('index', str(detail_object_collection_palette_idx))
            detail_object_collection_palette_node.appendChild(detail_object_collection_palette_element_node)

        SCENARIO.detail_object_collection_palette.append(get_palette(input_stream, SCENARIO, TAG, detail_object_collection_palette_element_node))

    for detail_object_collection_palette_idx, detail_object_collection_palette in enumerate(SCENARIO.detail_object_collection_palette):
        detail_object_collection_palette_name_length = detail_object_collection_palette.name_length
        if detail_object_collection_palette_name_length > 0:
            detail_object_collection_palette.name = TAG.read_variable_string(input_stream, detail_object_collection_palette_name_length, TAG)

        if XML_OUTPUT:
            detail_object_collection_palette_element_node = detail_object_collection_palette_node.childNodes[detail_object_collection_palette_idx]
            detail_object_collection_palette_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, detail_object_collection_palette_element_node, "name", "name")
            detail_object_collection_palette.append_xml_attributes(detail_object_collection_palette_tag_ref_node)

    actor_palette_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.actor_palette_tag_block.count, tag_node, "name", "actor palette")
    for actor_palette_idx in range(SCENARIO.actor_palette_tag_block.count):
        actor_palette_element_node = None
        if XML_OUTPUT:
            actor_palette_element_node = TAG.xml_doc.createElement('element')
            actor_palette_element_node.setAttribute('index', str(actor_palette_idx))
            actor_palette_node.appendChild(actor_palette_element_node)

        SCENARIO.actor_palette.append(get_palette(input_stream, SCENARIO, TAG, actor_palette_element_node, 0))

    for actor_palette_idx, actor_palette in enumerate(SCENARIO.actor_palette):
        actor_palette_name_length = actor_palette.name_length
        if actor_palette_name_length > 0:
            actor_palette.name = TAG.read_variable_string(input_stream, actor_palette_name_length, TAG)

        if XML_OUTPUT:
            actor_palette_element_node = actor_palette_node.childNodes[actor_palette_idx]
            actor_palette_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, actor_palette_element_node, "name", "name")
            actor_palette.append_xml_attributes(actor_palette_tag_ref_node)

    encounter_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.encounters_tag_block.count, tag_node, "name", "encounters")
    for encounter_idx in range(SCENARIO.encounters_tag_block.count):
        encounter_element_node = None
        if XML_OUTPUT:
            encounter_element_node = TAG.xml_doc.createElement('element')
            encounter_element_node.setAttribute('index', str(encounter_idx))
            encounter_node.appendChild(encounter_element_node)

        SCENARIO.encounters.append(get_encounters(input_stream, SCENARIO, TAG, encounter_element_node))

    for encounter_idx, encounter in enumerate(SCENARIO.encounters):
        encounter_element_node = None
        if XML_OUTPUT:
            encounter_element_node = encounter_node.childNodes[encounter_idx]

        encounter.squads = []
        encounter.platoons = []
        encounter.firing_positions = []
        encounter.player_starting_locations = []
        squad_node = tag_format.get_xml_node(XML_OUTPUT, encounter.squads_tag_block.count, encounter_element_node, "name", "squads")
        platoon_node = tag_format.get_xml_node(XML_OUTPUT, encounter.platoons_tag_block.count, encounter_element_node, "name", "platoons")
        firing_position_node = tag_format.get_xml_node(XML_OUTPUT, encounter.firing_positions_tag_block.count, encounter_element_node, "name", "firing positions")
        player_starting_locations_node = tag_format.get_xml_node(XML_OUTPUT, encounter.player_starting_locations_tag_block.count, encounter_element_node, "name", "player starting locations")
        for squad_idx in range(encounter.squads_tag_block.count):
            squad_element_node = None
            if XML_OUTPUT:
                squad_element_node = TAG.xml_doc.createElement('element')
                squad_element_node.setAttribute('index', str(squad_idx))
                squad_node.appendChild(squad_element_node)

            encounter.squads.append(get_squads(input_stream, SCENARIO, TAG, squad_element_node, encounter.squads_tag_block.count, encounter.platoons_tag_block.count))

        for squad_idx, squad in enumerate(encounter.squads):
            squad_element_node = None
            if XML_OUTPUT:
                squad_element_node = squad_node.childNodes[squad_idx]

            squad.move_positions = []
            squad.starting_locations = []
            move_position_node = tag_format.get_xml_node(XML_OUTPUT, squad.move_positions_tag_block.count, squad_element_node, "name", "move positions")
            starting_location_node = tag_format.get_xml_node(XML_OUTPUT, squad.starting_locations_tag_block.count, squad_element_node, "name", "starting locations")
            for move_position_idx in range(squad.move_positions_tag_block.count):
                move_position_element_node = None
                if XML_OUTPUT:
                    move_position_element_node = TAG.xml_doc.createElement('element')
                    move_position_element_node.setAttribute('index', str(move_position_idx))
                    move_position_node.appendChild(move_position_element_node)

                squad.move_positions.append(get_move_positions(input_stream, SCENARIO, TAG, move_position_element_node))

            for starting_location_idx in range(squad.starting_locations_tag_block.count):
                starting_location_element_node = None
                if XML_OUTPUT:
                    starting_location_element_node = TAG.xml_doc.createElement('element')
                    starting_location_element_node.setAttribute('index', str(starting_location_idx))
                    starting_location_node.appendChild(starting_location_element_node)

                squad.starting_locations.append(get_starting_locations(input_stream, SCENARIO, TAG, starting_location_element_node))

        for platoon_idx in range(encounter.platoons_tag_block.count):
            platoon_element_node = None
            if XML_OUTPUT:
                platoon_element_node = TAG.xml_doc.createElement('element')
                platoon_element_node.setAttribute('index', str(platoon_idx))
                platoon_node.appendChild(platoon_element_node)

            encounter.platoons.append(get_platoons(input_stream, SCENARIO, TAG, platoon_element_node, encounter.platoons_tag_block.count))

        for firing_position_idx in range(encounter.firing_positions_tag_block.count):
            firing_position_element_node = None
            if XML_OUTPUT:
                firing_position_element_node = TAG.xml_doc.createElement('element')
                firing_position_element_node.setAttribute('index', str(firing_position_idx))
                firing_position_node.appendChild(firing_position_element_node)

            encounter.firing_positions.append(get_firing_positions(input_stream, SCENARIO, TAG, firing_position_element_node))

        for player_starting_location_idx in range(encounter.player_starting_locations_tag_block.count):
            player_starting_location_element_node = None
            if XML_OUTPUT:
                player_starting_location_element_node = TAG.xml_doc.createElement('element')
                player_starting_location_element_node.setAttribute('index', str(player_starting_location_idx))
                player_starting_locations_node.appendChild(player_starting_location_element_node)

            encounter.player_starting_locations.append(get_player_starting_locations(input_stream, SCENARIO, TAG, player_starting_location_element_node))

    command_list_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.command_lists_tag_block.count, tag_node, "name", "command list")
    for command_list_idx in range(SCENARIO.command_lists_tag_block.count):
        command_list_element_node = None
        if XML_OUTPUT:
            command_list_element_node = TAG.xml_doc.createElement('element')
            command_list_element_node.setAttribute('index', str(command_list_idx))
            command_list_node.appendChild(command_list_element_node)

        SCENARIO.command_lists.append(get_command_list(input_stream, SCENARIO, TAG, command_list_element_node))

    for command_list_idx, command_list in enumerate(SCENARIO.command_lists):
        command_list_element_node = None
        if XML_OUTPUT:
            command_list_element_node = command_list_node.childNodes[command_list_idx]

        command_list.commands = []
        command_list.points = []
        command_node = tag_format.get_xml_node(XML_OUTPUT, command_list.command_tag_block.count, command_list_element_node, "name", "commands")
        point_node = tag_format.get_xml_node(XML_OUTPUT, command_list.points_tag_block.count, command_list_element_node, "name", "points")
        for command_idx in range(command_list.command_tag_block.count):
            command_element_node = None
            if XML_OUTPUT:
                command_element_node = TAG.xml_doc.createElement('element')
                command_element_node.setAttribute('index', str(command_idx))
                command_node.appendChild(command_element_node)

            command_list.commands.append(get_commands(input_stream, SCENARIO, TAG, command_element_node, command_list.points_tag_block.count, command_list.command_tag_block.count))

        for point_idx in range(command_list.points_tag_block.count):
            point_element_node = None
            if XML_OUTPUT:
                point_element_node = TAG.xml_doc.createElement('element')
                point_element_node.setAttribute('index', str(point_idx))
                point_node.appendChild(point_element_node)

            command_list.points.append(get_point(input_stream, SCENARIO, TAG, point_element_node))

    ai_animation_reference_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.ai_animation_references_tag_block.count, tag_node, "name", "ai animation references")
    for ai_animation_reference_idx in range(SCENARIO.ai_animation_references_tag_block.count):
        ai_animation_reference_element_node = None
        if XML_OUTPUT:
            ai_animation_reference_element_node = TAG.xml_doc.createElement('element')
            ai_animation_reference_element_node.setAttribute('index', str(ai_animation_reference_idx))
            ai_animation_reference_node.appendChild(ai_animation_reference_element_node)

        SCENARIO.ai_animation_references.append(get_ai_animation_reference(input_stream, SCENARIO, TAG, ai_animation_reference_element_node))

    for ai_animation_reference_idx, ai_animation_reference in enumerate(SCENARIO.ai_animation_references):
        ai_animation_reference_name_length = ai_animation_reference.animation_reference.name_length
        if ai_animation_reference_name_length > 0:
            ai_animation_reference.animation_reference.name = TAG.read_variable_string(input_stream, ai_animation_reference_name_length, TAG)

        if XML_OUTPUT:
            ai_animation_reference_element_node = ai_animation_reference_node.childNodes[ai_animation_reference_idx]
            aai_animation_reference_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, ai_animation_reference_element_node, "name", "animation graph")
            ai_animation_reference.animation_reference.append_xml_attributes(aai_animation_reference_tag_ref_node)

    ai_script_reference_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.ai_script_references_tag_block.count, tag_node, "name", "ai script references")
    for ai_script_reference_idx in range(SCENARIO.ai_script_references_tag_block.count):
        ai_script_reference_element_node = None
        if XML_OUTPUT:
            ai_script_reference_element_node = TAG.xml_doc.createElement('element')
            ai_script_reference_element_node.setAttribute('index', str(ai_script_reference_idx))
            ai_script_reference_node.appendChild(ai_script_reference_element_node)

        SCENARIO.ai_script_references.append(get_name(input_stream, SCENARIO, TAG, ai_script_reference_element_node))

    ai_recording_reference_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.ai_recording_references_tag_block.count, tag_node, "name", "ai recording references")
    for ai_recording_reference_idx in range(SCENARIO.ai_recording_references_tag_block.count):
        ai_recording_reference_element_node = None
        if XML_OUTPUT:
            ai_recording_reference_element_node = TAG.xml_doc.createElement('element')
            ai_recording_reference_element_node.setAttribute('index', str(ai_recording_reference_idx))
            ai_recording_reference_node.appendChild(ai_recording_reference_element_node)

        SCENARIO.ai_recording_references.append(get_name(input_stream, SCENARIO, TAG, ai_recording_reference_element_node))

    ai_conversations_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.ai_conversations_tag_block.count, tag_node, "name", "ai conversations")
    for ai_conversation_idx in range(SCENARIO.ai_conversations_tag_block.count):
        ai_conversation_element_node = None
        if XML_OUTPUT:
            ai_conversation_element_node = TAG.xml_doc.createElement('element')
            ai_conversation_element_node.setAttribute('index', str(ai_conversation_idx))
            ai_conversations_node.appendChild(ai_conversation_element_node)

        SCENARIO.ai_conversations.append(get_ai_conversations(input_stream, SCENARIO, TAG, ai_conversation_element_node))

    for ai_conversation_idx, ai_conversation in enumerate(SCENARIO.ai_conversations):
        ai_conversation_element_node = None
        if XML_OUTPUT:
            ai_conversation_element_node = ai_conversations_node.childNodes[ai_conversation_idx]

        ai_conversation.participants = []
        ai_conversation.lines = []
        participants_node = tag_format.get_xml_node(XML_OUTPUT, ai_conversation.participants_tag_block.count, ai_conversation_element_node, "name", "participants")
        lines_node = tag_format.get_xml_node(XML_OUTPUT, ai_conversation.lines_tag_block.count, ai_conversation_element_node, "name", "lines")
        for participant_idx in range(ai_conversation.participants_tag_block.count):
            participant_element_node = None
            if XML_OUTPUT:
                participant_element_node = TAG.xml_doc.createElement('element')
                participant_element_node.setAttribute('index', str(participant_idx))
                participants_node.appendChild(participant_element_node)

            ai_conversation.participants.append(get_participants(input_stream, SCENARIO, TAG, participant_element_node))

        for line_idx in range(ai_conversation.lines_tag_block.count):
            line_element_node = None
            if XML_OUTPUT:
                line_element_node = TAG.xml_doc.createElement('element')
                line_element_node.setAttribute('index', str(line_idx))
                lines_node.appendChild(line_element_node)

            ai_conversation.lines.append(get_lines(input_stream, SCENARIO, TAG, line_element_node, ai_conversation.participants_tag_block.count))

        for line_idx, line in enumerate(ai_conversation.lines):
            variant_1_name_length = line.variant_1.name_length
            variant_2_name_length = line.variant_2.name_length
            variant_3_name_length = line.variant_3.name_length
            variant_4_name_length = line.variant_4.name_length
            variant_5_name_length = line.variant_5.name_length
            variant_6_name_length = line.variant_6.name_length
            if variant_1_name_length > 0:
                line.variant_1.name = TAG.read_variable_string(input_stream, variant_1_name_length, TAG)
            if variant_2_name_length > 0:
                line.variant_2.name = TAG.read_variable_string(input_stream, variant_2_name_length, TAG)
            if variant_3_name_length > 0:
                line.variant_3.name = TAG.read_variable_string(input_stream, variant_3_name_length, TAG)
            if variant_4_name_length > 0:
                line.variant_4.name = TAG.read_variable_string(input_stream, variant_4_name_length, TAG)
            if variant_5_name_length > 0:
                line.variant_5.name = TAG.read_variable_string(input_stream, variant_5_name_length, TAG)
            if variant_6_name_length > 0:
                line.variant_6.name = TAG.read_variable_string(input_stream, variant_6_name_length, TAG)

            if XML_OUTPUT:
                line_element_node = lines_node.childNodes[line_idx]
                variant_1_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, line_element_node, "name", "variant 1")
                variant_2_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, line_element_node, "name", "variant 2")
                variant_3_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, line_element_node, "name", "variant 3")
                variant_4_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, line_element_node, "name", "variant 4")
                variant_5_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, line_element_node, "name", "variant 5")
                variant_6_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, line_element_node, "name", "variant 6")
                line.variant_1.append_xml_attributes(variant_1_tag_ref_node)
                line.variant_2.append_xml_attributes(variant_2_tag_ref_node)
                line.variant_3.append_xml_attributes(variant_3_tag_ref_node)
                line.variant_4.append_xml_attributes(variant_4_tag_ref_node)
                line.variant_5.append_xml_attributes(variant_5_tag_ref_node)
                line.variant_6.append_xml_attributes(variant_6_tag_ref_node)

    SCENARIO.script_syntax_data = input_stream.read(SCENARIO.script_syntax_data_tag_data.size)
    SCENARIO.script_string_data = input_stream.read(SCENARIO.script_string_data_tag_data.size)

    script_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scripts_tag_block.count, tag_node, "name", "scripts")
    for script_idx in range(SCENARIO.scripts_tag_block.count):
        script_element_node = None
        if XML_OUTPUT:
            script_element_node = TAG.xml_doc.createElement('element')
            script_element_node.setAttribute('index', str(script_idx))
            script_node.appendChild(script_element_node)

        SCENARIO.scripts.append(get_scripts(input_stream, SCENARIO, TAG, script_element_node))

    for scripts_idx, script in enumerate(SCENARIO.scripts):
        script_element_node = None
        if XML_OUTPUT:
            script_element_node = script_node.childNodes[scripts_idx]

        script.parameters = []
        parameter_node = tag_format.get_xml_node(XML_OUTPUT, script.parameters_tag_block.count, script_element_node, "name", "parameters")
        for parameter_idx in range(script.parameters_tag_block.count):
            parameter_element_node = None
            if XML_OUTPUT:
                parameter_element_node = TAG.xml_doc.createElement('element')
                parameter_element_node.setAttribute('index', str(parameter_idx))
                parameter_node.appendChild(parameter_element_node)

            script.parameters.append(get_parameters(input_stream, SCENARIO, TAG, parameter_element_node))

    global_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.globals_tag_block.count, tag_node, "name", "globals")
    for global_idx in range(SCENARIO.globals_tag_block.count):
        global_element_node = None
        if XML_OUTPUT:
            global_element_node = TAG.xml_doc.createElement('element')
            global_element_node.setAttribute('index', str(global_idx))
            global_node.appendChild(global_element_node)

        SCENARIO.script_globals.append(get_globals(input_stream, SCENARIO, TAG, global_element_node))

    reference_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.references_tag_block.count, tag_node, "name", "references")
    for reference_idx in range(SCENARIO.references_tag_block.count):
        reference_element_node = None
        if XML_OUTPUT:
            reference_element_node = TAG.xml_doc.createElement('element')
            reference_element_node.setAttribute('index', str(reference_idx))
            reference_node.appendChild(reference_element_node)

        SCENARIO.references.append(get_references(input_stream, SCENARIO, TAG, reference_element_node))

    for references_idx, reference in enumerate(SCENARIO.references):
        reference_name_length = reference.name_length
        if reference_name_length > 0:
            reference.name = TAG.read_variable_string(input_stream, reference_name_length, TAG)

        if XML_OUTPUT:
            reference_element_node = reference_node.childNodes[references_idx]
            reference_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, reference_element_node, "name", "reference")
            reference.append_xml_attributes(reference_tag_ref_node)

    source_file_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.source_files_tag_block.count, tag_node, "name", "source files")
    for source_file_idx in range(SCENARIO.source_files_tag_block.count):
        source_file_element_node = None
        if XML_OUTPUT:
            source_file_element_node = TAG.xml_doc.createElement('element')
            source_file_element_node.setAttribute('index', str(source_file_idx))
            source_file_node.appendChild(source_file_element_node)

        SCENARIO.source_files.append(get_source_file(input_stream, SCENARIO, TAG, source_file_element_node))

    for source_file_idx, source_file in enumerate(SCENARIO.source_files):
        source_file.source = TAG.read_variable_string_no_terminator(input_stream, source_file.source_tag_data.size, TAG)

    cutscene_flag_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.cutscene_flags_tag_block.count, tag_node, "name", "cutscene flags")
    for cutscene_flag_idx in range(SCENARIO.cutscene_flags_tag_block.count):
        cutscene_flag_element_node = None
        if XML_OUTPUT:
            cutscene_flag_element_node = TAG.xml_doc.createElement('element')
            cutscene_flag_element_node.setAttribute('index', str(cutscene_flag_idx))
            cutscene_flag_node.appendChild(cutscene_flag_element_node)

        SCENARIO.cutscene_flags.append(get_cutscene_flags(input_stream, SCENARIO, TAG, cutscene_flag_element_node))

    cutscene_camera_point_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.cutscene_camera_points_tag_block.count, tag_node, "name", "cutscene camera points")
    for cutscene_camera_point_idx in range(SCENARIO.cutscene_camera_points_tag_block.count):
        cutscene_camera_point_element_node = None
        if XML_OUTPUT:
            cutscene_camera_point_element_node = TAG.xml_doc.createElement('element')
            cutscene_camera_point_element_node.setAttribute('index', str(cutscene_camera_point_idx))
            cutscene_camera_point_node.appendChild(cutscene_camera_point_element_node)

        SCENARIO.cutscene_camera_points.append(get_cutscene_camera_points(input_stream, SCENARIO, TAG, cutscene_camera_point_element_node))

    cutscene_title_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.cutscene_titles_tag_block.count, tag_node, "name", "cutscene titles")
    for cutscene_title_idx in range(SCENARIO.cutscene_titles_tag_block.count):
        cutscene_title_element_node = None
        if XML_OUTPUT:
            cutscene_title_element_node = TAG.xml_doc.createElement('element')
            cutscene_title_element_node.setAttribute('index', str(cutscene_title_idx))
            cutscene_title_node.appendChild(cutscene_title_element_node)

        SCENARIO.cutscene_titles.append(get_cutscene_titles(input_stream, SCENARIO, TAG, cutscene_title_element_node))

    custom_object_names_tag_ref = SCENARIO.custom_object_names_tag_ref
    chapter_title_text_tag_ref = SCENARIO.chapter_title_text_tag_ref
    hud_messages_tag_ref = SCENARIO.hud_messages_tag_ref
    custom_object_names_name_length = custom_object_names_tag_ref.name_length
    chapter_title_text_name_length = chapter_title_text_tag_ref.name_length
    hud_messages_name_length = hud_messages_tag_ref.name_length
    if custom_object_names_name_length > 0:
        custom_object_names_tag_ref.name = TAG.read_variable_string(input_stream, custom_object_names_name_length, TAG)

    if chapter_title_text_name_length > 0:
        chapter_title_text_tag_ref.name = TAG.read_variable_string(input_stream, chapter_title_text_name_length, TAG)

    if hud_messages_name_length > 0:
        hud_messages_tag_ref.name = TAG.read_variable_string(input_stream, hud_messages_name_length, TAG)

    if XML_OUTPUT:
        custom_object_names_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "custom object names")
        chapter_title_text_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "chapter title text")
        hud_messages_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "hud messages")
        custom_object_names_tag_ref.append_xml_attributes(custom_object_names_node)
        chapter_title_text_tag_ref.append_xml_attributes(chapter_title_text_node)
        hud_messages_tag_ref.append_xml_attributes(hud_messages_node)

    structure_bsp_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.structure_bsps_tag_block.count, tag_node, "name", "structure bsps")
    for structure_bsp_idx in range(SCENARIO.structure_bsps_tag_block.count):
        structure_bsp_element_node = None
        if XML_OUTPUT:
            structure_bsp_element_node = TAG.xml_doc.createElement('element')
            structure_bsp_element_node.setAttribute('index', str(structure_bsp_idx))
            structure_bsp_node.appendChild(structure_bsp_element_node)

        SCENARIO.structure_bsps.append(get_structure_bsp(input_stream, SCENARIO, TAG, structure_bsp_element_node))

    for structure_bsp_idx, structure_bsp in enumerate(SCENARIO.structure_bsps):
        structure_bsp_name_length = structure_bsp.name_length
        if structure_bsp_name_length > 0:
            structure_bsp.name = TAG.read_variable_string(input_stream, structure_bsp_name_length, TAG)

        if XML_OUTPUT:
            structure_bsp_element_node = structure_bsp_node.childNodes[structure_bsp_idx]
            structure_bsp_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, structure_bsp_element_node, "name", "structure bsp")
            structure_bsp.append_xml_attributes(structure_bsp_tag_ref_node)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, SCENARIO.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return SCENARIO
