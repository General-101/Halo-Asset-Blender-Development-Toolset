# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Steven Garcia
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

def write_tag_header(output_stream, SCENARIO):
    output_stream.write(struct.pack('<h', SCENARIO.header.unk1))
    output_stream.write(struct.pack('<b', SCENARIO.header.flags))
    output_stream.write(struct.pack('<b', SCENARIO.header.type))
    output_stream.write(struct.pack('<32s', SCENARIO.header.name))
    output_stream.write(struct.pack('<4s', SCENARIO.header.tag_group))
    output_stream.write(struct.pack('<I', SCENARIO.header.checksum))
    output_stream.write(struct.pack('<I', SCENARIO.header.data_offset))
    output_stream.write(struct.pack('<I', SCENARIO.header.data_length))
    output_stream.write(struct.pack('<I', SCENARIO.header.unk2))
    output_stream.write(struct.pack('<H', SCENARIO.header.version))
    output_stream.write(struct.pack('<b', SCENARIO.header.destination))
    output_stream.write(struct.pack('<b', SCENARIO.header.plugin_handle))
    output_stream.write(struct.pack('<4s', SCENARIO.header.engine_tag))

def write_tag_block_header(output_stream, header):
    output_stream.write(struct.pack('<4s3I', header.name, header.version, header.count, header.size))

def write_tag_reference(output_stream, tag_reference):
    output_stream.write(struct.pack('<4s4xii', tag_reference.tag_group, tag_reference.name_length, tag_reference.index))

def write_tag_block(output_stream, tag_block):
    output_stream.write(struct.pack('<iII', tag_block.count, tag_block.address, tag_block.definition))

def write_tag_data(output_stream, tag_data):
    output_stream.write(struct.pack('<iiIII', tag_data.size, tag_data.flags, tag_data.raw_pointer, tag_data.pointer, tag_data.id))

def write_body(output_stream, SCENARIO):
    write_tag_block_header(output_stream, SCENARIO.scenario_body_header)
    write_tag_reference(output_stream, SCENARIO.scenario_body.unused_tag_ref)
    write_tag_block(output_stream, SCENARIO.scenario_body.skies_tag_block)
    output_stream.write(struct.pack('<HH', SCENARIO.scenario_body.scenario_type, SCENARIO.scenario_body.scenario_flags))
    write_tag_block(output_stream, SCENARIO.scenario_body.child_scenarios_tag_block)
    output_stream.write(struct.pack('<f', SCENARIO.scenario_body.local_north))
    write_tag_block(output_stream, SCENARIO.scenario_body.predicted_resources_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.functions_tag_block)
    write_tag_data(output_stream, SCENARIO.scenario_body.editor_scenario_data)
    write_tag_block(output_stream, SCENARIO.scenario_body.comments_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.environment_objects_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.object_names_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.scenery_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.scenery_palette_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.bipeds_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.biped_palette_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.vehicles_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.vehicle_palette_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.equipment_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.equipment_palette_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.weapons_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.weapon_palette_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.device_groups_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.machines_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.machine_palette_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.controls_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.control_palette_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.light_fixtures_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.light_fixtures_palette_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.sound_scenery_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.sound_scenery_palette_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.light_volumes_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.light_volume_palette_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.player_starting_profile_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.player_starting_locations_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.trigger_volumes_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.recorded_animations_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.netgame_flags_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.netgame_equipment_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.starting_equipment_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.bsp_switch_trigger_volumes_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.decals_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.decal_palette_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.detail_object_collection_palette_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.style_palette_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.squad_groups_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.squads_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.zones_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.mission_scenes_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.character_palette_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.ai_pathfinding_data_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.ai_animation_references_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.ai_script_references_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.ai_recording_references_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.ai_conversations_tag_block)
    write_tag_data(output_stream, SCENARIO.scenario_body.script_syntax_data_tag_data)
    write_tag_data(output_stream, SCENARIO.scenario_body.script_string_data_tag_data)
    write_tag_block(output_stream, SCENARIO.scenario_body.scripts_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.globals_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.references_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.source_files_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.scripting_data_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.cutscene_flags_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.cutscene_camera_points_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.cutscene_titles_tag_block)
    write_tag_reference(output_stream, SCENARIO.scenario_body.custom_object_names_tag_ref)
    write_tag_reference(output_stream, SCENARIO.scenario_body.chapter_title_text_tag_ref)
    write_tag_reference(output_stream, SCENARIO.scenario_body.hud_messages_tag_ref)
    write_tag_block(output_stream, SCENARIO.scenario_body.structure_bsps_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.scenario_resources_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.old_structure_physics_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.hs_unit_seats_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.scenario_kill_triggers_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.hs_syntax_datums_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.orders_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.triggers_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.background_sound_palette_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.sound_environment_palette_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.weather_palette_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.unused_0_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.unused_1_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.unused_2_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.unused_3_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.scavenger_hunt_objects_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.scenario_cluster_data_tag_block)
    for salt in SCENARIO.scenario_body.salt_array:
        output_stream.write(struct.pack('<i', salt))

    write_tag_block(output_stream, SCENARIO.scenario_body.spawn_data_tag_block)
    write_tag_reference(output_stream, SCENARIO.scenario_body.sound_effect_collection_tag_ref)
    write_tag_block(output_stream, SCENARIO.scenario_body.crates_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.crate_palette_tag_block)
    write_tag_reference(output_stream, SCENARIO.scenario_body.global_lighting_tag_ref)
    write_tag_block(output_stream, SCENARIO.scenario_body.atmospheric_fog_palette_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.planar_fog_palette_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.flocks_tag_block)
    write_tag_reference(output_stream, SCENARIO.scenario_body.subtitles_tag_ref)
    write_tag_block(output_stream, SCENARIO.scenario_body.decorators_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.creatures_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.creature_palette_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.decorator_palette_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.bsp_transition_volumes_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.structure_bsp_lighting_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.editor_folders_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.level_data_tag_block)
    write_tag_reference(output_stream, SCENARIO.scenario_body.game_engine_strings_tag_ref)
    output_stream.write(struct.pack('<8x'))
    write_tag_block(output_stream, SCENARIO.scenario_body.mission_dialogue_tag_block)
    write_tag_reference(output_stream, SCENARIO.scenario_body.objectives_tag_ref)
    write_tag_block(output_stream, SCENARIO.scenario_body.interpolators_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.shared_references_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.screen_effect_references_tag_block)
    write_tag_block(output_stream, SCENARIO.scenario_body.simulation_definition_table_tag_block)

def write_object_names(output_stream, SCENARIO):
    if len(SCENARIO.object_names) > 0:
        write_tag_block_header(output_stream, SCENARIO.object_name_header)
        for object_name_element in SCENARIO.object_names:
            output_stream.write(struct.pack('<31sxhh', object_name_element.name, object_name_element.object_type, object_name_element.placement_index))

def write_object(output_stream, scenery_element):
    output_stream.write(struct.pack('<h', scenery_element.palette_index))
    output_stream.write(struct.pack('<h', scenery_element.name_index))
    output_stream.write(struct.pack('<I', scenery_element.placement_flags))
    output_stream.write(struct.pack('<fff', scenery_element.position[0], scenery_element.position[1], scenery_element.position[2]))
    output_stream.write(struct.pack('<fff', scenery_element.rotation[0], scenery_element.rotation[1], scenery_element.rotation[2]))
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


def write_scenery(output_stream, SCENARIO):
    if len(SCENARIO.scenery) > 0:
        write_tag_block_header(output_stream, SCENARIO.scenery_header)
        for scenery_element in SCENARIO.scenery:
            write_object(output_stream, scenery_element)
            output_stream.write(struct.pack('>I', scenery_element.variant_name_length))
            write_color_change(output_stream, scenery_element)
            output_stream.write(struct.pack('<h', scenery_element.pathfinding_policy))
            output_stream.write(struct.pack('<h', scenery_element.lightmap_policy))
            output_stream.write(struct.pack('<14x'))
            output_stream.write(struct.pack('<h', scenery_element.valid_multiplayer_games))

        for scenery_element in SCENARIO.scenery:
            write_tag_block_header(output_stream, scenery_element.sobj_header)
            write_tag_block_header(output_stream, scenery_element.obj0_header)
            write_tag_block_header(output_stream, scenery_element.sper_header)
            write_tag_block_header(output_stream, scenery_element.sct3_header)

def write_units(output_stream, unit_list, unit_header):
    if len(unit_list) > 0:
        write_tag_block_header(output_stream, unit_header)
        for unit_element in unit_list:
            write_object(output_stream, unit_element)
            output_stream.write(struct.pack('>I', unit_element.variant_name_length))
            write_color_change(output_stream, unit_element)
            output_stream.write(struct.pack('<f', unit_element.body_vitality))
            output_stream.write(struct.pack('<I', unit_element.flags))

        for unit_element in unit_list:
            write_tag_block_header(output_stream, unit_element.sobj_header)
            write_tag_block_header(output_stream, unit_element.obj0_header)
            write_tag_block_header(output_stream, unit_element.sper_header)
            write_tag_block_header(output_stream, unit_element.sunt_header)

def write_equipment(output_stream, SCENARIO):
    if len(SCENARIO.equipment) > 0:
        write_tag_block_header(output_stream, SCENARIO.equipment_header)
        for equipment_element in SCENARIO.equipment:
            write_object(output_stream, equipment_element)
            output_stream.write(struct.pack('<I', equipment_element.flags))

        for equipment_element in SCENARIO.equipment:
            write_tag_block_header(output_stream, equipment_element.sobj_header)
            write_tag_block_header(output_stream, equipment_element.obj0_header)
            write_tag_block_header(output_stream, equipment_element.seqt_header)

def write_weapons(output_stream, SCENARIO):
    if len(SCENARIO.weapons) > 0:
        write_tag_block_header(output_stream, SCENARIO.weapon_header)
        for weapon_element in SCENARIO.weapons:
            write_object(output_stream, weapon_element)
            output_stream.write(struct.pack('>I', weapon_element.variant_name_length))
            write_color_change(output_stream, weapon_element)
            output_stream.write(struct.pack('<h', weapon_element.rounds_left))
            output_stream.write(struct.pack('<h', weapon_element.rounds_loaded))
            output_stream.write(struct.pack('<I', weapon_element.flags))

        for weapon_element in SCENARIO.weapons:
            write_tag_block_header(output_stream, weapon_element.sobj_header)
            write_tag_block_header(output_stream, weapon_element.obj0_header)
            write_tag_block_header(output_stream, weapon_element.sper_header)
            write_tag_block_header(output_stream, weapon_element.swpt_header)

def write_trigger_volumes(output_stream, SCENARIO):
    if len(SCENARIO.trigger_volumes) > 0:
        write_tag_block_header(output_stream, SCENARIO.trigger_volumes_header)
        for trigger_volume_element in SCENARIO.trigger_volumes:
            output_stream.write(struct.pack('>i', trigger_volume_element.name_length))
            output_stream.write(struct.pack('<i', trigger_volume_element.object_name_index))
            output_stream.write(struct.pack('>i', trigger_volume_element.node_name_length))

            output_stream.write(struct.pack('<fff', trigger_volume_element.forward[0], trigger_volume_element.forward[1], trigger_volume_element.forward[2]))
            output_stream.write(struct.pack('<fff', trigger_volume_element.up[0], trigger_volume_element.up[1], trigger_volume_element.up[2]))
            output_stream.write(struct.pack('<fff', trigger_volume_element.position[0], trigger_volume_element.position[1], trigger_volume_element.position[2]))
            output_stream.write(struct.pack('<fff', trigger_volume_element.extents[0], trigger_volume_element.extents[1], trigger_volume_element.extents[2]))
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('<h', trigger_volume_element.kill_trigger_volume_index))
            output_stream.write(struct.pack('<2x'))

        for trigger_volume_element in SCENARIO.trigger_volumes:
            output_stream.write(struct.pack('<%ss' % trigger_volume_element.name_length, trigger_volume_element.name))

def write_decals(output_stream, SCENARIO):
    if len(SCENARIO.decals) > 0:
        write_tag_block_header(output_stream, SCENARIO.decals_header)
        for decal_element in SCENARIO.decals:
            output_stream.write(struct.pack('<h', decal_element.palette_index))
            output_stream.write(struct.pack('<b', decal_element.yaw))
            output_stream.write(struct.pack('<b', decal_element.pitch))
            output_stream.write(struct.pack('<fff', decal_element.position[0], decal_element.position[1], decal_element.position[2]))

def write_squad_groups(output_stream, SCENARIO):
    if len(SCENARIO.squad_groups) > 0:
        write_tag_block_header(output_stream, SCENARIO.squad_groups_header)
        for squad_group_element in SCENARIO.squad_groups:
            output_stream.write(struct.pack('<31sx', squad_group_element.name))
            output_stream.write(struct.pack('<hh', squad_group_element.parent_index, squad_group_element.initial_order_index))

def write_squads(output_stream, SCENARIO):
    if len(SCENARIO.squads) > 0:
        write_tag_block_header(output_stream, SCENARIO.squads_header)
        for squad in SCENARIO.squads:
            output_stream.write(struct.pack('<31sx', squad.name))
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
            output_stream.write(struct.pack('>i', squad.vehicle_variant_length))
            write_tag_block(output_stream, squad.starting_locations_tag_block)
            output_stream.write(struct.pack('<31sx', squad.placement_script))
            output_stream.write(struct.pack('<4x'))

        for squad in SCENARIO.squads:
            if len(squad.starting_locations) > 0:
                write_tag_block_header(output_stream, squad.starting_locations_header)
                for starting_location in squad.starting_locations:
                    output_stream.write(struct.pack('>i', starting_location.name_length))
                    output_stream.write(struct.pack('<fff', starting_location.position[0], starting_location.position[1], starting_location.position[2]))
                    output_stream.write(struct.pack('<i', starting_location.reference_frame))
                    output_stream.write(struct.pack('<ff', starting_location.facing_y, starting_location.facing_p))
                    output_stream.write(struct.pack('<i', starting_location.flags))
                    output_stream.write(struct.pack('<h', starting_location.character_type_index))
                    output_stream.write(struct.pack('<h', starting_location.initial_weapon_index))
                    output_stream.write(struct.pack('<h2x', starting_location.initial_secondary_weapon_index))
                    output_stream.write(struct.pack('<h', starting_location.vehicle_type_index))
                    output_stream.write(struct.pack('<h', starting_location.seat_type))
                    output_stream.write(struct.pack('<h', starting_location.grenade_type))
                    output_stream.write(struct.pack('<h', starting_location.swarm_count))
                    output_stream.write(struct.pack('>i', starting_location.actor_variant_name_length))
                    output_stream.write(struct.pack('>i', starting_location.vehicle_variant_name_length))
                    output_stream.write(struct.pack('>f', starting_location.initial_movement_distance))
                    output_stream.write(struct.pack('<h', starting_location.emitter_vehicle_index))
                    output_stream.write(struct.pack('<h', starting_location.initial_movement_mode))
                    output_stream.write(struct.pack('<31sx', starting_location.placement_script))
                    output_stream.write(struct.pack('<4x'))

                for starting_location in squad.starting_locations:
                    output_stream.write(struct.pack('<%ss' % starting_location.name_length, starting_location.name))

def write_zones(output_stream, SCENARIO):
    if len(SCENARIO.zones) > 0:
        write_tag_block_header(output_stream, SCENARIO.zones_header)
        for zone in SCENARIO.zones:
            output_stream.write(struct.pack('<31sx', zone.name))
            output_stream.write(struct.pack('<I', zone.flags))
            output_stream.write(struct.pack('<h2x', zone.manual_bsp_index))
            write_tag_block(output_stream, zone.firing_positions_tag_block)
            write_tag_block(output_stream, zone.areas_tag_block)

        for zone in SCENARIO.zones:
            if len(zone.firing_positions) > 0:
                write_tag_block_header(output_stream, zone.firing_positions_header)
                for firing_position in zone.firing_positions:
                    output_stream.write(struct.pack('<fff', firing_position.position[0], firing_position.position[1], firing_position.position[2]))
                    output_stream.write(struct.pack('<h', firing_position.reference_frame))
                    output_stream.write(struct.pack('<H', firing_position.flags))
                    output_stream.write(struct.pack('<h', firing_position.area_index))
                    output_stream.write(struct.pack('<h', firing_position.cluster_index))
                    output_stream.write(struct.pack('<4x'))
                    output_stream.write(struct.pack('<ff', firing_position.normal_y, 0.0))

            if len(zone.areas) > 0:
                write_tag_block_header(output_stream, zone.areas_header)
                for area in zone.areas:
                    output_stream.write(struct.pack('<31sx', area.name))
                    output_stream.write(struct.pack('<I', area.flags))
                    output_stream.write(struct.pack('<20x'))
                    output_stream.write(struct.pack('<h', area.runtime_starting_index))
                    output_stream.write(struct.pack('<h', area.runtime_count))
                    output_stream.write(struct.pack('<64x'))
                    output_stream.write(struct.pack('<h', area.manual_reference_frame))
                    output_stream.write(struct.pack('<2x'))
                    write_tag_block(output_stream, area.flight_hints_tag_block)

def write_scripting_data(output_stream, SCENARIO):
    if len(SCENARIO.scripting_data) > 0:
        write_tag_block_header(output_stream, SCENARIO.scripting_data_header)
        for scripting_data in SCENARIO.scripting_data:
            write_tag_block(output_stream, scripting_data.point_sets_tag_block)
            output_stream.write(struct.pack('>120x'))
            if len(scripting_data.point_sets) > 0:
                write_tag_block_header(output_stream, scripting_data.point_sets_header)
                for point_set in scripting_data.point_sets:
                    output_stream.write(struct.pack('>31sx', point_set.name))
                    write_tag_block(output_stream, point_set.points_tag_block)
                    output_stream.write(struct.pack('<h', point_set.bsp_index))
                    output_stream.write(struct.pack('<h', point_set.manual_reference_frame))
                    output_stream.write(struct.pack('<I', point_set.flags))

                for point_set in scripting_data.point_sets:
                    if len(point_set.points) > 0:
                        write_tag_block_header(output_stream, point_set.points_header)
                        for point in point_set.points:
                            output_stream.write(struct.pack('>31sx', point.name))
                            output_stream.write(struct.pack('<fff', point.position[0], point.position[1], point.position[2]))
                            output_stream.write(struct.pack('<i', point.reference_frame))
                            output_stream.write(struct.pack('<i', point.surface_index))
                            output_stream.write(struct.pack('<ff', point.facing_direction_y, point.facing_direction_p))

def write_cutscene_flags(output_stream, SCENARIO):
    if len(SCENARIO.cutscene_flags) > 0:
        write_tag_block_header(output_stream, SCENARIO.cutscene_flags_header)
        for cutscene_flag in SCENARIO.cutscene_flags:
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('>31sx', cutscene_flag.name))
            output_stream.write(struct.pack('<fff', cutscene_flag.position[0], cutscene_flag.position[1], cutscene_flag.position[2]))
            output_stream.write(struct.pack('<ff', cutscene_flag.facing_y, cutscene_flag.facing_p))

def write_cutscene_camera_points(output_stream, SCENARIO):
    if len(SCENARIO.cutscene_camera_points) > 0:
        write_tag_block_header(output_stream, SCENARIO.cutscene_camera_points_header)
        for cutscene_camera_point in SCENARIO.cutscene_camera_points:
            output_stream.write(struct.pack('<h', cutscene_camera_point.flags))
            output_stream.write(struct.pack('<h', cutscene_camera_point.camera_type))
            output_stream.write(struct.pack('<31sx', cutscene_camera_point.name))
            output_stream.write(struct.pack('<4x'))
            output_stream.write(struct.pack('<fff', cutscene_camera_point.position[0], cutscene_camera_point.position[1], cutscene_camera_point.position[2]))
            output_stream.write(struct.pack('<fff', cutscene_camera_point.orientation[0], cutscene_camera_point.orientation[1], cutscene_camera_point.orientation[2]))

def write_orders(output_stream, SCENARIO):
    if len(SCENARIO.orders) > 0:
        write_tag_block_header(output_stream, SCENARIO.orders_header)
        for order in SCENARIO.orders:
            output_stream.write(struct.pack('<31sx', order.name))
            output_stream.write(struct.pack('<h2x', order.style_index))
            output_stream.write(struct.pack('<I', order.flags))
            output_stream.write(struct.pack('<i', order.force_combat_status))
            output_stream.write(struct.pack('<31sx', order.entry_script))
            output_stream.write(struct.pack('<2xh', order.follow_squad))
            output_stream.write(struct.pack('<f', order.follow_radius))
            write_tag_block(output_stream, order.primary_area_set_tag_block)
            write_tag_block(output_stream, order.secondary_area_set_tag_block)
            write_tag_block(output_stream, order.secondary_set_trigger_tag_block)
            write_tag_block(output_stream, order.special_movement_tag_block)
            write_tag_block(output_stream, order.order_endings_tag_block)

        for order in SCENARIO.orders:
            if len(order.primary_area_set) > 0:
                write_tag_block_header(output_stream, order.primary_area_set_header)
                for primary_area_set in order.primary_area_set:
                    output_stream.write(struct.pack('<i', primary_area_set.area_type))
                    output_stream.write(struct.pack('<h', primary_area_set.zone_index))
                    output_stream.write(struct.pack('<h', primary_area_set.area_index))

            if len(order.order_endings) > 0:
                write_tag_block_header(output_stream, order.order_endings_header)
                for order_ending in order.order_endings:
                    output_stream.write(struct.pack('<h', order_ending.next_order_index))
                    output_stream.write(struct.pack('<h', order_ending.combination_rule))
                    output_stream.write(struct.pack('<f', order_ending.delay_time))
                    output_stream.write(struct.pack('<i', order_ending.dialogue_type))
                    write_tag_block(output_stream, order_ending.triggers_tag_block)

                for order_ending in order.order_endings:
                    if len(order_ending.triggers) > 0:
                        write_tag_block_header(output_stream, order_ending.triggers_header)
                        for trigger in order_ending.triggers:
                            output_stream.write(struct.pack('<i', trigger.trigger_flags))
                            output_stream.write(struct.pack('<h2x', trigger.trigger_index))

def write_triggers(output_stream, SCENARIO):
    if len(SCENARIO.triggers) > 0:
        write_tag_block_header(output_stream, SCENARIO.triggers_header)
        for trigger in SCENARIO.triggers:
            output_stream.write(struct.pack('<30s2x', trigger.name))
            output_stream.write(struct.pack('<I', trigger.trigger_flags))
            output_stream.write(struct.pack('<I', trigger.combination_rule))
            write_tag_block(output_stream, trigger.conditions_tag_block)

        for trigger in SCENARIO.triggers:
            if len(trigger.conditions) > 0:
                write_tag_block_header(output_stream, trigger.conditions_header)
                for condition in trigger.conditions:
                    output_stream.write(struct.pack('<h', condition.rule_type))
                    output_stream.write(struct.pack('<h', condition.squad_index))
                    output_stream.write(struct.pack('<h', condition.squad_group_index))
                    output_stream.write(struct.pack('<h', condition.a))
                    output_stream.write(struct.pack('<f', condition.x))
                    output_stream.write(struct.pack('<i', condition.trigger_volume_index))
                    output_stream.write(struct.pack('<30s2x', condition.exit_condition_script))
                    output_stream.write(struct.pack('<4x'))
                    output_stream.write(struct.pack('<I', condition.flags))

def write_palette(output_stream, palette, palette_header, size):
    if len(palette) > 0:
        write_tag_block_header(output_stream, palette_header)
        for palette_element in palette:
            write_tag_reference(output_stream, palette_element)
            output_stream.write(struct.pack('<%sx' % size))

        for palette_element in palette:
            output_stream.write(struct.pack('<%ssx' % palette_element.name_length, palette_element.name))

def build_asset(output_stream, SCENARIO, report):
    write_tag_header(output_stream, SCENARIO)
    write_body(output_stream, SCENARIO)

    write_object_names(output_stream, SCENARIO)

    write_scenery(output_stream, SCENARIO)
    write_palette(output_stream, SCENARIO.scenery_palette, SCENARIO.scenery_palette_header, 32)

    write_units(output_stream, SCENARIO.bipeds, SCENARIO.bipeds_header)
    write_palette(output_stream, SCENARIO.biped_palette, SCENARIO.biped_palette_header, 32)

    write_units(output_stream, SCENARIO.vehicles, SCENARIO.vehicles_header)
    write_palette(output_stream, SCENARIO.vehicle_palette, SCENARIO.vehicle_palette_header, 32)

    write_equipment(output_stream, SCENARIO)
    write_palette(output_stream, SCENARIO.equipment_palette, SCENARIO.equipment_palette_header, 32)

    write_weapons(output_stream, SCENARIO)
    write_palette(output_stream, SCENARIO.weapon_palette, SCENARIO.weapon_palette_header, 32)

    write_trigger_volumes(output_stream, SCENARIO)

    write_decals(output_stream, SCENARIO)
    write_palette(output_stream, SCENARIO.decal_palette, SCENARIO.decal_palette_header, 0)

    write_palette(output_stream, SCENARIO.style_palette, SCENARIO.style_palette_header, 0)

    write_squad_groups(output_stream, SCENARIO)

    write_squads(output_stream, SCENARIO)

    write_zones(output_stream, SCENARIO)

    write_palette(output_stream, SCENARIO.character_palette, SCENARIO.character_palette_header, 0)

    write_scripting_data(output_stream, SCENARIO)

    write_cutscene_flags(output_stream, SCENARIO)

    write_cutscene_camera_points(output_stream, SCENARIO)

    write_orders(output_stream, SCENARIO)

    write_triggers(output_stream, SCENARIO)
