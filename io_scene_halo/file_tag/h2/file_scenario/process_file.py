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
        CommentTypeEnum,
        ObjectFlags,
        TransformFlags,
        ObjectTypeFlags,
        ObjectSourceFlags,
        ObjectBSPPolicyFlags,
        ObjectColorChangeFlags,
        PathfindingPolicyEnum,
        LightmappingPolicyEnum,
        ObjectGametypeEnum,
        UnitFlags,
        ItemFlags,
        DeviceGroupFlags,
        DeviceFlags,
        MachineFlags,
        ControlFlags,
        VolumeTypeEnum,
        ShapeTypeEnum,
        LightFlags,
        LightmapTypeEnum,
        LightmapFlags,
        TeamDesignatorEnum,
        GametypeEnum,
        SpawnTypeEnum,
        CampaignPlayerTypeEnum,
        NetGameEnum,
        NetGameFlags,
        NetGameEquipmentFlags,
        RespawnTimerStartsEnum,
        ClassificationEnum,
        StartingEquipment,
        SquadFlags,
        TeamEnum,
        MajorUpgradeEnum,
        GrenadeTypeEnum,
        StartingLocationFlags,
        SeatTypeEnum,
        InitialMovementModeEnum,
        ZoneFlags,
        FiringPointFlags,
        AreaFlags,
        MissionSceneFlags,
        CombinationRuleEnum,
        TriggerFlags,
        GroupEnum,
        PathfindingSectorFlags,
        LinkFlags,
        ObjectRefFlags,
        NodeFlags,
        HintTypeEnum,
        GeometryFlags,
        ForceJumpHeightEnum,
        JumpControlFlags,
        HintFlags,
        WellTypeEnum,
        AIConversationFlags,
        LineFlags,
        AddresseeEnum,
        ScriptTypeEnum,
        ReturnTypeEnum,
        PointSetFlags,
        CameraFlags,
        CameraTypeEnum,
        JustificationEnum,
        FontEnum,
        StructureBSPFlags,
        OrderFlags,
        OrderEnum,
        AreaTypeEnum,
        DialogueTypeEnum,
        SpecialMovementFlags,
        AITriggerFlags,
        RuleTypeEnum,
        ScaleFlags,
        OverloadTypeEnum,
        RelevantTeamFlags,
        RelevantGamesFlags,
        SpawnZoneFlags,
        CameraImmersionFlags,
        SALT_SIZE
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
    function.scale_period_by = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "scale period by", None, SCENARIO.scenario_body.functions_tag_block.count, "scenario_function_block"))
    function.function_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "function", FunctionEnum))
    function.scale_function_by = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "scale function by", None, SCENARIO.scenario_body.functions_tag_block.count, "scenario_function_block"))
    function.wobble_function_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "function", FunctionEnum))
    function.wobble_period = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "wobble period"))
    function.wobble_magnitude = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "wobble magnitude"))
    function.square_wave_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "square wave threshold"))
    function.step_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "step count"))
    function.map_to = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "map to", MapEnum))
    function.sawtooth_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "sawtooth count"))
    input_stream.read(2) # Padding?
    function.scale_result_by = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "scale result by", None, SCENARIO.scenario_body.functions_tag_block.count, "scenario_function_block"))
    function.bounds_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "bounds mode", BoundsModeEnum))
    function.bounds = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(node_element, "bounds"))
    input_stream.read(6) # Padding?
    function.turn_off_with = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "turn off with", None, SCENARIO.scenario_body.functions_tag_block.count, "scenario_function_block"))
    input_stream.read(32) # Padding?

    return function

def get_comments(input_stream, SCENARIO, TAG, node_element):
    comment = SCENARIO.Comment()
    comment.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    comment.type = TAG.read_enum_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "type", CommentTypeEnum))
    comment.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    comment.comment = TAG.read_string256(input_stream, TAG, tag_format.XMLData(node_element, "comment"))

    return comment

def get_environment_objects(input_stream, SCENARIO, TAG, node_element):
    environment_object = SCENARIO.EnvironmentObject()
    environment_object.bsp_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "bsp", None, SCENARIO.scenario_body.structure_bsps_tag_block.count, "scenario_bsp_block"))
    environment_object.runtime_object_type = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "runtime object type"))
    environment_object.unique_id = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "unique id"))
    input_stream.read(4) # Padding?
    environment_object.object_definition_tag = TAG.read_variable_string_no_terminator_reversed(input_stream, 4, TAG, tag_format.XMLData(node_element, "object definition tag"))
    environment_object.environment_object = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "object"))
    input_stream.read(44) # Padding?

    return environment_object

def get_object_names(input_stream, SCENARIO, TAG, node_element):
    object_name = SCENARIO.ObjectName()
    object_name.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    object_name.object_type = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "object type", None, 1, ""))
    object_name.placement_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "placement index", None, 1, ""))

    return object_name

def object_helper(tag_element, TAG, input_stream, SCENARIO, node_element, palette_count, palette_name):
    tag_element.palette_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "type", None, palette_count, palette_name))
    tag_element.name_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "name", None, SCENARIO.scenario_body.object_names_tag_block.count, "scenario_object_names_block"))
    tag_element.placement_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "placement flags", ObjectFlags))
    tag_element.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    tag_element.rotation = TAG.read_euler_angles(input_stream, TAG, tag_format.XMLData(node_element, "rotation"))
    tag_element.scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "scale"))
    tag_element.transform_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "transform flags", TransformFlags))
    tag_element.manual_bsp_flags = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "manual bsp flags"))
    tag_element.unique_id = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "unique id"))
    tag_element.origin_bsp_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "origin bsp index", None, SCENARIO.scenario_body.structure_bsps_tag_block.count, "scenario_bsp_block"))
    tag_element.object_type = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "object type", ObjectTypeFlags))
    tag_element.source = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "source", ObjectSourceFlags))
    tag_element.bsp_policy = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "bsp policy", ObjectBSPPolicyFlags))
    input_stream.read(1) # Padding?
    tag_element.editor_folder_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "editor folder", None, SCENARIO.scenario_body.editor_folders_tag_block.count, "scenario_editor_folder_block"))

def get_scenery(input_stream, SCENARIO, TAG, node_element):
    scenery = SCENARIO.Scenery()
    object_helper(scenery, TAG, input_stream, SCENARIO, node_element, SCENARIO.scenario_body.scenery_palette_tag_block.count, "scenario_scenery_palette_block")

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    scenery.variant_name_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    scenery.active_change_colors = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "active change colors", ObjectColorChangeFlags))
    scenery.primary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "primary color"))
    scenery.secondary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "secondary color"))
    scenery.tertiary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "tertiary color"))
    scenery.quaternary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "quaternary color"))
    scenery.pathfinding_policy = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "pathfinding policy", PathfindingPolicyEnum))
    scenery.lightmap_policy = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "lightmap policy", LightmappingPolicyEnum))
    scenery.pathfinding_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "pathfinding references"))
    input_stream.read(2) # Padding?
    scenery.valid_multiplayer_games = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "valid multiplayer games", ObjectGametypeEnum))

    return scenery

def get_units(input_stream, SCENARIO, TAG, node_element, palette_count, palette_name):
    unit = SCENARIO.Unit()
    object_helper(unit, TAG, input_stream, SCENARIO, node_element, palette_count, palette_name)

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    unit.variant_name_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    unit.active_change_colors = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "active change colors", ObjectColorChangeFlags))
    unit.primary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "primary color"))
    unit.secondary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "secondary color"))
    unit.tertiary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "tertiary color"))
    unit.quaternary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "quaternary color"))
    unit.body_vitality = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "body vitality"))
    unit.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", UnitFlags))

    return unit

def get_equipment(input_stream, SCENARIO, TAG, node_element):
    equipment = SCENARIO.Equipment()
    object_helper(equipment, TAG, input_stream, SCENARIO, node_element, SCENARIO.scenario_body.equipment_palette_tag_block.count, "scenario_equipment_palette_block")

    equipment.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", ItemFlags))

    return equipment

def get_weapons(input_stream, SCENARIO, TAG, node_element):
    weapon = SCENARIO.Weapon()
    object_helper(weapon, TAG, input_stream, SCENARIO, node_element, SCENARIO.scenario_body.weapon_palette_tag_block.count, "scenario_weapon_palette_block")

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    weapon.variant_name_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    weapon.active_change_colors = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "active change colors", ObjectColorChangeFlags))
    weapon.primary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "primary color"))
    weapon.secondary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "secondary color"))
    weapon.tertiary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "tertiary color"))
    weapon.quaternary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "quaternary color"))
    weapon.rounds_left = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "rounds left"))
    weapon.rounds_loaded = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "rounds loaded"))
    weapon.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", ItemFlags))

    return weapon

def get_device_groups(input_stream, SCENARIO, TAG, node_element):
    device_group = SCENARIO.DeviceGroup()
    device_group.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    device_group.initial_value = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "initial value"))
    device_group.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", DeviceGroupFlags))

    return device_group

def get_machines(input_stream, SCENARIO, TAG, node_element):
    machine = SCENARIO.DeviceMachine()
    object_helper(machine, TAG, input_stream, SCENARIO, node_element, SCENARIO.scenario_body.machine_palette_tag_block.count, "scenario_machine_palette_block")

    machine.power_group_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "power group", None, SCENARIO.scenario_body.device_groups_tag_block.count, "scenario_device_groups_block"))
    machine.position_group_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "position group", None, SCENARIO.scenario_body.device_groups_tag_block.count, "scenario_device_groups_block"))
    machine.flags_0 = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", DeviceFlags))
    machine.flags_1 = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", MachineFlags))
    machine.pathfinding_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "pathfinding references"))

    return machine

def get_controls(input_stream, SCENARIO, TAG, node_element):
    control = SCENARIO.DeviceControl()
    object_helper(control, TAG, input_stream, SCENARIO, node_element, SCENARIO.scenario_body.control_palette_tag_block.count, "scenario_control_palette_block")

    control.power_group_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "power group", None, SCENARIO.scenario_body.device_groups_tag_block.count, "scenario_device_groups_block"))
    control.position_group_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "position group", None, SCENARIO.scenario_body.device_groups_tag_block.count, "scenario_device_groups_block"))
    control.flags_0 = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", DeviceFlags))
    control.flags_1 = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", ControlFlags))
    control.unk = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "unknown"))
    input_stream.read(2) # Padding?

    return control

def get_light_fixtures(input_stream, SCENARIO, TAG, node_element):
    light_fixture = SCENARIO.LightFixture()
    object_helper(light_fixture, TAG, input_stream, SCENARIO, node_element, SCENARIO.scenario_body.light_fixtures_palette_tag_block.count, "scenario_light_fixtures_palette_block")

    light_fixture.power_group_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "power group", None, SCENARIO.scenario_body.device_groups_tag_block.count, "scenario_device_groups_block"))
    light_fixture.position_group_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "position group", None, SCENARIO.scenario_body.device_groups_tag_block.count, "scenario_device_groups_block"))
    light_fixture.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", DeviceFlags))
    light_fixture.color_RGBA = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(node_element, "color"))
    light_fixture.intensity = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "intensity"))
    light_fixture.falloff_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(node_element, "falloff angle"))
    light_fixture.cutoff_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(node_element, "cutoff angle"))

    return light_fixture

def get_sound_scenery(input_stream, SCENARIO, TAG, node_element):
    sound_scenery = SCENARIO.SoundScenery()
    object_helper(sound_scenery, TAG, input_stream, SCENARIO, node_element, SCENARIO.scenario_body.sound_scenery_palette_tag_block.count, "scenario_sound_scenery_palette_block")

    sound_scenery.volume_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "volume type", VolumeTypeEnum))
    input_stream.read(2) # Padding?
    sound_scenery.height = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "height"))
    sound_scenery.override_distance_bounds = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(node_element, "override distance bounds"))
    sound_scenery.override_core_angle_bounds = TAG.read_min_max_degree(input_stream, TAG, tag_format.XMLData(node_element, "override core angle bounds"))
    sound_scenery.override_outer_core_gain = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "override outer core gain"))

    return sound_scenery

def get_light_volumes(input_stream, SCENARIO, TAG, node_element):
    light_volume = SCENARIO.LightVolume()
    object_helper(light_volume, TAG, input_stream, SCENARIO, node_element, SCENARIO.scenario_body.light_volume_palette_tag_block.count, "scenario_light_volume_palette_block")

    light_volume.power_group_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "power group", None, SCENARIO.scenario_body.device_groups_tag_block.count, "scenario_device_groups_block"))
    light_volume.position_group_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "position group", None, SCENARIO.scenario_body.device_groups_tag_block.count, "scenario_device_groups_block"))
    light_volume.flags_0 = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", DeviceFlags))
    light_volume.shape_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "shape type", ShapeTypeEnum))
    light_volume.flags_1 = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "flags", LightFlags))
    light_volume.lightmap_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "lightmap type", LightmapTypeEnum))
    light_volume.lightmap_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "lightmap flags", LightmapFlags))
    light_volume.lightmap_half_life = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "lightmap half life"))
    light_volume.lightmap_light_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "lightmap light scale"))
    light_volume.target_point = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "target point"))
    light_volume.width = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "width"))
    light_volume.height_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "height scale"))
    light_volume.field_of_view = TAG.read_degree(input_stream, TAG, tag_format.XMLData(node_element, "field of view"))
    light_volume.falloff_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "falloff distance"))
    light_volume.cutoff_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "cutoff distance"))

    return light_volume

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
    player_starting_profile.starting_custom_2_grenade_count = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "starting unknown2 grenade count"))
    player_starting_profile.starting_custom_3_grenade_count = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "starting unknown3 grenade count"))

    return player_starting_profile

def get_player_starting_locations(input_stream, SCENARIO, TAG, node_element):
    player_starting_location = SCENARIO.PlayerStartingLocation()
    player_starting_location.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    player_starting_location.facing = TAG.read_degree(input_stream, TAG, tag_format.XMLData(node_element, "facing"))
    player_starting_location.team_designator = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "team designator", TeamDesignatorEnum))
    player_starting_location.bsp_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "bsp index", None, SCENARIO.scenario_body.structure_bsps_tag_block.count, "scenario_bsp_block"))
    player_starting_location.type_0 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type 0", GametypeEnum))
    player_starting_location.type_1 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type 1", GametypeEnum))
    player_starting_location.type_2 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type 2", GametypeEnum))
    player_starting_location.type_3 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type 3", GametypeEnum))
    player_starting_location.spawn_type_0 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "spawn type 0", SpawnTypeEnum))
    player_starting_location.spawn_type_1 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "spawn type 1", SpawnTypeEnum))
    player_starting_location.spawn_type_2 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "spawn type 2", SpawnTypeEnum))
    player_starting_location.spawn_type_3 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "spawn type 3", SpawnTypeEnum))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    player_starting_location.unk_0_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    player_starting_location.unk_1_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    player_starting_location.campaign_player_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "campaign player type", CampaignPlayerTypeEnum))
    input_stream.read(6) # Padding?

    return player_starting_location

def get_trigger_volumes(input_stream, SCENARIO, TAG, node_element):
    trigger_volume = SCENARIO.TriggerVolume()

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    trigger_volume.name_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    trigger_volume.object_name_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "object name", None, SCENARIO.scenario_body.object_names_tag_block.count, "scenario_object_names_block"))
    input_stream.read(2) # Padding?

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    trigger_volume.node_name_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    trigger_volume.forward = TAG.read_vector(input_stream, TAG, tag_format.XMLData(node_element, "forward"))
    trigger_volume.up = TAG.read_vector(input_stream, TAG, tag_format.XMLData(node_element, "up"))
    trigger_volume.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    trigger_volume.extents = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "extents"))
    input_stream.read(4) # Padding?
    trigger_volume.kill_trigger_volume_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "kill trigger volume", None, SCENARIO.scenario_body.scenario_kill_triggers_tag_block.count, "scenario_kill_triggers_block"))
    input_stream.read(2) # Padding?

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
    netgame_flag.team_designator = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "team designator", TeamDesignatorEnum))
    netgame_flag.identifer = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "identifer"))
    netgame_flag.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "flags", NetGameFlags))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    netgame_flag.spawn_object_name_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    netgame_flag.spawn_marker_name_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    return netgame_flag

def get_netgame_equipment(input_stream, SCENARIO, TAG, node_element):
    netgame_equipment = SCENARIO.NetGameEquipment()
    netgame_equipment.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", NetGameEquipmentFlags))
    netgame_equipment.type_0 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type 0", GametypeEnum))
    netgame_equipment.type_1 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type 1", GametypeEnum))
    netgame_equipment.type_2 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type 2", GametypeEnum))
    netgame_equipment.type_3 = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type 3", GametypeEnum))
    input_stream.read(2) # Padding?
    netgame_equipment.spawn_time = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "spawn time"))
    netgame_equipment.respawn_on_empty_time = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "respawn on empty time"))
    netgame_equipment.respawn_timer_starts = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "respawn timer starts", RespawnTimerStartsEnum))
    netgame_equipment.classification = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "classification", ClassificationEnum))
    input_stream.read(42) # Padding?
    netgame_equipment.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    netgame_equipment.orientation = TAG.read_euler_angles(input_stream, TAG, tag_format.XMLData(node_element, "orientation"))
    netgame_equipment.item_vehicle_collection = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "item vehicle collection"))
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
    bsp_switch_trigger_volume.trigger_volume = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "trigger volume", None, SCENARIO.scenario_body.trigger_volumes_tag_block.count, "scenario_trigger_volumes_block"))
    bsp_switch_trigger_volume.source = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "source", None, SCENARIO.scenario_body.structure_bsps_tag_block.count, "scenario_structure_bsps_block"))
    bsp_switch_trigger_volume.destination = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "destination", None, SCENARIO.scenario_body.structure_bsps_tag_block.count, "scenario_structure_bsps_block"))
    input_stream.read(8) # Padding?

    return bsp_switch_trigger_volume

def get_decals(input_stream, SCENARIO, TAG, node_element):
    decal = SCENARIO.Decal()
    decal.palette_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "palette index", None, SCENARIO.scenario_body.decal_palette_tag_block.count, "scenario_decal_palette_block"))
    decal.yaw = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "yaw"))
    decal.pitch = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "pitch"))
    decal.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))

    return decal

def get_squad_groups(input_stream, SCENARIO, TAG, node_element):
    squad_group = SCENARIO.SquadGroups()
    squad_group.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    squad_group.parent_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "parent", None, SCENARIO.scenario_body.squad_groups_tag_block.count, "scenario_squad_groups_block"))
    squad_group.initial_order_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "initial orders", None, SCENARIO.scenario_body.orders_tag_block.count, "scenario_orders_block"))

    return squad_group

def get_squads(input_stream, SCENARIO, TAG, node_element):
    squad = SCENARIO.Squad()
    squad.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    squad.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", SquadFlags))
    squad.team = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "team", TeamEnum))
    squad.parent_squad_group_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "parent", None, SCENARIO.scenario_body.squad_groups_tag_block.count, "scenario_squad_groups_block"))
    squad.squad_delay_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "squad delay time"))
    squad.normal_difficulty_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "normal diff count"))
    squad.insane_difficulty_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "insane diff count"))
    squad.major_upgrade = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "major upgrade", MajorUpgradeEnum))
    input_stream.read(2) # Padding?
    squad.vehicle_type_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "vehicle type", None, SCENARIO.scenario_body.vehicle_palette_tag_block.count, "scenario_vehicle_palette_block"))
    squad.character_type_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "character type", None, SCENARIO.scenario_body.character_palette_tag_block.count, "scenario_character_palette_block"))
    squad.initial_zone_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "initial zone", None, SCENARIO.scenario_body.zones_tag_block.count, "scenario_zones_block"))
    input_stream.read(2) # Padding?
    squad.initial_weapon_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "initial weapon", None, SCENARIO.scenario_body.weapon_palette_tag_block.count, "scenario_weapon_palette_block"))
    squad.initial_secondary_weapon_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "initial secondary weapon", None, SCENARIO.scenario_body.weapon_palette_tag_block.count, "scenario_weapon_palette_block"))
    squad.grenade_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "grenade type", GrenadeTypeEnum))
    squad.initial_order_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "initial order", None, SCENARIO.scenario_body.orders_tag_block.count, "scenario_orders_block"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    squad.vehicle_variant_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    squad.starting_locations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "starting locations"))
    squad.placement_script = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "placement script"))
    input_stream.read(4) # Padding?

    return squad

def get_zones(input_stream, SCENARIO, TAG, node_element):
    zone = SCENARIO.Zone()
    zone.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    zone.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", ZoneFlags))
    zone.manual_bsp_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "manual bsp index", None, SCENARIO.scenario_body.structure_bsps_tag_block.count, "scenario_structure_bsps_block"))
    input_stream.read(2) # Padding?
    zone.firing_positions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "firing positions"))
    zone.areas_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "areas"))

    return zone

def get_mission_scenes(input_stream, SCENARIO, TAG, node_element):
    mission_scene = SCENARIO.MissionScene()

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    mission_scene.name_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    mission_scene.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", MissionSceneFlags))
    mission_scene.trigger_conditions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "trigger conditions"))
    mission_scene.roles_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "roles"))

    return mission_scene

def get_ai_pathfinding_data(input_stream, SCENARIO, TAG, node_element):
    ai_pathfinding_data = SCENARIO.AIPathfindingData()
    ai_pathfinding_data.sectors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "sectors"))
    ai_pathfinding_data.links_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "links"))
    ai_pathfinding_data.refs_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "refs"))
    ai_pathfinding_data.bsp2d_nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "bsp2d nodes"))
    ai_pathfinding_data.surface_flags_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "surface flags"))
    ai_pathfinding_data.vertices_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "vertices"))
    ai_pathfinding_data.object_refs_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "object refs"))
    ai_pathfinding_data.pathfinding_hints_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "pathfinding hints"))
    ai_pathfinding_data.instanced_geometry_refs_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "instanced geometry refs"))
    ai_pathfinding_data.structure_checksum = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "structure checksum"))
    input_stream.read(32) # Padding?
    ai_pathfinding_data.user_placed_hints_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "user placed hints"))

    return ai_pathfinding_data

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
    input_stream.read(8) # Padding?
    participant.use_this_object = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "use this object", None, SCENARIO.scenario_body.object_names_tag_block.count, "scenario_object_names_block"))
    participant.set_new_name = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "set new name", None, SCENARIO.scenario_body.object_names_tag_block.count, "scenario_object_names_block"))
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

    return script

def get_globals(input_stream, SCENARIO, TAG, node_element):
    script_global = SCENARIO.ScriptGlobal()
    script_global.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    script_global.return_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type", ReturnTypeEnum))
    input_stream.read(2) # Padding
    script_global.initialization_expression_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "initialization expression index"))

    return script_global

def get_references(input_stream, SCENARIO, TAG, node_element):
    tag_reference = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "reference"))

    return tag_reference

def get_source_file(input_stream, SCENARIO, TAG, node_element):
    source_file = SCENARIO.SourceFile()
    source_file.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    source_file.source_tag_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(node_element, "source"))

    return source_file

def get_scripting_data(input_stream, SCENARIO, TAG, node_element):
    scripting_data = SCENARIO.ScriptingData()
    scripting_data.point_sets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "point sets"))
    input_stream.read(120) # Padding

    return scripting_data

def get_cutscene_flags(input_stream, SCENARIO, TAG, node_element):
    cutscene_flag = SCENARIO.CutsceneFlag()
    input_stream.read(4) # Padding
    cutscene_flag.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    cutscene_flag.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    cutscene_flag.facing = TAG.read_degree_2d(input_stream, TAG, tag_format.XMLData(node_element, "facing"))

    return cutscene_flag

def get_cutscene_camera_points(input_stream, SCENARIO, TAG, node_element):
    cutscene_camera = SCENARIO.CutsceneCameraPoint()
    cutscene_camera.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "flags", CameraFlags))
    cutscene_camera.camera_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "flags", CameraTypeEnum))
    cutscene_camera.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    input_stream.read(4) # Padding
    cutscene_camera.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    cutscene_camera.orientation = TAG.read_euler_angles(input_stream, TAG, tag_format.XMLData(node_element, "orientation"))

    return cutscene_camera

def get_cutscene_titles(input_stream, SCENARIO, TAG, node_element):
    cutscene_title = SCENARIO.CutsceneTitle()

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    cutscene_title.name_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    cutscene_title.text_bounds = TAG.read_rectangle(input_stream, TAG, tag_format.XMLData(node_element, "text bounds"))
    cutscene_title.justification = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "justification", JustificationEnum))
    cutscene_title.font = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "font", FontEnum))
    cutscene_title.text_color = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "text color"))
    cutscene_title.shadow_color = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "shadow color"))
    cutscene_title.fade_in_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "fade in time"))
    cutscene_title.up_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "up time"))
    cutscene_title.fade_out_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "fade out time"))

    return cutscene_title

def get_structure_bsp(input_stream, SCENARIO, TAG, node_element):
    structure_bsp = SCENARIO.StructureBSP()

    input_stream.read(16) # Padding?
    structure_bsp.structure_bsp = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "structure bsp"))
    structure_bsp.structure_lightmap = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "structure lightmap"))
    input_stream.read(4) # Padding
    structure_bsp.unused_radiance_estimated_search_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "radiance estimated search distance"))
    input_stream.read(4) # Padding
    structure_bsp.unused_luminels_per_world_unit = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "luminels per world unit"))
    structure_bsp.unused_output_white_reference = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "output white reference"))
    input_stream.read(8) # Padding
    structure_bsp.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", StructureBSPFlags))
    structure_bsp.default_sky = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "default sky", None, SCENARIO.scenario_body.skies_tag_block.count, "scenario_skies_block"))
    input_stream.read(2) # Padding

    return structure_bsp

def get_palette(input_stream, TAG, node_element, padding=32):
    tag_reference = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    input_stream.read(padding) # Padding?

    return tag_reference

def palette_helper(input_stream, palette_count, palette_name, palette_header, palette, node, TAG, padding=32):
    if palette_count > 0:
        palette_header = TAG.TagBlockHeader().read(input_stream, TAG)
        palette_node = tag_format.get_xml_node(XML_OUTPUT, palette_count, node, "name", palette_name)
        for palette_idx in range(palette_count):
            palette_element_node = None
            if XML_OUTPUT:
                palette_element_node = TAG.xml_doc.createElement('element')
                palette_element_node.setAttribute('index', str(palette_idx))
                palette_node.appendChild(palette_element_node)

            palette.append(get_palette(input_stream, TAG, palette_element_node, padding))

        for palette_idx, palette_element in enumerate(palette):
            palette_name_length = palette_element.name_length
            if palette_name_length > 0:
                palette_element.name = TAG.read_variable_string(input_stream, palette_name_length, TAG)

            if XML_OUTPUT:
                palette_element_node = palette_node.childNodes[palette_idx]
                palette_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, palette_element_node, "name", "name")
                palette_element.append_xml_attributes(palette_tag_ref_node)

def initilize_scenario(SCENARIO):
    SCENARIO.skies = []
    SCENARIO.child_scenarios = []
    SCENARIO.predicted_resources = []
    SCENARIO.functions = []
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
    SCENARIO.scripts = []
    SCENARIO.globals = []
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

def read_scenario_body(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    SCENARIO.scenario_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    SCENARIO.scenario_body = SCENARIO.ScenarioBody()
    SCENARIO.scenario_body.unused_tag_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "unused"))
    SCENARIO.scenario_body.skies_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "skies"))
    SCENARIO.scenario_body.scenario_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "type", ScenarioTypeEnum))
    SCENARIO.scenario_body.scenario_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ScenarioFlags))
    SCENARIO.scenario_body.child_scenarios_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "child scenarios"))
    SCENARIO.scenario_body.local_north = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "local north"))
    SCENARIO.scenario_body.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    SCENARIO.scenario_body.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    SCENARIO.scenario_body.editor_scenario_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(tag_node, "editor scenario data"))
    SCENARIO.scenario_body.comments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "comments"))
    SCENARIO.scenario_body.environment_objects_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "environment objects"))
    SCENARIO.scenario_body.object_names_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "object names"))
    SCENARIO.scenario_body.scenery_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "scenery"))
    SCENARIO.scenario_body.scenery_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "scenery palette"))
    SCENARIO.scenario_body.bipeds_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "bipeds"))
    SCENARIO.scenario_body.biped_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "bipeds palette"))
    SCENARIO.scenario_body.vehicles_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "vehicles"))
    SCENARIO.scenario_body.vehicle_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "vehicles palette"))
    SCENARIO.scenario_body.equipment_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "equipment"))
    SCENARIO.scenario_body.equipment_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "equipment palette"))
    SCENARIO.scenario_body.weapons_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "weapons"))
    SCENARIO.scenario_body.weapon_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "weapon palette"))
    SCENARIO.scenario_body.device_groups_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "device groups"))
    SCENARIO.scenario_body.machines_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "machines"))
    SCENARIO.scenario_body.machine_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "machine palette"))
    SCENARIO.scenario_body.controls_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "controls"))
    SCENARIO.scenario_body.control_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "control palette"))
    SCENARIO.scenario_body.light_fixtures_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "light fixtures"))
    SCENARIO.scenario_body.light_fixtures_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "light fixtures palette"))
    SCENARIO.scenario_body.sound_scenery_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "sound scenery"))
    SCENARIO.scenario_body.sound_scenery_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "sound scenery palette"))
    SCENARIO.scenario_body.light_volumes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "light volumes"))
    SCENARIO.scenario_body.light_volume_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "light volume palette"))
    SCENARIO.scenario_body.player_starting_profile_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "player starting profile"))
    SCENARIO.scenario_body.player_starting_locations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "player starting locations"))
    SCENARIO.scenario_body.trigger_volumes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "trigger volumes"))
    SCENARIO.scenario_body.recorded_animations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "recorded animations"))
    SCENARIO.scenario_body.netgame_flags_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "netgame flags"))
    SCENARIO.scenario_body.netgame_equipment_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "netgame equipment"))
    SCENARIO.scenario_body.starting_equipment_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "starting equipment"))
    SCENARIO.scenario_body.bsp_switch_trigger_volumes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "bsp switch trigger volumes"))
    SCENARIO.scenario_body.decals_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "decals"))
    SCENARIO.scenario_body.decal_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "decal palette"))
    SCENARIO.scenario_body.detail_object_collection_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "detail object collection palette"))
    SCENARIO.scenario_body.style_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "style palette"))
    SCENARIO.scenario_body.squad_groups_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "squad groups"))
    SCENARIO.scenario_body.squads_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "squads"))
    SCENARIO.scenario_body.zones_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "zones"))
    SCENARIO.scenario_body.mission_scenes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "mission scenes"))
    SCENARIO.scenario_body.character_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "character palette"))
    SCENARIO.scenario_body.ai_pathfinding_data_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai pathfinding data"))
    SCENARIO.scenario_body.ai_animation_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai animation references"))
    SCENARIO.scenario_body.ai_script_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai script references"))
    SCENARIO.scenario_body.ai_recording_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai recording references"))
    SCENARIO.scenario_body.ai_conversations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai conversations"))
    SCENARIO.scenario_body.script_syntax_data_tag_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(tag_node, "script syntax data"))
    SCENARIO.scenario_body.script_string_data_tag_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(tag_node, "script string data"))
    SCENARIO.scenario_body.scripts_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "scripts"))
    SCENARIO.scenario_body.globals_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "globals"))
    SCENARIO.scenario_body.references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "references"))
    SCENARIO.scenario_body.source_files_tag_block =TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "source files"))
    SCENARIO.scenario_body.scripting_data_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "scripting data"))
    SCENARIO.scenario_body.cutscene_flags_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "cutscene flags"))
    SCENARIO.scenario_body.cutscene_camera_points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "cutscene camera points"))
    SCENARIO.scenario_body.cutscene_titles_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "cutscene titles"))
    SCENARIO.scenario_body.custom_object_names_tag_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "custom object names"))
    SCENARIO.scenario_body.chapter_title_text_tag_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "chapter title text"))
    SCENARIO.scenario_body.hud_messages_tag_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "hud messages"))
    SCENARIO.scenario_body.structure_bsps_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "structure bsps"))
    SCENARIO.scenario_body.scenario_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "scenario resources"))
    SCENARIO.scenario_body.old_structure_physics_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "old structure physics"))
    SCENARIO.scenario_body.hs_unit_seats_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "hs unit seats"))
    SCENARIO.scenario_body.scenario_kill_triggers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "scenario kill triggers"))
    SCENARIO.scenario_body.hs_syntax_datums_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "hs syntax datums"))
    SCENARIO.scenario_body.orders_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "orders"))
    SCENARIO.scenario_body.triggers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "triggers"))
    SCENARIO.scenario_body.background_sound_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "background sound palette"))
    SCENARIO.scenario_body.sound_environment_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "sound environment palette"))
    SCENARIO.scenario_body.weather_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "weather palette"))
    SCENARIO.scenario_body.unused_0_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "unused 0"))
    SCENARIO.scenario_body.unused_1_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "unused 1"))
    SCENARIO.scenario_body.unused_2_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "unused 2"))
    SCENARIO.scenario_body.unused_3_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "unused 3"))
    SCENARIO.scenario_body.scavenger_hunt_objects_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "scavenger hunt objects"))
    SCENARIO.scenario_body.scenario_cluster_data_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "scenario cluster data"))

    SCENARIO.scenario_body.salt_array = []
    for salt_idx in range(SALT_SIZE):
        SCENARIO.scenario_body.salt_array.append(TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(tag_node, "salt %s" % salt_idx)))

    SCENARIO.scenario_body.spawn_data_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "spawn data"))
    SCENARIO.scenario_body.sound_effect_collection_tag_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "sound effect collection"))
    SCENARIO.scenario_body.crates_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "crates"))
    SCENARIO.scenario_body.crate_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "crate palette"))
    SCENARIO.scenario_body.global_lighting_tag_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "global lighting"))
    SCENARIO.scenario_body.atmospheric_fog_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "atmospheric fog palette"))
    SCENARIO.scenario_body.planar_fog_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "planar fog palette"))
    SCENARIO.scenario_body.flocks_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "flocks"))
    SCENARIO.scenario_body.subtitles_tag_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "subtitles"))
    SCENARIO.scenario_body.decorators_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "decorators"))
    SCENARIO.scenario_body.creatures_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "creatures"))
    SCENARIO.scenario_body.creature_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "creatures palette"))
    SCENARIO.scenario_body.decorator_palette_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "decorator palette"))
    SCENARIO.scenario_body.bsp_transition_volumes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "bsp transition volumes"))
    SCENARIO.scenario_body.structure_bsp_lighting_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "structure bsp lighting"))
    SCENARIO.scenario_body.editor_folders_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "editor folders"))
    SCENARIO.scenario_body.level_data_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "level data"))
    SCENARIO.scenario_body.game_engine_strings_tag_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "game engine strings"))
    input_stream.read(8) # Padding?
    SCENARIO.scenario_body.mission_dialogue_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "mission dialogue"))
    SCENARIO.scenario_body.objectives_tag_ref = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "objectives"))
    SCENARIO.scenario_body.interpolators_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "interpolators"))
    SCENARIO.scenario_body.shared_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "shared references"))
    SCENARIO.scenario_body.screen_effect_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "screen effect references"))
    SCENARIO.scenario_body.simulation_definition_table_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "simulation definition table"))

def read_skies(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.skies_tag_block.count > 0:
        SCENARIO.skies_header = TAG.TagBlockHeader().read(input_stream, TAG)
        sky_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.skies_tag_block.count, tag_node, "name", "skies")
        for sky_idx in range(SCENARIO.scenario_body.skies_tag_block.count):
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

def read_child_scenarios(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.child_scenarios_tag_block.count > 0:
        SCENARIO.child_scenario_header = TAG.TagBlockHeader().read(input_stream, TAG)
        child_scenario_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.child_scenarios_tag_block.count, tag_node, "name", "child scenarios")
        for child_scenario_idx in range(SCENARIO.scenario_body.child_scenarios_tag_block.count):
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

def read_predicted_resources(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.predicted_resources_tag_block.count > 0:
        SCENARIO.predicted_resources_header = TAG.TagBlockHeader().read(input_stream, TAG)
        predicted_resource_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.predicted_resources_tag_block.count, tag_node, "name", "predicted resources")
        for predicted_resource_idx in range(SCENARIO.scenario_body.predicted_resources_tag_block.count):
            predicted_resource_element_node = None
            if XML_OUTPUT:
                predicted_resource_element_node = TAG.xml_doc.createElement('element')
                predicted_resource_element_node.setAttribute('index', str(predicted_resource_idx))
                predicted_resource_node.appendChild(predicted_resource_element_node)

            SCENARIO.predicted_resources.append(get_predicted_resource(input_stream, SCENARIO, TAG, predicted_resource_element_node))

    if SCENARIO.scenario_body.functions_tag_block.count > 0:
        SCENARIO.functions_header = TAG.TagBlockHeader().read(input_stream, TAG)
        function_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.functions_tag_block.count, tag_node, "name", "functions")
        for function_idx in range(SCENARIO.scenario_body.functions_tag_block.count):
            function_element_node = None
            if XML_OUTPUT:
                function_element_node = TAG.xml_doc.createElement('element')
                function_element_node.setAttribute('index', str(function_idx))
                function_node.appendChild(function_element_node)

            SCENARIO.functions.append(get_functions(input_stream, SCENARIO, TAG, function_element_node))

def read_comments(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.comments_tag_block.count > 0:
        SCENARIO.comment_header = TAG.TagBlockHeader().read(input_stream, TAG)
        comment_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.comments_tag_block.count, tag_node, "name", "comments")
        for comment_idx in range(SCENARIO.scenario_body.comments_tag_block.count):
            comment_element_node = None
            if XML_OUTPUT:
                comment_element_node = TAG.xml_doc.createElement('element')
                comment_element_node.setAttribute('index', str(comment_idx))
                comment_node.appendChild(comment_element_node)

            SCENARIO.comments.append(get_comments(input_stream, SCENARIO, TAG, comment_element_node))

def read_environment_objects(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.environment_objects_tag_block.count > 0:
        SCENARIO.environment_objects_header = TAG.TagBlockHeader().read(input_stream, TAG)
        environment_objects_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.environment_objects_tag_block.count, tag_node, "name", "environment objects")
        for environment_object_idx in range(SCENARIO.scenario_body.environment_objects_tag_block.count):
            environment_object_element_node = None
            if XML_OUTPUT:
                environment_object_element_node = TAG.xml_doc.createElement('element')
                environment_object_element_node.setAttribute('index', str(environment_object_idx))
                environment_objects_node.appendChild(environment_object_element_node)

            SCENARIO.environment_objects.append(get_environment_objects(input_stream, SCENARIO, TAG, environment_object_element_node))

def read_object_names(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.object_names_tag_block.count > 0:
        SCENARIO.object_name_header = TAG.TagBlockHeader().read(input_stream, TAG)
        object_name_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.object_names_tag_block.count, tag_node, "name", "object names")
        for object_name_idx in range(SCENARIO.scenario_body.object_names_tag_block.count):
            object_name_element_node = None
            if XML_OUTPUT:
                object_name_element_node = TAG.xml_doc.createElement('element')
                object_name_element_node.setAttribute('index', str(object_name_idx))
                object_name_node.appendChild(object_name_element_node)

            SCENARIO.object_names.append(get_object_names(input_stream, SCENARIO, TAG, object_name_element_node))

def read_scenery(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.scenery_tag_block.count > 0:
        SCENARIO.scenery_header = TAG.TagBlockHeader().read(input_stream, TAG)
        scenery_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.scenery_tag_block.count, tag_node, "name", "scenery")
        for scenery_idx in range(SCENARIO.scenario_body.scenery_tag_block.count):
            scenery_element_node = None
            if XML_OUTPUT:
                scenery_element_node = TAG.xml_doc.createElement('element')
                scenery_element_node.setAttribute('index', str(scenery_idx))
                scenery_node.appendChild(scenery_element_node)

            SCENARIO.scenery.append(get_scenery(input_stream, SCENARIO, TAG, scenery_element_node))

        for scenery_idx, scenery in enumerate(SCENARIO.scenery):
            scenery_element_node = None
            if XML_OUTPUT:
                scenery_element_node = scenery_node.childNodes[scenery_idx]

            scenery.sobj_header = TAG.TagBlockHeader().read(input_stream, TAG)
            scenery.obj0_header = TAG.TagBlockHeader().read(input_stream, TAG)
            scenery.sper_header = TAG.TagBlockHeader().read(input_stream, TAG)
            if scenery.variant_name_length > 0:
                scenery.variant_name = TAG.read_variable_string_no_terminator(input_stream, scenery.variant_name_length, TAG, tag_format.XMLData(scenery_element_node, "variant name"))

            scenery.sct3_header = TAG.TagBlockHeader().read(input_stream, TAG)

            scenery.pathfinding_references = []
            if scenery.pathfinding_references_tag_block.count > 0:
                scenery.pathfinding_references_header = TAG.TagBlockHeader().read(input_stream, TAG)
                pathfinding_reference_node = tag_format.get_xml_node(XML_OUTPUT, scenery.pathfinding_references_tag_block.count, scenery_element_node, "name", "pathfinding references")
                for pathfinding_reference_idx in range(scenery.pathfinding_references_tag_block.count):
                    pathfinding_reference_element_node = None
                    if XML_OUTPUT:
                        pathfinding_reference_element_node = TAG.xml_doc.createElement('element')
                        pathfinding_reference_element_node.setAttribute('index', str(pathfinding_reference_idx))
                        pathfinding_reference_node.appendChild(pathfinding_reference_element_node)

                    pathfinding_reference = SCENARIO.PathfindingReference()
                    pathfinding_reference.bsp_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(pathfinding_reference_element_node, "bsp index"))
                    pathfinding_reference.pathfinding_object_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(pathfinding_reference_element_node, "pathfinding object index"))

                    scenery.pathfinding_references.append(pathfinding_reference)

    palette_helper(input_stream, SCENARIO.scenario_body.scenery_palette_tag_block.count, "scenery palette", SCENARIO.scenery_palette_header, SCENARIO.scenery_palette, tag_node, TAG)

def read_bipeds(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.bipeds_tag_block.count > 0:
        SCENARIO.bipeds_header = TAG.TagBlockHeader().read(input_stream, TAG)
        biped_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.bipeds_tag_block.count, tag_node, "name", "bipeds")
        for biped_idx in range(SCENARIO.scenario_body.bipeds_tag_block.count):
            biped_element_node = None
            if XML_OUTPUT:
                biped_element_node = TAG.xml_doc.createElement('element')
                biped_element_node.setAttribute('index', str(biped_idx))
                biped_node.appendChild(biped_element_node)

            SCENARIO.bipeds.append(get_units(input_stream, SCENARIO, TAG, biped_element_node, SCENARIO.scenario_body.biped_palette_tag_block.count, "scenario_biped_palette_block"))

        for biped_idx, biped in enumerate(SCENARIO.bipeds):
            biped_element_node = None
            if XML_OUTPUT:
                biped_element_node = biped_node.childNodes[biped_idx]

            biped.sobj_header = TAG.TagBlockHeader().read(input_stream, TAG)
            biped.obj0_header = TAG.TagBlockHeader().read(input_stream, TAG)
            biped.sper_header = TAG.TagBlockHeader().read(input_stream, TAG)
            if biped.variant_name_length > 0:
                biped.variant_name = TAG.read_variable_string_no_terminator(input_stream, biped.variant_name_length, TAG, tag_format.XMLData(biped_element_node, "variant name"))

            biped.sunt_header = TAG.TagBlockHeader().read(input_stream, TAG)

    palette_helper(input_stream, SCENARIO.scenario_body.biped_palette_tag_block.count, "bipeds palette", SCENARIO.biped_palette_header, SCENARIO.biped_palette, tag_node, TAG)

def read_vehicles(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.vehicles_tag_block.count > 0:
        SCENARIO.vehicles_header = TAG.TagBlockHeader().read(input_stream, TAG)
        vehicle_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.vehicles_tag_block.count, tag_node, "name", "vehicles")
        for vehicle_idx in range(SCENARIO.scenario_body.vehicles_tag_block.count):
            vehicle_element_node = None
            if XML_OUTPUT:
                vehicle_element_node = TAG.xml_doc.createElement('element')
                vehicle_element_node.setAttribute('index', str(vehicle_idx))
                vehicle_node.appendChild(vehicle_element_node)

            SCENARIO.vehicles.append(get_units(input_stream, SCENARIO, TAG, vehicle_element_node, SCENARIO.scenario_body.vehicle_palette_tag_block.count, "scenario_vehicle_palette_block"))

        for vehicle_idx, vehicle in enumerate(SCENARIO.vehicles):
            vehicle_element_node = None
            if XML_OUTPUT:
                vehicle_element_node = vehicle_node.childNodes[vehicle_idx]

            vehicle.sobj_header = TAG.TagBlockHeader().read(input_stream, TAG)
            vehicle.obj0_header = TAG.TagBlockHeader().read(input_stream, TAG)
            vehicle.sper_header = TAG.TagBlockHeader().read(input_stream, TAG)
            if vehicle.variant_name_length > 0:
                vehicle.variant_name = TAG.read_variable_string_no_terminator(input_stream, vehicle.variant_name_length, TAG, tag_format.XMLData(vehicle_element_node, "variant name"))

            vehicle.sunt_header = TAG.TagBlockHeader().read(input_stream, TAG)

    palette_helper(input_stream, SCENARIO.scenario_body.vehicle_palette_tag_block.count, "vehicles palette", SCENARIO.vehicle_palette_header, SCENARIO.vehicle_palette, tag_node, TAG)

def read_equipment(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.equipment_tag_block.count > 0:
        SCENARIO.equipment_header = TAG.TagBlockHeader().read(input_stream, TAG)
        equipment_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.equipment_tag_block.count, tag_node, "name", "equipment")
        for equipment_idx in range(SCENARIO.scenario_body.equipment_tag_block.count):
            equipment_element_node = None
            if XML_OUTPUT:
                equipment_element_node = TAG.xml_doc.createElement('element')
                equipment_element_node.setAttribute('index', str(equipment_idx))
                equipment_node.appendChild(equipment_element_node)

            SCENARIO.equipment.append(get_equipment(input_stream, SCENARIO, TAG, equipment_element_node))

        for equipment_idx, equipment in enumerate(SCENARIO.equipment):
            equipment_element_node = None
            if XML_OUTPUT:
                equipment_element_node = equipment_node.childNodes[equipment_idx]

            equipment.sobj_header = TAG.TagBlockHeader().read(input_stream, TAG)
            equipment.obj0_header = TAG.TagBlockHeader().read(input_stream, TAG)
            equipment.seqt_header = TAG.TagBlockHeader().read(input_stream, TAG)

    palette_helper(input_stream, SCENARIO.scenario_body.equipment_palette_tag_block.count, "equipment palette", SCENARIO.equipment_palette_header, SCENARIO.equipment_palette, tag_node, TAG)

def read_weapon(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.weapons_tag_block.count > 0:
        SCENARIO.weapon_header = TAG.TagBlockHeader().read(input_stream, TAG)
        weapon_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.weapons_tag_block.count, tag_node, "name", "weapons")
        for weapon_idx in range(SCENARIO.scenario_body.weapons_tag_block.count):
            weapon_element_node = None
            if XML_OUTPUT:
                weapon_element_node = TAG.xml_doc.createElement('element')
                weapon_element_node.setAttribute('index', str(weapon_idx))
                weapon_node.appendChild(weapon_element_node)

            SCENARIO.weapons.append(get_weapons(input_stream, SCENARIO, TAG, weapon_element_node))

        for weapon_idx, weapon in enumerate(SCENARIO.weapons):
            weapon_element_node = None
            if XML_OUTPUT:
                weapon_element_node = weapon_node.childNodes[weapon_idx]

            weapon.sobj_header = TAG.TagBlockHeader().read(input_stream, TAG)
            weapon.obj0_header = TAG.TagBlockHeader().read(input_stream, TAG)
            weapon.sper_header = TAG.TagBlockHeader().read(input_stream, TAG)
            if weapon.variant_name_length > 0:
                weapon.variant_name = TAG.read_variable_string_no_terminator(input_stream, weapon.variant_name_length, TAG, tag_format.XMLData(weapon_element_node, "variant name"))

            weapon.swpt_header = TAG.TagBlockHeader().read(input_stream, TAG)

    palette_helper(input_stream, SCENARIO.scenario_body.weapon_palette_tag_block.count, "weapon palette", SCENARIO.weapon_palette_header, SCENARIO.weapon_palette, tag_node, TAG)

def read_device_groups(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.device_groups_tag_block.count > 0:
        SCENARIO.device_group_header = TAG.TagBlockHeader().read(input_stream, TAG)
        device_group_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.device_groups_tag_block.count, tag_node, "name", "device groups")
        for device_group_idx in range(SCENARIO.scenario_body.device_groups_tag_block.count):
            device_group_element_node = None
            if XML_OUTPUT:
                device_group_element_node = TAG.xml_doc.createElement('element')
                device_group_element_node.setAttribute('index', str(device_group_idx))
                device_group_node.appendChild(device_group_element_node)

            SCENARIO.device_groups.append(get_device_groups(input_stream, SCENARIO, TAG, device_group_element_node))

def read_machines(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.machines_tag_block.count > 0:
        SCENARIO.device_machine_header = TAG.TagBlockHeader().read(input_stream, TAG)
        device_machine_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.machines_tag_block.count, tag_node, "name", "machines")
        for device_machine_idx in range(SCENARIO.scenario_body.machines_tag_block.count):
            device_machine_element_node = None
            if XML_OUTPUT:
                device_machine_element_node = TAG.xml_doc.createElement('element')
                device_machine_element_node.setAttribute('index', str(device_machine_idx))
                device_machine_node.appendChild(device_machine_element_node)

            SCENARIO.device_machines.append(get_machines(input_stream, SCENARIO, TAG, device_machine_element_node))

        for device_machine_idx, device_machine in enumerate(SCENARIO.device_machines):
            device_machine_element_node = None
            if XML_OUTPUT:
                device_machine_element_node = device_machine_node.childNodes[device_machine_idx]

            device_machine.sobj_header = TAG.TagBlockHeader().read(input_stream, TAG)
            device_machine.obj0_header = TAG.TagBlockHeader().read(input_stream, TAG)
            device_machine.sdvt_header = TAG.TagBlockHeader().read(input_stream, TAG)
            device_machine.smht_header = TAG.TagBlockHeader().read(input_stream, TAG)

            device_machine.pathfinding_references = []
            if device_machine.pathfinding_references_tag_block.count > 0:
                device_machine.pathfinding_references_header = TAG.TagBlockHeader().read(input_stream, TAG)
                pathfinding_reference_node = tag_format.get_xml_node(XML_OUTPUT, device_machine.pathfinding_references_tag_block.count, device_machine_element_node, "name", "pathfinding references")
                for pathfinding_reference_idx in range(device_machine.pathfinding_references_tag_block.count):
                    pathfinding_reference_element_node = None
                    if XML_OUTPUT:
                        pathfinding_reference_element_node = TAG.xml_doc.createElement('element')
                        pathfinding_reference_element_node.setAttribute('index', str(pathfinding_reference_idx))
                        pathfinding_reference_node.appendChild(pathfinding_reference_element_node)

                    pathfinding_reference = SCENARIO.PathfindingReference()
                    pathfinding_reference.bsp_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(pathfinding_reference_element_node, "bsp index"))
                    pathfinding_reference.pathfinding_object_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(pathfinding_reference_element_node, "pathfinding object index"))

                    device_machine.pathfinding_references.append(pathfinding_reference)

    palette_helper(input_stream, SCENARIO.scenario_body.machine_palette_tag_block.count, "machine palette", SCENARIO.device_machine_palette_header, SCENARIO.device_machine_palette, tag_node, TAG)

def read_controls(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.controls_tag_block.count > 0:
        SCENARIO.device_control_header = TAG.TagBlockHeader().read(input_stream, TAG)
        device_control_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.controls_tag_block.count, tag_node, "name", "controls")
        for device_control_idx in range(SCENARIO.scenario_body.controls_tag_block.count):
            device_control_element_node = None
            if XML_OUTPUT:
                device_control_element_node = TAG.xml_doc.createElement('element')
                device_control_element_node.setAttribute('index', str(device_control_idx))
                device_control_node.appendChild(device_control_element_node)

            SCENARIO.device_controls.append(get_controls(input_stream, SCENARIO, TAG, device_control_element_node))

        for device_control_idx, device_control in enumerate(SCENARIO.device_controls):
            device_control_element_node = None
            if XML_OUTPUT:
                device_control_element_node = device_control_node.childNodes[device_control_idx]

            device_control.sobj_header = TAG.TagBlockHeader().read(input_stream, TAG)
            device_control.obj0_header = TAG.TagBlockHeader().read(input_stream, TAG)
            device_control.sdvt_header = TAG.TagBlockHeader().read(input_stream, TAG)
            device_control.sctt_header = TAG.TagBlockHeader().read(input_stream, TAG)

    palette_helper(input_stream, SCENARIO.scenario_body.control_palette_tag_block.count, "control palette", SCENARIO.device_control_palette_header, SCENARIO.device_control_palette, tag_node, TAG)

def read_light_fixtures(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.light_fixtures_tag_block.count > 0:
        SCENARIO.device_light_fixture_header = TAG.TagBlockHeader().read(input_stream, TAG)
        light_fixtures_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.light_fixtures_tag_block.count, tag_node, "name", "light fixtures")
        for light_fixture_idx in range(SCENARIO.scenario_body.light_fixtures_tag_block.count):
            light_fixture_element_node = None
            if XML_OUTPUT:
                light_fixture_element_node = TAG.xml_doc.createElement('element')
                light_fixture_element_node.setAttribute('index', str(light_fixture_idx))
                light_fixtures_node.appendChild(light_fixture_element_node)

            SCENARIO.device_light_fixtures.append(get_light_fixtures(input_stream, SCENARIO, TAG, light_fixture_element_node))

        for device_light_fixture_idx, device_light_fixture in enumerate(SCENARIO.device_light_fixtures):
            light_fixture_element_node = None
            if XML_OUTPUT:
                light_fixture_element_node = light_fixtures_node.childNodes[device_light_fixture_idx]

            device_light_fixture.sobj_header = TAG.TagBlockHeader().read(input_stream, TAG)
            device_light_fixture.obj0_header = TAG.TagBlockHeader().read(input_stream, TAG)
            device_light_fixture.sdvt_header = TAG.TagBlockHeader().read(input_stream, TAG)
            device_light_fixture.slft_header = TAG.TagBlockHeader().read(input_stream, TAG)

    palette_helper(input_stream, SCENARIO.scenario_body.light_fixtures_palette_tag_block.count, "light fixtures palette", SCENARIO.device_light_fixture_palette_header, SCENARIO.device_light_fixtures_palette, tag_node, TAG)

def read_sound_scenery(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.sound_scenery_tag_block.count > 0:
        SCENARIO.sound_scenery_header = TAG.TagBlockHeader().read(input_stream, TAG)
        sound_scenery_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.sound_scenery_tag_block.count, tag_node, "name", "sound scenery")
        for sound_scenery_idx in range(SCENARIO.scenario_body.sound_scenery_tag_block.count):
            sound_scenery_element_node = None
            if XML_OUTPUT:
                sound_scenery_element_node = TAG.xml_doc.createElement('element')
                sound_scenery_element_node.setAttribute('index', str(sound_scenery_idx))
                sound_scenery_node.appendChild(sound_scenery_element_node)

            SCENARIO.sound_scenery.append(get_sound_scenery(input_stream, SCENARIO, TAG, sound_scenery_element_node))

        for sound_scenery_idx, device_light_fixture in enumerate(SCENARIO.sound_scenery):
            sound_scenery_element_node = None
            if XML_OUTPUT:
                sound_scenery_element_node = sound_scenery_node.childNodes[sound_scenery_idx]

            device_light_fixture.sobj_header = TAG.TagBlockHeader().read(input_stream, TAG)
            device_light_fixture.obj0_header = TAG.TagBlockHeader().read(input_stream, TAG)
            device_light_fixture._sc__header = TAG.TagBlockHeader().read(input_stream, TAG)

    palette_helper(input_stream, SCENARIO.scenario_body.sound_scenery_palette_tag_block.count, "sound scenery palette", SCENARIO.sound_scenery_palette_header, SCENARIO.sound_scenery_palette, tag_node, TAG)

def read_light_volumes(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.light_volumes_tag_block.count > 0:
        SCENARIO.light_volume_header = TAG.TagBlockHeader().read(input_stream, TAG)
        light_volume_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.light_volumes_tag_block.count, tag_node, "name", "light volumes")
        for light_volume_idx in range(SCENARIO.scenario_body.light_volumes_tag_block.count):
            light_volume_element_node = None
            if XML_OUTPUT:
                light_volume_element_node = TAG.xml_doc.createElement('element')
                light_volume_element_node.setAttribute('index', str(light_volume_idx))
                light_volume_node.appendChild(light_volume_element_node)

            SCENARIO.light_volumes.append(get_light_volumes(input_stream, SCENARIO, TAG, light_volume_element_node))

        for light_volume_idx, light_volume in enumerate(SCENARIO.light_volumes):
            light_volume_element_node = None
            if XML_OUTPUT:
                light_volume_element_node = light_volume_node.childNodes[light_volume_idx]

            light_volume.sobj_header = TAG.TagBlockHeader().read(input_stream, TAG)
            light_volume.obj0_header = TAG.TagBlockHeader().read(input_stream, TAG)
            light_volume.sdvt_header = TAG.TagBlockHeader().read(input_stream, TAG)
            light_volume.slit_header = TAG.TagBlockHeader().read(input_stream, TAG)

    palette_helper(input_stream, SCENARIO.scenario_body.light_volume_palette_tag_block.count, "light volume palette", SCENARIO.light_volume_palette_header, SCENARIO.light_volume_palette, tag_node, TAG)

def read_player_starting_profiles(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.player_starting_profile_tag_block.count > 0:
        SCENARIO.player_starting_profile_header = TAG.TagBlockHeader().read(input_stream, TAG)
        player_starting_profile_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.player_starting_profile_tag_block.count, tag_node, "name", "player starting profile")
        for player_starting_profile_idx in range(SCENARIO.scenario_body.player_starting_profile_tag_block.count):
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

def read_player_starting_locations(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.player_starting_locations_tag_block.count > 0:
        SCENARIO.player_starting_location_header = TAG.TagBlockHeader().read(input_stream, TAG)
        player_starting_locations_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.player_starting_locations_tag_block.count, tag_node, "name", "player starting locations")
        for player_starting_location_idx in range(SCENARIO.scenario_body.player_starting_locations_tag_block.count):
            player_starting_location_element_node = None
            if XML_OUTPUT:
                player_starting_location_element_node = TAG.xml_doc.createElement('element')
                player_starting_location_element_node.setAttribute('index', str(player_starting_location_idx))
                player_starting_locations_node.appendChild(player_starting_location_element_node)

            SCENARIO.player_starting_locations.append(get_player_starting_locations(input_stream, SCENARIO, TAG, player_starting_location_element_node))

        for player_starting_location_idx, player_starting_location in enumerate(SCENARIO.player_starting_locations):
            player_starting_location_element_node = None
            if XML_OUTPUT:
                player_starting_location_element_node = player_starting_locations_node.childNodes[player_starting_location_idx]

            if player_starting_location.unk_0_length > 0:
                player_starting_location.unk_0 = TAG.read_variable_string_no_terminator(input_stream, player_starting_location.unk_0_length, TAG, tag_format.XMLData(player_starting_location_element_node, "unused_names0"))
            if player_starting_location.unk_1_length > 0:
                player_starting_location.unk_1 = TAG.read_variable_string_no_terminator(input_stream, player_starting_location.unk_1_length, TAG, tag_format.XMLData(player_starting_location_element_node, "unused_names1"))

def read_trigger_volumes(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.trigger_volumes_tag_block.count > 0:
        SCENARIO.trigger_volumes_header = TAG.TagBlockHeader().read(input_stream, TAG)
        trigger_volume_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.trigger_volumes_tag_block.count, tag_node, "name", "trigger volumes")
        for trigger_volume_idx in range(SCENARIO.scenario_body.trigger_volumes_tag_block.count):
            trigger_volume_element_node = None
            if XML_OUTPUT:
                trigger_volume_element_node = TAG.xml_doc.createElement('element')
                trigger_volume_element_node.setAttribute('index', str(trigger_volume_idx))
                trigger_volume_node.appendChild(trigger_volume_element_node)

            SCENARIO.trigger_volumes.append(get_trigger_volumes(input_stream, SCENARIO, TAG, trigger_volume_element_node))

        for trigger_volume_idx, trigger_volume in enumerate(SCENARIO.trigger_volumes):
            trigger_volume_element_node = None
            if XML_OUTPUT:
                trigger_volume_element_node = trigger_volume_node.childNodes[trigger_volume_idx]

            if trigger_volume.name_length > 0:
                trigger_volume.name = TAG.read_variable_string_no_terminator(input_stream, trigger_volume.name_length, TAG, tag_format.XMLData(trigger_volume_element_node, "name"))
            if trigger_volume.node_name_length > 0:
                trigger_volume.node_name = TAG.read_variable_string_no_terminator(input_stream, trigger_volume.node_name_length, TAG, tag_format.XMLData(trigger_volume_element_node, "node name"))

def read_recorded_animations(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.recorded_animations_tag_block.count > 0:
        SCENARIO.recorded_animation_header = TAG.TagBlockHeader().read(input_stream, TAG)
        recorded_animations_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.recorded_animations_tag_block.count, tag_node, "name", "recorded animations")
        for recorded_animation_idx in range(SCENARIO.scenario_body.recorded_animations_tag_block.count):
            recorded_animation_element_node = None
            if XML_OUTPUT:
                recorded_animation_element_node = TAG.xml_doc.createElement('element')
                recorded_animation_element_node.setAttribute('index', str(recorded_animation_idx))
                recorded_animations_node.appendChild(recorded_animation_element_node)

            SCENARIO.recorded_animations.append(get_recorded_animations(input_stream, SCENARIO, TAG, recorded_animation_element_node))

        for recorded_animation in SCENARIO.recorded_animations:
            recorded_animation.recorded_animation_event_stream = input_stream.read(recorded_animation.recorded_animation_event_stream_tag_data.size)

def read_netgame_flags(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.netgame_flags_tag_block.count > 0:
        SCENARIO.netgame_flag_header = TAG.TagBlockHeader().read(input_stream, TAG)
        netgame_flag_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.netgame_flags_tag_block.count, tag_node, "name", "netgame flags")
        for netgame_flag_idx in range(SCENARIO.scenario_body.netgame_flags_tag_block.count):
            netgame_flag_element_node = None
            if XML_OUTPUT:
                netgame_flag_element_node = TAG.xml_doc.createElement('element')
                netgame_flag_element_node.setAttribute('index', str(netgame_flag_idx))
                netgame_flag_node.appendChild(netgame_flag_element_node)

            SCENARIO.netgame_flags.append(get_netgame_flags(input_stream, SCENARIO, TAG, netgame_flag_element_node))

        for netgame_flag_idx, netgame_flag in enumerate(SCENARIO.netgame_flags):
            netgame_flag_element_node = None
            if XML_OUTPUT:
                netgame_flag_element_node = netgame_flag_node.childNodes[netgame_flag_idx]

            if netgame_flag.spawn_object_name_length > 0:
                netgame_flag.spawn_object_name = TAG.read_variable_string_no_terminator(input_stream, netgame_flag.spawn_object_name_length, TAG, tag_format.XMLData(netgame_flag_element_node, "spawn_object_name"))
            if netgame_flag.spawn_marker_name_length > 0:
                netgame_flag.spawn_marker_name = TAG.read_variable_string_no_terminator(input_stream, netgame_flag.spawn_marker_name_length, TAG, tag_format.XMLData(netgame_flag_element_node, "spawn_marker_name"))

def read_netgame_equipment(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.netgame_equipment_tag_block.count > 0:
        SCENARIO.netgame_equipment_header = TAG.TagBlockHeader().read(input_stream, TAG)
        netgame_equipment_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.netgame_equipment_tag_block.count, tag_node, "name", "netgame equipment")
        for netgame_equipment_idx in range(SCENARIO.scenario_body.netgame_equipment_tag_block.count):
            netgame_equipment_element_node = None
            if XML_OUTPUT:
                netgame_equipment_element_node = TAG.xml_doc.createElement('element')
                netgame_equipment_element_node.setAttribute('index', str(netgame_equipment_idx))
                netgame_equipment_node.appendChild(netgame_equipment_element_node)

            SCENARIO.netgame_equipment.append(get_netgame_equipment(input_stream, SCENARIO, TAG, netgame_equipment_element_node))

        for netgame_equipment_idx, netgame_equipment in enumerate(SCENARIO.netgame_equipment):
            item_collection = netgame_equipment.item_vehicle_collection
            item_collection_name_length = item_collection.name_length
            netgame_equipment.ntor_header = TAG.TagBlockHeader().read(input_stream, TAG)

            if item_collection_name_length > 0:
                item_collection.name = TAG.read_variable_string(input_stream, item_collection_name_length, TAG)

            if XML_OUTPUT:
                netgame_equipment_element_node = netgame_equipment_node.childNodes[netgame_equipment_idx]
                item_collection_node = tag_format.get_xml_node(XML_OUTPUT, 1, netgame_equipment_element_node, "name", "item vehicle collection")
                item_collection.append_xml_attributes(item_collection_node)

def read_starting_equipment(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.starting_equipment_tag_block.count > 0:
        SCENARIO.starting_equipment_header = TAG.TagBlockHeader().read(input_stream, TAG)
        starting_equipment_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.starting_equipment_tag_block.count, tag_node, "name", "starting equipment")
        for starting_equipment_idx in range(SCENARIO.scenario_body.starting_equipment_tag_block.count):
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

def read_bsp_switch_trigger_volumes(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.bsp_switch_trigger_volumes_tag_block.count > 0:
        SCENARIO.bsp_switch_trigger_volumes_header = TAG.TagBlockHeader().read(input_stream, TAG)
        bsp_switch_trigger_volume_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.bsp_switch_trigger_volumes_tag_block.count, tag_node, "name", "bsp switch trigger volumes")
        for bsp_switch_trigger_volume_idx in range(SCENARIO.scenario_body.bsp_switch_trigger_volumes_tag_block.count):
            bsp_switch_trigger_volume_element_node = None
            if XML_OUTPUT:
                bsp_switch_trigger_volume_element_node = TAG.xml_doc.createElement('element')
                bsp_switch_trigger_volume_element_node.setAttribute('index', str(bsp_switch_trigger_volume_idx))
                bsp_switch_trigger_volume_node.appendChild(bsp_switch_trigger_volume_element_node)

            SCENARIO.bsp_switch_trigger_volumes.append(get_bsp_switch_trigger_volumes(input_stream, SCENARIO, TAG, bsp_switch_trigger_volume_element_node))

def read_decals(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.decals_tag_block.count > 0:
        SCENARIO.decals_header = TAG.TagBlockHeader().read(input_stream, TAG)
        decal_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.decals_tag_block.count, tag_node, "name", "decals")
        for decal_idx in range(SCENARIO.scenario_body.decals_tag_block.count):
            decal_element_node = None
            if XML_OUTPUT:
                decal_element_node = TAG.xml_doc.createElement('element')
                decal_element_node.setAttribute('index', str(decal_idx))
                decal_node.appendChild(decal_element_node)

            SCENARIO.decals.append(get_decals(input_stream, SCENARIO, TAG, decal_element_node))

def read_decal_palette(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.decal_palette_tag_block.count > 0:
        SCENARIO.decal_palette_header = TAG.TagBlockHeader().read(input_stream, TAG)
        decal_palette_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.decal_palette_tag_block.count, tag_node, "name", "decal palette")
        for decal_palette_idx in range(SCENARIO.scenario_body.decal_palette_tag_block.count):
            decal_palette_element_node = None
            if XML_OUTPUT:
                decal_palette_element_node = TAG.xml_doc.createElement('element')
                decal_palette_element_node.setAttribute('index', str(decal_palette_idx))
                decal_palette_node.appendChild(decal_palette_element_node)

            SCENARIO.decal_palette.append(get_palette(input_stream, TAG, decal_palette_element_node, 0))

        for decal_palette_idx, decal_palette in enumerate(SCENARIO.decal_palette):
            decal_palette_name_length = decal_palette.name_length
            if decal_palette_name_length > 0:
                decal_palette.name = TAG.read_variable_string(input_stream, decal_palette_name_length, TAG)

            if XML_OUTPUT:
                decal_palette_element_node = decal_palette_node.childNodes[decal_palette_idx]
                decal_palette_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, decal_palette_element_node, "name", "name")
                decal_palette.append_xml_attributes(decal_palette_tag_ref_node)

def read_detail_object_collection_palette(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.detail_object_collection_palette_tag_block.count > 0:
        SCENARIO.detail_object_collection_palette_header = TAG.TagBlockHeader().read(input_stream, TAG)
        detail_object_collection_palette_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.detail_object_collection_palette_tag_block.count, tag_node, "name", "detail object collection palette")
        for detail_object_collection_palette_idx in range(SCENARIO.scenario_body.detail_object_collection_palette_tag_block.count):
            detail_object_collection_palette_element_node = None
            if XML_OUTPUT:
                detail_object_collection_palette_element_node = TAG.xml_doc.createElement('element')
                detail_object_collection_palette_element_node.setAttribute('index', str(detail_object_collection_palette_idx))
                detail_object_collection_palette_node.appendChild(detail_object_collection_palette_element_node)

            SCENARIO.detail_object_collection_palette.append(get_palette(input_stream, TAG, detail_object_collection_palette_element_node))

        for detail_object_collection_palette_idx, detail_object_collection_palette in enumerate(SCENARIO.detail_object_collection_palette):
            detail_object_collection_palette_name_length = detail_object_collection_palette.name_length
            if detail_object_collection_palette_name_length > 0:
                detail_object_collection_palette.name = TAG.read_variable_string(input_stream, detail_object_collection_palette_name_length, TAG)

            if XML_OUTPUT:
                detail_object_collection_palette_element_node = detail_object_collection_palette_node.childNodes[detail_object_collection_palette_idx]
                detail_object_collection_palette_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, detail_object_collection_palette_element_node, "name", "name")
                detail_object_collection_palette.append_xml_attributes(detail_object_collection_palette_tag_ref_node)

def read_style_palette(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.style_palette_tag_block.count > 0:
        SCENARIO.style_palette_header = TAG.TagBlockHeader().read(input_stream, TAG)
        style_palette_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.style_palette_tag_block.count, tag_node, "name", "style palette")
        for style_palette_idx in range(SCENARIO.scenario_body.style_palette_tag_block.count):
            style_palette_element_node = None
            if XML_OUTPUT:
                style_palette_element_node = TAG.xml_doc.createElement('element')
                style_palette_element_node.setAttribute('index', str(style_palette_idx))
                style_palette_node.appendChild(style_palette_element_node)

            SCENARIO.style_palette.append(get_palette(input_stream, TAG, style_palette_element_node, 0))

        for style_palette_idx, style_palette in enumerate(SCENARIO.style_palette):
            style_palette_name_length = style_palette.name_length
            if style_palette_name_length > 0:
                style_palette.name = TAG.read_variable_string(input_stream, style_palette_name_length, TAG)

            if XML_OUTPUT:
                style_palette_element_node = style_palette_node.childNodes[style_palette_idx]
                style_palette_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, style_palette_element_node, "name", "name")
                style_palette.append_xml_attributes(style_palette_tag_ref_node)

def read_squad_groups(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.squad_groups_tag_block.count > 0:
        SCENARIO.squad_groups_header = TAG.TagBlockHeader().read(input_stream, TAG)
        squad_group_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.squad_groups_tag_block.count, tag_node, "name", "squad groups")
        for squad_group_idx in range(SCENARIO.scenario_body.squad_groups_tag_block.count):
            squad_group_element_node = None
            if XML_OUTPUT:
                squad_group_element_node = TAG.xml_doc.createElement('element')
                squad_group_element_node.setAttribute('index', str(squad_group_idx))
                squad_group_node.appendChild(squad_group_element_node)

            SCENARIO.squad_groups.append(get_squad_groups(input_stream, SCENARIO, TAG, squad_group_element_node))

def read_squads(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.squads_tag_block.count > 0:
        SCENARIO.squads_header = TAG.TagBlockHeader().read(input_stream, TAG)
        squads_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.squads_tag_block.count, tag_node, "name", "squads")
        for squads_idx in range(SCENARIO.scenario_body.squads_tag_block.count):
            squads_element_node = None
            if XML_OUTPUT:
                squads_element_node = TAG.xml_doc.createElement('element')
                squads_element_node.setAttribute('index', str(squads_idx))
                squads_node.appendChild(squads_element_node)

            SCENARIO.squads.append(get_squads(input_stream, SCENARIO, TAG, squads_element_node))

        for squad_idx, squad in enumerate(SCENARIO.squads):
            squad_element_node = None
            if XML_OUTPUT:
                squad_element_node = squads_node.childNodes[squad_idx]

            if squad.vehicle_variant_length > 0:
                squad.vehicle_variant = TAG.read_variable_string_no_terminator(input_stream, squad.vehicle_variant_length, TAG, tag_format.XMLData(squad_element_node, "vehicle variant"))

            squad.starting_locations = []
            if squad.starting_locations_tag_block.count > 0:
                squad.starting_locations_header = TAG.TagBlockHeader().read(input_stream, TAG)
                starting_location_node = tag_format.get_xml_node(XML_OUTPUT, squad.starting_locations_tag_block.count, squad_element_node, "name", "starting locations")
                for starting_location_idx in range(squad.starting_locations_tag_block.count):
                    starting_location_element_node = None
                    if XML_OUTPUT:
                        starting_location_element_node = TAG.xml_doc.createElement('element')
                        starting_location_element_node.setAttribute('index', str(starting_location_idx))
                        starting_location_node.appendChild(starting_location_element_node)

                    starting_location = SCENARIO.StartingLocation()

                    TAG.big_endian = True
                    input_stream.read(2) # Padding?
                    starting_location.name_length = TAG.read_signed_short(input_stream, TAG)
                    TAG.big_endian = False

                    starting_location.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(starting_location_element_node, "position"))
                    starting_location.reference_frame = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(starting_location_element_node, "reference frame"))
                    input_stream.read(2) # Padding?
                    starting_location.facing = TAG.read_degree_2d(input_stream, TAG, tag_format.XMLData(starting_location_element_node, "position"))
                    starting_location.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(starting_location_element_node, "flags", StartingLocationFlags))
                    starting_location.character_type_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(starting_location_element_node, "character type", None, SCENARIO.scenario_body.character_palette_tag_block.count, "scenario_character_palette_block"))
                    starting_location.initial_weapon_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(starting_location_element_node, "initial weapon", None, SCENARIO.scenario_body.weapon_palette_tag_block.count, "scenario_weapon_palette_block"))
                    starting_location.initial_secondary_weapon_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(starting_location_element_node, "initial secondary weapon", None, SCENARIO.scenario_body.weapon_palette_tag_block.count, "scenario_weapon_palette_block"))
                    input_stream.read(2) # Padding?
                    starting_location.vehicle_type_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(starting_location_element_node, "vehicle type", None, SCENARIO.scenario_body.vehicle_palette_tag_block.count, "scenario_vehicle_palette_block"))
                    starting_location.seat_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(starting_location_element_node, "seat type", SeatTypeEnum))
                    starting_location.grenade_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(starting_location_element_node, "grenade type", GrenadeTypeEnum))
                    starting_location.swarm_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(starting_location_element_node, "swarm count"))

                    TAG.big_endian = True
                    input_stream.read(2) # Padding?
                    starting_location.actor_variant_length = TAG.read_signed_short(input_stream, TAG)
                    input_stream.read(2) # Padding?
                    starting_location.vehicle_variant_length = TAG.read_signed_short(input_stream, TAG)
                    TAG.big_endian = False

                    starting_location.initial_movement_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(starting_location_element_node, "initial movement distance"))
                    starting_location.emitter_vehicle_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(starting_location_element_node, "emitter vehicle", None, SCENARIO.scenario_body.vehicles_tag_block.count, "scenario_vehicles_block"))
                    starting_location.initial_movement_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(starting_location_element_node, "grenade type", InitialMovementModeEnum))
                    starting_location.placement_script = TAG.read_string32(input_stream, TAG, tag_format.XMLData(starting_location_element_node, "placement script"))
                    input_stream.read(4) # Padding?

                    squad.starting_locations.append(starting_location)

                for starting_location_idx, starting_location in enumerate(squad.starting_locations):
                    starting_location_element_node = None
                    if XML_OUTPUT:
                        starting_location_element_node = starting_location_node.childNodes[starting_location_idx]

                    if starting_location.name_length > 0:
                        starting_location.name = TAG.read_variable_string_no_terminator(input_stream, starting_location.name_length, TAG, tag_format.XMLData(starting_location_element_node, "name"))

                    if starting_location.actor_variant_length > 0:
                        starting_location.actor_variant = TAG.read_variable_string_no_terminator(input_stream, starting_location.actor_variant_length, TAG, tag_format.XMLData(starting_location_element_node, "actor variant"))

                    if starting_location.vehicle_variant_length > 0:
                        starting_location.vehicle_variant = TAG.read_variable_string_no_terminator(input_stream, starting_location.vehicle_variant_length, TAG, tag_format.XMLData(starting_location_element_node, "vehicle variant"))

def read_zones(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.zones_tag_block.count > 0:
        SCENARIO.zones_header = TAG.TagBlockHeader().read(input_stream, TAG)
        zone_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.zones_tag_block.count, tag_node, "name", "zones")
        for zone_idx in range(SCENARIO.scenario_body.zones_tag_block.count):
            zone_element_node = None
            if XML_OUTPUT:
                zone_element_node = TAG.xml_doc.createElement('element')
                zone_element_node.setAttribute('index', str(zone_idx))
                zone_node.appendChild(zone_element_node)

            SCENARIO.zones.append(get_zones(input_stream, SCENARIO, TAG, zone_element_node))

        for zone_idx, zone in enumerate(SCENARIO.zones):
            zone_element_node = None
            if XML_OUTPUT:
                zone_element_node = zone_node.childNodes[zone_idx]

            zone.firing_positions = []
            zone.areas = []
            if zone.firing_positions_tag_block.count > 0:
                zone.starting_locations_header = TAG.TagBlockHeader().read(input_stream, TAG)
                firing_position_node = tag_format.get_xml_node(XML_OUTPUT, zone.firing_positions_tag_block.count, zone_element_node, "name", "firing positions")
                for firing_position_idx in range(zone.firing_positions_tag_block.count):
                    firing_position_element_node = None
                    if XML_OUTPUT:
                        firing_position_element_node = TAG.xml_doc.createElement('element')
                        firing_position_element_node.setAttribute('index', str(firing_position_idx))
                        firing_position_node.appendChild(firing_position_element_node)

                    firing_position = SCENARIO.FiringPosition()

                    firing_position.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(firing_position_element_node, "position"))
                    firing_position.reference_frame = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(firing_position_element_node, "reference frame"))
                    firing_position.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(firing_position_element_node, "flags", FiringPointFlags))
                    firing_position.area_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(firing_position_element_node, "area index", None, zone.areas_tag_block.count, "scenario_areas_block"))
                    firing_position.cluster_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(firing_position_element_node, "cluster index"))
                    input_stream.read(4) # Padding?
                    firing_position.normal = TAG.read_degree_2d(input_stream, TAG, tag_format.XMLData(firing_position_element_node, "normal"))

                    zone.firing_positions.append(firing_position)

            if zone.areas_tag_block.count > 0:
                zone.areas_header = TAG.TagBlockHeader().read(input_stream, TAG)
                area_node = tag_format.get_xml_node(XML_OUTPUT, zone.areas_tag_block.count, zone_element_node, "name", "areas")
                for area_idx in range(zone.areas_tag_block.count):
                    area_element_node = None
                    if XML_OUTPUT:
                        area_element_node = TAG.xml_doc.createElement('element')
                        area_element_node.setAttribute('index', str(area_idx))
                        area_node.appendChild(area_element_node)

                    area = SCENARIO.Area()

                    area.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(area_element_node, "name"))
                    area.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(area_element_node, "flags", AreaFlags))
                    input_stream.read(22) # Padding?
                    area.runtime_starting_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(area_element_node, "runtime starting index"))
                    area.runtime_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(area_element_node, "runtime count"))
                    input_stream.read(64) # Padding?
                    area.manual_reference_frame = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(area_element_node, "manual reference frame"))
                    input_stream.read(2) # Padding?
                    area.flight_hints_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(area_element_node, "flight hints"))

                    zone.areas.append(area)

                for area_idx, area in enumerate(zone.areas):
                    area_element_node = None
                    if XML_OUTPUT:
                        area_element_node = area_node.childNodes[area_idx]

                    area.flight_hints = []
                    if area.flight_hints_tag_block.count > 0:
                        area.flight_hints_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        flight_hints_node = tag_format.get_xml_node(XML_OUTPUT, area.flight_hints_tag_block.count, area_element_node, "name", "flight hints")
                        for flight_hint_idx in range(area.flight_hints_tag_block.count):
                            flight_hint_element_node = None
                            if XML_OUTPUT:
                                flight_hint_element_node = TAG.xml_doc.createElement('element')
                                flight_hint_element_node.setAttribute('index', str(flight_hint_idx))
                                flight_hints_node.appendChild(flight_hint_element_node)

                            flight_hint = SCENARIO.FlightHint()

                            flight_hint.flight_hint_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(flight_hint_element_node, "flight hint index"))
                            flight_hint.point_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(flight_hint_element_node, "point index"))

                            area.flight_hints.append(flight_hint)

def read_mission_scenes(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.mission_scenes_tag_block.count > 0:
        SCENARIO.mission_scenes_header = TAG.TagBlockHeader().read(input_stream, TAG)
        mission_scene_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.mission_scenes_tag_block.count, tag_node, "name", "mission scenes")
        for mission_scene_idx in range(SCENARIO.scenario_body.mission_scenes_tag_block.count):
            mission_scene_element_node = None
            if XML_OUTPUT:
                mission_scene_element_node = TAG.xml_doc.createElement('element')
                mission_scene_element_node.setAttribute('index', str(mission_scene_idx))
                mission_scene_node.appendChild(mission_scene_element_node)

            SCENARIO.mission_scenes.append(get_mission_scenes(input_stream, SCENARIO, TAG, mission_scene_element_node))

        for mission_scene_idx, mission_scene in enumerate(SCENARIO.mission_scenes):
            mission_scene_element_node = None
            if XML_OUTPUT:
                mission_scene_element_node = mission_scene_node.childNodes[mission_scene_idx]

            if mission_scene.name_length > 0:
                mission_scene.name = TAG.read_variable_string_no_terminator(input_stream, mission_scene.name_length, TAG, tag_format.XMLData(mission_scene_element_node, "name"))

            mission_scene.trigger_conditions = []
            mission_scene.roles = []
            if mission_scene.trigger_conditions_tag_block.count > 0:
                mission_scene.trigger_conditions_header = TAG.TagBlockHeader().read(input_stream, TAG)
                trigger_conditions_node = tag_format.get_xml_node(XML_OUTPUT, mission_scene.trigger_conditions_tag_block.count, mission_scene_element_node, "name", "trigger conditions")
                for trigger_condition_idx in range(mission_scene.trigger_conditions_tag_block.count):
                    trigger_condition_element_node = None
                    if XML_OUTPUT:
                        trigger_condition_element_node = TAG.xml_doc.createElement('element')
                        trigger_condition_element_node.setAttribute('index', str(trigger_condition_idx))
                        trigger_conditions_node.appendChild(trigger_condition_element_node)

                    trigger_condition = SCENARIO.TriggerCondition()

                    trigger_condition.combination_rule = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(trigger_condition_element_node, "combination rule", CombinationRuleEnum))
                    input_stream.read(2) # Padding?
                    trigger_condition.triggers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(trigger_condition_element_node, "triggers"))

                    mission_scene.trigger_conditions.append(trigger_condition)

                for trigger_condition_idx, trigger_condition in enumerate(mission_scene.trigger_conditions):
                    trigger_condition_element_node = None
                    if XML_OUTPUT:
                        trigger_condition_element_node = trigger_conditions_node.childNodes[trigger_condition_idx]

                    trigger_condition.triggers = []
                    if trigger_condition.triggers_tag_block.count > 0:
                        trigger_condition.triggers_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        trigger_node = tag_format.get_xml_node(XML_OUTPUT, trigger_condition.triggers_tag_block.count, trigger_condition_element_node, "name", "triggers")
                        for trigger_idx in range(trigger_condition.triggers_tag_block.count):
                            trigger_element_node = None
                            if XML_OUTPUT:
                                trigger_element_node = TAG.xml_doc.createElement('element')
                                trigger_element_node.setAttribute('index', str(trigger_idx))
                                trigger_node.appendChild(trigger_element_node)

                            trigger = SCENARIO.Trigger()

                            trigger.trigger_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(trigger_element_node, "trigger flags", TriggerFlags))
                            trigger.trigger = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(trigger_element_node, "trigger", None, SCENARIO.scenario_body.triggers_tag_block.count, "scenario_triggers_block"))
                            input_stream.read(2) # Padding?

                            trigger_condition.triggers.append(trigger)

            if mission_scene.roles_tag_block.count > 0:
                mission_scene.roles_header = TAG.TagBlockHeader().read(input_stream, TAG)
                role_node = tag_format.get_xml_node(XML_OUTPUT, mission_scene.roles_tag_block.count, mission_scene_element_node, "name", "roles")
                for role_idx in range(mission_scene.roles_tag_block.count):
                    role_element_node = None
                    if XML_OUTPUT:
                        role_element_node = TAG.xml_doc.createElement('element')
                        role_element_node.setAttribute('index', str(role_idx))
                        role_node.appendChild(role_element_node)

                    role = SCENARIO.Role()

                    TAG.big_endian = True
                    input_stream.read(2) # Padding?
                    role.name_length = TAG.read_signed_short(input_stream, TAG)
                    TAG.big_endian = False

                    role.group = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(role_element_node, "group", GroupEnum))
                    input_stream.read(2) # Padding?
                    role.role_variants_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(role_element_node, "role variants"))

                    mission_scene.roles.append(role)

                for role_idx, role in enumerate(mission_scene.roles):
                    role_element_node = None
                    if XML_OUTPUT:
                        role_element_node = role_node.childNodes[role_idx]

                    if role.name_length > 0:
                        role.name = TAG.read_variable_string_no_terminator(input_stream, role.name_length, TAG, tag_format.XMLData(role_element_node, "name"))

                    role.role_variants = []
                    if role.role_variants_tag_block.count > 0:
                        role.role_variants_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        role_variant_node = tag_format.get_xml_node(XML_OUTPUT, role.role_variants_tag_block.count, role_element_node, "name", "role variants")
                        for role_variant_idx in range(role.role_variants_tag_block.count):
                            role_variant_element_node = None
                            if XML_OUTPUT:
                                role_variant_element_node = TAG.xml_doc.createElement('element')
                                role_variant_element_node.setAttribute('index', str(role_variant_idx))
                                role_variant_node.appendChild(role_variant_element_node)

                            role_variant = SCENARIO.RoleVariant()

                            TAG.big_endian = True
                            input_stream.read(2) # Padding?
                            role_variant.name_length = TAG.read_signed_short(input_stream, TAG)
                            TAG.big_endian = False

                            role.role_variants.append(role_variant)

                        for role_variant_idx, role_variant in enumerate(role.role_variants):
                            role_variant_element_node = None
                            if XML_OUTPUT:
                                role_variant_element_node = role_variant_node.childNodes[role_variant_idx]

                            if role_variant.name_length > 0:
                                role_variant.name = TAG.read_variable_string_no_terminator(input_stream, role_variant.name_length, TAG, tag_format.XMLData(role_variant_element_node, "name"))

def read_character_palette(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.character_palette_tag_block.count > 0:
        SCENARIO.character_palette_header = TAG.TagBlockHeader().read(input_stream, TAG)
        character_palette_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.character_palette_tag_block.count, tag_node, "name", "character palette")
        for character_palette_idx in range(SCENARIO.scenario_body.character_palette_tag_block.count):
            character_palette_element_node = None
            if XML_OUTPUT:
                character_palette_element_node = TAG.xml_doc.createElement('element')
                character_palette_element_node.setAttribute('index', str(character_palette_idx))
                character_palette_node.appendChild(character_palette_element_node)

            SCENARIO.character_palette.append(get_palette(input_stream, TAG, character_palette_element_node, 0))

        for character_palette_idx, character_palette in enumerate(SCENARIO.character_palette):
            character_palette_name_length = character_palette.name_length
            if character_palette_name_length > 0:
                character_palette.name = TAG.read_variable_string(input_stream, character_palette_name_length, TAG)

            if XML_OUTPUT:
                character_palette_element_node = character_palette_node.childNodes[character_palette_idx]
                character_palette_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, character_palette_element_node, "name", "name")
                character_palette.append_xml_attributes(character_palette_tag_ref_node)

def get_sectors(input_stream, SCENARIO, TAG, node_element):
    sector = SCENARIO.Sector()

    sector.pathfinding_sector_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "pathfinding sector flags", PathfindingSectorFlags))
    sector.hint_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "hint index"))
    sector.first_link = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "first link"))

    return sector

def get_links(input_stream, SCENARIO, TAG, node_element):
    link = SCENARIO.Link()

    link.vertex_1 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "vertex 1"))
    link.vertex_2 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "vertex 2"))
    link.link_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "link flags", LinkFlags))
    link.hint_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "hint index"))
    link.forward_link = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "forward link"))
    link.reverse_link = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "reverse link"))
    link.left_sector = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "left sector"))
    link.right_sector = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "right sector"))

    return link

def get_bsp2d_nodes(input_stream, SCENARIO, TAG, node_element):
    bsp2d_node = SCENARIO.Bsp2DNode()

    bsp2d_node.plane = TAG.Plane2D().read(input_stream, TAG, tag_format.XMLData(node_element, "plane"))
    bsp2d_node.left_child = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "left child"))
    bsp2d_node.right_child = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "right child"))

    return bsp2d_node

def get_object_ref(input_stream, SCENARIO, TAG, node_element):
    object_ref = SCENARIO.ObjectRef()

    object_ref.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", ObjectRefFlags))
    object_ref.first_sector = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "first sector"))
    object_ref.last_sector = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "last sector"))
    object_ref.bsps_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "bsps"))
    object_ref.nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "nodes"))

    return object_ref

def get_object_ref_bsp(input_stream, SCENARIO, TAG, node_element):
    bsp = SCENARIO.BSP()

    bsp.bsp_reference = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "bsp reference"))
    bsp.first_sector = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "first sector"))
    bsp.last_sector = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "last sector"))
    bsp.node_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "node index"))
    input_stream.read(2) # Padding?

    return bsp

def get_object_ref_nodes(input_stream, SCENARIO, TAG, node_element):
    node = SCENARIO.Node()

    node.reference_frame_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "reference frame index"))
    node.projection_axis = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(node_element, "projection axis"))
    node.projection_sign = TAG.read_flag_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "projection sign", NodeFlags))

    return node

def get_pathfinding_hints(input_stream, SCENARIO, TAG, node_element):
    pathfinding_hint = SCENARIO.PathfindingHint()

    pathfinding_hint.hint_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "hint type", HintTypeEnum))
    pathfinding_hint.next_hint_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "next hint index"))
    pathfinding_hint.hint_data_0 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "hint data 0"))
    pathfinding_hint.hint_data_1 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "hint data 1"))
    pathfinding_hint.hint_data_2 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "hint data 2"))
    pathfinding_hint.hint_data_3 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "hint data 3"))
    pathfinding_hint.hint_data_4 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "hint data 4"))
    pathfinding_hint.hint_data_5 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "hint data 5"))
    pathfinding_hint.hint_data_6 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "hint data 6"))
    pathfinding_hint.hint_data_7 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "hint data 7"))

    return pathfinding_hint

def get_user_placed_hints(input_stream, SCENARIO, TAG, node_element):
    user_placed_hint = SCENARIO.UserPlacedHint()

    user_placed_hint.point_geometry_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "point geometry"))
    user_placed_hint.ray_geometry_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "ray geometry"))
    user_placed_hint.line_segment_geometry_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "line segment geometry"))
    user_placed_hint.parallelogram_geometry_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "parallelogram geometry"))
    user_placed_hint.polygon_geometry_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "polygon geometry"))
    user_placed_hint.jump_hints_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "jump hints"))
    user_placed_hint.climb_hints_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "climb hints"))
    user_placed_hint.well_hints_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "well hints"))
    user_placed_hint.flight_hints_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "flight hints"))

    return user_placed_hint

def get_point_geometry(input_stream, SCENARIO, TAG, node_element):
    point_geometry = SCENARIO.PointGeometry()

    point_geometry.point = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "point"))
    point_geometry.reference_frame = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "reference frame"))
    input_stream.read(2) # Padding?

    return point_geometry

def get_ray_geometry(input_stream, SCENARIO, TAG, node_element):
    ray_geometry = SCENARIO.RayGeometry()

    ray_geometry.point = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "point"))
    ray_geometry.reference_frame = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "reference frame"))
    input_stream.read(2) # Padding?
    ray_geometry.vector = TAG.read_vector(input_stream, TAG, tag_format.XMLData(node_element, "vector"))

    return ray_geometry

def get_line_segment_geometry(input_stream, SCENARIO, TAG, node_element):
    line_segment_geometry = SCENARIO.LineSegmentGeometry()

    line_segment_geometry.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "flags", GeometryFlags))
    input_stream.read(2) # Padding?
    line_segment_geometry.point_0 = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "point 0"))
    line_segment_geometry.reference_frame_0 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "reference frame"))
    input_stream.read(2) # Padding?
    line_segment_geometry.point_1 = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "point 1"))
    line_segment_geometry.reference_frame_1 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "reference frame"))
    input_stream.read(2) # Padding?

    return line_segment_geometry

def get_parallelogram_geometry(input_stream, SCENARIO, TAG, node_element):
    parallelogram_geometry = SCENARIO.ParallelogramGeometry()

    parallelogram_geometry.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "flags", GeometryFlags))
    input_stream.read(2) # Padding?
    parallelogram_geometry.point_0 = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "point 0"))
    parallelogram_geometry.reference_frame_0 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "reference frame"))
    input_stream.read(2) # Padding?
    parallelogram_geometry.point_1 = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "point 1"))
    parallelogram_geometry.reference_frame_1 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "reference frame"))
    input_stream.read(2) # Padding?
    parallelogram_geometry.point_2 = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "point 2"))
    parallelogram_geometry.reference_frame_2 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "reference frame"))
    input_stream.read(2) # Padding?
    parallelogram_geometry.point_3 = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "point 3"))
    parallelogram_geometry.reference_frame_3 = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "reference frame"))
    input_stream.read(2) # Padding?

    return parallelogram_geometry

def get_polygon_geometry(input_stream, SCENARIO, TAG, node_element):
    polygon_geometry = SCENARIO.Hint()

    polygon_geometry.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "flags", GeometryFlags))
    input_stream.read(2) # Padding?
    polygon_geometry.points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "points"))

    return polygon_geometry

def read_ai_pathfinding_data(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.ai_pathfinding_data_tag_block.count > 0:
        SCENARIO.ai_pathfinding_data_header = TAG.TagBlockHeader().read(input_stream, TAG)
        ai_pathfinding_data_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.ai_pathfinding_data_tag_block.count, tag_node, "name", "ai pathfinding data")
        for ai_pathfinding_data_idx in range(SCENARIO.scenario_body.ai_pathfinding_data_tag_block.count):
            ai_pathfinding_data_element_node = None
            if XML_OUTPUT:
                ai_pathfinding_data_element_node = TAG.xml_doc.createElement('element')
                ai_pathfinding_data_element_node.setAttribute('index', str(ai_pathfinding_data_idx))
                ai_pathfinding_data_node.appendChild(ai_pathfinding_data_element_node)

            SCENARIO.ai_pathfinding_data.append(get_ai_pathfinding_data(input_stream, SCENARIO, TAG, ai_pathfinding_data_element_node))

        for ai_pathfinding_data_idx, ai_pathfinding_data in enumerate(SCENARIO.ai_pathfinding_data):
            ai_pathfinding_data_element_node = None
            if XML_OUTPUT:
                ai_pathfinding_data_element_node = ai_pathfinding_data_node.childNodes[ai_pathfinding_data_idx]

            ai_pathfinding_data.sectors = []
            ai_pathfinding_data.links = []
            ai_pathfinding_data.refs = []
            ai_pathfinding_data.bsp2d_nodes = []
            ai_pathfinding_data.surface_flags = []
            ai_pathfinding_data.vertices = []
            ai_pathfinding_data.object_refs = []
            ai_pathfinding_data.pathfinding_hints = []
            ai_pathfinding_data.instanced_geometry_refs = []
            ai_pathfinding_data.user_placed_hints = []
            if ai_pathfinding_data.sectors_tag_block.count > 0:
                ai_pathfinding_data.sectors_header = TAG.TagBlockHeader().read(input_stream, TAG)
                sector_node = tag_format.get_xml_node(XML_OUTPUT, ai_pathfinding_data.sectors_tag_block.count, ai_pathfinding_data_element_node, "name", "sectors")
                for sector_idx in range(ai_pathfinding_data.sectors_tag_block.count):
                    sector_element_node = None
                    if XML_OUTPUT:
                        sector_element_node = TAG.xml_doc.createElement('element')
                        sector_element_node.setAttribute('index', str(sector_idx))
                        sector_node.appendChild(sector_element_node)

                    ai_pathfinding_data.sectors.append(get_sectors(input_stream, SCENARIO, TAG, sector_element_node))

            if ai_pathfinding_data.links_tag_block.count > 0:
                ai_pathfinding_data.links_header = TAG.TagBlockHeader().read(input_stream, TAG)
                link_node = tag_format.get_xml_node(XML_OUTPUT, ai_pathfinding_data.links_tag_block.count, ai_pathfinding_data_element_node, "name", "links")
                for link_idx in range(ai_pathfinding_data.links_tag_block.count):
                    link_element_node = None
                    if XML_OUTPUT:
                        link_element_node = TAG.xml_doc.createElement('element')
                        link_element_node.setAttribute('index', str(link_idx))
                        link_node.appendChild(link_element_node)

                    ai_pathfinding_data.links.append(get_links(input_stream, SCENARIO, TAG, link_element_node))

            if ai_pathfinding_data.refs_tag_block.count > 0:
                ai_pathfinding_data.refs_header = TAG.TagBlockHeader().read(input_stream, TAG)
                ref_node = tag_format.get_xml_node(XML_OUTPUT, ai_pathfinding_data.refs_tag_block.count, ai_pathfinding_data_element_node, "name", "refs")
                for ref_idx in range(ai_pathfinding_data.refs_tag_block.count):
                    ref_element_node = None
                    if XML_OUTPUT:
                        ref_element_node = TAG.xml_doc.createElement('element')
                        ref_element_node.setAttribute('index', str(ref_idx))
                        ref_node.appendChild(ref_element_node)

                    ai_pathfinding_data.refs.append(TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(ref_element_node, "node ref or sector ref")))

            if ai_pathfinding_data.bsp2d_nodes_tag_block.count > 0:
                ai_pathfinding_data.bsp2d_nodes_header = TAG.TagBlockHeader().read(input_stream, TAG)
                bsp2d_node = tag_format.get_xml_node(XML_OUTPUT, ai_pathfinding_data.bsp2d_nodes_tag_block.count, ai_pathfinding_data_element_node, "name", "bsp2d nodes")
                for bsp2d_idx in range(ai_pathfinding_data.bsp2d_nodes_tag_block.count):
                    bsp2d_element_node = None
                    if XML_OUTPUT:
                        bsp2d_element_node = TAG.xml_doc.createElement('element')
                        bsp2d_element_node.setAttribute('index', str(bsp2d_idx))
                        bsp2d_node.appendChild(bsp2d_element_node)

                    ai_pathfinding_data.bsp2d_nodes.append(get_bsp2d_nodes(input_stream, SCENARIO, TAG, bsp2d_element_node))

            if ai_pathfinding_data.surface_flags_tag_block.count > 0:
                ai_pathfinding_data.surface_flags_header = TAG.TagBlockHeader().read(input_stream, TAG)
                surface_flags_node = tag_format.get_xml_node(XML_OUTPUT, ai_pathfinding_data.surface_flags_tag_block.count, ai_pathfinding_data_element_node, "name", "surface flags")
                for surface_flags_idx in range(ai_pathfinding_data.surface_flags_tag_block.count):
                    surface_flags_element_node = None
                    if XML_OUTPUT:
                        surface_flags_element_node = TAG.xml_doc.createElement('element')
                        surface_flags_element_node.setAttribute('index', str(surface_flags_idx))
                        surface_flags_node.appendChild(surface_flags_element_node)

                    ai_pathfinding_data.surface_flags.append(TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(surface_flags_element_node, "flags")))

            if ai_pathfinding_data.vertices_tag_block.count > 0:
                ai_pathfinding_data.vertices_header = TAG.TagBlockHeader().read(input_stream, TAG)
                vertices_node = tag_format.get_xml_node(XML_OUTPUT, ai_pathfinding_data.vertices_tag_block.count, ai_pathfinding_data_element_node, "name", "vertices")
                for vertex_idx in range(ai_pathfinding_data.vertices_tag_block.count):
                    vertex_element_node = None
                    if XML_OUTPUT:
                        vertex_element_node = TAG.xml_doc.createElement('element')
                        vertex_element_node.setAttribute('index', str(vertex_idx))
                        vertices_node.appendChild(vertex_element_node)

                    ai_pathfinding_data.vertices.append(TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(vertex_element_node, "position")))

            if ai_pathfinding_data.object_refs_tag_block.count > 0:
                ai_pathfinding_data.object_refs_header = TAG.TagBlockHeader().read(input_stream, TAG)
                object_refs_node = tag_format.get_xml_node(XML_OUTPUT, ai_pathfinding_data.object_refs_tag_block.count, ai_pathfinding_data_element_node, "name", "object refs")
                for object_ref_idx in range(ai_pathfinding_data.object_refs_tag_block.count):
                    object_ref_element_node = None
                    if XML_OUTPUT:
                        object_ref_element_node = TAG.xml_doc.createElement('element')
                        object_ref_element_node.setAttribute('index', str(object_ref_idx))
                        object_refs_node.appendChild(object_ref_element_node)

                    ai_pathfinding_data.object_refs.append(get_object_ref(input_stream, SCENARIO, TAG, object_ref_element_node))

                for object_ref_idx, object_ref in enumerate(ai_pathfinding_data.object_refs):
                    object_ref_element_node = None
                    if XML_OUTPUT:
                        object_ref_element_node = object_refs_node.childNodes[object_ref_idx]

                    object_ref.bsps = []
                    object_ref.nodes = []
                    if object_ref.bsps_tag_block.count > 0:
                        object_ref.bsps_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        bsp_node = tag_format.get_xml_node(XML_OUTPUT, object_ref.bsps_tag_block.count, object_ref_element_node, "name", "bsps")
                        for bsp_idx in range(object_ref.bsps_tag_block.count):
                            bsp_element_node = None
                            if XML_OUTPUT:
                                bsp_element_node = TAG.xml_doc.createElement('element')
                                bsp_element_node.setAttribute('index', str(bsp_idx))
                                bsp_node.appendChild(bsp_element_node)

                            object_ref.bsps.append(get_object_ref_bsp(input_stream, SCENARIO, TAG, bsp_element_node))

                    if object_ref.nodes_tag_block.count > 0:
                        object_ref.nodes_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        node_node = tag_format.get_xml_node(XML_OUTPUT, object_ref.nodes_tag_block.count, object_ref_element_node, "name", "nodes")
                        for node_idx in range(object_ref.nodes_tag_block.count):
                            node_element_node = None
                            if XML_OUTPUT:
                                node_element_node = TAG.xml_doc.createElement('element')
                                node_element_node.setAttribute('index', str(node_idx))
                                node_node.appendChild(node_element_node)

                            object_ref.nodes.append(get_object_ref_nodes(input_stream, SCENARIO, TAG, node_element_node))

            if ai_pathfinding_data.pathfinding_hints_tag_block.count > 0:
                ai_pathfinding_data.pathfinding_hints_header = TAG.TagBlockHeader().read(input_stream, TAG)
                pathfinding_hint_node = tag_format.get_xml_node(XML_OUTPUT, ai_pathfinding_data.pathfinding_hints_tag_block.count, ai_pathfinding_data_element_node, "name", "pathfinding hints")
                for pathfinding_hint_idx in range(ai_pathfinding_data.pathfinding_hints_tag_block.count):
                    pathfinding_hint_element_node = None
                    if XML_OUTPUT:
                        pathfinding_hint_element_node = TAG.xml_doc.createElement('element')
                        pathfinding_hint_element_node.setAttribute('index', str(pathfinding_hint_idx))
                        pathfinding_hint_node.appendChild(pathfinding_hint_element_node)

                    ai_pathfinding_data.pathfinding_hints.append(get_pathfinding_hints(input_stream, SCENARIO, TAG, pathfinding_hint_element_node))

            if ai_pathfinding_data.instanced_geometry_refs_tag_block.count > 0:
                ai_pathfinding_data.instanced_geometry_refs_header = TAG.TagBlockHeader().read(input_stream, TAG)
                instanced_geometry_ref_node = tag_format.get_xml_node(XML_OUTPUT, ai_pathfinding_data.instanced_geometry_refs_tag_block.count, ai_pathfinding_data_element_node, "name", "instanced geometry refs")
                for instanced_geometry_ref_idx in range(ai_pathfinding_data.instanced_geometry_refs_tag_block.count):
                    instanced_geometry_ref_element_node = None
                    if XML_OUTPUT:
                        instanced_geometry_ref_element_node = TAG.xml_doc.createElement('element')
                        instanced_geometry_ref_element_node.setAttribute('index', str(instanced_geometry_ref_idx))
                        instanced_geometry_ref_node.appendChild(instanced_geometry_ref_element_node)

                    ai_pathfinding_data.instanced_geometry_refs.append(TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(instanced_geometry_ref_element_node, "pathfinding_object_index")))
                    input_stream.read(2) # Padding?

            if ai_pathfinding_data.user_placed_hints_tag_block.count > 0:
                ai_pathfinding_data.user_placed_hints_header = TAG.TagBlockHeader().read(input_stream, TAG)
                user_placed_hint_node = tag_format.get_xml_node(XML_OUTPUT, ai_pathfinding_data.user_placed_hints_tag_block.count, ai_pathfinding_data_element_node, "name", "user placed hints")
                for user_placed_hint_idx in range(ai_pathfinding_data.user_placed_hints_tag_block.count):
                    user_placed_hint_element_node = None
                    if XML_OUTPUT:
                        user_placed_hint_element_node = TAG.xml_doc.createElement('element')
                        user_placed_hint_element_node.setAttribute('index', str(user_placed_hint_idx))
                        user_placed_hint_node.appendChild(user_placed_hint_element_node)

                    ai_pathfinding_data.user_placed_hints.append(get_user_placed_hints(input_stream, SCENARIO, TAG, user_placed_hint_element_node))

                for user_placed_hint_idx, user_placed_hint in enumerate(ai_pathfinding_data.user_placed_hints):
                    user_placed_hint_element_node = None
                    if XML_OUTPUT:
                        user_placed_hint_element_node = user_placed_hint_node.childNodes[user_placed_hint_idx]

                    user_placed_hint.point_geometry = []
                    user_placed_hint.ray_geometry = []
                    user_placed_hint.line_segment_geometry = []
                    user_placed_hint.parallelogram_geometry = []
                    user_placed_hint.polygon_geometry = []
                    user_placed_hint.jump_hints = []
                    user_placed_hint.climb_hints = []
                    user_placed_hint.well_hints = []
                    user_placed_hint.flight_hints = []
                    if user_placed_hint.point_geometry_tag_block.count > 0:
                        user_placed_hint.point_geometry_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        point_geometry_node = tag_format.get_xml_node(XML_OUTPUT, user_placed_hint.point_geometry_tag_block.count, user_placed_hint_element_node, "name", "point geometry")
                        for point_geometry_idx in range(user_placed_hint.point_geometry_tag_block.count):
                            point_geometry_element_node = None
                            if XML_OUTPUT:
                                point_geometry_element_node = TAG.xml_doc.createElement('element')
                                point_geometry_element_node.setAttribute('index', str(point_geometry_idx))
                                point_geometry_node.appendChild(point_geometry_element_node)

                            user_placed_hint.point_geometry.append(get_point_geometry(input_stream, SCENARIO, TAG, point_geometry_element_node))

                    if user_placed_hint.ray_geometry_tag_block.count > 0:
                        user_placed_hint.ray_geometry_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        ray_geometry_node = tag_format.get_xml_node(XML_OUTPUT, user_placed_hint.ray_geometry_tag_block.count, user_placed_hint_element_node, "name", "ray geometry")
                        for ray_geometry_idx in range(user_placed_hint.ray_geometry_tag_block.count):
                            ray_geometry_element_node = None
                            if XML_OUTPUT:
                                ray_geometry_element_node = TAG.xml_doc.createElement('element')
                                ray_geometry_element_node.setAttribute('index', str(ray_geometry_idx))
                                ray_geometry_node.appendChild(ray_geometry_element_node)

                            user_placed_hint.ray_geometry.append(get_ray_geometry(input_stream, SCENARIO, TAG, ray_geometry_element_node))

                    if user_placed_hint.line_segment_geometry_tag_block.count > 0:
                        user_placed_hint.line_segment_geometry_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        line_segment_geometry_node = tag_format.get_xml_node(XML_OUTPUT, user_placed_hint.line_segment_geometry_tag_block.count, user_placed_hint_element_node, "name", "line segment geometry")
                        for line_segment_geometry_idx in range(user_placed_hint.line_segment_geometry_tag_block.count):
                            line_segment_geometry_element_node = None
                            if XML_OUTPUT:
                                line_segment_geometry_element_node = TAG.xml_doc.createElement('element')
                                line_segment_geometry_element_node.setAttribute('index', str(line_segment_geometry_idx))
                                line_segment_geometry_node.appendChild(line_segment_geometry_element_node)

                            user_placed_hint.line_segment_geometry.append(get_line_segment_geometry(input_stream, SCENARIO, TAG, line_segment_geometry_element_node))

                    if user_placed_hint.parallelogram_geometry_tag_block.count > 0:
                        user_placed_hint.parallelogram_geometry_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        parallelogram_geometry_node = tag_format.get_xml_node(XML_OUTPUT, user_placed_hint.parallelogram_geometry_tag_block.count, user_placed_hint_element_node, "name", "parallelogram geometry")
                        for parallelogram_geometry_idx in range(user_placed_hint.parallelogram_geometry_tag_block.count):
                            parallelogram_geometry_element_node = None
                            if XML_OUTPUT:
                                parallelogram_geometry_element_node = TAG.xml_doc.createElement('element')
                                parallelogram_geometry_element_node.setAttribute('index', str(parallelogram_geometry_idx))
                                parallelogram_geometry_node.appendChild(parallelogram_geometry_element_node)

                            user_placed_hint.parallelogram_geometry.append(get_parallelogram_geometry(input_stream, SCENARIO, TAG, parallelogram_geometry_element_node))

                    if user_placed_hint.polygon_geometry_tag_block.count > 0:
                        user_placed_hint.polygon_geometry_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        polygon_geometry_node = tag_format.get_xml_node(XML_OUTPUT, user_placed_hint.polygon_geometry_tag_block.count, user_placed_hint_element_node, "name", "polygon geometry")
                        for polygon_geometry_idx in range(user_placed_hint.polygon_geometry_tag_block.count):
                            polygon_geometry_element_node = None
                            if XML_OUTPUT:
                                polygon_geometry_element_node = TAG.xml_doc.createElement('element')
                                polygon_geometry_element_node.setAttribute('index', str(polygon_geometry_idx))
                                polygon_geometry_node.appendChild(polygon_geometry_element_node)

                            user_placed_hint.polygon_geometry.append(get_polygon_geometry(input_stream, SCENARIO, TAG, polygon_geometry_element_node))

                        for polygon_geometry_idx, polygon_geometry in enumerate(user_placed_hint.polygon_geometry):
                            polygon_geometry_element_node = None
                            if XML_OUTPUT:
                                polygon_geometry_element_node = polygon_geometry_node.childNodes[polygon_geometry_idx]

                            polygon_geometry.points = []
                            if polygon_geometry.points_tag_block.count > 0:
                                polygon_geometry.points_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                point_node = tag_format.get_xml_node(XML_OUTPUT, polygon_geometry.points_tag_block.count, polygon_geometry_element_node, "name", "points")
                                for point_idx in range(polygon_geometry.points_tag_block.count):
                                    point_element_node = None
                                    if XML_OUTPUT:
                                        point_element_node = TAG.xml_doc.createElement('element')
                                        point_element_node.setAttribute('index', str(point_idx))
                                        point_node.appendChild(point_element_node)

                                    point = SCENARIO.PointGeometry()

                                    point.point = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(point_element_node, "point"))
                                    point.reference_frame = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(point_element_node, "reference frame"))
                                    input_stream.read(2) # Padding?

                                    polygon_geometry.points.append(point)

                    if user_placed_hint.jump_hints_tag_block.count > 0:
                        user_placed_hint.jump_hints_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        jump_hint_node = tag_format.get_xml_node(XML_OUTPUT, user_placed_hint.jump_hints_tag_block.count, user_placed_hint_element_node, "name", "jump hints")
                        for jump_hint_idx in range(user_placed_hint.jump_hints_tag_block.count):
                            jump_hint_element_node = None
                            if XML_OUTPUT:
                                jump_hint_element_node = TAG.xml_doc.createElement('element')
                                jump_hint_element_node.setAttribute('index', str(jump_hint_idx))
                                jump_hint_node.appendChild(jump_hint_element_node)

                            jump_hint = SCENARIO.JumpHint()

                            jump_hint.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(jump_hint_element_node, "flags", GeometryFlags))
                            jump_hint.geometry_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(jump_hint_element_node, "geometry index", None, user_placed_hint.parallelogram_geometry_tag_block.count, "parallelogram_geometry_block"))
                            jump_hint.force_jump_height = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(jump_hint_element_node, "function", ForceJumpHeightEnum))
                            jump_hint.control_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(jump_hint_element_node, "flags", JumpControlFlags))

                            user_placed_hint.jump_hints.append(jump_hint)

                    if user_placed_hint.climb_hints_tag_block.count > 0:
                        user_placed_hint.climb_hints_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        climb_hint_node = tag_format.get_xml_node(XML_OUTPUT, user_placed_hint.climb_hints_tag_block.count, user_placed_hint_element_node, "name", "climb hints")
                        for climb_hint_node_idx in range(user_placed_hint.climb_hints_tag_block.count):
                            climb_hint_node_element_node = None
                            if XML_OUTPUT:
                                climb_hint_node_element_node = TAG.xml_doc.createElement('element')
                                climb_hint_node_element_node.setAttribute('index', str(climb_hint_node_idx))
                                climb_hint_node.appendChild(climb_hint_node_element_node)

                            climb_hint = SCENARIO.ClimbHint()

                            climb_hint.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(climb_hint_node_element_node, "flags", GeometryFlags))
                            climb_hint.geometry_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(climb_hint_node_element_node, "geometry index", None, user_placed_hint.line_segment_geometry_tag_block.count, "line_segment_geometry_block"))

                            user_placed_hint.climb_hints.append(climb_hint)

                    if user_placed_hint.well_hints_tag_block.count > 0:
                        user_placed_hint.well_hints_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        well_hint_node = tag_format.get_xml_node(XML_OUTPUT, user_placed_hint.well_hints_tag_block.count, user_placed_hint_element_node, "name", "well hints")
                        for well_hint_idx in range(user_placed_hint.well_hints_tag_block.count):
                            well_hint_element_node = None
                            if XML_OUTPUT:
                                well_hint_element_node = TAG.xml_doc.createElement('element')
                                well_hint_element_node.setAttribute('index', str(well_hint_idx))
                                well_hint_node.appendChild(well_hint_element_node)

                            well_hint = SCENARIO.Hint()

                            well_hint.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(well_hint_element_node, "flags", HintFlags))
                            input_stream.read(2) # Padding?
                            well_hint.points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(well_hint_element_node, "points"))

                            user_placed_hint.well_hints.append(well_hint)

                        for well_hint_idx, well_hint in enumerate(user_placed_hint.well_hints):
                            well_hint_element_node = None
                            if XML_OUTPUT:
                                well_hint_element_node = well_hint_node.childNodes[well_hint_idx]

                            well_hint.points = []
                            if well_hint.points_tag_block.count > 0:
                                well_hint.points_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                well_point_node = tag_format.get_xml_node(XML_OUTPUT, well_hint.points_tag_block.count, well_hint_element_node, "name", "points")
                                for well_point_idx in range(well_hint.points_tag_block.count):
                                    well_point_element_node = None
                                    if XML_OUTPUT:
                                        well_point_element_node = TAG.xml_doc.createElement('element')
                                        well_point_element_node.setAttribute('index', str(well_point_idx))
                                        well_point_node.appendChild(well_point_element_node)

                                    well_point = SCENARIO.WellPoint()

                                    well_point.type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(well_point_element_node, "type", WellTypeEnum))
                                    input_stream.read(2) # Padding?
                                    well_point.point = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(well_point_element_node, "point"))
                                    well_point.reference_frame = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(well_point_element_node, "reference frame"))
                                    input_stream.read(2) # Padding?
                                    well_point.sector_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(well_point_element_node, "sector index"))
                                    well_point.normal = TAG.read_degree_2d(input_stream, TAG, tag_format.XMLData(well_point_element_node, "normal"))

                                    well_hint.points.append(well_point)

                    if user_placed_hint.flight_hints_tag_block.count > 0:
                        user_placed_hint.flight_hints_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        flight_hint_node = tag_format.get_xml_node(XML_OUTPUT, user_placed_hint.flight_hints_tag_block.count, user_placed_hint_element_node, "name", "flight hints")
                        for flight_hint_idx in range(user_placed_hint.flight_hints_tag_block.count):
                            flight_hint_element_node = None
                            if XML_OUTPUT:
                                flight_hint_element_node = TAG.xml_doc.createElement('element')
                                flight_hint_element_node.setAttribute('index', str(flight_hint_idx))
                                flight_hint_node.appendChild(flight_hint_element_node)

                            flight_hint = SCENARIO.FlightHint()

                            flight_hint.points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(flight_hint_element_node, "points"))

                            user_placed_hint.flight_hints.append(flight_hint)

                        for flight_hint_idx, flight_hint in enumerate(user_placed_hint.flight_hints):
                            flight_hint_element_node = None
                            if XML_OUTPUT:
                                flight_hint_element_node = flight_hint_node.childNodes[flight_hint_idx]

                            flight_hint.points = []
                            if flight_hint.points_tag_block.count > 0:
                                flight_hint.points_header = TAG.TagBlockHeader().read(input_stream, TAG)
                                flight_point_node = tag_format.get_xml_node(XML_OUTPUT, flight_hint.points_tag_block.count, flight_hint_element_node, "name", "points")
                                for flight_point_idx in range(flight_hint.points_tag_block.count):
                                    flight_point_element_node = None
                                    if XML_OUTPUT:
                                        flight_point_element_node = TAG.xml_doc.createElement('element')
                                        flight_point_element_node.setAttribute('index', str(flight_point_idx))
                                        flight_point_node.appendChild(flight_point_element_node)

                                    flight_hint.points.append(TAG.read_vector(input_stream, TAG, tag_format.XMLData(flight_point_element_node, "point")))

def read_ai_animation_references(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.ai_animation_references_tag_block.count > 0:
        SCENARIO.ai_animation_references_header = TAG.TagBlockHeader().read(input_stream, TAG)
        ai_animation_reference_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.ai_animation_references_tag_block.count, tag_node, "name", "ai animation references")
        for ai_animation_reference_idx in range(SCENARIO.scenario_body.ai_animation_references_tag_block.count):
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

def read_ai_script_references(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.ai_script_references_tag_block.count > 0:
        SCENARIO.ai_script_references_header = TAG.TagBlockHeader().read(input_stream, TAG)
        ai_script_reference_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.ai_script_references_tag_block.count, tag_node, "name", "ai script references")
        for ai_script_reference_idx in range(SCENARIO.scenario_body.ai_script_references_tag_block.count):
            ai_script_reference_element_node = None
            if XML_OUTPUT:
                ai_script_reference_element_node = TAG.xml_doc.createElement('element')
                ai_script_reference_element_node.setAttribute('index', str(ai_script_reference_idx))
                ai_script_reference_node.appendChild(ai_script_reference_element_node)

            SCENARIO.ai_script_references.append(get_name(input_stream, SCENARIO, TAG, ai_script_reference_element_node))

def read_ai_recording_references(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.ai_recording_references_tag_block.count > 0:
        SCENARIO.ai_recording_references_header = TAG.TagBlockHeader().read(input_stream, TAG)
        ai_recording_reference_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.ai_recording_references_tag_block.count, tag_node, "name", "ai recording references")
        for ai_recording_reference_idx in range(SCENARIO.scenario_body.ai_recording_references_tag_block.count):
            ai_recording_reference_element_node = None
            if XML_OUTPUT:
                ai_recording_reference_element_node = TAG.xml_doc.createElement('element')
                ai_recording_reference_element_node.setAttribute('index', str(ai_recording_reference_idx))
                ai_recording_reference_node.appendChild(ai_recording_reference_element_node)

            SCENARIO.ai_recording_references.append(get_name(input_stream, SCENARIO, TAG, ai_recording_reference_element_node))

def read_ai_conversations(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.ai_conversations_tag_block.count > 0:
        SCENARIO.ai_conversations_header = TAG.TagBlockHeader().read(input_stream, TAG)
        ai_conversations_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.ai_conversations_tag_block.count, tag_node, "name", "ai conversations")
        for ai_conversation_idx in range(SCENARIO.scenario_body.ai_conversations_tag_block.count):
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
            if ai_conversation.participants_tag_block.count > 0:
                ai_conversation.participants_header = TAG.TagBlockHeader().read(input_stream, TAG)
                participants_node = tag_format.get_xml_node(XML_OUTPUT, ai_conversation.participants_tag_block.count, ai_conversation_element_node, "name", "participants")
                for participant_idx in range(ai_conversation.participants_tag_block.count):
                    participant_element_node = None
                    if XML_OUTPUT:
                        participant_element_node = TAG.xml_doc.createElement('element')
                        participant_element_node.setAttribute('index', str(participant_idx))
                        participants_node.appendChild(participant_element_node)

                    ai_conversation.participants.append(get_participants(input_stream, SCENARIO, TAG, participant_element_node))

            if ai_conversation.lines_tag_block.count > 0:
                ai_conversation.lines_header = TAG.TagBlockHeader().read(input_stream, TAG)
                lines_node = tag_format.get_xml_node(XML_OUTPUT, ai_conversation.lines_tag_block.count, ai_conversation_element_node, "name", "lines")
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

def read_scripts(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.scripts_tag_block.count > 0:
        SCENARIO.scripts_header = TAG.TagBlockHeader().read(input_stream, TAG)
        script_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.scripts_tag_block.count, tag_node, "name", "scripts")
        for script_idx in range(SCENARIO.scenario_body.scripts_tag_block.count):
            script_element_node = None
            if XML_OUTPUT:
                script_element_node = TAG.xml_doc.createElement('element')
                script_element_node.setAttribute('index', str(script_idx))
                script_node.appendChild(script_element_node)

            SCENARIO.scripts.append(get_scripts(input_stream, SCENARIO, TAG, script_element_node))

def read_globals(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.globals_tag_block.count > 0:
        SCENARIO.globals_header = TAG.TagBlockHeader().read(input_stream, TAG)
        global_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.globals_tag_block.count, tag_node, "name", "globals")
        for global_idx in range(SCENARIO.scenario_body.globals_tag_block.count):
            global_element_node = None
            if XML_OUTPUT:
                global_element_node = TAG.xml_doc.createElement('element')
                global_element_node.setAttribute('index', str(global_idx))
                global_node.appendChild(global_element_node)

            SCENARIO.globals.append(get_globals(input_stream, SCENARIO, TAG, global_element_node))

def read_references(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.references_tag_block.count > 0:
        SCENARIO.references_header = TAG.TagBlockHeader().read(input_stream, TAG)
        reference_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.references_tag_block.count, tag_node, "name", "references")
        for reference_idx in range(SCENARIO.scenario_body.references_tag_block.count):
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

def read_source_files(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.source_files_tag_block.count > 0:
        SCENARIO.source_files_header = TAG.TagBlockHeader().read(input_stream, TAG)
        source_file_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.source_files_tag_block.count, tag_node, "name", "source files")
        for source_file_idx in range(SCENARIO.scenario_body.source_files_tag_block.count):
            source_file_element_node = None
            if XML_OUTPUT:
                source_file_element_node = TAG.xml_doc.createElement('element')
                source_file_element_node.setAttribute('index', str(source_file_idx))
                source_file_node.appendChild(source_file_element_node)

            SCENARIO.source_files.append(get_source_file(input_stream, SCENARIO, TAG, source_file_element_node))

        for source_file_idx, source_file in enumerate(SCENARIO.source_files):
            source_file.source = TAG.read_variable_string_no_terminator(input_stream, source_file.source_tag_data.size, TAG)

def read_scripting_data(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.scripting_data_tag_block.count > 0:
        SCENARIO.scripting_data_header = TAG.TagBlockHeader().read(input_stream, TAG)
        scripting_data_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.scripting_data_tag_block.count, tag_node, "name", "scripting data")
        for scripting_data_idx in range(SCENARIO.scenario_body.scripting_data_tag_block.count):
            scripting_data_element_node = None
            if XML_OUTPUT:
                scripting_data_element_node = TAG.xml_doc.createElement('element')
                scripting_data_element_node.setAttribute('index', str(scripting_data_idx))
                scripting_data_node.appendChild(scripting_data_element_node)

            SCENARIO.scripting_data.append(get_scripting_data(input_stream, SCENARIO, TAG, scripting_data_element_node))

        for scripting_data_idx, scripting_data in enumerate(SCENARIO.scripting_data):
            scripting_data_element_node = None
            if XML_OUTPUT:
                scripting_data_element_node = scripting_data_node.childNodes[scripting_data_idx]

            scripting_data.point_sets = []
            if scripting_data.point_sets_tag_block.count > 0:
                scripting_data.point_sets_header = TAG.TagBlockHeader().read(input_stream, TAG)
                point_set_node = tag_format.get_xml_node(XML_OUTPUT, scripting_data.point_sets_tag_block.count, scripting_data_element_node, "name", "point sets")
                for point_set_idx in range(scripting_data.point_sets_tag_block.count):
                    point_set_element_node = None
                    if XML_OUTPUT:
                        point_set_element_node = TAG.xml_doc.createElement('element')
                        point_set_element_node.setAttribute('index', str(point_set_idx))
                        point_set_node.appendChild(point_set_element_node)

                    point_set = SCENARIO.PointSet()

                    point_set.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(point_set_element_node, "name"))
                    point_set.points_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(point_set_element_node, "points"))
                    point_set.bsp_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(point_set_element_node, "bsp index", None, SCENARIO.scenario_body.structure_bsps_tag_block.count, "scenario_structure_bsps_block"))
                    point_set.manual_reference_frame = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(point_set_element_node, "manual reference frame"))
                    point_set.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(point_set_element_node, "flags", PointSetFlags))

                    scripting_data.point_sets.append(point_set)

                for point_set_idx, point_set in enumerate(scripting_data.point_sets):
                    point_set_element_node = None
                    if XML_OUTPUT:
                        point_set_element_node = point_set_node.childNodes[point_set_idx]

                    point_set.points = []
                    if point_set.points_tag_block.count > 0:
                        point_set.points_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        point_node = tag_format.get_xml_node(XML_OUTPUT, point_set.points_tag_block.count, point_set_element_node, "name", "points")
                        for point_idx in range(point_set.points_tag_block.count):
                            point_element_node = None
                            if XML_OUTPUT:
                                point_element_node = TAG.xml_doc.createElement('element')
                                point_element_node.setAttribute('index', str(point_idx))
                                point_node.appendChild(point_element_node)

                            point = SCENARIO.Point()

                            point.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(point_element_node, "name"))
                            point.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(point_element_node, "position"))
                            point.reference_frame = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(point_element_node, "reference frame"))
                            input_stream.read(2) # Padding
                            point.surface_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(point_element_node, "surface index"))
                            point.facing_direction = TAG.read_degree_2d(input_stream, TAG, tag_format.XMLData(point_element_node, "facing direction"))

                            point_set.points.append(point)

def read_cutscene_flags(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.cutscene_flags_tag_block.count > 0:
        SCENARIO.cutscene_flags_header = TAG.TagBlockHeader().read(input_stream, TAG)
        cutscene_flag_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.cutscene_flags_tag_block.count, tag_node, "name", "cutscene flags")
        for cutscene_flag_idx in range(SCENARIO.scenario_body.cutscene_flags_tag_block.count):
            cutscene_flag_element_node = None
            if XML_OUTPUT:
                cutscene_flag_element_node = TAG.xml_doc.createElement('element')
                cutscene_flag_element_node.setAttribute('index', str(cutscene_flag_idx))
                cutscene_flag_node.appendChild(cutscene_flag_element_node)

            SCENARIO.cutscene_flags.append(get_cutscene_flags(input_stream, SCENARIO, TAG, cutscene_flag_element_node))

def read_cutscene_camera_points(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.cutscene_camera_points_tag_block.count > 0:
        SCENARIO.cutscene_camera_points_header = TAG.TagBlockHeader().read(input_stream, TAG)
        cutscene_camera_point_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.cutscene_camera_points_tag_block.count, tag_node, "name", "cutscene camera points")
        for cutscene_camera_point_idx in range(SCENARIO.scenario_body.cutscene_camera_points_tag_block.count):
            cutscene_camera_point_element_node = None
            if XML_OUTPUT:
                cutscene_camera_point_element_node = TAG.xml_doc.createElement('element')
                cutscene_camera_point_element_node.setAttribute('index', str(cutscene_camera_point_idx))
                cutscene_camera_point_node.appendChild(cutscene_camera_point_element_node)

            SCENARIO.cutscene_camera_points.append(get_cutscene_camera_points(input_stream, SCENARIO, TAG, cutscene_camera_point_element_node))

def read_cutscene_titles(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.cutscene_titles_tag_block.count > 0:
        SCENARIO.cutscene_titles_header = TAG.TagBlockHeader().read(input_stream, TAG)
        cutscene_title_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.cutscene_titles_tag_block.count, tag_node, "name", "cutscene titles")
        for cutscene_title_idx in range(SCENARIO.scenario_body.cutscene_titles_tag_block.count):
            cutscene_title_element_node = None
            if XML_OUTPUT:
                cutscene_title_element_node = TAG.xml_doc.createElement('element')
                cutscene_title_element_node.setAttribute('index', str(cutscene_title_idx))
                cutscene_title_node.appendChild(cutscene_title_element_node)

            SCENARIO.cutscene_titles.append(get_cutscene_titles(input_stream, SCENARIO, TAG, cutscene_title_element_node))

        for cutscene_title_idx, cutscene_title in enumerate(SCENARIO.cutscene_titles):
            cutscene_title_element_node = None
            if XML_OUTPUT:
                cutscene_title_element_node = cutscene_title_node.childNodes[cutscene_title_idx]

            if cutscene_title.name_length > 0:
                cutscene_title.name = TAG.read_variable_string_no_terminator(input_stream, cutscene_title.name_length, TAG, tag_format.XMLData(cutscene_title_element_node, "name"))

def read_structure_bsps(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.structure_bsps_tag_block.count > 0:
        SCENARIO.structure_bsps_header = TAG.TagBlockHeader().read(input_stream, TAG)
        structure_bsp_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.structure_bsps_tag_block.count, tag_node, "name", "structure bsps")
        for structure_bsp_idx in range(SCENARIO.scenario_body.structure_bsps_tag_block.count):
            structure_bsp_element_node = None
            if XML_OUTPUT:
                structure_bsp_element_node = TAG.xml_doc.createElement('element')
                structure_bsp_element_node.setAttribute('index', str(structure_bsp_idx))
                structure_bsp_node.appendChild(structure_bsp_element_node)

            SCENARIO.structure_bsps.append(get_structure_bsp(input_stream, SCENARIO, TAG, structure_bsp_element_node))

        for structure_bsp_idx, structure_bsp in enumerate(SCENARIO.structure_bsps):
            structure_bsp_name_length = structure_bsp.structure_bsp.name_length
            structure_lightmap_name_length = structure_bsp.structure_lightmap.name_length
            if structure_bsp_name_length > 0:
                structure_bsp.structure_bsp.name = TAG.read_variable_string(input_stream, structure_bsp_name_length, TAG)

            if structure_lightmap_name_length > 0:
                structure_bsp.structure_lightmap.name = TAG.read_variable_string(input_stream, structure_lightmap_name_length, TAG)

            if XML_OUTPUT:
                structure_bsp_element_node = structure_bsp_node.childNodes[structure_bsp_idx]
                structure_bsp_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, structure_bsp_element_node, "name", "structure bsp")
                structure_lightmap_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, structure_bsp_element_node, "name", "structure lightmap")
                structure_bsp.structure_bsp.append_xml_attributes(structure_bsp_tag_ref_node)
                structure_bsp.structure_lightmap.append_xml_attributes(structure_lightmap_tag_ref_node)

def read_scenario_resoruces(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.scenario_resources_tag_block.count > 0:
        SCENARIO.scenario_resources_header = TAG.TagBlockHeader().read(input_stream, TAG)
        scenario_resources_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.scenario_resources_tag_block.count, tag_node, "name", "scenario resources")
        for scenario_resource_idx in range(SCENARIO.scenario_body.scenario_resources_tag_block.count):
            scenario_resource_element_node = None
            if XML_OUTPUT:
                scenario_resource_element_node = TAG.xml_doc.createElement('element')
                scenario_resource_element_node.setAttribute('index', str(scenario_resource_idx))
                scenario_resources_node.appendChild(scenario_resource_element_node)

            scenario_resource = SCENARIO.ScenarioResource()
            scenario_resource.references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(scenario_resource_element_node, "references"))
            scenario_resource.script_source_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(scenario_resource_element_node, "script source"))
            scenario_resource.ai_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(scenario_resource_element_node, "ai resources"))

            SCENARIO.scenario_resources.append(scenario_resource)

        for scenario_resource_idx, scenario_resource in enumerate(SCENARIO.scenario_resources):
            scenario_resource_element_node = None
            if XML_OUTPUT:
                scenario_resource_element_node = scenario_resources_node.childNodes[scenario_resource_idx]

            scenario_resource.references = []
            scenario_resource.script_source = []
            scenario_resource.ai_resources = []
            palette_helper(input_stream, scenario_resource.references_tag_block.count, "references", scenario_resource.references_header, scenario_resource.references, scenario_resource_element_node, TAG, 0)
            palette_helper(input_stream, scenario_resource.script_source_tag_block.count, "script source", scenario_resource.script_source_header, scenario_resource.script_source, scenario_resource_element_node, TAG, 0)
            palette_helper(input_stream, scenario_resource.ai_resources_tag_block.count, "ai resources", scenario_resource.ai_resources_header, scenario_resource.ai_resources, scenario_resource_element_node, TAG, 0)

def read_old_structure_physics(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.old_structure_physics_tag_block.count > 0:
        SCENARIO.old_structure_physics_header = TAG.TagBlockHeader().read(input_stream, TAG)
        old_structure_physics_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.old_structure_physics_tag_block.count, tag_node, "name", "old structure physics")
        for old_structure_physics_idx in range(SCENARIO.scenario_body.old_structure_physics_tag_block.count):
            old_structure_physics_element_node = None
            if XML_OUTPUT:
                old_structure_physics_element_node = TAG.xml_doc.createElement('element')
                old_structure_physics_element_node.setAttribute('index', str(old_structure_physics_idx))
                old_structure_physics_node.appendChild(old_structure_physics_element_node)

            old_structure_physics = SCENARIO.OldStructurePhysics()
            old_structure_physics.physics_tag_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(old_structure_physics_element_node, "mopp"))
            old_structure_physics.object_identifiers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(old_structure_physics_element_node, "object identifiers"))
            input_stream.read(4) # Padding
            old_structure_physics.mopp_bounds_min = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(old_structure_physics_element_node, "mopp bounds min"))
            old_structure_physics.mopp_bounds_max = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(old_structure_physics_element_node, "mopp bounds max"))

            SCENARIO.old_structure_physics.append(old_structure_physics)

        for old_structure_physics_idx, old_structure_physics in enumerate(SCENARIO.old_structure_physics):
            old_structure_physics_element_node = None
            if XML_OUTPUT:
                old_structure_physics_element_node = old_structure_physics_node.childNodes[old_structure_physics_idx]

            old_structure_physics.object_identifiers = []
            old_structure_physics.physics_data = input_stream.read(old_structure_physics.physics_tag_data.size)
            if old_structure_physics.object_identifiers_tag_block.count > 0:
                old_structure_physics.object_identifiers_header = TAG.TagBlockHeader().read(input_stream, TAG)
                object_identifiers_node = tag_format.get_xml_node(XML_OUTPUT, old_structure_physics.object_identifiers_tag_block.count, old_structure_physics_element_node, "name", "object identifiers")
                for object_identifier_idx in range(old_structure_physics.object_identifiers_tag_block.count):
                    object_identifier_element_node = None
                    if XML_OUTPUT:
                        object_identifier_element_node = TAG.xml_doc.createElement('element')
                        object_identifier_element_node.setAttribute('index', str(object_identifier_idx))
                        object_identifiers_node.appendChild(object_identifier_element_node)

                    object_identifier = SCENARIO.ObjectIdentifier()

                    object_identifier.unique_id = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(object_identifier_element_node, "unique id"))
                    object_identifier.origin_bsp_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(object_identifier_element_node, "origin bsp index", None, SCENARIO.scenario_body.structure_bsps_tag_block.count, "scenario_bsp_block"))
                    object_identifier.object_type = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(object_identifier_element_node, "object type", ObjectTypeFlags))
                    object_identifier.source = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(object_identifier_element_node, "source", ObjectSourceFlags))
                    object_identifier.sobj_header = TAG.TagBlockHeader().read(input_stream, TAG)

                    old_structure_physics.object_identifiers.append(object_identifier)

def read_hs_unit_seats(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.hs_unit_seats_tag_block.count > 0:
        SCENARIO.hs_unit_seat_header = TAG.TagBlockHeader().read(input_stream, TAG)
        hs_unit_seats_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.hs_unit_seats_tag_block.count, tag_node, "name", "hs unit seats")
        for hs_unit_seat_idx in range(SCENARIO.scenario_body.hs_unit_seats_tag_block.count):
            hs_unit_seat_element_node = None
            if XML_OUTPUT:
                hs_unit_seat_element_node = TAG.xml_doc.createElement('element')
                hs_unit_seat_element_node.setAttribute('index', str(hs_unit_seat_idx))
                hs_unit_seats_node.appendChild(hs_unit_seat_element_node)

            hs_unit_seat = SCENARIO.HSUnitSeat()
            hs_unit_seat.unit_definition_tag_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(hs_unit_seat_element_node, "unit definition tag index"))
            hs_unit_seat.unit_seats = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(hs_unit_seat_element_node, "unit seats"))

            SCENARIO.hs_unit_seats.append(hs_unit_seat)

def read_scenario_kill_triggers(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.scenario_kill_triggers_tag_block.count > 0:
        SCENARIO.scenario_kill_triggers_header = TAG.TagBlockHeader().read(input_stream, TAG)
        scenario_kill_triggers_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.scenario_kill_triggers_tag_block.count, tag_node, "name", "scenario kill triggers")
        for scenario_kill_trigger_idx in range(SCENARIO.scenario_body.scenario_kill_triggers_tag_block.count):
            scenario_kill_trigger_element_node = None
            if XML_OUTPUT:
                scenario_kill_trigger_element_node = TAG.xml_doc.createElement('element')
                scenario_kill_trigger_element_node.setAttribute('index', str(scenario_kill_trigger_idx))
                scenario_kill_triggers_node.appendChild(scenario_kill_trigger_element_node)

            trigger_volume = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(scenario_kill_trigger_element_node, "trigger volume", None, SCENARIO.scenario_body.trigger_volumes_tag_block.count, "scenario_trigger_volumes_block"))

            SCENARIO.scenario_kill_triggers.append(trigger_volume)

def read_hs_syntax_datum(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.hs_syntax_datums_tag_block.count > 0:
        SCENARIO.hs_syntax_datums_header = TAG.TagBlockHeader().read(input_stream, TAG)
        hs_syntax_datums_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.hs_syntax_datums_tag_block.count, tag_node, "name", "hs syntax datums")
        for hs_syntax_datum_idx in range(SCENARIO.scenario_body.hs_syntax_datums_tag_block.count):
            hs_syntax_datum_element_node = None
            if XML_OUTPUT:
                hs_syntax_datum_element_node = TAG.xml_doc.createElement('element')
                hs_syntax_datum_element_node.setAttribute('index', str(hs_syntax_datum_idx))
                hs_syntax_datums_node.appendChild(hs_syntax_datum_element_node)

            hs_syntax_datum = SCENARIO.HSSyntaxDatum()
            hs_syntax_datum.datum_header = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(hs_syntax_datum_element_node, "datum header"))
            hs_syntax_datum.script_index_function_index_con = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(hs_syntax_datum_element_node, "script index/function index/con"))
            hs_syntax_datum.datum_type = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(hs_syntax_datum_element_node, "type"))
            hs_syntax_datum.flags = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(hs_syntax_datum_element_node, "flags"))
            hs_syntax_datum.next_node_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(hs_syntax_datum_element_node, "next node index"))
            hs_syntax_datum.data = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(hs_syntax_datum_element_node, "data"))
            hs_syntax_datum.source_offset = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(hs_syntax_datum_element_node, "source_offset"))

            SCENARIO.hs_syntax_datums.append(hs_syntax_datum)

def read_orders(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.orders_tag_block.count > 0:
        SCENARIO.orders_header = TAG.TagBlockHeader().read(input_stream, TAG)
        orders_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.orders_tag_block.count, tag_node, "name", "orders")
        for order_idx in range(SCENARIO.scenario_body.orders_tag_block.count):
            order_element_node = None
            if XML_OUTPUT:
                order_element_node = TAG.xml_doc.createElement('element')
                order_element_node.setAttribute('index', str(order_idx))
                orders_node.appendChild(order_element_node)

            order = SCENARIO.Order()
            order.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(order_element_node, "name"))
            order.style_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(order_element_node, "style", None, SCENARIO.scenario_body.style_palette_tag_block.count, "style_palette_block"))
            input_stream.read(2) # Padding
            order.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(order_element_node, "flags", OrderFlags))
            order.force_combat_status = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(order_element_node, "force combat status", OrderEnum))
            input_stream.read(2) # Padding
            order.entry_script = TAG.read_string32(input_stream, TAG, tag_format.XMLData(order_element_node, "entry script"))
            input_stream.read(2) # Padding
            order.follow_squad = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(order_element_node, "follow squad", None, SCENARIO.scenario_body.squads_tag_block.count, "squads_block"))
            order.follow_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(order_element_node, "follow radius"))
            order.primary_area_set_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(order_element_node, "primary area set"))
            order.secondary_area_set_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(order_element_node, "secondary area set"))
            order.secondary_set_trigger_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(order_element_node, "secondary set trigger"))
            order.special_movement_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(order_element_node, "special movement"))
            order.order_endings_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(order_element_node, "order endings"))

            SCENARIO.orders.append(order)

        for order_idx, order in enumerate(SCENARIO.orders):
            orders_element_node = None
            if XML_OUTPUT:
                orders_element_node = orders_node.childNodes[order_idx]

            order.primary_area_set = []
            order.secondary_area_set = []
            order.secondary_set_trigger = []
            order.special_movement = []
            order.order_endings = []
            if order.primary_area_set_tag_block.count > 0:
                order.primary_area_set_header = TAG.TagBlockHeader().read(input_stream, TAG)
                primary_area_set_node = tag_format.get_xml_node(XML_OUTPUT, order.primary_area_set_tag_block.count, orders_element_node, "name", "primary area set")
                for primary_area_set_idx in range(order.primary_area_set_tag_block.count):
                    primary_area_set_element_node = None
                    if XML_OUTPUT:
                        primary_area_set_element_node = TAG.xml_doc.createElement('element')
                        primary_area_set_element_node.setAttribute('index', str(primary_area_set_idx))
                        primary_area_set_node.appendChild(primary_area_set_element_node)

                    area_set = SCENARIO.AreaSet()
                    area_set.area_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(primary_area_set_element_node, "area type", AreaTypeEnum))
                    input_stream.read(2) # Padding
                    area_set.zone_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(primary_area_set_element_node, "zone", None, SCENARIO.scenario_body.zones_tag_block.count, "zone_block"))
                    area_block_count = 0
                    if not area_set.zone_index == -1 and not area_set.zone_index >= SCENARIO.scenario_body.zones_tag_block.count:
                        area_block_count = SCENARIO.zones[area_set.zone_index].areas_tag_block.count

                    area_set.area_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(primary_area_set_element_node, "area", None, area_block_count, "areas_block"))

                    order.primary_area_set.append(area_set)

            if order.secondary_area_set_tag_block.count > 0:
                order.secondary_area_set_header = TAG.TagBlockHeader().read(input_stream, TAG)
                secondary_area_set_node = tag_format.get_xml_node(XML_OUTPUT, order.secondary_area_set_tag_block.count, orders_element_node, "name", "secondary area set")
                for secondary_area_set_idx in range(order.secondary_area_set_tag_block.count):
                    secondary_area_set_element_node = None
                    if XML_OUTPUT:
                        secondary_area_set_element_node = TAG.xml_doc.createElement('element')
                        secondary_area_set_element_node.setAttribute('index', str(secondary_area_set_idx))
                        secondary_area_set_node.appendChild(secondary_area_set_element_node)

                    area_set = SCENARIO.AreaSet()
                    area_set.area_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(secondary_area_set_element_node, "area type", AreaTypeEnum))
                    input_stream.read(2) # Padding
                    area_set.zone_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(secondary_area_set_element_node, "zone", None, SCENARIO.scenario_body.zones_tag_block.count, "zone_block"))
                    area_block_count = 0
                    if not area_set.zone_index == -1 and not area_set.zone_index >= SCENARIO.scenario_body.zones_tag_block.count:
                        area_block_count = SCENARIO.zones[area_set.zone_index].areas_tag_block.count

                    area_set.area_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(secondary_area_set_element_node, "area", None, area_block_count, "areas_block"))

                    order.secondary_area_set.append(area_set)

            if order.secondary_set_trigger_tag_block.count > 0:
                order.secondary_set_trigger_header = TAG.TagBlockHeader().read(input_stream, TAG)
                secondary_set_trigger_node = tag_format.get_xml_node(XML_OUTPUT, order.secondary_set_trigger_tag_block.count, orders_element_node, "name", "secondary set trigger")
                for secondary_set_trigger_idx in range(order.secondary_set_trigger_tag_block.count):
                    secondary_set_trigger_element_node = None
                    if XML_OUTPUT:
                        secondary_set_trigger_element_node = TAG.xml_doc.createElement('element')
                        secondary_set_trigger_element_node.setAttribute('index', str(secondary_set_trigger_idx))
                        secondary_set_trigger_node.appendChild(secondary_set_trigger_element_node)

                    set_trigger = SCENARIO.SetTrigger()

                    set_trigger.combination_rule = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(secondary_set_trigger_element_node, "combination rule", CombinationRuleEnum))
                    set_trigger.dialogue_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(secondary_set_trigger_element_node, "dialogue type", DialogueTypeEnum))
                    set_trigger.triggers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(secondary_set_trigger_element_node, "triggers"))

                    order.secondary_set_trigger.append(set_trigger)

                for secondary_set_trigger_idx, secondary_set_trigger in enumerate(order.secondary_set_trigger):
                    secondary_set_trigger_element_node = None
                    if XML_OUTPUT:
                        secondary_set_trigger_element_node = secondary_set_trigger_node.childNodes[secondary_set_trigger_idx]

                    secondary_set_trigger.triggers = []
                    if secondary_set_trigger.triggers_tag_block.count > 0:
                        secondary_set_trigger.triggers_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        triggers_node = tag_format.get_xml_node(XML_OUTPUT, secondary_set_trigger.triggers_tag_block.count, secondary_set_trigger_element_node, "name", "triggers")
                        for trigger_idx in range(secondary_set_trigger.triggers_tag_block.count):
                            trigger_element_node = None
                            if XML_OUTPUT:
                                trigger_element_node = TAG.xml_doc.createElement('element')
                                trigger_element_node.setAttribute('index', str(trigger_idx))
                                triggers_node.appendChild(trigger_element_node)

                            trigger = SCENARIO.Trigger()

                            trigger.trigger_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(trigger_element_node, "flags", TriggerFlags))
                            trigger.trigger = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(trigger_element_node, "trigger", None, SCENARIO.scenario_body.triggers_tag_block.count, "triggers_block"))
                            input_stream.read(2) # Padding

                            secondary_set_trigger.triggers.append(trigger)

            if order.special_movement_tag_block.count > 0:
                order.special_movement_header = TAG.TagBlockHeader().read(input_stream, TAG)
                special_movement_node = tag_format.get_xml_node(XML_OUTPUT, order.special_movement_tag_block.count, orders_element_node, "name", "special movement")
                for special_movement_idx in range(order.special_movement_tag_block.count):
                    special_movement_element_node = None
                    if XML_OUTPUT:
                        special_movement_element_node = TAG.xml_doc.createElement('element')
                        special_movement_element_node.setAttribute('index', str(special_movement_idx))
                        special_movement_node.appendChild(special_movement_element_node)

                    special_movement = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(special_movement_element_node, "flags", SpecialMovementFlags))

                    order.special_movement.append(special_movement)

            if order.order_endings_tag_block.count > 0:
                order.order_endings_header = TAG.TagBlockHeader().read(input_stream, TAG)
                order_endings_node = tag_format.get_xml_node(XML_OUTPUT, order.order_endings_tag_block.count, orders_element_node, "name", "order endings")
                for order_ending_idx in range(order.order_endings_tag_block.count):
                    order_ending_element_node = None
                    if XML_OUTPUT:
                        order_ending_element_node = TAG.xml_doc.createElement('element')
                        order_ending_element_node.setAttribute('index', str(order_ending_idx))
                        order_endings_node.appendChild(order_ending_element_node)

                    order_ending = SCENARIO.OrderEnding()

                    order_ending.next_order_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(order_ending_element_node, "next order", None, SCENARIO.scenario_body.orders_tag_block.count, "orders_block"))
                    order_ending.combination_rule = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(order_ending_element_node, "combination rule", CombinationRuleEnum))
                    order_ending.delay_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(order_ending_element_node, "delay time"))
                    order_ending.dialogue_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(order_ending_element_node, "dialogue type", DialogueTypeEnum))
                    input_stream.read(2) # Padding
                    order_ending.triggers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(order_ending_element_node, "triggers"))

                    order.order_endings.append(order_ending)

                for order_ending_idx, order_ending in enumerate(order.order_endings):
                    order_ending_element_node = None
                    if XML_OUTPUT:
                        order_ending_element_node = order_endings_node.childNodes[order_ending_idx]

                    order_ending.triggers = []
                    if order_ending.triggers_tag_block.count > 0:
                        order_ending.triggers_header = TAG.TagBlockHeader().read(input_stream, TAG)
                        triggers_node = tag_format.get_xml_node(XML_OUTPUT, order_ending.triggers_tag_block.count, order_ending_element_node, "name", "triggers")
                        for trigger_idx in range(order_ending.triggers_tag_block.count):
                            trigger_element_node = None
                            if XML_OUTPUT:
                                trigger_element_node = TAG.xml_doc.createElement('element')
                                trigger_element_node.setAttribute('index', str(trigger_idx))
                                triggers_node.appendChild(trigger_element_node)

                            trigger = SCENARIO.Trigger()

                            trigger.trigger_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(trigger_element_node, "flags", TriggerFlags))
                            trigger.trigger = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(trigger_element_node, "trigger", None, SCENARIO.scenario_body.triggers_tag_block.count, "triggers_block"))
                            input_stream.read(2) # Padding

                            order_ending.triggers.append(trigger)

def read_triggers(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.triggers_tag_block.count > 0:
        SCENARIO.triggers_header = TAG.TagBlockHeader().read(input_stream, TAG)
        triggers_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.triggers_tag_block.count, tag_node, "name", "triggers")
        for trigger_idx in range(SCENARIO.scenario_body.triggers_tag_block.count):
            trigger_element_node = None
            if XML_OUTPUT:
                trigger_element_node = TAG.xml_doc.createElement('element')
                trigger_element_node.setAttribute('index', str(trigger_idx))
                triggers_node.appendChild(trigger_element_node)

            trigger = SCENARIO.AITrigger()
            trigger.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(trigger_element_node, "name"))
            trigger.trigger_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(trigger_element_node, "trigger flags", AITriggerFlags))
            trigger.combination_rule = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(trigger_element_node, "combination rule", CombinationRuleEnum))
            input_stream.read(2) # Padding
            trigger.conditions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(trigger_element_node, "conditions"))

            SCENARIO.triggers.append(trigger)

        for trigger_idx, trigger in enumerate(SCENARIO.triggers):
            trigger_element_node = None
            if XML_OUTPUT:
                trigger_element_node = triggers_node.childNodes[trigger_idx]

            trigger.conditions = []
            if trigger.conditions_tag_block.count > 0:
                trigger.conditions_header = TAG.TagBlockHeader().read(input_stream, TAG)
                conditions_node = tag_format.get_xml_node(XML_OUTPUT, trigger.conditions_tag_block.count, trigger_element_node, "name", "conditions")
                for condition_idx in range(trigger.conditions_tag_block.count):
                    condition_element_node = None
                    if XML_OUTPUT:
                        condition_element_node = TAG.xml_doc.createElement('element')
                        condition_element_node.setAttribute('index', str(condition_idx))
                        conditions_node.appendChild(condition_element_node)

                    condition = SCENARIO.Condition()
                    condition.rule_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(condition_element_node, "rule type", RuleTypeEnum))
                    condition.squad_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(condition_element_node, "squad", None, SCENARIO.scenario_body.squads_tag_block.count, "squads_block"))
                    condition.squad_group_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(condition_element_node, "squad group", None, SCENARIO.scenario_body.squad_groups_tag_block.count, "squad_groups_block"))
                    condition.a = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(condition_element_node, "resource index"))
                    condition.x = TAG.read_float(input_stream, TAG, tag_format.XMLData(condition_element_node, "period"))
                    condition.trigger_volume_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(condition_element_node, "trigger volume index", None, SCENARIO.scenario_body.trigger_volumes_tag_block.count, "scenario_trigger_volume_block"))
                    input_stream.read(2) # Padding
                    condition.exit_condition_script = TAG.read_string32(input_stream, TAG, tag_format.XMLData(condition_element_node, "exit condition script"))
                    condition.exit_condition_script_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(condition_element_node, "exit condition script index"))
                    input_stream.read(2) # Padding
                    condition.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(condition_element_node, "flags", TriggerFlags))

                    trigger.conditions.append(condition)

def read_background_sound_palette(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.background_sound_palette_tag_block.count > 0:
        SCENARIO.background_sound_palette_header = TAG.TagBlockHeader().read(input_stream, TAG)
        background_sound_palette_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.background_sound_palette_tag_block.count, tag_node, "name", "background sound palette")
        for background_sound_palette_idx in range(SCENARIO.scenario_body.background_sound_palette_tag_block.count):
            background_sound_palette_element_node = None
            if XML_OUTPUT:
                background_sound_palette_element_node = TAG.xml_doc.createElement('element')
                background_sound_palette_element_node.setAttribute('index', str(background_sound_palette_idx))
                background_sound_palette_node.appendChild(background_sound_palette_element_node)

            background_sound_palette = SCENARIO.BackgroundSoundPalette()
            background_sound_palette.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(background_sound_palette_element_node, "name"))
            background_sound_palette.background_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(background_sound_palette_element_node, "background sound"))
            background_sound_palette.inside_cluster_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(background_sound_palette_element_node, "inside cluster sound"))
            input_stream.read(20) # Padding
            background_sound_palette.cutoff_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(background_sound_palette_element_node, "cutoff distance"))
            background_sound_palette.scale_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(background_sound_palette_element_node, "scale flags", ScaleFlags))
            background_sound_palette.interior_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(background_sound_palette_element_node, "interior scale"))
            background_sound_palette.portal_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(background_sound_palette_element_node, "portal scale"))
            background_sound_palette.exterior_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(background_sound_palette_element_node, "exterior scale"))
            background_sound_palette.interpolation_speed = TAG.read_float(input_stream, TAG, tag_format.XMLData(background_sound_palette_element_node, "interpolation speed"))
            input_stream.read(8) # Padding

            SCENARIO.background_sound_palette.append(background_sound_palette)

        for background_sound_palette_idx, background_sound_palette in enumerate(SCENARIO.background_sound_palette):
            background_sound_palette_element_node = None

            background_sound_name_length = background_sound_palette.background_sound.name_length
            inside_cluster_sound_name_length = background_sound_palette.inside_cluster_sound.name_length
            if background_sound_name_length > 0:
                background_sound_palette.background_sound.name = TAG.read_variable_string(input_stream, background_sound_name_length, TAG)

            if inside_cluster_sound_name_length > 0:
                background_sound_palette.inside_cluster_sound.name = TAG.read_variable_string(input_stream, inside_cluster_sound_name_length, TAG)

            if XML_OUTPUT:
                background_sound_palette_element_node = background_sound_palette_node.childNodes[background_sound_palette_idx]
                background_sound_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, background_sound_palette_element_node, "name", "background sound")
                inside_cluster_sound_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, background_sound_palette_element_node, "name", "inside cluster sound")
                background_sound_palette.background_sound.append_xml_attributes(background_sound_tag_ref_node)
                background_sound_palette.inside_cluster_sound.append_xml_attributes(inside_cluster_sound_tag_ref_node)

def read_sound_environment_palette(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.sound_environment_palette_tag_block.count > 0:
        SCENARIO.sound_environment_palette_header = TAG.TagBlockHeader().read(input_stream, TAG)
        sound_environment_palette_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.sound_environment_palette_tag_block.count, tag_node, "name", "sound environment palette")
        for sound_environment_palette_idx in range(SCENARIO.scenario_body.sound_environment_palette_tag_block.count):
            sound_environment_palette_element_node = None
            if XML_OUTPUT:
                sound_environment_palette_element_node = TAG.xml_doc.createElement('element')
                sound_environment_palette_element_node.setAttribute('index', str(sound_environment_palette_idx))
                sound_environment_palette_node.appendChild(sound_environment_palette_element_node)

            sound_environment_palette = SCENARIO.SoundEnvironmentPalette()
            sound_environment_palette.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(sound_environment_palette_element_node, "name"))
            sound_environment_palette.sound_environment = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(sound_environment_palette_element_node, "sound environment"))
            sound_environment_palette.cutoff_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(sound_environment_palette_element_node, "cutoff distance"))
            sound_environment_palette.interpolation_speed = TAG.read_float(input_stream, TAG, tag_format.XMLData(sound_environment_palette_element_node, "interpolation speed"))
            input_stream.read(24) # Padding

            SCENARIO.sound_environment_palette.append(sound_environment_palette)

        for sound_environment_palette_idx, sound_environment_palette in enumerate(SCENARIO.sound_environment_palette):
            sound_environment_palette_element_node = None

            sound_environment_name_length = sound_environment_palette.sound_environment.name_length
            if sound_environment_name_length > 0:
                sound_environment_palette.sound_environment.name = TAG.read_variable_string(input_stream, sound_environment_name_length, TAG)

            if XML_OUTPUT:
                sound_environment_palette_element_node = sound_environment_palette_node.childNodes[sound_environment_palette_idx]
                sound_environment_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, sound_environment_palette_element_node, "name", "sound environment")
                sound_environment_palette.sound_environment.append_xml_attributes(sound_environment_tag_ref_node)

def read_weather_palette(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.weather_palette_tag_block.count > 0:
        SCENARIO.weather_palette_header = TAG.TagBlockHeader().read(input_stream, TAG)
        weather_palette_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.weather_palette_tag_block.count, tag_node, "name", "weather palette")
        for weather_palette_idx in range(SCENARIO.scenario_body.weather_palette_tag_block.count):
            weather_palette_element_node = None
            if XML_OUTPUT:
                weather_palette_element_node = TAG.xml_doc.createElement('element')
                weather_palette_element_node.setAttribute('index', str(weather_palette_idx))
                weather_palette_node.appendChild(weather_palette_element_node)

            weather_palette = SCENARIO.WeatherPalette()
            weather_palette.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(weather_palette_element_node, "name"))
            weather_palette.weather_system = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(weather_palette_element_node, "weather system"))
            input_stream.read(36) # Padding
            weather_palette.wind = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(weather_palette_element_node, "wind"))
            weather_palette.wind_direction = TAG.read_vector(input_stream, TAG, tag_format.XMLData(weather_palette_element_node, "wind direction"))
            weather_palette.wind_magnitude = TAG.read_float(input_stream, TAG, tag_format.XMLData(weather_palette_element_node, "wind magnitude"))
            input_stream.read(4) # Padding
            weather_palette.wind_scale_function = TAG.read_string32(input_stream, TAG, tag_format.XMLData(weather_palette_element_node, "wind scale function"))

            SCENARIO.weather_palette.append(weather_palette)

        for weather_palette_idx, weather_palette in enumerate(SCENARIO.weather_palette):
            weather_palette_element_node = None

            weather_system_name_length = weather_palette.weather_system.name_length
            wind_name_length = weather_palette.wind.name_length
            if weather_system_name_length > 0:
                weather_palette.weather_system.name = TAG.read_variable_string(input_stream, weather_system_name_length, TAG)

            if wind_name_length > 0:
                weather_palette.wind.name = TAG.read_variable_string(input_stream, wind_name_length, TAG)

            if XML_OUTPUT:
                weather_palette_element_node = weather_palette_node.childNodes[weather_palette_idx]
                weather_system_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, weather_palette_element_node, "name", "weather system")
                wind_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, weather_palette_element_node, "name", "wind")
                weather_palette.weather_system.append_xml_attributes(weather_system_tag_ref_node)
                weather_palette.wind.append_xml_attributes(wind_tag_ref_node)

def read_scavenger_hunt_objects(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.scavenger_hunt_objects_tag_block.count > 0:
        SCENARIO.scavenger_hunt_objects_header = TAG.TagBlockHeader().read(input_stream, TAG)
        scavenger_hunt_objects_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.scavenger_hunt_objects_tag_block.count, tag_node, "name", "scavenger hunt objects")
        for scavenger_hunt_object_idx in range(SCENARIO.scenario_body.scavenger_hunt_objects_tag_block.count):
            scavenger_hunt_object_element_node = None
            if XML_OUTPUT:
                scavenger_hunt_object_element_node = TAG.xml_doc.createElement('element')
                scavenger_hunt_object_element_node.setAttribute('index', str(scavenger_hunt_object_idx))
                scavenger_hunt_objects_node.appendChild(scavenger_hunt_object_element_node)

            scavenger_hunt_object = SCENARIO.ScavengerHuntObject()
            scavenger_hunt_object.exported_name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(scavenger_hunt_object_element_node, "exported name"))
            scavenger_hunt_object.scenario_object_name_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(scavenger_hunt_object_element_node, "scenario object name index", None, SCENARIO.scenario_body.object_names_tag_block.count, "scenario_object_names_block"))
            input_stream.read(2) # Padding

            SCENARIO.scavenger_hunt_objects.append(scavenger_hunt_object)

def read_scenario_cluster_data(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.scenario_cluster_data_tag_block.count > 0:
        SCENARIO.scenario_cluster_data_header = TAG.TagBlockHeader().read(input_stream, TAG)
        scenario_cluster_data_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.scenario_cluster_data_tag_block.count, tag_node, "name", "scenario cluster data")
        for scenario_cluster_data_idx in range(SCENARIO.scenario_body.scenario_cluster_data_tag_block.count):
            scenario_cluster_data_element_node = None
            if XML_OUTPUT:
                scenario_cluster_data_element_node = TAG.xml_doc.createElement('element')
                scenario_cluster_data_element_node.setAttribute('index', str(scenario_cluster_data_idx))
                scenario_cluster_data_node.appendChild(scenario_cluster_data_element_node)

            scenario_cluster_data = SCENARIO.ScenarioClusterData()
            scenario_cluster_data.bsp = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(scenario_cluster_data_element_node, "bsp"))
            scenario_cluster_data.background_sounds_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(scenario_cluster_data_element_node, "background sounds"))
            scenario_cluster_data.sound_environments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(scenario_cluster_data_element_node, "sound environments"))
            scenario_cluster_data.bsp_checksum = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(scenario_cluster_data_element_node, "bsp checksum"))
            scenario_cluster_data.cluster_centroids_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(scenario_cluster_data_element_node, "cluster centroids"))
            scenario_cluster_data.weather_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(scenario_cluster_data_element_node, "weather properties"))
            scenario_cluster_data.atmospheric_fog_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(scenario_cluster_data_element_node, "atmospheric fog properties"))

            SCENARIO.scenario_cluster_data.append(scenario_cluster_data)

        for scenario_cluster_data_idx, scenario_cluster_data in enumerate(SCENARIO.scenario_cluster_data):
            scenario_cluster_data_element_node = None
            if XML_OUTPUT:
                scenario_cluster_data_element_node = scenario_cluster_data_node.childNodes[scenario_cluster_data_idx]

            bsp_name_length = scenario_cluster_data.bsp.name_length
            if bsp_name_length > 0:
                scenario_cluster_data.bsp.name = TAG.read_variable_string(input_stream, bsp_name_length, TAG)

            if XML_OUTPUT:
                bsp_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, scenario_cluster_data_element_node, "name", "bsp")
                scenario_cluster_data.bsp.append_xml_attributes(bsp_tag_ref_node)

            scenario_cluster_data.background_sounds = []
            scenario_cluster_data.sound_environments = []
            scenario_cluster_data.cluster_centroids = []
            scenario_cluster_data.weather_properties = []
            scenario_cluster_data.atmospheric_fog_properties = []
            if scenario_cluster_data.background_sounds_tag_block.count > 0:
                scenario_cluster_data.background_sounds_header = TAG.TagBlockHeader().read(input_stream, TAG)
                background_sounds_node = tag_format.get_xml_node(XML_OUTPUT, scenario_cluster_data.background_sounds_tag_block.count, scenario_cluster_data_element_node, "name", "background sounds")
                for background_sound_idx in range(scenario_cluster_data.background_sounds_tag_block.count):
                    background_sound_element_node = None
                    if XML_OUTPUT:
                        background_sound_element_node = TAG.xml_doc.createElement('element')
                        background_sound_element_node.setAttribute('index', str(background_sound_idx))
                        background_sounds_node.appendChild(background_sound_element_node)

                    background_sound_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(background_sound_element_node, "type", None, SCENARIO.scenario_body.background_sound_palette_tag_block.count, "structure_bsp_background_sound_palette_block"))
                    input_stream.read(2) # Padding

                    scenario_cluster_data.background_sounds.append(background_sound_index)

            if scenario_cluster_data.sound_environments_tag_block.count > 0:
                scenario_cluster_data.sound_environments_header = TAG.TagBlockHeader().read(input_stream, TAG)
                sound_environments_node = tag_format.get_xml_node(XML_OUTPUT, scenario_cluster_data.sound_environments_tag_block.count, scenario_cluster_data_element_node, "name", "sound environments")
                for sound_environment_idx in range(scenario_cluster_data.sound_environments_tag_block.count):
                    sound_environment_element_node = None
                    if XML_OUTPUT:
                        sound_environment_element_node = TAG.xml_doc.createElement('element')
                        sound_environment_element_node.setAttribute('index', str(sound_environment_idx))
                        sound_environments_node.appendChild(sound_environment_element_node)

                    sound_environment_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(sound_environment_element_node, "type", None, SCENARIO.scenario_body.sound_environment_palette_tag_block.count, "structure_bsp_sound_environment_palette_block"))
                    input_stream.read(2) # Padding

                    scenario_cluster_data.sound_environments.append(sound_environment_index)

            if scenario_cluster_data.cluster_centroids_tag_block.count > 0:
                scenario_cluster_data.cluster_centroids_header = TAG.TagBlockHeader().read(input_stream, TAG)
                cluster_centroids_node = tag_format.get_xml_node(XML_OUTPUT, scenario_cluster_data.cluster_centroids_tag_block.count, scenario_cluster_data_element_node, "name", "cluster centroids")
                for cluster_centroid_idx in range(scenario_cluster_data.cluster_centroids_tag_block.count):
                    cluster_centroid_element_node = None
                    if XML_OUTPUT:
                        cluster_centroid_element_node = TAG.xml_doc.createElement('element')
                        cluster_centroid_element_node.setAttribute('index', str(cluster_centroid_idx))
                        cluster_centroids_node.appendChild(cluster_centroid_element_node)

                    centroid = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(cluster_centroid_element_node, "centroid"))

                    scenario_cluster_data.cluster_centroids.append(centroid)

            if scenario_cluster_data.weather_properties_tag_block.count > 0:
                scenario_cluster_data.weather_properties_header = TAG.TagBlockHeader().read(input_stream, TAG)
                weather_properties_node = tag_format.get_xml_node(XML_OUTPUT, scenario_cluster_data.weather_properties_tag_block.count, scenario_cluster_data_element_node, "name", "weather properties")
                for weather_property_idx in range(scenario_cluster_data.weather_properties_tag_block.count):
                    weather_property_element_node = None
                    if XML_OUTPUT:
                        weather_property_element_node = TAG.xml_doc.createElement('element')
                        weather_property_element_node.setAttribute('index', str(weather_property_idx))
                        weather_properties_node.appendChild(weather_property_element_node)

                    weather_property_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(weather_property_element_node, "type", None, SCENARIO.scenario_body.weather_palette_tag_block.count, "structure_bsp_weather_palette_block"))
                    input_stream.read(2) # Padding

                    scenario_cluster_data.weather_properties.append(weather_property_index)

            if scenario_cluster_data.atmospheric_fog_properties_tag_block.count > 0:
                scenario_cluster_data.atmospheric_fog_properties_header = TAG.TagBlockHeader().read(input_stream, TAG)
                atmospheric_fog_properties_node = tag_format.get_xml_node(XML_OUTPUT, scenario_cluster_data.atmospheric_fog_properties_tag_block.count, scenario_cluster_data_element_node, "name", "atmospheric fog properties")
                for atmospheric_fog_property_idx in range(scenario_cluster_data.atmospheric_fog_properties_tag_block.count):
                    atmospheric_fog_property_element_node = None
                    if XML_OUTPUT:
                        atmospheric_fog_property_element_node = TAG.xml_doc.createElement('element')
                        atmospheric_fog_property_element_node.setAttribute('index', str(atmospheric_fog_property_idx))
                        atmospheric_fog_properties_node.appendChild(atmospheric_fog_property_element_node)

                    atmospheric_fog_property_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(atmospheric_fog_property_element_node, "type", None, SCENARIO.scenario_body.atmospheric_fog_palette_tag_block.count, "scenario_atmospheric_fog_palette"))
                    input_stream.read(2) # Padding

                    scenario_cluster_data.atmospheric_fog_properties.append(atmospheric_fog_property_index)

def read_spawn_data(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.spawn_data_tag_block.count > 0:
        SCENARIO.spawn_data_header = TAG.TagBlockHeader().read(input_stream, TAG)
        spawn_data_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.spawn_data_tag_block.count, tag_node, "name", "spawn data")
        for spawn_data_idx in range(SCENARIO.scenario_body.spawn_data_tag_block.count):
            spawn_data_element_node = None
            if XML_OUTPUT:
                spawn_data_element_node = TAG.xml_doc.createElement('element')
                spawn_data_element_node.setAttribute('index', str(spawn_data_idx))
                spawn_data_node.appendChild(spawn_data_element_node)

            spawn_data = SCENARIO.SpawnData()
            spawn_data.dynamic_spawn_lower_height = TAG.read_float(input_stream, TAG, tag_format.XMLData(spawn_data_element_node, "dynamic spawn lower height"))
            spawn_data.dynamic_spawn_upper_height = TAG.read_float(input_stream, TAG, tag_format.XMLData(spawn_data_element_node, "dynamic spawn upper height"))
            spawn_data.game_object_reset_height = TAG.read_float(input_stream, TAG, tag_format.XMLData(spawn_data_element_node, "game object reset height"))
            input_stream.read(60) # Padding?
            spawn_data.dynamic_spawn_overloads_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(spawn_data_element_node, "dynamic spawn overloads"))
            spawn_data.static_respawn_zones_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(spawn_data_element_node, "static respawn zones"))
            spawn_data.static_initial_spawn_zones_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(spawn_data_element_node, "static initial spawn zones"))

            SCENARIO.spawn_data.append(spawn_data)

        for spawn_data_idx, spawn_data in enumerate(SCENARIO.spawn_data):
            spawn_data_element_node = None
            if XML_OUTPUT:
                spawn_data_element_node = spawn_data_node.childNodes[spawn_data_idx]

            spawn_data.dynamic_spawn_overloads = []
            spawn_data.static_respawn_zones = []
            spawn_data.static_initial_spawn_zones = []
            if spawn_data.dynamic_spawn_overloads_tag_block.count > 0:
                spawn_data.dynamic_spawn_overloads_header = TAG.TagBlockHeader().read(input_stream, TAG)
                dynamic_spawn_overloads_node = tag_format.get_xml_node(XML_OUTPUT, spawn_data.dynamic_spawn_overloads_tag_block.count, spawn_data_element_node, "name", "dynamic spawn overloads")
                for dynamic_spawn_overload_idx in range(spawn_data.dynamic_spawn_overloads_tag_block.count):
                    dynamic_spawn_overload_element_node = None
                    if XML_OUTPUT:
                        dynamic_spawn_overload_element_node = TAG.xml_doc.createElement('element')
                        dynamic_spawn_overload_element_node.setAttribute('index', str(dynamic_spawn_overload_idx))
                        dynamic_spawn_overloads_node.appendChild(dynamic_spawn_overload_element_node)

                    dynamic_spawn_overload = SCENARIO.DynamicSpawnOverload()
                    dynamic_spawn_overload.overload_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(dynamic_spawn_overload_element_node, "overload type", OverloadTypeEnum))
                    input_stream.read(2) # Padding
                    dynamic_spawn_overload.inner_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(dynamic_spawn_overload_element_node, "inner radius"))
                    dynamic_spawn_overload.outer_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(dynamic_spawn_overload_element_node, "outer radius"))
                    dynamic_spawn_overload.weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(dynamic_spawn_overload_element_node, "weight"))

                    spawn_data.dynamic_spawn_overloads.append(dynamic_spawn_overload)

            if spawn_data.static_respawn_zones_tag_block.count > 0:
                spawn_data.static_respawn_zones_header = TAG.TagBlockHeader().read(input_stream, TAG)
                static_respawn_zones_node = tag_format.get_xml_node(XML_OUTPUT, spawn_data.static_respawn_zones_tag_block.count, spawn_data_element_node, "name", "static respawn zones")
                for static_respawn_zone_idx in range(spawn_data.static_respawn_zones_tag_block.count):
                    static_respawn_zone_element_node = None
                    if XML_OUTPUT:
                        static_respawn_zone_element_node = TAG.xml_doc.createElement('element')
                        static_respawn_zone_element_node.setAttribute('index', str(static_respawn_zone_idx))
                        static_respawn_zones_node.appendChild(static_respawn_zone_element_node)

                    static_respawn_zone = SCENARIO.StaticSpawnZone()

                    TAG.big_endian = True
                    input_stream.read(2) # Padding?
                    static_respawn_zone.name_length = TAG.read_signed_short(input_stream, TAG)
                    TAG.big_endian = False

                    static_respawn_zone.relevant_teams = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(static_respawn_zone_element_node, "relevant teams", ObjectFlags))
                    static_respawn_zone.relevant_games = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(static_respawn_zone_element_node, "relevant games", ObjectFlags))
                    static_respawn_zone.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(static_respawn_zone_element_node, "flags", ObjectFlags))
                    static_respawn_zone.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(static_respawn_zone_element_node, "position"))
                    static_respawn_zone.lower_height = TAG.read_float(input_stream, TAG, tag_format.XMLData(static_respawn_zone_element_node, "lower_height"))
                    static_respawn_zone.upper_height = TAG.read_float(input_stream, TAG, tag_format.XMLData(static_respawn_zone_element_node, "upper_height"))
                    static_respawn_zone.inner_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(static_respawn_zone_element_node, "inner radius"))
                    static_respawn_zone.outer_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(static_respawn_zone_element_node, "outer_radius"))
                    static_respawn_zone.weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(static_respawn_zone_element_node, "weight"))

                    spawn_data.static_respawn_zones.append(static_respawn_zone)

                for static_respawn_zone_idx, static_respawn_zone in enumerate(spawn_data.static_respawn_zones):
                    static_respawn_zone_element_node = None
                    if XML_OUTPUT:
                        static_respawn_zone_element_node = static_respawn_zones_node.childNodes[static_respawn_zone_idx]

                    static_respawn_zone.sszd_header = TAG.TagBlockHeader().read(input_stream, TAG)
                    spawn_name_length = static_respawn_zone.name_length
                    if spawn_name_length > 0:
                        static_respawn_zone.variant_name = TAG.read_variable_string_no_terminator(input_stream, spawn_name_length, TAG, tag_format.XMLData(static_respawn_zone_element_node, "name"))

            if spawn_data.static_initial_spawn_zones_tag_block.count > 0:
                spawn_data.static_initial_spawn_zones_header = TAG.TagBlockHeader().read(input_stream, TAG)
                static_initial_spawn_zones_node = tag_format.get_xml_node(XML_OUTPUT, spawn_data.static_initial_spawn_zones_tag_block.count, spawn_data_element_node, "name", "static initial spawn zones")
                for static_initial_spawn_zone_idx in range(spawn_data.static_initial_spawn_zones_tag_block.count):
                    static_initial_spawn_zone_element_node = None
                    if XML_OUTPUT:
                        static_initial_spawn_zone_element_node = TAG.xml_doc.createElement('element')
                        static_initial_spawn_zone_element_node.setAttribute('index', str(static_initial_spawn_zone_idx))
                        static_initial_spawn_zones_node.appendChild(static_initial_spawn_zone_element_node)

                    static_initial_spawn_zone = SCENARIO.StaticSpawnZone()

                    TAG.big_endian = True
                    input_stream.read(2) # Padding?
                    static_initial_spawn_zone.name_length = TAG.read_signed_short(input_stream, TAG)
                    TAG.big_endian = False

                    static_initial_spawn_zone.relevant_teams = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(static_initial_spawn_zone_element_node, "relevant teams", RelevantTeamFlags))
                    static_initial_spawn_zone.relevant_games = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(static_initial_spawn_zone_element_node, "relevant games", RelevantGamesFlags))
                    static_initial_spawn_zone.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(static_initial_spawn_zone_element_node, "flags", SpawnZoneFlags))
                    static_initial_spawn_zone.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(static_initial_spawn_zone_element_node, "position"))
                    static_initial_spawn_zone.lower_height = TAG.read_float(input_stream, TAG, tag_format.XMLData(static_initial_spawn_zone_element_node, "lower_height"))
                    static_initial_spawn_zone.upper_height = TAG.read_float(input_stream, TAG, tag_format.XMLData(static_initial_spawn_zone_element_node, "upper_height"))
                    static_initial_spawn_zone.inner_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(static_initial_spawn_zone_element_node, "inner radius"))
                    static_initial_spawn_zone.outer_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(static_initial_spawn_zone_element_node, "outer_radius"))
                    static_initial_spawn_zone.weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(static_initial_spawn_zone_element_node, "weight"))

                    spawn_data.static_initial_spawn_zones.append(static_initial_spawn_zone)

                for static_initial_spawn_zone_idx, static_initial_spawn_zone in enumerate(spawn_data.static_initial_spawn_zones):
                    static_initial_spawn_zone_element_node = None
                    if XML_OUTPUT:
                        static_initial_spawn_zone_element_node = static_initial_spawn_zones_node.childNodes[static_initial_spawn_zone_idx]

                    static_initial_spawn_zone.sszd_header = TAG.TagBlockHeader().read(input_stream, TAG)
                    spawn_name_length = static_initial_spawn_zone.name_length
                    if spawn_name_length > 0:
                        static_initial_spawn_zone.variant_name = TAG.read_variable_string_no_terminator(input_stream, spawn_name_length, TAG, tag_format.XMLData(static_initial_spawn_zone_element_node, "name"))

def get_crate(input_stream, SCENARIO, TAG, node_element):
    crate = SCENARIO.Crate()
    object_helper(crate, TAG, input_stream, SCENARIO, node_element, SCENARIO.scenario_body.crate_palette_tag_block.count, "scenario_crate_palette_block")

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    crate.variant_name_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    crate.active_change_colors = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "active change colors", ObjectColorChangeFlags))
    crate.primary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "primary color"))
    crate.secondary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "secondary color"))
    crate.tertiary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "tertiary color"))
    crate.quaternary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "quaternary color"))

    return crate

def read_crates(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.crates_tag_block.count > 0:
        SCENARIO.crates_header = TAG.TagBlockHeader().read(input_stream, TAG)
        crates_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.crates_tag_block.count, tag_node, "name", "crates")
        for crate_idx in range(SCENARIO.scenario_body.crates_tag_block.count):
            crate_element_node = None
            if XML_OUTPUT:
                crate_element_node = TAG.xml_doc.createElement('element')
                crate_element_node.setAttribute('index', str(crate_idx))
                crates_node.appendChild(crate_element_node)

            SCENARIO.crates.append(get_crate(input_stream, SCENARIO, TAG, crate_element_node))

        for crate_idx, crate in enumerate(SCENARIO.crates):
            crate_element_node = None
            if XML_OUTPUT:
                crate_element_node = crates_node.childNodes[crate_idx]

            crate.sobj_header = TAG.TagBlockHeader().read(input_stream, TAG)
            crate.obj0_header = TAG.TagBlockHeader().read(input_stream, TAG)
            crate.sper_header = TAG.TagBlockHeader().read(input_stream, TAG)
            if crate.variant_name_length > 0:
                crate.variant_name = TAG.read_variable_string_no_terminator(input_stream, crate.variant_name_length, TAG, tag_format.XMLData(crate_element_node, "variant name"))

    palette_helper(input_stream, SCENARIO.scenario_body.crate_palette_tag_block.count, "crate palette", SCENARIO.crates_palette_header, SCENARIO.crates_palette, tag_node, TAG)

def read_atmospheric_fog_palette(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT):
    if SCENARIO.scenario_body.atmospheric_fog_palette_tag_block.count > 0:
        SCENARIO.atmospheric_fog_palette_header = TAG.TagBlockHeader().read(input_stream, TAG)
        atmospheric_fog_palette_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.atmospheric_fog_palette_tag_block.count, tag_node, "name", "atmospheric fog palette")
        for atmospheric_fog_palette_idx in range(SCENARIO.scenario_body.atmospheric_fog_palette_tag_block.count):
            atmospheric_fog_palette_element_node = None
            if XML_OUTPUT:
                atmospheric_fog_palette_element_node = TAG.xml_doc.createElement('element')
                atmospheric_fog_palette_element_node.setAttribute('index', str(atmospheric_fog_palette_idx))
                atmospheric_fog_palette_node.appendChild(atmospheric_fog_palette_element_node)

            atmospheric_fog_palette = SCENARIO.AtmosphericFogPalette()

            TAG.big_endian = True
            input_stream.read(2) # Padding?
            atmospheric_fog_palette.name_length = TAG.read_signed_short(input_stream, TAG)
            TAG.big_endian = False

            atmospheric_fog_palette.atmospheric_fog_color_RGBA = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "color"))
            atmospheric_fog_palette.atmospheric_fog_spread_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "spread distance"))
            input_stream.read(4) # Padding?
            atmospheric_fog_palette.atmospheric_fog_maximum_density = TAG.read_float(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "maximum density"))
            atmospheric_fog_palette.atmospheric_fog_start_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "start distance"))
            atmospheric_fog_palette.atmospheric_fog_opaque_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "opaque distance"))
            atmospheric_fog_palette.secondary_fog_color_RGBA = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "color"))
            input_stream.read(4) # Padding?
            atmospheric_fog_palette.secondary_fog_maximum_density = TAG.read_float(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "maximum density"))
            atmospheric_fog_palette.secondary_fog_start_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "start distance"))
            atmospheric_fog_palette.secondary_fog_opaque_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "opaque distance"))
            input_stream.read(4) # Padding?
            atmospheric_fog_palette.planar_color_RGBA = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "planar color"))
            input_stream.read(4) # Padding?
            atmospheric_fog_palette.planar_max_density = TAG.read_float(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "planar max density"))
            atmospheric_fog_palette.planar_override_amount = TAG.read_float(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "planar override amount"))
            atmospheric_fog_palette.planar_min_distance_bias = TAG.read_float(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "planar min distance bias"))
            input_stream.read(44) # Padding?
            atmospheric_fog_palette.patchy_color_RGBA = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "planar color"))
            input_stream.read(8) # Padding?
            atmospheric_fog_palette.patchy_density = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "patchy density"))
            atmospheric_fog_palette.patchy_distance = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "patchy distance"))
            input_stream.read(32) # Padding?
            atmospheric_fog_palette.patchy_fog = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "patchy fog"))
            atmospheric_fog_palette.mixers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "mixers"))
            atmospheric_fog_palette.amount = TAG.read_float(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "planar max density"))
            atmospheric_fog_palette.threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "planar max density"))
            atmospheric_fog_palette.brightness = TAG.read_float(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "planar max density"))
            atmospheric_fog_palette.gamma_power = TAG.read_float(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "planar max density"))
            atmospheric_fog_palette.camera_immersion_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "camera immersion flags", CameraImmersionFlags))
            input_stream.read(2) # Padding?

            SCENARIO.atmospheric_fog_palette.append(atmospheric_fog_palette)

        for atmospheric_fog_palette_idx, atmospheric_fog_palette in enumerate(SCENARIO.atmospheric_fog_palette):
            atmospheric_fog_palette_element_node = None
            if XML_OUTPUT:
                atmospheric_fog_palette_element_node = atmospheric_fog_palette_node.childNodes[atmospheric_fog_palette_idx]

            name_length = atmospheric_fog_palette.name_length
            if name_length > 0:
                atmospheric_fog_palette.name = TAG.read_variable_string_no_terminator(input_stream, name_length, TAG, tag_format.XMLData(atmospheric_fog_palette_element_node, "name"))

            patchy_fog_name_length = atmospheric_fog_palette.patchy_fog.name_length
            if patchy_fog_name_length > 0:
                atmospheric_fog_palette.patchy_fog.name = TAG.read_variable_string(input_stream, patchy_fog_name_length, TAG)

            if XML_OUTPUT:
                patchy_fog_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, atmospheric_fog_palette_element_node, "name", "patchy fog")
                atmospheric_fog_palette.patchy_fog.append_xml_attributes(patchy_fog_tag_ref_node)

            atmospheric_fog_palette.mixers = []
            if atmospheric_fog_palette.mixers_tag_block.count > 0:
                atmospheric_fog_palette.mixers_header = TAG.TagBlockHeader().read(input_stream, TAG)
                mixers_node = tag_format.get_xml_node(XML_OUTPUT, atmospheric_fog_palette.mixers_tag_block.count, atmospheric_fog_palette_element_node, "name", "mixers")
                for mixer_idx in range(atmospheric_fog_palette.mixers_tag_block.count):
                    mixer_element_node = None
                    if XML_OUTPUT:
                        mixer_element_node = TAG.xml_doc.createElement('element')
                        mixer_element_node.setAttribute('index', str(mixer_idx))
                        mixers_node.appendChild(mixer_element_node)

                    mixer = SCENARIO.Mixer()

                    input_stream.read(4) # Padding?
                    TAG.big_endian = True
                    input_stream.read(2) # Padding?
                    mixer.atmospheric_fog_source_length = TAG.read_signed_short(input_stream, TAG)
                    input_stream.read(2) # Padding?
                    mixer.interpolator_length = TAG.read_signed_short(input_stream, TAG)
                    TAG.big_endian = False
                    input_stream.read(4) # Padding?

                    atmospheric_fog_palette.mixers.append(mixer)

                for mixer_idx, mixer in enumerate(atmospheric_fog_palette.mixers):
                    mixer_element_node = None
                    if XML_OUTPUT:
                        mixer_element_node = mixers_node.childNodes[mixer_idx]

                    atmospheric_fog_length = mixer.atmospheric_fog_source_length
                    interpolator_length = mixer.interpolator_length
                    if atmospheric_fog_length > 0:
                        mixer.atmospheric_fog_source = TAG.read_variable_string_no_terminator(input_stream, atmospheric_fog_length, TAG, tag_format.XMLData(mixer_element_node, "atmospheric fog source"))

                    if interpolator_length > 0:
                        mixer.interpolator = TAG.read_variable_string_no_terminator(input_stream, interpolator_length, TAG, tag_format.XMLData(mixer_element_node, "interpolator"))

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    SCENARIO = ScenarioAsset()
    TAG.is_legacy = False
    TAG.big_endian = False
    tag_node = None
    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    SCENARIO.header = TAG.Header().read(input_stream, TAG)
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    initilize_scenario(SCENARIO)
    read_scenario_body(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    unused_tag_ref = SCENARIO.scenario_body.unused_tag_ref
    custom_object_names_tag_ref = SCENARIO.scenario_body.custom_object_names_tag_ref
    chapter_title_text_tag_ref = SCENARIO.scenario_body.chapter_title_text_tag_ref
    hud_messages_tag_ref = SCENARIO.scenario_body.hud_messages_tag_ref
    sound_effect_collection_tag_ref = SCENARIO.scenario_body.sound_effect_collection_tag_ref
    global_lighting_tag_ref = SCENARIO.scenario_body.global_lighting_tag_ref
    unused_name_length = unused_tag_ref.name_length
    custom_object_names_name_length = custom_object_names_tag_ref.name_length
    chapter_title_text_name_length = chapter_title_text_tag_ref.name_length
    hud_messages_name_length = hud_messages_tag_ref.name_length
    sound_effect_collection_name_length = sound_effect_collection_tag_ref.name_length
    global_lighting_name_length = global_lighting_tag_ref.name_length
    if unused_name_length > 0:
        unused_tag_ref.name = TAG.read_variable_string(input_stream, unused_name_length, TAG)

    read_skies(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_child_scenarios(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_predicted_resources(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    SCENARIO.editor_scenario_data = input_stream.read(SCENARIO.scenario_body.editor_scenario_data.size)
    read_comments(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_environment_objects(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_object_names(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_scenery(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_bipeds(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_vehicles(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_equipment(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_weapon(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_device_groups(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_machines(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_controls(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_light_fixtures(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_sound_scenery(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_light_volumes(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_player_starting_profiles(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_player_starting_locations(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_trigger_volumes(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_recorded_animations(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_netgame_flags(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_netgame_equipment(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_starting_equipment(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_bsp_switch_trigger_volumes(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_decals(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_decal_palette(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_detail_object_collection_palette(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_style_palette(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_squad_groups(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_squads(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_zones(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_mission_scenes(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_character_palette(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_ai_pathfinding_data(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_ai_animation_references(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_ai_script_references(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_ai_recording_references(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_ai_conversations(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    SCENARIO.script_syntax_data = input_stream.read(SCENARIO.scenario_body.script_syntax_data_tag_data.size)
    SCENARIO.script_string_data = input_stream.read(SCENARIO.scenario_body.script_string_data_tag_data.size)
    read_scripts(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_globals(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_references(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_source_files(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_scripting_data(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_cutscene_flags(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_cutscene_camera_points(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_cutscene_titles(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    if custom_object_names_name_length > 0:
        custom_object_names_tag_ref.name = TAG.read_variable_string(input_stream, custom_object_names_name_length, TAG)

    if chapter_title_text_name_length > 0:
        chapter_title_text_tag_ref.name = TAG.read_variable_string(input_stream, chapter_title_text_name_length, TAG)

    if hud_messages_name_length > 0:
        hud_messages_tag_ref.name = TAG.read_variable_string(input_stream, hud_messages_name_length, TAG)

    read_structure_bsps(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_scenario_resoruces(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_old_structure_physics(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_hs_unit_seats(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_scenario_kill_triggers(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_hs_syntax_datum(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_orders(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_triggers(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_background_sound_palette(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_sound_environment_palette(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_weather_palette(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_scavenger_hunt_objects(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_scenario_cluster_data(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    read_spawn_data(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    if sound_effect_collection_name_length > 0:
        sound_effect_collection_tag_ref.name = TAG.read_variable_string(input_stream, sound_effect_collection_name_length, TAG)

    read_crates(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)
    if global_lighting_name_length > 0:
        global_lighting_tag_ref.name = TAG.read_variable_string(input_stream, global_lighting_name_length, TAG)

    read_atmospheric_fog_palette(SCENARIO, TAG, input_stream, tag_node, XML_OUTPUT)

    if XML_OUTPUT:
        unused_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "unused")
        custom_object_names_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "custom object names")
        chapter_title_text_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "chapter title text")
        hud_messages_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "hud messages")
        sound_effect_collection_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "sound effect collection")
        global_lighting_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "global lighting")
        unused_tag_ref.append_xml_attributes(unused_node)
        custom_object_names_tag_ref.append_xml_attributes(custom_object_names_node)
        chapter_title_text_tag_ref.append_xml_attributes(chapter_title_text_node)
        hud_messages_tag_ref.append_xml_attributes(hud_messages_node)
        sound_effect_collection_tag_ref.append_xml_attributes(sound_effect_collection_node)
        global_lighting_tag_ref.append_xml_attributes(global_lighting_node)


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
