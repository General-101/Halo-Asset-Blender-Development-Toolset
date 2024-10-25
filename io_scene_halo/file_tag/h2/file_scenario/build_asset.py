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

def write_body(output_stream, SCENARIO, TAG):
    SCENARIO.body_header.write(output_stream, TAG, True)
    SCENARIO.unused_tag_ref.write(output_stream, False, True)
    SCENARIO.skies_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<HH', SCENARIO.scenario_type, SCENARIO.scenario_flags))
    SCENARIO.child_scenarios_tag_block.write(output_stream, False)
    output_stream.write(struct.pack('<f', radians(SCENARIO.local_north)))
    SCENARIO.predicted_resources_tag_block.write(output_stream, False)
    SCENARIO.functions_tag_block.write(output_stream, False)
    SCENARIO.editor_scenario_data.write(output_stream, False)
    SCENARIO.comments_tag_block.write(output_stream, False)
    SCENARIO.environment_objects_tag_block.write(output_stream, False)
    SCENARIO.object_names_tag_block.write(output_stream, False)
    SCENARIO.scenery_tag_block.write(output_stream, False)
    SCENARIO.scenery_palette_tag_block.write(output_stream, False)
    SCENARIO.bipeds_tag_block.write(output_stream, False)
    SCENARIO.biped_palette_tag_block.write(output_stream, False)
    SCENARIO.vehicles_tag_block.write(output_stream, False)
    SCENARIO.vehicle_palette_tag_block.write(output_stream, False)
    SCENARIO.equipment_tag_block.write(output_stream, False)
    SCENARIO.equipment_palette_tag_block.write(output_stream, False)
    SCENARIO.weapons_tag_block.write(output_stream, False)
    SCENARIO.weapon_palette_tag_block.write(output_stream, False)
    SCENARIO.device_groups_tag_block.write(output_stream, False)
    SCENARIO.machines_tag_block.write(output_stream, False)
    SCENARIO.machine_palette_tag_block.write(output_stream, False)
    SCENARIO.controls_tag_block.write(output_stream, False)
    SCENARIO.control_palette_tag_block.write(output_stream, False)
    SCENARIO.light_fixtures_tag_block.write(output_stream, False)
    SCENARIO.light_fixtures_palette_tag_block.write(output_stream, False)
    SCENARIO.sound_scenery_tag_block.write(output_stream, False)
    SCENARIO.sound_scenery_palette_tag_block.write(output_stream, False)
    SCENARIO.light_volumes_tag_block.write(output_stream, False)
    SCENARIO.light_volume_palette_tag_block.write(output_stream, False)
    SCENARIO.player_starting_profile_tag_block.write(output_stream, False)
    SCENARIO.player_starting_locations_tag_block.write(output_stream, False)
    SCENARIO.trigger_volumes_tag_block.write(output_stream, False)
    SCENARIO.recorded_animations_tag_block.write(output_stream, False)
    SCENARIO.netgame_flags_tag_block.write(output_stream, False)
    SCENARIO.netgame_equipment_tag_block.write(output_stream, False)
    SCENARIO.starting_equipment_tag_block.write(output_stream, False)
    SCENARIO.bsp_switch_trigger_volumes_tag_block.write(output_stream, False)
    SCENARIO.decals_tag_block.write(output_stream, False)
    SCENARIO.decal_palette_tag_block.write(output_stream, False)
    SCENARIO.detail_object_collection_palette_tag_block.write(output_stream, False)
    SCENARIO.style_palette_tag_block.write(output_stream, False)
    SCENARIO.squad_groups_tag_block.write(output_stream, False)
    SCENARIO.squads_tag_block.write(output_stream, False)
    SCENARIO.zones_tag_block.write(output_stream, False)
    SCENARIO.mission_scenes_tag_block.write(output_stream, False)
    SCENARIO.character_palette_tag_block.write(output_stream, False)
    SCENARIO.ai_pathfinding_data_tag_block.write(output_stream, False)
    SCENARIO.ai_animation_references_tag_block.write(output_stream, False)
    SCENARIO.ai_script_references_tag_block.write(output_stream, False)
    SCENARIO.ai_recording_references_tag_block.write(output_stream, False)
    SCENARIO.ai_conversations_tag_block.write(output_stream, False)
    SCENARIO.script_syntax_data_tag_data.write(output_stream, False)
    SCENARIO.script_string_data_tag_data.write(output_stream, False)
    SCENARIO.scripts_tag_block.write(output_stream, False)
    SCENARIO.globals_tag_block.write(output_stream, False)
    SCENARIO.references_tag_block.write(output_stream, False)
    SCENARIO.source_files_tag_block.write(output_stream, False)
    SCENARIO.scripting_data_tag_block.write(output_stream, False)
    SCENARIO.cutscene_flags_tag_block.write(output_stream, False)
    SCENARIO.cutscene_camera_points_tag_block.write(output_stream, False)
    SCENARIO.cutscene_titles_tag_block.write(output_stream, False)
    SCENARIO.custom_object_names_tag_ref.write(output_stream, False, True)
    SCENARIO.chapter_title_text_tag_ref.write(output_stream, False, True)
    SCENARIO.hud_messages_tag_ref.write(output_stream, False, True)
    SCENARIO.structure_bsps_tag_block.write(output_stream, False)
    SCENARIO.scenario_resources_tag_block.write(output_stream, False)
    SCENARIO.old_structure_physics_tag_block.write(output_stream, False)
    SCENARIO.hs_unit_seats_tag_block.write(output_stream, False)
    SCENARIO.scenario_kill_triggers_tag_block.write(output_stream, False)
    SCENARIO.hs_syntax_datums_tag_block.write(output_stream, False)
    SCENARIO.orders_tag_block.write(output_stream, False)
    SCENARIO.triggers_tag_block.write(output_stream, False)
    SCENARIO.background_sound_palette_tag_block.write(output_stream, False)
    SCENARIO.sound_environment_palette_tag_block.write(output_stream, False)
    SCENARIO.weather_palette_tag_block.write(output_stream, False)
    SCENARIO.unused_0_tag_block.write(output_stream, False)
    SCENARIO.unused_1_tag_block.write(output_stream, False)
    SCENARIO.unused_2_tag_block.write(output_stream, False)
    SCENARIO.unused_3_tag_block.write(output_stream, False)
    SCENARIO.scavenger_hunt_objects_tag_block.write(output_stream, False)
    SCENARIO.scenario_cluster_data_tag_block.write(output_stream, False)
    for salt in SCENARIO.salt_array:
        output_stream.write(struct.pack('<i', salt))

    SCENARIO.spawn_data_tag_block.write(output_stream, False)
    SCENARIO.sound_effect_collection_tag_ref.write(output_stream, False, True)
    SCENARIO.crates_tag_block.write(output_stream, False)
    SCENARIO.crate_palette_tag_block.write(output_stream, False)
    SCENARIO.global_lighting_tag_ref.write(output_stream, False, True)
    SCENARIO.atmospheric_fog_palette_tag_block.write(output_stream, False)
    SCENARIO.planar_fog_palette_tag_block.write(output_stream, False)
    SCENARIO.flocks_tag_block.write(output_stream, False)
    SCENARIO.subtitles_tag_ref.write(output_stream, False, True)
    SCENARIO.decorators_tag_block.write(output_stream, False)
    SCENARIO.creatures_tag_block.write(output_stream, False)
    SCENARIO.creature_palette_tag_block.write(output_stream, False)
    SCENARIO.decorator_palette_tag_block.write(output_stream, False)
    SCENARIO.bsp_transition_volumes_tag_block.write(output_stream, False)
    SCENARIO.structure_bsp_lighting_tag_block.write(output_stream, False)
    SCENARIO.editor_folders_tag_block.write(output_stream, False)
    SCENARIO.level_data_tag_block.write(output_stream, False)
    SCENARIO.game_engine_strings_tag_ref.write(output_stream, False, True)
    output_stream.write(struct.pack('<8x'))
    SCENARIO.mission_dialogue_tag_block.write(output_stream, False)
    SCENARIO.objectives_tag_ref.write(output_stream, False, True)
    SCENARIO.interpolators_tag_block.write(output_stream, False)
    SCENARIO.shared_references_tag_block.write(output_stream, False)
    SCENARIO.screen_effect_references_tag_block.write(output_stream, False)
    SCENARIO.simulation_definition_table_tag_block.write(output_stream, False)

def write_comments(output_stream, SCENARIO, TAG):
    if len(SCENARIO.comments) > 0:
        SCENARIO.comment_header.write(output_stream, TAG, True)
        for comment_element in SCENARIO.comments:
            output_stream.write(struct.pack('<fff', comment_element.position[0], comment_element.position[1], comment_element.position[2]))
            output_stream.write(struct.pack('<I', comment_element.type))
            output_stream.write(struct.pack('<30s2x', tag_format.string_to_bytes(comment_element.name, False)))
            output_stream.write(struct.pack('<254s2x', tag_format.string_to_bytes(comment_element.comment, False)))

def write_object_names(output_stream, SCENARIO, TAG):
    if len(SCENARIO.object_names) > 0:
        SCENARIO.object_name_header.write(output_stream, TAG, True)
        for object_name_element in SCENARIO.object_names:
            output_stream.write(struct.pack('<31sx', tag_format.string_to_bytes(object_name_element.name, False)))
            output_stream.write(struct.pack('<h', object_name_element.object_type))
            output_stream.write(struct.pack('<h', object_name_element.placement_index))

def write_object(output_stream, scenery_element):
    output_stream.write(struct.pack('<h', scenery_element.palette_index))
    output_stream.write(struct.pack('<h', scenery_element.name_index))
    output_stream.write(struct.pack('<I', scenery_element.placement_flags))
    output_stream.write(struct.pack('<fff', scenery_element.position[0], scenery_element.position[1], scenery_element.position[2]))
    output_stream.write(struct.pack('<fff', radians(scenery_element.rotation[0]), radians(scenery_element.rotation[1]), radians(scenery_element.rotation[2])))
    output_stream.write(struct.pack('<f', scenery_element.scale))
    output_stream.write(struct.pack('<H', scenery_element.transform_flags))
    output_stream.write(struct.pack('<H', scenery_element.manual_bsp_flags))
    output_stream.write(struct.pack('<i', scenery_element.unique_id))
    output_stream.write(struct.pack('<h', scenery_element.origin_bsp_index))
    output_stream.write(struct.pack('<bbbx', scenery_element.object_type, scenery_element.source, scenery_element.bsp_policy))
    output_stream.write(struct.pack('<h', scenery_element.editor_folder_index))

def write_color_change(output_stream, scenery_element):
    output_stream.write(struct.pack('>I', scenery_element.active_change_colors))
    output_stream.write(struct.pack('<bbbx', scenery_element.primary_color_BGRA[0], scenery_element.primary_color_BGRA[1], scenery_element.primary_color_BGRA[2]))
    output_stream.write(struct.pack('<bbbx', scenery_element.secondary_color_BGRA[0], scenery_element.secondary_color_BGRA[1], scenery_element.secondary_color_BGRA[2]))
    output_stream.write(struct.pack('<bbbx', scenery_element.tertiary_color_BGRA[0], scenery_element.tertiary_color_BGRA[1], scenery_element.tertiary_color_BGRA[2]))
    output_stream.write(struct.pack('<bbbx', scenery_element.quaternary_color_BGRA[0], scenery_element.quaternary_color_BGRA[1], scenery_element.quaternary_color_BGRA[2]))

def write_scenery(output_stream, SCENARIO, TAG):
    if len(SCENARIO.scenery) > 0:
        SCENARIO.scenery_header.write(output_stream, TAG, True)
        for scenery_element in SCENARIO.scenery:
            write_object(output_stream, scenery_element)
            output_stream.write(struct.pack('>I', len(scenery_element.variant_name)))
            write_color_change(output_stream, scenery_element)
            output_stream.write(struct.pack('<h', scenery_element.pathfinding_policy))
            output_stream.write(struct.pack('<h', scenery_element.lightmap_policy))
            scenery_element.pathfinding_references_tag_block.write(output_stream, False)
            output_stream.write(struct.pack('<2x'))
            output_stream.write(struct.pack('<h', scenery_element.valid_multiplayer_games))

        for scenery_element in SCENARIO.scenery:
            scenery_element.sobj_header.write(output_stream, TAG, True)
            scenery_element.obj0_header.write(output_stream, TAG, True)
            scenery_element.sper_header.write(output_stream, TAG, True)
            variant_count = len(scenery_element.variant_name)
            if variant_count > 0:
                output_stream.write(struct.pack('<%ss' % variant_count, tag_format.string_to_bytes(scenery_element.variant_name, False)))

            scenery_element.sct3_header.write(output_stream, TAG, True)

def write_units(output_stream, unit_list, unit_header, TAG):
    if len(unit_list) > 0:
        unit_header.write(output_stream, TAG, True)
        for unit_element in unit_list:
            write_object(output_stream, unit_element)
            output_stream.write(struct.pack('>I', len(unit_element.variant_name)))
            write_color_change(output_stream, unit_element)
            output_stream.write(struct.pack('<f', unit_element.body_vitality))
            output_stream.write(struct.pack('<I', unit_element.flags))

        for unit_element in unit_list:
            unit_element.sobj_header.write(output_stream, TAG, True)
            unit_element.obj0_header.write(output_stream, TAG, True)
            unit_element.sper_header.write(output_stream, TAG, True)
            variant_count = len(unit_element.variant_name)
            if variant_count > 0:
                output_stream.write(struct.pack('<%ss' % variant_count, tag_format.string_to_bytes(unit_element.variant_name, False)))

            unit_element.sunt_header.write(output_stream, TAG, True)

def write_equipment(output_stream, SCENARIO, TAG):
    if len(SCENARIO.equipment) > 0:
        SCENARIO.equipment_header.write(output_stream, TAG, True)
        for equipment_element in SCENARIO.equipment:
            write_object(output_stream, equipment_element)
            output_stream.write(struct.pack('<I', equipment_element.flags))

        for equipment_element in SCENARIO.equipment:
            equipment_element.sobj_header.write(output_stream, TAG, True)
            equipment_element.obj0_header.write(output_stream, TAG, True)
            equipment_element.seqt_header.write(output_stream, TAG, True)

def write_weapons(output_stream, SCENARIO, TAG):
    if len(SCENARIO.weapons) > 0:
        SCENARIO.weapon_header.write(output_stream, TAG, True)
        for weapon_element in SCENARIO.weapons:
            write_object(output_stream, weapon_element)
            output_stream.write(struct.pack('>I', len(weapon_element.variant_name)))
            write_color_change(output_stream, weapon_element)
            output_stream.write(struct.pack('<h', weapon_element.rounds_left))
            output_stream.write(struct.pack('<h', weapon_element.rounds_loaded))
            output_stream.write(struct.pack('<I', weapon_element.flags))

        for weapon_element in SCENARIO.weapons:
            weapon_element.sobj_header.write(output_stream, TAG, True)
            weapon_element.obj0_header.write(output_stream, TAG, True)
            weapon_element.sper_header.write(output_stream, TAG, True)
            variant_count = len(weapon_element.variant_name)
            if variant_count > 0:
                output_stream.write(struct.pack('<%ss' % variant_count, tag_format.string_to_bytes(weapon_element.variant_name, False)))

            weapon_element.swpt_header.write(output_stream, TAG, True)

def write_device_groups(output_stream, SCENARIO, TAG):
    if len(SCENARIO.device_groups) > 0:
        SCENARIO.device_group_header.write(output_stream, TAG, True)
        for device_group_element in SCENARIO.device_groups:
            output_stream.write(struct.pack('<30s2x', tag_format.string_to_bytes(device_group_element.name, False)))
            output_stream.write(struct.pack('<f', device_group_element.initial_value))
            output_stream.write(struct.pack('<I', device_group_element.flags))

def write_machines(output_stream, SCENARIO, TAG):
    if len(SCENARIO.device_machines) > 0:
        SCENARIO.device_machine_header.write(output_stream, TAG, True)
        for device_machines_element in SCENARIO.device_machines:
            write_object(output_stream, device_machines_element)
            output_stream.write(struct.pack('<h', device_machines_element.power_group_index))
            output_stream.write(struct.pack('<h', device_machines_element.position_group_index))
            output_stream.write(struct.pack('<I', device_machines_element.flags_0))
            output_stream.write(struct.pack('<I', device_machines_element.flags_1))
            device_machines_element.pathfinding_references_tag_block.write(output_stream, False)

        for device_machines_element in SCENARIO.device_machines:
            device_machines_element.sobj_header.write(output_stream, TAG, True)
            device_machines_element.obj0_header.write(output_stream, TAG, True)
            device_machines_element.sdvt_header.write(output_stream, TAG, True)
            device_machines_element.smht_header.write(output_stream, TAG, True)

def write_controls(output_stream, SCENARIO, TAG):
    if len(SCENARIO.device_controls) > 0:
        SCENARIO.device_control_header.write(output_stream, TAG, True)
        for device_control_element in SCENARIO.device_controls:
            write_object(output_stream, device_control_element)
            output_stream.write(struct.pack('<h', device_control_element.power_group_index))
            output_stream.write(struct.pack('<h', device_control_element.position_group_index))
            output_stream.write(struct.pack('<I', device_control_element.flags_0))
            output_stream.write(struct.pack('<I', device_control_element.flags_1))
            output_stream.write(struct.pack('<i', device_control_element.unk))

        for device_control_element in SCENARIO.device_controls:
            device_control_element.sobj_header.write(output_stream, TAG, True)
            device_control_element.obj0_header.write(output_stream, TAG, True)
            device_control_element.sdvt_header.write(output_stream, TAG, True)
            device_control_element.sctt_header.write(output_stream, TAG, True)

def write_light_fixtures(output_stream, SCENARIO, TAG):
    if len(SCENARIO.device_light_fixtures) > 0:
        SCENARIO.device_light_fixture_header.write(output_stream, TAG, True)
        for light_fixture_element in SCENARIO.device_light_fixtures:
            write_object(output_stream, light_fixture_element)
            output_stream.write(struct.pack('<h', light_fixture_element.power_group_index))
            output_stream.write(struct.pack('<h', light_fixture_element.position_group_index))
            output_stream.write(struct.pack('<I', light_fixture_element.flags))
            output_stream.write(struct.pack('<fff', light_fixture_element.color_RGBA[0], light_fixture_element.color_RGBA[1], light_fixture_element.color_RGBA[2]))
            output_stream.write(struct.pack('<f', light_fixture_element.intensity))
            output_stream.write(struct.pack('<f', radians(light_fixture_element.falloff_angle)))
            output_stream.write(struct.pack('<f', radians(light_fixture_element.cutoff_angle)))

        for light_fixture_element in SCENARIO.device_light_fixtures:
            light_fixture_element.sobj_header.write(output_stream, TAG, True)
            light_fixture_element.obj0_header.write(output_stream, TAG, True)
            light_fixture_element.sdvt_header.write(output_stream, TAG, True)
            light_fixture_element.slft_header.write(output_stream, TAG, True)

def write_sound_scenery(output_stream, SCENARIO, TAG):
    if len(SCENARIO.sound_scenery) > 0:
        SCENARIO.sound_scenery_header.write(output_stream, TAG, True)
        for sound_scenery_element in SCENARIO.sound_scenery:
            write_object(output_stream, sound_scenery_element)
            output_stream.write(struct.pack('<I', sound_scenery_element.volume_type))
            output_stream.write(struct.pack('<f', sound_scenery_element.height))
            output_stream.write(struct.pack('<ff', sound_scenery_element.override_distance_bounds[0], sound_scenery_element.override_distance_bounds[1]))
            output_stream.write(struct.pack('<ff', radians(sound_scenery_element.override_core_angle_bounds[0]), radians(sound_scenery_element.override_core_angle_bounds[1])))
            output_stream.write(struct.pack('<f', sound_scenery_element.override_outer_core_gain))

        for sound_scenery_element in SCENARIO.sound_scenery:
            sound_scenery_element.sobj_header.write(output_stream, TAG, True)
            sound_scenery_element.obj0_header.write(output_stream, TAG, True)
            sound_scenery_element._sc__header.write(output_stream, TAG, True)

def write_light_volumes(output_stream, SCENARIO, TAG):
    if len(SCENARIO.light_volumes) > 0:
        SCENARIO.light_volume_header.write(output_stream, TAG, True)
        for light_volume_element in SCENARIO.light_volumes:
            write_object(output_stream, light_volume_element)
            output_stream.write(struct.pack('<h', light_volume_element.power_group_index))
            output_stream.write(struct.pack('<h', light_volume_element.position_group_index))
            output_stream.write(struct.pack('<I', light_volume_element.flags_0))
            output_stream.write(struct.pack('<h', light_volume_element.shape_type))
            output_stream.write(struct.pack('<h', light_volume_element.flags_1))
            output_stream.write(struct.pack('<h', light_volume_element.lightmap_type))
            output_stream.write(struct.pack('<h', light_volume_element.lightmap_flags))
            output_stream.write(struct.pack('<f', light_volume_element.lightmap_half_life))
            output_stream.write(struct.pack('<f', light_volume_element.lightmap_light_scale))
            output_stream.write(struct.pack('<fff', light_volume_element.target_point[0], light_volume_element.target_point[1], light_volume_element.target_point[2]))
            output_stream.write(struct.pack('<f', light_volume_element.width))
            output_stream.write(struct.pack('<f', light_volume_element.height_scale))
            output_stream.write(struct.pack('<f', radians(light_volume_element.field_of_view)))
            output_stream.write(struct.pack('<f', light_volume_element.falloff_distance))
            output_stream.write(struct.pack('<f', light_volume_element.cutoff_distance))

        for light_volume_element in SCENARIO.light_volumes:
            light_volume_element.sobj_header.write(output_stream, TAG, True)
            light_volume_element.obj0_header.write(output_stream, TAG, True)
            light_volume_element.sdvt_header.write(output_stream, TAG, True)
            light_volume_element.slit_header.write(output_stream, TAG, True)

def write_player_starting_profiles(output_stream, SCENARIO, TAG):
    if len(SCENARIO.player_starting_profiles) > 0:
        SCENARIO.player_starting_profile_header.write(output_stream, TAG, True)
        for player_starting_profile_element in SCENARIO.player_starting_profiles:
            output_stream.write(struct.pack('<31sx', tag_format.string_to_bytes(player_starting_profile_element.name, False)))
            output_stream.write(struct.pack('<f', player_starting_profile_element.starting_health_damage))
            output_stream.write(struct.pack('<f', player_starting_profile_element.starting_shield_damage))
            player_starting_profile_element.primary_weapon_tag_ref.write(output_stream, False, True)
            output_stream.write(struct.pack('<h', player_starting_profile_element.primary_rounds_loaded))
            output_stream.write(struct.pack('<h', player_starting_profile_element.primary_rounds_total))
            player_starting_profile_element.secondary_weapon_tag_ref.write(output_stream, False, True)
            output_stream.write(struct.pack('<h', player_starting_profile_element.secondary_rounds_loaded))
            output_stream.write(struct.pack('<h', player_starting_profile_element.secondary_rounds_total))
            output_stream.write(struct.pack('<b', player_starting_profile_element.starting_fragmentation_grenades_count))
            output_stream.write(struct.pack('<b', player_starting_profile_element.starting_plasma_grenade_count))
            output_stream.write(struct.pack('<b', player_starting_profile_element.starting_custom_2_grenade_count))
            output_stream.write(struct.pack('<b', player_starting_profile_element.starting_custom_3_grenade_count))

        for player_starting_profile_element in SCENARIO.player_starting_profiles:
            primary_weapon_name_length = len(player_starting_profile_element.primary_weapon_tag_ref.name)
            secondary_weapon_name_length = len(player_starting_profile_element.secondary_weapon_tag_ref.name)
            if primary_weapon_name_length > 0:
                output_stream.write(struct.pack('<%ssx' % primary_weapon_name_length, tag_format.string_to_bytes(player_starting_profile_element.primary_weapon_tag_ref.name, False)))

            if secondary_weapon_name_length > 0:
                output_stream.write(struct.pack('<%ssx' % secondary_weapon_name_length, tag_format.string_to_bytes(player_starting_profile_element.secondary_weapon_tag_ref.name, False)))

def write_player_starting_locations(output_stream, SCENARIO, TAG):
    if len(SCENARIO.player_starting_locations) > 0:
        SCENARIO.player_starting_location_header.write(output_stream, TAG, True)
        for player_starting_location_element in SCENARIO.player_starting_locations:
            output_stream.write(struct.pack('<fff', player_starting_location_element.position[0], player_starting_location_element.position[1], player_starting_location_element.position[2]))
            output_stream.write(struct.pack('<f', radians(player_starting_location_element.facing)))
            output_stream.write(struct.pack('<h', player_starting_location_element.team_designator))
            output_stream.write(struct.pack('<h', player_starting_location_element.bsp_index))
            output_stream.write(struct.pack('<h', player_starting_location_element.type_0))
            output_stream.write(struct.pack('<h', player_starting_location_element.type_1))
            output_stream.write(struct.pack('<h', player_starting_location_element.type_2))
            output_stream.write(struct.pack('<h', player_starting_location_element.type_3))
            output_stream.write(struct.pack('<h', player_starting_location_element.spawn_type_0))
            output_stream.write(struct.pack('<h', player_starting_location_element.spawn_type_1))
            output_stream.write(struct.pack('<h', player_starting_location_element.spawn_type_2))
            output_stream.write(struct.pack('<h', player_starting_location_element.spawn_type_3))
            output_stream.write(struct.pack('>I', player_starting_location_element.unk_0_length))
            output_stream.write(struct.pack('>I', player_starting_location_element.unk_1_length))
            output_stream.write(struct.pack('<h6x', player_starting_location_element.campaign_player_type))

        for player_starting_location_element in SCENARIO.player_starting_locations:
            unk_0_name_length = len(player_starting_location_element.unk_0)
            unk_1_name_length = len(player_starting_location_element.unk_1)
            if unk_0_name_length > 0:
                output_stream.write(struct.pack('<%ss' % unk_0_name_length, tag_format.string_to_bytes(player_starting_location_element.unk_0, False)))

            if unk_1_name_length > 0:
                output_stream.write(struct.pack('<%ss' % unk_1_name_length, tag_format.string_to_bytes(player_starting_location_element.unk_1, False)))

def write_trigger_volumes(output_stream, SCENARIO, TAG):
    if len(SCENARIO.trigger_volumes) > 0:
        SCENARIO.trigger_volumes_header.write(output_stream, TAG, True)
        for trigger_volume_element in SCENARIO.trigger_volumes:
            output_stream.write(struct.pack('>i', len(trigger_volume_element.name)))
            output_stream.write(struct.pack('<i', trigger_volume_element.object_name_index))
            output_stream.write(struct.pack('>i', len(trigger_volume_element.node_name)))

            output_stream.write(struct.pack('<fff', trigger_volume_element.forward[0], trigger_volume_element.forward[1], trigger_volume_element.forward[2]))
            output_stream.write(struct.pack('<fff', trigger_volume_element.up[0], trigger_volume_element.up[1], trigger_volume_element.up[2]))
            output_stream.write(struct.pack('<fff', trigger_volume_element.position[0], trigger_volume_element.position[1], trigger_volume_element.position[2]))
            output_stream.write(struct.pack('<fff', trigger_volume_element.extents[0], trigger_volume_element.extents[1], trigger_volume_element.extents[2]))
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('<h', trigger_volume_element.kill_trigger_volume_index))
            output_stream.write(struct.pack('<2x'))

        for trigger_volume_element in SCENARIO.trigger_volumes:
            output_stream.write(struct.pack('<%ss' % len(trigger_volume_element.name), tag_format.string_to_bytes(trigger_volume_element.name, False)))

def write_recorded_animations(output_stream, SCENARIO, TAG):
    if len(SCENARIO.recorded_animations) > 0:
        SCENARIO.recorded_animation_header.write(output_stream, TAG, True)
        for recorded_animation_element in SCENARIO.recorded_animations:
            output_stream.write(struct.pack('<30s2x', tag_format.string_to_bytes(recorded_animation_element.name, False)))
            output_stream.write(struct.pack('<3bx', recorded_animation_element.version, recorded_animation_element.raw_animation_data, recorded_animation_element.unit_control_data_version))
            output_stream.write(struct.pack('<h6x', recorded_animation_element.length_of_animation))
            recorded_animation_element.recorded_animation_event_stream_tag_data.write(output_stream, False)

        for recorded_animation_element in SCENARIO.recorded_animations:
            output_stream.write(recorded_animation_element.recorded_animation_event_stream)

def write_netgame_flags(output_stream, SCENARIO, TAG):
    if len(SCENARIO.netgame_flags) > 0:
        SCENARIO.netgame_flag_header.write(output_stream, TAG, True)
        for netgame_flag_element in SCENARIO.netgame_flags:
            output_stream.write(struct.pack('<fff', netgame_flag_element.position[0], netgame_flag_element.position[1], netgame_flag_element.position[2]))
            output_stream.write(struct.pack('<f', radians(netgame_flag_element.facing)))
            output_stream.write(struct.pack('<4h', netgame_flag_element.type, netgame_flag_element.team_designator, netgame_flag_element.identifer, netgame_flag_element.flags))
            output_stream.write(struct.pack('>2I', len(netgame_flag_element.spawn_object_name), len(netgame_flag_element.spawn_marker_name)))

        for netgame_flag_element in SCENARIO.netgame_flags:
            output_stream.write(struct.pack('<%ss' % len(netgame_flag_element.spawn_object_name), tag_format.string_to_bytes(netgame_flag_element.spawn_object_name, False)))
            output_stream.write(struct.pack('<%ss' % len(netgame_flag_element.spawn_marker_name), tag_format.string_to_bytes(netgame_flag_element.spawn_marker_name, False)))

def write_netgame_equipment(output_stream, SCENARIO, TAG):
    if len(SCENARIO.netgame_equipment) > 0:
        SCENARIO.netgame_equipment_header.write(output_stream, TAG, True)
        for netgame_equipment_element in SCENARIO.netgame_equipment:
            output_stream.write(struct.pack('<I', netgame_equipment_element.flags))
            output_stream.write(struct.pack('<4h', netgame_equipment_element.type_0, netgame_equipment_element.type_1, netgame_equipment_element.type_2, netgame_equipment_element.type_3))
            output_stream.write(struct.pack('<2x4h', netgame_equipment_element.spawn_time, netgame_equipment_element.respawn_on_empty_time, netgame_equipment_element.respawn_timer_starts, netgame_equipment_element.classification))
            output_stream.write(struct.pack('<42xfff', netgame_equipment_element.position[0], netgame_equipment_element.position[1], netgame_equipment_element.position[2]))
            output_stream.write(struct.pack('<fff', netgame_equipment_element.orientation[0], netgame_equipment_element.orientation[1], netgame_equipment_element.orientation[2]))
            netgame_equipment_element.item_vehicle_collection.write(output_stream, False, True)
            output_stream.write(struct.pack('<48x'))

        for netgame_equipment_element in SCENARIO.netgame_equipment:
            netgame_equipment_element.ntor_header.write(output_stream, TAG, True)
            item_vehicle_collection_name_length = len(netgame_equipment_element.item_vehicle_collection.name)
            if item_vehicle_collection_name_length > 0:
                output_stream.write(struct.pack('<%ssx' % item_vehicle_collection_name_length, tag_format.string_to_bytes(netgame_equipment_element.item_vehicle_collection.name, False)))

def write_starting_equipment(output_stream, SCENARIO, TAG):
    if len(SCENARIO.starting_equipment) > 0:
        SCENARIO.starting_equipment_header.write(output_stream, TAG, True)
        for starting_equipment_element in SCENARIO.starting_equipment:
            output_stream.write(struct.pack('<I', starting_equipment_element.flags))
            output_stream.write(struct.pack('<4h', starting_equipment_element.type_0, starting_equipment_element.type_1, starting_equipment_element.type_2, starting_equipment_element.type_3))
            output_stream.write(struct.pack('<48x'))
            starting_equipment_element.item_collection_1.write(output_stream, False, True)
            starting_equipment_element.item_collection_2.write(output_stream, False, True)
            starting_equipment_element.item_collection_3.write(output_stream, False, True)
            starting_equipment_element.item_collection_4.write(output_stream, False, True)
            starting_equipment_element.item_collection_5.write(output_stream, False, True)
            starting_equipment_element.item_collection_6.write(output_stream, False, True)
            output_stream.write(struct.pack('<48x'))

        for starting_equipment_element in SCENARIO.starting_equipment:
            item_collection_1_name_length = len(starting_equipment_element.item_collection_1.name)
            item_collection_2_name_length = len(starting_equipment_element.item_collection_2.name)
            item_collection_3_name_length = len(starting_equipment_element.item_collection_3.name)
            item_collection_4_name_length = len(starting_equipment_element.item_collection_4.name)
            item_collection_5_name_length = len(starting_equipment_element.item_collection_5.name)
            item_collection_6_name_length = len(starting_equipment_element.item_collection_6.name)

            if item_collection_1_name_length > 0:
                output_stream.write(struct.pack('<%ssx' % item_collection_1_name_length, tag_format.string_to_bytes(starting_equipment_element.item_collection_1.name, False)))

            if item_collection_2_name_length > 0:
                output_stream.write(struct.pack('<%ssx' % item_collection_2_name_length, tag_format.string_to_bytes(starting_equipment_element.item_collection_2.name, False)))

            if item_collection_3_name_length > 0:
                output_stream.write(struct.pack('<%ssx' % item_collection_3_name_length, tag_format.string_to_bytes(starting_equipment_element.item_collection_3.name, False)))

            if item_collection_4_name_length > 0:
                output_stream.write(struct.pack('<%ssx' % item_collection_4_name_length, tag_format.string_to_bytes(starting_equipment_element.item_collection_4.name, False)))

            if item_collection_5_name_length > 0:
                output_stream.write(struct.pack('<%ssx' % item_collection_5_name_length, tag_format.string_to_bytes(starting_equipment_element.item_collection_5.name, False)))

            if item_collection_6_name_length > 0:
                output_stream.write(struct.pack('<%ssx' % item_collection_6_name_length, tag_format.string_to_bytes(starting_equipment_element.item_collection_6.name, False)))

def write_decals(output_stream, SCENARIO, TAG):
    if len(SCENARIO.decals) > 0:
        SCENARIO.decals_header.write(output_stream, TAG, True)
        for decal_element in SCENARIO.decals:
            output_stream.write(struct.pack('<h', decal_element.palette_index))
            output_stream.write(struct.pack('<b', decal_element.yaw))
            output_stream.write(struct.pack('<b', decal_element.pitch))
            output_stream.write(struct.pack('<fff', decal_element.position[0], decal_element.position[1], decal_element.position[2]))

def write_squad_groups(output_stream, SCENARIO, TAG):
    if len(SCENARIO.squad_groups) > 0:
        SCENARIO.squad_groups_header.write(output_stream, TAG, True)
        for squad_group_element in SCENARIO.squad_groups:
            output_stream.write(struct.pack('<31sx', tag_format.string_to_bytes(squad_group_element.name, False)))
            output_stream.write(struct.pack('<hh', squad_group_element.parent_index, squad_group_element.initial_order_index))

def write_squads(output_stream, SCENARIO, TAG):
    if len(SCENARIO.squads) > 0:
        SCENARIO.squads_header.write(output_stream, TAG, True)
        for squad in SCENARIO.squads:
            output_stream.write(struct.pack('<31sx', tag_format.string_to_bytes(squad.name, False)))
            output_stream.write(struct.pack('<I', squad.flags))
            output_stream.write(struct.pack('<h', squad.team))
            output_stream.write(struct.pack('<h', squad.parent_squad_group_index))
            output_stream.write(struct.pack('<f', squad.squad_delay_time))
            output_stream.write(struct.pack('<h', squad.normal_difficulty_count))
            output_stream.write(struct.pack('<h', squad.insane_difficulty_count))
            output_stream.write(struct.pack('<i', squad.major_upgrade))
            output_stream.write(struct.pack('<h', squad.vehicle_type_index))
            output_stream.write(struct.pack('<h', squad.character_type_index))
            output_stream.write(struct.pack('<h2x', squad.initial_zone_index))
            output_stream.write(struct.pack('<h', squad.initial_weapon_index))
            output_stream.write(struct.pack('<h', squad.initial_secondary_weapon_index))
            output_stream.write(struct.pack('<h', squad.grenade_type))
            output_stream.write(struct.pack('<h', squad.initial_order_index))
            output_stream.write(struct.pack('>i', len(squad.vehicle_variant)))
            squad.starting_locations_tag_block.write(output_stream, False)
            output_stream.write(struct.pack('<31sx', tag_format.string_to_bytes(squad.placement_script, False)))
            output_stream.write(struct.pack('<4x'))

        for squad in SCENARIO.squads:
            output_stream.write(struct.pack('<%ss' % len(squad.vehicle_variant), tag_format.string_to_bytes(squad.vehicle_variant, False)))

            if len(squad.starting_locations) > 0:
                squad.starting_locations_header.write(output_stream, TAG, True)
                for starting_location in squad.starting_locations:
                    output_stream.write(struct.pack('>i', len(starting_location.name)))
                    output_stream.write(struct.pack('<fff', starting_location.position[0], starting_location.position[1], starting_location.position[2]))
                    output_stream.write(struct.pack('<i', starting_location.reference_frame))
                    output_stream.write(struct.pack('<ff', radians(starting_location.facing[0]), radians(starting_location.facing[1])))
                    output_stream.write(struct.pack('<i', starting_location.flags))
                    output_stream.write(struct.pack('<h', starting_location.character_type_index))
                    output_stream.write(struct.pack('<h', starting_location.initial_weapon_index))
                    output_stream.write(struct.pack('<h2x', starting_location.initial_secondary_weapon_index))
                    output_stream.write(struct.pack('<h', starting_location.vehicle_type_index))
                    output_stream.write(struct.pack('<h', starting_location.seat_type))
                    output_stream.write(struct.pack('<h', starting_location.grenade_type))
                    output_stream.write(struct.pack('<h', starting_location.swarm_count))
                    output_stream.write(struct.pack('>i', len(starting_location.actor_variant)))
                    output_stream.write(struct.pack('>i', len(starting_location.vehicle_variant)))
                    output_stream.write(struct.pack('>f', starting_location.initial_movement_distance))
                    output_stream.write(struct.pack('<h', starting_location.emitter_vehicle_index))
                    output_stream.write(struct.pack('<h', starting_location.initial_movement_mode))
                    output_stream.write(struct.pack('<31sx', tag_format.string_to_bytes(starting_location.placement_script, False)))
                    output_stream.write(struct.pack('<4x'))

                for starting_location in squad.starting_locations:
                    output_stream.write(struct.pack('<%ss' % len(starting_location.name), tag_format.string_to_bytes(starting_location.name, False)))
                    output_stream.write(struct.pack('<%ss' % len(starting_location.actor_variant), tag_format.string_to_bytes(starting_location.actor_variant, False)))
                    output_stream.write(struct.pack('<%ss' % len(starting_location.vehicle_variant), tag_format.string_to_bytes(starting_location.vehicle_variant, False)))

def write_zones(output_stream, SCENARIO, TAG):
    if len(SCENARIO.zones) > 0:
        SCENARIO.zones_header.write(output_stream, TAG, True)
        for zone in SCENARIO.zones:
            output_stream.write(struct.pack('<31sx', tag_format.string_to_bytes(zone.name, False)))
            output_stream.write(struct.pack('<I', zone.flags))
            output_stream.write(struct.pack('<h2x', zone.manual_bsp_index))
            zone.firing_positions_tag_block.write(output_stream, False)
            zone.areas_tag_block.write(output_stream, False)

        for zone in SCENARIO.zones:
            if len(zone.firing_positions) > 0:
                zone.firing_positions_header.write(output_stream, TAG, True)
                for firing_position in zone.firing_positions:
                    output_stream.write(struct.pack('<fff', firing_position.position[0], firing_position.position[1], firing_position.position[2]))
                    output_stream.write(struct.pack('<h', firing_position.reference_frame))
                    output_stream.write(struct.pack('<H', firing_position.flags))
                    output_stream.write(struct.pack('<h', firing_position.area_index))
                    output_stream.write(struct.pack('<h', firing_position.cluster_index))
                    output_stream.write(struct.pack('<4x'))
                    output_stream.write(struct.pack('<ff', radians(firing_position.normal[0]), radians(firing_position.normal[1])))

            if len(zone.areas) > 0:
                zone.areas_header.write(output_stream, TAG, True)
                for area in zone.areas:
                    output_stream.write(struct.pack('<31sx', tag_format.string_to_bytes(area.name, False)))
                    output_stream.write(struct.pack('<I', area.flags))
                    output_stream.write(struct.pack('<20x'))
                    output_stream.write(struct.pack('<h', area.runtime_starting_index))
                    output_stream.write(struct.pack('<h', area.runtime_count))
                    output_stream.write(struct.pack('<64x'))
                    output_stream.write(struct.pack('<h', area.manual_reference_frame))
                    output_stream.write(struct.pack('<2x'))
                    area.flight_hints_tag_block.write(output_stream, False)

def write_scripting_data(output_stream, SCENARIO, TAG):
    if len(SCENARIO.scripting_data) > 0:
        SCENARIO.scripting_data_header.write(output_stream, TAG, True)
        for scripting_data in SCENARIO.scripting_data:
            scripting_data.point_sets_tag_block.write(output_stream, False)
            output_stream.write(struct.pack('>120x'))
            if len(scripting_data.point_sets) > 0:
                scripting_data.point_sets_header.write(output_stream, TAG, True)
                for point_set in scripting_data.point_sets:
                    output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(point_set.name, False)))
                    point_set.points_tag_block.write(output_stream, False)
                    output_stream.write(struct.pack('<h', point_set.bsp_index))
                    output_stream.write(struct.pack('<h', point_set.manual_reference_frame))
                    output_stream.write(struct.pack('<I', point_set.flags))

                for point_set in scripting_data.point_sets:
                    if len(point_set.points) > 0:
                        point_set.points_header.write(output_stream, TAG, True)
                        for point in point_set.points:
                            output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(point.name, False)))
                            output_stream.write(struct.pack('<fff', point.position[0], point.position[1], point.position[2]))
                            output_stream.write(struct.pack('<i', point.reference_frame))
                            output_stream.write(struct.pack('<i', point.surface_index))
                            output_stream.write(struct.pack('<ff', radians(point.facing_direction[0]), radians(point.facing_direction[1])))

def write_cutscene_flags(output_stream, SCENARIO, TAG):
    if len(SCENARIO.cutscene_flags) > 0:
        SCENARIO.cutscene_flags_header.write(output_stream, TAG, True)
        for cutscene_flag in SCENARIO.cutscene_flags:
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('>31sx', tag_format.string_to_bytes(cutscene_flag.name, False)))
            output_stream.write(struct.pack('<fff', cutscene_flag.position[0], cutscene_flag.position[1], cutscene_flag.position[2]))
            output_stream.write(struct.pack('<ff', radians(cutscene_flag.facing[0]), radians(cutscene_flag.facing[1])))

def write_cutscene_camera_points(output_stream, SCENARIO, TAG):
    if len(SCENARIO.cutscene_camera_points) > 0:
        SCENARIO.cutscene_camera_points_header.write(output_stream, TAG, True)
        for cutscene_camera_point in SCENARIO.cutscene_camera_points:
            output_stream.write(struct.pack('<h', cutscene_camera_point.flags))
            output_stream.write(struct.pack('<h', cutscene_camera_point.camera_type))
            output_stream.write(struct.pack('<31sx', tag_format.string_to_bytes(cutscene_camera_point.name, False)))
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('<fff', cutscene_camera_point.position[0], cutscene_camera_point.position[1], cutscene_camera_point.position[2]))
            output_stream.write(struct.pack('<fff', radians(cutscene_camera_point.orientation[0]), radians(cutscene_camera_point.orientation[1]), radians(cutscene_camera_point.orientation[2])))

def write_cutscene_titles(output_stream, SCENARIO, TAG):
    if len(SCENARIO.cutscene_titles) > 0:
        SCENARIO.cutscene_titles_header.write(output_stream, TAG, True)
        for cutscene_title in SCENARIO.cutscene_titles:
            output_stream.write(struct.pack('>I', len(cutscene_title.name)))
            output_stream.write(struct.pack('<4h', cutscene_title.text_bounds[1], cutscene_title.text_bounds[0], cutscene_title.text_bounds[3], cutscene_title.text_bounds[2]))
            output_stream.write(struct.pack('<h', cutscene_title.justification))
            output_stream.write(struct.pack('<h', cutscene_title.font))
            output_stream.write(struct.pack('<3Bx', cutscene_title.text_color[0], cutscene_title.text_color[1], cutscene_title.text_color[2]))
            output_stream.write(struct.pack('<3Bx', cutscene_title.shadow_color[0], cutscene_title.shadow_color[1], cutscene_title.shadow_color[2]))
            output_stream.write(struct.pack('<f', cutscene_title.fade_in_time))
            output_stream.write(struct.pack('<f', cutscene_title.up_time))
            output_stream.write(struct.pack('<f', cutscene_title.fade_out_time))

        for cutscene_title in SCENARIO.cutscene_titles:
                output_stream.write(struct.pack('<%ss' % len(cutscene_title.name), tag_format.string_to_bytes(cutscene_title.name, False)))

def write_structure_bsps(output_stream, SCENARIO, TAG):
    if len(SCENARIO.structure_bsps) > 0:
        SCENARIO.structure_bsps_header.write(output_stream, TAG, True)
        for structure_bsp in SCENARIO.structure_bsps:
            output_stream.write(struct.pack('>16x'))
            structure_bsp.structure_bsp.write(output_stream, False, True)
            structure_bsp.structure_lightmap.write(output_stream, False, True)
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('<f', structure_bsp.unused_radiance_estimated_search_distance))
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('<f', structure_bsp.unused_luminels_per_world_unit))
            output_stream.write(struct.pack('<f', structure_bsp.unused_output_white_reference))
            output_stream.write(struct.pack('<8x'))
            output_stream.write(struct.pack('<I', structure_bsp.flags))
            output_stream.write(struct.pack('<h2x', structure_bsp.default_sky))

        for structure_bsp_element in SCENARIO.structure_bsps:
            structure_bsp_name_length = len(structure_bsp_element.structure_bsp.name)
            structure_lightmap_name_length = len(structure_bsp_element.structure_lightmap.name)
            if structure_bsp_name_length > 0:
                output_stream.write(struct.pack('<%ssx' % structure_bsp_name_length, tag_format.string_to_bytes(structure_bsp_element.structure_bsp.name, False)))

            if structure_lightmap_name_length > 0:
                output_stream.write(struct.pack('<%ssx' % structure_lightmap_name_length, tag_format.string_to_bytes(structure_bsp_element.structure_lightmap.name, False)))

def write_orders(output_stream, SCENARIO, TAG):
    if len(SCENARIO.orders) > 0:
        SCENARIO.orders_header.write(output_stream, TAG, True)
        for order in SCENARIO.orders:
            output_stream.write(struct.pack('<31sx', tag_format.string_to_bytes(order.name, False)))
            output_stream.write(struct.pack('<h2x', order.style_index))
            output_stream.write(struct.pack('<I', order.flags))
            output_stream.write(struct.pack('<i', order.force_combat_status))
            output_stream.write(struct.pack('<31sx', tag_format.string_to_bytes(order.entry_script, False)))
            output_stream.write(struct.pack('<2xh', order.follow_squad))
            output_stream.write(struct.pack('<f', order.follow_radius))
            order.primary_area_set_tag_block.write(output_stream, False)
            order.secondary_area_set_tag_block.write(output_stream, False)
            order.secondary_set_trigger_tag_block.write(output_stream, False)
            order.special_movement_tag_block.write(output_stream, False)
            order.order_endings_tag_block.write(output_stream, False)

        for order in SCENARIO.orders:
            if len(order.primary_area_set) > 0:
                order.primary_area_set_header.write(output_stream, TAG, True)
                for primary_area_set in order.primary_area_set:
                    output_stream.write(struct.pack('<i', primary_area_set.area_type))
                    output_stream.write(struct.pack('<h', primary_area_set.zone_index))
                    output_stream.write(struct.pack('<h', primary_area_set.area_index))

            if len(order.order_endings) > 0:
                order.order_endings_header.write(output_stream, TAG, True)
                for order_ending in order.order_endings:
                    output_stream.write(struct.pack('<h', order_ending.next_order_index))
                    output_stream.write(struct.pack('<h', order_ending.combination_rule))
                    output_stream.write(struct.pack('<f', order_ending.delay_time))
                    output_stream.write(struct.pack('<i', order_ending.dialogue_type))
                    order_ending.triggers_tag_block.write(output_stream, False)

                for order_ending in order.order_endings:
                    if len(order_ending.triggers) > 0:
                        order_ending.triggers_header.write(output_stream, TAG, True)
                        for trigger in order_ending.triggers:
                            output_stream.write(struct.pack('<i', trigger.trigger_flags))
                            output_stream.write(struct.pack('<h2x', trigger.trigger_index))

def write_triggers(output_stream, SCENARIO, TAG):
    if len(SCENARIO.triggers) > 0:
        SCENARIO.triggers_header.write(output_stream, TAG, True)
        for trigger in SCENARIO.triggers:
            output_stream.write(struct.pack('<30s2x', tag_format.string_to_bytes(trigger.name, False)))
            output_stream.write(struct.pack('<I', trigger.trigger_flags))
            output_stream.write(struct.pack('<I', trigger.combination_rule))
            trigger.conditions_tag_block.write(output_stream, False)

        for trigger in SCENARIO.triggers:
            if len(trigger.conditions) > 0:
                trigger.conditions_header.write(output_stream, TAG, True)
                for condition in trigger.conditions:
                    output_stream.write(struct.pack('<h', condition.rule_type))
                    output_stream.write(struct.pack('<h', condition.squad_index))
                    output_stream.write(struct.pack('<h', condition.squad_group_index))
                    output_stream.write(struct.pack('<h', condition.a))
                    output_stream.write(struct.pack('<f', condition.x))
                    output_stream.write(struct.pack('<i', condition.trigger_volume_index))
                    output_stream.write(struct.pack('<30s2x', tag_format.string_to_bytes(condition.exit_condition_script, False)))
                    output_stream.write(struct.pack('<4x'))
                    output_stream.write(struct.pack('<I', condition.flags))

def write_background_sound_palette(output_stream, SCENARIO, TAG):
    if len(SCENARIO.background_sound_palette) > 0:
        SCENARIO.background_sound_palette_header.write(output_stream, TAG, True)
        for background_sound in SCENARIO.background_sound_palette:
            output_stream.write(struct.pack('<30s2x', tag_format.string_to_bytes(background_sound.name, False)))
            background_sound.background_sound.write(output_stream, False, True)
            background_sound.inside_cluster_sound.write(output_stream, False, True)
            output_stream.write(struct.pack('<20x'))
            output_stream.write(struct.pack('<f', background_sound.cutoff_distance))
            output_stream.write(struct.pack('<I', background_sound.scale_flags))
            output_stream.write(struct.pack('<f', background_sound.interior_scale))
            output_stream.write(struct.pack('<f', background_sound.portal_scale))
            output_stream.write(struct.pack('<f', background_sound.exterior_scale))
            output_stream.write(struct.pack('<f', background_sound.interpolation_speed))
            output_stream.write(struct.pack('<8x'))

        for background_sound in SCENARIO.background_sound_palette:
            background_sound_name_length = len(background_sound.background_sound.name)
            inside_cluster_sound_name_length = len(background_sound.inside_cluster_sound.name)
            if background_sound_name_length > 0:
                output_stream.write(struct.pack('<%ssx' % background_sound_name_length, tag_format.string_to_bytes(background_sound.background_sound.name, False)))

            if inside_cluster_sound_name_length > 0:
                output_stream.write(struct.pack('<%ssx' % inside_cluster_sound_name_length, tag_format.string_to_bytes(background_sound.inside_cluster_sound.name, False)))

def write_sound_environment_palette(output_stream, SCENARIO, TAG):
    if len(SCENARIO.sound_environment_palette) > 0:
        SCENARIO.sound_environment_palette_header.write(output_stream, TAG, True)
        for sound_environment in SCENARIO.sound_environment_palette:
            output_stream.write(struct.pack('<30s2x', tag_format.string_to_bytes(sound_environment.name, False)))
            sound_environment.sound_environment.write(output_stream, False, True)
            output_stream.write(struct.pack('<f', sound_environment.cutoff_distance))
            output_stream.write(struct.pack('<f', sound_environment.interpolation_speed))
            output_stream.write(struct.pack('<24x'))

        for sound_environment in SCENARIO.sound_environment_palette:
            sound_environment_name_length = len(sound_environment.sound_environment.name)
            if sound_environment_name_length > 0:
                output_stream.write(struct.pack('<%ssx' % sound_environment_name_length, tag_format.string_to_bytes(sound_environment.sound_environment.name, False)))

def write_crates(output_stream, SCENARIO, TAG):
    if len(SCENARIO.crates) > 0:
        SCENARIO.crates_header.write(output_stream, TAG, True)
        for crate_element in SCENARIO.crates:
            write_object(output_stream, crate_element)
            output_stream.write(struct.pack('>I', len(crate_element.variant_name)))
            write_color_change(output_stream, crate_element)

        for crate_element in SCENARIO.crates:
            crate_element.sobj_header.write(output_stream, TAG, True)
            crate_element.obj0_header.write(output_stream, TAG, True)
            crate_element.sper_header.write(output_stream, TAG, True)
            variant_count = len(crate_element.variant_name)
            if variant_count > 0:
                output_stream.write(struct.pack('<%ss' % variant_count, tag_format.string_to_bytes(crate_element.variant_name, False)))

def write_palette(output_stream, palette, palette_header, size, TAG):
    if len(palette) > 0:
        palette_header.write(output_stream, TAG, True)
        for palette_element in palette:
            palette_element.write(output_stream, False, True)
            output_stream.write(struct.pack('<%sx' % size))

        for palette_element in palette:
            palette_name_length = len(palette_element.name)
            if palette_name_length > 0:
                output_stream.write(struct.pack('<%ssx' % palette_name_length, tag_format.string_to_bytes(palette_element.name, False)))

def build_asset(output_stream, SCENARIO, report):
    TAG = tag_format.TagAsset()
    TAG.big_endian = False

    SCENARIO.header.write(output_stream, False, True)
    write_body(output_stream, SCENARIO, TAG)

    write_palette(output_stream, SCENARIO.skies, SCENARIO.skies_header, 0, TAG)

    write_palette(output_stream, SCENARIO.child_scenarios, SCENARIO.child_scenario_header, 16, TAG)

    write_comments(output_stream, SCENARIO, TAG)

    write_object_names(output_stream, SCENARIO, TAG)

    write_scenery(output_stream, SCENARIO, TAG)
    write_palette(output_stream, SCENARIO.scenery_palette, SCENARIO.scenery_palette_header, 32, TAG)

    write_units(output_stream, SCENARIO.bipeds, SCENARIO.bipeds_header, TAG)
    write_palette(output_stream, SCENARIO.biped_palette, SCENARIO.biped_palette_header, 32, TAG)

    write_units(output_stream, SCENARIO.vehicles, SCENARIO.vehicles_header, TAG)
    write_palette(output_stream, SCENARIO.vehicle_palette, SCENARIO.vehicle_palette_header, 32, TAG)

    write_equipment(output_stream, SCENARIO, TAG)
    write_palette(output_stream, SCENARIO.equipment_palette, SCENARIO.equipment_palette_header, 32, TAG)

    write_weapons(output_stream, SCENARIO, TAG)
    write_palette(output_stream, SCENARIO.weapon_palette, SCENARIO.weapon_palette_header, 32, TAG)

    write_device_groups(output_stream, SCENARIO, TAG)

    write_machines(output_stream, SCENARIO, TAG)
    write_palette(output_stream, SCENARIO.device_machine_palette, SCENARIO.device_machine_palette_header, 32, TAG)

    write_controls(output_stream, SCENARIO, TAG)
    write_palette(output_stream, SCENARIO.device_control_palette, SCENARIO.device_control_palette_header, 32, TAG)

    write_light_fixtures(output_stream, SCENARIO, TAG)
    write_palette(output_stream, SCENARIO.device_light_fixtures_palette, SCENARIO.device_light_fixture_palette_header, 32, TAG)

    write_sound_scenery(output_stream, SCENARIO, TAG)
    write_palette(output_stream, SCENARIO.sound_scenery_palette, SCENARIO.sound_scenery_palette_header, 32, TAG)

    write_light_volumes(output_stream, SCENARIO, TAG)
    write_palette(output_stream, SCENARIO.light_volume_palette, SCENARIO.light_volume_palette_header, 32, TAG)

    write_player_starting_profiles(output_stream, SCENARIO, TAG)

    write_player_starting_locations(output_stream, SCENARIO, TAG)

    write_trigger_volumes(output_stream, SCENARIO, TAG)

    write_recorded_animations(output_stream, SCENARIO, TAG)

    write_netgame_flags(output_stream, SCENARIO, TAG)

    write_netgame_equipment(output_stream, SCENARIO, TAG)

    write_starting_equipment(output_stream, SCENARIO, TAG)

    write_decals(output_stream, SCENARIO, TAG)
    write_palette(output_stream, SCENARIO.decal_palette, SCENARIO.decal_palette_header, 0, TAG)

    write_palette(output_stream, SCENARIO.style_palette, SCENARIO.style_palette_header, 0, TAG)

    write_squad_groups(output_stream, SCENARIO, TAG)

    write_squads(output_stream, SCENARIO, TAG)

    write_zones(output_stream, SCENARIO, TAG)

    write_palette(output_stream, SCENARIO.character_palette, SCENARIO.character_palette_header, 0, TAG)

    write_scripting_data(output_stream, SCENARIO, TAG)

    write_cutscene_flags(output_stream, SCENARIO, TAG)

    write_cutscene_camera_points(output_stream, SCENARIO, TAG)

    write_cutscene_titles(output_stream, SCENARIO, TAG)

    write_structure_bsps(output_stream, SCENARIO, TAG)

    write_orders(output_stream, SCENARIO, TAG)

    write_triggers(output_stream, SCENARIO, TAG)

    write_background_sound_palette(output_stream, SCENARIO, TAG)

    write_sound_environment_palette(output_stream, SCENARIO, TAG)

    write_crates(output_stream, SCENARIO, TAG)
    write_palette(output_stream, SCENARIO.crates_palette, SCENARIO.crates_palette_header, 32, TAG)
