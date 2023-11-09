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
from .format_retail import (
        ScenarioAsset,
        ScenarioTypeEnum,
        ScenarioFlags,
        ResourceTypeEnum,
        FunctionFlags,
        FunctionEnum,
        MapEnum,
        BoundsModeEnum,
        ObjectFlags,
        GametypeEnum,
        NetGameEnum,
        StartingEquipment,
        SALT_SIZE
        )

XML_OUTPUT = True

def process_file(input_stream, tag_format, report):
    TAG = tag_format.TagAsset()
    SCENARIO = ScenarioAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    SCENARIO.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    level_tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG)
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
    SCENARIO.scenario_body.ai_conversations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai conversations references"))
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

    unused_tag_ref = SCENARIO.scenario_body.unused_tag_ref
    custom_object_names_tag_ref = SCENARIO.scenario_body.custom_object_names_tag_ref
    chapter_title_text_tag_ref = SCENARIO.scenario_body.chapter_title_text_tag_ref
    hud_messages_tag_ref = SCENARIO.scenario_body.hud_messages_tag_ref
    sound_effect_collection_tag_ref = SCENARIO.scenario_body.sound_effect_collection_tag_ref
    global_lighting_tag_ref = SCENARIO.scenario_body.global_lighting_tag_ref
    subtitles_tag_ref = SCENARIO.scenario_body.subtitles_tag_ref
    game_engine_strings_tag_ref = SCENARIO.scenario_body.game_engine_strings_tag_ref
    objectives_tag_ref = SCENARIO.scenario_body.objectives_tag_ref
    unused_name_length = unused_tag_ref.name_length
    custom_object_names_name_length = custom_object_names_tag_ref.name_length
    chapter_title_text_name_length = chapter_title_text_tag_ref.name_length
    hud_messages_name_length = hud_messages_tag_ref.name_length
    sound_effect_collection_name_length = sound_effect_collection_tag_ref.name_length
    global_lighting_name_length = global_lighting_tag_ref.name_length
    subtitles_name_length = subtitles_tag_ref.name_length
    game_engine_strings_name_length = game_engine_strings_tag_ref.name_length
    objectives_name_length = objectives_tag_ref.name_length
    if unused_name_length > 0:
        unused_tag_ref.name = TAG.read_variable_string(input_stream, unused_name_length, TAG)

    if custom_object_names_name_length > 0:
        custom_object_names_tag_ref.name = TAG.read_variable_string(input_stream, custom_object_names_name_length, TAG)

    if chapter_title_text_name_length > 0:
        chapter_title_text_tag_ref.name = TAG.read_variable_string(input_stream, chapter_title_text_name_length, TAG)

    if hud_messages_name_length > 0:
        hud_messages_tag_ref.name = TAG.read_variable_string(input_stream, hud_messages_name_length, TAG)

    if sound_effect_collection_name_length > 0:
        sound_effect_collection_tag_ref.name = TAG.read_variable_string(input_stream, sound_effect_collection_name_length, TAG)

    if global_lighting_name_length > 0:
        global_lighting_tag_ref.name = TAG.read_variable_string(input_stream, global_lighting_name_length, TAG)

    if subtitles_name_length > 0:
        subtitles_tag_ref.name = TAG.read_variable_string(input_stream, subtitles_name_length, TAG)

    if game_engine_strings_name_length > 0:
        game_engine_strings_tag_ref.name = TAG.read_variable_string(input_stream, game_engine_strings_name_length, TAG)

    if objectives_name_length > 0:
        objectives_tag_ref.name = TAG.read_variable_string(input_stream, objectives_name_length, TAG)

    if XML_OUTPUT:
        unused_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "unused")
        custom_object_names_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "custom object names")
        chapter_title_text_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "chapter title text")
        hud_messages_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "hud messages")
        sound_effect_collection_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "sound effect collection")
        global_lighting_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "global lighting")
        subtitles_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "subtitles")
        game_engine_strings_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "game engine strings")
        objectives_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "objectives")
        unused_tag_ref.append_xml_attributes(unused_node)
        custom_object_names_tag_ref.append_xml_attributes(custom_object_names_node)
        chapter_title_text_tag_ref.append_xml_attributes(chapter_title_text_node)
        hud_messages_tag_ref.append_xml_attributes(hud_messages_node)
        sound_effect_collection_tag_ref.append_xml_attributes(sound_effect_collection_node)
        global_lighting_tag_ref.append_xml_attributes(global_lighting_node)
        subtitles_tag_ref.append_xml_attributes(subtitles_node)
        game_engine_strings_tag_ref.append_xml_attributes(game_engine_strings_node)
        objectives_tag_ref.append_xml_attributes(objectives_node)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, SCENARIO.header.tag_group, TAG.is_legacy, True)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return SCENARIO
