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

import os
import json
import struct

from math import degrees, radians
from .format import ScenarioAsset, SALT_SIZE

DEBUG_PARSER = True
DEBUG_HEADER = True
DEBUG_BODY = True

def tag_block_header(TAG, header_group, version, count, size):
    TAGBLOCKHEADER = TAG.TagBlockHeader()
    TAGBLOCKHEADER.name = TAG.string_to_bytes(header_group, True)
    TAGBLOCKHEADER.version = version
    TAGBLOCKHEADER.count = count
    TAGBLOCKHEADER.size = size

    return TAGBLOCKHEADER

def get_object_names(dump_dic, TAG, SCENARIO):
    object_name_tag_block = dump_dic['Data']['Object Names']
    SCENARIO.object_names = []
    for object_name_element in object_name_tag_block:
        object_name = SCENARIO.ObjectName()
        object_name.name = TAG.string_to_bytes(object_name_element['Name'], False)
        object_name.object_type = -1
        object_name.placement_index = -1

        SCENARIO.object_names.append(object_name)

    SCENARIO.object_name_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.object_names), 36)

def get_scenery_palette(dump_dic, TAG, SCENARIO):
    scenery_palette_tag_block = dump_dic['Data']['Scenery Palette']
    SCENARIO.scenery_palette = []
    for scenery_palette_element in scenery_palette_tag_block:
        tag_ref = scenery_palette_element['Scenery']
        tag_group = TAG.string_to_bytes(tag_ref['GroupName'], False)
        tag_path = TAG.string_to_bytes(os.path.normpath(tag_ref['Path']), False)
        tag_reference = TAG.TagRef()
        tag_reference.tag_group = tag_group
        tag_reference.name = tag_path
        tag_reference.name_length = len(tag_path)
        tag_reference.salt = 0
        tag_reference.index = -1

        SCENARIO.scenery_palette.append(tag_reference)

    SCENARIO.scenery_palette_header = tag_block_header(TAG, "tbfd", 0, len(SCENARIO.scenery_palette), 48)

def process_json(input_stream, tag_format, report):
    dump_dic = json.load(input_stream)

    TAG = tag_format.TagAsset()
    SCENARIO = ScenarioAsset()

    SCENARIO.header = TAG.Header()
    SCENARIO.header.unk1 = 0
    SCENARIO.header.flags = 0
    SCENARIO.header.type = 0
    SCENARIO.header.name = TAG.string_to_bytes("", False)
    SCENARIO.header.tag_group = TAG.string_to_bytes("scnr", True)
    SCENARIO.header.checksum = 0
    SCENARIO.header.data_offset = 64
    SCENARIO.header.data_length = 0
    SCENARIO.header.unk2 = 0
    SCENARIO.header.version = 2
    SCENARIO.header.destination = 0
    SCENARIO.header.plugin_handle = -1
    SCENARIO.header.engine_tag = TAG.string_to_bytes("BLM!", True)

    get_object_names(dump_dic, TAG, SCENARIO)
    get_scenery_palette(dump_dic, TAG, SCENARIO)

    SCENARIO.scenario_body_header = tag_block_header(TAG, "tbfd", 2, 1, 1476)
    SCENARIO.scenario_body = SCENARIO.ScenarioBody()
    SCENARIO.scenario_body.unused_tag_ref = TAG.TagRef(TAG.string_to_bytes("sbsp", True), "", 0, 0, -1)
    SCENARIO.scenario_body.skies_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.scenario_type = 0
    SCENARIO.scenario_body.scenario_flags = 0
    SCENARIO.scenario_body.child_scenarios_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.local_north = radians(0)
    SCENARIO.scenario_body.predicted_resources_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.functions_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.editor_scenario_data = TAG.RawData(0, 0, 0, 0, 0)
    SCENARIO.scenario_body.comments_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.environment_objects_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.object_names_tag_block = TAG.TagBlock(len(SCENARIO.object_names), 0, 0, 0)
    SCENARIO.scenario_body.scenery_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.scenery_palette_tag_block = TAG.TagBlock(len(SCENARIO.scenery_palette), 0, 0, 0)
    SCENARIO.scenario_body.bipeds_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.biped_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.vehicles_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.vehicle_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.equipment_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.equipment_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.weapons_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.weapon_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.device_groups_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.machines_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.machine_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.controls_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.control_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.light_fixtures_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.light_fixtures_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.sound_scenery_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.sound_scenery_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.light_volumes_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.light_volume_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.player_starting_profile_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.player_starting_locations_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.trigger_volumes_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.recorded_animations_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.netgame_flags_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.netgame_equipment_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.starting_equipment_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.bsp_switch_trigger_volumes_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.decals_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.decal_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.detail_object_collection_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.style_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.squad_groups_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.squads_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.zones_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.mission_scenes_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.character_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
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
    SCENARIO.scenario_body.scripting_data_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.cutscene_flags_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.cutscene_camera_points_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.cutscene_titles_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.custom_object_names_tag_ref = TAG.TagRef(TAG.string_to_bytes("unic", True), "", 0, 0, -1)
    SCENARIO.scenario_body.chapter_title_text_tag_ref = TAG.TagRef(TAG.string_to_bytes("unic", True), "", 0, 0, -1)
    SCENARIO.scenario_body.hud_messages_tag_ref = TAG.TagRef(TAG.string_to_bytes("hmt ", True), "", 0, 0, -1)
    SCENARIO.scenario_body.structure_bsps_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.scenario_resources_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.old_structure_physics_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.hs_unit_seats_tag_block =TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.scenario_kill_triggers_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.hs_syntax_datums_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.orders_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.triggers_tag_block = TAG.TagBlock(0, 0, 0, 0)
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
    SCENARIO.scenario_body.sound_effect_collection_tag_ref = TAG.TagRef(TAG.string_to_bytes("sfx+", True), "", 0, 0, -1)
    SCENARIO.scenario_body.crates_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.crate_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.global_lighting_tag_ref = TAG.TagRef(TAG.string_to_bytes("gldf", True), "", 0, 0, -1)
    SCENARIO.scenario_body.atmospheric_fog_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.planar_fog_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.flocks_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.subtitles_tag_ref = TAG.TagRef(TAG.string_to_bytes("unic", True), "", 0, 0, -1)
    SCENARIO.scenario_body.decorators_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.creatures_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.creature_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.decorator_palette_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.bsp_transition_volumes_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.structure_bsp_lighting_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.editor_folders_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.level_data_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.game_engine_strings_tag_ref = TAG.TagRef(TAG.string_to_bytes("unic", True), "", 0, 0, -1)
    SCENARIO.scenario_body.mission_dialogue_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.objectives_tag_ref = TAG.TagRef(TAG.string_to_bytes("unic", True), "", 0, 0, -1)
    SCENARIO.scenario_body.interpolators_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.shared_references_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.screen_effect_references_tag_block = TAG.TagBlock(0, 0, 0, 0)
    SCENARIO.scenario_body.simulation_definition_table_tag_block = TAG.TagBlock(0, 0, 0, 0)

    return SCENARIO
