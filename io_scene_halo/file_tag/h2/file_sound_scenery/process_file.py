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
from .format import SoundSceneryAsset

XML_OUTPUT = False

def initilize_scenery(SOUNDSCENERY):
    SOUNDSCENERY.ai_properties = []
    SOUNDSCENERY.functions = []
    SOUNDSCENERY.attachments = []
    SOUNDSCENERY.widgets = []
    SOUNDSCENERY.old_functions = []
    SOUNDSCENERY.change_colors = []
    SOUNDSCENERY.predicted_resources = []

def read_sound_scenery_body_v0(SOUNDSCENERY, TAG, input_stream, tag_node, XML_OUTPUT):
    SOUNDSCENERY.body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    input_stream.read(2) # Padding?
    SOUNDSCENERY.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    SOUNDSCENERY.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    SOUNDSCENERY.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    input_stream.read(12) # Padding?
    SOUNDSCENERY.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    SOUNDSCENERY.lightmap_shadow_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap shadow mode", LightmapShadowModeEnum))
    SOUNDSCENERY.sweetner_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sweetner size", SweetenerSizeEnum))
    input_stream.read(36) # Padding?
    SOUNDSCENERY.dynamic_light_sphere_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere radius"))
    SOUNDSCENERY.dynamic_light_sphere_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere offset"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    SOUNDSCENERY.default_model_variant_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    SOUNDSCENERY.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    SOUNDSCENERY.crate_object = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "crate object"))
    input_stream.read(16) # Padding?
    SOUNDSCENERY.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    SOUNDSCENERY.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    SOUNDSCENERY.material_effects = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "material effects"))
    input_stream.read(24) # Padding?
    SOUNDSCENERY.ai_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai properties"))
    input_stream.read(24) # Padding?
    SOUNDSCENERY.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    input_stream.read(16) # Padding?
    SOUNDSCENERY.apply_collision_damage_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "apply collision damage scale"))
    SOUNDSCENERY.min_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game acc"))
    SOUNDSCENERY.max_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game acc"))
    SOUNDSCENERY.min_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game scale"))
    SOUNDSCENERY.max_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game scale"))
    SOUNDSCENERY.min_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs acc"))
    SOUNDSCENERY.max_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs acc"))
    SOUNDSCENERY.min_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs scale"))
    SOUNDSCENERY.max_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs scale"))
    SOUNDSCENERY.hud_text_message_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    input_stream.read(2) # Padding?
    SOUNDSCENERY.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    SOUNDSCENERY.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    SOUNDSCENERY.old_functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "old functions"))
    SOUNDSCENERY.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    SOUNDSCENERY.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    input_stream.read(128) # Padding?

def read_sound_scenery_body_retail(SOUNDSCENERY, TAG, input_stream, tag_node, XML_OUTPUT):
    SOUNDSCENERY.body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    input_stream.read(2) # Padding?
    SOUNDSCENERY.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    SOUNDSCENERY.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    SOUNDSCENERY.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    SOUNDSCENERY.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    SOUNDSCENERY.lightmap_shadow_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap shadow mode", LightmapShadowModeEnum))
    SOUNDSCENERY.sweetner_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sweetner size", SweetenerSizeEnum))
    input_stream.read(4) # Padding?
    SOUNDSCENERY.dynamic_light_sphere_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere radius"))
    SOUNDSCENERY.dynamic_light_sphere_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere offset"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    SOUNDSCENERY.default_model_variant_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    SOUNDSCENERY.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    SOUNDSCENERY.crate_object = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "crate object"))
    SOUNDSCENERY.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    SOUNDSCENERY.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    SOUNDSCENERY.material_effects = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "material effects"))
    SOUNDSCENERY.ai_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai properties"))
    SOUNDSCENERY.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    SOUNDSCENERY.apply_collision_damage_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "apply collision damage scale"))
    SOUNDSCENERY.min_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game acc"))
    SOUNDSCENERY.max_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game acc"))
    SOUNDSCENERY.min_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game scale"))
    SOUNDSCENERY.max_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game scale"))
    SOUNDSCENERY.min_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs acc"))
    SOUNDSCENERY.max_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs acc"))
    SOUNDSCENERY.min_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs scale"))
    SOUNDSCENERY.max_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs scale"))
    SOUNDSCENERY.hud_text_message_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    input_stream.read(2) # Padding?
    SOUNDSCENERY.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    SOUNDSCENERY.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    SOUNDSCENERY.old_functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "old functions"))
    SOUNDSCENERY.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    SOUNDSCENERY.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    input_stream.read(16) # Padding?

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    SOUNDSCENERY = SoundSceneryAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    SOUNDSCENERY.header = TAG.Header().read(input_stream, TAG)
    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    initilize_scenery(SOUNDSCENERY)
    if SOUNDSCENERY.header.engine_tag == "LAMB":
        read_sound_scenery_body_v0(SOUNDSCENERY, TAG, input_stream, tag_node, XML_OUTPUT)
    elif SOUNDSCENERY.header.engine_tag == "MLAB":
        read_sound_scenery_body_v0(SOUNDSCENERY, TAG, input_stream, tag_node, XML_OUTPUT)
    elif SOUNDSCENERY.header.engine_tag == "BLM!":
        read_sound_scenery_body_retail(SOUNDSCENERY, TAG, input_stream, tag_node, XML_OUTPUT)

    if SOUNDSCENERY.default_model_variant_length > 0:
        SOUNDSCENERY.default_model_variant = TAG.read_variable_string_no_terminator(input_stream, SOUNDSCENERY.default_model_variant_length, TAG, tag_format.XMLData(tag_node, "default model variant"))

    if SOUNDSCENERY.model.name_length > 0:
        SOUNDSCENERY.model.name = TAG.read_variable_string(input_stream, SOUNDSCENERY.model.name_length, TAG)

    if SOUNDSCENERY.crate_object.name_length > 0:
        SOUNDSCENERY.crate_object.name = TAG.read_variable_string(input_stream, SOUNDSCENERY.crate_object.name_length, TAG)

    if SOUNDSCENERY.modifier_shader.name_length > 0:
        SOUNDSCENERY.modifier_shader.name = TAG.read_variable_string(input_stream, SOUNDSCENERY.modifier_shader.name_length, TAG)

    if SOUNDSCENERY.creation_effect.name_length > 0:
        SOUNDSCENERY.creation_effect.name = TAG.read_variable_string(input_stream, SOUNDSCENERY.creation_effect.name_length, TAG)

    if SOUNDSCENERY.material_effects.name_length > 0:
        SOUNDSCENERY.material_effects.name = TAG.read_variable_string(input_stream, SOUNDSCENERY.material_effects.name_length, TAG)

    if XML_OUTPUT:
        model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "model")
        crate_object_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "crate object")
        modifier_shader_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "modifier shader")
        creation_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "creation effect")
        material_effects_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "material effects")
        SOUNDSCENERY.model.append_xml_attributes(model_node)
        SOUNDSCENERY.crate_object.append_xml_attributes(crate_object_node)
        SOUNDSCENERY.modifier_shader.append_xml_attributes(modifier_shader_node)
        SOUNDSCENERY.creation_effect.append_xml_attributes(creation_effect_node)
        SOUNDSCENERY.material_effects.append_xml_attributes(material_effects_node)

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
