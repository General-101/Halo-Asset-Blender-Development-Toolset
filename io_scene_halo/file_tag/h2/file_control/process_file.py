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
from ..file_object.format import ObjectFlags, LightmapShadowModeEnum, SweetenerSizeEnum
from ..file_device.format import DeviceFlags, LightmapFlags
from .format import ControlAsset, ControlTypeEnum, TriggersWhenEnum

XML_OUTPUT = False

def initilize_CONTROL(CONTROL):
    CONTROL.ai_properties = []
    CONTROL.functions = []
    CONTROL.attachments = []
    CONTROL.widgets = []
    CONTROL.old_functions = []
    CONTROL.change_colors = []
    CONTROL.predicted_resources = []

def read_control_body_v0(CONTROL, TAG, input_stream, tag_node, XML_OUTPUT):
    CONTROL.control_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    CONTROL.control_body = CONTROL.ControlBody()
    input_stream.read(2) # Padding?
    CONTROL.control_body.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    CONTROL.control_body.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    CONTROL.control_body.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    input_stream.read(12) # Padding?
    CONTROL.control_body.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    CONTROL.control_body.lightmap_shadow_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap shadow mode", LightmapShadowModeEnum))
    CONTROL.control_body.sweetner_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sweetner size", SweetenerSizeEnum))
    input_stream.read(36) # Padding?
    CONTROL.control_body.dynamic_light_sphere_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere radius"))
    CONTROL.control_body.dynamic_light_sphere_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere offset"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    CONTROL.control_body.default_model_variant_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    CONTROL.control_body.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    CONTROL.control_body.crate_object = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "crate object"))
    input_stream.read(16) # Padding?
    CONTROL.control_body.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    CONTROL.control_body.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    CONTROL.control_body.material_effects = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "material effects"))
    input_stream.read(24) # Padding?
    CONTROL.control_body.ai_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai properties"))
    input_stream.read(24) # Padding?
    CONTROL.control_body.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    input_stream.read(16) # Padding?
    CONTROL.control_body.apply_collision_damage_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "apply collision damage scale"))
    CONTROL.control_body.min_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game acc"))
    CONTROL.control_body.max_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game acc"))
    CONTROL.control_body.min_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game scale"))
    CONTROL.control_body.max_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game scale"))
    CONTROL.control_body.min_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs acc"))
    CONTROL.control_body.max_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs acc"))
    CONTROL.control_body.min_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs scale"))
    CONTROL.control_body.max_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs scale"))
    CONTROL.control_body.hud_text_message_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    input_stream.read(2) # Padding?
    CONTROL.control_body.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    CONTROL.control_body.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    CONTROL.control_body.old_functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "old functions"))
    CONTROL.control_body.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    CONTROL.control_body.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    CONTROL.control_body.device_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", DeviceFlags))
    input_stream.read(2) # Padding?
    CONTROL.control_body.power_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "power transition time"))
    CONTROL.control_body.power_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "power acceleration time"))
    CONTROL.control_body.position_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "position transition time"))
    CONTROL.control_body.position_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "position acceleration time"))
    CONTROL.control_body.depowered_position_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "depowered position transition time"))
    CONTROL.control_body.depowered_position_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "depowered position acceleration time"))
    CONTROL.control_body.lightmap_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap flags", LightmapFlags))
    input_stream.read(6) # Padding?
    CONTROL.control_body.open_up = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "open"))
    CONTROL.control_body.close_down = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "close"))
    CONTROL.control_body.opened = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "opened"))
    CONTROL.control_body.closed = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "closed"))
    CONTROL.control_body.depowered = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "depowered"))
    CONTROL.control_body.repowered = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "repowered"))
    CONTROL.control_body.delay_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "delay time"))
    input_stream.read(8) # Padding?
    CONTROL.control_body.delay_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "delay effect"))
    CONTROL.control_body.automatic_activation_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "automatic activation radius"))
    input_stream.read(112) # Padding?
    CONTROL.control_body.control_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "type", ControlTypeEnum))
    CONTROL.control_body.triggers_when = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "triggers when", TriggersWhenEnum))
    CONTROL.control_body.call_value = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "call value"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    CONTROL.control_body.action_string_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    CONTROL.control_body.on = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "on"))
    CONTROL.control_body.off = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "off"))
    CONTROL.control_body.deny = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "deny"))

def read_control_body_retail(CONTROL, TAG, input_stream, tag_node, XML_OUTPUT):
    CONTROL.control_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    CONTROL.control_body = CONTROL.ControlBody()
    input_stream.read(2) # Padding?
    CONTROL.control_body.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    CONTROL.control_body.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    CONTROL.control_body.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    CONTROL.control_body.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    CONTROL.control_body.lightmap_shadow_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap shadow mode", LightmapShadowModeEnum))
    CONTROL.control_body.sweetner_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sweetner size", SweetenerSizeEnum))
    input_stream.read(4) # Padding?
    CONTROL.control_body.dynamic_light_sphere_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere radius"))
    CONTROL.control_body.dynamic_light_sphere_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere offset"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    CONTROL.control_body.default_model_variant_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    CONTROL.control_body.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    CONTROL.control_body.crate_object = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "crate object"))
    CONTROL.control_body.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    CONTROL.control_body.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    CONTROL.control_body.material_effects = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "material effects"))
    CONTROL.control_body.ai_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai properties"))
    CONTROL.control_body.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    CONTROL.control_body.apply_collision_damage_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "apply collision damage scale"))
    CONTROL.control_body.min_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game acc"))
    CONTROL.control_body.max_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game acc"))
    CONTROL.control_body.min_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game scale"))
    CONTROL.control_body.max_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game scale"))
    CONTROL.control_body.min_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs acc"))
    CONTROL.control_body.max_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs acc"))
    CONTROL.control_body.min_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs scale"))
    CONTROL.control_body.max_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs scale"))
    CONTROL.control_body.hud_text_message_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    input_stream.read(2) # Padding?
    CONTROL.control_body.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    CONTROL.control_body.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    CONTROL.control_body.old_functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "old functions"))
    CONTROL.control_body.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    CONTROL.control_body.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    CONTROL.control_body.device_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", DeviceFlags))
    input_stream.read(2) # Padding?
    CONTROL.control_body.power_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "power transition time"))
    CONTROL.control_body.power_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "power acceleration time"))
    CONTROL.control_body.position_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "position transition time"))
    CONTROL.control_body.position_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "position acceleration time"))
    CONTROL.control_body.depowered_position_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "depowered position transition time"))
    CONTROL.control_body.depowered_position_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "depowered position acceleration time"))
    CONTROL.control_body.lightmap_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap flags", LightmapFlags))
    input_stream.read(2) # Padding?
    CONTROL.control_body.open_up = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "open"))
    CONTROL.control_body.close_down = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "close"))
    CONTROL.control_body.opened = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "opened"))
    CONTROL.control_body.closed = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "closed"))
    CONTROL.control_body.depowered = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "depowered"))
    CONTROL.control_body.repowered = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "repowered"))
    CONTROL.control_body.delay_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "delay time"))
    CONTROL.control_body.delay_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "delay effect"))
    CONTROL.control_body.automatic_activation_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "automatic activation radius"))
    CONTROL.control_body.control_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "type", ControlTypeEnum))
    CONTROL.control_body.triggers_when = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "triggers when", TriggersWhenEnum))
    CONTROL.control_body.call_value = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "call value"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    CONTROL.control_body.action_string_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    CONTROL.control_body.on = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "on"))
    CONTROL.control_body.off = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "off"))
    CONTROL.control_body.deny = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "deny"))

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    CONTROL = ControlAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    CONTROL.header = TAG.Header().read(input_stream, TAG)
    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    initilize_CONTROL(CONTROL)
    if CONTROL.header.engine_tag == "LAMB":
        read_control_body_v0(CONTROL, TAG, input_stream, tag_node, XML_OUTPUT)
    elif CONTROL.header.engine_tag == "MLAB":
        read_control_body_v0(CONTROL, TAG, input_stream, tag_node, XML_OUTPUT)
    elif CONTROL.header.engine_tag == "BLM!":
        read_control_body_retail(CONTROL, TAG, input_stream, tag_node, XML_OUTPUT)

    if CONTROL.control_body.default_model_variant_length > 0:
        CONTROL.control_body.default_model_variant = TAG.read_variable_string_no_terminator(input_stream, CONTROL.control_body.default_model_variant_length, TAG, tag_format.XMLData(tag_node, "default model variant"))

    if CONTROL.control_body.model.name_length > 0:
        CONTROL.control_body.model.name = TAG.read_variable_string(input_stream, CONTROL.control_body.model.name_length, TAG)

    if CONTROL.control_body.crate_object.name_length > 0:
        CONTROL.control_body.crate_object.name = TAG.read_variable_string(input_stream, CONTROL.control_body.crate_object.name_length, TAG)

    if CONTROL.control_body.modifier_shader.name_length > 0:
        CONTROL.control_body.modifier_shader.name = TAG.read_variable_string(input_stream, CONTROL.control_body.modifier_shader.name_length, TAG)

    if CONTROL.control_body.creation_effect.name_length > 0:
        CONTROL.control_body.creation_effect.name = TAG.read_variable_string(input_stream, CONTROL.control_body.creation_effect.name_length, TAG)

    if CONTROL.control_body.material_effects.name_length > 0:
        CONTROL.control_body.material_effects.name = TAG.read_variable_string(input_stream, CONTROL.control_body.material_effects.name_length, TAG)

    if XML_OUTPUT:
        model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "model")
        crate_object_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "crate object")
        modifier_shader_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "modifier shader")
        creation_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "creation effect")
        material_effects_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "material effects")
        CONTROL.control_body.model.append_xml_attributes(model_node)
        CONTROL.control_body.crate_object.append_xml_attributes(crate_object_node)
        CONTROL.control_body.modifier_shader.append_xml_attributes(modifier_shader_node)
        CONTROL.control_body.creation_effect.append_xml_attributes(creation_effect_node)
        CONTROL.control_body.material_effects.append_xml_attributes(material_effects_node)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, CONTROL.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return CONTROL
