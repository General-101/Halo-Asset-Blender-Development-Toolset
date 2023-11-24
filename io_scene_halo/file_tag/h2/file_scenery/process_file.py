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
from .format import (
        SceneryAsset, 
        ObjectFlags, 
        LightmapShadowModeEnum, 
        SweetenerSizeEnum,
        PathfindingPolicyEnum,
        SceneryFlags,
        LightmappingPolicyEnum,
        )

XML_OUTPUT = False

def initilize_scenery(SCENERY):
    SCENERY.ai_properties = []
    SCENERY.functions = []
    SCENERY.attachments = []
    SCENERY.widgets = []
    SCENERY.old_functions = []
    SCENERY.change_colors = []
    SCENERY.predicted_resources = []

def read_scenery_body_v0(SCENERY, TAG, input_stream, tag_format, tag_node, XML_OUTPUT):
    SCENERY.scenery_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    SCENERY.scenery_body = SCENERY.SceneryBody()
    input_stream.read(2) # Padding?
    SCENERY.scenery_body.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    SCENERY.scenery_body.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    SCENERY.scenery_body.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    input_stream.read(12) # Padding?
    SCENERY.scenery_body.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    SCENERY.scenery_body.lightmap_shadow_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap shadow mode", LightmapShadowModeEnum))
    SCENERY.scenery_body.sweetner_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sweetner size", SweetenerSizeEnum))
    input_stream.read(36) # Padding?
    SCENERY.scenery_body.dynamic_light_sphere_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere radius"))
    SCENERY.scenery_body.dynamic_light_sphere_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere offset"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    SCENERY.scenery_body.default_model_variant_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    SCENERY.scenery_body.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    SCENERY.scenery_body.crate_object = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "crate object"))
    input_stream.read(16) # Padding?
    SCENERY.scenery_body.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    SCENERY.scenery_body.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    SCENERY.scenery_body.material_effects = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "material effects"))
    input_stream.read(24) # Padding?
    SCENERY.scenery_body.ai_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai properties"))
    input_stream.read(24) # Padding?
    SCENERY.scenery_body.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    input_stream.read(16) # Padding?
    SCENERY.scenery_body.apply_collision_damage_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "apply collision damage scale"))
    SCENERY.scenery_body.min_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game acc"))
    SCENERY.scenery_body.max_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game acc"))
    SCENERY.scenery_body.min_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game scale"))
    SCENERY.scenery_body.max_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game scale"))
    SCENERY.scenery_body.min_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs acc"))
    SCENERY.scenery_body.max_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs acc"))
    SCENERY.scenery_body.min_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs scale"))
    SCENERY.scenery_body.max_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs scale"))
    SCENERY.scenery_body.hud_text_message_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    input_stream.read(2) # Padding?
    SCENERY.scenery_body.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    SCENERY.scenery_body.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    SCENERY.scenery_body.old_functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "old functions"))
    SCENERY.scenery_body.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    SCENERY.scenery_body.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    SCENERY.scenery_body.pathfinding_policy = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "pathfinding policy", PathfindingPolicyEnum))
    SCENERY.scenery_body.scenery_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", SceneryFlags))
    SCENERY.scenery_body.lightmapping_policy = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmapping policy", LightmappingPolicyEnum))
    input_stream.read(122) # Padding?

def read_scenery_body_retail(SCENERY, TAG, input_stream, tag_format, tag_node, XML_OUTPUT):
    SCENERY.scenery_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    SCENERY.scenery_body = SCENERY.SceneryBody()
    input_stream.read(2) # Padding?
    SCENERY.scenery_body.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    SCENERY.scenery_body.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    SCENERY.scenery_body.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    SCENERY.scenery_body.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    SCENERY.scenery_body.lightmap_shadow_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap shadow mode", LightmapShadowModeEnum))
    SCENERY.scenery_body.sweetner_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sweetner size", SweetenerSizeEnum))
    input_stream.read(4) # Padding?
    SCENERY.scenery_body.dynamic_light_sphere_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere radius"))
    SCENERY.scenery_body.dynamic_light_sphere_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere offset"))

    TAG.big_endian = True
    SCENERY.scenery_body.default_model_variant_length = TAG.read_signed_integer(input_stream, TAG)
    TAG.big_endian = False

    SCENERY.scenery_body.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    SCENERY.scenery_body.crate_object = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "crate object"))
    SCENERY.scenery_body.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    SCENERY.scenery_body.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    SCENERY.scenery_body.material_effects = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "material effects"))
    SCENERY.scenery_body.ai_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai properties"))
    SCENERY.scenery_body.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    SCENERY.scenery_body.apply_collision_damage_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "apply collision damage scale"))
    SCENERY.scenery_body.min_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game acc"))
    SCENERY.scenery_body.max_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game acc"))
    SCENERY.scenery_body.min_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game scale"))
    SCENERY.scenery_body.max_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game scale"))
    SCENERY.scenery_body.min_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs acc"))
    SCENERY.scenery_body.max_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs acc"))
    SCENERY.scenery_body.min_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs scale"))
    SCENERY.scenery_body.max_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs scale"))
    SCENERY.scenery_body.hud_text_message_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    input_stream.read(2) # Padding?
    SCENERY.scenery_body.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    SCENERY.scenery_body.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    SCENERY.scenery_body.old_functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "old functions"))
    SCENERY.scenery_body.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    SCENERY.scenery_body.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    SCENERY.scenery_body.pathfinding_policy = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "pathfinding policy", PathfindingPolicyEnum))
    SCENERY.scenery_body.scenery_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", SceneryFlags))
    SCENERY.scenery_body.lightmapping_policy = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmapping policy", LightmappingPolicyEnum))
    input_stream.read(2) # Padding?

def process_file(input_stream, tag_format, report):
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
    if SCENERY.header.engine_tag == "BMAL":
        read_scenery_body_v0(SCENERY, TAG, input_stream, tag_format, tag_node, XML_OUTPUT)
    elif SCENERY.header.engine_tag == "BALM":
        read_scenery_body_v0(SCENERY, TAG, input_stream, tag_format, tag_node, XML_OUTPUT)
    elif SCENERY.header.engine_tag == "!MLB":
        read_scenery_body_retail(SCENERY, TAG, input_stream, tag_format, tag_node, XML_OUTPUT)

    if SCENERY.scenery_body.default_model_variant_length > 0:
        SCENERY.scenery_body.default_model_variant = TAG.read_variable_string_no_terminator(input_stream, SCENERY.scenery_body.default_model_variant_length, TAG, tag_format.XMLData(tag_node, "default model variant"))

    if SCENERY.scenery_body.model.name_length > 0:
        SCENERY.scenery_body.model.name = TAG.read_variable_string(input_stream, SCENERY.scenery_body.model.name_length, TAG)

    if SCENERY.scenery_body.crate_object.name_length > 0:
        SCENERY.scenery_body.crate_object.name = TAG.read_variable_string(input_stream, SCENERY.scenery_body.crate_object.name_length, TAG)

    if SCENERY.scenery_body.modifier_shader.name_length > 0:
        SCENERY.scenery_body.modifier_shader.name = TAG.read_variable_string(input_stream, SCENERY.scenery_body.modifier_shader.name_length, TAG)

    if SCENERY.scenery_body.creation_effect.name_length > 0:
        SCENERY.scenery_body.creation_effect.name = TAG.read_variable_string(input_stream, SCENERY.scenery_body.creation_effect.name_length, TAG)

    if SCENERY.scenery_body.material_effects.name_length > 0:
        SCENERY.scenery_body.material_effects.name = TAG.read_variable_string(input_stream, SCENERY.scenery_body.material_effects.name_length, TAG)

    if XML_OUTPUT:
        model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "model")
        crate_object_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "crate object")
        modifier_shader_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "modifier shader")
        creation_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "creation effect")
        material_effects_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "material effects")
        SCENERY.scenery_body.model.append_xml_attributes(model_node)
        SCENERY.scenery_body.crate_object.append_xml_attributes(crate_object_node)
        SCENERY.scenery_body.modifier_shader.append_xml_attributes(modifier_shader_node)
        SCENERY.scenery_body.creation_effect.append_xml_attributes(creation_effect_node)
        SCENERY.scenery_body.material_effects.append_xml_attributes(material_effects_node)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, SCENERY.header.tag_group, TAG.is_legacy, True)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return SCENERY
