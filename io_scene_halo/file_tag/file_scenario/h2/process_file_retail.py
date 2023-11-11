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
        GametypeEnum,
        NetGameEnum,
        StartingEquipment,
        SALT_SIZE
        )

XML_OUTPUT = True

def get_predicted_resource(input_stream, SCENARIO, TAG, tag_format, node_element):
    predicted_resource = SCENARIO.PredictedResource()
    predicted_resource.tag_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "type", ResourceTypeEnum))
    predicted_resource.resource_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "resource index"))
    predicted_resource.tag_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "tag index"))

    return predicted_resource

def get_functions(input_stream, SCENARIO, TAG, tag_format, node_element):
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

def get_comments(input_stream, SCENARIO, TAG, tag_format, node_element):
    comment = SCENARIO.Comment()
    comment.position = TAG.read_point_3d(input_stream, TAG,  tag_format.XMLData(node_element, "position"))
    comment.type = TAG.read_enum_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "type", CommentTypeEnum))
    comment.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    comment.comment = TAG.read_string256(input_stream, TAG, tag_format.XMLData(node_element, "comment"))

    return comment

def get_environment_objects(input_stream, SCENARIO, TAG, tag_format, node_element):
    environment_object = SCENARIO.EnvironmentObject()
    environment_object.bsp_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "bsp", None, SCENARIO.scenario_body.structure_bsps_tag_block.count, "scenario_bsp_block"))
    environment_object.runtime_object_type = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "runtime object type"))
    environment_object.unique_id = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "unique id"))
    input_stream.read(4) # Padding?
    environment_object.object_definition_tag = TAG.read_variable_string_no_terminator_reversed(input_stream, 4, TAG, tag_format.XMLData(node_element, "object definition tag"))
    environment_object.environment_object = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "object"))
    input_stream.read(44) # Padding?

    return environment_object

def get_object_names(input_stream, SCENARIO, TAG, tag_format, node_element):
    object_name = SCENARIO.ObjectName()
    object_name.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    object_name.object_type = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "object type", None, 1, ""))
    object_name.placement_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "placement index", None, 1, ""))

    return object_name

def get_scenery(input_stream, SCENARIO, TAG, tag_format, node_element):
    scenery = SCENARIO.Scenery()
    scenery.palette_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "type", None, SCENARIO.scenario_body.scenery_palette_tag_block.count, "scenario_scenery_palette_block"))
    scenery.name_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "name", None, SCENARIO.scenario_body.object_names_tag_block.count, "scenario_object_names_block"))
    scenery.placement_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "placement flags", ObjectFlags))
    scenery.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    scenery.rotation = TAG.read_euler_angles(input_stream, TAG, tag_format.XMLData(node_element, "rotation"))
    scenery.scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "scale"))
    scenery.transform_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "transform flags", TransformFlags))
    scenery.manual_bsp_flags = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "manual bsp flags"))
    scenery.unique_id = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "unique id"))
    scenery.origin_bsp_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "origin bsp index", None, SCENARIO.scenario_body.structure_bsps_tag_block.count, "scenario_bsp_block"))
    scenery.object_type = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "object type", ObjectTypeFlags))
    scenery.source = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "source", ObjectSourceFlags))
    scenery.bsp_policy = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "bsp policy", ObjectBSPPolicyFlags))
    input_stream.read(1) # Padding?
    scenery.editor_folder_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "editor folder", None, SCENARIO.scenario_body.editor_folders_tag_block.count, "scenario_editor_folder_block"))

    TAG.big_endian = True
    scenery.variant_name_length = TAG.read_signed_integer(input_stream, TAG)
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

def get_units(input_stream, SCENARIO, TAG, tag_format, node_element, palette_count, palette_name):
    unit = SCENARIO.Unit()
    unit.palette_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "type", None, palette_count, palette_name))
    unit.name_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "name", None, SCENARIO.scenario_body.object_names_tag_block.count, "scenario_object_names_block"))
    unit.placement_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "placement flags", ObjectFlags))
    unit.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    unit.rotation = TAG.read_euler_angles(input_stream, TAG, tag_format.XMLData(node_element, "rotation"))
    unit.scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "scale"))
    unit.transform_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "transform flags", TransformFlags))
    unit.manual_bsp_flags = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "manual bsp flags"))
    unit.unique_id = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "unique id"))
    unit.origin_bsp_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "origin bsp index", None, SCENARIO.scenario_body.structure_bsps_tag_block.count, "scenario_bsp_block"))
    unit.object_type = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "object type", ObjectTypeFlags))
    unit.source = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "source", ObjectSourceFlags))
    unit.bsp_policy = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "bsp policy", ObjectBSPPolicyFlags))
    input_stream.read(1) # Padding?
    unit.editor_folder_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "editor folder", None, SCENARIO.scenario_body.editor_folders_tag_block.count, "scenario_editor_folder_block"))

    TAG.big_endian = True
    unit.variant_name_length = TAG.read_signed_integer(input_stream, TAG)
    TAG.big_endian = False

    unit.active_change_colors = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "active change colors", ObjectColorChangeFlags))
    unit.primary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "primary color"))
    unit.secondary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "secondary color"))
    unit.tertiary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "tertiary color"))
    unit.quaternary_color_BGRA = TAG.read_bgr_byte(input_stream, TAG, tag_format.XMLData(node_element, "quaternary color"))
    unit.body_vitality = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "body vitality"))
    unit.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", UnitFlags))

    return unit

def get_equipment(input_stream, SCENARIO, TAG, tag_format, node_element, palette_count, palette_name):
    equipment = SCENARIO.Equipment()
    equipment.palette_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "type", None, palette_count, palette_name))
    equipment.name_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "name", None, SCENARIO.scenario_body.object_names_tag_block.count, "scenario_object_names_block"))
    equipment.placement_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "placement flags", ObjectFlags))
    equipment.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    equipment.rotation = TAG.read_euler_angles(input_stream, TAG, tag_format.XMLData(node_element, "rotation"))
    equipment.scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "scale"))
    equipment.transform_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "transform flags", TransformFlags))
    equipment.manual_bsp_flags = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "manual bsp flags"))
    equipment.unique_id = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "unique id"))
    equipment.origin_bsp_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "origin bsp index", None, SCENARIO.scenario_body.structure_bsps_tag_block.count, "scenario_bsp_block"))
    equipment.object_type = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "object type", ObjectTypeFlags))
    equipment.source = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "source", ObjectSourceFlags))
    equipment.bsp_policy = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "bsp policy", ObjectBSPPolicyFlags))
    input_stream.read(1) # Padding?
    equipment.editor_folder_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "editor folder", None, SCENARIO.scenario_body.editor_folders_tag_block.count, "scenario_editor_folder_block"))

    equipment.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", ItemFlags))

    return equipment

def get_weapons(input_stream, SCENARIO, TAG, tag_format, node_element):
    weapon = SCENARIO.Weapon()
    weapon.palette_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "type", None, SCENARIO.scenario_body.scenery_palette_tag_block.count, "scenario_scenery_palette_block"))
    weapon.name_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "name", None, SCENARIO.scenario_body.object_names_tag_block.count, "scenario_object_names_block"))
    weapon.placement_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "placement flags", ObjectFlags))
    weapon.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    weapon.rotation = TAG.read_euler_angles(input_stream, TAG, tag_format.XMLData(node_element, "rotation"))
    weapon.scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "scale"))
    weapon.transform_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "transform flags", TransformFlags))
    weapon.manual_bsp_flags = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "manual bsp flags"))
    weapon.unique_id = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "unique id"))
    weapon.origin_bsp_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "origin bsp index", None, SCENARIO.scenario_body.structure_bsps_tag_block.count, "scenario_bsp_block"))
    weapon.object_type = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "object type", ObjectTypeFlags))
    weapon.source = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "source", ObjectSourceFlags))
    weapon.bsp_policy = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "bsp policy", ObjectBSPPolicyFlags))
    input_stream.read(1) # Padding?
    weapon.editor_folder_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "editor folder", None, SCENARIO.scenario_body.editor_folders_tag_block.count, "scenario_editor_folder_block"))

    TAG.big_endian = True
    weapon.variant_name_length = TAG.read_signed_integer(input_stream, TAG)
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

def get_device_groups(input_stream, SCENARIO, TAG, tag_format, node_element):
    device_group = SCENARIO.DeviceGroup()
    device_group.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    device_group.initial_value = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "initial value"))
    device_group.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", DeviceGroupFlags))

    return device_group

def get_machines(input_stream, SCENARIO, TAG, tag_format, node_element):
    machine = SCENARIO.DeviceMachine()
    machine.palette_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "type", None, SCENARIO.scenario_body.scenery_palette_tag_block.count, "scenario_scenery_palette_block"))
    machine.name_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "name", None, SCENARIO.scenario_body.object_names_tag_block.count, "scenario_object_names_block"))
    machine.placement_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "placement flags", ObjectFlags))
    machine.position = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(node_element, "position"))
    machine.rotation = TAG.read_euler_angles(input_stream, TAG, tag_format.XMLData(node_element, "rotation"))
    machine.scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(node_element, "scale"))
    machine.transform_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(node_element, "transform flags", TransformFlags))
    machine.manual_bsp_flags = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "manual bsp flags"))
    machine.unique_id = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(node_element, "unique id"))
    machine.origin_bsp_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "origin bsp index", None, SCENARIO.scenario_body.structure_bsps_tag_block.count, "scenario_bsp_block"))
    machine.object_type = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "object type", ObjectTypeFlags))
    machine.source = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "source", ObjectSourceFlags))
    machine.bsp_policy = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(node_element, "bsp policy", ObjectBSPPolicyFlags))
    input_stream.read(1) # Padding?
    machine.editor_folder_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "editor folder", None, SCENARIO.scenario_body.editor_folders_tag_block.count, "scenario_editor_folder_block"))

    machine.power_group_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "power group", None, SCENARIO.scenario_body.device_groups_tag_block.count, "scenario_device_groups_block"))
    machine.position_group_index = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(node_element, "position group", None, SCENARIO.scenario_body.device_groups_tag_block.count, "scenario_device_groups_block"))
    machine.flags_0 = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", DeviceFlags))
    machine.flags_1 = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(node_element, "flags", MachineFlags))
    machine.pathfinding_references_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(node_element, "pathfinding references"))

    return machine

def get_palette(input_stream, TAG, tag_format, node_element, padding=32):
    tag_reference = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(node_element, "name"))
    input_stream.read(padding) # Padding?

    return tag_reference

def palette_helper(input_stream, palette_count, palette_name, palette_header, palette, node, TAG, tag_format):
    if palette_count > 0:
        palette_header = TAG.TagBlockHeader().read(input_stream, TAG)
        palette_node = tag_format.get_xml_node(XML_OUTPUT, palette_count, node, "name", palette_name)
        for palette_idx in range(palette_count):
            palette_element_node = None
            if XML_OUTPUT:
                palette_element_node = TAG.xml_doc.createElement('element')
                palette_element_node.setAttribute('index', str(palette_idx))
                palette_node.appendChild(palette_element_node)

            palette.append(get_palette(input_stream, TAG, tag_format, palette_element_node))

        for palette_idx, palette_element in enumerate(palette):
            palette_name_length = palette_element.name_length
            if palette_name_length > 0:
                palette_element.name = TAG.read_variable_string(input_stream, palette_name_length, TAG)

            if XML_OUTPUT:
                palette_element_node = palette_node.childNodes[palette_idx]
                palette_tag_ref_node = tag_format.get_xml_node(XML_OUTPUT, 1, palette_element_node, "name", "name")
                palette_element.append_xml_attributes(palette_tag_ref_node)

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
    SCENARIO.hs_unit_seat = []
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

    if SCENARIO.scenario_body.predicted_resources_tag_block.count > 0:
        SCENARIO.predicted_resources_header = TAG.TagBlockHeader().read(input_stream, TAG)
        predicted_resource_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.predicted_resources_tag_block.count, tag_node, "name", "predicted resources")
        for predicted_resource_idx in range(SCENARIO.scenario_body.predicted_resources_tag_block.count):
            predicted_resource_element_node = None
            if XML_OUTPUT:
                predicted_resource_element_node = TAG.xml_doc.createElement('element')
                predicted_resource_element_node.setAttribute('index', str(predicted_resource_idx))
                predicted_resource_node.appendChild(predicted_resource_element_node)

            SCENARIO.predicted_resources.append(get_predicted_resource(input_stream, SCENARIO, TAG, tag_format, predicted_resource_element_node))

    if SCENARIO.scenario_body.functions_tag_block.count > 0:
        SCENARIO.functions_header = TAG.TagBlockHeader().read(input_stream, TAG)
        function_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.functions_tag_block.count, tag_node, "name", "functions")
        for function_idx in range(SCENARIO.scenario_body.functions_tag_block.count):
            function_element_node = None
            if XML_OUTPUT:
                function_element_node = TAG.xml_doc.createElement('element')
                function_element_node.setAttribute('index', str(function_idx))
                function_node.appendChild(function_element_node)

            SCENARIO.functions.append(get_functions(input_stream, SCENARIO, TAG, tag_format, function_element_node))

    SCENARIO.editor_scenario_data = input_stream.read(SCENARIO.scenario_body.editor_scenario_data.size)

    if SCENARIO.scenario_body.comments_tag_block.count > 0:
        SCENARIO.comment_header = TAG.TagBlockHeader().read(input_stream, TAG)
        comment_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.comments_tag_block.count, tag_node, "name", "comments")
        for comment_idx in range(SCENARIO.scenario_body.comments_tag_block.count):
            comment_element_node = None
            if XML_OUTPUT:
                comment_element_node = TAG.xml_doc.createElement('element')
                comment_element_node.setAttribute('index', str(comment_idx))
                comment_node.appendChild(comment_element_node)

            SCENARIO.comments.append(get_comments(input_stream, SCENARIO, TAG, tag_format, comment_element_node))

    if SCENARIO.scenario_body.environment_objects_tag_block.count > 0:
        SCENARIO.environment_objects_header = TAG.TagBlockHeader().read(input_stream, TAG)
        environment_objects_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.environment_objects_tag_block.count, tag_node, "name", "environment objects")
        for environment_object_idx in range(SCENARIO.scenario_body.environment_objects_tag_block.count):
            environment_object_element_node = None
            if XML_OUTPUT:
                environment_object_element_node = TAG.xml_doc.createElement('element')
                environment_object_element_node.setAttribute('index', str(environment_object_idx))
                environment_objects_node.appendChild(environment_object_element_node)

            SCENARIO.environment_objects.append(get_environment_objects(input_stream, SCENARIO, TAG, tag_format, environment_object_element_node))

    if SCENARIO.scenario_body.object_names_tag_block.count > 0:
        SCENARIO.object_name_header = TAG.TagBlockHeader().read(input_stream, TAG)
        object_name_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.object_names_tag_block.count, tag_node, "name", "object names")
        for object_name_idx in range(SCENARIO.scenario_body.object_names_tag_block.count):
            object_name_element_node = None
            if XML_OUTPUT:
                object_name_element_node = TAG.xml_doc.createElement('element')
                object_name_element_node.setAttribute('index', str(object_name_idx))
                object_name_node.appendChild(object_name_element_node)

            SCENARIO.object_names.append(get_object_names(input_stream, SCENARIO, TAG, tag_format, object_name_element_node))

    if SCENARIO.scenario_body.scenery_tag_block.count > 0:
        SCENARIO.scenery_header = TAG.TagBlockHeader().read(input_stream, TAG)
        scenery_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.scenery_tag_block.count, tag_node, "name", "scenery")
        for scenery_idx in range(SCENARIO.scenario_body.scenery_tag_block.count):
            scenery_element_node = None
            if XML_OUTPUT:
                scenery_element_node = TAG.xml_doc.createElement('element')
                scenery_element_node.setAttribute('index', str(scenery_idx))
                scenery_node.appendChild(scenery_element_node)

            SCENARIO.scenery.append(get_scenery(input_stream, SCENARIO, TAG, tag_format, scenery_element_node))

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

    palette_helper(input_stream, SCENARIO.scenario_body.scenery_palette_tag_block.count, "scenery palette", SCENARIO.scenery_palette_header, SCENARIO.scenery_palette, tag_node, TAG, tag_format)

    if SCENARIO.scenario_body.bipeds_tag_block.count > 0:
        SCENARIO.bipeds_header = TAG.TagBlockHeader().read(input_stream, TAG)
        biped_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.bipeds_tag_block.count, tag_node, "name", "bipeds")
        for biped_idx in range(SCENARIO.scenario_body.bipeds_tag_block.count):
            biped_element_node = None
            if XML_OUTPUT:
                biped_element_node = TAG.xml_doc.createElement('element')
                biped_element_node.setAttribute('index', str(biped_idx))
                biped_node.appendChild(biped_element_node)

            SCENARIO.bipeds.append(get_units(input_stream, SCENARIO, TAG, tag_format, biped_element_node, SCENARIO.scenario_body.biped_palette_tag_block.count, "scenario_biped_palette_block"))

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

    palette_helper(input_stream, SCENARIO.scenario_body.biped_palette_tag_block.count, "bipeds palette", SCENARIO.biped_palette_header, SCENARIO.biped_palette, tag_node, TAG, tag_format)

    if SCENARIO.scenario_body.vehicles_tag_block.count > 0:
        SCENARIO.vehicles_header = TAG.TagBlockHeader().read(input_stream, TAG)
        vehicle_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.vehicles_tag_block.count, tag_node, "name", "vehicles")
        for vehicle_idx in range(SCENARIO.scenario_body.vehicles_tag_block.count):
            vehicle_element_node = None
            if XML_OUTPUT:
                vehicle_element_node = TAG.xml_doc.createElement('element')
                vehicle_element_node.setAttribute('index', str(vehicle_idx))
                vehicle_node.appendChild(vehicle_element_node)

            SCENARIO.vehicles.append(get_units(input_stream, SCENARIO, TAG, tag_format, vehicle_element_node, SCENARIO.scenario_body.vehicle_palette_tag_block.count, "scenario_vehicle_palette_block"))

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

    palette_helper(input_stream, SCENARIO.scenario_body.vehicle_palette_tag_block.count, "vehicles palette", SCENARIO.vehicle_palette_header, SCENARIO.vehicle_palette, tag_node, TAG, tag_format)

    if SCENARIO.scenario_body.equipment_tag_block.count > 0:
        SCENARIO.equipment_header = TAG.TagBlockHeader().read(input_stream, TAG)
        equipment_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.equipment_tag_block.count, tag_node, "name", "equipment")
        for equipment_idx in range(SCENARIO.scenario_body.equipment_tag_block.count):
            equipment_element_node = None
            if XML_OUTPUT:
                equipment_element_node = TAG.xml_doc.createElement('element')
                equipment_element_node.setAttribute('index', str(equipment_idx))
                equipment_node.appendChild(equipment_element_node)

            SCENARIO.equipment.append(get_equipment(input_stream, SCENARIO, TAG, tag_format, equipment_element_node, SCENARIO.scenario_body.equipment_palette_tag_block.count, "scenario_equipment_palette_block"))

        for equipment_idx, equipment in enumerate(SCENARIO.equipment):
            equipment_element_node = None
            if XML_OUTPUT:
                equipment_element_node = equipment_node.childNodes[equipment_idx]

            equipment.sobj_header = TAG.TagBlockHeader().read(input_stream, TAG)
            equipment.obj0_header = TAG.TagBlockHeader().read(input_stream, TAG)
            equipment.seqt_header = TAG.TagBlockHeader().read(input_stream, TAG)

    palette_helper(input_stream, SCENARIO.scenario_body.equipment_palette_tag_block.count, "equipment palette", SCENARIO.equipment_palette_header, SCENARIO.equipment_palette, tag_node, TAG, tag_format)

    if SCENARIO.scenario_body.weapons_tag_block.count > 0:
        SCENARIO.weapon_header = TAG.TagBlockHeader().read(input_stream, TAG)
        weapon_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.weapons_tag_block.count, tag_node, "name", "weapons")
        for weapon_idx in range(SCENARIO.scenario_body.weapons_tag_block.count):
            weapon_element_node = None
            if XML_OUTPUT:
                weapon_element_node = TAG.xml_doc.createElement('element')
                weapon_element_node.setAttribute('index', str(weapon_idx))
                weapon_node.appendChild(weapon_element_node)

            SCENARIO.weapons.append(get_weapons(input_stream, SCENARIO, TAG, tag_format, weapon_element_node))

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

    palette_helper(input_stream, SCENARIO.scenario_body.weapon_palette_tag_block.count, "weapon palette", SCENARIO.weapon_palette_header, SCENARIO.weapon_palette, tag_node, TAG, tag_format)

    if SCENARIO.scenario_body.device_groups_tag_block.count > 0:
        SCENARIO.device_group_header = TAG.TagBlockHeader().read(input_stream, TAG)
        device_group_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.device_groups_tag_block.count, tag_node, "name", "device groups")
        for device_group_idx in range(SCENARIO.scenario_body.device_groups_tag_block.count):
            device_group_element_node = None
            if XML_OUTPUT:
                device_group_element_node = TAG.xml_doc.createElement('element')
                device_group_element_node.setAttribute('index', str(device_group_idx))
                device_group_node.appendChild(device_group_element_node)

            SCENARIO.device_groups.append(get_device_groups(input_stream, SCENARIO, TAG, tag_format, device_group_element_node))

    if SCENARIO.scenario_body.machines_tag_block.count > 0:
        SCENARIO.device_machine_header = TAG.TagBlockHeader().read(input_stream, TAG)
        device_machine_node = tag_format.get_xml_node(XML_OUTPUT, SCENARIO.scenario_body.machines_tag_block.count, tag_node, "name", "machines")
        for device_machine_idx in range(SCENARIO.scenario_body.machines_tag_block.count):
            device_machine_element_node = None
            if XML_OUTPUT:
                device_machine_element_node = TAG.xml_doc.createElement('element')
                device_machine_element_node.setAttribute('index', str(device_machine_idx))
                device_machine_node.appendChild(device_machine_element_node)

            SCENARIO.device_machines.append(get_machines(input_stream, SCENARIO, TAG, tag_format, device_machine_element_node))

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

    palette_helper(input_stream, SCENARIO.scenario_body.machine_palette_tag_block.count, "machine palette", SCENARIO.device_machine_palette_header, SCENARIO.device_machine_palette, tag_node, TAG, tag_format)

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
