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

import os

from xml.dom import minidom
from ....global_functions import tag_format
from ..file_object.format import ObjectFlags, ObjectFunctionEnum, ResourceTypeEnum
from ..file_object.process_file import read_attachments, read_widgets, read_functions, read_change_colors, read_predicted_resources
from ..file_item.format import ItemFlags, ItemFunctionEnum
from .format import (
    WeaponAsset,
    WeaponFlags,
    SecondaryTriggerModeEnum,
    WeaponFunctionEnum,
    MovementPenalizedEnum,
    WeaponTypeEnum,
    MagazineFlags,
    TriggerFlags,
    PredictionEnum,
    FiringNoiseEnum,
    OverchargedActionEnum,
    DistributionFunctionEnum
    )

XML_OUTPUT = True

def read_weapon_predicted_resources(WEAPON, TAG, input_stream, tag_node, XML_OUTPUT):
    predicted_resources_node = tag_format.get_xml_node(XML_OUTPUT, WEAPON.weapon_predicted_resources_tag_block.count, tag_node, "name", "weapon predicted resources")
    for predicted_resource_idx in range(WEAPON.weapon_predicted_resources_tag_block.count):
        predicted_resource_element_node = None
        if XML_OUTPUT:
            predicted_resource_element_node = TAG.xml_doc.createElement('element')
            predicted_resource_element_node.setAttribute('index', str(predicted_resource_idx))
            predicted_resources_node.appendChild(predicted_resource_element_node)

        predicted_resource = WEAPON.PredictedResource()
        predicted_resource.predicted_resources_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(predicted_resource_element_node, "type", ResourceTypeEnum))
        predicted_resource.resource_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(predicted_resource_element_node, "resource index"))
        predicted_resource.tag_index = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(predicted_resource_element_node, "tag index"))

        WEAPON.weapon_predicted_resources.append(predicted_resource)

def read_magazines(WEAPON, TAG, input_stream, tag_node, XML_OUTPUT):
    magazines_stat_node = tag_format.get_xml_node(XML_OUTPUT, WEAPON.magazines_tag_block.count, tag_node, "name", "magazines")
    for magazine_idx in range(WEAPON.magazines_tag_block.count):
        magazine_element_node = None
        if XML_OUTPUT:
            magazine_element_node = TAG.xml_doc.createElement('element')
            magazine_element_node.setAttribute('index', str(magazine_idx))
            magazines_stat_node.appendChild(magazine_element_node)

        magazine_stats = WEAPON.MagazineStats()
        magazine_stats.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(magazine_element_node, "flags", MagazineFlags))
        magazine_stats.rounds_recharged = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(magazine_element_node, "rounds recharged"))
        magazine_stats.rounds_total_initial = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(magazine_element_node, "rounds total initial"))
        magazine_stats.rounds_total_maximum = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(magazine_element_node, "rounds total maximum"))
        magazine_stats.rounds_loaded_maximum = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(magazine_element_node, "rounds loaded maximum"))
        input_stream.read(8) # Padding?
        magazine_stats.reload_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(magazine_element_node, "reload time"))
        magazine_stats.rounds_reloaded = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(magazine_element_node, "rounds reloaded"))
        input_stream.read(2) # Padding?
        magazine_stats.chamber_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(magazine_element_node, "chamber time"))
        input_stream.read(24) # Padding?
        magazine_stats.reloading_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(magazine_element_node, "reloading effect"))
        magazine_stats.chambering_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(magazine_element_node, "chambering effect"))
        input_stream.read(12) # Padding?
        magazine_stats.magazines_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(magazine_element_node, "magazines"))

        WEAPON.magazines.append(magazine_stats)

    for magazine_stat_idx, magazine_stats in enumerate(WEAPON.magazines):
        magazine_stats_element_node = None
        if XML_OUTPUT:
            magazine_stats_element_node = magazines_stat_node.childNodes[magazine_stat_idx]

        if magazine_stats.reloading_effect.name_length > 0:
            magazine_stats.reloading_effect.name = TAG.read_variable_string(input_stream, magazine_stats.reloading_effect.name_length, TAG)

        if magazine_stats.chambering_effect.name_length > 0:
            magazine_stats.chambering_effect.name = TAG.read_variable_string(input_stream, magazine_stats.chambering_effect.name_length, TAG)

        if XML_OUTPUT:
            reloading_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, magazine_stats_element_node, "name", "reloading effect")
            chambering_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, magazine_stats_element_node, "name", "chambering effect")
            magazine_stats.reloading_effect.append_xml_attributes(reloading_effect_node)
            magazine_stats.chambering_effect.append_xml_attributes(chambering_effect_node)

        magazine_stats.magazines = []
        magazines_node = tag_format.get_xml_node(XML_OUTPUT, magazine_stats.magazines_tag_block.count, magazine_stats_element_node, "name", "magazines")
        for magazine_idx in range(magazine_stats.magazines_tag_block.count):
            magazine_element_node = None
            if XML_OUTPUT:
                magazine_element_node = TAG.xml_doc.createElement('element')
                magazine_element_node.setAttribute('index', str(magazine_idx))
                magazines_node.appendChild(magazine_element_node)

            magazine = WEAPON.Magazine()
            magazine.rounds = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(magazine_element_node, "rounds"))
            input_stream.read(10) # Padding?
            magazine.equipment = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(magazine_element_node, "equipment"))

            magazine_stats.magazines.append(magazine)

        for magazines_idx, magazine in enumerate(magazine_stats.magazines):
            magazines_element_node = None
            if XML_OUTPUT:
                magazines_element_node = magazines_node.childNodes[magazines_idx]

            if magazine.equipment.name_length > 0:
                magazine.equipment.name = TAG.read_variable_string(input_stream, magazine.equipment.name_length, TAG)

            if XML_OUTPUT:
                equipment_node = tag_format.get_xml_node(XML_OUTPUT, 1, magazines_element_node, "name", "equipment")
                magazine.equipment.append_xml_attributes(equipment_node)

def read_triggers(WEAPON, TAG, input_stream, tag_node, XML_OUTPUT):
    triggers_node = tag_format.get_xml_node(XML_OUTPUT, WEAPON.triggers_tag_block.count, tag_node, "name", "triggers")
    for trigger_idx in range(WEAPON.triggers_tag_block.count):
        trigger_element_node = None
        if XML_OUTPUT:
            trigger_element_node = TAG.xml_doc.createElement('element')
            trigger_element_node.setAttribute('index', str(trigger_idx))
            triggers_node.appendChild(trigger_element_node)

        trigger = WEAPON.Trigger()
        trigger.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(trigger_element_node, "flags", TriggerFlags))
        trigger.rounds_per_second = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(trigger_element_node, "rounds per second"))
        trigger.firing_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(trigger_element_node, "firing acceleration time"))
        trigger.firing_deceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(trigger_element_node, "firing deceleration time"))
        trigger.blurred_rate_of_fire = TAG.read_float(input_stream, TAG, tag_format.XMLData(trigger_element_node, "blurred rate of fire"))
        input_stream.read(8) # Padding?
        trigger.magazine = TAG.read_block_index_signed_short(input_stream, TAG, tag_format.XMLData(trigger_element_node, "magazine", None, WEAPON.magazines_tag_block.count, "weapon_magazine_block"))
        trigger.rounds_per_shot = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(trigger_element_node, "rounds per shot"))
        trigger.minimum_rounds_loaded = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(trigger_element_node, "minimum rounds loaded"))
        trigger.rounds_between_tracers = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(trigger_element_node, "rounds between tracers"))
        input_stream.read(4) # Padding?
        trigger.prediction_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(trigger_element_node, "prediction type", PredictionEnum))
        trigger.firing_noise = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(trigger_element_node, "firing noise", FiringNoiseEnum))
        trigger.error = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(trigger_element_node, "error"))
        trigger.error_acceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(trigger_element_node, "error acceleration time"))
        trigger.error_deceleration_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(trigger_element_node, "error deceleration time"))
        input_stream.read(8) # Padding?
        trigger.charging_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(trigger_element_node, "charging time"))
        trigger.charged_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(trigger_element_node, "charged time"))
        trigger.overcharged_action = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(trigger_element_node, "overcharged action", OverchargedActionEnum))
        input_stream.read(2) # Padding?
        trigger.charged_illumination = TAG.read_float(input_stream, TAG, tag_format.XMLData(trigger_element_node, "charged illumination"))
        trigger.spew_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(trigger_element_node, "spew time"))
        trigger.charging_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(trigger_element_node, "charging effect"))
        trigger.distribution_function = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(trigger_element_node, "distribution function", DistributionFunctionEnum))
        trigger.projectiles_per_shot = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(trigger_element_node, "projectiles per shot"))
        trigger.distribution_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(trigger_element_node, "distribution angle"))
        input_stream.read(4) # Padding?
        trigger.minimum_error = TAG.read_degree(input_stream, TAG, tag_format.XMLData(trigger_element_node, "minimum error"))
        trigger.error_angle = TAG.read_degree_2d(input_stream, TAG, tag_format.XMLData(trigger_element_node, "error angle"))
        trigger.first_person_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(trigger_element_node, "first person offset"))
        input_stream.read(4) # Padding?
        trigger.projectile = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(trigger_element_node, "projectile"))
        trigger.ejection_port_recovery_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(trigger_element_node, "ejection port recovery time"))
        trigger.illumination_recovery_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(trigger_element_node, "illumination recovery time"))
        input_stream.read(12) # Padding?
        trigger.heat_generated_per_round = TAG.read_float(input_stream, TAG, tag_format.XMLData(trigger_element_node, "heat generated per round"))
        trigger.age_generated_per_round = TAG.read_float(input_stream, TAG, tag_format.XMLData(trigger_element_node, "age generated per round"))
        input_stream.read(4) # Padding?
        trigger.overload_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(trigger_element_node, "overload time"))
        input_stream.read(64) # Padding?
        trigger.firing_effects_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(trigger_element_node, "firing effects"))

        WEAPON.triggers.append(trigger)

    for trigger_idx, trigger in enumerate(WEAPON.triggers):
        trigger_element_node = None
        if XML_OUTPUT:
            trigger_element_node = triggers_node.childNodes[trigger_idx]

        if trigger.charging_effect.name_length > 0:
            trigger.charging_effect.name = TAG.read_variable_string(input_stream, trigger.charging_effect.name_length, TAG)

        if trigger.projectile.name_length > 0:
            trigger.projectile.name = TAG.read_variable_string(input_stream, trigger.projectile.name_length, TAG)

        if XML_OUTPUT:
            charging_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, trigger_element_node, "name", "charging effect")
            projectile_node = tag_format.get_xml_node(XML_OUTPUT, 1, trigger_element_node, "name", "projectile")
            trigger.charging_effect.append_xml_attributes(charging_effect_node)
            trigger.projectile.append_xml_attributes(projectile_node)

        trigger.firing_effects = []
        firing_effects_node = tag_format.get_xml_node(XML_OUTPUT, trigger.firing_effects_tag_block.count, trigger_element_node, "name", "firing effects")
        for firing_effect_idx in range(trigger.firing_effects_tag_block.count):
            firing_effect_element_node = None
            if XML_OUTPUT:
                firing_effect_element_node = TAG.xml_doc.createElement('element')
                firing_effect_element_node.setAttribute('index', str(firing_effect_idx))
                firing_effects_node.appendChild(firing_effect_element_node)

            firing_effect = WEAPON.FiringEffect()
            firing_effect.shot_count_lower_bound = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(firing_effect_element_node, "shot count lower bound"))
            firing_effect.shot_count_upper_bound = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(firing_effect_element_node, "shot count upper bound"))
            input_stream.read(32) # Padding?
            firing_effect.firing_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(firing_effect_element_node, "firing effect"))
            firing_effect.misfire_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(firing_effect_element_node, "misfire effect"))
            firing_effect.empty_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(firing_effect_element_node, "empty effect"))
            firing_effect.firing_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(firing_effect_element_node, "firing damage"))
            firing_effect.misfire_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(firing_effect_element_node, "misfire damage"))
            firing_effect.empty_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(firing_effect_element_node, "empty damage"))

            trigger.firing_effects.append(firing_effect)

        for firing_effect_idx, firing_effect in enumerate(trigger.firing_effects):
            firing_effect_element_node = None
            if XML_OUTPUT:
                firing_effect_element_node = firing_effects_node.childNodes[firing_effect_idx]

            if firing_effect.firing_effect.name_length > 0:
                firing_effect.firing_effect.name = TAG.read_variable_string(input_stream, firing_effect.firing_effect.name_length, TAG)

            if firing_effect.misfire_effect.name_length > 0:
                firing_effect.misfire_effect.name = TAG.read_variable_string(input_stream, firing_effect.misfire_effect.name_length, TAG)

            if firing_effect.empty_effect.name_length > 0:
                firing_effect.empty_effect.name = TAG.read_variable_string(input_stream, firing_effect.empty_effect.name_length, TAG)

            if firing_effect.firing_damage.name_length > 0:
                firing_effect.firing_damage.name = TAG.read_variable_string(input_stream, firing_effect.firing_damage.name_length, TAG)

            if firing_effect.misfire_damage.name_length > 0:
                firing_effect.misfire_damage.name = TAG.read_variable_string(input_stream, firing_effect.misfire_damage.name_length, TAG)

            if firing_effect.empty_damage.name_length > 0:
                firing_effect.empty_damage.name = TAG.read_variable_string(input_stream, firing_effect.empty_damage.name_length, TAG)

            if XML_OUTPUT:
                firing_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, firing_effect_element_node, "name", "firing effect")
                misfire_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, firing_effect_element_node, "name", "misfire effect")
                empty_effect_node = tag_format.get_xml_node(XML_OUTPUT, 1, firing_effect_element_node, "name", "empty effect")
                firing_damage_node = tag_format.get_xml_node(XML_OUTPUT, 1, firing_effect_element_node, "name", "firing damage")
                misfire_damage_node = tag_format.get_xml_node(XML_OUTPUT, 1, firing_effect_element_node, "name", "misfire damage")
                empty_damage_node = tag_format.get_xml_node(XML_OUTPUT, 1, firing_effect_element_node, "name", "empty damage")
                firing_effect.firing_effect.append_xml_attributes(firing_effect_node)
                firing_effect.misfire_effect.append_xml_attributes(misfire_effect_node)
                firing_effect.empty_effect.append_xml_attributes(empty_effect_node)
                firing_effect.firing_damage.append_xml_attributes(firing_damage_node)
                firing_effect.misfire_damage.append_xml_attributes(misfire_damage_node)
                firing_effect.empty_damage.append_xml_attributes(empty_damage_node)

def initilize_weapon(WEAPON):
    WEAPON.attachments = []
    WEAPON.widgets = []
    WEAPON.functions = []
    WEAPON.change_colors = []
    WEAPON.object_predicted_resources = []
    WEAPON.weapon_predicted_resources = []
    WEAPON.magazines = []
    WEAPON.triggers = []

def read_weapon_body(WEAPON, TAG, input_stream, tag_node, XML_OUTPUT):
    input_stream.read(2) # Padding?
    WEAPON.object_flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ObjectFlags))
    WEAPON.bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    WEAPON.bounding_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "bounding offset"))
    WEAPON.origin_offset = TAG.read_point_3d(input_stream, TAG, tag_format.XMLData(tag_node, "origin offset"))
    WEAPON.acceleration_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "acceleration scale"))
    input_stream.read(4) # Padding?
    WEAPON.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    WEAPON.animation_graph = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "animation graph"))
    input_stream.read(40) # Padding?
    WEAPON.collision_model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision model"))
    WEAPON.physics = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "physics"))
    WEAPON.modifier_shader = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "modifier shader"))
    WEAPON.creation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "creation effect"))
    input_stream.read(84) # Padding?
    WEAPON.render_bounding_radius = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "render bounding radius"))
    WEAPON.object_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", ObjectFunctionEnum))
    WEAPON.object_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", ObjectFunctionEnum))
    WEAPON.object_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", ObjectFunctionEnum))
    WEAPON.object_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", ObjectFunctionEnum))
    input_stream.read(44) # Padding?
    WEAPON.hud_text_message_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud text message index"))
    WEAPON.forced_shader_permutation_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "forced shader_permutation index"))
    WEAPON.attachments_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "attachments"))
    WEAPON.widgets_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "widgets"))
    WEAPON.functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "functions"))
    WEAPON.change_colors_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "change colors"))
    WEAPON.predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "predicted resources"))
    WEAPON.item_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ItemFlags))
    WEAPON.message_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "message index"))
    WEAPON.sort_order = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "sort order"))
    WEAPON.scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "scale"))
    WEAPON.hud_message_value_scale = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "hud message value scale"))
    input_stream.read(18) # Padding?
    WEAPON.item_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", ItemFunctionEnum))
    WEAPON.item_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", ItemFunctionEnum))
    WEAPON.item_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", ItemFunctionEnum))
    WEAPON.item_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", ItemFunctionEnum))
    input_stream.read(164) # Padding?
    WEAPON.material_effects = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "material effects"))
    WEAPON.collision_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "collision sound"))
    input_stream.read(120) # Padding?
    WEAPON.detonation_delay = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "detonation delay"))
    WEAPON.detonating_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detonating effect"))
    WEAPON.detonation_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detonation effect"))
    WEAPON.weapon_flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(tag_node, "flags", WeaponFlags))
    WEAPON.label = TAG.read_string32(input_stream, TAG, tag_format.XMLData(tag_node, "label"))
    WEAPON.secondary_trigger_mode = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "secondary trigger mode", SecondaryTriggerModeEnum))
    WEAPON.maximum_alternate_shots_loaded = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "maximum alternate shots loaded"))
    WEAPON.weapon_a_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "a in", WeaponFunctionEnum))
    WEAPON.weapon_b_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "b in", WeaponFunctionEnum))
    WEAPON.weapon_c_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "c in", WeaponFunctionEnum))
    WEAPON.weapon_d_in = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "d in", WeaponFunctionEnum))
    WEAPON.ready_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "ready time"))
    WEAPON.ready_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "ready effect"))
    WEAPON.heat_recovery_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "heat recovery threshold"))
    WEAPON.overheated_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "overheated threshold"))
    WEAPON.heat_detonation_threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "heat detonation threshold"))
    WEAPON.heat_detonation_fraction = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "heat detonation fraction"))
    WEAPON.heat_loss_per_second = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "heat loss per second"))
    WEAPON.heat_illumination = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "heat illumination"))
    input_stream.read(16) # Padding?
    WEAPON.overheated = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "overheated"))
    WEAPON.detonation = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "detonation"))
    WEAPON.player_melee_damage = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "player melee damage"))
    WEAPON.player_melee_response = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "player melee response"))
    input_stream.read(8) # Padding?
    WEAPON.actor_firing_parameters = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "actor firing parameters"))
    WEAPON.near_reticle_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "near reticle range"))
    WEAPON.far_reticle_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "far reticle range"))
    WEAPON.intersection_reticle_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "intersection reticle range"))
    input_stream.read(2) # Padding?
    WEAPON.magnification_levels = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "magnification levels"))
    WEAPON.magnification_range = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "magnification range"))
    WEAPON.autoaim_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "autoaim angle"))
    WEAPON.autoaim_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "autoaim range"))
    WEAPON.magnetism_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "magnetism angle"))
    WEAPON.magnetism_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "magnetism range"))
    WEAPON.deviation_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "deviation angle"))
    input_stream.read(4) # Padding?
    WEAPON.movement_penalized = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "movement penalized", MovementPenalizedEnum))
    input_stream.read(2) # Padding?
    WEAPON.forward_movement_penalty = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "forward movement penalty"))
    WEAPON.sideways_movement_penalty = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "sideways movement penalty"))
    input_stream.read(4) # Padding?
    WEAPON.minimum_target_range = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "minimum target range"))
    WEAPON.looking_time_modifier = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "looking time modifier"))
    input_stream.read(4) # Padding?
    WEAPON.light_power_on_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "light power on time"))
    WEAPON.light_power_off_time = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "light power off time"))
    WEAPON.light_power_on_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "light power on effect"))
    WEAPON.light_power_off_effect = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "light power off effect"))
    WEAPON.age_heat_recovery_penalty = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "age heat recovery penalty"))
    WEAPON.age_rate_of_fire_penalty = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "age rate of fire penalty"))
    WEAPON.age_misfire_start = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "age misfire start"))
    WEAPON.age_misfire_chance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "age misfire chance"))
    input_stream.read(12) # Padding?
    WEAPON.first_person_model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "first person model"))
    WEAPON.first_person_animations = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "first person animations"))
    input_stream.read(4) # Padding?
    WEAPON.hud_interface = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "hud interface"))
    WEAPON.pickup_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "pickup sound"))
    WEAPON.zoom_in_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "zoom in sound"))
    WEAPON.zoom_out_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "zoom out sound"))
    input_stream.read(12) # Padding?
    WEAPON.active_camo_ding = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "active camo ding"))
    WEAPON.active_camo_regrowth_rate = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "active camo regrowth rate"))
    input_stream.read(14) # Padding?
    WEAPON.weapon_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "weapon type", WeaponTypeEnum))
    WEAPON.weapon_predicted_resources_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "weapon predicted resources"))
    WEAPON.magazines_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "magazines"))
    WEAPON.triggers_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "triggers"))

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    WEAPON = WeaponAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    WEAPON.header = TAG.Header().read(input_stream, TAG)
    tags_folder = "%stags%s" % (os.sep, os.sep)
    if tags_folder in input_stream.name:
        WEAPON.header.local_path = input_stream.name.split("tags%s" % os.sep)[1].rsplit(".", 1)[0]
    else:
        WEAPON.header.local_path = input_stream.name.rsplit(".", 1)[0]

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    initilize_weapon(WEAPON)
    read_weapon_body(WEAPON, TAG, input_stream, tag_node, XML_OUTPUT)

    if WEAPON.model.name_length > 0:
        WEAPON.model.name = TAG.read_variable_string(input_stream, WEAPON.model.name_length, TAG)

    if WEAPON.animation_graph.name_length > 0:
        WEAPON.animation_graph.name = TAG.read_variable_string(input_stream, WEAPON.animation_graph.name_length, TAG)

    if WEAPON.collision_model.name_length > 0:
        WEAPON.collision_model.name = TAG.read_variable_string(input_stream, WEAPON.collision_model.name_length, TAG)

    if WEAPON.physics.name_length > 0:
        WEAPON.physics.name = TAG.read_variable_string(input_stream, WEAPON.physics.name_length, TAG)

    if WEAPON.modifier_shader.name_length > 0:
        WEAPON.modifier_shader.name = TAG.read_variable_string(input_stream, WEAPON.modifier_shader.name_length, TAG)

    if WEAPON.creation_effect.name_length > 0:
        WEAPON.creation_effect.name = TAG.read_variable_string(input_stream, WEAPON.creation_effect.name_length, TAG)

    read_attachments(WEAPON, TAG, input_stream, tag_node, XML_OUTPUT)
    read_widgets(WEAPON, TAG, input_stream, tag_node, XML_OUTPUT)
    read_functions(WEAPON, TAG, input_stream, tag_node, XML_OUTPUT)
    read_change_colors(WEAPON, TAG, input_stream, tag_node, XML_OUTPUT)
    read_predicted_resources(WEAPON, TAG, input_stream, tag_node, XML_OUTPUT)

    if WEAPON.material_effects.name_length > 0:
        WEAPON.material_effects.name = TAG.read_variable_string(input_stream, WEAPON.material_effects.name_length, TAG)

    if WEAPON.collision_sound.name_length > 0:
        WEAPON.collision_sound.name = TAG.read_variable_string(input_stream, WEAPON.collision_sound.name_length, TAG)

    if WEAPON.detonating_effect.name_length > 0:
        WEAPON.detonating_effect.name = TAG.read_variable_string(input_stream, WEAPON.detonating_effect.name_length, TAG)

    if WEAPON.detonation_effect.name_length > 0:
        WEAPON.detonation_effect.name = TAG.read_variable_string(input_stream, WEAPON.detonation_effect.name_length, TAG)

    if WEAPON.ready_effect.name_length > 0:
        WEAPON.ready_effect.name = TAG.read_variable_string(input_stream, WEAPON.ready_effect.name_length, TAG)

    if WEAPON.overheated.name_length > 0:
        WEAPON.overheated.name = TAG.read_variable_string(input_stream, WEAPON.overheated.name_length, TAG)

    if WEAPON.detonation.name_length > 0:
        WEAPON.detonation.name = TAG.read_variable_string(input_stream, WEAPON.detonation.name_length, TAG)

    if WEAPON.player_melee_damage.name_length > 0:
        WEAPON.player_melee_damage.name = TAG.read_variable_string(input_stream, WEAPON.player_melee_damage.name_length, TAG)

    if WEAPON.player_melee_response.name_length > 0:
        WEAPON.player_melee_response.name = TAG.read_variable_string(input_stream, WEAPON.player_melee_response.name_length, TAG)

    if WEAPON.actor_firing_parameters.name_length > 0:
        WEAPON.actor_firing_parameters.name = TAG.read_variable_string(input_stream, WEAPON.actor_firing_parameters.name_length, TAG)

    if WEAPON.light_power_on_effect.name_length > 0:
        WEAPON.light_power_on_effect.name = TAG.read_variable_string(input_stream, WEAPON.light_power_on_effect.name_length, TAG)

    if WEAPON.light_power_off_effect.name_length > 0:
        WEAPON.light_power_off_effect.name = TAG.read_variable_string(input_stream, WEAPON.light_power_off_effect.name_length, TAG)

    if WEAPON.first_person_model.name_length > 0:
        WEAPON.first_person_model.name = TAG.read_variable_string(input_stream, WEAPON.first_person_model.name_length, TAG)

    if WEAPON.first_person_animations.name_length > 0:
        WEAPON.first_person_animations.name = TAG.read_variable_string(input_stream, WEAPON.first_person_animations.name_length, TAG)

    if WEAPON.hud_interface.name_length > 0:
        WEAPON.hud_interface.name = TAG.read_variable_string(input_stream, WEAPON.hud_interface.name_length, TAG)

    if WEAPON.pickup_sound.name_length > 0:
        WEAPON.pickup_sound.name = TAG.read_variable_string(input_stream, WEAPON.pickup_sound.name_length, TAG)

    if WEAPON.zoom_in_sound.name_length > 0:
        WEAPON.zoom_in_sound.name = TAG.read_variable_string(input_stream, WEAPON.zoom_in_sound.name_length, TAG)

    if WEAPON.zoom_out_sound.name_length > 0:
        WEAPON.zoom_out_sound.name = TAG.read_variable_string(input_stream, WEAPON.zoom_out_sound.name_length, TAG)

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
        WEAPON.model.append_xml_attributes(model_node)
        WEAPON.animation_graph.append_xml_attributes(animation_graph_node)
        WEAPON.collision_model.append_xml_attributes(collision_model_node)
        WEAPON.physics.append_xml_attributes(physics_node)
        WEAPON.modifier_shader.append_xml_attributes(modifier_shader_node)
        WEAPON.creation_effect.append_xml_attributes(creation_effect_node)
        WEAPON.material_effects.append_xml_attributes(material_effects_node)
        WEAPON.collision_sound.append_xml_attributes(collision_sound_node)
        WEAPON.detonating_effect.append_xml_attributes(detonating_effect_node)
        WEAPON.detonation_effect.append_xml_attributes(detonation_effect_node)
        WEAPON.ready_effect.append_xml_attributes(ready_effect_node)
        WEAPON.overheated.append_xml_attributes(overheated_node)
        WEAPON.detonation.append_xml_attributes(detonation_node)
        WEAPON.player_melee_damage.append_xml_attributes(player_melee_damage_node)
        WEAPON.player_melee_response.append_xml_attributes(player_melee_response_node)
        WEAPON.actor_firing_parameters.append_xml_attributes(actor_firing_parameters_node)
        WEAPON.light_power_on_effect.append_xml_attributes(light_power_on_effect_node)
        WEAPON.light_power_off_effect.append_xml_attributes(light_power_off_effect_node)
        WEAPON.first_person_model.append_xml_attributes(first_person_model_node)
        WEAPON.first_person_animations.append_xml_attributes(first_person_animations_node)
        WEAPON.hud_interface.append_xml_attributes(hud_interface_node)
        WEAPON.pickup_sound.append_xml_attributes(pickup_sound_node)
        WEAPON.zoom_in_sound.append_xml_attributes(zoom_in_sound_node)
        WEAPON.zoom_out_sound.append_xml_attributes(zoom_out_sound_node)

    read_weapon_predicted_resources(WEAPON, TAG, input_stream, tag_node, XML_OUTPUT)
    read_magazines(WEAPON, TAG, input_stream, tag_node, XML_OUTPUT)
    read_triggers(WEAPON, TAG, input_stream, tag_node, XML_OUTPUT)

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
