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
from .format_retail import (WeaponAsset, 
                            ObjectFlags, 
                            ObjectFunctionEnum, 
                            ItemFlags, 
                            ItemFunctionEnum, 
                            WeaponFlags, 
                            SecondaryTriggerModeEnum, 
                            WeaponFunctionEnum, 
                            MovementPenalizedEnum, 
                            WeaponTypeEnum)

XML_OUTPUT = False

def process_file_retail(input_stream, tag_format, report):
    TAG = tag_format.TagAsset()
    WEAPON = WeaponAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    WEAPON.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    WEAPON.weapon_body = WEAPON.WeaponBody()
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    WEAPON.weapon_body.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    WEAPON.weapon_body.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    WEAPON.weapon_body.origin_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "origin offset"))
    WEAPON.weapon_body.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    input_stream.read(4) # Padding?
    WEAPON.weapon_body.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    WEAPON.weapon_body.animation_graph = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "animation graph"))
    input_stream.read(40) # Padding?
    WEAPON.weapon_body.collision_model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision model"))
    WEAPON.weapon_body.physics = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "physics"))
    WEAPON.weapon_body.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    WEAPON.weapon_body.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    input_stream.read(84) # Padding?
    WEAPON.weapon_body.render_bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "render bounding radius"))
    WEAPON.weapon_body.object_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", ObjectFunctionEnum))
    WEAPON.weapon_body.object_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", ObjectFunctionEnum))
    WEAPON.weapon_body.object_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", ObjectFunctionEnum))
    WEAPON.weapon_body.object_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", ObjectFunctionEnum))
    input_stream.read(44) # Padding?
    WEAPON.weapon_body.hud_text_message_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    WEAPON.weapon_body.forced_shader_permutation_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "forced shader_permutation index"))
    WEAPON.weapon_body.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    WEAPON.weapon_body.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    WEAPON.weapon_body.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    WEAPON.weapon_body.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    WEAPON.weapon_body.object_predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.item_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ItemFlags))
    WEAPON.weapon_body.message_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "message index"))
    WEAPON.weapon_body.sort_order = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sort order"))
    WEAPON.weapon_body.scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "scale"))
    WEAPON.weapon_body.hud_message_value_scale = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud message value scale"))
    input_stream.read(18) # Padding?
    WEAPON.weapon_body.item_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", ItemFunctionEnum))
    WEAPON.weapon_body.item_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", ItemFunctionEnum))
    WEAPON.weapon_body.item_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", ItemFunctionEnum))
    WEAPON.weapon_body.item_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", ItemFunctionEnum))
    input_stream.read(164) # Padding?
    WEAPON.weapon_body.material_effects = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "material effects"))
    WEAPON.weapon_body.collision_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision sound"))
    input_stream.read(120) # Padding?
    WEAPON.weapon_body.detonation_delay = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "detonation delay"))
    WEAPON.weapon_body.detonating_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detonating effect"))
    WEAPON.weapon_body.detonation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detonation effect"))
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.weapon_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", WeaponFlags))
    WEAPON.weapon_body.label = TAG.read_string32(input_stream, TAG, tag_format.XMLData(tag_node, "label"))
    WEAPON.weapon_body.secondary_trigger_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "secondary trigger mode", SecondaryTriggerModeEnum))
    WEAPON.weapon_body.maximum_alternate_shots_loaded = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "maximum alternate shots loaded"))
    WEAPON.weapon_body.weapon_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", WeaponFunctionEnum))
    WEAPON.weapon_body.weapon_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", WeaponFunctionEnum))
    WEAPON.weapon_body.weapon_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", WeaponFunctionEnum))
    WEAPON.weapon_body.weapon_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", WeaponFunctionEnum))
    WEAPON.weapon_body.ready_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ready time"))
    WEAPON.weapon_body.ready_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "ready effect"))
    WEAPON.weapon_body.heat_recovery_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "heat recovery threshold"))
    WEAPON.weapon_body.overheated_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "overheated threshold"))
    WEAPON.weapon_body.heat_detonation_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "heat detonation threshold"))
    WEAPON.weapon_body.heat_detonation_fraction = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "heat detonation fraction"))
    WEAPON.weapon_body.heat_loss_per_second = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "heat loss per second"))
    WEAPON.weapon_body.heat_illumination = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "heat illumination"))
    input_stream.read(16) # Padding?
    WEAPON.weapon_body.overheated = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "overheated"))
    WEAPON.weapon_body.detonation = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detonation"))
    WEAPON.weapon_body.player_melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "player melee damage"))
    WEAPON.weapon_body.player_melee_response = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "player melee response"))
    input_stream.read(8) # Padding?
    WEAPON.weapon_body.actor_firing_parameters = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "actor firing parameters"))
    WEAPON.weapon_body.near_reticle_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "near reticle range"))
    WEAPON.weapon_body.far_reticle_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "far reticle range"))
    WEAPON.weapon_body.intersection_reticle_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "intersection reticle range"))
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.magnification_levels = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "magnification levels"))
    WEAPON.weapon_body.magnification_range = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "magnification range"))
    WEAPON.weapon_body.autoaim_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "autoaim angle"))
    WEAPON.weapon_body.autoaim_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "autoaim range"))
    WEAPON.weapon_body.magnetism_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "magnetism angle"))
    WEAPON.weapon_body.magnetism_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "magnetism range"))
    WEAPON.weapon_body.deviation_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "deviation angle"))
    input_stream.read(4) # Padding?
    WEAPON.weapon_body.movement_penalized = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "movement penalized", MovementPenalizedEnum))
    input_stream.read(2) # Padding?
    WEAPON.weapon_body.forward_movement_penalty = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "forward movement penalty"))
    WEAPON.weapon_body.sideways_movement_penalty = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "sideways movement penalty"))
    input_stream.read(4) # Padding?
    WEAPON.weapon_body.minimum_target_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "minimum target range"))
    WEAPON.weapon_body.looking_time_modifier = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "looking time modifier"))
    input_stream.read(4) # Padding?
    WEAPON.weapon_body.light_power_on_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "light power on time"))
    WEAPON.weapon_body.light_power_off_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "light power off time"))
    WEAPON.weapon_body.light_power_on_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "light power on effect"))
    WEAPON.weapon_body.light_power_off_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "light power off effect"))
    WEAPON.weapon_body.age_heat_recovery_penalty = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "age heat recovery penalty"))
    WEAPON.weapon_body.age_rate_of_fire_penalty = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "age rate of fire penalty"))
    WEAPON.weapon_body.age_misfire_start = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "age misfire start"))
    WEAPON.weapon_body.age_misfire_chance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "age misfire chance"))
    input_stream.read(12) # Padding?
    WEAPON.weapon_body.first_person_model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "first person model"))
    WEAPON.weapon_body.first_person_animations = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "first person animations"))
    input_stream.read(4) # Padding?
    WEAPON.weapon_body.hud_interface = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "hud interface"))
    WEAPON.weapon_body.pickup_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "pickup sound"))
    WEAPON.weapon_body.zoom_in_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "zoom in sound"))
    WEAPON.weapon_body.zoom_out_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "zoom out sound"))
    input_stream.read(12) # Padding?
    WEAPON.weapon_body.active_camo_ding = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "active camo ding"))
    WEAPON.weapon_body.active_camo_regrowth_rate = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "active camo regrowth rate"))
    input_stream.read(14) # Padding?
    WEAPON.weapon_body.weapon_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "weapon type", WeaponTypeEnum))
    WEAPON.weapon_body.weapon_predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    WEAPON.weapon_body.magazines_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "magazines"))
    WEAPON.weapon_body.triggers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "triggers"))

    if WEAPON.weapon_body.model.name_length > 0:
        WEAPON.weapon_body.model.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.model.name_length, TAG)

    if WEAPON.weapon_body.animation_graph.name_length > 0:
        WEAPON.weapon_body.animation_graph.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.animation_graph.name_length, TAG)

    if WEAPON.weapon_body.collision_model.name_length > 0:
        WEAPON.weapon_body.collision_model.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.collision_model.name_length, TAG)

    if WEAPON.weapon_body.physics.name_length > 0:
        WEAPON.weapon_body.physics.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.physics.name_length, TAG)

    if WEAPON.weapon_body.modifier_shader.name_length > 0:
        WEAPON.weapon_body.modifier_shader.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.modifier_shader.name_length, TAG)

    if WEAPON.weapon_body.creation_effect.name_length > 0:
        WEAPON.weapon_body.creation_effect.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.creation_effect.name_length, TAG)

    if WEAPON.weapon_body.material_effects.name_length > 0:
        WEAPON.weapon_body.material_effects.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.material_effects.name_length, TAG)

    if WEAPON.weapon_body.collision_sound.name_length > 0:
        WEAPON.weapon_body.collision_sound.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.collision_sound.name_length, TAG)

    if WEAPON.weapon_body.detonating_effect.name_length > 0:
        WEAPON.weapon_body.detonating_effect.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.detonating_effect.name_length, TAG)

    if WEAPON.weapon_body.detonation_effect.name_length > 0:
        WEAPON.weapon_body.detonation_effect.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.detonation_effect.name_length, TAG)

    if WEAPON.weapon_body.ready_effect.name_length > 0:
        WEAPON.weapon_body.ready_effect.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.ready_effect.name_length, TAG)

    if WEAPON.weapon_body.overheated.name_length > 0:
        WEAPON.weapon_body.overheated.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.overheated.name_length, TAG)

    if WEAPON.weapon_body.detonation.name_length > 0:
        WEAPON.weapon_body.detonation.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.detonation.name_length, TAG)

    if WEAPON.weapon_body.player_melee_damage.name_length > 0:
        WEAPON.weapon_body.player_melee_damage.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.player_melee_damage.name_length, TAG)

    if WEAPON.weapon_body.player_melee_response.name_length > 0:
        WEAPON.weapon_body.player_melee_response.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.player_melee_response.name_length, TAG)

    if WEAPON.weapon_body.actor_firing_parameters.name_length > 0:
        WEAPON.weapon_body.actor_firing_parameters.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.actor_firing_parameters.name_length, TAG)

    if WEAPON.weapon_body.light_power_on_effect.name_length > 0:
        WEAPON.weapon_body.light_power_on_effect.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.light_power_on_effect.name_length, TAG)

    if WEAPON.weapon_body.light_power_off_effect.name_length > 0:
        WEAPON.weapon_body.light_power_off_effect.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.light_power_off_effect.name_length, TAG)

    if WEAPON.weapon_body.first_person_model.name_length > 0:
        WEAPON.weapon_body.first_person_model.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.first_person_model.name_length, TAG)

    if WEAPON.weapon_body.first_person_animations.name_length > 0:
        WEAPON.weapon_body.first_person_animations.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.first_person_animations.name_length, TAG)

    if WEAPON.weapon_body.hud_interface.name_length > 0:
        WEAPON.weapon_body.hud_interface.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.hud_interface.name_length, TAG)

    if WEAPON.weapon_body.pickup_sound.name_length > 0:
        WEAPON.weapon_body.pickup_sound.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.pickup_sound.name_length, TAG)

    if WEAPON.weapon_body.zoom_in_sound.name_length > 0:
        WEAPON.weapon_body.zoom_in_sound.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.zoom_in_sound.name_length, TAG)

    if WEAPON.weapon_body.zoom_out_sound.name_length > 0:
        WEAPON.weapon_body.zoom_out_sound.name = TAG.read_variable_string(input_stream, WEAPON.weapon_body.zoom_out_sound.name_length, TAG)

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
        ready_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "ready effect")
        overheated_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "overheated")
        detonation_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "detonation")
        player_melee_damage_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "player melee damage")
        player_melee_response_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "player melee response")
        actor_firing_parameters_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "actor firing parameters")
        light_power_on_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "light power on effect")
        light_power_off_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "light power off effect")
        first_person_model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "first person model")
        first_person_animations_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "first person animations")
        hud_interface_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "hud interface")
        pickup_sound_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "pickup sound")
        zoom_in_sound_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "zoom in sound")
        zoom_out_sound_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "zoom out sound")
        WEAPON.weapon_body.model.append_xml_attributes(model_node)
        WEAPON.weapon_body.animation_graph.append_xml_attributes(animation_graph_node)
        WEAPON.weapon_body.collision_model.append_xml_attributes(collision_model_node)
        WEAPON.weapon_body.physics.append_xml_attributes(physics_node)
        WEAPON.weapon_body.modifier_shader.append_xml_attributes(modifier_shader_node)
        WEAPON.weapon_body.creation_effect.append_xml_attributes(creation_effect_node)
        WEAPON.weapon_body.material_effects.append_xml_attributes(material_effects_node)
        WEAPON.weapon_body.collision_sound.append_xml_attributes(collision_sound_node)
        WEAPON.weapon_body.detonating_effect.append_xml_attributes(detonating_effect_node)
        WEAPON.weapon_body.detonation_effect.append_xml_attributes(detonation_effect_node)
        WEAPON.weapon_body.ready_effect.append_xml_attributes(ready_effect_node)
        WEAPON.weapon_body.overheated.append_xml_attributes(overheated_node)
        WEAPON.weapon_body.detonation.append_xml_attributes(detonation_node)
        WEAPON.weapon_body.player_melee_damage.append_xml_attributes(player_melee_damage_node)
        WEAPON.weapon_body.player_melee_response.append_xml_attributes(player_melee_response_node)
        WEAPON.weapon_body.actor_firing_parameters.append_xml_attributes(actor_firing_parameters_node)
        WEAPON.weapon_body.light_power_on_effect.append_xml_attributes(light_power_on_effect_node)
        WEAPON.weapon_body.light_power_off_effect.append_xml_attributes(light_power_off_effect_node)
        WEAPON.weapon_body.first_person_model.append_xml_attributes(first_person_model_node)
        WEAPON.weapon_body.first_person_animations.append_xml_attributes(first_person_animations_node)
        WEAPON.weapon_body.hud_interface.append_xml_attributes(hud_interface_node)
        WEAPON.weapon_body.pickup_sound.append_xml_attributes(pickup_sound_node)
        WEAPON.weapon_body.zoom_in_sound.append_xml_attributes(zoom_in_sound_node)
        WEAPON.weapon_body.zoom_out_sound.append_xml_attributes(zoom_out_sound_node)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, WEAPON.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return WEAPON
