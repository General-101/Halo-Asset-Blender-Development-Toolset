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
from .format import LightFixtureAsset, ObjectFlags, ObjectFunctionEnum, DeviceFlags, DeviceFunctionEnum

XML_OUTPUT = False

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    LIGHTFIXTURE = LightFixtureAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    LIGHTFIXTURE.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    input_stream.read(2) # Padding?
    LIGHTFIXTURE.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    LIGHTFIXTURE.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    LIGHTFIXTURE.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    LIGHTFIXTURE.origin_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "origin offset"))
    LIGHTFIXTURE.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    input_stream.read(4) # Padding?
    LIGHTFIXTURE.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    LIGHTFIXTURE.animation_graph = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "animation graph"))
    input_stream.read(40) # Padding?
    LIGHTFIXTURE.collision_model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision model"))
    LIGHTFIXTURE.physics = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "physics"))
    LIGHTFIXTURE.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    LIGHTFIXTURE.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    input_stream.read(84) # Padding?
    LIGHTFIXTURE.render_bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "render bounding radius"))
    LIGHTFIXTURE.object_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", ObjectFunctionEnum))
    LIGHTFIXTURE.object_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", ObjectFunctionEnum))
    LIGHTFIXTURE.object_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", ObjectFunctionEnum))
    LIGHTFIXTURE.object_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", ObjectFunctionEnum))
    input_stream.read(44) # Padding?
    LIGHTFIXTURE.hud_text_message_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    LIGHTFIXTURE.forced_shader_permutation_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "forced shader_permutation index"))
    LIGHTFIXTURE.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    LIGHTFIXTURE.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    LIGHTFIXTURE.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    LIGHTFIXTURE.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change_colors"))
    LIGHTFIXTURE.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted_resources"))
    input_stream.read(2) # Padding?
    LIGHTFIXTURE.device_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", DeviceFlags))
    LIGHTFIXTURE.power_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "power transition time"))
    LIGHTFIXTURE.power_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "power acceleration time"))
    LIGHTFIXTURE.position_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "position transition time"))
    LIGHTFIXTURE.position_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "position acceleration time"))
    LIGHTFIXTURE.depowered_position_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "depowered position transition time"))
    LIGHTFIXTURE.depowered_position_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "depowered position acceleration time"))
    LIGHTFIXTURE.machine_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", DeviceFunctionEnum))
    LIGHTFIXTURE.machine_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", DeviceFunctionEnum))
    LIGHTFIXTURE.machine_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", DeviceFunctionEnum))
    LIGHTFIXTURE.machine_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", DeviceFunctionEnum))
    LIGHTFIXTURE.open_up = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "open up"))
    LIGHTFIXTURE.close_down = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "close down"))
    LIGHTFIXTURE.opened = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "opened"))
    LIGHTFIXTURE.closed = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "closed"))
    LIGHTFIXTURE.depowered = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "depowered"))
    LIGHTFIXTURE.repowered = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "repowered"))
    LIGHTFIXTURE.delay_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "delay time"))
    input_stream.read(8) # Padding?
    LIGHTFIXTURE.delay_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "delay effect"))
    LIGHTFIXTURE.automatic_activation_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "automatic activation radius"))
    input_stream.read(176) # Padding?

    if LIGHTFIXTURE.model.name_length > 0:
        LIGHTFIXTURE.model.name = TAG.read_variable_string(input_stream, LIGHTFIXTURE.model.name_length, TAG)

    if LIGHTFIXTURE.animation_graph.name_length > 0:
        LIGHTFIXTURE.animation_graph.name = TAG.read_variable_string(input_stream, LIGHTFIXTURE.animation_graph.name_length, TAG)

    if LIGHTFIXTURE.collision_model.name_length > 0:
        LIGHTFIXTURE.collision_model.name = TAG.read_variable_string(input_stream, LIGHTFIXTURE.collision_model.name_length, TAG)

    if LIGHTFIXTURE.physics.name_length > 0:
        LIGHTFIXTURE.physics.name = TAG.read_variable_string(input_stream, LIGHTFIXTURE.physics.name_length, TAG)

    if LIGHTFIXTURE.modifier_shader.name_length > 0:
        LIGHTFIXTURE.modifier_shader.name = TAG.read_variable_string(input_stream, LIGHTFIXTURE.modifier_shader.name_length, TAG)

    if LIGHTFIXTURE.creation_effect.name_length > 0:
        LIGHTFIXTURE.creation_effect.name = TAG.read_variable_string(input_stream, LIGHTFIXTURE.creation_effect.name_length, TAG)

    if LIGHTFIXTURE.open_up.name_length > 0:
        LIGHTFIXTURE.open_up.name = TAG.read_variable_string(input_stream, LIGHTFIXTURE.open_up.name_length, TAG)

    if LIGHTFIXTURE.close_down.name_length > 0:
        LIGHTFIXTURE.close_down.name = TAG.read_variable_string(input_stream, LIGHTFIXTURE.close_down.name_length, TAG)

    if LIGHTFIXTURE.opened.name_length > 0:
        LIGHTFIXTURE.opened.name = TAG.read_variable_string(input_stream, LIGHTFIXTURE.opened.name_length, TAG)

    if LIGHTFIXTURE.closed.name_length > 0:
        LIGHTFIXTURE.closed.name = TAG.read_variable_string(input_stream, LIGHTFIXTURE.closed.name_length, TAG)

    if LIGHTFIXTURE.depowered.name_length > 0:
        LIGHTFIXTURE.depowered.name = TAG.read_variable_string(input_stream, LIGHTFIXTURE.depowered.name_length, TAG)

    if LIGHTFIXTURE.repowered.name_length > 0:
        LIGHTFIXTURE.repowered.name = TAG.read_variable_string(input_stream, LIGHTFIXTURE.repowered.name_length, TAG)

    if LIGHTFIXTURE.delay_effect.name_length > 0:
        LIGHTFIXTURE.delay_effect.name = TAG.read_variable_string(input_stream, LIGHTFIXTURE.delay_effect.name_length, TAG)

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
        LIGHTFIXTURE.model.append_xml_attributes(model_node)
        LIGHTFIXTURE.animation_graph.append_xml_attributes(animation_graph_node)
        LIGHTFIXTURE.collision_model.append_xml_attributes(collision_model_node)
        LIGHTFIXTURE.physics.append_xml_attributes(physics_node)
        LIGHTFIXTURE.modifier_shader.append_xml_attributes(modifier_shader_node)
        LIGHTFIXTURE.creation_effect.append_xml_attributes(creation_effect_node)
        LIGHTFIXTURE.open_up.append_xml_attributes(open_up_node)
        LIGHTFIXTURE.close_down.append_xml_attributes(close_down_node)
        LIGHTFIXTURE.opened.append_xml_attributes(opened_node)
        LIGHTFIXTURE.closed.append_xml_attributes(closed_node)
        LIGHTFIXTURE.depowered.append_xml_attributes(depowered_node)
        LIGHTFIXTURE.repowered.append_xml_attributes(repowered_node)
        LIGHTFIXTURE.delay_effect.append_xml_attributes(delay_effect_node)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, LIGHTFIXTURE.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return LIGHTFIXTURE
