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
from .format_retail import SoundSceneryAsset, ObjectFlags, ObjectFunctionEnum

XML_OUTPUT = False

def process_file_retail(input_stream, tag_format, report):
    TAG = tag_format.TagAsset()
    SOUNDSCENERY = SoundSceneryAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    SOUNDSCENERY.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    SOUNDSCENERY.sound_scenery_body = SOUNDSCENERY.SoundSceneryBody()
    input_stream.read(2) # Padding?
    SOUNDSCENERY.sound_scenery_body.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    SOUNDSCENERY.sound_scenery_body.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    SOUNDSCENERY.sound_scenery_body.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    SOUNDSCENERY.sound_scenery_body.origin_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "origin offset"))
    SOUNDSCENERY.sound_scenery_body.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    input_stream.read(4) # Padding?
    SOUNDSCENERY.sound_scenery_body.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    SOUNDSCENERY.sound_scenery_body.animation_graph = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "animation graph"))
    input_stream.read(40) # Padding?
    SOUNDSCENERY.sound_scenery_body.collision_model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision model"))
    SOUNDSCENERY.sound_scenery_body.physics = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "physics"))
    SOUNDSCENERY.sound_scenery_body.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    SOUNDSCENERY.sound_scenery_body.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    input_stream.read(84) # Padding?
    SOUNDSCENERY.sound_scenery_body.render_bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "render bounding radius"))
    SOUNDSCENERY.sound_scenery_body.a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", ObjectFunctionEnum))
    SOUNDSCENERY.sound_scenery_body.b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", ObjectFunctionEnum))
    SOUNDSCENERY.sound_scenery_body.c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", ObjectFunctionEnum))
    SOUNDSCENERY.sound_scenery_body.d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", ObjectFunctionEnum))
    input_stream.read(44) # Padding?
    SOUNDSCENERY.sound_scenery_body.hud_text_message_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    SOUNDSCENERY.sound_scenery_body.forced_shader_permutation_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "forced shader_permutation index"))
    SOUNDSCENERY.sound_scenery_body.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    SOUNDSCENERY.sound_scenery_body.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    SOUNDSCENERY.sound_scenery_body.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    SOUNDSCENERY.sound_scenery_body.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    SOUNDSCENERY.sound_scenery_body.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    input_stream.read(128) # Padding?

    if SOUNDSCENERY.sound_scenery_body.model.name_length > 0:
        SOUNDSCENERY.sound_scenery_body.model.name = TAG.read_variable_string(input_stream, SOUNDSCENERY.sound_scenery_body.model.name_length, TAG)

    if SOUNDSCENERY.sound_scenery_body.animation_graph.name_length > 0:
        SOUNDSCENERY.sound_scenery_body.animation_graph.name = TAG.read_variable_string(input_stream, SOUNDSCENERY.sound_scenery_body.animation_graph.name_length, TAG)

    if SOUNDSCENERY.sound_scenery_body.collision_model.name_length > 0:
        SOUNDSCENERY.sound_scenery_body.collision_model.name = TAG.read_variable_string(input_stream, SOUNDSCENERY.sound_scenery_body.collision_model.name_length, TAG)

    if SOUNDSCENERY.sound_scenery_body.physics.name_length > 0:
        SOUNDSCENERY.sound_scenery_body.physics.name = TAG.read_variable_string(input_stream, SOUNDSCENERY.sound_scenery_body.physics.name_length, TAG)

    if SOUNDSCENERY.sound_scenery_body.modifier_shader.name_length > 0:
        SOUNDSCENERY.sound_scenery_body.modifier_shader.name = TAG.read_variable_string(input_stream, SOUNDSCENERY.sound_scenery_body.modifier_shader.name_length, TAG)

    if SOUNDSCENERY.sound_scenery_body.creation_effect.name_length > 0:
        SOUNDSCENERY.sound_scenery_body.creation_effect.name = TAG.read_variable_string(input_stream, SOUNDSCENERY.sound_scenery_body.creation_effect.name_length, TAG)

    if XML_OUTPUT:
        model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "model")
        animation_graph_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "animation graph")
        collision_model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "collision model")
        physics_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "physics")
        modifier_shader_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "modifier shader")
        creation_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "creation effect")
        SOUNDSCENERY.sound_scenery_body.model.append_xml_attributes(model_node)
        SOUNDSCENERY.sound_scenery_body.animation_graph.append_xml_attributes(animation_graph_node)
        SOUNDSCENERY.sound_scenery_body.collision_model.append_xml_attributes(collision_model_node)
        SOUNDSCENERY.sound_scenery_body.physics.append_xml_attributes(physics_node)
        SOUNDSCENERY.sound_scenery_body.modifier_shader.append_xml_attributes(modifier_shader_node)
        SOUNDSCENERY.sound_scenery_body.creation_effect.append_xml_attributes(creation_effect_node)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, SOUNDSCENERY.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return SOUNDSCENERY
