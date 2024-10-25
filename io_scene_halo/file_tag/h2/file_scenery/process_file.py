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
from .format import SceneryAsset, PathfindingPolicyEnum, SceneryFlags, LightmappingPolicyEnum
from ....file_tag.h2.file_object.process_file import (read_ai_properties_retail, 
                                                      read_functions_retail, 
                                                      read_attachments_retail,
                                                      read_widgets_retail,
                                                      read_old_functions_retail)

XML_OUTPUT = False

def initilize_scenery(SCENERY):
    SCENERY.ai_properties = []
    SCENERY.functions = []
    SCENERY.attachments = []
    SCENERY.widgets = []
    SCENERY.old_functions = []
    SCENERY.change_colors = []
    SCENERY.predicted_resources = []

def read_scenery_body_v0(SCENERY, TAG, input_stream, tag_node, XML_OUTPUT):
    SCENERY.body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    input_stream.read(2) # Padding?
    SCENERY.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    SCENERY.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    SCENERY.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    input_stream.read(12) # Padding?
    SCENERY.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    SCENERY.lightmap_shadow_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap shadow mode", LightmapShadowModeEnum))
    SCENERY.sweetner_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sweetner size", SweetenerSizeEnum))
    input_stream.read(36) # Padding?
    SCENERY.dynamic_light_sphere_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere radius"))
    SCENERY.dynamic_light_sphere_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere offset"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    SCENERY.default_model_variant_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    SCENERY.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    SCENERY.crate_object = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "crate object"))
    input_stream.read(16) # Padding?
    SCENERY.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    SCENERY.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    SCENERY.material_effects = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "material effects"))
    input_stream.read(24) # Padding?
    SCENERY.ai_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai properties"))
    input_stream.read(24) # Padding?
    SCENERY.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    input_stream.read(16) # Padding?
    SCENERY.apply_collision_damage_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "apply collision damage scale"))
    SCENERY.min_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game acc"))
    SCENERY.max_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game acc"))
    SCENERY.min_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game scale"))
    SCENERY.max_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game scale"))
    SCENERY.min_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs acc"))
    SCENERY.max_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs acc"))
    SCENERY.min_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs scale"))
    SCENERY.max_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs scale"))
    SCENERY.hud_text_message_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    input_stream.read(2) # Padding?
    SCENERY.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    SCENERY.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    SCENERY.old_functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "old functions"))
    SCENERY.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    SCENERY.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    SCENERY.pathfinding_policy = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "pathfinding policy", PathfindingPolicyEnum))
    SCENERY.scenery_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", SceneryFlags))
    SCENERY.lightmapping_policy = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmapping policy", LightmappingPolicyEnum))
    input_stream.read(122) # Padding?

def read_scenery_body_retail(SCENERY, TAG, input_stream, tag_node, XML_OUTPUT):
    SCENERY.body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    input_stream.read(2) # Padding?
    SCENERY.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    SCENERY.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    SCENERY.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    SCENERY.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    SCENERY.lightmap_shadow_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap shadow mode", LightmapShadowModeEnum))
    SCENERY.sweetner_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sweetner size", SweetenerSizeEnum))
    input_stream.read(4) # Padding?
    SCENERY.dynamic_light_sphere_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere radius"))
    SCENERY.dynamic_light_sphere_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere offset"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    SCENERY.default_model_variant_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    SCENERY.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    SCENERY.crate_object = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "crate object"))
    SCENERY.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    SCENERY.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    SCENERY.material_effects = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "material effects"))
    SCENERY.ai_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai properties"))
    SCENERY.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    SCENERY.apply_collision_damage_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "apply collision damage scale"))
    SCENERY.min_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game acc"))
    SCENERY.max_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game acc"))
    SCENERY.min_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game scale"))
    SCENERY.max_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game scale"))
    SCENERY.min_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs acc"))
    SCENERY.max_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs acc"))
    SCENERY.min_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs scale"))
    SCENERY.max_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs scale"))
    SCENERY.hud_text_message_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    input_stream.read(2) # Padding?
    SCENERY.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    SCENERY.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    SCENERY.old_functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "old functions"))
    SCENERY.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    SCENERY.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    SCENERY.pathfinding_policy = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "pathfinding policy", PathfindingPolicyEnum))
    SCENERY.scenery_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", SceneryFlags))
    SCENERY.lightmapping_policy = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmapping policy", LightmappingPolicyEnum))
    input_stream.read(2) # Padding?

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    SCENERY = SceneryAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    SCENERY.header = TAG.Header().read(input_stream, TAG)
    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    initilize_scenery(SCENERY)
    if SCENERY.header.engine_tag == "LAMB":
        read_scenery_body_v0(SCENERY, TAG, input_stream, tag_node, XML_OUTPUT)
    elif SCENERY.header.engine_tag == "MLAB":
        read_scenery_body_v0(SCENERY, TAG, input_stream, tag_node, XML_OUTPUT)
    elif SCENERY.header.engine_tag == "BLM!":
        read_scenery_body_retail(SCENERY, TAG, input_stream, tag_node, XML_OUTPUT)

    if SCENERY.default_model_variant_length > 0:
        SCENERY.default_model_variant = TAG.read_variable_string_no_terminator(input_stream, SCENERY.default_model_variant_length, TAG, tag_format.XMLData(tag_node, "default model variant"))

    if SCENERY.model.name_length > 0:
        SCENERY.model.name = TAG.read_variable_string(input_stream, SCENERY.model.name_length, TAG)

    if SCENERY.crate_object.name_length > 0:
        SCENERY.crate_object.name = TAG.read_variable_string(input_stream, SCENERY.crate_object.name_length, TAG)

    if SCENERY.modifier_shader.name_length > 0:
        SCENERY.modifier_shader.name = TAG.read_variable_string(input_stream, SCENERY.modifier_shader.name_length, TAG)

    if SCENERY.creation_effect.name_length > 0:
        SCENERY.creation_effect.name = TAG.read_variable_string(input_stream, SCENERY.creation_effect.name_length, TAG)

    if SCENERY.material_effects.name_length > 0:
        SCENERY.material_effects.name = TAG.read_variable_string(input_stream, SCENERY.material_effects.name_length, TAG)

    read_ai_properties_retail(SCENERY, TAG, input_stream, tag_node, XML_OUTPUT)
    read_functions_retail(SCENERY, TAG, input_stream, tag_node, XML_OUTPUT)
    read_attachments_retail(SCENERY, TAG, input_stream, tag_node, XML_OUTPUT)
    read_widgets_retail(SCENERY, TAG, input_stream, tag_node, XML_OUTPUT)
    read_old_functions_retail(SCENERY, TAG, input_stream, tag_node, XML_OUTPUT)

    if XML_OUTPUT:
        model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "model")
        crate_object_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "crate object")
        modifier_shader_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "modifier shader")
        creation_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "creation effect")
        material_effects_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "material effects")
        SCENERY.model.append_xml_attributes(model_node)
        SCENERY.crate_object.append_xml_attributes(crate_object_node)
        SCENERY.modifier_shader.append_xml_attributes(modifier_shader_node)
        SCENERY.creation_effect.append_xml_attributes(creation_effect_node)
        SCENERY.material_effects.append_xml_attributes(material_effects_node)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, SCENERY.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return SCENERY
