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
from .format import ControlAsset, ObjectFlags, ObjectFunctionEnum, DeviceFlags, DeviceFunctionEnum, ControlTypeEnum, ControlFlags

XML_OUTPUT = False

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    CONTROL = ControlAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    CONTROL.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    input_stream.read(2) # Padding?
    CONTROL.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    CONTROL.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    CONTROL.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    CONTROL.origin_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "origin offset"))
    CONTROL.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    input_stream.read(4) # Padding?
    CONTROL.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    CONTROL.animation_graph = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "animation graph"))
    input_stream.read(40) # Padding?
    CONTROL.collision_model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision model"))
    CONTROL.physics = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "physics"))
    CONTROL.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    CONTROL.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    input_stream.read(84) # Padding?
    CONTROL.render_bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "render bounding radius"))
    CONTROL.object_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", ObjectFunctionEnum))
    CONTROL.object_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", ObjectFunctionEnum))
    CONTROL.object_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", ObjectFunctionEnum))
    CONTROL.object_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", ObjectFunctionEnum))
    input_stream.read(44) # Padding?
    CONTROL.hud_text_message_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    CONTROL.forced_shader_permutation_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "forced shader_permutation index"))
    CONTROL.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    CONTROL.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    CONTROL.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    CONTROL.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change_colors"))
    CONTROL.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted_resources"))
    input_stream.read(2) # Padding?
    CONTROL.device_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", DeviceFlags))
    CONTROL.power_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "power transition time"))
    CONTROL.power_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "power acceleration time"))
    CONTROL.position_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "position transition time"))
    CONTROL.position_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "position acceleration time"))
    CONTROL.depowered_position_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "depowered position transition time"))
    CONTROL.depowered_position_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "depowered position acceleration time"))
    CONTROL.machine_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", DeviceFunctionEnum))
    CONTROL.machine_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", DeviceFunctionEnum))
    CONTROL.machine_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", DeviceFunctionEnum))
    CONTROL.machine_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", DeviceFunctionEnum))
    CONTROL.open_up = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "open up"))
    CONTROL.close_down = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "close down"))
    CONTROL.opened = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "opened"))
    CONTROL.closed = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "closed"))
    CONTROL.depowered = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "depowered"))
    CONTROL.repowered = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "repowered"))
    CONTROL.delay_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "delay time"))
    input_stream.read(8) # Padding?
    CONTROL.delay_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "delay effect"))
    CONTROL.automatic_activation_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "automatic activation radius"))
    input_stream.read(112) # Padding?
    CONTROL.control_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "type", ControlTypeEnum))
    CONTROL.control_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ControlFlags))
    CONTROL.call_value = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "call value"))
    input_stream.read(80) # Padding?
    CONTROL.on = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "on"))
    CONTROL.off = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "off"))
    CONTROL.delay = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "delay"))

    if CONTROL.model.name_length > 0:
        CONTROL.model.name = TAG.read_variable_string(input_stream, CONTROL.model.name_length, TAG)

    if CONTROL.animation_graph.name_length > 0:
        CONTROL.animation_graph.name = TAG.read_variable_string(input_stream, CONTROL.animation_graph.name_length, TAG)

    if CONTROL.collision_model.name_length > 0:
        CONTROL.collision_model.name = TAG.read_variable_string(input_stream, CONTROL.collision_model.name_length, TAG)

    if CONTROL.physics.name_length > 0:
        CONTROL.physics.name = TAG.read_variable_string(input_stream, CONTROL.physics.name_length, TAG)

    if CONTROL.modifier_shader.name_length > 0:
        CONTROL.modifier_shader.name = TAG.read_variable_string(input_stream, CONTROL.modifier_shader.name_length, TAG)

    if CONTROL.creation_effect.name_length > 0:
        CONTROL.creation_effect.name = TAG.read_variable_string(input_stream, CONTROL.creation_effect.name_length, TAG)

    if CONTROL.open_up.name_length > 0:
        CONTROL.open_up.name = TAG.read_variable_string(input_stream, CONTROL.open_up.name_length, TAG)

    if CONTROL.close_down.name_length > 0:
        CONTROL.close_down.name = TAG.read_variable_string(input_stream, CONTROL.close_down.name_length, TAG)

    if CONTROL.opened.name_length > 0:
        CONTROL.opened.name = TAG.read_variable_string(input_stream, CONTROL.opened.name_length, TAG)

    if CONTROL.closed.name_length > 0:
        CONTROL.closed.name = TAG.read_variable_string(input_stream, CONTROL.closed.name_length, TAG)

    if CONTROL.depowered.name_length > 0:
        CONTROL.depowered.name = TAG.read_variable_string(input_stream, CONTROL.depowered.name_length, TAG)

    if CONTROL.repowered.name_length > 0:
        CONTROL.repowered.name = TAG.read_variable_string(input_stream, CONTROL.repowered.name_length, TAG)

    if CONTROL.delay_effect.name_length > 0:
        CONTROL.delay_effect.name = TAG.read_variable_string(input_stream, CONTROL.delay_effect.name_length, TAG)

    if CONTROL.on.name_length > 0:
        CONTROL.on.name = TAG.read_variable_string(input_stream, CONTROL.on.name_length, TAG)

    if CONTROL.off.name_length > 0:
        CONTROL.off.name = TAG.read_variable_string(input_stream, CONTROL.off.name_length, TAG)

    if CONTROL.delay.name_length > 0:
        CONTROL.delay.name = TAG.read_variable_string(input_stream, CONTROL.delay.name_length, TAG)

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
        CONTROL.model.append_xml_attributes(model_node)
        CONTROL.animation_graph.append_xml_attributes(animation_graph_node)
        CONTROL.collision_model.append_xml_attributes(collision_model_node)
        CONTROL.physics.append_xml_attributes(physics_node)
        CONTROL.modifier_shader.append_xml_attributes(modifier_shader_node)
        CONTROL.creation_effect.append_xml_attributes(creation_effect_node)
        CONTROL.open_up.append_xml_attributes(open_up_node)
        CONTROL.close_down.append_xml_attributes(close_down_node)
        CONTROL.opened.append_xml_attributes(opened_node)
        CONTROL.closed.append_xml_attributes(closed_node)
        CONTROL.depowered.append_xml_attributes(depowered_node)
        CONTROL.repowered.append_xml_attributes(repowered_node)
        CONTROL.delay_effect.append_xml_attributes(delay_effect_node)
        CONTROL.on.append_xml_attributes(on_node)
        CONTROL.off.append_xml_attributes(off_node)
        CONTROL.delay.append_xml_attributes(delay_node)

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
