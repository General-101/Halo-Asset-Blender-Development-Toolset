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
from .format_retail import ControlAsset, ObjectFlags, ObjectFunctionEnum, DeviceFlags, DeviceFunctionEnum, ControlTypeEnum, ControlFlags

XML_OUTPUT = False

def process_file_retail(input_stream, tag_format, report):
    TAG = tag_format.TagAsset()
    CONTROL = ControlAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    CONTROL.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    CONTROL.control_body = CONTROL.ControlBody()
    input_stream.read(2) # Padding?
    CONTROL.control_body.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    CONTROL.control_body.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    CONTROL.control_body.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    CONTROL.control_body.origin_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "origin offset"))
    CONTROL.control_body.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    input_stream.read(4) # Padding?
    CONTROL.control_body.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    CONTROL.control_body.animation_graph = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "animation graph"))
    input_stream.read(40) # Padding?
    CONTROL.control_body.collision_model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision model"))
    CONTROL.control_body.physics = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "physics"))
    CONTROL.control_body.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    CONTROL.control_body.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    input_stream.read(84) # Padding?
    CONTROL.control_body.render_bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "render bounding radius"))
    CONTROL.control_body.object_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", ObjectFunctionEnum))
    CONTROL.control_body.object_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", ObjectFunctionEnum))
    CONTROL.control_body.object_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", ObjectFunctionEnum))
    CONTROL.control_body.object_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", ObjectFunctionEnum))
    input_stream.read(44) # Padding?
    CONTROL.control_body.hud_text_message_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    CONTROL.control_body.forced_shader_permutation_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "forced shader_permutation index"))
    CONTROL.control_body.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    CONTROL.control_body.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    CONTROL.control_body.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    CONTROL.control_body.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change_colors"))
    CONTROL.control_body.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted_resources"))
    input_stream.read(2) # Padding?
    CONTROL.control_body.device_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", DeviceFlags))
    CONTROL.control_body.power_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "power transition time"))
    CONTROL.control_body.power_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "power acceleration time"))
    CONTROL.control_body.position_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "position transition time"))
    CONTROL.control_body.position_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "position acceleration time"))
    CONTROL.control_body.depowered_position_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "depowered position transition time"))
    CONTROL.control_body.depowered_position_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "depowered position acceleration time"))
    CONTROL.control_body.machine_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", DeviceFunctionEnum))
    CONTROL.control_body.machine_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", DeviceFunctionEnum))
    CONTROL.control_body.machine_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", DeviceFunctionEnum))
    CONTROL.control_body.machine_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", DeviceFunctionEnum))
    CONTROL.control_body.open_up = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "open up"))
    CONTROL.control_body.close_down = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "close down"))
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
    CONTROL.control_body.control_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ControlFlags))
    CONTROL.control_body.call_value = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "call value"))
    input_stream.read(80) # Padding?
    CONTROL.control_body.on = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "on"))
    CONTROL.control_body.off = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "off"))
    CONTROL.control_body.delay = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "delay"))

    if CONTROL.control_body.model.name_length > 0:
        CONTROL.control_body.model.name = TAG.read_variable_string(input_stream, CONTROL.control_body.model.name_length, TAG)

    if CONTROL.control_body.animation_graph.name_length > 0:
        CONTROL.control_body.animation_graph.name = TAG.read_variable_string(input_stream, CONTROL.control_body.animation_graph.name_length, TAG)

    if CONTROL.control_body.collision_model.name_length > 0:
        CONTROL.control_body.collision_model.name = TAG.read_variable_string(input_stream, CONTROL.control_body.collision_model.name_length, TAG)

    if CONTROL.control_body.physics.name_length > 0:
        CONTROL.control_body.physics.name = TAG.read_variable_string(input_stream, CONTROL.control_body.physics.name_length, TAG)

    if CONTROL.control_body.modifier_shader.name_length > 0:
        CONTROL.control_body.modifier_shader.name = TAG.read_variable_string(input_stream, CONTROL.control_body.modifier_shader.name_length, TAG)

    if CONTROL.control_body.creation_effect.name_length > 0:
        CONTROL.control_body.creation_effect.name = TAG.read_variable_string(input_stream, CONTROL.control_body.creation_effect.name_length, TAG)

    if CONTROL.control_body.open_up.name_length > 0:
        CONTROL.control_body.open_up.name = TAG.read_variable_string(input_stream, CONTROL.control_body.open_up.name_length, TAG)

    if CONTROL.control_body.close_down.name_length > 0:
        CONTROL.control_body.close_down.name = TAG.read_variable_string(input_stream, CONTROL.control_body.close_down.name_length, TAG)

    if CONTROL.control_body.opened.name_length > 0:
        CONTROL.control_body.opened.name = TAG.read_variable_string(input_stream, CONTROL.control_body.opened.name_length, TAG)

    if CONTROL.control_body.closed.name_length > 0:
        CONTROL.control_body.closed.name = TAG.read_variable_string(input_stream, CONTROL.control_body.closed.name_length, TAG)

    if CONTROL.control_body.depowered.name_length > 0:
        CONTROL.control_body.depowered.name = TAG.read_variable_string(input_stream, CONTROL.control_body.depowered.name_length, TAG)

    if CONTROL.control_body.repowered.name_length > 0:
        CONTROL.control_body.repowered.name = TAG.read_variable_string(input_stream, CONTROL.control_body.repowered.name_length, TAG)

    if CONTROL.control_body.delay_effect.name_length > 0:
        CONTROL.control_body.delay_effect.name = TAG.read_variable_string(input_stream, CONTROL.control_body.delay_effect.name_length, TAG)

    if CONTROL.control_body.on.name_length > 0:
        CONTROL.control_body.on.name = TAG.read_variable_string(input_stream, CONTROL.control_body.on.name_length, TAG)

    if CONTROL.control_body.off.name_length > 0:
        CONTROL.control_body.off.name = TAG.read_variable_string(input_stream, CONTROL.control_body.off.name_length, TAG)

    if CONTROL.control_body.delay.name_length > 0:
        CONTROL.control_body.delay.name = TAG.read_variable_string(input_stream, CONTROL.control_body.delay.name_length, TAG)

    if XML_OUTPUT:
        model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "model")
        animation_graph_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "animation graph")
        collision_model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "collision model")
        physics_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "physics")
        modifier_shader_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "modifier shader")
        creation_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "creation effect")
        open_up_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "open up")
        close_down_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "close down")
        opened_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "opened")
        closed_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "closed")
        depowered_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "depowered")
        repowered_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "repowered")
        delay_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "delay effect")
        on_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "on")
        off_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "off")
        delay_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "delay")
        CONTROL.control_body.model.append_xml_attributes(model_node)
        CONTROL.control_body.animation_graph.append_xml_attributes(animation_graph_node)
        CONTROL.control_body.collision_model.append_xml_attributes(collision_model_node)
        CONTROL.control_body.physics.append_xml_attributes(physics_node)
        CONTROL.control_body.modifier_shader.append_xml_attributes(modifier_shader_node)
        CONTROL.control_body.creation_effect.append_xml_attributes(creation_effect_node)
        CONTROL.control_body.open_up.append_xml_attributes(open_up_node)
        CONTROL.control_body.close_down.append_xml_attributes(close_down_node)
        CONTROL.control_body.opened.append_xml_attributes(opened_node)
        CONTROL.control_body.closed.append_xml_attributes(closed_node)
        CONTROL.control_body.depowered.append_xml_attributes(depowered_node)
        CONTROL.control_body.repowered.append_xml_attributes(repowered_node)
        CONTROL.control_body.delay_effect.append_xml_attributes(delay_effect_node)
        CONTROL.control_body.on.append_xml_attributes(on_node)
        CONTROL.control_body.off.append_xml_attributes(off_node)
        CONTROL.control_body.delay.append_xml_attributes(delay_node)

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
