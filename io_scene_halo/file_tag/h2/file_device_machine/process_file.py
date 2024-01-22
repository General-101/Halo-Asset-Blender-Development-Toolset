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
    MachineAsset, 
    ObjectFlags, 
    LightmapShadowModeEnum, 
    SweetenerSizeEnum,
    DeviceFlags,
    LightmapFlags,
    MachineTypeEnum,
    MachineFlags,
    CollisionResponseEnum,
    PathfindingPolicyEnum,
    )

XML_OUTPUT = False

def initilize_machine(MACHINE):
    MACHINE.ai_properties = []
    MACHINE.functions = []
    MACHINE.attachments = []
    MACHINE.widgets = []
    MACHINE.old_functions = []
    MACHINE.change_colors = []
    MACHINE.predicted_resources = []

def read_machine_body_v0(MACHINE, TAG, input_stream, tag_node, XML_OUTPUT):
    MACHINE.machine_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    MACHINE.machine_body = MACHINE.MachineBody()
    input_stream.read(2) # Padding?
    MACHINE.machine_body.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    MACHINE.machine_body.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    MACHINE.machine_body.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    input_stream.read(12) # Padding?
    MACHINE.machine_body.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    MACHINE.machine_body.lightmap_shadow_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap shadow mode", LightmapShadowModeEnum))
    MACHINE.machine_body.sweetner_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sweetner size", SweetenerSizeEnum))
    input_stream.read(36) # Padding?
    MACHINE.machine_body.dynamic_light_sphere_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere radius"))
    MACHINE.machine_body.dynamic_light_sphere_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere offset"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    MACHINE.machine_body.default_model_variant_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    MACHINE.machine_body.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    MACHINE.machine_body.crate_object = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "crate object"))
    input_stream.read(16) # Padding?
    MACHINE.machine_body.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    MACHINE.machine_body.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    MACHINE.machine_body.material_effects = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "material effects"))
    input_stream.read(24) # Padding?
    MACHINE.machine_body.ai_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai properties"))
    input_stream.read(24) # Padding?
    MACHINE.machine_body.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    input_stream.read(16) # Padding?
    MACHINE.machine_body.apply_collision_damage_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "apply collision damage scale"))
    MACHINE.machine_body.min_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game acc"))
    MACHINE.machine_body.max_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game acc"))
    MACHINE.machine_body.min_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game scale"))
    MACHINE.machine_body.max_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game scale"))
    MACHINE.machine_body.min_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs acc"))
    MACHINE.machine_body.max_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs acc"))
    MACHINE.machine_body.min_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs scale"))
    MACHINE.machine_body.max_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs scale"))
    MACHINE.machine_body.hud_text_message_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    input_stream.read(2) # Padding?
    MACHINE.machine_body.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    MACHINE.machine_body.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    MACHINE.machine_body.old_functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "old functions"))
    MACHINE.machine_body.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    MACHINE.machine_body.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    MACHINE.machine_body.device_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", DeviceFlags))
    input_stream.read(2) # Padding?
    MACHINE.machine_body.power_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "power transition time"))
    MACHINE.machine_body.power_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "power acceleration time"))
    MACHINE.machine_body.position_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "position transition time"))
    MACHINE.machine_body.position_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "position acceleration time"))
    MACHINE.machine_body.depowered_position_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "depowered position transition time"))
    MACHINE.machine_body.depowered_position_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "depowered position acceleration time"))
    MACHINE.machine_body.lightmap_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap flags", LightmapFlags))
    input_stream.read(6) # Padding?
    MACHINE.machine_body.open_up = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "open"))
    MACHINE.machine_body.close_down = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "close"))
    MACHINE.machine_body.opened = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "opened"))
    MACHINE.machine_body.closed = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "closed"))
    MACHINE.machine_body.depowered = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "depowered"))
    MACHINE.machine_body.repowered = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "repowered"))
    MACHINE.machine_body.delay_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "delay time"))
    input_stream.read(8) # Padding?
    MACHINE.machine_body.delay_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "delay effect"))
    MACHINE.machine_body.automatic_activation_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "automatic activation radius"))
    input_stream.read(112) # Padding?
    MACHINE.machine_body.machine_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "type", MachineTypeEnum))
    MACHINE.machine_body.machine_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", MachineFlags))
    MACHINE.machine_body.door_open_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "door open time"))
    MACHINE.machine_body.door_occlusion_time = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "door occlusion time"))
    input_stream.read(72) # Padding?
    MACHINE.machine_body.collision_response = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "collision response", CollisionResponseEnum))
    MACHINE.machine_body.elevator_node = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "elevator node"))
    input_stream.read(68) # Padding?
    MACHINE.machine_body.pathfinding_policy = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "pathfinding policy", PathfindingPolicyEnum))
    input_stream.read(2) # Padding?

def read_machine_body_retail(MACHINE, TAG, input_stream, tag_node, XML_OUTPUT):
    MACHINE.machine_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    MACHINE.machine_body = MACHINE.MachineBody()
    input_stream.read(2) # Padding?
    MACHINE.machine_body.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    MACHINE.machine_body.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    MACHINE.machine_body.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    MACHINE.machine_body.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    MACHINE.machine_body.lightmap_shadow_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap shadow mode", LightmapShadowModeEnum))
    MACHINE.machine_body.sweetner_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sweetner size", SweetenerSizeEnum))
    input_stream.read(4) # Padding?
    MACHINE.machine_body.dynamic_light_sphere_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere radius"))
    MACHINE.machine_body.dynamic_light_sphere_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere offset"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    MACHINE.machine_body.default_model_variant_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    MACHINE.machine_body.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    MACHINE.machine_body.crate_object = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "crate object"))
    MACHINE.machine_body.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    MACHINE.machine_body.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    MACHINE.machine_body.material_effects = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "material effects"))
    MACHINE.machine_body.ai_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai properties"))
    MACHINE.machine_body.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    MACHINE.machine_body.apply_collision_damage_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "apply collision damage scale"))
    MACHINE.machine_body.min_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game acc"))
    MACHINE.machine_body.max_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game acc"))
    MACHINE.machine_body.min_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game scale"))
    MACHINE.machine_body.max_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game scale"))
    MACHINE.machine_body.min_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs acc"))
    MACHINE.machine_body.max_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs acc"))
    MACHINE.machine_body.min_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs scale"))
    MACHINE.machine_body.max_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs scale"))
    MACHINE.machine_body.hud_text_message_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    input_stream.read(2) # Padding?
    MACHINE.machine_body.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    MACHINE.machine_body.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    MACHINE.machine_body.old_functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "old functions"))
    MACHINE.machine_body.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    MACHINE.machine_body.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    MACHINE.machine_body.device_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", DeviceFlags))
    input_stream.read(2) # Padding?
    MACHINE.machine_body.power_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "power transition time"))
    MACHINE.machine_body.power_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "power acceleration time"))
    MACHINE.machine_body.position_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "position transition time"))
    MACHINE.machine_body.position_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "position acceleration time"))
    MACHINE.machine_body.depowered_position_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "depowered position transition time"))
    MACHINE.machine_body.depowered_position_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "depowered position acceleration time"))
    MACHINE.machine_body.lightmap_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap flags", LightmapFlags))
    input_stream.read(2) # Padding?
    MACHINE.machine_body.open_up = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "open"))
    MACHINE.machine_body.close_down = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "close"))
    MACHINE.machine_body.opened = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "opened"))
    MACHINE.machine_body.closed = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "closed"))
    MACHINE.machine_body.depowered = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "depowered"))
    MACHINE.machine_body.repowered = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "repowered"))
    MACHINE.machine_body.delay_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "delay time"))
    MACHINE.machine_body.delay_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "delay effect"))
    MACHINE.machine_body.automatic_activation_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "automatic activation radius"))
    MACHINE.machine_body.machine_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "type", MachineTypeEnum))
    MACHINE.machine_body.machine_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", MachineFlags))
    MACHINE.machine_body.door_open_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "door open time"))
    MACHINE.machine_body.door_occlusion_time = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "door occlusion time"))
    MACHINE.machine_body.collision_response = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "collision response", CollisionResponseEnum))
    MACHINE.machine_body.elevator_node = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "elevator node"))
    MACHINE.machine_body.pathfinding_policy = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "pathfinding policy", PathfindingPolicyEnum))
    input_stream.read(2) # Padding?

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    MACHINE = MachineAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    MACHINE.header = TAG.Header().read(input_stream, TAG)
    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    initilize_machine(MACHINE)
    if MACHINE.header.engine_tag == "LAMB":
        read_machine_body_v0(MACHINE, TAG, input_stream, tag_node, XML_OUTPUT)
    elif MACHINE.header.engine_tag == "MLAB":
        read_machine_body_v0(MACHINE, TAG, input_stream, tag_node, XML_OUTPUT)
    elif MACHINE.header.engine_tag == "BLM!":
        read_machine_body_retail(MACHINE, TAG, input_stream, tag_node, XML_OUTPUT)

    if MACHINE.machine_body.default_model_variant_length > 0:
        MACHINE.machine_body.default_model_variant = TAG.read_variable_string_no_terminator(input_stream, MACHINE.machine_body.default_model_variant_length, TAG, tag_format.XMLData(tag_node, "default model variant"))

    if MACHINE.machine_body.model.name_length > 0:
        MACHINE.machine_body.model.name = TAG.read_variable_string(input_stream, MACHINE.machine_body.model.name_length, TAG)

    if MACHINE.machine_body.crate_object.name_length > 0:
        MACHINE.machine_body.crate_object.name = TAG.read_variable_string(input_stream, MACHINE.machine_body.crate_object.name_length, TAG)

    if MACHINE.machine_body.modifier_shader.name_length > 0:
        MACHINE.machine_body.modifier_shader.name = TAG.read_variable_string(input_stream, MACHINE.machine_body.modifier_shader.name_length, TAG)

    if MACHINE.machine_body.creation_effect.name_length > 0:
        MACHINE.machine_body.creation_effect.name = TAG.read_variable_string(input_stream, MACHINE.machine_body.creation_effect.name_length, TAG)

    if MACHINE.machine_body.material_effects.name_length > 0:
        MACHINE.machine_body.material_effects.name = TAG.read_variable_string(input_stream, MACHINE.machine_body.material_effects.name_length, TAG)

    if XML_OUTPUT:
        model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "model")
        crate_object_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "crate object")
        modifier_shader_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "modifier shader")
        creation_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "creation effect")
        material_effects_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "material effects")
        MACHINE.machine_body.model.append_xml_attributes(model_node)
        MACHINE.machine_body.crate_object.append_xml_attributes(crate_object_node)
        MACHINE.machine_body.modifier_shader.append_xml_attributes(modifier_shader_node)
        MACHINE.machine_body.creation_effect.append_xml_attributes(creation_effect_node)
        MACHINE.machine_body.material_effects.append_xml_attributes(material_effects_node)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, MACHINE.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return MACHINE
