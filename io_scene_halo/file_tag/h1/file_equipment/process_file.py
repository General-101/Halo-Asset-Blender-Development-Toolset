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
from .format import EquipmentAsset, ObjectFlags, ObjectFunctionEnum, ItemFlags, ItemFunctionEnum, PowerupTypeEnum, GrenadeTypeEnum

XML_OUTPUT = False

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    EQUIPMENT = EquipmentAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    EQUIPMENT.header = TAG.Header().read(input_stream, TAG)
    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    input_stream.read(2) # Padding?
    EQUIPMENT.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    EQUIPMENT.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    EQUIPMENT.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    EQUIPMENT.origin_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "origin offset"))
    EQUIPMENT.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    input_stream.read(4) # Padding?
    EQUIPMENT.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    EQUIPMENT.animation_graph = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "animation graph"))
    input_stream.read(40) # Padding?
    EQUIPMENT.collision_model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision model"))
    EQUIPMENT.physics = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "physics"))
    EQUIPMENT.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    EQUIPMENT.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    input_stream.read(84) # Padding?
    EQUIPMENT.render_bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "render bounding radius"))
    EQUIPMENT.object_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", ObjectFunctionEnum))
    EQUIPMENT.object_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", ObjectFunctionEnum))
    EQUIPMENT.object_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", ObjectFunctionEnum))
    EQUIPMENT.object_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", ObjectFunctionEnum))
    input_stream.read(44) # Padding?
    EQUIPMENT.hud_text_message_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    EQUIPMENT.forced_shader_permutation_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "forced shader_permutation index"))
    EQUIPMENT.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    EQUIPMENT.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    EQUIPMENT.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    EQUIPMENT.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    EQUIPMENT.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    input_stream.read(2) # Padding?
    EQUIPMENT.equipment_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ItemFlags))
    EQUIPMENT.message_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "message index"))
    EQUIPMENT.sort_order = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sort order"))
    EQUIPMENT.scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "scale"))
    EQUIPMENT.hud_message_value_scale = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud message value scale"))
    input_stream.read(18) # Padding?
    EQUIPMENT.equipment_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", ItemFunctionEnum))
    EQUIPMENT.equipment_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", ItemFunctionEnum))
    EQUIPMENT.equipment_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", ItemFunctionEnum))
    EQUIPMENT.equipment_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", ItemFunctionEnum))
    input_stream.read(164) # Padding?
    EQUIPMENT.material_effects = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "material effects"))
    EQUIPMENT.collision_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision sound"))
    input_stream.read(120) # Padding?
    EQUIPMENT.detonation_delay = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "detonation delay"))
    EQUIPMENT.detonating_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detonating effect"))
    EQUIPMENT.detonation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detonation effect"))
    EQUIPMENT.powerup_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "powerup type", PowerupTypeEnum))
    EQUIPMENT.grenade_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "grenade type", GrenadeTypeEnum))
    EQUIPMENT.powerup_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "powerup time"))
    EQUIPMENT.pickup_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "pickup sound"))
    input_stream.read(144) # Padding?
    if EQUIPMENT.model.name_length > 0:
        EQUIPMENT.model.name = TAG.read_variable_string(input_stream, EQUIPMENT.model.name_length, TAG)

    if EQUIPMENT.animation_graph.name_length > 0:
        EQUIPMENT.animation_graph.name = TAG.read_variable_string(input_stream, EQUIPMENT.animation_graph.name_length, TAG)

    if EQUIPMENT.collision_model.name_length > 0:
        EQUIPMENT.collision_model.name = TAG.read_variable_string(input_stream, EQUIPMENT.collision_model.name_length, TAG)

    if EQUIPMENT.physics.name_length > 0:
        EQUIPMENT.physics.name = TAG.read_variable_string(input_stream, EQUIPMENT.physics.name_length, TAG)

    if EQUIPMENT.modifier_shader.name_length > 0:
        EQUIPMENT.modifier_shader.name = TAG.read_variable_string(input_stream, EQUIPMENT.modifier_shader.name_length, TAG)

    if EQUIPMENT.creation_effect.name_length > 0:
        EQUIPMENT.creation_effect.name = TAG.read_variable_string(input_stream, EQUIPMENT.creation_effect.name_length, TAG)

    if EQUIPMENT.material_effects.name_length > 0:
        EQUIPMENT.material_effects.name = TAG.read_variable_string(input_stream, EQUIPMENT.material_effects.name_length, TAG)

    if EQUIPMENT.collision_sound.name_length > 0:
        EQUIPMENT.collision_sound.name = TAG.read_variable_string(input_stream, EQUIPMENT.collision_sound.name_length, TAG)

    if EQUIPMENT.detonating_effect.name_length > 0:
        EQUIPMENT.detonating_effect.name = TAG.read_variable_string(input_stream, EQUIPMENT.detonating_effect.name_length, TAG)

    if EQUIPMENT.detonation_effect.name_length > 0:
        EQUIPMENT.detonation_effect.name = TAG.read_variable_string(input_stream, EQUIPMENT.detonation_effect.name_length, TAG)

    if EQUIPMENT.pickup_sound.name_length > 0:
        EQUIPMENT.pickup_sound.name = TAG.read_variable_string(input_stream, EQUIPMENT.pickup_sound.name_length, TAG)

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
        EQUIPMENT.model.append_xml_attributes(model_node)
        EQUIPMENT.animation_graph.append_xml_attributes(animation_graph_node)
        EQUIPMENT.collision_model.append_xml_attributes(collision_model_node)
        EQUIPMENT.physics.append_xml_attributes(physics_node)
        EQUIPMENT.modifier_shader.append_xml_attributes(modifier_shader_node)
        EQUIPMENT.creation_effect.append_xml_attributes(creation_effect_node)
        EQUIPMENT.material_effects.append_xml_attributes(material_effects_node)
        EQUIPMENT.collision_sound.append_xml_attributes(collision_sound_node)
        EQUIPMENT.detonating_effect.append_xml_attributes(detonating_effect_node)
        EQUIPMENT.detonation_effect.append_xml_attributes(detonation_effect_node)
        EQUIPMENT.pickup_sound.append_xml_attributes(pickup_sound_node)

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
