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

import struct

from math import radians
from ....global_functions import tag_format

def write_body(output_stream, SCENARIO):
    SCENARIO.scenario_body.dont_use_tag_ref.write(output_stream, True)
    SCENARIO.scenario_body.wont_use_tag_ref.write(output_stream, True)
    SCENARIO.scenario_body.cant_use_tag_ref.write(output_stream, True)
    SCENARIO.scenario_body.skies_tag_block.write(output_stream, True)
    output_stream.write(struct.pack('>HH', SCENARIO.scenario_body.scenario_type, SCENARIO.scenario_body.scenario_flags))
    SCENARIO.scenario_body.child_scenarios_tag_block.write(output_stream, True)
    output_stream.write(struct.pack('>f', radians(SCENARIO.scenario_body.local_north)))
    output_stream.write(struct.pack('>156x'))
    SCENARIO.scenario_body.predicted_resources_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.functions_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.editor_scenario_data.write(output_stream, True)
    SCENARIO.scenario_body.comments_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.scavenger_hunt_objects_tag_block.write(output_stream, True)
    output_stream.write(struct.pack('>212x'))
    SCENARIO.scenario_body.object_names_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.scenery_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.scenery_palette_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.bipeds_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.biped_palette_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.vehicles_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.vehicle_palette_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.equipment_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.equipment_palette_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.weapons_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.weapon_palette_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.device_groups_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.machines_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.machine_palette_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.controls_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.control_palette_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.light_fixtures_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.light_fixtures_palette_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.sound_scenery_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.sound_scenery_palette_tag_block.write(output_stream, True)
    output_stream.write(struct.pack('>84x'))
    SCENARIO.scenario_body.player_starting_profile_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.player_starting_locations_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.trigger_volumes_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.recorded_animations_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.netgame_flags_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.netgame_equipment_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.starting_equipment_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.bsp_switch_trigger_volumes_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.decals_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.decal_palette_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.detail_object_collection_palette_tag_block.write(output_stream, True)
    output_stream.write(struct.pack('>84x'))
    SCENARIO.scenario_body.actor_palette_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.encounters_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.command_lists_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.ai_animation_references_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.ai_script_references_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.ai_recording_references_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.ai_conversations_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.script_syntax_data_tag_data.write(output_stream, True)
    SCENARIO.scenario_body.script_string_data_tag_data.write(output_stream, True)
    SCENARIO.scenario_body.scripts_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.globals_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.references_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.source_files_tag_block.write(output_stream, True)
    output_stream.write(struct.pack('>24x'))
    SCENARIO.scenario_body.cutscene_flags_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.cutscene_camera_points_tag_block.write(output_stream, True)
    SCENARIO.scenario_body.cutscene_titles_tag_block.write(output_stream, True)
    output_stream.write(struct.pack('>108x'))
    SCENARIO.scenario_body.custom_object_names_tag_ref.write(output_stream, True)
    SCENARIO.scenario_body.chapter_title_text_tag_ref.write(output_stream, True)
    SCENARIO.scenario_body.hud_messages_tag_ref.write(output_stream, True)
    SCENARIO.scenario_body.structure_bsps_tag_block.write(output_stream, True)

def write_predicted_resources(output_stream, SCENARIO):
    for predicted_resource_element in SCENARIO.predicted_resources:
        output_stream.write(struct.pack('>h', predicted_resource_element.tag_type))
        output_stream.write(struct.pack('>h', predicted_resource_element.resource_index))
        output_stream.write(struct.pack('>i', predicted_resource_element.tag_index))

def write_functions(output_stream, SCENARIO):
    for function_element in SCENARIO.functions:
        output_stream.write(struct.pack('>2x'))
        output_stream.write(struct.pack('>h', function_element.flags))
        output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(function_element.name, False)))
        output_stream.write(struct.pack('>f', function_element.period))
        output_stream.write(struct.pack('>h', function_element.scale_period_by))
        output_stream.write(struct.pack('>h', function_element.function_type))
        output_stream.write(struct.pack('>h', function_element.scale_function_by))
        output_stream.write(struct.pack('>h', function_element.wobble_function_type))
        output_stream.write(struct.pack('>f', function_element.wobble_period))
        output_stream.write(struct.pack('>f', function_element.wobble_magnitude))
        output_stream.write(struct.pack('>f', function_element.square_wave_threshold))
        output_stream.write(struct.pack('>h', function_element.step_count))
        output_stream.write(struct.pack('>h', function_element.map_to))
        output_stream.write(struct.pack('>h', function_element.sawtooth_count))
        output_stream.write(struct.pack('>2x'))
        output_stream.write(struct.pack('>h', function_element.scale_result_by))
        output_stream.write(struct.pack('>h', function_element.bounds_mode))
        output_stream.write(struct.pack('>ff', function_element.bounds[0], function_element.bounds[1]))
        output_stream.write(struct.pack('>6x'))
        output_stream.write(struct.pack('>h', function_element.turn_off_with))
        output_stream.write(struct.pack('>32x'))

def write_comments(output_stream, comment_tag_block):
    for comment_element in comment_tag_block:
        output_stream.write(struct.pack('>fff', comment_element.position[0], comment_element.position[1], comment_element.position[2]))
        output_stream.write(struct.pack('>16x'))
        comment_element.data.write(output_stream, True)
        output_stream.write(struct.pack('>%ssx' % len(comment_element.text), tag_format.string_to_bytes(comment_element.text, False)))

def write_scavenger_hunt_objects(output_stream, SCENARIO):
    for scavenger_hunt_object_element in SCENARIO.scavenger_hunt_objects:
        output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(scavenger_hunt_object_element.exported_name, False)))
        output_stream.write(struct.pack('>h', scavenger_hunt_object_element.scenario_object_name_index))
        output_stream.write(struct.pack('>2x'))

def write_object_names(output_stream, SCENARIO):
    for object_name in SCENARIO.object_names:
        output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(object_name.name, False)))
        output_stream.write(struct.pack('>4x'))

def write_object(output_stream, scenery_element):
    output_stream.write(struct.pack('>h', scenery_element.type_index))
    output_stream.write(struct.pack('>h', scenery_element.name_index))
    output_stream.write(struct.pack('>h', scenery_element.placement_flags))
    output_stream.write(struct.pack('>h', scenery_element.desired_permutation))
    output_stream.write(struct.pack('>fff', scenery_element.position[0], scenery_element.position[1], scenery_element.position[2]))
    output_stream.write(struct.pack('>fff', radians(scenery_element.rotation[0]), radians(scenery_element.rotation[1]), radians(scenery_element.rotation[2])))

def write_scenery(output_stream, SCENARIO):
    for scenery_element in SCENARIO.scenery:
        write_object(output_stream, scenery_element)
        output_stream.write(struct.pack('>4x'))
        output_stream.write(struct.pack('>b', scenery_element.appearance_player_index))
        output_stream.write(struct.pack('>35x'))

def write_bipeds(output_stream, SCENARIO):
    for biped_element in SCENARIO.bipeds:
        write_object(output_stream, biped_element)
        output_stream.write(struct.pack('>4x'))
        output_stream.write(struct.pack('>b', biped_element.appearance_player_index))
        output_stream.write(struct.pack('>35x'))
        output_stream.write(struct.pack('>f', biped_element.body_vitality))
        output_stream.write(struct.pack('>I', biped_element.flags))
        output_stream.write(struct.pack('>40x'))

def write_vehicles(output_stream, SCENARIO):
    for vehicle_element in SCENARIO.vehicles:
        write_object(output_stream, vehicle_element)
        output_stream.write(struct.pack('>4x'))
        output_stream.write(struct.pack('>b', vehicle_element.appearance_player_index))
        output_stream.write(struct.pack('>35x'))
        output_stream.write(struct.pack('>f', vehicle_element.body_vitality))
        output_stream.write(struct.pack('>2x'))
        output_stream.write(struct.pack('>h', vehicle_element.flags))
        output_stream.write(struct.pack('>8x'))
        output_stream.write(struct.pack('>b', vehicle_element.multiplayer_team_index))
        output_stream.write(struct.pack('>1x'))
        output_stream.write(struct.pack('>H', vehicle_element.multiplayer_spawn_flags))
        output_stream.write(struct.pack('>28x'))

def write_equipment(output_stream, SCENARIO):
    for equipment_element in SCENARIO.equipment:
        write_object(output_stream, equipment_element)
        output_stream.write(struct.pack('>I', equipment_element.misc_flags))
        output_stream.write(struct.pack('>b', equipment_element.appearance_player_index))
        output_stream.write(struct.pack('>3x'))

def write_weapons(output_stream, SCENARIO):
    for weapon_element in SCENARIO.weapons:
        write_object(output_stream, weapon_element)
        output_stream.write(struct.pack('>4x'))
        output_stream.write(struct.pack('>b', weapon_element.appearance_player_index))
        output_stream.write(struct.pack('>35x'))
        output_stream.write(struct.pack('>h', weapon_element.rounds_left))
        output_stream.write(struct.pack('>h', weapon_element.rounds_loaded))
        output_stream.write(struct.pack('>h', weapon_element.flags))
        output_stream.write(struct.pack('>14x'))

def write_device_groups(output_stream, device_group_tag_block):
    for device_group_element in device_group_tag_block:
        output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(device_group_element.name, False)))
        output_stream.write(struct.pack('>f', device_group_element.initial_value))
        output_stream.write(struct.pack('>I', device_group_element.flags))
        output_stream.write(struct.pack('>12x'))

def write_machines(output_stream, SCENARIO):
    for device_machine_element in SCENARIO.device_machines:
        write_object(output_stream, device_machine_element)
        output_stream.write(struct.pack('>4x'))
        output_stream.write(struct.pack('>b', device_machine_element.appearance_player_index))
        output_stream.write(struct.pack('>3x'))
        output_stream.write(struct.pack('>h', device_machine_element.power_group_index))
        output_stream.write(struct.pack('>h', device_machine_element.position_group_index))
        output_stream.write(struct.pack('>I', device_machine_element.flags_0))
        output_stream.write(struct.pack('>I', device_machine_element.flags_1))
        output_stream.write(struct.pack('>12x'))

def write_device_controls(output_stream, SCENARIO):
    for device_control_element in SCENARIO.device_controls:
        write_object(output_stream, device_control_element)
        output_stream.write(struct.pack('>4x'))
        output_stream.write(struct.pack('>b', device_control_element.appearance_player_index))
        output_stream.write(struct.pack('>3x'))
        output_stream.write(struct.pack('>h', device_control_element.power_group_index))
        output_stream.write(struct.pack('>h', device_control_element.position_group_index))
        output_stream.write(struct.pack('>I', device_control_element.flags_0))
        output_stream.write(struct.pack('>I', device_control_element.flags_1))
        output_stream.write(struct.pack('>h', device_control_element.unknown))
        output_stream.write(struct.pack('>10x'))

def write_device_light_fixtures(output_stream, SCENARIO):
    for device_light_fixture_element in SCENARIO.device_light_fixtures:
        write_object(output_stream, device_light_fixture_element)
        output_stream.write(struct.pack('>4x'))
        output_stream.write(struct.pack('>b', device_light_fixture_element.appearance_player_index))
        output_stream.write(struct.pack('>3x'))
        output_stream.write(struct.pack('>h', device_light_fixture_element.power_group_index))
        output_stream.write(struct.pack('>h', device_light_fixture_element.position_group_index))
        output_stream.write(struct.pack('>I', device_light_fixture_element.flags))
        output_stream.write(struct.pack('>fff', device_light_fixture_element.color_RGBA[0], device_light_fixture_element.color_RGBA[1], device_light_fixture_element.color_RGBA[2]))
        output_stream.write(struct.pack('>f', device_light_fixture_element.intensity))
        output_stream.write(struct.pack('>f', device_light_fixture_element.falloff_angle))
        output_stream.write(struct.pack('>f', device_light_fixture_element.cutoff_angle))
        output_stream.write(struct.pack('>16x'))

def write_sound_scenery(output_stream, SCENARIO):
    for sound_scenery_element in SCENARIO.sound_scenery:
        write_object(output_stream, sound_scenery_element)
        output_stream.write(struct.pack('>4x'))
        output_stream.write(struct.pack('>b', sound_scenery_element.appearance_player_index))
        output_stream.write(struct.pack('>3x'))

def write_player_starting_profiles(output_stream, SCENARIO, TAG):
    for player_starting_profile_element in SCENARIO.player_starting_profiles:
        output_stream.write(struct.pack('>31sx', TAG.string_to_bytes(player_starting_profile_element.name, False)))
        output_stream.write(struct.pack('>f', player_starting_profile_element.starting_health_damage))
        output_stream.write(struct.pack('>f', player_starting_profile_element.starting_shield_damage))
        player_starting_profile_element.primary_weapon_tag_ref.write(output_stream, True, False)
        output_stream.write(struct.pack('>h', player_starting_profile_element.primary_rounds_loaded))
        output_stream.write(struct.pack('>h', player_starting_profile_element.primary_rounds_total))
        player_starting_profile_element.secondary_weapon_tag_ref.write(output_stream, True, False)
        output_stream.write(struct.pack('>h', player_starting_profile_element.secondary_rounds_loaded))
        output_stream.write(struct.pack('>h', player_starting_profile_element.secondary_rounds_total))
        output_stream.write(struct.pack('>b', player_starting_profile_element.starting_fragmentation_grenades_count))
        output_stream.write(struct.pack('>b', player_starting_profile_element.starting_plasma_grenade_count))
        output_stream.write(struct.pack('>b', player_starting_profile_element.starting_grenade_type2_count))
        output_stream.write(struct.pack('>b', player_starting_profile_element.starting_grenade_type3_count))
        output_stream.write(struct.pack('>20x'))

    for player_starting_profile_element in SCENARIO.player_starting_profiles:
        primary_weapon_name_length = len(player_starting_profile_element.primary_weapon_tag_ref.name)
        secondary_weapon_name_length = len(player_starting_profile_element.secondary_weapon_tag_ref.name)
        if primary_weapon_name_length > 0:
            output_stream.write(struct.pack('>%ssx' % primary_weapon_name_length, TAG.string_to_bytes(player_starting_profile_element.primary_weapon_tag_ref.name, False)))

        if secondary_weapon_name_length > 0:
            output_stream.write(struct.pack('>%ssx' % secondary_weapon_name_length, TAG.string_to_bytes(player_starting_profile_element.secondary_weapon_tag_ref.name, False)))

def write_player_starting_locations(output_stream, SCENARIO):
    for player_starting_location_element in SCENARIO.player_starting_locations:
        output_stream.write(struct.pack('>fff', player_starting_location_element.position[0], player_starting_location_element.position[1], player_starting_location_element.position[2]))
        output_stream.write(struct.pack('>f', radians(player_starting_location_element.facing)))
        output_stream.write(struct.pack('>h', player_starting_location_element.team_index))
        output_stream.write(struct.pack('>h', player_starting_location_element.bsp_index))
        output_stream.write(struct.pack('>h', player_starting_location_element.type_0))
        output_stream.write(struct.pack('>h', player_starting_location_element.type_1))
        output_stream.write(struct.pack('>h', player_starting_location_element.type_2))
        output_stream.write(struct.pack('>h', player_starting_location_element.type_3))
        output_stream.write(struct.pack('>24x'))

def write_trigger_volumes(output_stream, SCENARIO):
    for trigger_volume_element in SCENARIO.trigger_volumes:
        output_stream.write(struct.pack('<i', 1)) # Rotation flag?
        output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(trigger_volume_element.name, False)))
        output_stream.write(struct.pack('>fff', trigger_volume_element.parameter[0], trigger_volume_element.parameter[1], trigger_volume_element.parameter[2]))
        output_stream.write(struct.pack('>fff', trigger_volume_element.forward[0], trigger_volume_element.forward[1], trigger_volume_element.forward[2]))
        output_stream.write(struct.pack('>fff', trigger_volume_element.up[0], trigger_volume_element.up[1], trigger_volume_element.up[2]))
        output_stream.write(struct.pack('>fff', trigger_volume_element.position[0], trigger_volume_element.position[1], trigger_volume_element.position[2]))
        output_stream.write(struct.pack('>fff', trigger_volume_element.extents[0], trigger_volume_element.extents[1], trigger_volume_element.extents[2]))

def write_recorded_animations(output_stream, SCENARIO):
    for recorded_animation_element in SCENARIO.recorded_animations:
        output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(recorded_animation_element.name, False)))
        output_stream.write(struct.pack('>b', recorded_animation_element.version))
        output_stream.write(struct.pack('>b', recorded_animation_element.raw_animation_data))
        output_stream.write(struct.pack('>b', recorded_animation_element.unit_control_data_version))
        output_stream.write(struct.pack('>x'))
        output_stream.write(struct.pack('>h', recorded_animation_element.length_of_animation))
        output_stream.write(struct.pack('>6x'))
        recorded_animation_element.recorded_animation_event_stream_tag_data.write(output_stream, True)

    for recorded_animation_element in SCENARIO.recorded_animations:
        output_stream.write(recorded_animation_element.recorded_animation_event_stream)

def write_netgame_flags(output_stream, SCENARIO):
    for netgame_flag_element in SCENARIO.netgame_flags:
        output_stream.write(struct.pack('>fff', netgame_flag_element.position[0], netgame_flag_element.position[1], netgame_flag_element.position[2]))
        output_stream.write(struct.pack('>f', radians(netgame_flag_element.facing)))
        output_stream.write(struct.pack('>h', netgame_flag_element.type))
        output_stream.write(struct.pack('>h', netgame_flag_element.usage_id))
        netgame_flag_element.weapon_group.write(output_stream, True, False)
        output_stream.write(struct.pack('>112x'))

    for netgame_flag_element in SCENARIO.netgame_flags:
        weapon_group_name_length = len(netgame_flag_element.weapon_group.name)
        if weapon_group_name_length > 0:
            output_stream.write(struct.pack('>%ssx' % weapon_group_name_length, tag_format.string_to_bytes(netgame_flag_element.weapon_group.name, False)))

def write_netgame_equipment(output_stream, SCENARIO):
    for netgame_equipment_element in SCENARIO.netgame_equipment:
        output_stream.write(struct.pack('>2x'))
        output_stream.write(struct.pack('>h', netgame_equipment_element.flags))
        output_stream.write(struct.pack('>h', netgame_equipment_element.type_0))
        output_stream.write(struct.pack('>h', netgame_equipment_element.type_1))
        output_stream.write(struct.pack('>h', netgame_equipment_element.type_2))
        output_stream.write(struct.pack('>h', netgame_equipment_element.type_3))
        output_stream.write(struct.pack('>h', netgame_equipment_element.team_index))
        output_stream.write(struct.pack('>h', netgame_equipment_element.spawn_time))
        output_stream.write(struct.pack('>48x'))
        output_stream.write(struct.pack('>fff', netgame_equipment_element.position[0], netgame_equipment_element.position[1], netgame_equipment_element.position[2]))
        output_stream.write(struct.pack('>f', radians(netgame_equipment_element.facing)))
        netgame_equipment_element.item_collection.write(output_stream, True, False)
        output_stream.write(struct.pack('>48x'))

    for netgame_equipment_element in SCENARIO.netgame_equipment:
        item_collection_name_length = len(netgame_equipment_element.item_collection.name)
        if item_collection_name_length > 0:
            output_stream.write(struct.pack('>%ssx' % item_collection_name_length, tag_format.string_to_bytes(netgame_equipment_element.item_collection.name, False)))

def write_starting_equipment(output_stream, SCENARIO):
    for starting_equipment_element in SCENARIO.starting_equipment:
        output_stream.write(struct.pack('>2x'))
        output_stream.write(struct.pack('>h', starting_equipment_element.flags))
        output_stream.write(struct.pack('>h', starting_equipment_element.type_0))
        output_stream.write(struct.pack('>h', starting_equipment_element.type_1))
        output_stream.write(struct.pack('>h', starting_equipment_element.type_2))
        output_stream.write(struct.pack('>h', starting_equipment_element.type_3))
        output_stream.write(struct.pack('>48x'))
        starting_equipment_element.item_collection_1.write(output_stream, True, False)
        starting_equipment_element.item_collection_2.write(output_stream, True, False)
        starting_equipment_element.item_collection_3.write(output_stream, True, False)
        starting_equipment_element.item_collection_4.write(output_stream, True, False)
        starting_equipment_element.item_collection_5.write(output_stream, True, False)
        starting_equipment_element.item_collection_6.write(output_stream, True, False)
        output_stream.write(struct.pack('>48x'))

    for starting_equipment_element in SCENARIO.starting_equipment:
        item_collection_1_name_length = len(starting_equipment_element.item_collection_1.name)
        item_collection_2_name_length = len(starting_equipment_element.item_collection_2.name)
        item_collection_3_name_length = len(starting_equipment_element.item_collection_3.name)
        item_collection_4_name_length = len(starting_equipment_element.item_collection_4.name)
        item_collection_5_name_length = len(starting_equipment_element.item_collection_5.name)
        item_collection_6_name_length = len(starting_equipment_element.item_collection_6.name)
        if item_collection_1_name_length > 0:
            output_stream.write(struct.pack('>%ssx' % item_collection_1_name_length, tag_format.string_to_bytes(starting_equipment_element.item_collection_1.name, False)))
        if item_collection_2_name_length > 0:
            output_stream.write(struct.pack('>%ssx' % item_collection_2_name_length, tag_format.string_to_bytes(starting_equipment_element.item_collection_2.name, False)))
        if item_collection_3_name_length > 0:
            output_stream.write(struct.pack('>%ssx' % item_collection_3_name_length, tag_format.string_to_bytes(starting_equipment_element.item_collection_3.name, False)))
        if item_collection_4_name_length > 0:
            output_stream.write(struct.pack('>%ssx' % item_collection_4_name_length, tag_format.string_to_bytes(starting_equipment_element.item_collection_4.name, False)))
        if item_collection_5_name_length > 0:
            output_stream.write(struct.pack('>%ssx' % item_collection_5_name_length, tag_format.string_to_bytes(starting_equipment_element.item_collection_5.name, False)))
        if item_collection_6_name_length > 0:
            output_stream.write(struct.pack('>%ssx' % item_collection_6_name_length, tag_format.string_to_bytes(starting_equipment_element.item_collection_6.name, False)))

def write_bsp_switch_trigger_volumes(output_stream, SCENARIO):
    for bsp_switch_trigger_volume_element in SCENARIO.bsp_switch_trigger_volumes:
        output_stream.write(struct.pack('>h', bsp_switch_trigger_volume_element.trigger_volume))
        output_stream.write(struct.pack('>h', bsp_switch_trigger_volume_element.source))
        output_stream.write(struct.pack('>h', bsp_switch_trigger_volume_element.destination))
        output_stream.write(struct.pack('>2x'))

def write_decals(output_stream, SCENARIO):
    for decal_element in SCENARIO.decals:
        output_stream.write(struct.pack('>h', decal_element.palette_index))
        output_stream.write(struct.pack('>b', decal_element.yaw))
        output_stream.write(struct.pack('>b', decal_element.pitch))
        output_stream.write(struct.pack('>fff', decal_element.position[0], decal_element.position[1], decal_element.position[2]))

def write_encounters(output_stream, SCENARIO):
    for encounter in SCENARIO.encounters:
        output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(encounter.name, False)))
        output_stream.write(struct.pack('>I', encounter.flags))
        output_stream.write(struct.pack('>h', encounter.team_index))
        output_stream.write(struct.pack('>h', 0)) # What is this?
        output_stream.write(struct.pack('>h', encounter.search_behavior))
        output_stream.write(struct.pack('>h', encounter.manual_bsp_index))
        output_stream.write(struct.pack('>ff', encounter.respawn_delay[0], encounter.respawn_delay[1]))
        output_stream.write(struct.pack('>76x'))
        encounter.squads_tag_block.write(output_stream, True)
        encounter.platoons_tag_block.write(output_stream, True)
        encounter.firing_positions_tag_block.write(output_stream, True)
        encounter.player_starting_locations_tag_block.write(output_stream, True)

    for encounter in SCENARIO.encounters:
        for squad in encounter.squads:
            output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(squad.name, False)))
            output_stream.write(struct.pack('>h', squad.actor_type))
            output_stream.write(struct.pack('>h', squad.platoon))
            output_stream.write(struct.pack('>h', squad.initial_state))
            output_stream.write(struct.pack('>h', squad.return_state))
            output_stream.write(struct.pack('>i', squad.flags))
            output_stream.write(struct.pack('>h', squad.unique_leader_type))
            output_stream.write(struct.pack('>32x'))
            output_stream.write(struct.pack('>h', squad.maneuver_to_squad))
            output_stream.write(struct.pack('>f', squad.squad_delay_time))
            output_stream.write(struct.pack('>i', squad.attacking))
            output_stream.write(struct.pack('>i', squad.attacking_search))
            output_stream.write(struct.pack('>i', squad.attacking_guard))
            output_stream.write(struct.pack('>i', squad.defending))
            output_stream.write(struct.pack('>i', squad.defending_search))
            output_stream.write(struct.pack('>i', squad.defending_guard))
            output_stream.write(struct.pack('>i', squad.pursuing))
            output_stream.write(struct.pack('>12x'))
            output_stream.write(struct.pack('>h', squad.normal_diff_count))
            output_stream.write(struct.pack('>h', squad.insane_diff_count))
            output_stream.write(struct.pack('>h', squad.major_upgrade))
            output_stream.write(struct.pack('>2x'))
            output_stream.write(struct.pack('>h', squad.respawn_min_actors))
            output_stream.write(struct.pack('>h', squad.respawn_max_actors))
            output_stream.write(struct.pack('>h', squad.respawn_total))
            output_stream.write(struct.pack('>2x'))
            output_stream.write(struct.pack('>ff', squad.respawn_delay[0], squad.respawn_delay[1]))
            output_stream.write(struct.pack('>48x'))
            squad.move_positions_tag_block.write(output_stream, True)
            squad.starting_locations_tag_block.write(output_stream, True)
            output_stream.write(struct.pack('>12x'))

        for squad in encounter.squads:
            for move_position in squad.move_positions:
                output_stream.write(struct.pack('>fff', move_position.position[0], move_position.position[1], move_position.position[2]))
                output_stream.write(struct.pack('>f', radians(move_position.facing)))
                output_stream.write(struct.pack('>f', move_position.weight))
                output_stream.write(struct.pack('>ff', move_position.time[0], move_position.time[1]))
                output_stream.write(struct.pack('>h', move_position.animation))
                output_stream.write(struct.pack('>b', move_position.sequence_id))
                output_stream.write(struct.pack('>45x'))
                output_stream.write(struct.pack('>i', move_position.surface_index))

            for starting_location in squad.starting_locations:
                output_stream.write(struct.pack('>fff', starting_location.position[0], starting_location.position[1], starting_location.position[2]))
                output_stream.write(struct.pack('>f', radians(starting_location.facing)))
                output_stream.write(struct.pack('>2x'))
                output_stream.write(struct.pack('>b', starting_location.sequence_id))
                output_stream.write(struct.pack('>b', starting_location.flags))
                output_stream.write(struct.pack('>h', starting_location.return_state))
                output_stream.write(struct.pack('>h', starting_location.initial_state))
                output_stream.write(struct.pack('>h', starting_location.actor_type))
                output_stream.write(struct.pack('>h', starting_location.command_list))

        for platoon in encounter.platoons:
            output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(platoon.name, False)))
            output_stream.write(struct.pack('>i', platoon.flags))
            output_stream.write(struct.pack('>12x'))
            output_stream.write(struct.pack('>h', platoon.change_attacking_defending_state))
            output_stream.write(struct.pack('>h', platoon.happens_to_a))
            output_stream.write(struct.pack('>8x'))
            output_stream.write(struct.pack('>h', platoon.maneuver_when))
            output_stream.write(struct.pack('>h', platoon.happens_to_b))
            output_stream.write(struct.pack('>108x'))

        for firing_position in encounter.firing_positions:
            output_stream.write(struct.pack('>fff', firing_position.position[0], firing_position.position[1], firing_position.position[2]))
            output_stream.write(struct.pack('>h', firing_position.group_index))
            output_stream.write(struct.pack('>10x'))

        for player_starting_location_element in encounter.player_starting_locations:
            output_stream.write(struct.pack('>fff', player_starting_location_element.position[0], player_starting_location_element.position[1], player_starting_location_element.position[2]))
            output_stream.write(struct.pack('>f', radians(player_starting_location_element.facing)))
            output_stream.write(struct.pack('>h', player_starting_location_element.team_index))
            output_stream.write(struct.pack('>h', player_starting_location_element.bsp_index))
            output_stream.write(struct.pack('>h', player_starting_location_element.type_0))
            output_stream.write(struct.pack('>h', player_starting_location_element.type_1))
            output_stream.write(struct.pack('>h', player_starting_location_element.type_2))
            output_stream.write(struct.pack('>h', player_starting_location_element.type_3))
            output_stream.write(struct.pack('>24x'))

def write_command_lists(output_stream, SCENARIO):
    for command_list in SCENARIO.command_lists:
        output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(command_list.name, False)))
        output_stream.write(struct.pack('>2x'))
        output_stream.write(struct.pack('>h', command_list.flags))
        output_stream.write(struct.pack('>8x'))
        output_stream.write(struct.pack('>h', command_list.manual_bsp_index))
        output_stream.write(struct.pack('>2x'))
        command_list.command_tag_block.write(output_stream, True)
        command_list.points_tag_block.write(output_stream, True)
        output_stream.write(struct.pack('>24x'))

    for command_list in SCENARIO.command_lists:
        for command in command_list.commands:
            output_stream.write(struct.pack('>h', command.atom_type))
            output_stream.write(struct.pack('>h', command.atom_modifier))
            output_stream.write(struct.pack('>f', command.parameter1))
            output_stream.write(struct.pack('>f', command.parameter2))
            output_stream.write(struct.pack('>h', command.point_1))
            output_stream.write(struct.pack('>h', command.point_2))
            output_stream.write(struct.pack('>h', command.animation))
            output_stream.write(struct.pack('>h', command.script))
            output_stream.write(struct.pack('>h', command.recording))
            output_stream.write(struct.pack('>h', command.command))
            output_stream.write(struct.pack('>h', command.object_name))
            output_stream.write(struct.pack('>6x'))

        for point in command_list.points:
            output_stream.write(struct.pack('>fff', point[0], point[1], point[2]))
            output_stream.write(struct.pack('>8x'))

def write_ai_animation_references(output_stream, SCENARIO):
    for ai_animation_reference in SCENARIO.ai_animation_references:
        output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(ai_animation_reference.name, False)))
        ai_animation_reference.animation_reference.write(output_stream, True, False)
        output_stream.write(struct.pack('>12x'))

    for ai_animation_reference in SCENARIO.ai_animation_references:
        animation_reference_name_length = len(ai_animation_reference.animation_reference.name)
        if animation_reference_name_length > 0:
            output_stream.write(struct.pack('>%ssx' % animation_reference_name_length, tag_format.string_to_bytes(ai_animation_reference.animation_reference.name, False)))

def write_ai_references(output_stream, tag_block):
    for element in tag_block:
        output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(element, False)))
        output_stream.write(struct.pack('>8x'))

def write_ai_conversations(output_stream, SCENARIO):
    for ai_conversation in SCENARIO.ai_conversations:
        output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(ai_conversation.name, False)))
        output_stream.write(struct.pack('>h', ai_conversation.flags))
        output_stream.write(struct.pack('>2x'))
        output_stream.write(struct.pack('>f', ai_conversation.trigger_distance))
        output_stream.write(struct.pack('>f', ai_conversation.run_to_player_distance))
        output_stream.write(struct.pack('>36x'))
        ai_conversation.participants_tag_block.write(output_stream, True)
        ai_conversation.lines_tag_block.write(output_stream, True)
        output_stream.write(struct.pack('>12x'))

    for ai_conversation in SCENARIO.ai_conversations:
        for participant in ai_conversation.participants:
            output_stream.write(struct.pack('>2x'))
            output_stream.write(struct.pack('>h', participant.flags))
            output_stream.write(struct.pack('>h', participant.selection_type))
            output_stream.write(struct.pack('>h', participant.actor_type))
            output_stream.write(struct.pack('>h', participant.use_this_object))
            output_stream.write(struct.pack('>h', participant.set_new_name))
            output_stream.write(struct.pack('>24x'))
            output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(participant.encounter_name, False)))
            output_stream.write(struct.pack('>16x'))

        for line in ai_conversation.lines:
            output_stream.write(struct.pack('>h', line.flags))
            output_stream.write(struct.pack('>h', line.participant))
            output_stream.write(struct.pack('>h', line.addresses))
            output_stream.write(struct.pack('>h', line.addresse_participant))
            output_stream.write(struct.pack('>4x'))
            output_stream.write(struct.pack('>f', line.line_delay_time))
            output_stream.write(struct.pack('>12x'))
            line.variant_1.write(output_stream, True, False)
            line.variant_2.write(output_stream, True, False)
            line.variant_3.write(output_stream, True, False)
            line.variant_4.write(output_stream, True, False)
            line.variant_5.write(output_stream, True, False)
            line.variant_6.write(output_stream, True, False)

        for line in ai_conversation.lines:
            variant_1_name_length = len(line.variant_1.name)
            variant_2_name_length = len(line.variant_2.name)
            variant_3_name_length = len(line.variant_3.name)
            variant_4_name_length = len(line.variant_4.name)
            variant_5_name_length = len(line.variant_5.name)
            variant_6_name_length = len(line.variant_6.name)
            if variant_1_name_length > 0:
                output_stream.write(struct.pack('>%ssx' % variant_1_name_length, tag_format.string_to_bytes(line.variant_1.name, False)))

            if variant_2_name_length > 0:
                output_stream.write(struct.pack('>%ssx' % variant_2_name_length, tag_format.string_to_bytes(line.variant_2.name, False)))

            if variant_3_name_length > 0:
                output_stream.write(struct.pack('>%ssx' % variant_3_name_length, tag_format.string_to_bytes(line.variant_3.name, False)))

            if variant_4_name_length > 0:
                output_stream.write(struct.pack('>%ssx' % variant_4_name_length, tag_format.string_to_bytes(line.variant_4.name, False)))

            if variant_5_name_length > 0:
                output_stream.write(struct.pack('>%ssx' % variant_5_name_length, tag_format.string_to_bytes(line.variant_5.name, False)))

            if variant_6_name_length > 0:
                output_stream.write(struct.pack('>%ssx' % variant_6_name_length, tag_format.string_to_bytes(line.variant_6.name, False)))

def write_scripts(output_stream, SCENARIO):
    for script in SCENARIO.scripts:
        output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(script.name, False)))
        output_stream.write(struct.pack('>h', script.script_type))
        output_stream.write(struct.pack('>h', script.return_type))
        output_stream.write(struct.pack('>i', script.root_expression_index))
        output_stream.write(struct.pack('>40x'))
        script.parameters_tag_block.write(output_stream, True)

    for script in SCENARIO.scripts:
        for parameter in script.parameters:
            output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(parameter.name, False)))
            output_stream.write(struct.pack('>h', parameter.return_type))
            output_stream.write(struct.pack('>2x'))

def write_globals(output_stream, SCENARIO):
    for global_element in SCENARIO.globals:
        output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(global_element.name, False)))
        output_stream.write(struct.pack('>h', global_element.return_type))
        output_stream.write(struct.pack('>6x'))
        output_stream.write(struct.pack('>i', global_element.initialization_expression_index))
        output_stream.write(struct.pack('>48x'))

def write_references(output_stream, SCENARIO):
    for reference in SCENARIO.references:
        output_stream.write(struct.pack('>24x'))
        reference.write(output_stream, True, False)

    for reference in SCENARIO.references:
        reference_name_length = len(reference.name)
        if reference_name_length > 0:
            output_stream.write(struct.pack('>%ssx' % reference_name_length, tag_format.string_to_bytes(reference.name, False)))

def write_source_files(output_stream, SCENARIO):
    for source_file in SCENARIO.source_files:
        output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(source_file.name, False)))
        source_file.source_tag_data.write(output_stream, True)

    for source_file in SCENARIO.source_files:
        output_stream.write(tag_format.string_to_bytes(source_file.source, False))
        output_stream.write(struct.pack('>x'))

def write_cutscene_flags(output_stream, SCENARIO):
    for cutscene_flag in SCENARIO.cutscene_flags:
        output_stream.write(struct.pack('>4x'))
        output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(cutscene_flag.name, False)))
        output_stream.write(struct.pack('>fff', cutscene_flag.position[0], cutscene_flag.position[1], cutscene_flag.position[2]))
        output_stream.write(struct.pack('>ff', radians(cutscene_flag.facing[0]), radians(cutscene_flag.facing[1])))
        output_stream.write(struct.pack('>36x'))

def write_cutscene_camera_points(output_stream, SCENARIO):
    for cutscene_camera_point in SCENARIO.cutscene_camera_points:
        output_stream.write(struct.pack('>4x'))
        output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(cutscene_camera_point.name, False)))
        output_stream.write(struct.pack('>4x'))
        output_stream.write(struct.pack('>fff', cutscene_camera_point.position[0], cutscene_camera_point.position[1], cutscene_camera_point.position[2]))
        output_stream.write(struct.pack('>fff', radians(cutscene_camera_point.orientation[0]), radians(cutscene_camera_point.orientation[1]), radians(cutscene_camera_point.orientation[2])))
        output_stream.write(struct.pack('>f', radians(cutscene_camera_point.field_of_view)))
        output_stream.write(struct.pack('>36x'))

def write_cutscene_titles(output_stream, SCENARIO):
    for cutscene_title in SCENARIO.cutscene_titles:
        output_stream.write(struct.pack('>4x'))
        output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(cutscene_title.name, False)))
        output_stream.write(struct.pack('>4x'))
        output_stream.write(struct.pack('>4h', cutscene_title.text_bounds[0], cutscene_title.text_bounds[1], cutscene_title.text_bounds[2], cutscene_title.text_bounds[3]))
        output_stream.write(struct.pack('>h', cutscene_title.string_index))
        output_stream.write(struct.pack('>h', cutscene_title.style))
        output_stream.write(struct.pack('>h', cutscene_title.justification))
        output_stream.write(struct.pack('>2x'))
        output_stream.write(struct.pack('>i', cutscene_title.text_flags))
        output_stream.write(struct.pack('>4B', cutscene_title.text_color[3], cutscene_title.text_color[0], cutscene_title.text_color[1], cutscene_title.text_color[2]))
        output_stream.write(struct.pack('>4B', cutscene_title.shadow_color[3], cutscene_title.shadow_color[0], cutscene_title.shadow_color[1], cutscene_title.shadow_color[2]))
        output_stream.write(struct.pack('>f', cutscene_title.fade_in_time))
        output_stream.write(struct.pack('>f', cutscene_title.up_time))
        output_stream.write(struct.pack('>f', cutscene_title.fade_out_time))
        output_stream.write(struct.pack('>16x'))

def write_structure_bsps(output_stream, SCENARIO):
    for structure_bsp in SCENARIO.structure_bsps:
        output_stream.write(struct.pack('>16x'))
        structure_bsp.write(output_stream, True, False)

    for structure_bsp_element in SCENARIO.structure_bsps:
        structure_bsp_name_length = len(structure_bsp_element.name)
        if structure_bsp_name_length > 0:
            output_stream.write(struct.pack('>%ssx' % structure_bsp_name_length, tag_format.string_to_bytes(structure_bsp_element.name, False)))

def write_palette(output_stream, palette, size):
    for palette_element in palette:
        palette_element.write(output_stream, True)
        output_stream.write(struct.pack('>%sx' % size))

    for palette_element in palette:
        palette_name_length = palette_element.name_length
        if palette_name_length > 0:
            output_stream.write(struct.pack('>%ss1x' % palette_name_length, tag_format.string_to_bytes(palette_element.name, False)))

def build_asset(output_stream, SCENARIO, report):
    SCENARIO.header.write(output_stream, True)
    write_body(output_stream, SCENARIO)

    dont_use_length = SCENARIO.scenario_body.dont_use_tag_ref.name_length
    if dont_use_length > 0:
        output_stream.write(struct.pack('>%ssx' % dont_use_length, tag_format.string_to_bytes(SCENARIO.scenario_body.dont_use_tag_ref.name, False)))

    wont_use_length = SCENARIO.scenario_body.wont_use_tag_ref.name_length
    if wont_use_length > 0:
        output_stream.write(struct.pack('>%ssx' % wont_use_length, tag_format.string_to_bytes(SCENARIO.scenario_body.wont_use_tag_ref.name, False)))

    cant_use_length = SCENARIO.scenario_body.cant_use_tag_ref.name_length
    if cant_use_length > 0:
        output_stream.write(struct.pack('>%ssx' % cant_use_length, tag_format.string_to_bytes(SCENARIO.scenario_body.cant_use_tag_ref.name, False)))

    write_palette(output_stream, SCENARIO.skies, 0)

    write_palette(output_stream, SCENARIO.child_scenarios, 16)

    write_predicted_resources(output_stream, SCENARIO)

    write_functions(output_stream, SCENARIO)

    output_stream.write(SCENARIO.editor_scenario_data)

    write_comments(output_stream, SCENARIO.comments)

    write_scavenger_hunt_objects(output_stream, SCENARIO)

    write_object_names(output_stream, SCENARIO)

    write_scenery(output_stream, SCENARIO)
    write_palette(output_stream, SCENARIO.scenery_palette, 32)

    write_bipeds(output_stream, SCENARIO)
    write_palette(output_stream, SCENARIO.biped_palette, 32)

    write_vehicles(output_stream, SCENARIO)
    write_palette(output_stream, SCENARIO.vehicle_palette, 32)

    write_equipment(output_stream, SCENARIO)
    write_palette(output_stream, SCENARIO.equipment_palette, 32)

    write_weapons(output_stream, SCENARIO)
    write_palette(output_stream, SCENARIO.weapon_palette, 32)

    write_device_groups(output_stream, SCENARIO.device_groups)

    write_machines(output_stream, SCENARIO)
    write_palette(output_stream, SCENARIO.device_machine_palette, 32)

    write_device_controls(output_stream, SCENARIO)
    write_palette(output_stream, SCENARIO.device_control_palette, 32)

    write_device_light_fixtures(output_stream, SCENARIO)
    write_palette(output_stream, SCENARIO.device_light_fixtures_palette, 32)

    write_sound_scenery(output_stream, SCENARIO)
    write_palette(output_stream, SCENARIO.sound_scenery_palette, 32)

    write_player_starting_profiles(output_stream, SCENARIO)

    write_player_starting_locations(output_stream, SCENARIO)

    write_trigger_volumes(output_stream, SCENARIO)

    write_recorded_animations(output_stream, SCENARIO)

    write_netgame_flags(output_stream, SCENARIO)

    write_netgame_equipment(output_stream, SCENARIO)

    write_starting_equipment(output_stream, SCENARIO)

    write_bsp_switch_trigger_volumes(output_stream, SCENARIO)

    write_decals(output_stream, SCENARIO)
    write_palette(output_stream, SCENARIO.decal_palette, 0)

    write_palette(output_stream, SCENARIO.detail_object_collection_palette, 32)

    write_palette(output_stream, SCENARIO.actor_palette, 0)

    write_encounters(output_stream, SCENARIO)

    write_command_lists(output_stream, SCENARIO)

    write_ai_animation_references(output_stream, SCENARIO)

    write_ai_references(output_stream, SCENARIO.ai_script_references)

    write_ai_references(output_stream, SCENARIO.ai_recording_references)

    write_ai_conversations(output_stream, SCENARIO)

    output_stream.write(SCENARIO.script_syntax_data)
    output_stream.write(SCENARIO.script_string_data)

    write_scripts(output_stream, SCENARIO)

    write_globals(output_stream, SCENARIO)

    write_references(output_stream, SCENARIO)

    write_source_files(output_stream, SCENARIO)

    write_cutscene_flags(output_stream, SCENARIO)

    write_cutscene_camera_points(output_stream, SCENARIO)

    write_cutscene_titles(output_stream, SCENARIO)

    custom_object_names_length = SCENARIO.scenario_body.custom_object_names_tag_ref.name_length
    if custom_object_names_length > 0:
        output_stream.write(struct.pack('>%ssx' % custom_object_names_length, tag_format.string_to_bytes(SCENARIO.scenario_body.custom_object_names_tag_ref.name, False)))

    chapter_title_text_length = SCENARIO.scenario_body.chapter_title_text_tag_ref.name_length
    if chapter_title_text_length > 0:
        output_stream.write(struct.pack('>%ssx' % chapter_title_text_length, tag_format.string_to_bytes(SCENARIO.scenario_body.chapter_title_text_tag_ref.name, False)))

    hud_messages_length = SCENARIO.scenario_body.hud_messages_tag_ref.name_length
    if hud_messages_length > 0:
        output_stream.write(struct.pack('>%ssx' % hud_messages_length, tag_format.string_to_bytes(SCENARIO.scenario_body.hud_messages_tag_ref.name, False)))

    write_structure_bsps(output_stream, SCENARIO)
