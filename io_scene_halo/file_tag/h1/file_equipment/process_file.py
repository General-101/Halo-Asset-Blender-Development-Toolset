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
from .format import EquipmentAsset, ObjectFlags, ObjectFunctionEnum, ItemFlags, ItemFunctionEnum, PowerupTypeEnum, GrenadeTypeEnum

XML_OUTPUT = False

def process_file(input_stream, tag_format, report):
    TAG = tag_format.TagAsset()
    EQUIPMENT = EquipmentAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    EQUIPMENT.header = TAG.Header().read(input_stream, TAG)
    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    EQUIPMENT.equipment_body = EQUIPMENT.EquipmentBody()
    input_stream.read(2) # Padding?
    EQUIPMENT.equipment_body.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    EQUIPMENT.equipment_body.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    EQUIPMENT.equipment_body.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    EQUIPMENT.equipment_body.origin_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "origin offset"))
    EQUIPMENT.equipment_body.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    input_stream.read(4) # Padding?
    EQUIPMENT.equipment_body.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    EQUIPMENT.equipment_body.animation_graph = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "animation graph"))
    input_stream.read(40) # Padding?
    EQUIPMENT.equipment_body.collision_model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision model"))
    EQUIPMENT.equipment_body.physics = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "physics"))
    EQUIPMENT.equipment_body.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    EQUIPMENT.equipment_body.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    input_stream.read(84) # Padding?
    EQUIPMENT.equipment_body.render_bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "render bounding radius"))
    EQUIPMENT.equipment_body.object_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", ObjectFunctionEnum))
    EQUIPMENT.equipment_body.object_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", ObjectFunctionEnum))
    EQUIPMENT.equipment_body.object_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", ObjectFunctionEnum))
    EQUIPMENT.equipment_body.object_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", ObjectFunctionEnum))
    input_stream.read(44) # Padding?
    EQUIPMENT.equipment_body.hud_text_message_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    EQUIPMENT.equipment_body.forced_shader_permutation_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "forced shader_permutation index"))
    EQUIPMENT.equipment_body.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    EQUIPMENT.equipment_body.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    EQUIPMENT.equipment_body.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    EQUIPMENT.equipment_body.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    EQUIPMENT.equipment_body.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    input_stream.read(2) # Padding?
    EQUIPMENT.equipment_body.equipment_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ItemFlags))
    EQUIPMENT.equipment_body.message_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "message index"))
    EQUIPMENT.equipment_body.sort_order = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sort order"))
    EQUIPMENT.equipment_body.scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "scale"))
    EQUIPMENT.equipment_body.hud_message_value_scale = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud message value scale"))
    input_stream.read(18) # Padding?
    EQUIPMENT.equipment_body.equipment_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", ItemFunctionEnum))
    EQUIPMENT.equipment_body.equipment_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", ItemFunctionEnum))
    EQUIPMENT.equipment_body.equipment_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", ItemFunctionEnum))
    EQUIPMENT.equipment_body.equipment_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", ItemFunctionEnum))
    input_stream.read(164) # Padding?
    EQUIPMENT.equipment_body.material_effects = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "material effects"))
    EQUIPMENT.equipment_body.collision_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision sound"))
    input_stream.read(120) # Padding?
    EQUIPMENT.equipment_body.detonation_delay = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "detonation delay"))
    EQUIPMENT.equipment_body.detonating_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detonating effect"))
    EQUIPMENT.equipment_body.detonation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detonation effect"))
    EQUIPMENT.equipment_body.powerup_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "powerup type", PowerupTypeEnum))
    EQUIPMENT.equipment_body.grenade_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "grenade type", GrenadeTypeEnum))
    EQUIPMENT.equipment_body.powerup_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "powerup time"))
    EQUIPMENT.equipment_body.pickup_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "pickup sound"))
    input_stream.read(144) # Padding?
    if EQUIPMENT.equipment_body.model.name_length > 0:
        EQUIPMENT.equipment_body.model.name = TAG.read_variable_string(input_stream, EQUIPMENT.equipment_body.model.name_length, TAG)

    if EQUIPMENT.equipment_body.animation_graph.name_length > 0:
        EQUIPMENT.equipment_body.animation_graph.name = TAG.read_variable_string(input_stream, EQUIPMENT.equipment_body.animation_graph.name_length, TAG)

    if EQUIPMENT.equipment_body.collision_model.name_length > 0:
        EQUIPMENT.equipment_body.collision_model.name = TAG.read_variable_string(input_stream, EQUIPMENT.equipment_body.collision_model.name_length, TAG)

    if EQUIPMENT.equipment_body.physics.name_length > 0:
        EQUIPMENT.equipment_body.physics.name = TAG.read_variable_string(input_stream, EQUIPMENT.equipment_body.physics.name_length, TAG)

    if EQUIPMENT.equipment_body.modifier_shader.name_length > 0:
        EQUIPMENT.equipment_body.modifier_shader.name = TAG.read_variable_string(input_stream, EQUIPMENT.equipment_body.modifier_shader.name_length, TAG)

    if EQUIPMENT.equipment_body.creation_effect.name_length > 0:
        EQUIPMENT.equipment_body.creation_effect.name = TAG.read_variable_string(input_stream, EQUIPMENT.equipment_body.creation_effect.name_length, TAG)

    if EQUIPMENT.equipment_body.material_effects.name_length > 0:
        EQUIPMENT.equipment_body.material_effects.name = TAG.read_variable_string(input_stream, EQUIPMENT.equipment_body.material_effects.name_length, TAG)

    if EQUIPMENT.equipment_body.collision_sound.name_length > 0:
        EQUIPMENT.equipment_body.collision_sound.name = TAG.read_variable_string(input_stream, EQUIPMENT.equipment_body.collision_sound.name_length, TAG)

    if EQUIPMENT.equipment_body.detonating_effect.name_length > 0:
        EQUIPMENT.equipment_body.detonating_effect.name = TAG.read_variable_string(input_stream, EQUIPMENT.equipment_body.detonating_effect.name_length, TAG)

    if EQUIPMENT.equipment_body.detonation_effect.name_length > 0:
        EQUIPMENT.equipment_body.detonation_effect.name = TAG.read_variable_string(input_stream, EQUIPMENT.equipment_body.detonation_effect.name_length, TAG)

    if EQUIPMENT.equipment_body.pickup_sound.name_length > 0:
        EQUIPMENT.equipment_body.pickup_sound.name = TAG.read_variable_string(input_stream, EQUIPMENT.equipment_body.pickup_sound.name_length, TAG)

    if XML_OUTPUT:
        model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "model")
        animation_graph_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "animation graph")
        collision_model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "collision model")
        physics_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "physics")
        modifier_shader_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "modifier shader")
        creation_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "creation effect")
        material_effects_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "material effects")
        collision_sound_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "collision sound")
        detonating_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "detonating effect")
        detonation_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "detonation effect")
        pickup_sound_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "pickup sound")
        EQUIPMENT.equipment_body.model.append_xml_attributes(model_node)
        EQUIPMENT.equipment_body.animation_graph.append_xml_attributes(animation_graph_node)
        EQUIPMENT.equipment_body.collision_model.append_xml_attributes(collision_model_node)
        EQUIPMENT.equipment_body.physics.append_xml_attributes(physics_node)
        EQUIPMENT.equipment_body.modifier_shader.append_xml_attributes(modifier_shader_node)
        EQUIPMENT.equipment_body.creation_effect.append_xml_attributes(creation_effect_node)
        EQUIPMENT.equipment_body.material_effects.append_xml_attributes(material_effects_node)
        EQUIPMENT.equipment_body.collision_sound.append_xml_attributes(collision_sound_node)
        EQUIPMENT.equipment_body.detonating_effect.append_xml_attributes(detonating_effect_node)
        EQUIPMENT.equipment_body.detonation_effect.append_xml_attributes(detonation_effect_node)
        EQUIPMENT.equipment_body.pickup_sound.append_xml_attributes(pickup_sound_node)

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
