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
from ..file_item.format import ItemFlags
from .format import EquipmentAsset, PowerupTypeEnum, GrenadeTypeEnum

XML_OUTPUT = False

def initilize_equipment(EQUIPMENT):
    EQUIPMENT.ai_properties = []
    EQUIPMENT.functions = []
    EQUIPMENT.attachments = []
    EQUIPMENT.widgets = []
    EQUIPMENT.old_functions = []
    EQUIPMENT.change_colors = []
    EQUIPMENT.predicted_resources = []
    EQUIPMENT.predicted_bitmaps = []

def read_equipment_body_v0(EQUIPMENT, TAG, input_stream, tag_node, XML_OUTPUT):
    EQUIPMENT.body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    input_stream.read(2) # Padding?
    EQUIPMENT.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    EQUIPMENT.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    EQUIPMENT.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    input_stream.read(12) # Padding?
    EQUIPMENT.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    EQUIPMENT.lightmap_shadow_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap shadow mode", LightmapShadowModeEnum))
    EQUIPMENT.sweetner_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sweetner size", SweetenerSizeEnum))
    input_stream.read(36) # Padding?
    EQUIPMENT.dynamic_light_sphere_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere radius"))
    EQUIPMENT.dynamic_light_sphere_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere offset"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    EQUIPMENT.default_model_variant_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    EQUIPMENT.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    EQUIPMENT.crate_object = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "crate object"))
    input_stream.read(16) # Padding?
    EQUIPMENT.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    EQUIPMENT.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    EQUIPMENT.material_effects = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "material effects"))
    input_stream.read(24) # Padding?
    EQUIPMENT.ai_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai properties"))
    input_stream.read(24) # Padding?
    EQUIPMENT.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    input_stream.read(16) # Padding?
    EQUIPMENT.apply_collision_damage_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "apply collision damage scale"))
    EQUIPMENT.min_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game acc"))
    EQUIPMENT.max_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game acc"))
    EQUIPMENT.min_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game scale"))
    EQUIPMENT.max_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game scale"))
    EQUIPMENT.min_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs acc"))
    EQUIPMENT.max_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs acc"))
    EQUIPMENT.min_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs scale"))
    EQUIPMENT.max_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs scale"))
    EQUIPMENT.hud_text_message_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    input_stream.read(2) # Padding?
    EQUIPMENT.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    EQUIPMENT.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    EQUIPMENT.old_functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "old functions"))
    EQUIPMENT.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    EQUIPMENT.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    EQUIPMENT.equipment_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ItemFlags))
    input_stream.read(2) # Padding?
    EQUIPMENT.old_message_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "old message index"))
    EQUIPMENT.sort_order = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "sort order"))
    EQUIPMENT.multiplayer_on_ground_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "multiplayer on ground scale"))
    EQUIPMENT.campaign_on_ground_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "campaign on ground scale"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    EQUIPMENT.pickup_msg_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    EQUIPMENT.swap_msg_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    EQUIPMENT.pickup_or_dual_msg_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    EQUIPMENT.swap_or_dual_msg_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    EQUIPMENT.dual_only_msg_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    EQUIPMENT.picked_up_msg_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    EQUIPMENT.singluar_quantity_msg_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    EQUIPMENT.plural_quantity_msg_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    EQUIPMENT.switch_to_msg_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    EQUIPMENT.switch_to_from_ai_msg_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    input_stream.read(148) # Padding?
    EQUIPMENT.unused = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "unused"))
    EQUIPMENT.collision_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision sound"))
    EQUIPMENT.predicted_bitmaps_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted bitmaps"))
    input_stream.read(92) # Padding?
    EQUIPMENT.detonation_damage_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detonation damage effect"))
    EQUIPMENT.detonation_delay = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "detonation delay"))
    EQUIPMENT.detonating_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detonating effect"))
    EQUIPMENT.detonation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detonation effect"))
    EQUIPMENT.powerup_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "powerup type", PowerupTypeEnum))
    EQUIPMENT.grenade_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "grenade type", GrenadeTypeEnum))
    EQUIPMENT.powerup_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "powerup time"))
    EQUIPMENT.pickup_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "pickup sound"))
    input_stream.read(144) # Padding?

def read_equipment_body_retail(EQUIPMENT, TAG, input_stream, tag_node, XML_OUTPUT):
    EQUIPMENT.body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    input_stream.read(2) # Padding?
    EQUIPMENT.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    EQUIPMENT.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    EQUIPMENT.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    EQUIPMENT.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    EQUIPMENT.lightmap_shadow_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "lightmap shadow mode", LightmapShadowModeEnum))
    EQUIPMENT.sweetner_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sweetner size", SweetenerSizeEnum))
    input_stream.read(4) # Padding?
    EQUIPMENT.dynamic_light_sphere_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere radius"))
    EQUIPMENT.dynamic_light_sphere_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "dynamic light sphere offset"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    EQUIPMENT.default_model_variant_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    EQUIPMENT.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    EQUIPMENT.crate_object = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "crate object"))
    EQUIPMENT.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    EQUIPMENT.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    EQUIPMENT.material_effects = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "material effects"))
    EQUIPMENT.ai_properties_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "ai properties"))
    EQUIPMENT.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    EQUIPMENT.apply_collision_damage_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "apply collision damage scale"))
    EQUIPMENT.min_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game acc"))
    EQUIPMENT.max_game_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game acc"))
    EQUIPMENT.min_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min game scale"))
    EQUIPMENT.max_game_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max game scale"))
    EQUIPMENT.min_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs acc"))
    EQUIPMENT.max_abs_acc = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs acc"))
    EQUIPMENT.min_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "min abs scale"))
    EQUIPMENT.max_abs_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "max abs scale"))
    EQUIPMENT.hud_text_message_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    input_stream.read(2) # Padding?
    EQUIPMENT.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    EQUIPMENT.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    EQUIPMENT.old_functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "old functions"))
    EQUIPMENT.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    EQUIPMENT.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    EQUIPMENT.equipment_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ItemFlags))
    input_stream.read(2) # Padding?
    EQUIPMENT.old_message_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "old message index"))
    EQUIPMENT.sort_order = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "sort order"))
    EQUIPMENT.multiplayer_on_ground_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "multiplayer on ground scale"))
    EQUIPMENT.campaign_on_ground_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "campaign on ground scale"))

    TAG.big_endian = True
    input_stream.read(2) # Padding?
    EQUIPMENT.pickup_msg_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    EQUIPMENT.swap_msg_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    EQUIPMENT.pickup_or_dual_msg_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    EQUIPMENT.swap_or_dual_msg_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    EQUIPMENT.dual_only_msg_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    EQUIPMENT.picked_up_msg_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    EQUIPMENT.singluar_quantity_msg_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    EQUIPMENT.plural_quantity_msg_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    EQUIPMENT.switch_to_msg_length = TAG.read_signed_short(input_stream, TAG)
    input_stream.read(2) # Padding?
    EQUIPMENT.switch_to_from_ai_msg_length = TAG.read_signed_short(input_stream, TAG)
    TAG.big_endian = False

    EQUIPMENT.unused = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "unused"))
    EQUIPMENT.collision_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision sound"))
    EQUIPMENT.predicted_bitmaps_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted bitmaps"))
    EQUIPMENT.detonation_damage_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detonation damage effect"))
    EQUIPMENT.detonation_delay = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "detonation delay"))
    EQUIPMENT.detonating_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detonating effect"))
    EQUIPMENT.detonation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detonation effect"))
    EQUIPMENT.powerup_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "powerup type", PowerupTypeEnum))
    EQUIPMENT.grenade_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "grenade type", GrenadeTypeEnum))
    EQUIPMENT.powerup_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "powerup time"))
    EQUIPMENT.pickup_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "pickup sound"))

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    EQUIPMENT = EquipmentAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    EQUIPMENT.header = TAG.Header().read(input_stream, TAG)
    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    initilize_equipment(EQUIPMENT)

    if EQUIPMENT.header.engine_tag == "LAMB":
        read_equipment_body_v0(EQUIPMENT, TAG, input_stream, tag_node, XML_OUTPUT)
    elif EQUIPMENT.header.engine_tag == "MLAB":
        read_equipment_body_v0(EQUIPMENT, TAG, input_stream, tag_node, XML_OUTPUT)
    elif EQUIPMENT.header.engine_tag == "BLM!":
        read_equipment_body_retail(EQUIPMENT, TAG, input_stream, tag_node, XML_OUTPUT)

    if EQUIPMENT.default_model_variant_length > 0:
        EQUIPMENT.default_model_variant = TAG.read_variable_string_no_terminator(input_stream, EQUIPMENT.default_model_variant_length, TAG, tag_format.XMLData(tag_node, "default model variant"))

    if EQUIPMENT.model.name_length > 0:
        EQUIPMENT.model.name = TAG.read_variable_string(input_stream, EQUIPMENT.model.name_length, TAG)

    if EQUIPMENT.crate_object.name_length > 0:
        EQUIPMENT.crate_object.name = TAG.read_variable_string(input_stream, EQUIPMENT.crate_object.name_length, TAG)

    if EQUIPMENT.modifier_shader.name_length > 0:
        EQUIPMENT.modifier_shader.name = TAG.read_variable_string(input_stream, EQUIPMENT.modifier_shader.name_length, TAG)

    if EQUIPMENT.creation_effect.name_length > 0:
        EQUIPMENT.creation_effect.name = TAG.read_variable_string(input_stream, EQUIPMENT.creation_effect.name_length, TAG)

    if EQUIPMENT.material_effects.name_length > 0:
        EQUIPMENT.material_effects.name = TAG.read_variable_string(input_stream, EQUIPMENT.material_effects.name_length, TAG)

    if XML_OUTPUT:
        model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "model")
        crate_object_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "crate object")
        modifier_shader_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "modifier shader")
        creation_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "creation effect")
        material_effects_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "material effects")
        EQUIPMENT.model.append_xml_attributes(model_node)
        EQUIPMENT.crate_object.append_xml_attributes(crate_object_node)
        EQUIPMENT.modifier_shader.append_xml_attributes(modifier_shader_node)
        EQUIPMENT.creation_effect.append_xml_attributes(creation_effect_node)
        EQUIPMENT.material_effects.append_xml_attributes(material_effects_node)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, EQUIPMENT.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return EQUIPMENT
