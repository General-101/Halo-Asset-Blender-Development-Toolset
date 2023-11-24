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
from .format import MachineAsset, ObjectFlags, ObjectFunctionEnum, DeviceFlags, DeviceFunctionEnum, MachineTypeEnum, MachineFlags, CollisionResponseEnum

XML_OUTPUT = False

def process_file(input_stream, tag_format, report):
    TAG = tag_format.TagAsset()
    MACHINE = MachineAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    MACHINE.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    MACHINE.machine_body = MACHINE.MachineBody()
    input_stream.read(2) # Padding?
    MACHINE.machine_body.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    MACHINE.machine_body.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    MACHINE.machine_body.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    MACHINE.machine_body.origin_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "origin offset"))
    MACHINE.machine_body.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    input_stream.read(4) # Padding?
    MACHINE.machine_body.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    MACHINE.machine_body.animation_graph = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "animation graph"))
    input_stream.read(40) # Padding?
    MACHINE.machine_body.collision_model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision model"))
    MACHINE.machine_body.physics = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "physics"))
    MACHINE.machine_body.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    MACHINE.machine_body.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    input_stream.read(84) # Padding?
    MACHINE.machine_body.render_bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "render bounding radius"))
    MACHINE.machine_body.object_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", ObjectFunctionEnum))
    MACHINE.machine_body.object_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", ObjectFunctionEnum))
    MACHINE.machine_body.object_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", ObjectFunctionEnum))
    MACHINE.machine_body.object_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", ObjectFunctionEnum))
    input_stream.read(44) # Padding?
    MACHINE.machine_body.hud_text_message_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    MACHINE.machine_body.forced_shader_permutation_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "forced shader_permutation index"))
    MACHINE.machine_body.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    MACHINE.machine_body.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    MACHINE.machine_body.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    MACHINE.machine_body.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change_colors"))
    MACHINE.machine_body.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted_resources"))
    input_stream.read(2) # Padding?
    MACHINE.machine_body.device_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", DeviceFlags))
    MACHINE.machine_body.power_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "power transition time"))
    MACHINE.machine_body.power_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "power acceleration time"))
    MACHINE.machine_body.position_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "position transition time"))
    MACHINE.machine_body.position_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "position acceleration time"))
    MACHINE.machine_body.depowered_position_transition_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "depowered position transition time"))
    MACHINE.machine_body.depowered_position_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "depowered position acceleration time"))
    MACHINE.machine_body.machine_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", DeviceFunctionEnum))
    MACHINE.machine_body.machine_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", DeviceFunctionEnum))
    MACHINE.machine_body.machine_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", DeviceFunctionEnum))
    MACHINE.machine_body.machine_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", DeviceFunctionEnum))
    MACHINE.machine_body.open_up = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "open up"))
    MACHINE.machine_body.close_down = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "close down"))
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
    input_stream.read(80) # Padding?
    MACHINE.machine_body.collision_response = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "collision response", CollisionResponseEnum))
    MACHINE.machine_body.elevator_node = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "elevator node"))
    input_stream.read(56) # Padding?

    if MACHINE.machine_body.model.name_length > 0:
        MACHINE.machine_body.model.name = TAG.read_variable_string(input_stream, MACHINE.machine_body.model.name_length, TAG)

    if MACHINE.machine_body.animation_graph.name_length > 0:
        MACHINE.machine_body.animation_graph.name = TAG.read_variable_string(input_stream, MACHINE.machine_body.animation_graph.name_length, TAG)

    if MACHINE.machine_body.collision_model.name_length > 0:
        MACHINE.machine_body.collision_model.name = TAG.read_variable_string(input_stream, MACHINE.machine_body.collision_model.name_length, TAG)

    if MACHINE.machine_body.physics.name_length > 0:
        MACHINE.machine_body.physics.name = TAG.read_variable_string(input_stream, MACHINE.machine_body.physics.name_length, TAG)

    if MACHINE.machine_body.modifier_shader.name_length > 0:
        MACHINE.machine_body.modifier_shader.name = TAG.read_variable_string(input_stream, MACHINE.machine_body.modifier_shader.name_length, TAG)

    if MACHINE.machine_body.creation_effect.name_length > 0:
        MACHINE.machine_body.creation_effect.name = TAG.read_variable_string(input_stream, MACHINE.machine_body.creation_effect.name_length, TAG)

    if MACHINE.machine_body.open_up.name_length > 0:
        MACHINE.machine_body.open_up.name = TAG.read_variable_string(input_stream, MACHINE.machine_body.open_up.name_length, TAG)

    if MACHINE.machine_body.close_down.name_length > 0:
        MACHINE.machine_body.close_down.name = TAG.read_variable_string(input_stream, MACHINE.machine_body.close_down.name_length, TAG)

    if MACHINE.machine_body.opened.name_length > 0:
        MACHINE.machine_body.opened.name = TAG.read_variable_string(input_stream, MACHINE.machine_body.opened.name_length, TAG)

    if MACHINE.machine_body.closed.name_length > 0:
        MACHINE.machine_body.closed.name = TAG.read_variable_string(input_stream, MACHINE.machine_body.closed.name_length, TAG)

    if MACHINE.machine_body.depowered.name_length > 0:
        MACHINE.machine_body.depowered.name = TAG.read_variable_string(input_stream, MACHINE.machine_body.depowered.name_length, TAG)

    if MACHINE.machine_body.repowered.name_length > 0:
        MACHINE.machine_body.repowered.name = TAG.read_variable_string(input_stream, MACHINE.machine_body.repowered.name_length, TAG)

    if MACHINE.machine_body.delay_effect.name_length > 0:
        MACHINE.machine_body.delay_effect.name = TAG.read_variable_string(input_stream, MACHINE.machine_body.delay_effect.name_length, TAG)

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
        MACHINE.machine_body.model.append_xml_attributes(model_node)
        MACHINE.machine_body.animation_graph.append_xml_attributes(animation_graph_node)
        MACHINE.machine_body.collision_model.append_xml_attributes(collision_model_node)
        MACHINE.machine_body.physics.append_xml_attributes(physics_node)
        MACHINE.machine_body.modifier_shader.append_xml_attributes(modifier_shader_node)
        MACHINE.machine_body.creation_effect.append_xml_attributes(creation_effect_node)
        MACHINE.machine_body.open_up.append_xml_attributes(open_up_node)
        MACHINE.machine_body.close_down.append_xml_attributes(close_down_node)
        MACHINE.machine_body.opened.append_xml_attributes(opened_node)
        MACHINE.machine_body.closed.append_xml_attributes(closed_node)
        MACHINE.machine_body.depowered.append_xml_attributes(depowered_node)
        MACHINE.machine_body.repowered.append_xml_attributes(repowered_node)
        MACHINE.machine_body.delay_effect.append_xml_attributes(delay_effect_node)

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
