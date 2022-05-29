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

from .format import SALT_SIZE

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

def write_scenery_palette(output_stream, SCENARIO):
    if len(SCENARIO.scenery_palette) > 0:
        write_tag_block_header(output_stream, SCENARIO.scenery_palette_header)
        for scenery_palette_element in SCENARIO.scenery_palette:
            write_tag_reference(output_stream, scenery_palette_element)
            output_stream.write(struct.pack('<32x'))

        for scenery_palette_element in SCENARIO.scenery_palette:
            output_stream.write(struct.pack('<%ssx' % scenery_palette_element.name_length, scenery_palette_element.name))

def build_asset(output_stream, SCENARIO, report):
    write_tag_header(output_stream, SCENARIO)
    write_body(output_stream, SCENARIO)
    write_object_names(output_stream, SCENARIO)
    write_scenery_palette(output_stream, SCENARIO)
