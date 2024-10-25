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
        ModelAsset,
        ShadowFadeDistanceEnum,
        ModelFlags,
        RuntimeFlags,
        SALT_SIZE
        )

XML_OUTPUT = False

def initilize_model(MODEL):
    MODEL.variants = []
    MODEL.materials = []
    MODEL.new_damage_info = []
    MODEL.targets = []
    MODEL.runtime_regions = []
    MODEL.runtime_nodes = []
    MODEL.model_object_data = []
    MODEL.scenario_load_parameters = []

def read_model_body_v0(MODEL, TAG, input_stream, tag_node, XML_OUTPUT):
    MODEL.body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    MODEL.render_model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "render model"))
    MODEL.collision_model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision model"))
    MODEL.animation = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "animation"))
    MODEL.physics = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "physics"))
    MODEL.physics_model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "physics model"))
    MODEL.disappear_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "disappear distance"))
    MODEL.begin_fade_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "begin fade distance"))
    input_stream.read(4) # Padding?
    MODEL.reduce_to_l1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "reduce to l1"))
    MODEL.reduce_to_l2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "reduce to l2"))
    MODEL.reduce_to_l3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "reduce to l3"))
    MODEL.reduce_to_l4 = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "reduce to l4"))
    MODEL.reduce_to_l5 = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "reduce to l5"))
    input_stream.read(4) # Padding?
    MODEL.shadow_fade_distance = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "shadow fade distance", ShadowFadeDistanceEnum))
    input_stream.read(2) # Padding?
    MODEL.variants_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "variants"))
    MODEL.materials_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "materials"))
    MODEL.new_damage_info_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "new damage info"))
    MODEL.targets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "targets"))
    MODEL.runtime_regions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "runtime regions"))
    MODEL.runtime_nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "runtime nodes"))
    input_stream.read(4) # Padding?
    MODEL.model_object_data_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "model object data"))

    MODEL.default_dialogue = TAG.TagRef()
    MODEL.unused = TAG.TagRef()
    MODEL.salt_array = []
    MODEL.scenario_load_parameters_tag_block = TAG.TagBlock()
    MODEL.hologram_shader = TAG.TagRef()

    if MODEL.body_header.size >= 224:
        MODEL.default_dialogue = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "default dialogue"))

    if MODEL.body_header.size >= 240:
        MODEL.unused = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "unused"))

    if MODEL.body_header.size >= 244:
        MODEL.flags = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ModelFlags))
        input_stream.read(2) # Padding?

    if MODEL.body_header.size >= 248:
        TAG.big_endian = True
        input_stream.read(2) # Padding?
        MODEL.default_dialogue_effect_length = TAG.read_signed_short(input_stream, TAG)
        TAG.big_endian = False

    if MODEL.body_header.size >= 316:
        for salt_idx in range(SALT_SIZE):
            MODEL.salt_array.append(TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(tag_node, "salt %s" % salt_idx)))

        MODEL.runtime_flags = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "runtime flags", RuntimeFlags))
        input_stream.read(2) # Padding?

    if MODEL.body_header.size >= 328:
        MODEL.scenario_load_parameters_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "scenariom load parameters"))

    if MODEL.body_header.size >= 348:
        MODEL.hologram_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "hologram shader"))

        TAG.big_endian = True
        input_stream.read(2) # Padding?
        MODEL.hologram_control_function_length = TAG.read_signed_short(input_stream, TAG)
        TAG.big_endian = False

def read_model_body_retail(MODEL, TAG, input_stream, tag_node, XML_OUTPUT):
    MODEL.body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    MODEL.render_model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "render model"))
    MODEL.collision_model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision model"))
    MODEL.animation = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "animation"))
    MODEL.physics = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "physics"))
    MODEL.physics_model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "physics model"))
    MODEL.disappear_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "disappear distance"))
    MODEL.begin_fade_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "begin fade distance"))
    input_stream.read(4) # Padding?
    MODEL.reduce_to_l1 = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "reduce to l1"))
    MODEL.reduce_to_l2 = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "reduce to l2"))
    MODEL.reduce_to_l3 = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "reduce to l3"))
    MODEL.reduce_to_l4 = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "reduce to l4"))
    MODEL.reduce_to_l5 = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "reduce to l5"))
    input_stream.read(4) # Padding?
    MODEL.shadow_fade_distance = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "shadow fade distance", ShadowFadeDistanceEnum))
    input_stream.read(2) # Padding?
    MODEL.variants_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "variants"))
    MODEL.materials_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "materials"))
    MODEL.new_damage_info_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "new damage info"))
    MODEL.targets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "targets"))
    MODEL.runtime_regions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "runtime regions"))
    MODEL.runtime_nodes_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "runtime nodes"))
    input_stream.read(4) # Padding?
    MODEL.model_object_data_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "model object data"))
    MODEL.default_dialogue = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "default dialogue"))
    MODEL.unused = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "unused"))
    MODEL.flags = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ModelFlags))
    input_stream.read(2) # Padding?

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    MODEL.default_dialogue_effect_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    MODEL.salt_array = []
    for salt_idx in range(SALT_SIZE):
        MODEL.salt_array.append(TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(tag_node, "salt %s" % salt_idx)))

    MODEL.runtime_flags = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "runtime flags", RuntimeFlags))
    input_stream.read(2) # Padding?
    MODEL.scenario_load_parameters_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "scenariom load parameters"))
    MODEL.hologram_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "hologram shader"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    MODEL.hologram_control_function_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    MODEL = ModelAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    MODEL.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    initilize_model(MODEL)
    if MODEL.header.engine_tag == "LAMB":
        read_model_body_v0(MODEL, TAG, input_stream, tag_node, XML_OUTPUT)
    elif MODEL.header.engine_tag == "MLAB":
        read_model_body_retail(MODEL, TAG, input_stream, tag_node, XML_OUTPUT)
    elif MODEL.header.engine_tag == "BLM!":
        read_model_body_retail(MODEL, TAG, input_stream, tag_node, XML_OUTPUT)

    if MODEL.render_model.name_length > 0:
        MODEL.render_model.name = TAG.read_variable_string(input_stream, MODEL.render_model.name_length, TAG)

    if MODEL.collision_model.name_length > 0:
        MODEL.collision_model.name = TAG.read_variable_string(input_stream, MODEL.collision_model.name_length, TAG)

    if MODEL.animation.name_length > 0:
        MODEL.animation.name = TAG.read_variable_string(input_stream, MODEL.animation.name_length, TAG)

    if MODEL.physics.name_length > 0:
        MODEL.physics.name = TAG.read_variable_string(input_stream, MODEL.physics.name_length, TAG)

    if MODEL.physics_model.name_length > 0:
        MODEL.physics_model.name = TAG.read_variable_string(input_stream, MODEL.physics_model.name_length, TAG)

    #if MODEL.default_dialogue.name_length > 0:
        #MODEL.default_dialogue.name = TAG.read_variable_string(input_stream, MODEL.default_dialogue.name_length, TAG)

    #if MODEL.unused.name_length > 0:
        #MODEL.unused.name = TAG.read_variable_string(input_stream, MODEL.unused.name_length, TAG)

    #if MODEL.default_dialogue_effect_length > 0:
        #MODEL.default_dialogue_effect = TAG.read_variable_string_no_terminator(input_stream, MODEL.default_dialogue_effect_length, TAG, tag_format.XMLData(tag_node, "default dialogue effect"))

    #if MODEL.hologram_shader.name_length > 0:
        #MODEL.hologram_shader.name = TAG.read_variable_string(input_stream, MODEL.hologram_shader.name_length, TAG)

    #if MODEL.hologram_control_function_length > 0:
        #MODEL.hologram_control_function = TAG.read_variable_string_no_terminator(input_stream, MODEL.hologram_control_function_length, TAG, tag_format.XMLData(tag_node, "hologram control function"))

    if XML_OUTPUT:
        render_model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "render model")
        collision_model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "collision model")
        animation_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "animation")
        physics_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "physics")
        physics_model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "physics model")
        #default_dialogue_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "default dialogue")
        #unused_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "unused")
        #hologram_shader_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "hologram shader")
        MODEL.render_model.append_xml_attributes(render_model_node)
        MODEL.collision_model.append_xml_attributes(collision_model_node)
        MODEL.animation.append_xml_attributes(animation_node)
        MODEL.physics.append_xml_attributes(physics_node)
        MODEL.physics_model.append_xml_attributes(physics_model_node)
        #MODEL.default_dialogue.append_xml_attributes(default_dialogue_node)
        #MODEL.unused.append_xml_attributes(unused_node)
        #MODEL.hologram_shader.append_xml_attributes(hologram_shader_node)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, MODEL.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return MODEL
