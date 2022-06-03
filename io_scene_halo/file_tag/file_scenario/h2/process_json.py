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

def get_scenery(dump_dic, TAG, SCENARIO):
    scenery_tag_block = dump_dic['Data']['Scenery']
    SCENARIO.scenery = []
    for scenery_element in scenery_tag_block:
        source = scenery_element['Source']['Value']
        if not source == 0:
            primary = scenery_element['Primary Color']
            secondary = scenery_element['Secondary Color']
            tertiary = scenery_element['Tertiary Color']
            quaternary = scenery_element['Quaternary Color']

            scenery = SCENARIO.Scenery()

            scenery.sobj_header = tag_block_header(TAG, "sobj", 1, 1, 48)
            scenery.obj0_header = tag_block_header(TAG, "obj#", 0, 1, 8)
            scenery.sper_header = tag_block_header(TAG, "sper", 0, 1, 24)
            scenery.sct3_header = tag_block_header(TAG, "sct3", 0, 1, 20)

            scenery.palette_index = scenery_element['Palette Index']
            scenery.name_index = scenery_element['Name Index']
            scenery.placement_flags = scenery_element['Placement Flags']
            scenery.position = scenery_element['Position']
            scenery.rotation = scenery_element['Rotation']
            scenery.scale = scenery_element['Scale']
            scenery.transform_flags = scenery_element['Transform Flags']
            scenery.manual_bsp_flags = scenery_element['Manual BSP Flags']
            scenery.unique_id = scenery_element['Unique ID']
            scenery.origin_bsp_index = scenery_element['Origin BSP Index']
            scenery.object_type = scenery_element['Type']['Value']
            scenery.source = scenery_element['Source']['Value']
            scenery.bsp_policy = 0
            scenery.editor_folder_index = -1

            scenery.variant_name_length = 0
            scenery.active_change_colors = 0
            scenery.primary_color_BGRA = (primary['B'], primary['G'], primary['R'], 1)
            scenery.secondary_color_BGRA = (secondary['B'], secondary['G'], secondary['R'], 1)
            scenery.tertiary_color_BGRA = (tertiary['B'], tertiary['G'], tertiary['R'], 1)
            scenery.quaternary_color_BGRA = (quaternary['B'], quaternary['G'], quaternary['R'], 1)
            scenery.pathfinding_policy = scenery_element['Pathfinding Policy']['Value']
            scenery.lightmap_policy = scenery_element['Lightmapping Policy']['Value']
            scenery.valid_multiplayer_games = 0

            SCENARIO.scenery.append(scenery)

    SCENARIO.scenery_header = tag_block_header(TAG, "tbfd", 4, len(SCENARIO.scenery), 96)

def get_unit(dump_dic, TAG, SCENARIO, unit):
    unit_tag_block = dump_dic['Data'][unit]
    unit_list = []
    for unit_element in unit_tag_block:
        primary = unit_element['Primary Color']
        secondary = unit_element['Secondary Color']
        tertiary = unit_element['Tertiary Color']
        quaternary = unit_element['Quaternary Color']

        unit = SCENARIO.Unit()

        unit.sobj_header = tag_block_header(TAG, "sobj", 1, 1, 48)
        unit.obj0_header = tag_block_header(TAG, "obj#", 0, 1, 8)
        unit.sper_header = tag_block_header(TAG, "sper", 0, 1, 24)
        unit.sunt_header = tag_block_header(TAG, "sunt", 0, 1, 8)

        unit.palette_index = unit_element['Palette Index']
        unit.name_index = unit_element['Name Index']
        unit.placement_flags = unit_element['Placement Flags']
        unit.position = unit_element['Position']
        unit.rotation = unit_element['Rotation']
        unit.scale = unit_element['Scale']
        unit.transform_flags = unit_element['Transform Flags']
        unit.manual_bsp_flags = unit_element['Manual BSP Flags']
        unit.unique_id = unit_element['Unique ID']
        unit.origin_bsp_index = unit_element['Origin BSP Index']
        unit.object_type = unit_element['Type']['Value']
        unit.source = unit_element['Source']['Value']
        unit.bsp_policy = 0
        unit.editor_folder_index = -1

        unit.variant_name_length = 0
        unit.active_change_colors = 0
        unit.primary_color_BGRA = (primary['B'], primary['G'], primary['R'], 1)
        unit.secondary_color_BGRA = (secondary['B'], secondary['G'], secondary['R'], 1)
        unit.tertiary_color_BGRA = (tertiary['B'], tertiary['G'], tertiary['R'], 1)
        unit.quaternary_color_BGRA = (quaternary['B'], quaternary['G'], quaternary['R'], 1)
        unit.body_vitality = 0
        unit.flags = 0

        unit_list.append(unit)

    return tag_block_header(TAG, "tbfd", 2, len(unit_list), 84), unit_list

def get_equipment(dump_dic, TAG, SCENARIO):
    equipment_tag_block = dump_dic['Data']['Equipment']
    SCENARIO.equipment = []
    for equipment_element in equipment_tag_block:
        equipment = SCENARIO.Equipment()

        equipment.sobj_header = tag_block_header(TAG, "sobj", 1, 1, 48)
        equipment.obj0_header = tag_block_header(TAG, "obj#", 0, 1, 8)
        equipment.seqt_header = tag_block_header(TAG, "seqt", 0, 1, 4)

        equipment.palette_index = equipment_element['Palette Index']
        equipment.name_index = equipment_element['Name Index']
        equipment.placement_flags = equipment_element['Placement Flags']
        equipment.position = equipment_element['Position']
        equipment.rotation = equipment_element['Rotation']
        equipment.scale = equipment_element['Scale']
        equipment.transform_flags = equipment_element['Transform Flags']
        equipment.manual_bsp_flags = equipment_element['Manual BSP Flags']
        equipment.unique_id = equipment_element['Unique ID']
        equipment.origin_bsp_index = equipment_element['Origin BSP Index']
        equipment.object_type = equipment_element['Type']['Value']
        equipment.source = equipment_element['Source']['Value']
        equipment.bsp_policy = 0
        equipment.editor_folder_index = -1

        equipment.flags = 0

        SCENARIO.equipment.append(equipment)

    SCENARIO.equipment_header = tag_block_header(TAG, "tbfd", 2, len(SCENARIO.equipment), 56)

def get_weapon(dump_dic, TAG, SCENARIO):
    weapon_tag_block = dump_dic['Data']['Weapons']
    SCENARIO.weapons = []
    for weapon_element in weapon_tag_block:
        primary = weapon_element['Primary Color']
        secondary = weapon_element['Secondary Color']
        tertiary = weapon_element['Tertiary Color']
        quaternary = weapon_element['Quaternary Color']

        weapon = SCENARIO.Weapon()

        weapon.sobj_header = tag_block_header(TAG, "sobj", 1, 1, 48)
        weapon.obj0_header = tag_block_header(TAG, "obj#", 0, 1, 8)
        weapon.sper_header = tag_block_header(TAG, "sper", 0, 1, 24)
        weapon.swpt_header = tag_block_header(TAG, "swpt", 0, 1, 8)

        weapon.palette_index = weapon_element['Palette Index']
        weapon.name_index = weapon_element['Name Index']
        weapon.placement_flags = weapon_element['Placement Flags']
        weapon.position = weapon_element['Position']
        weapon.rotation = weapon_element['Rotation']
        weapon.scale = weapon_element['Scale']
        weapon.transform_flags = weapon_element['Transform Flags']
        weapon.manual_bsp_flags = weapon_element['Manual BSP Flags']
        weapon.unique_id = weapon_element['Unique ID']
        weapon.origin_bsp_index = weapon_element['Origin BSP Index']
        weapon.object_type = weapon_element['Type']['Value']
        weapon.source = weapon_element['Source']['Value']
        weapon.bsp_policy = 0
        weapon.editor_folder_index = -1

        weapon.variant_name_length = 0
        weapon.active_change_colors = 0
        weapon.primary_color_BGRA = (primary['B'], primary['G'], primary['R'], 1)
        weapon.secondary_color_BGRA = (secondary['B'], secondary['G'], secondary['R'], 1)
        weapon.tertiary_color_BGRA = (tertiary['B'], tertiary['G'], tertiary['R'], 1)
        weapon.quaternary_color_BGRA = (quaternary['B'], quaternary['G'], quaternary['R'], 1)
        weapon.rounds_left = 0
        weapon.rounds_loaded = 0
        weapon.flags = 0

        SCENARIO.weapons.append(weapon)

    SCENARIO.weapon_header = tag_block_header(TAG, "tbfd", 2, len(SCENARIO.weapons), 84)

def get_palette(dump_dic, TAG, palette_element_keyword, palette_keyword):
    palette_tag_block = dump_dic['Data'][palette_keyword]
    palette_list = []
    for palette_element in palette_tag_block:
        tag_ref = palette_element[palette_element_keyword]
        tag_group = TAG.string_to_bytes(tag_ref['GroupName'], True)
        tag_path = TAG.string_to_bytes(os.path.normpath(tag_ref['Path']), False)
        tag_reference = TAG.TagRef()
        tag_reference.tag_group = tag_group
        tag_reference.name = tag_path
        tag_reference.name_length = len(tag_path)
        tag_reference.salt = 0
        tag_reference.index = -1

        palette_list.append(tag_reference)

    return tag_block_header(TAG, "tbfd", 0, len(palette_list), 48), palette_list

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

    get_scenery(dump_dic, TAG, SCENARIO)
    SCENARIO.scenery_palette_header, SCENARIO.scenery_palette = get_palette(dump_dic, TAG, 'Scenery', 'Scenery Palette')

    SCENARIO.bipeds_header, SCENARIO.bipeds = get_unit(dump_dic, TAG, SCENARIO, 'Bipeds')
    SCENARIO.biped_palette_header, SCENARIO.biped_palette = get_palette(dump_dic, TAG, 'Biped', 'Biped Palette')

    SCENARIO.vehicles_header, SCENARIO.vehicles = get_unit(dump_dic, TAG, SCENARIO, 'Vehicles')
    SCENARIO.vehicle_palette_header, SCENARIO.vehicle_palette = get_palette(dump_dic, TAG, 'Vehicle', 'Vehicle Palette')

    get_equipment(dump_dic, TAG, SCENARIO)
    SCENARIO.equipment_palette_header, SCENARIO.equipment_palette = get_palette(dump_dic, TAG, 'Equipment', 'Equipment Palette')

    get_weapon(dump_dic, TAG, SCENARIO)
    SCENARIO.weapon_palette_header, SCENARIO.weapon_palette = get_palette(dump_dic, TAG, 'Weapon', 'Weapon Palette')

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
